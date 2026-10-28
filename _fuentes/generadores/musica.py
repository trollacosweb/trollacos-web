import urllib.parse, html, json, os
os.chdir('/home/claude/trollacos-web')
g = open('gta-6/index.html').read()
style = g[g.find('<style>'):g.find('</style>') + 8]
foot = g[g.find('<footer>'):g.find('</footer>') + 9]
extra = (".yt-btn{display:inline-block;white-space:nowrap;font-family:'VT323',monospace;font-size:19px;text-decoration:none;color:#fff;"
         "background:#1db954;color:#07120b;padding:3px 11px;border-radius:5px;box-shadow:0 0 10px rgba(29,185,84,.45)}\n"
         ".yt-btn:hover{background:#2be06a}\ntd{font-size:17.5px}\n"
         ".destacado{border:2px solid var(--pink);border-radius:10px;padding:18px;background:linear-gradient(135deg,rgba(255,43,214,.12),rgba(31,242,255,.06));margin:8px 0 18px}\n"
         ".destacado h3{font-size:26px}\n"
         ".migas{font-family:'VT323',monospace;font-size:20px;margin:24px 0 0;color:var(--muted)}.migas a{color:var(--cyan);text-decoration:none}\n</style>")
style2 = style.replace('</style>', extra)


def yt(a, s):
    return 'https://open.spotify.com/search/' + urllib.parse.quote(f'{a.split(" (feat")[0]} {s}')


def tabla(lista):
    filas = '\n'.join(
        f'      <tr><td><strong>{html.escape(s)}</strong></td><td>{html.escape(a)}</td>'
        f'<td><a class="yt-btn" href="{yt(a, s)}" target="_blank" rel="noopener">▶ Spotify</a></td></tr>'
        for a, s in lista)
    return ('  <div class="tabla"><table>\n      <tr><th>Canción</th><th>Artista</th><th>Escuchar</th></tr>\n'
            + filas + '\n  </table></div>')


album = [("Justice (feat. Tame Impala, SZA, King Gizzard & The Lizard Wizard)", "Flower in a Hurricane"),
         ("Yung Lean (feat. Future & Metro Boomin)", "That's It"), ("Travis Scott", "RHYNO"),
         ("CA7RIEL & Paco Amoroso, PinkPantheress, Fred again.. & Étienne de Crécy", "Sexy Magic"),
         ("Morgan Wallen", "Last Thing You Need"), ("Fuerza Regida", "Suzuki"), ("Rauw Alejandro", "Macacoa 2000"),
         ("Cardi B", "Don't Chart"), ("Keith Richards", "Bright Lights, Big City")]
trailers = [("Tom Petty", "Love Is a Long Road"), ("The Pointer Sisters", "Hot Together"),
            ("Wang Chung", "Everybody Have Fun Tonight"), ("Tammy Wynette", "Talkin' to Myself Again"),
            ("Zenglen", "Child Support")]
ext = [("Birdman (feat. Lil Wayne)", "Pop Bottles"), ("Sexyy Red & Tay Keith", "Pound Town"), ("Kodak Black", "Skrilla"),
       ("The Bellamy Brothers", "Let Your Love Flow"), ("Def Leppard", "Love Bites"), ("Depeche Mode", "People Are People"),
       ("Captain & Tennille", "But I Think It's a Dream"), ("Prefab Sprout", "Cars and Girls"),
       ("!!! (feat. Meah Pace)", "Off the Grid"), ("Cliff Richard", "Devil Woman"),
       ("Chimbala & Omega", "Se Me Nota (Agárrame)"), ("Phil Collins", "Against All Odds (Take a Look at Me Now)"),
       ("Aluna & Jayda G", "Mine O' Mine"), ("Bob Moses & Elderbrook", "Inner Light")]
radios = [("💃", "Cocoteo", "Música latina actual", "El Martillo y La Gata"),
          ("🤠", "Back Country", "Country con espíritu gamberro", "MW y Delta Dawne"),
          ("🌍", "Afro Bank FM", "Amapiano, clásicos africanos, 3-step y más", "Burna y Palmsy"),
          ("🤘", "The Chamber", "Metal", "DJ Kerry y DJ Tom"),
          ("✨", "Flash FM", "Pop. Una institución de Vice City", "Robyn y Alex"),
          ("🎤", "Dirty South Classics", "Clásicos del rap y hip-hop del sur", "Trick y Trina")]
