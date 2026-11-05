"""Especial «Juegos de fútbol: de ISS a EA Sports FC» → /especiales/juegos-de-futbol/ (+ portada /especiales/ y sitemap).
Firma Danna. Datos con fuente citada por su nombre (sin enlaces a otras webs); la opinión es nuestra.
Portadas: campo 'portada' de cada ficha → /img/especiales/futbol/<slug>.webp (si no existe, sale un icono).
Uso: python3 _fuentes/generadores/especial_futbol.py   (desde cualquier sitio)"""
import os, html, json, re

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(RAIZ)
URL = '/especiales/juegos-de-futbol/'
FECHA = '5 de noviembre de 2026'
def esc(t): return html.escape(t, quote=True)

# ───────────────────────── línea del tiempo ─────────────────────────
TIEMPO = [
    ('1992', 'Simulador Profesional de Fútbol', 'Dinamic lanza en PC el abuelo de PC Fútbol.', 'pcfutbol'),
    ('1993', 'FIFA International Soccer', 'EA estrena la saga en Mega Drive el 15 de diciembre, con la licencia de la FIFA.', 'fifa'),
    ('1994', 'International Superstar Soccer', 'Konami (estudio de Osaka) saca el primer ISS en Super Nintendo.', 'iss'),
    ('1995', 'J.League Jikkyou Winning Eleven', 'El estudio de Konami en Tokio lanza en Japón el primer Winning Eleven para PlayStation.', 'we'),
    ('1996', 'PC Fútbol 5.0', '305.000 copias vendidas: España entera haciendo fichajes en el PC de casa.', 'pcfutbol'),
    ('1997', 'ISS Pro e ISS 64', 'Los dos equipos de Konami chocan: ISS Pro en PlayStation, ISS 64 en Nintendo 64.', 'iss'),
    ('1998', 'UEFA Champions League 98-99', 'Silicon Dreams y Eidos ponen el himno de la Champions en tu PlayStation.', 'champions'),
    ('1999', 'This Is Football', 'Sony entra en la pelea con su propio juego de fútbol (10 de diciembre).', 'tif'),
    ('2000', 'Ronaldo V-Football', 'El Fenómeno pone cara y nombre a un juego de Infogrames.', 'ronaldo'),
    ('2001', 'Pro Evolution Soccer', 'Nace el PES (en Japón, Winning Eleven 5) en PlayStation y PS2. Empieza la edad de oro.', 'pes'),
    ('2004', 'Football Kingdom', 'Namco prueba suerte en Japón con un juego de fútbol con licencia FIFPro.', 'fk'),
    ('2008', 'PES 2009', 'Primera entrega de PES con la licencia oficial de la Champions League.', 'pes'),
    ('2011', 'FIFA 12', 'Más de 3,2 millones de copias en su primera semana: récord de juego deportivo.', 'fifa'),
    ('2021', 'eFootball', 'Konami cambia PES por un free-to-play… y se estrella el día del estreno.', 'efootball'),
    ('2022', 'Adiós, FIFA', 'EA y la FIFA anuncian el 10 de mayo el fin de 30 años de matrimonio.', 'fifa'),
    ('2023', 'EA Sports FC 24', 'Primer juego de fútbol de EA sin el nombre «FIFA» en la portada.', 'eafc'),
]

# ───────────────────────── fichas ─────────────────────────
F = []
def ficha(slug, titulo, sub, anio, plataformas, estudio, icono, intro, datos, troll, fuentes, extra=''):
    F.append(dict(slug=slug, titulo=titulo, sub=sub, anio=anio, plataformas=plataformas, estudio=estudio, icono=icono,
                  intro=intro, datos=datos, troll=troll, fuentes=fuentes, extra=extra))

ficha('iss', 'International Superstar Soccer', 'El primer amor de Konami', '1994–2003', 'Super Nintendo, Nintendo 64, PlayStation 2…',
      'Konami (estudio de Osaka)', '⚽',
      'Antes de que existiera el PES, en muchas casas el fútbol de Konami se llamaba ISS. Salió en Super Nintendo en 1994 y '
      'en Nintendo 64 tuvo sus años de gloria con <em>International Superstar Soccer 64</em> (1997) e <em>ISS 98</em>. En Japón la saga '
      'se conocía como <em>Jikkyō World Soccer</em>. El último ISS salió en 2003.',
      ['Konami tenía <strong>dos equipos haciendo fútbol a la vez</strong>: el de Osaka con ISS y el de Tokio con Winning Eleven, cada uno con su propio juego.',
       '<em>ISS 98</em> salió en Japón como <em>Jikkyō World Soccer: World Cup France \'98</em>, con el Mundial de Francia de fondo.',
       'Al final ganó la línea de Tokio: de ella salieron ISS Pro y, después, el PES.'],
      'Yo aprendí a jugar con ISS 64. Bueno, aprendí a darle al botón de tiro muy fuerte y rezar.',
      ['Wikipedia (en inglés), «International Superstar Soccer»'])

