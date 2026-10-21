#!/usr/bin/env python3
"""
Trollacos - actualizador de noticias.

Lee los RSS de fuentes.json, se queda con lo mas reciente de cada categoria
y lo escribe dentro de index.html, entre las marcas
<!--NOTICIAS:INICIO--> y <!--NOTICIAS:FIN-->.

Solo usa la libreria estandar de Python (no hay que instalar nada).
Uso:  python scripts/actualizar_noticias.py [ruta_fuentes.json] [ruta_index.html]
"""
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

try:
    from zoneinfo import ZoneInfo
    MADRID = ZoneInfo("Europe/Madrid")
except Exception:  # por si el sistema no tiene zonas horarias
    MADRID = timezone(timedelta(hours=2))

RAIZ = Path(__file__).resolve().parent.parent
FUENTES = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "fuentes.json"
INDEX = Path(sys.argv[2]) if len(sys.argv) > 2 else RAIZ / "index.html"

INICIO, FIN = "<!--NOTICIAS:INICIO-->", "<!--NOTICIAS:FIN-->"
GTA_INICIO, GTA_FIN = "<!--GTA:INICIO-->", "<!--GTA:FIN-->"
RSS = INDEX.parent / "rss.xml"
WEB = "https://trollacos.com"
NS = {
    "media": "http://search.yahoo.com/mrss/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "atom": "http://www.w3.org/2005/Atom",
}
CATEGORIAS = [("videojuegos", "// VIDEOJUEGOS"), ("salseo", "// SALSEO"), ("futbol", "// FÚTBOL EUROPEO"), ("cine", "// CINE Y SERIES")]
ICONOS = {"videojuegos": "🎮", "salseo": "🍿", "futbol": "⚽", "cine": "🎬", "especial": "🌴"}
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def descargar(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; TrollacosBot/1.0; +https://trollacos.com)",
        "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*",
    })
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read()


def texto_limpio(s, maximo=160):
    if not s:
        return ""
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) > maximo:
        s = s[:maximo].rsplit(" ", 1)[0].rstrip(",.;:") + "…"
    return s


def leer_fecha(s):
    if not s:
        return None
    s = s.strip()
    try:
        d = parsedate_to_datetime(s)
    except Exception:
        try:
            d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except Exception:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc)


def primera_imagen(*bloques):
    for b in bloques:
        if b:
            m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', b, re.I)
            if m:
                return html.unescape(m.group(1))
    return ""


def url_valida(u):
    return u if u and re.match(r"^https?://", u.strip(), re.I) else ""


def hijo(el, *nombres):
    for n in nombres:
        x = el.find(n, NS)
        if x is not None:
            return x
    return None


def texto_de(el, *nombres):
    x = hijo(el, *nombres)
    return (x.text or "").strip() if x is not None and x.text else ""


def imagen_de(item, desc, contenido):
    for tag in ("media:content", "media:thumbnail"):
        for m in item.findall(tag, NS):
            u = m.get("url", "")
            tipo = m.get("type", "") or m.get("medium", "")
            if u and (not tipo or "image" in tipo or tipo == "image"):
                return u
    grupo = item.find("media:group", NS)
    if grupo is not None:
        for m in grupo.findall("media:content", NS) + grupo.findall("media:thumbnail", NS):
            if m.get("url"):
                return m.get("url")
    enc = item.find("enclosure")
    if enc is not None and "image" in (enc.get("type") or "image"):
        if enc.get("url"):
            return enc.get("url")
    return primera_imagen(contenido, desc)


