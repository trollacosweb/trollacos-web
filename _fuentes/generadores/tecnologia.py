"""Genera la sección de Tecnología: /tecnologia/ (portada) y /tecnologia/<slug>/.
Datos en _fuentes/generadores/tecnologia.json. Uso: python3 _fuentes/generadores/tecnologia.py
Textos propios, sin enlaces a otras webs (la fuente se cita por su nombre). Productos con enlace de afiliado de Amazon
(solo en la web, nunca en correos). Opinan el Trollaco y la Princesa Neón; firma Danna."""
import json, os, html, urllib.parse, re
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(RAIZ)
N = json.load(open('_fuentes/generadores/tecnologia.json', encoding='utf-8'))
N.sort(key=lambda n: n['fecha'], reverse=True)
g = open('gta-6/index.html', encoding='utf-8').read()
style = g[g.find('<style>'):g.find('</style>') + 8]
foot = g[g.find('<footer>'):g.find('</footer>') + 9]
TAG = 'trollacos-21'
DANNA_IG = 'dannapixel'
MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
def fecha_txt(f):
    d = date.fromisoformat(f); return f'{d.day} de {MESES[d.month-1]} de {d.year}'
def esc(t): return html.escape(t, quote=True)
def amazon(q): return f'https://www.amazon.es/s?k={urllib.parse.quote_plus(q)}&tag={TAG}'

extra = """
.art{max-width:780px;margin:0 auto}
.art .meta{font-family:'VT323',monospace;font-size:21px;color:var(--cyan);margin:0 0 14px}
.art .lead{font-size:22px;color:#fff;font-weight:700;margin-bottom:18px}
.art p{font-size:19px}
.firma{display:flex;align-items:center;gap:12px;margin:0 0 18px}
.firma img{width:56px;height:56px;border-radius:50%;border:3px solid var(--pink);box-shadow:0 0 12px var(--pink);object-fit:cover}
.firma b{display:block;font-family:'Righteous',sans-serif;font-weight:400;font-size:20px;color:#fff}
.firma span{font-size:15px;color:var(--muted)}.firma a{color:var(--cyan)}
.nota{display:flex;gap:14px;align-items:flex-start;margin:22px 0;padding:14px 16px;border:2px dashed var(--yellow);border-radius:12px;background:rgba(255,210,63,.07)}
.nota img{width:44px;height:auto;image-rendering:pixelated;flex:none}.nota p{margin:0;font-size:17px}.nota b{color:var(--yellow)}
.nota.pri{border-color:#ff5ccf;background:rgba(255,92,207,.08)}.nota.pri b{color:#ff5ccf}
.rumor{margin:22px 0;padding:12px 16px;border-left:4px solid #9d4dff;background:rgba(157,77,255,.1);border-radius:6px;font-size:16px}
.rumor b{color:#c9a2ff}
.prods{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));gap:12px;margin:14px 0 6px}
.prod{display:block;text-decoration:none;padding:14px 16px;border:2px solid rgba(255,210,63,.5);border-radius:12px;background:rgba(255,210,63,.06)}
.prod:hover{border-color:var(--yellow);box-shadow:0 0 14px rgba(255,210,63,.35)}
.prod b{display:block;font-family:'Righteous',sans-serif;font-weight:400;font-size:19px;color:#fff}
.prod span{display:block;font-size:15px;color:var(--muted);margin:4px 0 8px}
.prod i{font-style:normal;font-family:'VT323',monospace;font-size:19px;color:var(--yellow)}
.afil{font-size:13px;color:var(--muted)}
.galeria{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:12px 0 4px}
.g-it{margin:0;border:2px solid rgba(31,242,255,.3);border-radius:12px;overflow:hidden;background:#000}
.g-it video,.g-it img{display:block;width:100%;height:220px;object-fit:cover;background:#000}
.g-it img{object-fit:contain;background:#f5f5f7;height:260px}
.g-it.alto video,.g-it.alto img{height:100%;min-height:220px;max-height:460px;object-fit:contain}
.g-it.alto{grid-row:span 2}
.g-it figcaption{font-size:14px;color:#e9e6ff;padding:8px 10px;background:#140830}
@media(max-width:560px){.galeria{grid-template-columns:1fr}.g-it.alto{grid-row:auto}.g-it.alto video{max-height:520px}}
.portada-art{margin:0 0 20px}.portada-art img{width:100%;height:auto;max-height:440px;object-fit:contain;border-radius:14px;background:radial-gradient(circle at 50% 40%,#2a0b4a,#07021a);border:2px solid rgba(31,242,255,.35)}
.portada-art figcaption{font-size:13px;color:var(--muted);margin-top:4px;text-align:right}
.tarj .mini-foto{width:84px;height:84px;object-fit:contain;flex:none;border-radius:10px;background:#14063a}
.fuente{font-size:15px;color:var(--muted);border-top:1px solid rgba(233,230,255,.15);padding-top:12px;margin-top:24px}
.autora{display:flex;gap:18px;align-items:center;margin:28px 0;padding:18px;border:3px solid var(--pink);border-radius:16px;background:linear-gradient(135deg,rgba(255,43,214,.16),rgba(31,242,255,.08))}
.autora img{width:96px;height:96px;border-radius:50%;border:4px solid var(--cyan);flex:none;object-fit:cover}
.autora span{font-family:'VT323',monospace;font-size:19px;color:var(--cyan)}
.autora b{display:block;font-family:'Righteous',sans-serif;font-weight:400;font-size:28px;color:#fff}
.autora p{margin:4px 0 10px;font-size:16px;color:var(--muted)}
.btn-ig{display:inline-block;padding:9px 16px;border-radius:10px;background:linear-gradient(90deg,#ff2bd6,#7a2bff);color:#fff;font-weight:700;text-decoration:none;font-size:16px}
@media(max-width:520px){.autora{flex-direction:column;text-align:center}}
.lista-not{display:grid;gap:14px}
.tarj{display:flex;gap:14px;align-items:center;text-decoration:none;padding:16px 18px;border:1px solid rgba(31,242,255,.4);border-radius:12px;background:rgba(31,242,255,.05)}
.tarj:hover{border-color:var(--pink)}
.tarj .e{font-size:38px;flex:none}
.tarj small{font-family:'VT323',monospace;font-size:19px;color:var(--cyan)}
.tarj h3{font-family:'Righteous',sans-serif;font-weight:400;font-size:21px;color:#fff;margin:4px 0}
.tarj p{margin:0;color:var(--muted);font-size:16px}
.princesa-dice{display:flex;gap:14px;align-items:center;max-width:780px;margin:0 auto 22px}
.princesa-dice img{width:72px;image-rendering:pixelated;flex:none}
.princesa-dice p{margin:0;padding:12px 16px;background:#fff;color:#160828;border-radius:14px;font-weight:700;font-size:17px;box-shadow:4px 4px 0 #ff5ccf}
.compartir a{display:inline-block;margin:4px 6px 4px 0;padding:6px 14px;border:1px solid var(--pink);border-radius:6px;color:#fff;text-decoration:none;font-size:16px}
</style>"""
style2 = style.replace('</style>', extra)

