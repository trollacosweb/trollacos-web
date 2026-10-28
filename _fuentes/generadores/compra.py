import json, html, os, urllib.parse
os.chdir('/home/claude/trollacos-web')
g = open('gta-6/index.html').read()
style = g[g.find('<style>'):g.find('</style>') + 8]
foot = g[g.find('<footer>'):g.find('</footer>') + 9]
TAG = 'trollacos-21'

def amz(q):
    return f'https://www.amazon.es/s?k={urllib.parse.quote_plus(q)}&amp;tag={TAG}'

extra = """
.niveles{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin:12px 0 16px}
.nivel{display:flex;flex-direction:column;border:1px solid rgba(255,157,60,.45);border-radius:10px;padding:14px 16px;background:linear-gradient(180deg,rgba(255,157,60,.08),rgba(255,43,214,.04))}
.nivel.rec{border:2px solid var(--yellow);box-shadow:0 0 18px rgba(255,210,63,.25)}
.nivel .etq-n{font-family:'VT323',monospace;font-size:19px;letter-spacing:.06em;color:var(--orange)}
.nivel.rec .etq-n{color:var(--yellow)}
.nivel h3{font-size:21px;margin:4px 0 6px}
.nivel p{font-size:16.5px;color:var(--muted);margin:0 0 10px}
.nivel .amz{margin-top:auto;text-align:center}
.truco{display:flex;gap:12px;align-items:flex-start;margin:10px 0 18px;padding:12px 14px;border:2px dashed rgba(134,204,108,.6);border-radius:8px;background:rgba(86,204,108,.07)}
.truco img{width:38px;height:auto;flex:none}
.truco p{margin:0;font-size:17.5px;color:#d6ffe0}
.truco b{font-family:'VT323',monospace;font-weight:400;font-size:20px;color:#9dffb5}
.check{list-style:none;margin:8px 0 16px}
.check li{padding:4px 0 4px 30px;position:relative}
.check li::before{content:"✔";position:absolute;left:4px;color:var(--cyan)}
.check li.no::before{content:"✘";color:#ff6b6b}
.migas{font-family:'VT323',monospace;font-size:20px;margin:24px 0 0;color:var(--muted)}.migas a{color:var(--cyan);text-decoration:none}
.aviso-p{font-size:15px;color:var(--muted);border-left:3px solid var(--orange);padding:6px 12px;margin:10px 0}
</style>"""
style2 = style.replace('</style>', extra)

def niveles(items):
    out = []
    for etq, tit, txt, q, rec in items:
        out.append(f'''    <div class="nivel{' rec' if rec else ''}"><span class="etq-n">{etq}</span><h3>{tit}</h3><p>{txt}</p>
      <a class="amz" href="{amz(q) if not q.startswith('http') else q}" target="_blank" rel="sponsored nofollow noopener">VER EN AMAZON ›</a></div>''')
    return '  <div class="niveles">\n' + '\n'.join(out) + '\n  </div>'

def truco(t, pose='trollaco-mando'):
    return f'  <div class="truco"><img class="px troll" src="/img/{pose}.png" data-hw="/img/{pose}-hw.png" alt=""><p><b>TRUCO DEL TROLLACO:</b> {t}</p></div>'

