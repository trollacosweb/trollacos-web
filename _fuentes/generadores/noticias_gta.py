"""Genera las noticias propias de GTA VI: /gta-6/noticias/ (portada) y /gta-6/noticias/<slug>/.
Datos en _fuentes/generadores/noticias_gta.json (la más nueva primero).
Uso: python3 _fuentes/generadores/noticias_gta.py   (desde la raíz del repo)
Sin enlaces a otras webs: la fuente se cita por su nombre."""
import json, os, html, urllib.parse
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(RAIZ)
N = json.load(open('_fuentes/generadores/noticias_gta.json', encoding='utf-8'))
# Danna firma las noticias. Pon aquí su usuario de Instagram (sin @) y saldrá el enlace en cada noticia.
DANNA_IG = ''
def firma():
    ig = f' · <a href="https://www.instagram.com/{DANNA_IG}/" target="_blank" rel="noopener">@{DANNA_IG} en Instagram</a>' if DANNA_IG else ''
    return f'<div class="firma"><img src="/img/danna.jpg" alt="Danna" width="56" height="56"><div><b>Por Danna</b><span>Tu reportera del otro lado de la pantalla{ig} · <a href="/gta-6/noticias/#danna">¿Quién es?</a></span></div></div>'
N.sort(key=lambda n: n['fecha'], reverse=True)
g = open('gta-6/index.html', encoding='utf-8').read()
style = g[g.find('<style>'):g.find('</style>') + 8]
foot = g[g.find('<footer>'):g.find('</footer>') + 9]
MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
def fecha_txt(f):
    d = date.fromisoformat(f); return f'{d.day} de {MESES[d.month-1]} de {d.year}'
def esc(t): return html.escape(t, quote=True)
def strip(t):
    import re; return re.sub(r'<[^>]+>', '', t)

extra = """
.art{max-width:760px;margin:0 auto}
.art .meta{font-family:'VT323',monospace;font-size:21px;color:var(--cyan);margin:0 0 14px}
.art .lead{font-size:22px;color:#fff;font-weight:700;margin-bottom:18px}
.art p{font-size:19px}
.guia-cta{display:block;margin:26px 0;padding:18px 20px;border:3px solid var(--pink);border-radius:14px;text-decoration:none;background:rgba(255,43,214,.1);box-shadow:0 0 22px rgba(255,43,214,.3)}
.guia-cta span{display:block;font-family:'VT323',monospace;font-size:20px;color:var(--pink)}
.guia-cta b{font-family:'Righteous',sans-serif;font-weight:400;font-size:24px;color:#fff}
.fuente{font-size:15px;color:var(--muted);border-top:1px solid rgba(233,230,255,.15);padding-top:12px;margin-top:24px}
.lista-not{display:grid;gap:14px}
.tarj{display:block;text-decoration:none;padding:16px 18px;border:1px solid rgba(31,242,255,.4);border-radius:12px;background:rgba(31,242,255,.05)}
.tarj:hover{border-color:var(--pink)}
.tarj small{font-family:'VT323',monospace;font-size:19px;color:var(--cyan)}
.tarj h3{font-family:'Righteous',sans-serif;font-weight:400;font-size:22px;color:#fff;margin:4px 0}
.tarj p{margin:0;color:var(--muted);font-size:17px}
.nota{display:flex;gap:14px;align-items:flex-start;margin:22px 0;padding:14px 16px;border:2px dashed var(--yellow);border-radius:12px;background:rgba(255,210,63,.07)}
.nota img{width:40px;height:auto;image-rendering:pixelated;flex:none}.nota p{margin:0;font-size:17px}.nota b{color:var(--yellow)}
.firma{display:flex;align-items:center;gap:12px;margin:0 0 18px}
.firma img{width:56px;height:56px;border-radius:50%;border:3px solid var(--pink);box-shadow:0 0 12px var(--pink);object-fit:cover}
.firma b{display:block;font-family:'Righteous',sans-serif;font-weight:400;font-size:20px;color:#fff}
.firma span{font-size:15px;color:var(--muted)}.firma a{color:var(--cyan)}
.compartir a{display:inline-block;margin:4px 6px 4px 0;padding:6px 14px;border:1px solid var(--pink);border-radius:6px;color:#fff;text-decoration:none;font-size:16px}
</style>"""
style2 = style.replace('</style>', extra)
hw = "<script>(function(){var d=new Date(),m=d.getMonth(),n=d.getDate();if((m===9&&n>=15)||(m===10&&n<=2))document.documentElement.className+=' halloween'})()</script>"
hwjs = "<script>if(document.documentElement.className.indexOf('halloween')>-1){document.querySelectorAll('img.troll[data-hw]').forEach(function(i){i.src=i.getAttribute('data-hw')})}</script>"