ficha('winning-eleven', 'Winning Eleven e ISS Pro', 'El origen del PES', '1995–2001', 'PlayStation',
      'Konami (estudio de Tokio)', '🇯🇵',
      'El 21 de julio de 1995 salió en Japón <em>J.League Jikkyou Winning Eleven</em> para la primera PlayStation, con los 14 clubes de la J.League de aquel año. '
      'Aquí lo conocimos con otros nombres: <em>Goal Storm</em> y, sobre todo, <em>ISS Pro</em> (1997), el juego que hizo que media Europa '
      'se olvidara un rato de los demás.',
      ['En Japón la saga mantuvo siempre el nombre de <strong>Winning Eleven</strong>; en Europa pasó de ISS Pro a Pro Evolution Soccer.',
       'El primer PES de 2001 era, en Japón, <em>World Soccer: Winning Eleven 5</em>.',
       'ISS Pro Evolution fue el juego que convirtió el fútbol de Konami en un culto en los patios de colegio de toda Europa.'],
      'Lo de leer «Winning Eleven» en una revista japonesa importada era como enterarte de un secreto de Estado.',
      ['Wikipedia (en inglés), «Pro Evolution Soccer»'])

ficha('pes', 'Pro Evolution Soccer', 'La edad de oro', '2001–2020', 'PlayStation, PS2, PS3, PS4, PC, Xbox…',
      'Konami', '🔵',
      'Octubre de 2001: llega el primer <em>Pro Evolution Soccer</em> a PlayStation y PlayStation 2. Durante los años de PS2, el PES fue '
      'el rey para muchísimos jugadores: menos licencias que FIFA, pero un fútbol que se sentía de verdad. PES 5 y PES 6 todavía se '
      'nombran con la voz baja, como se habla de los grandes.',
      ['Según Konami, la saga había vendido <strong>111 millones de copias</strong> y sumaba <strong>400 millones de descargas</strong> en móvil a diciembre de 2020.',
       '<strong>PES 2009</strong> fue el primero con la licencia oficial de la Champions League; la tuvo hasta PES 2018.',
       'La Master League tenía sus propias leyendas inventadas. La más famosa, <strong>Castolo</strong>, el delantero brasileño que todos fichamos y todos recordamos.',
       'Desde PES 6 venía una liga de equipos genéricos totalmente editable, pensada para que tú pusieras los nombres reales.'],
      'Castolo no existe, pero metió más goles en mi Master League que todo el Madrid de los galácticos.',
      ['Wikipedia (en inglés), «Pro Evolution Soccer»', 'Konami Holdings, informe «Digital Entertainment Business» (diciembre de 2020)'])

ficha('fifa', 'FIFA', 'El gigante de EA', '1993–2022', 'De Mega Drive a PS5, PC, Xbox, Switch y móvil',
      'EA Sports (el primero, Extended Play Productions)', '🟢',
      'Todo empezó el 15 de diciembre de 1993 con <em>FIFA International Soccer</em> en Mega Drive. Treinta años después, FIFA era la saga '
      'de deportes más vendida del mundo. Su arma secreta siempre fue la misma: las licencias. Equipos, ligas, jugadores y estadios reales, '
      'mientras el resto se apañaba con nombres inventados.',
      ['Según Guinness World Records, la saga había vendido <strong>más de 325 millones de copias</strong> hasta 2021.',
       'Fue la primera saga de fútbol con licencia oficial de la FIFA.',
       '<strong>FIFA 12</strong> vendió más de 3,2 millones de copias y facturó más de 186 millones de dólares en su primera semana: récord de juego deportivo.',
       'Ya en 2000, según Guinness, FIFA había vendido más de 16 millones de copias.'],
      'Yo de pequeño elegía equipo por las equipaciones. FIFA me dejaba elegirlas todas. PES, a Man Red. Elegí con el corazón.',
      ['Wikipedia (en inglés), «FIFA (video game series)»', 'Guinness World Records'])