def firma():
    return (f'<div class="firma"><img src="/img/danna.jpg" alt="Danna" width="56" height="56"><div><b>Por Danna</b>'
            f'<span>Tu reportera del otro lado de la pantalla · <a href="https://www.instagram.com/{DANNA_IG}/" target="_blank" rel="noopener">📸 @{DANNA_IG}</a> · <a href="/gta-6/noticias/#danna">¿Quién es?</a></span></div></div>')
def autora():
    return (f'<div class="autora"><img src="/img/danna.jpg" alt="Danna" width="96" height="96"><div><span>&gt; ESTE ARTÍCULO TE LO HA CONTADO_</span><b>Danna</b>'
            f'<p>Tu reportera del otro lado de la pantalla. Tecnología y videojuegos, sin rodeos y con guasa.</p>'
            f'<a class="btn-ig" href="https://www.instagram.com/{DANNA_IG}/" target="_blank" rel="noopener">📸 Sigue a Danna en Instagram · @{DANNA_IG}</a></div></div>')

def pagina(titulo, desc, url, cuerpo, jsonld, tipo='article'):
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)} | Trollacos</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{tipo}">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://trollacos.com/portada.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/icono.png">
{style2}
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head>
<body>
<div class="scan"></div>
<nav class="top">
  <a href="/"><img class="px" src="/logo.webp" alt="Trollacos" width="1600" height="161"></a>
  <a href="/tecnologia/">‹ TECNOLOGÍA</a>