def pagina(titulo, desc, url, cuerpo, jsonld, tipo='article'):
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{hw}
<title>{esc(titulo)} | Trollacos</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{tipo}">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://trollacos.com/gta-6/portada.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/icono.png">
{style2}
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head>
<body>
<div class="scan"></div>
<nav class="top">
  <a href="/"><img class="px" src="/logo.webp" alt="Trollacos" width="1600" height="161"></a>
  <a href="/gta-6/">‹ GUÍA GTA VI</a>
</nav>
{cuerpo}
{foot}
{hwjs}
</body>
</html>
'''

def tarjeta(n):
    return f'<a class="tarj" href="/gta-6/noticias/{n["slug"]}/"><small>{fecha_txt(n["fecha"])}</small><h3>{esc(n["titulo"])}</h3><p>{esc(n["entradilla"])}</p></a>'

for i, n in enumerate(N):
    url = f'https://trollacos.com/gta-6/noticias/{n["slug"]}/'
    otras = [o for o in N if o is not n][:3]
    share = urllib.parse.quote(f'{n["titulo"]} {url}')
    cuerpo = f'''<main><article class="art">
  <p class="meta">&gt; NOTICIAS GTA VI · {fecha_txt(n["fecha"]).upper()}_</p>
  <h1>{esc(n["titulo"])}</h1>
  <p class="lead">{esc(n["entradilla"])}</p>
  {firma()}
  {''.join(f'<p>{p}</p>' for p in n["cuerpo"])}
  <div class="nota"><img class="troll" src="/img/trollaco.png" data-hw="/img/trollaco-hw.png" alt=""><p><b>EL TROLLACO OPINA:</b> {n["opina"]}</p></div>
  <a class="guia-cta" href="{n["guia"]}"><span>&gt; SIGUE LEYENDO EN LA GUÍA TROLLACOS DE GTA VI</span><b>{esc(n["guia_txt"])} ›</b></a>
  <p class="compartir"><a href="https://wa.me/?text={share}" target="_blank" rel="noopener">Compartir por WhatsApp</a><a href="https://t.me/share/url?url={urllib.parse.quote(url)}" target="_blank" rel="noopener">Telegram</a></p>
  <p class="fuente">Fuente: {esc(n["fuente"])}. Noticia de Trollacos, contada con nuestras palabras.</p>
  <h2>Más noticias de GTA VI</h2>
  <div class="lista-not">{''.join(tarjeta(o) for o in otras)}</div>
  <p style="margin-top:16px"><a href="/gta-6/noticias/">Ver todas las noticias ›</a></p>