ficha('this-is-football', 'This Is Football', 'El fútbol de la casa Sony', '1999–2006', 'PlayStation, PlayStation 2, PSP',
      'Team Soho y London Studio (Sony)', '🎮',
      'Sony quiso tener su propio juego de fútbol y lo tuvo: <em>This Is Football</em> salió el 10 de diciembre de 1999 para la primera PlayStation. '
      'Lo hizo Team Soho, un estudio de Sony en Londres, y la saga siguió en PS2 con entregas anuales hasta mediados de los 2000. '
      'En Estados Unidos se llamaba <em>World Tour Soccer</em>.',
      ['Team Soho se fusionó con London Studio, que hizo las entregas siguientes.',
       'La mejor nota de la saga en Metacritic fue para <strong>This Is Football 2003</strong> (78 sobre 100).',
       'En 2010 la marca volvió como juego de gestión, <em>This Is Football Management</em>.'],
      'This Is Football venía en tantas demos de revista que me lo sabía de memoria sin haberlo comprado nunca.',
      ['Wikipedia (en inglés), «This Is Football»'])

ficha('champions', 'El juego de la Champions', 'El himno en tu consola', '1996–2007', 'PlayStation, PC, PS2, Xbox, GameCube, PSP, Xbox 360',
      'Krisalis, Silicon Dreams y EA', '⭐',
      'Hubo varios juegos oficiales de la Champions League. El que más recuerda la gente de aquí es el de <strong>Silicon Dreams</strong> para '
      'PlayStation y PC: <em>UEFA Champions League 98-99</em> (Eidos) y sus continuaciones de 1999-2000 (Eidos), 2000-01 y 2001-02 (Take-Two). '
      'Antes, en 1996, Krisalis había hecho <em>UEFA Champions League 1996/1997</em>. Y después EA sacó <em>UEFA Champions League 2004-2005</em> '
      'y <em>UEFA Champions League 2006-2007</em>.',
      ['Lo mejor que tenían: el ambiente de la competición, con su himno y su presentación de noche europea.',
       'La licencia de la Champions acabó dentro de otros juegos: en PES de 2009 a 2018 y luego en FIFA.',
       'Hoy la competición aparece como modo dentro de los juegos de EA.'],
      'Encender la consola, oír el himno de la Champions y ponerte de pie en el salón. Eso no lo da ningún pase de temporada.',
      ['Wikipedia (en inglés), «UEFA Champions League video games»'])

ficha('ronaldo', 'Ronaldo V-Football', 'El juego del Fenómeno', '2000', 'PlayStation (y Game Boy Color en EE. UU.)',
      'PAM Development · Infogrames', '🇧🇷',
      'En pleno auge del Fenómeno, Infogrames le hizo su propio juego: <em>Ronaldo V-Football</em>, para PlayStation en Europa en el año 2000. '
      'En Estados Unidos salió en Game Boy Color con el nombre de <em>Ronaldo V-Soccer</em>.',
      ['Es el único videojuego que Ronaldo apoyó en exclusiva.',
       'Traía <strong>176 selecciones</strong> y 15 estadios con día, noche y distintos climas.',
       'En PlayStation se podía jugar hasta a cuatro con el multitap.',
       'Su canción principal era un remix bailable de «Belo Horizonti».'],
      'Elegir a Brasil, pasarle el balón a Ronaldo y correr. Esa era toda mi táctica. Y funcionaba.',
      ['Wikipedia (en inglés), «Ronaldo V-Football»'])

ficha('football-kingdom', 'Football Kingdom', 'La joya japonesa de Namco', '2004', 'PlayStation 2 (Japón)',
      'Namco', '👑',
      'Este es para los que saben. <em>Football Kingdom</em> (en su caja, <em>Football Kingdom: Trial Edition</em>) lo sacó <strong>Namco</strong> '
      'en Japón el 27 de mayo de 2004 para PlayStation 2, a 4.179 yenes. Su idea: más libertad que Winning Eleven y FIFA, con un control '
      'pensado para hacer de todo con el balón. No llegó a salir en Europa, y por eso aquí es casi una leyenda.',
      ['Tenía licencia de <strong>FIFPro</strong>, así que salían los nombres reales de los jugadores.',
       'Su imagen era el japonés <strong>Shunsuke Nakamura</strong>.',
       'Presumía de una inteligencia artificial patentada para los jugadores sin balón («off the ball»).',
       'Con el stick derecho movías la línea defensiva para tirar el fuera de juego; las tácticas iban en los gatillos.'],
      'Football Kingdom es como ese amigo que dice que «conoció un grupo antes de que fuera famoso». Pero esta vez es verdad.',
      ['Game Watch (Impress), anuncio del 16 de abril de 2004', 'MobyGames, ficha de «Football Kingdom: Trial Edition»'])