total = len(album) + len(trailers) + len(ext)
radio_html = '\n'.join(
    f'    <div class="zona"><span class="n">{e}</span><div><h3>{n}</h3><small>{gen.upper()}</small><p>Presentan: {h}</p></div></div>'
    for e, n, gen, h in radios)
faq = [("¿Cuál es la canción principal de GTA 6?",
        "«Flower in a Hurricane», de Justice con Tame Impala, SZA y King Gizzard & The Lizard Wizard. Justice también compone la banda sonora original del juego."),
       ("¿Cuántas canciones tiene GTA VI: The Album?",
        "34 canciones originales. Sale el 19 de noviembre de 2026, el mismo día que el juego, en digital, CD y vinilo."),
       ("¿Qué canción suena en el primer tráiler de GTA 6?", "«Love Is a Long Road», de Tom Petty."),
       ("¿Qué canción suena en el segundo tráiler de GTA 6?", "«Hot Together», de The Pointer Sisters."),
       ("¿Qué emisoras de radio tendrá GTA 6?",
        "Rockstar ha presentado seis: Cocoteo, Back Country, Afro Bank FM, The Chamber, Flash FM y Dirty South Classics. Habrá más.")]
faq_html = '\n'.join(f'  <details><summary>{q}</summary><p>{html.escape(a)}</p></details>' for q, a in faq)
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "Article", "headline": "Canciones de GTA 6: todas las confirmadas", "datePublished": "2026-10-23",
     "dateModified": "2026-10-23", "inLanguage": "es", "author": {"@type": "Organization", "name": "Trollacos"},
     "publisher": {"@type": "Organization", "name": "Trollacos",
                   "logo": {"@type": "ImageObject", "url": "https://trollacos.com/icono-512.png"}},
     "mainEntityOfPage": "https://trollacos.com/gta-6/musica/"},
    {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a.replace('«', '"').replace('»', '"')}}
        for q, a in faq]}]}

hw = "<script>(function(){var d=new Date(),m=d.getMonth(),n=d.getDate();if((m===9&&n>=15)||(m===10&&n<=2))document.documentElement.className+=' halloween'})()</script>"
swap = "if(document.documentElement.className.indexOf('halloween')>-1){document.querySelectorAll('img.troll[data-hw]').forEach(function(i){i.src=i.getAttribute('data-hw')})}"

page = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{hw}
<title>Canciones de GTA 6: banda sonora, emisoras y el álbum ({total} temas confirmados) | Trollacos</title>
<meta name="description" content="Todas las canciones confirmadas de GTA VI: el tema de Justice, GTA VI: The Album, la música de los tráilers y del vistazo extendido, y las emisoras de radio. Con enlace para escucharlas en Spotify.">
<link rel="canonical" href="https://trollacos.com/gta-6/musica/">
<meta property="og:type" content="article">
<meta property="og:title" content="Canciones de GTA 6: todas las confirmadas | Trollacos">
<meta property="og:description" content="Banda sonora, emisoras de radio y el álbum oficial de GTA VI, con enlaces para escucharlas.">
<meta property="og:url" content="https://trollacos.com/gta-6/musica/">
<meta property="og:image" content="https://trollacos.com/gta-6/musica/portada.jpg">
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
  <a href="/gta-6/">‹ GUÍA GTA VI</a>
</nav>
<header class="cab">
  <div class="etq">&gt; GUÍA TROLLACOS · MÚSICA_</div>
  <h1>Canciones de GTA 6: todas las confirmadas</h1>
  <p class="entradilla">El tema principal, el álbum oficial, lo que suena en los tráilers y las emisoras de radio. {total} canciones confirmadas, cada una con su enlace para escucharla en Spotify.</p>
  <p class="fecha-act">Actualizado el 23 de octubre de 2026 · La ampliaremos el 19 de noviembre</p>
  <div class="troll-cab" aria-hidden="true"><img class="px troll" src="/img/trollaco.png" data-hw="/img/trollaco-calabaza-hw.png" alt=""></div>