def parsear(xml_bytes, fuente):
    raiz = ET.fromstring(xml_bytes)
    noticias = []
    items = raiz.findall("./channel/item") or raiz.findall(".//item")
    if items:  # RSS 2.0
        for it in items:
            desc = texto_de(it, "description")
            contenido = texto_de(it, "content:encoded")
            titulo = texto_limpio(texto_de(it, "title"), 400)
            medio_origen = texto_de(it, "source")  # agregadores tipo Google Noticias
            resumen = texto_limpio(desc or contenido)
            if medio_origen:
                sufijo = " - " + medio_origen
                if titulo.endswith(sufijo):
                    titulo = titulo[: -len(sufijo)]
                resumen = ""
            noticias.append({
                "titulo": texto_limpio(titulo, 140),
                "enlace": texto_de(it, "link") or texto_de(it, "guid"),
                "resumen": resumen,
                "imagen": imagen_de(it, desc, contenido),
                "fecha": leer_fecha(texto_de(it, "pubDate", "dc:date")),
                "medio_origen": medio_origen,
            })
    else:  # Atom
        for en in raiz.findall("atom:entry", NS):
            enlace = ""
            for l in en.findall("atom:link", NS):
                if l.get("rel", "alternate") == "alternate" and l.get("href"):
                    enlace = l.get("href")
                    break
            desc = texto_de(en, "atom:summary")
            contenido = texto_de(en, "atom:content")
            noticias.append({
                "titulo": texto_limpio(texto_de(en, "atom:title"), 140),
                "enlace": enlace,
                "resumen": texto_limpio(desc or contenido),
                "imagen": imagen_de(en, desc, contenido),
                "fecha": leer_fecha(texto_de(en, "atom:published", "atom:updated")),
                "medio_origen": "",
            })
    validas = []
    for n in noticias:
        n["enlace"] = url_valida(n["enlace"])
        n["imagen"] = url_valida(n["imagen"])
        if n["titulo"] and n["enlace"]:
            origen = n.pop("medio_origen", "")
            n["medio"] = texto_limpio(origen, 40) if origen else fuente["nombre"]
            n["categoria"] = fuente["categoria"]
            validas.append(n)
    return validas


# ---------- Fotos para noticias que llegan sin imagen (p. ej. Google Noticias) ----------
NAVEGADOR = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def pedir(url, datos=None, timeout=12):
    cab = {"User-Agent": NAVEGADOR, "Accept-Language": "es-ES,es;q=0.9"}
    if datos is not None:
        cab["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8"
    req = urllib.request.Request(url, data=datos, headers=cab)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.geturl(), r.read(600_000).decode("utf-8", "replace")


def enlace_real_google(url):
    """Convierte un enlace news.google.com/rss/articles/... en el enlace del medio."""
    m = re.search(r"news\.google\.com/(?:rss/)?articles/([^?/#]+)", url)
    if not m:
        return url
    gid = m.group(1)
    firma = sello = None
    for intento, base in enumerate(("articles", "rss/articles", "articles")):
        try:
            _, pagina = pedir(f"https://news.google.com/{base}/{gid}")
            firma = re.search(r'data-n-a-sg="([^"]+)"', pagina)
            sello = re.search(r'data-n-a-ts="([^"]+)"', pagina)
            if firma and sello:
                break
        except Exception:
            pass
        time.sleep(1.5 * (intento + 1))
    if not firma or not sello:
        return ""
    peticion = ('["garturlreq",[["X","X",["X","X"],null,null,1,1,"ES:es",null,1,null,null,null,null,null,0,1],'
                '"X","X",1,[1,1,1],1,1,null,0,0,null,0],'
                f'"{gid}",{sello.group(1)},"{firma.group(1)}"]')
    freq = json.dumps([[["Fbv4je", peticion, None, "generic"]]])
    datos = urllib.parse.urlencode({"f.req": freq}).encode()
    for intento in range(3):
        try:
            _, resp = pedir("https://news.google.com/_/DotsSplashUi/data/batchexecute", datos)
            bloque = json.loads(resp.split("\n\n", 1)[1])[:-2]
            return json.loads(bloque[0][2])[1]
        except Exception:
            time.sleep(2 * (intento + 1))
    return ""


def foto_de_pagina(url):
    final, pagina = pedir(url)
    cabeza = pagina[: pagina.lower().find("</head>") if "</head>" in pagina.lower() else 200_000]
    for prop in ("og:image", "twitter:image", "og:image:url", "twitter:image:src"):
        for patron in (rf'<meta[^>]+(?:property|name)=["\']{prop}["\'][^>]*content=["\']([^"\']+)["\']',
                       rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]*(?:property|name)=["\']{prop}["\']'):
            m = re.search(patron, cabeza, re.I)
            if m:
                u = urllib.parse.urljoin(final, html.unescape(m.group(1)).strip())
                if url_valida(u) and not re.search(r"logo|favicon|default|placeholder", u, re.I):
                    return u
    return ""


def completar_fotos(noticias):
    """Busca la foto de portada de cada noticia sin imagen (en paralelo y sin romper nada si falla)."""
    sin_foto = [n for n in noticias if not n["imagen"]]
    if not sin_foto:
        return

    def una(n):
        paso = "google"
        try:
            real = enlace_real_google(n["enlace"])
            paso = "pagina " + (real or "")[:70]
            if real:
                if "news.google.com" in n["enlace"]:
                    n["enlace"] = real  # enlace directo al medio, mas limpio
                n["imagen"] = foto_de_pagina(real)
            if not n["imagen"]:
                print(f"::warning::sin foto ({paso or 'google vacio'}): {n['titulo'][:40]}")
        except Exception as ex:
            print(f"::warning::sin foto ({paso}): {type(ex).__name__} {str(ex)[:80]}")

    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(una, sin_foto))
    print(f"Fotos encontradas: {sum(1 for n in sin_foto if n['imagen'])} de {len(sin_foto)}")


