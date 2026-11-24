# /gta-6/trucos/ : «Trucos y sistemas de GTA VI» a partir de _fuentes/carruseles-gta6/datos.py
# (los mismos datos que los carruseles de redes). python3 _fuentes/generadores/trucos_gta.py
import json, html, os, re, sys
os.chdir('/home/claude/trollacos-web')
sys.path.insert(0, '_fuentes/carruseles-gta6')
from datos import TEMAS, FUENTES
from PIL import Image

g = open('gta-6/index.html', encoding='utf-8').read()
style = g[g.find('<style>'):g.find('</style>') + 8]
foot = g[g.find('<footer>'):g.find('</footer>') + 9]
esc = html.escape
FECHA = '24 de noviembre de 2026'
COL = {'y': '#ffd23f', 'o': '#ff9a3d', 'p': '#ff2bd6', 'v': '#b98cff', 'c': '#1ff2ff'}

extra = """
.tr-ind{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 8px}
.tr-ind a{font-family:'VT323',monospace;font-size:20px;padding:6px 12px;border:2px solid var(--cyan);border-radius:20px;color:var(--cyan);text-decoration:none}
.tema{margin:34px 0;padding-top:6px}
.tema h2{margin-bottom:4px}.tema .st{opacity:.9;margin:0 0 14px}
.tcs{display:flex;flex-direction:column;gap:12px}
.tc{display:flex;gap:14px;align-items:flex-start;background:rgba(20,9,74,.7);border:2px solid var(--c);border-left-width:8px;border-radius:14px;padding:12px 14px}
.tc .i{font-size:26px;line-height:1.2;flex:none;width:34px;text-align:center}
.tc b{display:block;color:var(--c);font-size:19px}.tc p{margin:3px 0 0}
.diapos{display:flex;gap:10px;overflow-x:auto;margin:14px 0 6px;padding-bottom:6px}
.diapos a{flex:none}.diapos img{width:150px;height:auto;border-radius:8px;border:2px solid rgba(31,242,255,.4);display:block}
.diapos-t{font-family:'VT323',monospace;font-size:18px;opacity:.8}
</style>"""
style2 = style.replace('</style>', extra)

os.makedirs('gta-6/trucos/img', exist_ok=True)
secciones, idx = [], []
for i, t in enumerate(TEMAS, 1):
    cards = ''.join(f'<div class="tc" style="--c:{COL[c[3]]}"><span class="i">{c[0]}</span><div><b>{esc(c[1])}</b><p>{esc(c[2])}</p></div></div>'
                    for s in t['slides'] for c in s)
    imgs = []
    for j in range(1, len(t['slides']) + 1):
        src = f'_fuentes/carruseles-gta6/salida/{i:02d}-{t["slug"]}-{j}.png'
        dst = f'gta-6/trucos/img/{t["slug"]}-{j}.webp'
        im = Image.open(src).convert('RGB'); im.save(dst, quality=84)
        im.resize((300, 375)).save(dst.replace('.webp', '-mini.webp'), quality=80)
        imgs.append(f'<a href="/{dst}" target="_blank" rel="noopener"><img src="/{dst.replace(".webp", "-mini.webp")}" alt="{esc(t["titulo"].capitalize())}, diapositiva {j}" width="300" height="375" loading="lazy"></a>')
    idx.append(f'<a href="#{t["slug"]}">{esc(t["titulo"].capitalize())}</a>')
    secciones.append(f'''<section class="tema" id="{t["slug"]}">
  <h2>{esc(t["titulo"].capitalize())}</h2>
  <p class="st">{esc(t["sub"])}</p>
  <div class="tcs">{cards}</div>
  <div class="nota"><div><b>EL TROLLACO OPINA:</b> {esc(t["troll"])}</div></div>
  <p class="diapos-t">📲 En versión carrusel (pincha para verla en grande y guardarla):</p>
  <div class="diapos">{''.join(imgs)}</div>
</section>''')