ficha('efootball', 'eFootball', 'El cambio que salió regular', '2021–hoy', 'PS4, PS5, Xbox, PC, Android, iOS',
      'Konami', '📉',
      'En 2020 Konami anunció que el PES pasaba a llamarse eFootball y cambiaba de motor. El 30 de septiembre de 2021 salió <em>eFootball</em> '
      'como juego gratuito… y el estreno fue un desastre: animaciones rotas, caras raras y una lluvia de críticas.',
      ['El día de su salida, <strong>Kotaku</strong> lo llamó el juego más odiado de Steam y <strong>Rock, Paper, Shotgun</strong> lo situó como el peor valorado de la tienda.',
       'Konami lo ha ido parcheando desde entonces y sigue vivo como free-to-play.',
       'Con él se cerró la etapa de los PES de caja de cada año.'],
      'Lo del lanzamiento de eFootball fue como el capítulo 1 del Trollaco Run: zombis por todas partes. Pero sin gracia.',
      ['Wikipedia (en inglés), «Pro Evolution Soccer»', 'Kotaku y Rock, Paper, Shotgun (30 de septiembre de 2021)'])

ficha('ea-sports-fc', 'EA Sports FC', 'La vida sin la FIFA', '2023–hoy', 'PS4, PS5, Xbox, PC, Switch, móvil',
      'EA Sports', '🔄',
      'El 10 de mayo de 2022, EA y la FIFA anunciaron el fin de su acuerdo de 30 años. FIFA 23 fue el último con ese nombre y en 2023 llegó '
      '<em>EA Sports FC 24</em>: mismo fútbol de EA, mismas licencias de clubes y jugadores, pero sin la palabra «FIFA» en la portada.',
      ['Según EA, FC 24 superó los <strong>14,5 millones de jugadores</strong> en consola y PC en sus cuatro primeras semanas.',
       'La versión de móvil, FC Mobile, pasó de los 11 millones de instalaciones en sus diez primeros días.',
       'Las licencias de equipos y jugadores no eran de la FIFA, así que siguieron en el juego.'],
      'Cambiaron el nombre y yo seguí diciendo «echamos un FIFA». Hay cosas que no se cambian por contrato.',
      ['Game Developer, noviembre de 2023 (cifras de EA)', 'Wikipedia (en inglés), «FIFA (video game series)»'])

# ───────────────────────── PC Fútbol ─────────────────────────
PCF = '''
<p>Si eres de aquí y tuviste un PC en los noventa, esto no hace falta explicártelo. <strong>PC Fútbol</strong> no era un juego: era una forma de
vivir la temporada. Fichajes, entrenamientos, la base de datos con todos los jugadores de la Liga, las finanzas del club… y Michael Robinson
como cara visible de todo.</p>
<div class="cifras">
  <div><b>1992</b><span>Simulador Profesional de Fútbol, el abuelo</span></div>
  <div><b>305.000</b><span>copias de PC Fútbol 5.0 (1996)</span></div>
  <div><b>370.000</b><span>copias de PC Fútbol 7.0 (temporada 98/99)</span></div>
</div>
<h3>Cómo nació</h3>
<p>Lo hizo <strong>Dinamic</strong>, de los hermanos Ruiz (Pablo, Víctor, Nacho y Gaby), con Carlos Abril y con Pedro Sudón programando el simulador de
partidos. En 1992 salió el <em>Simulador Profesional de Fútbol</em>, que se considera la primera entrega. La primera con el nombre de la saga fue
<strong>PC Fútbol 2.0</strong>, para la temporada 93/94, ya con el sello Dinamic Multimedia.</p>
<h3>Michael Robinson</h3>
<p>El periodista y comentarista fue mucho más que la cara de la caja: también escribía los análisis de cada equipo que leíamos antes de cada fichaje.
Para toda una generación, la voz y las palabras de Robinson eran parte del juego.</p>
<h3>El precio y el éxito</h3>
<p>Uno de sus secretos era el precio: costaba más o menos la mitad que un juego de PC de la época. Así, PC Fútbol 5.0 vendió 305.000 copias y
PC Fútbol 7.0, 370.000. Son cifras enormes para el mercado español de entonces.</p>
<h3>El final y lo que vino después</h3>
<p>En marzo de 1999 el equipo original vendió su parte y se marchó a fundar <strong>FX Interactive</strong>. <em>PC Fútbol 2000</em> fue la primera
entrega sin ellos, y <em>PC Fútbol 2001</em> se retrasó hasta marzo y subió de precio. Años más tarde, el espíritu volvió con
<em>FX Fútbol</em> (2013) y con <em>Football Club Simulator 19</em> (2019), presentado como su sucesor espiritual.</p>
'''