def fecha_bonita(d):
    d = d.astimezone(MADRID)
    return f"{d.day} {MESES[d.month - 1]}, {d:%H:%M}"


def tarjeta(n):
    e = lambda s: html.escape(s or "", quote=True)
    cat = n.get("categoria", "videojuegos")
    if n["imagen"]:
        img = (f'<img src="{e(n["imagen"])}" alt="" loading="lazy" referrerpolicy="no-referrer" '
               f'onerror="this.remove()">')
    else:
        img = f'<span class="mini mini-{e(cat)}" aria-hidden="true">{ICONOS.get(cat, "🕹️")}</span>'
    
    cuando = f' · {fecha_bonita(n["fecha"])}' if n["fecha"] else ""
    resumen = f'<p>{e(n["resumen"])}</p>' if n["resumen"] else ""
    return (f'      <article class="news-card"><a href="{e(n["enlace"])}" target="_blank" rel="noopener nofollow">'
            f'{img}<div><span class="src">{e(n["medio"])}{cuando}</span><h4>{e(n["titulo"])}</h4>{resumen}</div></a></article>')


def clave_de(n):
    return re.sub(r"\W+", "", n["titulo"].lower())[:60]


def menciona(n, palabras):
    texto = " " + re.sub(r"\s+", " ", (n["titulo"] + " " + n["resumen"]).lower()) + " "
    return any(re.search(r"(?<![a-z0-9])" + re.escape(p.lower()) + r"(?![a-z0-9])", texto) for p in palabras)


def elegir(noticias, cfg, excluir=()):
    ahora = datetime.now(timezone.utc)
    limite = ahora - timedelta(days=cfg.get("dias_maximos", 3))
    vistos, por_medio, elegidas = set(excluir), {}, []
    viejo = datetime(1970, 1, 1, tzinfo=timezone.utc)
    for n in sorted(noticias, key=lambda n: n["fecha"] or viejo, reverse=True):
        if n["fecha"] and n["fecha"] < limite:
            continue
        if n["fecha"] and n["fecha"] > ahora + timedelta(hours=2):
            n["fecha"] = ahora
        clave = clave_de(n)
        if clave in vistos or n["enlace"] in vistos:
            continue
        if por_medio.get(n["medio"], 0) >= cfg.get("maximo_por_medio", 3):
            continue
        vistos.update({clave, n["enlace"]})
        por_medio[n["medio"]] = por_medio.get(n["medio"], 0) + 1
        elegidas.append(n)
        if len(elegidas) >= cfg.get("noticias", cfg.get("noticias_por_categoria", 10)):
            break
    return elegidas