</article></main>'''
    ld = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": n["titulo"], "description": n["entradilla"],
          "datePublished": n["fecha"], "dateModified": n["fecha"], "inLanguage": "es", "mainEntityOfPage": url,
          "image": "https://trollacos.com/gta-6/portada.jpg", "author": {"@type": "Organization", "name": "Trollacos"},
          "publisher": {"@type": "Organization", "name": "Trollacos", "logo": {"@type": "ImageObject", "url": "https://trollacos.com/icono-512.png"}}}
    os.makedirs(f'gta-6/noticias/{n["slug"]}', exist_ok=True)
    open(f'gta-6/noticias/{n["slug"]}/index.html', 'w', encoding='utf-8').write(pagina(n["titulo"], n["entradilla"], url, cuerpo, ld))

url = 'https://trollacos.com/gta-6/noticias/'
cuerpo = f'''<header class="cab"><div class="etq">&gt; ÚLTIMA HORA DE LEONIDA_</div><h1>Noticias de GTA VI</h1>
<p class="entradilla">Todo lo que va saliendo de GTA VI, contado a nuestra manera. Y cada noticia, enlazada a su sitio en la guía.</p></header>
<main style="padding-bottom:0">{firma()}</main>
<main><div class="lista-not">{''.join(tarjeta(n) for n in N)}</div>
<a class="guia-cta" href="/gta-6/"><span>&gt; LA GUÍA MÁS COMPLETA EN ESPAÑOL</span><b>La Guía Trollacos de GTA VI ›</b></a>
<div class="nota" id="danna"><img src="/img/danna.jpg" alt="" style="width:56px;border-radius:50%"><p><b>¿QUIÉN ES DANNA?</b> Nuestra reportera del otro lado de la pantalla: un personaje digital creado por Trollacos, como el Trollaco, que pone cara a nuestras noticias. Los textos los prepara la redacción de Trollacos.</p></div></main>'''
ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Noticias de GTA VI", "url": url, "inLanguage": "es"}
os.makedirs('gta-6/noticias', exist_ok=True)
open('gta-6/noticias/index.html', 'w', encoding='utf-8').write(pagina('Noticias de GTA VI: última hora en español', 'Las últimas noticias de GTA VI contadas por Trollacos, enlazadas a la guía más completa en español.', url, cuerpo, ld, 'website'))

# sitemap
sm = open('sitemap.xml', encoding='utf-8').read()
urls = ['https://trollacos.com/gta-6/noticias/'] + [f'https://trollacos.com/gta-6/noticias/{n["slug"]}/' for n in N]
for u in urls:
    if f'<loc>{u}</loc>' not in sm:
        f = N[0]['fecha'] if u.endswith('/noticias/') else next(n['fecha'] for n in N if u.endswith(n['slug'] + '/'))
        sm = sm.replace('</urlset>', f'  <url><loc>{u}</loc><lastmod>{f}</lastmod><changefreq>weekly</changefreq></url>\n</urlset>')
sm = __import__('re').sub(r'(<loc>https://trollacos.com/gta-6/noticias/</loc><lastmod>)[0-9-]+', r'\g<1>' + N[0]['fecha'], sm)
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print(len(N), 'noticias')

# portada: bloque de GTA y "Lo último", solo con noticias propias (nada de enlaces a otras webs)
import re
def fcorta(f):
    d = date.fromisoformat(f); return f'{d.day} {MESES[d.month-1][:3]}'
def card(n, entr=True):
    p = f'<p>{esc(n["entradilla"])}</p>' if entr else ''
    return (f'      <article class="news-card"><a href="/gta-6/noticias/{n["slug"]}/"><span class="mini mini-especial" aria-hidden="true">{n.get("emoji","🌴")}</span>'
            f'<div><span class="src">DANNA · {fcorta(n["fecha"]).upper()}</span><h4>{esc(n["titulo"])}</h4>{p}</div></a></article>')
ix = open('index.html', encoding='utf-8').read()
gta = '<!--GTA:INICIO-->\n    <div class="news-list">\n' + '\n'.join(card(n, False) for n in N[:4]) + '\n    </div>\n    <p style="text-align:center;margin-top:14px"><a href="/gta-6/noticias/">Todas las noticias de GTA VI ›</a></p>\n<!--GTA:FIN-->'
ix = re.sub(r'<!--GTA:INICIO-->.*?<!--GTA:FIN-->', lambda m: gta, ix, flags=re.S)
lo = ('<!--NOTICIAS:INICIO-->\n  <div class="firma-portada"><img src="/img/danna.jpg" alt="Danna" width="64" height="64"><p><b>Danna</b>, tu reportera del otro lado de la pantalla, te cuenta lo último de GTA VI con nuestras palabras. Sin rodeos y sin mandarte a otras webs.</p></div>\n'
      '    <div class="news-list">\n' + '\n'.join(card(n) for n in N[:8]) + '\n    </div>\n  <p style="text-align:center;margin-top:16px"><a class="btn alt" href="/gta-6/noticias/">VER TODAS LAS NOTICIAS</a></p>\n<!--NOTICIAS:FIN-->')
ix = re.sub(r'<!--NOTICIAS:INICIO-->.*?<!--NOTICIAS:FIN-->', lambda m: lo, ix, flags=re.S)
ix = ix.replace('<p class="small" style="margin:-14px 0 18px">Lo más fresco del día, en pocas líneas.</p>', '<p class="small" style="margin:-14px 0 18px">Las noticias de la redacción de Trollacos.</p>')
if '.firma-portada' not in ix:
    ix = ix.replace('  .news-meta{', '  .firma-portada{display:flex;gap:14px;align-items:center;max-width:760px;margin:0 auto 20px}.firma-portada img{width:64px;height:64px;border-radius:50%;border:3px solid var(--pink);box-shadow:0 0 14px var(--pink);flex:none;object-fit:cover}.firma-portada p{margin:0}.firma-portada b{color:var(--pink)}\n  #noticias .news-list{max-width:760px;margin:0 auto}\n  .news-meta{', 1)
open('index.html', 'w', encoding='utf-8').write(ix)

# rss.xml con nuestras noticias
from email.utils import format_datetime
from datetime import datetime, timezone
items = ''.join(f'<item><title>{esc(n["titulo"])}</title><link>https://trollacos.com/gta-6/noticias/{n["slug"]}/</link><guid>https://trollacos.com/gta-6/noticias/{n["slug"]}/</guid>'
                f'<pubDate>{format_datetime(datetime.fromisoformat(n["fecha"]).replace(hour=9, tzinfo=timezone.utc))}</pubDate><description>{esc(n["entradilla"])}</description></item>' for n in N)
open('rss.xml', 'w', encoding='utf-8').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Trollacos · Noticias de GTA VI</title><link>https://trollacos.com/gta-6/noticias/</link><description>Las noticias de GTA VI contadas por Trollacos.</description><language>es-es</language>{items}</channel></rss>\n')
print('portada y rss listos')