# ───────────────────────── licencias y comunidad ─────────────────────────
LICENCIAS = '''
<p>Durante años, jugar al PES era aceptar que el Manchester United se llamaba otra cosa. FIFA tenía las licencias; Konami, el talento para
inventarse nombres. Algunos de los más recordados:</p>
<ul class="lista-nombres">
  <li><b>Man Red</b> (Manchester United) y <b>West London Blue</b> (Chelsea), en PES 4.</li>
  <li><b>Aragon</b> (Manchester United), <b>Europort</b> (Liverpool) y <b>Lake District</b> (West Ham), en PES 2.</li>
  <li>Los jugadores de la selección neerlandesa aparecieron en PES 2 bajo el equipo «Oranges».</li>
</ul>
<p>La gran baza de Konami llegó con <strong>PES 2009</strong>: la licencia oficial de la Champions League, que mantuvo hasta PES 2018. A partir de PES 2019, la
Champions se fue a EA. Y en 2022 la propia EA perdió el nombre «FIFA»… pero no las licencias de clubes y jugadores, que siguen en EA Sports FC.</p>
'''
COMUNIDAD = '''
<p>Si el PES sobrevivió tantos años sin licencias fue gracias a su comunidad. Había dos formas de arreglar el juego:</p>
<div class="cifras dos">
  <div><b>Option files</b><span>Archivos de datos que ponen los nombres reales a jugadores y equipos, meten los últimos fichajes y a veces retocan las medias.</span></div>
  <div><b>Parches</b><span>Modifican el juego para añadir equipos sin licencia, estadios, balones, botas y equipaciones.</span></div>
</div>
<p>Konami acabó cifrando los datos de equipaciones y estadísticas de sus últimas entregas… y la comunidad los acabó descifrando, como siempre.</p>
<p>Lo increíble es que esto <strong>sigue vivo</strong>: en el foro de Evo-Web hay un hilo dedicado al PES retro con cientos de páginas, y en Reddit
la comunidad r/WEPES sigue hablando de Winning Eleven y de los PES clásicos. PES 6 y PES 2013 se siguen jugando hoy con plantillas actualizadas
hechas por fans. En PC, la comunidad de FIFA también lleva años metiendo ligas, caras y equipaciones nuevas.</p>
<p class="aviso-c">🧯 Aquí no enlazamos descargas de parches ni de juegos: si te animas, usa siempre tu copia original y las comunidades oficiales de cada proyecto.</p>
'''

FUENTES = sorted({f for x in F for f in x['fuentes']} | {'Xataka, «PC Fútbol cumple 25 años» (18 de enero de 2019)'})