faq = [
 ("¿Se puede jugar a GTA 6 en PS4 o Xbox One?", "No. GTA VI solo sale en PS5 y Xbox Series X|S."),
 ("¿Cuánto ocupa GTA 6?", "Unos 210 GB en PS5, según la ficha de la PlayStation Store que publicó PlayStation Game Size el 27 de octubre. Rockstar no lo ha anunciado oficialmente, pero ese dato suele ser fiable. Deja al menos 250 GB libres para ir sobrado con las actualizaciones."),
 ("¿Merece la pena la PS5 Pro para GTA 6?", "Rockstar ha dicho que GTA VI apunta a 30 fps en todas las consolas, también en PS5 Pro. La Pro puede ofrecer mejor calidad de imagen, pero no más fluidez. Si ya tienes PS5, no necesitas cambiarla."),
 ("¿Necesito una tele de 120 Hz para GTA 6?", "No. Si el juego va a 30 fps, los 120 Hz no se notan en GTA VI. Es más importante que sea 4K con HDR y que tenga modo juego."),
 ("¿La edición física de GTA 6 trae disco?", "No. La caja trae un código de descarga, así que necesitarás espacio libre igualmente."),
]
faq_html = '\n'.join(f'  <details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
ld = {"@context": "https://schema.org", "@graph": [
  {"@type": "Article", "headline": "Qué necesitas para jugar a GTA VI: guía de compra 2026", "datePublished": "2026-10-24", "dateModified": "2026-10-28", "inLanguage": "es",
   "author": {"@type": "Organization", "name": "Trollacos"}, "publisher": {"@type": "Organization", "name": "Trollacos", "logo": {"@type": "ImageObject", "url": "https://trollacos.com/icono-512.png"}},
   "mainEntityOfPage": "https://trollacos.com/gta-6/que-comprar/"},
  {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}

hw = "<script>(function(){var d=new Date(),m=d.getMonth(),n=d.getDate();if((m===9&&n>=15)||(m===10&&n<=2))document.documentElement.className+=' halloween'})()</script>"

body = f'''
<main>
  <p class="migas"><a href="/">Trollacos</a> › <a href="/gta-6/">Guía GTA VI</a> › Qué comprar</p>
  <nav class="indice" aria-label="Índice">
    <b>&gt; ÍNDICE</b>
    <ol>
      <li><a href="#resumen">El resumen para los que tienen prisa</a></li>
      <li><a href="#consola">¿PS5, PS5 Pro o Xbox?</a></li>
      <li><a href="#espacio">Espacio para el juego</a></li>
      <li><a href="#tele">La tele o el monitor</a></li>
      <li><a href="#sonido">El sonido</a></li>
      <li><a href="#mandos">Mandos y accesorios</a></li>
      <li><a href="#edicion">¿Qué edición del juego?</a></li>
      <li><a href="#faq">Preguntas rápidas</a></li>
    </ol>
  </nav>
  <p class="aviso-p">Esta guía no es publicidad de ninguna marca: te contamos qué características buscar y por qué, con los datos de fabricantes y de Rockstar. Los botones llevan a Amazon con nuestro enlace de afiliado: si compras, Trollacos se lleva una pequeña comisión y a ti no te cuesta más.</p>

  <h2 id="resumen">El resumen para los que tienen prisa</h2>
  <div class="tabla"><table>
    <tr><th>Si tienes...</th><th>Lo que necesitas</th></tr>
    <tr><td><strong>PS4 o Xbox One</strong></td><td>Una consola nueva: GTA VI no sale en tu consola. Mira el apartado de consolas.</td></tr>
    <tr><td><strong>PS5 o Xbox Series X</strong></td><td>Probablemente solo <strong>espacio libre</strong>. Haz hueco o amplía el almacenamiento.</td></tr>
    <tr><td><strong>Xbox Series S</strong></td><td>Casi seguro, <strong>más espacio</strong>: la de 512 GB se queda muy justa.</td></tr>
    <tr><td><strong>Una tele antigua (Full HD)</strong></td><td>Se puede jugar, pero una 4K con HDR cambia muchísimo la experiencia en Vice City.</td></tr>
  </table></div>

  <h2 id="consola">¿PS5, PS5 Pro o Xbox?</h2>
  <p>Lo primero que hay que saber, porque ahorra mucho dinero: <strong>Rockstar ha dicho que GTA VI apuntará a 30 imágenes por segundo en todas las consolas</strong>, también en la PS5 Pro, y que todavía no ha decidido si habrá un modo a 60. La consola más cara no hará el juego más fluido. Puede verse algo mejor, pero no irá más rápido.</p>
  <p>Otra cosa a tener en cuenta: <strong>los precios de las consolas han subido mucho en 2026</strong>. La Xbox Series X cuesta ahora 799,99 € en la tienda oficial y la PS5 con lector, 649,99 €. En Amazon suelen estar algo por debajo, así que merece la pena comparar.</p>
{niveles([
 ('LA MÁS EQUILIBRADA', 'PS5 (Slim)', 'La opción que recomendaríamos a casi todo el mundo. Rockstar presenta a PlayStation como la plataforma donde mejor se juega, y es donde se capturó el tráiler de lanzamiento. Elige con lector si quieres juegos en disco de segunda mano.', 'PlayStation 5 Slim consola', True),
 ('A LO GRANDE', 'PS5 Pro', 'Para quien tiene una tele 4K grande y quiere la mejor imagen posible. Ojo: no hará que GTA VI vaya a más fps, y no trae lector de discos de serie.', 'PlayStation 5 Pro consola', False),
 ('LA ALTERNATIVA', 'Xbox Series X o S', 'La Series X es la equivalente a la PS5. La Series S es la más barata, pero va más justa de gráficos y de espacio (la de 512 GB se queda corta). Interesante si ya vives en Game Pass.', 'Xbox Series X consola', False)])}
{truco('Si ya tienes una PS5 normal, no te compres la Pro solo por GTA VI. Gástatelo mejor en un disco de más capacidad o en una buena tele.')}

  <h2 id="espacio">Espacio para el juego</h2>
  <p>Este es el apartado que más gente va a necesitar. La versión en caja <strong>no trae disco, trae un código de descarga</strong>, y GTA VI es enorme: <strong>unos 210 GB en PS5</strong>, según la ficha de la PlayStation Store que destapó PlayStation Game Size el 27 de octubre (Rockstar no lo ha anunciado, pero ese dato suele acertar). Es más o menos <strong>un tercio del espacio útil de una PS5</strong>. La precarga empieza el <strong>12 de noviembre</strong>, así que tienes hasta entonces para hacer hueco o ampliar.</p>
  <p><strong>Para PS5</strong>, la solución es un <strong>SSD M.2 interno</strong> en la ranura de ampliación. Lo que tiene que cumplir, según Sony:</p>
  <ul class="check">
    <li>Tipo <strong>M.2 NVMe PCIe Gen4</strong></li>
    <li>Velocidad de lectura de <strong>5.500 MB/s o más</strong> (recomendado)</li>
    <li>Con <strong>disipador</strong> (o uno que se le pueda poner)</li>
    <li class="no">Un disco duro USB normal sirve para guardar juegos, pero <strong>no para jugar</strong> a los de PS5</li>
  </ul>
{niveles([
 ('ECONÓMICO', 'SSD de 1 TB', 'Suficiente para GTA VI y unos cuantos juegos más. Busca uno PCIe 4.0 con disipador incluido.', 'SSD 1TB NVMe PCIe 4.0 disipador PS5', False),
 ('RECOMENDADO', 'SSD de 2 TB', 'El punto dulce: te olvidas del espacio durante años. Es la capacidad que más se recomienda para PS5.', 'SSD 2TB NVMe PCIe 4.0 disipador PS5', True),
 ('A LO GRANDE', 'SSD de 4 TB', 'Para tener toda la biblioteca instalada sin borrar nada nunca.', 'SSD 4TB NVMe PCIe 4.0 disipador PS5', False)])}
  <p><strong>Para Xbox Series</strong>, el equivalente es la <strong>tarjeta de expansión de almacenamiento</strong>, que se conecta por detrás y funciona igual que el disco interno. Un disco USB también sirve para guardar juegos, pero para jugar a los de Series X|S hace falta la tarjeta.</p>
  <p><a class="amz" href="{amz('tarjeta expansión almacenamiento Xbox Series')}" target="_blank" rel="sponsored nofollow noopener">💾 Ver tarjetas de expansión para Xbox</a></p>
{truco('Instalar un SSD en la PS5 son diez minutos y un destornillador. Hay vídeos oficiales de PlayStation que lo explican paso a paso. Hazlo antes del 12 de noviembre, que es cuando empieza la precarga.', 'trollaco')}

  <h2 id="tele">La tele o el monitor</h2>
  <p>Aquí también puedes ahorrar si sabes qué mirar. Como GTA VI irá a 30 fps, <strong>los 120 Hz y el HDMI 2.1 no se van a notar en este juego</strong> (sí en otros). Lo que de verdad cambia la experiencia es esto:</p>
  <ul class="check">
    <li><strong>4K</strong>: la PS5 y la Series X sacan imagen 4K, y Vice City tiene muchísimo detalle</li>
    <li><strong>HDR</strong>: los atardeceres de Leonida con HDR son otra cosa</li>
    <li><strong>Modo juego</strong> (ALLM): reduce el retraso entre mando y pantalla</li>
    <li>Tamaño: a 2 metros del sofá, de <strong>50 a 55 pulgadas</strong> va de lujo</li>
  </ul>
{niveles([
 ('ECONÓMICO', 'Tele 4K HDR de 43-50"', 'Para un dormitorio o un salón pequeño. Busca HDR y modo juego.', 'televisor 4K 50 pulgadas HDR modo juego', False),
 ('RECOMENDADO', 'Tele 4K HDR de 55" con buen brillo', 'El salto de calidad más claro para el dinero. Mira que tenga buen HDR (brillo alto) y modo juego.', 'televisor 4K 55 pulgadas HDR gaming', True),
 ('A LO GRANDE', 'Tele OLED o Mini-LED de 65"', 'Negros perfectos para las noches de Vice City. Si además juegas a otros títulos a 120 Hz, aquí sí lo aprovecharás.', 'televisor OLED 65 pulgadas gaming', False)])}

  <h2 id="sonido">El sonido</h2>
  <p>GTA VI tendrá su propio álbum y seis emisoras de radio confirmadas (las tienes en nuestra <a href="/gta-6/musica/">lista de canciones</a>). Para escucharlo bien, y para jugar de noche sin despertar a nadie:</p>
{niveles([
 ('ECONÓMICO', 'Auriculares con cable', 'Se conectan al mando, sin baterías ni complicaciones. Más que suficientes.', 'auriculares gaming cable PS5 Xbox', False),
 ('RECOMENDADO', 'Auriculares inalámbricos', 'Libertad total en el sofá. Comprueba que sean compatibles con tu consola (PS5 o Xbox).', 'auriculares gaming inalámbricos PS5', True),
 ('A LO GRANDE', 'Barra de sonido', 'Para que el salón suene como un cine cuando atraviesas Vice City a toda velocidad.', 'barra de sonido Dolby Atmos', False)])}

  <h2 id="mandos">Mandos y accesorios</h2>
  <p>Un segundo mando cargado es la diferencia entre seguir jugando o esperar con el cable enganchado. Y si sois dos en casa, la pelea por el mando está garantizada.</p>
{niveles([
 ('ESENCIAL', 'Mando extra', 'Un DualSense para PS5 o un mando inalámbrico de Xbox.', 'mando DualSense PS5', True),
 ('CÓMODO', 'Base de carga', 'Para dejar los mandos siempre cargados y no buscar cables.', 'base de carga mandos PS5', False),
 ('PARA LA ESPALDA', 'Silla gaming', 'Las partidas a GTA no duran diez minutos. Tu espalda te lo agradecerá.', 'silla gaming ergonómica', False)])}
{truco('Pide el día libre del 19 de noviembre ya. No te lo digo yo, te lo dice el sentido común. Y medio país.', 'trollaco')}

  <h2 id="edicion">¿Qué edición del juego?</h2>
  <p>La <strong>edición estándar</strong> (79,99 €) trae el juego completo. La <strong>Ultimate</strong> (99,99 $ en EE. UU.) añade coches, armas, ropa y objetos ligados a la historia de Jason y Lucía. Si solo quieres jugar la historia, la estándar es suficiente. Todas las reservas y compras antes del 20 de noviembre incluyen el <strong>Vintage Vice City Pack</strong>.</p>
  <p>
    <a class="amz" href="https://www.amazon.es/dp/B0GZH9BJYD?tag={TAG}" target="_blank" rel="sponsored nofollow noopener">🎮 GTA VI para PS5</a>
    <a class="amz" href="https://www.amazon.es/dp/B0GZVXB4DX?tag={TAG}" target="_blank" rel="sponsored nofollow noopener">🎮 GTA VI para Xbox</a>
  </p>
  <p>Más detalles de ediciones, personajes y mapa en la <a href="/gta-6/">guía completa de GTA VI</a>.</p>

  <h2 id="faq">Preguntas rápidas</h2>
{faq_html}

  <p class="ojo">Datos de Rockstar Games, Sony, Microsoft y medios especializados, actualizados a octubre de 2026. Los precios cambian a menudo: comprueba siempre el precio final en la tienda. Trollacos no tiene relación con Rockstar Games, Take-Two, Sony ni Microsoft.</p>
  <p style="text-align:center;margin-top:26px"><a href="/gta-6/" style="font-family:'VT323',monospace;font-size:24px;color:var(--cyan)">‹ Volver a la guía completa de GTA VI</a></p>
</main>'''

page = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{hw}
<title>Qué necesitas para jugar a GTA 6: guía de compra 2026 (consola, SSD, tele) | Trollacos</title>
<meta name="description" content="¿PS5, PS5 Pro o Xbox? ¿Cuánto espacio necesitas? ¿Hace falta una tele de 120 Hz? Todo lo que necesitas para jugar a GTA VI el 19 de noviembre, explicado claro y sin gastar de más.">
<link rel="canonical" href="https://trollacos.com/gta-6/que-comprar/">
<meta property="og:type" content="article">
<meta property="og:title" content="Qué necesitas para jugar a GTA 6 (sin gastar de más) | Trollacos">
<meta property="og:description" content="Consola, espacio, tele, sonido y edición: la guía de compra para el 19 de noviembre.">
<meta property="og:url" content="https://trollacos.com/gta-6/que-comprar/">
<meta property="og:image" content="https://trollacos.com/gta-6/que-comprar/portada.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
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
  <div class="etq">&gt; GUÍA DE COMPRA_</div>
  <h1>Qué necesitas para jugar a GTA VI (sin gastar de más)</h1>
  <p class="entradilla">Consola, espacio, tele, sonido y edición. Lo que de verdad hace falta para el 19 de noviembre y lo que es tirar el dinero, explicado para que lo entienda cualquiera.</p>
  <p class="fecha-act">Actualizado el 24 de octubre de 2026</p>
  <div class="troll-cab" aria-hidden="true"><img class="px troll" src="/img/trollaco-mando.png" data-hw="/img/trollaco-mando-hw.png" alt=""></div>
</header>
{body}
{foot}
<script>
if(document.documentElement.className.indexOf('halloween')>-1){{document.querySelectorAll('img.troll[data-hw]').forEach(function(i){{i.src=i.getAttribute('data-hw')}})}}
</script>
</body>
</html>
'''
os.makedirs('gta-6/que-comprar', exist_ok=True)
open('gta-6/que-comprar/index.html', 'w').write(page)
print('ok', len(page))