def escribir_rss(noticias, sello):
    """Feed propio de Trollacos (lo usa el boletin de correo)."""
    from email.utils import format_datetime
    e = lambda t: html.escape(t or "", quote=True)
    items = []
    for n in noticias:
        fecha = format_datetime(n["fecha"]) if n["fecha"] else format_datetime(sello)
        desc = f'{n["medio"]}. {n["resumen"]}' if n["resumen"] else n["medio"]
        img = (f'\n      <enclosure url="{e(n["imagen"])}" type="image/jpeg" length="0"/>') if n["imagen"] else ""
        items.append(f"""    <item>
      <title>{e(n["titulo"])}</title>
      <link>{e(n["enlace"])}</link>
      <guid isPermaLink="false">{e(n["enlace"])}</guid>
      <pubDate>{fecha}</pubDate>
      <description>{e(desc)}</description>{img}
    </item>""")
    RSS.write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Trollacos · Lo último</title>
    <link>{WEB}/</link>
    <atom:link href="{WEB}/rss.xml" rel="self" type="application/rss+xml"/>
    <description>Humor, videojuegos y cine desde 2012. Las noticias del día, con guasa.</description>
    <language>es-es</language>
    <lastBuildDate>{format_datetime(sello)}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
""", encoding="utf-8")


def main():
    cfg = json.loads(FUENTES.read_text(encoding="utf-8"))
    todas, fallos = [], []
    for f in cfg["fuentes"]:
        try:
            nuevas = parsear(descargar(f["url"]), f)
            print(f"OK    {f['nombre']}: {len(nuevas)} noticias")
            todas += nuevas
        except Exception as ex:
            fallos.append(f["nombre"])
            print(f"FALLO {f['nombre']}: {ex}")

    excluir = [w.lower() for w in cfg.get("excluir_palabras", [])]
    if excluir:
        todas = [n for n in todas if not menciona(n, excluir)]

    if not todas:
        print("No se ha podido leer ninguna fuente: dejo la web como estaba.")
        return 0

    # --- Especial (p. ej. GTA VI): lo que mencione las palabras clave, de cualquier medio ---
    esp_cfg = cfg.get("especial") or {}
    palabras = esp_cfg.get("palabras") or []
    especiales = elegir([n for n in todas if menciona(n, palabras)], esp_cfg) if palabras else []
    usados = {clave_de(n) for n in especiales} | {n["enlace"] for n in especiales}

    columnas, publicadas = [], list(especiales)
    por_columna = []
    for clave, titulo in CATEGORIAS:
        elegidas = elegir([n for n in todas if n["categoria"] == clave], cfg, excluir=usados)
        publicadas += elegidas
        por_columna.append((titulo, elegidas))

    completar_fotos(publicadas)

    for titulo, elegidas in por_columna:
        if elegidas:
            cuerpo = '    <div class="news-list">\n' + "\n".join(tarjeta(n) for n in elegidas) + "\n    </div>"
        else:
            cuerpo = '    <p class="news-empty">Hoy no hay noticias nuevas por aquí. Vuelve luego.</p>'
        columnas.append(f'    <div class="news-col"><h3>{titulo}</h3>\n{cuerpo}\n    </div>')

    sello = datetime.now(MADRID)
    bloque = (f'{INICIO}\n  <p class="news-meta">&gt; Actualizado el {fecha_bonita(sello)}_</p>\n'
              f'  <div class="news-cols">\n' + "\n".join(columnas) + f"\n  </div>\n{FIN}")

    pagina = INDEX.read_text(encoding="utf-8")
    if INICIO not in pagina or FIN not in pagina:
        print("ERROR: no encuentro las marcas de noticias en index.html")
        return 1
    nueva = re.sub(re.escape(INICIO) + r".*?" + re.escape(FIN), lambda _: bloque, pagina, flags=re.S)

    if GTA_INICIO in nueva and GTA_FIN in nueva:
        if especiales:
            cuerpo = '    <div class="news-list">\n' + "\n".join(tarjeta(n) for n in especiales) + "\n    </div>"
        else:
            cuerpo = '    <p class="news-empty">Sin noticias nuevas de Vice City en los últimos días. Volverán pronto.</p>'
        nueva = re.sub(re.escape(GTA_INICIO) + r".*?" + re.escape(GTA_FIN),
                       lambda _: f"{GTA_INICIO}\n{cuerpo}\n{GTA_FIN}", nueva, flags=re.S)

    INDEX.write_text(nueva, encoding="utf-8")
    escribir_rss(publicadas, sello)
    print(f"Web actualizada. Fuentes con fallo: {', '.join(fallos) or 'ninguna'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