# ───────────────────────── página ─────────────────────────
g = open('gta-6/index.html', encoding='utf-8').read()
style = g[g.find('<style>'):g.find('</style>') + 8]
foot = g[g.find('<footer>'):g.find('</footer>') + 9]
extra = '''.esp{max-width:900px;margin:0 auto;padding:0 16px}
.esp p,.esp li{font-size:19px;line-height:1.65}
.esp h2{margin-top:44px;scroll-margin-top:16px}.esp h3{font-family:'Righteous',sans-serif;font-weight:400;font-size:24px;color:var(--yellow);margin:26px 0 8px}
.esp .k{font-family:'VT323',monospace;font-size:22px;color:var(--cyan)}
.hero-f{margin:14px 0 20px;padding:26px 22px;border:3px solid var(--pink);border-radius:18px;background:linear-gradient(135deg,rgba(255,43,214,.18),rgba(31,242,255,.10) 60%,rgba(7,2,26,.9));box-shadow:0 0 30px rgba(255,43,214,.35)}
.hero-f h1{margin:4px 0 10px;font-size:clamp(34px,7vw,56px);line-height:1.05;text-shadow:3px 3px 0 var(--pink),0 0 22px rgba(255,43,214,.6)}
.hero-f p{margin:0}
.firma{display:flex;gap:12px;align-items:center;margin:14px 0}
.firma img{width:56px;height:56px;border-radius:50%;border:2px solid var(--pink);object-fit:cover;flex:none}
.firma b{display:block;color:#fff}.firma span{font-size:15px;color:#d9d0f0}.firma a{color:var(--cyan)}
.indice{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}
.indice a{font-family:'VT323',monospace;font-size:20px;padding:5px 12px;border:2px solid var(--cyan);border-radius:20px;color:#fff;text-decoration:none;background:rgba(31,242,255,.07)}
.indice a:hover{background:rgba(31,242,255,.2)}
.tl{position:relative;margin:18px 0;padding-left:26px;border-left:3px solid var(--pink)}
.tl li{list-style:none;position:relative;margin:0 0 14px;padding:10px 14px;border-radius:12px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08)}
.tl li::before{content:'';position:absolute;left:-36px;top:16px;width:15px;height:15px;border-radius:50%;background:var(--yellow);box-shadow:0 0 10px var(--yellow)}
.tl .a{font-family:'VT323',monospace;font-size:24px;color:var(--yellow);margin-right:8px}
.tl b{color:#fff}.tl span{display:block;font-size:17px;color:#d9d0f0}
.tl a{color:inherit;text-decoration:none}
.ficha-j{margin:22px 0;padding:20px;border:2px solid rgba(31,242,255,.55);border-radius:18px;background:rgba(31,242,255,.05);scroll-margin-top:16px}
.ficha-j .cab{display:grid;grid-template-columns:110px 1fr;gap:18px;align-items:center}
.ficha-j .port{width:110px;aspect-ratio:3/4;border-radius:10px;border:2px solid var(--pink);display:flex;align-items:center;justify-content:center;font-size:52px;background:linear-gradient(160deg,#2a0845,#07021a);overflow:hidden}
.ficha-j .port img{width:100%;height:100%;object-fit:cover;display:block}
.ficha-j h2{margin:0;font-size:30px}.ficha-j .sub{font-family:'VT323',monospace;font-size:21px;color:var(--pink)}
.ficha-j dl{display:grid;grid-template-columns:auto 1fr;gap:2px 10px;margin:8px 0 0;font-size:16px}
.ficha-j dt{font-family:'VT323',monospace;font-size:18px;color:var(--cyan)}.ficha-j dd{margin:0;color:#eee}
.flipar{margin:14px 0;padding:14px 16px 6px;border-left:5px solid var(--yellow);background:rgba(255,210,63,.07);border-radius:0 12px 12px 0}
.flipar b.t{display:block;font-family:'VT323',monospace;font-weight:400;font-size:22px;color:var(--yellow)}
.flipar ul{margin:6px 0;padding-left:20px}.flipar li{font-size:17px;margin-bottom:6px}
.nota{display:flex;gap:14px;align-items:flex-start;margin:16px 0;padding:14px 16px;border:2px dashed var(--yellow);border-radius:12px;background:rgba(255,210,63,.07)}
.nota img{width:44px;image-rendering:pixelated;flex:none}.nota p{margin:0;font-size:17px}.nota b{color:var(--yellow)}
.nota.pri{border-color:var(--pink);background:rgba(255,43,214,.08)}.nota.pri b{color:var(--pink)}
.fu{font-size:14px;color:#a9a0c9;margin:6px 0 0}
.bloque-pcf{margin:22px 0;padding:22px;border:3px solid var(--yellow);border-radius:18px;background:linear-gradient(135deg,rgba(255,210,63,.12),rgba(7,2,26,.85));scroll-margin-top:16px}
.cifras{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:16px 0}
.cifras.dos{grid-template-columns:1fr 1fr}
.cifras div{padding:14px;border-radius:14px;background:rgba(7,2,26,.7);border:2px solid var(--pink);text-align:center}
.cifras b{display:block;font-family:'Righteous',sans-serif;font-weight:400;font-size:30px;color:var(--yellow);text-shadow:2px 2px 0 var(--pink)}
.cifras span{font-size:15px;color:#e6dff7;line-height:1.35;display:block;margin-top:4px}
.cifras.dos b{font-size:24px}.cifras.dos span{text-align:left}
.lista-nombres li{margin-bottom:6px}
.aviso-c{font-size:16px;padding:10px 14px;border-radius:10px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12)}
.reto-f{margin:34px 0;padding:22px;text-align:center;border:3px solid var(--cyan);border-radius:18px;background:rgba(31,242,255,.07);box-shadow:0 0 24px rgba(31,242,255,.3)}
.reto-f p{margin:0 0 14px;font-family:'Righteous',sans-serif;font-size:26px}
.migas{font-family:'VT323',monospace;font-size:18px;color:#bdb3d9}.migas a{color:#bdb3d9}
.fuentes-l li{font-size:15px;line-height:1.5;color:#bdb3d9}
@media(max-width:700px){.cifras{grid-template-columns:1fr}.cifras.dos{grid-template-columns:1fr}.ficha-j .cab{grid-template-columns:84px 1fr;gap:14px}.ficha-j .port{width:84px;font-size:40px}.esp p,.esp li{font-size:18px}}
</style>'''
style2 = style.replace('</style>', extra)

def portada(x):
    p = f'img/especiales/futbol/{x["slug"]}.webp'
    if os.path.exists(p):
        return f'<div class="port"><img src="/{p}" alt="Portada de {esc(x["titulo"])}" width="220" height="293" loading="lazy"></div>'
    return f'<div class="port" aria-hidden="true">{x["icono"]}</div>'

