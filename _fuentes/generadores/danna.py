"""Ficha de Danna: /danna/. Uso: python3 _fuentes/generadores/danna.py"""
import os, json, html
RAIZ = '/home/claude/trollacos-web'; os.chdir(RAIZ)
IG = 'dannapixel'
g = open('gta-6/index.html', encoding='utf-8').read()
style = g[g.find('<style>'):g.find('</style>') + 8]
foot = g[g.find('<footer>'):g.find('</footer>') + 9]
noti = json.load(open('_fuentes/generadores/noticias_gta.json', encoding='utf-8'))
tec = json.load(open('_fuentes/generadores/tecnologia.json', encoding='utf-8'))
ult = sorted([(n['fecha'], n['titulo'], f'/gta-6/noticias/{n["slug"]}/', '🌴 GTA VI') for n in noti] +
             [(n['fecha'], n['titulo'], f'/tecnologia/{n["slug"]}/', '📱 TECNOLOGÍA') for n in tec], reverse=True)[:6]
extra = '''.dn{max-width:820px;margin:0 auto;padding:0 16px}
.dn .foto{margin:18px 0;border:4px solid var(--pink);border-radius:16px;overflow:hidden;box-shadow:0 0 28px rgba(255,43,214,.45)}
.dn .foto img{display:block;width:100%;height:auto}
.dn .k{font-family:'VT323',monospace;font-size:22px;color:var(--cyan)}
.dn h1{margin:6px 0 4px}.dn .cargo{font-family:'VT323',monospace;font-size:24px;color:var(--yellow);margin:0 0 6px}
.dn p{font-size:19px;line-height:1.6}.dn h2{margin-top:30px}
.areas{display:grid;gap:12px;margin:12px 0}
.area{padding:14px 16px;border:2px solid rgba(31,242,255,.45);border-radius:12px;background:rgba(31,242,255,.05)}
.area b{display:block;font-family:'Righteous',sans-serif;font-weight:400;font-size:21px;color:#fff;margin-bottom:4px}
.area span{font-size:17px;color:#d9d3f5}
.ficha-d{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px 16px;list-style:none;padding:14px 16px;margin:16px 0;border:2px dashed var(--yellow);border-radius:12px;background:rgba(255,210,63,.06);font-size:17px}
.ficha-d b{display:block;font-family:'VT323',monospace;font-weight:400;font-size:19px;color:var(--yellow)}
.ult{display:grid;gap:10px;margin:10px 0}.ult a{display:block;padding:12px 14px;border:1px solid rgba(255,43,214,.5);border-radius:10px;text-decoration:none;color:#fff}
.ult a:hover{border-color:var(--pink)}.ult small{display:block;font-family:'VT323',monospace;font-size:18px;color:var(--cyan)}
.btn-ig{display:inline-block;margin:10px 0;padding:12px 20px;border-radius:12px;background:linear-gradient(90deg,#ff2bd6,#7a2bff);color:#fff;font-weight:700;text-decoration:none;font-size:18px}
.nota{display:flex;gap:14px;align-items:flex-start;margin:22px 0;padding:14px 16px;border:2px dashed var(--yellow);border-radius:12px;background:rgba(255,210,63,.07)}
.nota img{width:44px;image-rendering:pixelated;flex:none}.nota p{margin:0;font-size:17px}.nota b{color:var(--yellow)}
</style>'''
ultimas = ''.join(f'<a href="{u}"><small>{s} · {f[8:10]}/{f[5:7]}</small>{html.escape(t)}</a>' for f, t, u, s in ult)
page = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Danna, reportera de Trollacos: gaming, redes y eventos | Trollacos</title>
<meta name="description" content="Quién es Danna, la reportera de Trollacos: noticias de GTA VI y videojuegos, tecnología, redes sociales, streamings y eventos. Con guasa y sin rodeos.">
<link rel="canonical" href="https://trollacos.com/danna/">
<meta property="og:title" content="Danna, la reportera de Trollacos"><meta property="og:image" content="https://trollacos.com/img/danna-setup.webp?v=2">
<link rel="icon" href="/icono.png">
{style.replace('</style>', extra)}
</head><body>
<div class="scan"></div>
<nav class="top"><a href="/"><img class="px" src="/logo.webp" alt="Trollacos" width="1600" height="161"></a><a href="/">‹ PORTADA</a></nav>
<main class="dn">
  <p class="k">&gt; FICHA DE LA REDACCIÓN_</p>
  <h1>Danna</h1>
  <p class="cargo">Editora de gaming, redes y tendencias · Tu reportera del otro lado de la pantalla</p>
  <figure class="foto"><img src="/img/danna-setup.webp?v=2" alt="Danna en su setup" width="1100" height="1100"></figure>
  <p><strong>Danna</strong> es la cara fresca, rápida y con el mando siempre cargado de Trollacos. Se encarga de contarte lo último de los videojuegos y la tecnología antes que tu primo «el que se entera de todo», y de que en nuestras redes nunca falte el salseo. Si el Dr. Aris V. Torres es el archivo polvoriento de los misterios, Danna es la notificación que te vibra en el bolsillo.</p>
  <ul class="ficha-d">
    <li><b>📍 Base de operaciones</b>Un setup rosa y cian con más ledes que una feria</li>
    <li><b>🎮 Juego favorito</b>Trollaco Run (no se lo digáis al Trollaco)</li>
    <li><b>☕ Combustible</b>Café, energía y la cuenta atrás de GTA VI</li>
    <li><b>😤 Su némesis</b>El lag. Y el Trollaco, según el día</li>
  </ul>
  <h2>A qué se dedica</h2>
  <div class="areas">
    <div class="area"><b>🌴 Gaming y novedades</b><span>Lanzamientos, tráileres, rumores (marcados como rumores) y todo lo que pasa en el sector. Ahora mismo, en modo GTA VI 24/7.</span></div>
    <div class="area"><b>📱 Tecnología</b><span>Móviles, gadgets y cacharros que vas a querer en Navidad, explicados sin tecnicismos y con el precio de verdad.</span></div>
    <div class="area"><b>📲 Redes sociales</b><span>Lleva el Instagram y el TikTok, contesta a la comunidad y se entera de cada trend antes de que se vuelva viral. O eso dice ella.</span></div>
    <div class="area"><b>🎙️ Moderadora de chats y streamings</b><span>Pone orden en los directos: banea trolls (menos a uno, que es el jefe), responde preguntas y evita que el chat se convierta en un concurso de mayúsculas.</span></div>
    <div class="area"><b>🎤 Reportera en eventos</b><span>Ferias, presentaciones y lanzamientos: allí donde haya una cola de tres horas para probar algo, está Danna con el micro… y con el bocadillo de tortilla.</span></div>
  </div>
  <h2>Su estilo</h2>
  <p>Cercana, directa y con guasa. No te va a soltar un párrafo de tres líneas para decirte la fecha de un juego: te la dice, te avisa de cuánto ocupa y te recuerda que hagas sitio en la consola. Su lema: <strong>«Si no te lo cuento yo, te lo cuenta tu cuñado, y mal»</strong>.</p>
  <p>Y sí: es la única de la redacción que le ha ganado al Trollaco en su propio arcade. Él dice que fue lag.</p>
  <div class="nota"><img src="/img/trollaco.png" alt=""><p><b>EL TROLLACO OPINA:</b> Lo del arcade fue lag. Clarísimamente lag. Tengo testigos. Bueno, un testigo. Bueno, yo.</p></div>
  <a class="btn-ig" href="https://www.instagram.com/{IG}/" target="_blank" rel="noopener">📸 Sigue a Danna en Instagram · @{IG}</a>
  <h2>Lo último que ha contado</h2>
  <div class="ult">{ultimas}</div>
</main>
{foot}
</body></html>'''
os.makedirs('danna', exist_ok=True)
open('danna/index.html', 'w', encoding='utf-8').write(page)
sm = open('sitemap.xml', encoding='utf-8').read()
if '/danna/' not in sm:
    open('sitemap.xml', 'w', encoding='utf-8').write(sm.replace('</urlset>', '  <url><loc>https://trollacos.com/danna/</loc><changefreq>weekly</changefreq></url>\n</urlset>'))
print('ficha de Danna ok')