</nav>
{cuerpo}
{foot}
</body>
</html>
'''

def foto(n):
    for ext in ('webp', 'jpg', 'png'):
        f = f'img/tecnologia/{n["slug"]}.{ext}'
        if os.path.exists(f): return '/' + f
    return None

def galeria(n):
    g = n.get('galeria') or []
    if not g: return ''
    def item(x):
        if x['tipo'] == 'video':
            m = f'<video src="{x["src"]}" poster="{x["src"][:-4]}.jpg" autoplay muted loop playsinline preload="metadata" aria-label="{esc(x["txt"])}"></video>'
        else:
            m = f'<img src="{x["src"]}" alt="{esc(x["txt"])}" loading="lazy">'
        return f'<figure class="g-it{" alto" if x.get("alto") else ""}">{m}<figcaption>{esc(x["txt"])}</figcaption></figure>'
    return (f'<h2>📸 En imágenes</h2><div class="galeria">{"".join(item(x) for x in g)}</div>'
            f'<p class="afil" style="text-align:right">Imágenes y vídeos: {esc(n.get("credito", "prensa oficial de la marca"))}</p>')

def tarjeta(n):
    ico = f'<img class="mini-foto" src="{foto(n)}" alt="" loading="lazy">' if foto(n) else f'<span class="e" aria-hidden="true">{n.get("emoji","📱")}</span>'
    return (f'<a class="tarj" href="/tecnologia/{n["slug"]}/">{ico}<div>'
            f'<small>{fecha_txt(n["fecha"])}</small><h3>{esc(n["titulo"])}</h3><p>{esc(n["entradilla"])}</p></div></a>')

for n in N:
    url = f'https://trollacos.com/tecnologia/{n["slug"]}/'
    otras = [o for o in N if o is not n][:3]
    share = urllib.parse.quote(f'{n["titulo"]} {url}')
    prods = ''.join(f'<a class="prod" href="{amazon(q)}" target="_blank" rel="sponsored nofollow noopener"><b>{esc(t)}</b><span>{esc(d)}</span><i>VER PRECIO EN AMAZON ›</i></a>'
                    for t, d, q in n.get('productos', []))
    rumor = f'<div class="rumor"><b>🕵️ RUMORES SIN CONFIRMAR:</b> {n["rumores"]}</div>' if n.get('rumores') else ''
    cuerpo = f'''<main><article class="art">
  <p class="meta">&gt; TECNOLOGÍA · {fecha_txt(n["fecha"]).upper()}_</p>
  <h1>{esc(n["titulo"])}</h1>
  <p class="lead">{esc(n["entradilla"])}</p>
  {firma()}
  {(f'<figure class="portada-art"><img src="{foto(n)}" alt="{esc(n.get("alt", n["titulo"]))}" loading="lazy"><figcaption>Imagen: {esc(n.get("credito", "prensa oficial de la marca"))}</figcaption></figure>') if foto(n) else ''}
  {''.join(f'<p>{p}</p>' for p in n["cuerpo"])}
  {galeria(n)}
  {rumor}
  <h2>🛒 Lo que te recomendamos</h2>
  <div class="prods">{prods}</div>
  <p class="afil">Enlaces de afiliado: si compras desde aquí, Trollacos se lleva una pequeña comisión sin que a ti te cueste nada más. Los precios cambian: mira el de Amazon al momento.</p>
  <div class="nota"><img src="/img/trollaco.png" alt=""><p><b>EL TROLLACO OPINA:</b> {n["opina"]}</p></div>
  <div class="nota pri"><img src="/img/princesa.png" alt=""><p><b>LA PRINCESA NEÓN OPINA:</b> {n["princesa"]}</p></div>
  {autora()}
  <p class="compartir"><a href="https://wa.me/?text={share}" target="_blank" rel="noopener">Compartir por WhatsApp</a><a href="https://t.me/share/url?url={urllib.parse.quote(url)}" target="_blank" rel="noopener">Telegram</a></p>
  <p class="fuente">Fuente: {esc(n["fuente"])}. Contado por Trollacos con nuestras palabras. Precios consultados el {fecha_txt(n["fecha"])}.</p>
  <h2>Más tecnología</h2>
  <div class="lista-not">{''.join(tarjeta(o) for o in otras)}</div>
  <p style="margin-top:16px"><a href="/tecnologia/">Ver toda la tecnología ›</a></p>