def html_ficha(x):
    datos = ''.join(f'<li>{d}</li>' for d in x['datos'])
    fu = ' · '.join(esc(f) for f in x['fuentes'])
    pie = '<p class="fu">Portada © sus titulares.</p>' if os.path.exists(f'img/especiales/futbol/{x["slug"]}.webp') else ''
    return f'''<section class="ficha-j" id="{x['slug']}">
<div class="cab">{portada(x)}<div><span class="sub">&gt; {esc(x['sub'].upper())}_</span><h2>{esc(x['titulo'])}</h2>
<dl><dt>AÑOS</dt><dd>{x['anio']}</dd><dt>DÓNDE</dt><dd>{esc(x['plataformas'])}</dd><dt>QUIÉN</dt><dd>{esc(x['estudio'])}</dd></dl></div></div>
<p>{x['intro']}</p>
<div class="flipar"><b class="t">🤯 DATOS PARA FLIPAR</b><ul>{datos}</ul></div>
<div class="nota"><img src="/img/trollaco.png" alt=""><p><b>EL TROLLACO OPINA:</b> {esc(x['troll'])}</p></div>
{pie}<p class="fu">Fuentes: {fu}.</p>
</section>'''

def tl_item(a, t, d, ancla):
    return f'<li><a href="#{ancla}"><span class="a">{a}</span><b>{esc(t)}</b><span>{esc(d)}</span></a></li>'
ANCLAS = {'pcfutbol': 'pc-futbol', 'we': 'winning-eleven', 'tif': 'this-is-football', 'fk': 'football-kingdom', 'eafc': 'ea-sports-fc'}
tl = ''.join(tl_item(a, t, d, ANCLAS.get(k, k)) for a, t, d, k in TIEMPO)
indice = ''.join(f'<a href="#{i}">{t}</a>' for i, t in [('linea', '🕰️ Línea del tiempo'), ('pc-futbol', '💾 PC Fútbol'), ('iss', 'ISS'), ('winning-eleven', 'Winning Eleven'),
    ('pes', 'PES'), ('fifa', 'FIFA'), ('this-is-football', 'This Is Football'), ('champions', 'Champions'), ('ronaldo', 'Ronaldo V-Football'),
    ('football-kingdom', 'Football Kingdom'), ('efootball', 'eFootball'), ('ea-sports-fc', 'EA Sports FC'), ('licencias', '🏷️ Licencias'), ('comunidad', '🛠️ Parches y mods')])
FIRMA = ('<div class="firma"><img src="/img/danna.jpg?v=3" alt="Danna" width="56" height="56"><div><b>Por Danna</b>'
         f'<span>Tu reportera del otro lado de la pantalla · <a href="https://www.instagram.com/dannapixel/" target="_blank" rel="noopener">📸 @dannapixel</a> · <a href="/danna/">¿Quién es?</a> · {FECHA}</span></div></div>')
orden = ['iss', 'winning-eleven', 'pes', 'fifa', 'this-is-football', 'champions', 'ronaldo', 'football-kingdom', 'efootball', 'ea-sports-fc']
fichas = ''.join(html_ficha(next(x for x in F if x['slug'] == s)) for s in orden)
fuentes = ''.join(f'<li>{esc(f)}</li>' for f in FUENTES)

titulo = 'De ISS a EA Sports FC: la historia de los juegos de fútbol'
desc = 'El especial más nostálgico de Trollacos: PES, FIFA, Winning Eleven, ISS, PC Fútbol, This Is Football, la Champions, Ronaldo V-Football, Football Kingdom, eFootball y EA FC. Datos, ventas, licencias, parches y comunidad.'
cuerpo = f'''<p class="migas"><a href="/">Portada</a> › <a href="/especiales/">Especiales</a> › Juegos de fútbol</p>
<div class="hero-f"><p class="k">&gt; ESPECIAL TROLLACOS_</p><h1>De ISS a EA Sports FC: la historia de los juegos de fútbol</h1>
<p>Treinta y pico años de mandos destrozados, piques en el sofá y Master Leagues hasta las tantas. Del <em>Simulador Profesional de Fútbol</em> al último EA FC,
pasando por el PES de la PS2, el PC Fútbol de Michael Robinson y una joya japonesa que casi nadie jugó aquí.</p></div>
{FIRMA}
<p>Os lo debía. Este especial va de los juegos con los que crecimos, de los que nos peleábamos por el mando y de los que se siguen jugando hoy gracias a
una comunidad que no se rinde. Datos con su fuente, opinión nuestra y mucha nostalgia. Coge sitio, que empieza el partido. ⚽</p>
<nav class="indice" aria-label="Índice">{indice}</nav>
<h2 id="linea">🕰️ La línea del tiempo</h2>
<ul class="tl">{tl}</ul>
<div class="nota pri"><img src="/img/princesa.png" alt=""><p><b>LA PRINCESA NEÓN OPINA:</b> Yo era de las que elegía el equipo por el color de la camiseta y ganaba igual. Que no se entere Glitch, que luego se pica.</p></div>
<section class="bloque-pcf" id="pc-futbol"><p class="k">&gt; HECHO EN ESPAÑA_</p><h2 style="margin-top:4px">💾 PC Fútbol: el juego que nos hizo presidentes</h2>
{PCF}
<div class="nota"><img src="/img/trollaco.png" alt=""><p><b>EL TROLLACO OPINA:</b> Yo fiché a cuatro delanteros, me quedé sin dinero para pagar la luz del estadio y bajé a Segunda. Como en la vida misma.</p></div>
<p class="fu">Fuente: Xataka, «PC Fútbol cumple 25 años» (18 de enero de 2019).</p></section>
<h2>🎮 Las sagas, una a una</h2>
{fichas}
<h2 id="licencias">🏷️ La guerra de las licencias</h2>
{LICENCIAS}
<p class="fu">Fuente: Wikipedia (en inglés), «Pro Evolution Soccer» y «FIFA (video game series)».</p>
<h2 id="comunidad">🛠️ Parches, mods y la comunidad que no se rinde</h2>
{COMUNIDAD}
<p class="fu">Fuentes: Wikipedia (en inglés), «Pro Evolution Soccer»; foro Evo-Web («The Retro-PES Corner»); Reddit, r/WEPES.</p>
<div class="reto-f"><p>¿Y tú sabes de fútbol de verdad, o solo de mando? ⚽</p><a class="btn" href="/porra/">DEMUÉSTRALO EN LA PORRA</a></div>
<h2>📚 Fuentes de los datos</h2>
<p style="font-size:16px">Los datos salen de estas fuentes, citadas por su nombre. La opinión, las bromas y la nostalgia son nuestras.</p>
<ul class="fuentes-l">{fuentes}</ul>
<p class="fu">FIFA, PES, eFootball, EA Sports FC, PC Fútbol y el resto de nombres y marcas citados son de sus respectivos dueños. Trollacos no tiene relación con ellos.</p>'''

