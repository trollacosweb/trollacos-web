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
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
    MADRID = ZoneInfo("Europe/Madrid")
except Exception:  # por si el sistema no tiene zonas horarias
    MADRID = timezone(timedelta(hours=2))

RAIZ = Path(__file__).resolve().parent.parent
FUENTES = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "fuentes.json"
INDEX = Path(sys.argv[2]) if len(sys.argv) > 2 else RAIZ / "index.html"

INICIO, FIN = "<!--NOTICIAS:INICIO-->", "<!--NOTICIAS:FIN-->"
NS = {
    "media": "http://search.yahoo.com/mrss/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "atom": "http://www.w3.org/2005/Atom",
}
CATEGORIAS = [("videojuegos", "// VIDEOJUEGOS"), ("cine", "// CINE Y SERIES")]
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
            noticias.append({
                "titulo": texto_limpio(texto_de(it, "title"), 140),
                "enlace": texto_de(it, "link") or texto_de(it, "guid"),
                "resumen": texto_limpio(desc or contenido),
                "imagen": imagen_de(it, desc, contenido),
                "fecha": leer_fecha(texto_de(it, "pubDate", "dc:date")),
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
            })
    validas = []
    for n in noticias:
        n["enlace"] = url_valida(n["enlace"])
        n["imagen"] = url_valida(n["imagen"])
        if n["titulo"] and n["enlace"]:
            n["medio"] = fuente["nombre"]
            n["categoria"] = fuente["categoria"]
            validas.append(n)
    return validas


def fecha_bonita(d):
    d = d.astimezone(MADRID)
    return f"{d.day} {MESES[d.month - 1]}, {d:%H:%M}"


def tarjeta(n):
    e = lambda s: html.escape(s or "", quote=True)
    img = (f'<img src="{e(n["imagen"])}" alt="" loading="lazy" referrerpolicy="no-referrer" '
           f'onerror="this.remove()">') if n["imagen"] else ""
    cuando = f' · {fecha_bonita(n["fecha"])}' if n["fecha"] else ""
    resumen = f'<p>{e(n["resumen"])}</p>' if n["resumen"] else ""
    return (f'      <article class="news-card"><a href="{e(n["enlace"])}" target="_blank" rel="noopener nofollow">'
            f'{img}<div><span class="src">{e(n["medio"])}{cuando}</span><h4>{e(n["titulo"])}</h4>{resumen}</div></a></article>')


def elegir(noticias, cfg):
    ahora = datetime.now(timezone.utc)
    limite = ahora - timedelta(days=cfg.get("dias_maximos", 3))
    vistos, por_medio, elegidas = set(), {}, []
    viejo = datetime(1970, 1, 1, tzinfo=timezone.utc)
    for n in sorted(noticias, key=lambda n: n["fecha"] or viejo, reverse=True):
        if n["fecha"] and n["fecha"] < limite:
            continue
        if n["fecha"] and n["fecha"] > ahora + timedelta(hours=2):
            n["fecha"] = ahora
        clave = re.sub(r"\W+", "", n["titulo"].lower())[:60]
        if clave in vistos or n["enlace"] in vistos:
            continue
        if por_medio.get(n["medio"], 0) >= cfg.get("maximo_por_medio", 3):
            continue
        vistos.update({clave, n["enlace"]})
        por_medio[n["medio"]] = por_medio.get(n["medio"], 0) + 1
        elegidas.append(n)
        if len(elegidas) >= cfg.get("noticias_por_categoria", 10):
            break
    return elegidas


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

    if not todas:
        print("No se ha podido leer ninguna fuente: dejo la web como estaba.")
        return 0

    columnas = []
    for clave, titulo in CATEGORIAS:
        elegidas = elegir([n for n in todas if n["categoria"] == clave], cfg)
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
    INDEX.write_text(nueva, encoding="utf-8")
    print(f"Web actualizada. Fuentes con fallo: {', '.join(fallos) or 'ninguna'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