</article></main>'''
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": n["titulo"], "description": n["entradilla"],
          "datePublished": n["fecha"], "dateModified": n["fecha"], "inLanguage": "es", "mainEntityOfPage": url,
          "image": "https://trollacos.com/portada.jpg", "author": {"@type": "Organization", "name": "Trollacos"},
          "publisher": {"@type": "Organization", "name": "Trollacos", "logo": {"@type": "ImageObject", "url": "https://trollacos.com/icono-512.png"}}}
    os.makedirs(f'tecnologia/{n["slug"]}', exist_ok=True)
    open(f'tecnologia/{n["slug"]}/index.html', 'w', encoding='utf-8').write(pagina(n["titulo"], n["entradilla"], url, cuerpo, ld))

url = 'https://trollacos.com/tecnologia/'
cuerpo = f'''<header class="cab"><div class="etq">&gt; TECNOLOGÍA CON GUASA_</div><h1>Tecnología</h1>
<p class="entradilla">Móviles, Alexa, gadgets y todo lo que vas a querer estas Navidades. Lo que cuesta de verdad, a quién le pega y la opinión (nada objetiva) del Trollaco y la Princesa Neón.</p></header>
<main>
<div class="princesa-dice"><img src="/img/princesa.png" alt="La Princesa Neón"><p>¡Hola! Soy la Princesa Neón. Mientras Trollaco me rescata, yo me dedico a la tecnología. Alguien en este castillo tiene que saber qué móvil comprar. 👑</p></div>
<div class="lista-not">{''.join(tarjeta(n) for n in N)}</div>
<p class="afil" style="margin-top:18px">Algunos enlaces son de afiliado de Amazon: si compras desde aquí, Trollacos se lleva una pequeña comisión sin que a ti te cueste nada más.</p>
</main>'''
ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Tecnología", "url": url, "inLanguage": "es"}
os.makedirs('tecnologia', exist_ok=True)
open('tecnologia/index.html', 'w', encoding='utf-8').write(pagina('Tecnología: móviles, Alexa y gadgets con guasa', 'Qué móvil comprar, los nuevos Echo y Alexa+, y la tecnología que vas a querer estas Navidades, contada por Trollacos.', url, cuerpo, ld, 'website'))

# portada: bloque de Tecnología entre <!--TEC:INICIO--> y <!--TEC:FIN-->
ix = open('index.html', encoding='utf-8').read()
def card_portada(n):
    ico = f'<img src="{foto(n)}" alt="" loading="lazy" style="width:100%;height:120px;object-fit:contain;border-radius:8px;background:#14063a;margin-bottom:8px">' if foto(n) else f'<span class="ico-a">{n.get("emoji","📱")}</span>'
    return (f'      <a class="arsenal-card" href="/tecnologia/{n["slug"]}/">{ico}'
            f'<h3>{esc(n["titulo"])}</h3><p>{esc(n["entradilla"])}</p><span class="ver">LEER ›</span></a>')
bloque = ('<!--TEC:INICIO-->\n  <div class="princesa-portada"><img class="px" src="/img/princesa.png" alt="La Princesa Neón" width="64" height="68">'
          '<span class="pp-b">¿Qué móvil me pido para Navidad? ¡Ayuda! 👑</span></div>\n'
          '  <div class="arsenal-grid">\n' + '\n'.join(card_portada(n) for n in N[:4]) + '\n  </div>\n'
          '  <p style="text-align:center;margin-top:16px"><a class="btn alt" href="/tecnologia/">TODA LA TECNOLOGÍA</a></p>\n<!--TEC:FIN-->')
if '<!--TEC:INICIO-->' in ix:
    ix = re.sub(r'<!--TEC:INICIO-->.*?<!--TEC:FIN-->', lambda m: bloque, ix, flags=re.S)
    open('index.html', 'w', encoding='utf-8').write(ix)

# sitemap
sm = open('sitemap.xml', encoding='utf-8').read()
for u, f in [(url, N[0]['fecha'])] + [(f'https://trollacos.com/tecnologia/{n["slug"]}/', n['fecha']) for n in N]:
    if f'<loc>{u}</loc>' not in sm:
        sm = sm.replace('</urlset>', f'  <url><loc>{u}</loc><lastmod>{f}</lastmod><changefreq>weekly</changefreq></url>\n</urlset>')
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print(len(N), 'artículos de tecnología')