ld = {'@context': 'https://schema.org', '@type': 'Article', 'headline': titulo, 'datePublished': '2026-11-05',
      'author': {'@type': 'Person', 'name': 'Danna', 'url': 'https://trollacos.com/danna/'},
      'publisher': {'@type': 'Organization', 'name': 'Trollacos'}, 'description': desc}

def pagina(titulo, desc, u, cuerpo, ld=None, volver=('/', '‹ PORTADA')):
    j = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ''
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)} | Trollacos</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="https://trollacos.com{u}">
<meta property="og:title" content="{esc(titulo)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:image" content="https://trollacos.com/img/danna-setup.webp?v=2">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/icono.png">
{style2}
{j}
</head><body>
<div class="scan"></div>
<nav class="top"><a href="/"><img class="px" src="/logo.webp" alt="Trollacos" width="1600" height="161"></a><a href="{volver[0]}">{volver[1]}</a></nav>
<main class="esp">
{cuerpo}
</main>
{foot}
</body></html>'''

def guarda(ruta, txt):
    os.makedirs(ruta, exist_ok=True)
    open(os.path.join(ruta, 'index.html'), 'w', encoding='utf-8').write(txt)

guarda('especiales/juegos-de-futbol', pagina(titulo, desc, URL, cuerpo, ld, volver=('/especiales/', '‹ ESPECIALES')))

# portada de especiales
hub = f'''<p class="migas"><a href="/">Portada</a> › Especiales</p>
<div class="hero-f"><p class="k">&gt; ESPECIALES TROLLACOS_</p><h1>Especiales</h1><p>Contenido largo, nostálgico y con datos: para leer con calma y con el mando cerca.</p></div>
<section class="ficha-j"><div class="cab"><div class="port" aria-hidden="true">⚽</div><div><span class="sub">&gt; NUEVO_</span><h2><a href="{URL}" style="color:#fff">{esc(titulo)}</a></h2>
<p style="margin:6px 0 0;font-size:17px">{esc(desc)}</p><p style="margin:12px 0 0"><a class="btn" href="{URL}">LEER EL ESPECIAL</a></p></div></div></section>'''
guarda('especiales', pagina('Especiales de Trollacos', 'Especiales largos y nostálgicos de Trollacos sobre videojuegos.', '/especiales/', hub))

sm = open('sitemap.xml', encoding='utf-8').read()
nuevas = ''.join(f'  <url><loc>https://trollacos.com{u}</loc><changefreq>monthly</changefreq></url>\n' for u in ('/especiales/', URL) if f'https://trollacos.com{u}<' not in sm)
if nuevas: open('sitemap.xml', 'w', encoding='utf-8').write(sm.replace('</urlset>', nuevas + '</urlset>'))
print(f'especial fútbol: {len(F)} fichas + PC Fútbol, {len(TIEMPO)} hitos, {len(FUENTES)} fuentes')
