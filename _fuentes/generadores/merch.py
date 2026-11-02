"""Genera /merch/: la tienda de Spreadshop integrada en la web, con el estilo de Trollacos.
Uso: python3 _fuentes/generadores/merch.py"""
import os
RAIZ = '/home/claude/trollacos-web'; os.chdir(RAIZ)
TIENDA = 'https://trollacos.myspreadshop.es'
g = open('gta-6/index.html', encoding='utf-8').read()
style = g[g.find('<style>'):g.find('</style>') + 8]
foot = g[g.find('<footer>'):g.find('</footer>') + 9]
extra = '''.merch{max-width:1100px;margin:0 auto}
.m-top{display:flex;gap:16px;align-items:center;max-width:780px;margin:0 auto 18px}
.m-top img{width:64px;image-rendering:pixelated;flex:none}
.m-top p{margin:0;padding:12px 16px;background:#fff;color:#160828;border-radius:14px;font-weight:700;font-size:17px;box-shadow:4px 4px 0 var(--pink)}
.m-btn{display:inline-block;padding:14px 22px;border-radius:12px;background:linear-gradient(90deg,#ff2bd6,#7a2bff);color:#fff;font-weight:700;font-size:18px;text-decoration:none;box-shadow:0 0 18px rgba(255,43,214,.5)}
.m-caja{text-align:center;margin:0 auto 22px}
#shop{background:#fff;color:#111;border-radius:16px;padding:10px;min-height:420px;border:3px solid var(--pink);box-shadow:0 0 26px rgba(255,43,214,.35);font-family:'Rubik',system-ui,sans-serif}
#shop .cargando{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:400px;gap:14px;color:#333;font-size:18px;text-align:center;padding:20px}
#shop .cargando img{width:56px;image-rendering:pixelated;animation:bote 1s ease-in-out infinite}
@keyframes bote{50%{transform:translateY(-8px)}}
.m-info{max-width:780px;margin:22px auto 0;font-size:15px;color:var(--muted)}
</style>'''
html = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Merch oficial de Trollacos: camisetas, sudaderas y más | Trollacos</title>
<meta name="description" content="La tienda oficial de Trollacos: camisetas, sudaderas, tazas y más con el logo y el Trollaco. Diseños propios, envío a toda España.">
<link rel="canonical" href="https://trollacos.com/merch/">
<meta property="og:title" content="Merch oficial de Trollacos">
<meta property="og:description" content="Camisetas, sudaderas y más con el logo de Trollacos. Diseños propios.">
<meta property="og:url" content="https://trollacos.com/merch/">
<meta property="og:image" content="https://trollacos.com/portada.jpg">
<link rel="icon" href="/icono.png">
{style.replace('</style>', extra)}
</head>
<body>
<div class="scan"></div>
<nav class="top">
  <a href="/"><img class="px" src="/logo.webp" alt="Trollacos" width="1600" height="161"></a>
  <a href="/">‹ PORTADA</a>
</nav>
<header class="cab"><div class="etq">&gt; MERCH OFICIAL_</div><h1>La tienda Trollacos</h1>
<p class="entradilla">Camisetas, sudaderas y más con el logo de Trollacos. Diseños nuestros, hechos para llevar con orgullo (y con algo de guasa).</p></header>
<main class="merch">
  <div class="m-top"><img src="/img/trollaco.png" alt="El Trollaco"><p>Si te la pones, eres del equipo. Si no te la pones… también, pero se nota menos.</p></div>
  <div class="m-caja"><a class="m-btn" href="{TIENDA}/" target="_blank" rel="noopener">👕 Abrir la tienda completa ›</a></div>
  <div id="shop"><div class="cargando"><img src="/img/trollaco-mando.png" alt=""><span>Cargando la tienda…</span></div></div>
  <p class="m-info">Los pedidos, los pagos, la fabricación y los envíos los gestiona <b>Spreadshop</b> (Spreadshirt), con sus propias condiciones de venta, devoluciones y privacidad. Cada prenda se fabrica cuando la pides. Los diseños y la marca Trollacos son nuestros: <a href="/aviso-legal/">todos los derechos reservados</a>.</p>
</main>
{foot}
<script>
var spread_shop_config = {{ prefix: '{TIENDA}', shopName: 'trollacos', locale: 'es_ES', baseId: 'shop' }};
// Si la tienda no carga (bloqueador, red…), dejamos un botón para abrirla directamente
setTimeout(function(){{var c=document.querySelector('#shop .cargando');if(c)c.innerHTML='<img src="/img/trollaco-mando.png" alt=""><span>La tienda no ha cargado aquí (a veces pasa con los bloqueadores de anuncios).</span><a class="m-btn" href="{TIENDA}/" target="_blank" rel="noopener">👕 Abrir la tienda en Spreadshop ›</a>';}},12000);
</script>
<script src="https://trollacos.myspreadshop.net/js/shopclient.nocache.js"></script>
</body>
</html>
'''
os.makedirs('merch', exist_ok=True)
open('merch/index.html', 'w', encoding='utf-8').write(html)
sm = open('sitemap.xml', encoding='utf-8').read()
if '/merch/' not in sm:
    sm = sm.replace('</urlset>', '  <url><loc>https://trollacos.com/merch/</loc><changefreq>monthly</changefreq></url>\n</urlset>')
    open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print('merch ok')