</header>
<main>
  <p class="migas"><a href="/">Trollacos</a> › <a href="/gta-6/">Guía GTA VI</a> › Música</p>
  <nav class="indice" aria-label="Índice">
    <b>&gt; ÍNDICE</b>
    <ol>
      <li><a href="#tema">El tema principal</a></li>
      <li><a href="#album">GTA VI: The Album</a></li>
      <li><a href="#trailers">Canciones de los tráilers</a></li>
      <li><a href="#extendido">Canciones del vistazo extendido</a></li>
      <li><a href="#radio">Las emisoras de radio</a></li>
      <li><a href="#faq">Preguntas rápidas</a></li>
    </ol>
  </nav>

  <h2 id="tema">El tema principal</h2>
  <div class="destacado">
    <span style="font-family:'VT323',monospace;font-size:19px;color:var(--orange)">CANCIÓN DEL TRÁILER DE LANZAMIENTO</span>
    <h3>Flower in a Hurricane</h3>
    <p style="margin:6px 0 12px">De <strong>Justice</strong>, con <strong>Tame Impala, SZA y King Gizzard &amp; The Lizard Wizard</strong>. Justice, el dúo francés de electrónica, es además el encargado de la <strong>banda sonora original</strong> del juego.</p>
    <a class="yt-btn" href="{yt('Justice', 'Flower in a Hurricane')}" target="_blank" rel="noopener">▶ Escuchar en Spotify</a>
  </div>

  <h2 id="album">GTA VI: The Album</h2>
  <p>Es el disco oficial del juego: <strong>34 canciones originales</strong> hechas para GTA VI. Sale el <strong>19 de noviembre</strong>, el mismo día que el juego, en digital, CD y vinilo. De momento se han publicado estos adelantos:</p>
{tabla(album)}
  <p><a class="amz" href="https://www.amazon.es/s?k=Grand+Theft+Auto+VI+The+Album+vinilo&amp;tag=trollacos-21" target="_blank" rel="sponsored nofollow noopener">💿 Buscar el vinilo y el CD en Amazon</a></p>
  <p class="afil">Enlace de afiliado: si compras desde aquí, Trollacos se lleva una pequeña comisión sin que a ti te cueste más.</p>

  <h2 id="trailers">Canciones de los tráilers</h2>
  <p>Las que han sonado en los tráilers oficiales 1 y 2. La de Tom Petty puso la piel de gallina a medio planeta en 2023.</p>
{tabla(trailers)}

  <h2 id="extendido">Canciones del vistazo extendido</h2>
  <p>En el vídeo de unos 26 minutos de juego real que se estrenó en agosto suenan estas canciones en la radio de los coches y en los locales. Ojo: Rockstar no ha confirmado en qué emisora irá cada una.</p>
{tabla(ext)}
  <div class="troll-dice"><img class="px troll" src="/img/trollaco-mando.png" data-hw="/img/trollaco-mando-hw.png" alt=""><p>El Trollaco opina: Phil Collins a todo volumen en un descapotable por Vice City. No hay más preguntas, señoría.</p></div>

  <h2 id="radio">Las emisoras de radio</h2>
  <p>Rockstar ha presentado seis emisoras, cada una con sus locutores. Habrá más (rock clásico, tertulias y pódcast), pero aún no tienen nombre oficial.</p>
  <div class="zonas">
{radio_html}
  </div>

  <h2 id="faq">Preguntas rápidas</h2>
{faq_html}

  <p class="ojo">Lista hecha con la información oficial de Rockstar y las canciones identificadas por medios especializados en los vídeos publicados. Los botones buscan cada canción en Spotify. Fuentes: <a href="https://www.rockstargames.com/VI/music" target="_blank" rel="noopener">música de GTA VI (Rockstar)</a>, <a href="https://www.gamespot.com/articles/gta-6-soundtrack-all-confirmed-songs-so-far/" target="_blank" rel="noopener">GameSpot</a>, <a href="https://www.redbull.com/us-en/gta-6-soundtrack-songs-music-radio" target="_blank" rel="noopener">Red Bull</a>, <a href="https://www.vice.com/en/article/every-song-confirmed-in-gta6-extended-look/" target="_blank" rel="noopener">VICE</a>. Trollacos no tiene relación con Rockstar Games ni con Take-Two Interactive.</p>
  <p style="text-align:center;margin-top:26px"><a href="/gta-6/" style="font-family:'VT323',monospace;font-size:24px;color:var(--cyan)">‹ Volver a la guía completa de GTA VI</a></p>
</main>
{foot}
<script>
{swap}
</script>
</body>
</html>
'''
open('gta-6/musica/index.html', 'w').write(page)
print(total)