ld = {"@context": "https://schema.org", "@type": "Article", "headline": "Trucos y sistemas de GTA VI: perfil criminal, estrellas, coches, WAiNK, BuckMe, atracos y más",
      "datePublished": "2026-11-24", "dateModified": "2026-11-24", "inLanguage": "es-ES",
      "author": {"@type": "Person", "name": "Danna", "url": "https://trollacos.com/danna/"},
      "publisher": {"@type": "Organization", "name": "Trollacos", "url": "https://trollacos.com/"},
      "image": "https://trollacos.com/gta-6/trucos/img/perfil-criminal-1.webp", "mainEntityOfPage": "https://trollacos.com/gta-6/trucos/"}

page = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Trucos de GTA 6: perfil criminal, estrellas, coches más rápidos, WAiNK y más | Trollacos</title>
<meta name="description" content="Cómo funcionan el perfil criminal, las estrellas de la policía, WAiNK, BuckMe, los rastreadores y la relación de Jason y Lucía en GTA VI, los coches más rápidos, las mejores armas y cómo atracar una tienda. En español de España y sin destripes.">
<link rel="canonical" href="https://trollacos.com/gta-6/trucos/">
<meta property="og:type" content="article">
<meta property="og:title" content="Trucos y sistemas de GTA VI | Trollacos">
<meta property="og:description" content="Perfil criminal, estrellas, coches, WAiNK, BuckMe, atracos, rastreadores, Jason y Lucía, jugar sin matar y mejores armas.">
<meta property="og:url" content="https://trollacos.com/gta-6/trucos/">
<meta property="og:image" content="https://trollacos.com/gta-6/trucos/img/perfil-criminal-1.webp">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/icono.png">
{style2}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<div class="scan"></div>
<nav class="top">
  <a href="/"><img class="px" src="/logo.webp" alt="Trollacos" width="1600" height="161"></a>
  <a href="/gta-6/">‹ GUÍA</a>
</nav>
<header class="cab">
  <div class="etq">&gt; TRUCOS Y SISTEMAS_</div>
  <h1>Trucos de GTA VI: todo lo que el juego no te explica bien</h1>
  <p class="entradilla">Perfil criminal, estrellas de la policía, coches más rápidos, WAiNK, BuckMe, atracos, rastreadores, la relación de Jason y Lucía, cómo jugar sin matar y las mejores armas. Explicado claro, en español de España y sin destripes de la historia.</p>
  <p class="fecha-act">Por <a href="/danna/">Danna</a> · Actualizado el {FECHA}</p>
  <div class="troll-cab" aria-hidden="true"><img class="px troll" src="/img/trollaco-mando.png" alt=""></div>
</header>
<main>
  <div class="tr-ind">{''.join(idx)}</div>
  <p style="opacity:.8;font-size:16px">Mandos: PS5 / Xbox. Las cifras de coches y armas son las de la ficha del juego, sobre 10.</p>
  {''.join(secciones)}
  <p class="ojo">Datos contrastados en varias guías ({esc(FUENTES)}). Trollacos no tiene relación con Rockstar Games ni Take-Two. Si ves algo que ha cambiado con un parche, avísanos en info@trollacos.com.</p>
  <p style="text-align:center;margin-top:26px"><a href="/gta-6/" style="font-family:'VT323',monospace;font-size:24px;color:var(--cyan)">‹ Volver a la guía completa de GTA VI</a></p>
</main>
{foot}
</body>
</html>
'''
open('gta-6/trucos/index.html', 'w', encoding='utf-8').write(page)

sm = open('sitemap.xml', encoding='utf-8').read()
if '/gta-6/trucos/' not in sm:
    sm = sm.replace('  <url><loc>https://trollacos.com/gta-6/que-comprar/</loc>', '  <url><loc>https://trollacos.com/gta-6/trucos/</loc><lastmod>2026-11-24</lastmod><changefreq>weekly</changefreq></url>\n  <url><loc>https://trollacos.com/gta-6/que-comprar/</loc>', 1)
    open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print('ok', len(page))
