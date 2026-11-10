"""Especial «De Monkey Island a Runaway: la historia de las aventuras gráficas» → /especiales/aventuras-graficas/ (+ portada /especiales/ y sitemap).
Firma Danna. Datos con fuente citada por su nombre (sin enlaces a otras webs); la opinión es nuestra.
Portadas: /img/especiales/aventuras/<slug>.webp (si no existe, sale un icono).
Uso: python3 _fuentes/generadores/especial_aventuras.py   (desde cualquier sitio)"""
import os, html, json

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(RAIZ)
URL = '/especiales/aventuras-graficas/'
FECHA = '10 de noviembre de 2026'
IMG = 'img/especiales/aventuras'
def esc(t): return html.escape(t, quote=True)
WP = 'Wikipedia (en inglés), '

# ───────────────────────── línea del tiempo ─────────────────────────
TIEMPO = [
    ('1976', 'Colossal Cave Adventure', 'Will Crowther escribe en un ordenador central una aventura de texto inspirada en las cuevas de Kentucky. Le da nombre al género.', 'origenes'),
    ('1977', 'Zork', 'Unos estudiantes del MIT empiezan su propia aventura de texto, que acabaría vendiendo Infocom.', 'origenes'),
    ('1980', 'Mystery House', 'Roberta y Ken Williams le ponen dibujos a una aventura. Nace la aventura gráfica… y nace Sierra.', 'mystery-house'),
    ('1984', 'King\'s Quest', 'Sierra pone a andar al protagonista por la pantalla. El rey Graham empieza su reinado.', 'kings-quest'),
    ('1987', 'Maniac Mansion y La abadía del crimen', 'LucasArts estrena el SCUMM y en España Opera Soft saca su abadía.', 'maniac-mansion'),
    ('1988', 'Aventuras AD', 'Andrés Samudio funda en Valencia el sello de aventuras de texto de Dinamic.', 'espana'),
    ('1990', 'The Secret of Monkey Island', 'Guybrush Threepwood quiere ser pirata. El resto es historia.', 'monkey-island'),
    ('1992', 'Indiana Jones and the Fate of Atlantis', 'La aventura más vendida de LucasArts: más de un millón de copias.', 'indiana-jones-atlantis'),
    ('1993', 'Day of the Tentacle, Myst y Gabriel Knight', 'El año más bestia del género: tentáculos, islas misteriosas y vudú en Nueva Orleans.', 'day-of-the-tentacle'),
    ('1994', 'Igor: Objetivo Uikokahonia', 'Pendulo Studios firma la primera aventura gráfica hecha en España.', 'igor'),
    ('1996', 'Broken Sword y Dráscula', 'Templarios en París (el primero de cinco Broken Sword) y un vampiro muy español.', 'broken-sword'),
    ('1997', 'Hollywood Monsters y The Curse of Monkey Island', 'Dinamic Multimedia lanza el gran éxito de Pendulo; Guybrush se hace dibujo animado.', 'hollywood-monsters'),
    ('1998', 'Grim Fandango', 'La obra maestra que no vendió lo suficiente… y el principio del fin de LucasArts en el género.', 'grim-fandango'),
    ('2001', 'Runaway y la caída de Dinamic Multimedia', 'Sale Runaway en julio; en septiembre Dinamic anuncia su liquidación.', 'runaway'),
    ('2009', 'Machinarium', 'Un robot checo sin una sola palabra de diálogo demuestra que el género sigue vivo.', 'machinarium'),
    ('2012', 'Double Fine Adventure y The Walking Dead', 'Kickstarter salva la aventura clásica y Telltale la convierte en drama.', 'broken-age'),
    ('2017', 'Thimbleweed Park', 'Ron Gilbert y Gary Winnick vuelven a los 80… a propósito.', 'thimbleweed-park'),
    ('2022', 'Return to Monkey Island', 'Treinta y un años después, Gilbert vuelve a la isla de los monos.', 'return-to-monkey-island'),
]

# ───────────────────────── fichas ─────────────────────────
F = []
def ficha(slug, titulo, sub, anio, plataformas, estudio, icono, intro, datos, troll, fuentes):
    F.append(dict(slug=slug, titulo=titulo, sub=sub, anio=anio, plataformas=plataformas, estudio=estudio, icono=icono,
                  intro=intro, datos=datos, troll=troll, fuentes=fuentes))

# ── Los orígenes ──
ficha('mystery-house', 'Mystery House', 'La primera con dibujos', '1980', 'Apple II', 'On-Line Systems (luego Sierra) · Roberta y Ken Williams', '🏚️',
      'Una mansión victoriana, siete invitados, unas joyas escondidas… y cadáveres que van apareciendo. Roberta Williams escribió y dibujó la historia, '
      'y su marido Ken la programó. Hasta entonces las aventuras eran solo texto: esta fue la primera aventura con gráficos.',
      ['Salió el <strong>5 de mayo de 1980</strong> y se vendía por correo: superó las <strong>10.000 copias</strong>, y con la reedición de 1982 llegó a unas <strong>80.000</strong>.',
       'Está considerada también uno de los <strong>primeros juegos de terror</strong> de la historia.',
       'En <strong>1987</strong>, por su séptimo aniversario, Sierra lo liberó como <strong>dominio público</strong>.',
       'Sus dibujos eran líneas blancas sobre fondo negro. Y aun así daba mal rollo.'],
      'Lo de matar invitados uno a uno en una mansión lo inventó Roberta Williams antes que muchos guionistas de Netflix.',
      [WP + '«Mystery House»'])

ficha('kings-quest', 'King\'s Quest', 'Sierra pone a andar al héroe', '1984', 'IBM PCjr, MS-DOS, Amiga, Atari ST, Master System…', 'Sierra On-Line · Roberta Williams', '👑',
      'Sir Graham tiene que salvar el reino de Daventry para convertirse en rey. Escribías las órdenes con el teclado («abrir puerta», «coger llave»), '
      'y el protagonista se movía por escenarios dibujados y animados, algo revolucionario entonces.',
      ['Salió el <strong>10 de mayo de 1984</strong> y se hizo, en origen, para el <strong>IBM PCjr</strong>.',
       'Usaba el motor <strong>AGI</strong> (<em>Adventure Game Interpreter</em>) de Sierra; el remake de 1990 ya iba con el nuevo SCI.',
       'Abrió una saga larguísima y convirtió a Roberta Williams en una de las diseñadoras más importantes de la historia.',
       'Hasta salió en <strong>Master System</strong>, en 1989.'],
      'Escribir «coger cubo» siete veces porque el juego quería «coge el cubo» era el Dark Souls de 1984.',
      [WP + '«King\'s Quest I»'])

ficha('space-quest', 'Space Quest', 'El conserje que salvó la galaxia', '1986–1995', 'MS-DOS, Amiga, Atari ST, Mac…', 'Sierra On-Line · Mark Crowe y Scott Murphy', '🧹',
      'Roger Wilco es conserje en una nave espacial y lucha «por la verdad, la justicia y los suelos bien limpios». Salva el universo casi siempre por accidente, '
      'y casi siempre acaba castigado por alguna tontería. Seis juegos de parodia de <em>Star Wars</em> y <em>Star Trek</em>.',
      ['Sus creadores se hacían llamar <strong>«los Dos Tipos de Andrómeda»</strong>.',
       'El primero salió en <strong>octubre de 1986</strong> y vendió más de <strong>100.000 copias</strong>.',
       'Querían que morir fuera <strong>divertido</strong>: había jugadores que buscaban muertes nuevas solo para ver el chiste.',
       'Llenos de juegos de palabras, absurdos y guiños a la cultura pop.'],
      'Un conserje que salva el universo y nadie le da las gracias. Yo me siento muy identificado.',
      [WP + '«Space Quest»'])

# ── LucasArts ──
ficha('maniac-mansion', 'Maniac Mansion', 'Nace el SCUMM', '1987', 'Commodore 64, Apple II, MS-DOS, Amiga, Atari ST, NES…', 'Lucasfilm Games · Ron Gilbert y Gary Winnick', '🏠',
      'Dave entra en la mansión del doctor Fred, un científico loco controlado por un meteorito, para rescatar a su novia Sandy. Eliges a dos de sus seis '
      'amigos para que le acompañen, y cada uno resuelve las cosas a su manera. Y lo más importante: aquí nació el motor que usaría LucasArts durante diez años.',
      ['<strong>SCUMM</strong> significa <em>Script Creation Utility for Maniac Mansion</em>. Lucasfilm lo reutilizó en <strong>once juegos más</strong>.',
       'Tiene <strong>cinco finales</strong> distintos.',
       'La versión de NES tuvo censura: Nintendo quitó un calendario de bañadores, una estatua y un póster. Lo del hámster en el microondas se les coló… hasta que lo vieron.',
       'Tuvo serie de televisión: <strong>tres temporadas y 66 episodios</strong> desde 1990.',
       'En Alemania Occidental fue el juego más vendido <strong>tres meses seguidos</strong>.'],
      'Lo del hámster no lo hagáis en casa. Ni en una mansión. Ni en ningún sitio.',
      [WP + '«Maniac Mansion»'])

ficha('monkey-island', 'The Secret of Monkey Island', 'Quiero ser pirata', '1990', 'MS-DOS, Amiga, Atari ST, Mac… (edición especial en 2009)', 'Lucasfilm Games · Ron Gilbert, Tim Schafer y Dave Grossman', '🏴‍☠️',
      'Guybrush Threepwood llega a la isla de Mêlée con un sueño: ser pirata. Para conseguirlo tendrá que superar tres pruebas, enamorarse de la gobernadora Elaine '
      'y enfrentarse al pirata fantasma LeChuck. Para muchos, la mejor aventura gráfica de la historia.',
      ['El ambiente sale de la atracción <strong>Piratas del Caribe</strong> de Disneylandia.',
       'Los <strong>duelos de insultos con espada</strong> nacieron cuando Ron Gilbert puso al equipo a ver películas de piratas de la época de Errol Flynn: se pasaban más tiempo insultándose que peleando.',
       'Gilbert no quería pruebas de reflejos: «no quería hacer un juego de reflejos, y ahí los insultos encajaban perfectamente».',
       'Tim Schafer al principio dudaba de que a la gente le fuera a gustar lo de los insultos.',
       'En <strong>2009</strong> salió la <strong>edición especial</strong>, con gráficos redibujados y voces, y la crítica la volvió a adorar.'],
      'Tengo un récord de insultos que ni Guybrush. El problema es que en la vida real no te dan puntos.',
      [WP + '«The Secret of Monkey Island»', 'GamesRadar+ (reportaje sobre el origen de los duelos de insultos)'])

ficha('monkey-island-2', 'Monkey Island 2: LeChuck\'s Revenge', 'La venganza (y el final más raro)', '1991', 'MS-DOS, Amiga, Mac, FM Towns… (edición especial en 2010)', 'LucasArts · Ron Gilbert, Tim Schafer y Dave Grossman', '💀',
      'Guybrush busca el legendario tesoro de Big Whoop, pero LeChuck ha vuelto, ahora convertido en zombi. Más grande, más loco y con un final que dejó '
      'a toda una generación con la boca abierta durante años.',
      ['Fue el <strong>primer juego de LucasArts con iMUSE</strong>, el sistema que hacía que la música cambiara sin cortes según dónde estuvieras.',
       'Salió en <strong>diciembre de 1991</strong>. La crítica lo adoró, pero en ventas fue una <strong>decepción</strong>.',
       'Su final era tan ambiguo que la tercera parte, seis años después, tuvo que explicarlo como pudo.',
       'Fue el último Monkey Island de Ron Gilbert… hasta 2022.'],
      'No os voy a destripar el final. Básicamente porque después de treinta años sigo sin entenderlo.',
      [WP + '«Monkey Island 2: LeChuck\'s Revenge»'])

ficha('indiana-jones-atlantis', 'Indiana Jones and the Fate of Atlantis', 'La película que nunca se rodó', '1992', 'MS-DOS, Amiga, Mac, FM Towns… (y Wii en 2009)', 'LucasArts · Hal Barwood y Noah Falstein', '🗿',
      'Año 1939: Indy busca la Atlántida antes que los nazis, que quieren usar su poder para la guerra. Le acompaña Sophia Hapgood, una antigua compañera con poderes '
      'psíquicos. Para muchos, la mejor película de Indiana Jones… que no es una película.',
      ['Superó el <strong>millón de copias</strong>: la aventura más vendida de LucasArts, según Falstein.',
       'Tenía <strong>tres caminos</strong>: en equipo con Sophia, de ingenio (más puzles) o de puños (más peleas).',
       'Harrison Ford <strong>no</strong> puso la voz en la versión en CD: lo hizo el actor Doug Lee.',
       'La idea original salía de un guion rechazado para la tercera película. Al final escribieron una historia nueva.',
       'Según Falstein, un <strong>30 % de quienes lo jugaban eran mujeres</strong>, mucho más de lo normal en LucasArts entonces.'],
      'Mejor guion que la de la calavera de cristal. Y lo digo con todo el respeto a las calaveras.',
      [WP + '«Indiana Jones and the Fate of Atlantis»'])

ficha('day-of-the-tentacle', 'Day of the Tentacle', 'Un váter que viaja en el tiempo', '1993', 'MS-DOS, Mac (remasterizado en 2016)', 'LucasArts · Dave Grossman y Tim Schafer', '🐙',
      'El Tentáculo Púrpura bebe un líquido tóxico y decide conquistar el mundo. Bernard, Hoagie y Laverne viajan en el tiempo para impedirlo… pero la máquina falla '
      'y cada uno acaba en una época: el pasado, el presente y el futuro. La secuela de Maniac Mansion y una de las comedias más redondas del género.',
      ['Dentro del juego hay un ordenador en el que puedes jugar a <strong>Maniac Mansion entero</strong>.',
       'Las máquinas del tiempo son <strong>retretes portátiles</strong> llamados Chron-O-John. Así, tal cual.',
       'Fue de los primeros juegos en salir en disquetes <strong>y en CD-ROM</strong>, y la primera aventura de LucasArts con voces desde el primer día.',
       'En <strong>2016</strong>, Double Fine (el estudio de Tim Schafer) lo remasterizó con dibujos en alta resolución y comentarios de los creadores.'],
      'Mandar cosas al futuro tirando de la cadena. Y luego dicen que los videojuegos no son educativos.',
      [WP + '«Day of the Tentacle»'])

ficha('sam-and-max', 'Sam & Max Hit the Road', 'Policías freelance', '1993', 'MS-DOS, Mac, Windows', 'LucasArts · Sean Clark, Michael Stemmle, Steve Purcell y Collette Michaud', '🐶',
      'Un perro con traje y un conejo hiperactivo (o «cosa parecida a un conejo»), la Policía Freelance, recorren Estados Unidos en busca de Bruno, un pie grande '
      'que se ha escapado de una feria. Por el camino visitan las atracciones de carretera más absurdas del país.',
      ['Está basado en los cómics de <strong>Steve Purcell</strong>, sobre todo en <em>On the Road</em> (1989).',
       'Muchas atracciones las sacaron de sitios reales que visitó el equipo, como <strong>la bola de cuerda más grande del mundo</strong>.',
       'La cadena «Snuckey\'s» es un homenaje a las tiendas de carretera Stuckey\'s en las que paraba la familia de Purcell de pequeño.',
       'LucasArts canceló dos secuelas; años después, la saga volvió con <strong>Telltale Games</strong>.'],
      'Max es lo que pasaría si me dejaran conducir un coche de policía. Por eso no me dejan.',
      [WP + '«Sam & Max Hit the Road»'])

ficha('full-throttle', 'Full Throttle', 'Moteros, gasolina y rock', '1995', 'MS-DOS, Mac (remasterizado en 2017)', 'LucasArts · Tim Schafer', '🏍️',
      'Ben, el líder de la banda de moteros Polecats, es acusado de un asesinato que no ha cometido: el del dueño de la última gran fábrica de motos. '
      'Una aventura corta, dura y con mucho estilo, que suena a rock y huele a gasolina.',
      ['Fue la <strong>primera aventura de LucasArts que salió solo en CD-ROM</strong>.',
       'Al malo, Adrian Ripburger, le pone la voz <strong>Mark Hamill</strong>, el Luke Skywalker de toda la vida.',
       'La música la ponía <strong>The Gone Jackals</strong>, una banda de rock de San Francisco.',
       'En <strong>2017</strong> salió la versión remasterizada para PC, PS4 y PS Vita.'],
      'Lo resolvía casi todo a patadas. Mi tipo de aventura gráfica.',
      [WP + '«Full Throttle (1995 video game)»'])

ficha('the-dig', 'The Dig', 'La idea de Spielberg', '1995', 'MS-DOS, Mac', 'LucasArts · Sean Clark y Brian Moriarty, con idea de Steven Spielberg', '☄️',
      'Un equipo de astronautas pone explosivos en un asteroide para desviarlo de la Tierra… y tres de ellos acaban en un planeta alienígena abandonado. '
      'Ciencia ficción seria, melancólica y muy distinta a las comedias de LucasArts.',
      ['La idea era de <strong>Steven Spielberg</strong>: primero quiso hacer un episodio de <em>Cuentos asombrosos</em> y luego una película, pero salía carísima.',
       'Es la aventura de LucasArts con el <strong>desarrollo más largo</strong>: anunciada para 1992, salió a finales de 1995 y pasó por <strong>cuatro jefes de proyecto</strong>.',
       'Al comandante Boston Low le pone voz <strong>Robert Patrick</strong>, el T-1000 de <em>Terminator 2</em>.',
       'Vendió <strong>300.000 copias</strong> hasta 1998, lo mejor de LucasArts en aventuras en su lanzamiento… pero había costado tanto que no recuperó la inversión.'],
      'Spielberg tuvo una idea demasiado cara para Hollywood. Para eso estaban los videojuegos, para hacer posible lo imposible (y arruinar a alguien).',
      [WP + '«The Dig (video game)»'])

ficha('curse-of-monkey-island', 'The Curse of Monkey Island', 'Guybrush, en dibujos animados', '1997', 'Windows (y macOS en 2018)', 'LucasArts · Larry Ahern y Jonathan Ackley', '🦜',
      'Guybrush le pide matrimonio a Elaine con un anillo maldito… y la convierte en una estatua de oro. Tocará deshacer la maldición mientras LeChuck vuelve a dar guerra. '
      'Fue la primera parte sin Ron Gilbert y llegó con un aspecto de película de dibujos animados.',
      ['Fue el <strong>último juego de LucasArts con el motor SCUMM</strong>, el número doce.',
       'Desde aquí, la voz de Guybrush es <strong>Dominic Armato</strong>.',
       'Según el artista Bill Tiller, vendió <strong>más de medio millón de copias</strong> en todo el mundo.',
       'En Alemania, Austria y Suiza ganó un premio de <strong>Oro</strong> por superar las 100.000 copias.'],
      'Pedirle matrimonio a alguien y convertirla en oro. Hay propuestas peores, pero no muchas.',
      [WP + '«The Curse of Monkey Island»'])

ficha('grim-fandango', 'Grim Fandango', 'La obra maestra que nadie compró', '1998', 'Windows (remasterizado en 2015)', 'LucasArts · Tim Schafer', '💀',
      'Manny Calavera es agente de viajes en la Tierra de los Muertos: vende a las almas el billete para su último viaje. Cuando intenta ayudar a Meche a llegar al Noveno '
      'Inframundo, destapa una trama criminal. Cine negro, Día de Muertos y cuatro años de historia en un solo juego.',
      ['Mezcla las <strong>calacas del Día de Muertos</strong> y la mitología azteca con el art déco y el cine negro de <em>Casablanca</em> y <em>El halcón maltés</em>.',
       'Fue la primera aventura de LucasArts <strong>sin el motor SCUMM</strong>: usaba el nuevo GrimE, en 3D.',
       'En Estados Unidos vendió unas <strong>58.600 copias</strong> en 1998. Se considera un <strong>fracaso comercial</strong> y se cita como una de las causas de que LucasArts abandonara el género.',
       'En <strong>2015</strong>, Double Fine lo remasterizó, con la banda sonora grabada por la <strong>Orquesta Sinfónica de Melbourne</strong>.'],
      'Un esqueleto vendiendo viajes al más allá. Ni siquiera muerto te libras de las agencias de viajes.',
      [WP + '«Grim Fandango»'])

# ── Sierra y Europa ──
ficha('gabriel-knight', 'Gabriel Knight: Sins of the Fathers', 'Vudú en Nueva Orleans', '1993', 'MS-DOS (remake en 2014)', 'Sierra On-Line · Jane Jensen', '🔮',
      'Gabriel es un escritor de terror sin éxito que tiene una librería en Nueva Orleans. Investigando los «asesinatos vudú» para su próxima novela, descubre que lo '
      'sobrenatural es real… y que su familia tiene mucho que ver. La aventura más adulta y oscura de Sierra.',
      ['En la versión en CD, a Gabriel le pone voz <strong>Tim Curry</strong>.',
       'Gabriel descubre que es un <strong>Schattenjäger</strong>, un «cazador de sombras».',
       'La saga tuvo tres juegos muy distintos: dibujos (1993), <strong>vídeo real con actores</strong> (1995) y 3D (1999).',
       'En <strong>2014</strong> salió una edición del 20.º aniversario con gráficos y sonido nuevos.'],
      'Un escritor que no vende y se mete en líos para tener algo que contar. Esto me suena de algo.',
      [WP + '«Gabriel Knight»'])

ficha('simon-the-sorcerer', 'Simon the Sorcerer', 'El mago más chulo de los 90', '1993', 'Amiga, MS-DOS, Windows… (y móviles)', 'Adventure Soft', '🧙',
      'Simon es un chaval que acaba en un mundo mágico por culpa de un libro de hechizos que le trae su perro. Allí le toca hacerse mago para rescatar al hechicero Calypso '
      'y derrotar al malvado Sordid. Parodia de <em>El señor de los anillos</em> y de los cuentos de toda la vida.',
      ['En la versión en CD, la voz de Simon es de <strong>Chris Barrie</strong>.',
       'Su aspecto está inspirado en <strong>la serie <em>La víbora negra</em></strong> (<em>Blackadder</em>).',
       'El estudio quería hacer un juego de Mundodisco, pero no consiguió la licencia.',
       'Superó las <strong>600.000 copias</strong> en 1999. Y el estudio antes se llamaba HorrorSoft: lo cambió al pasarse a la comedia.'],
      'Un adolescente chulo con capa y sombrero que va de listo. O sea, yo a los catorce.',
      [WP + '«Simon the Sorcerer»'])

ficha('myst', 'Myst', 'La isla que vendió CD-ROM', '1993', 'Mac, Windows', 'Cyan · Rand y Robyn Miller', '📖',
      'Tocas un libro y apareces en una isla desierta. Sin instrucciones, sin enemigos, sin nadie: solo mecanismos, libros y mundos por descubrir. '
      'Myst no se parecía a nada, y fue un fenómeno mundial.',
      ['Vendió más de <strong>6,3 millones</strong> de copias hasta el año 2000.',
       'Fue el <strong>juego de PC más vendido de los 90</strong>, hasta que lo superó <em>Los Sims</em> en 2002.',
       'Ayudó a que medio mundo se comprara un <strong>lector de CD-ROM</strong>.',
       'Se hizo con <strong>HyperCard</strong>, un programa de Apple: cada mundo era un archivo distinto.'],
      'Estuve tres horas en Myst sin saber qué hacer. Luego me dijeron que esa era la gracia.',
      ['Wikiwand/Wikipedia (en inglés), «Myst»'])

ficha('broken-sword', 'Broken Sword: la saga de los templarios', 'Cinco juegos (y contando)', '1996–2024', 'PC, PlayStation, PS2, Xbox, GBA, DS, Wii, móviles, PS4, Switch…', 'Revolution Software · Charles Cecil', '⚔️',
      'George Stobbart, un turista estadounidense, está tomando algo en una terraza de París cuando un payaso hace estallar el café. Investigando la explosión, '
      'y con la periodista francesa <strong>Nico Collard</strong>, acaba metido en una conspiración templaria que le lleva por media Europa y Oriente Medio. '
      'Fue el principio de una de las sagas más queridas del género, con <strong>cinco juegos</strong>:'
      '<ul class="saga">'
      '<li><b>1996 · La leyenda de los templarios</b> (<em>The Shadow of the Templars</em>): el original, dibujado a mano. Vendió alrededor de <strong>un millón de copias</strong> hasta 2001.</li>'
      '<li><b>1997 · Las fuerzas del mal</b> (<em>The Smoking Mirror</em>): segunda parte, también en 2D, con una piedra maya de por medio.</li>'
      '<li><b>2003 · El sueño del dragón</b> (<em>The Sleeping Dragon</em>): salto al <strong>3D</strong> y a más acción. Dividió a los fans.</li>'
      '<li><b>2006 · El ángel de la muerte</b> (<em>The Angel of Death</em>): sigue en 3D; fue la entrega menos querida.</li>'
      '<li><b>2013 · La maldición de la serpiente</b> (<em>The Serpent\'s Curse</em>): <strong>vuelta al 2D</strong>, pagada por los fans en Kickstarter.</li>'
      '</ul>',
      ['Entre las cinco, la saga ha pasado por <strong>más de quince sistemas</strong>: de la primera PlayStation a la Game Boy Advance, la Nintendo DS, la Wii, los móviles y la Switch.',
       'En el <strong>Director\'s Cut</strong> de 2009 (un remake del primero) por fin se podía <strong>jugar con Nico</strong>. En la versión original de 1996, no.',
       'La quinta parte se financió en Kickstarter en 2012: pedían unos 400.000 dólares y acabaron con <strong>más de 800.000</strong>, el doble.',
       'El <strong>19 de septiembre de 2024</strong> salió <em>Shadow of the Templars – Reforged</em>, el primero remasterizado en alta definición para PC y consolas.',
       'En Estados Unidos el primero se llamó <em>Circle of Blood</em>, y la música es de <strong>Barrington Pheloung</strong>, el de la serie <em>Inspector Morse</em>.'],
      'Todo empieza con un payaso que revienta una cafetería. Y luego dicen que yo exagero.',
      [WP + '«Broken Sword» y «Broken Sword: The Shadow of the Templars»', 'PCGamesN y VideoGamer (Kickstarter de Broken Sword 5, septiembre de 2012)', 'GamingOnLinux y Game Developer (lanzamiento de Reforged, 2024)'])

ficha('the-longest-journey', 'The Longest Journey', 'Entre dos mundos', '1999', 'Windows', 'Funcom · Ragnar Tørnquist', '🌗',
      'April Ryan, una estudiante de arte de 18 años, descubre que puede saltar entre dos mundos: Stark, una Tierra futurista e industrial, y Arcadia, '
      'un mundo de fantasía. El equilibrio entre los dos se está rompiendo y le toca arreglarlo. Una de las grandes historias del género.',
      ['Fue el <strong>primer proyecto original</strong> del estudio noruego Funcom.',
       'Superó las <strong>500.000 copias</strong> en 2004.',
       'Tuvo continuación con <em>Dreamfall</em> (2006) y <em>Dreamfall Chapters</em> (2014–2016), este último por episodios y financiado por los fans.'],
      'Saltar entre dos mundos. Yo lo hago a diario entre el sofá y la nevera.',
      [WP + '«The Longest Journey»'])

# ── Hecho en España ──
ficha('abadia-del-crimen', 'La abadía del crimen', 'El nombre de la rosa, a la española', '1987', 'Amstrad CPC, ZX Spectrum, MSX, MS-DOS', 'Opera Soft · Paco Menéndez y Juan Delcán', '⛪',
      'Un fraile franciscano, Guillermo de Occam, y su novicio Adso investigan una serie de asesinatos en una abadía medieval. Más videoaventura que aventura gráfica '
      'pura, pero con una ambición y una atmósfera que la convirtieron en uno de los grandes clásicos del software español.',
      ['Está inspirada en <em>El nombre de la rosa</em> de Umberto Eco. Como <strong>no consiguieron los derechos</strong>, le pusieron otro título.',
       'Y el título no es casual: la novela de Eco se llamó en sus inicios <strong>«La abadía del crimen»</strong>.',
       'Lo programó <strong>Paco Menéndez</strong> y los gráficos son de <strong>Juan Delcán</strong>, en perspectiva isométrica.',
       'En el libro el fraile se llama Guillermo de Baskerville; en el juego, <strong>Guillermo de Occam</strong>.'],
      'Lo de que el protagonista se llame Guillermo es pura casualidad. No se lo digáis al jefe, que se viene arriba.',
      [WP + '«La Abadía del Crimen»'])

ficha('igor', 'Igor: Objetivo Uikokahonia', 'La primera aventura gráfica española', '1994', 'MS-DOS', 'Pendulo Studios', '🪃',
      'Igor Parker, un universitario, quiere apuntarse al viaje de Biología a la isla de Uikokahonia… porque va Laura, la chica que le gusta. Y también va su rival, Philip. '
      'Con este juego empezó Pendulo Studios, el estudio madrileño que se convertiría en el rey de la aventura gráfica española.',
      ['Se considera <strong>la primera aventura gráfica desarrollada en España</strong>.',
       'Costó <strong>menos de 400.000 pesetas</strong>, y el equipo había aprendido por su cuenta.',
       'Pendulo se fundó en <strong>septiembre de 1993</strong>: Rafael Latiegui, Ramón Hernáez, Felipe Gómez Pinilla y Miguel Ángel Ramos.',
       'Como en LucasArts, <strong>no te podías morir</strong>. Y se inspiraba en <em>Indiana Jones and the Fate of Atlantis</em>.',
       'Lo publicó DROsoft en 1994; en <strong>1998</strong> volvió en CD-ROM con <em>El Mundo</em> y <strong>Dinamic Multimedia</strong>, y en 2007 se hizo gratuito.'],
      'Todo un juego para ir de excursión con la chica que te gusta. Lo más realista que se ha hecho nunca.',
      [WP + '«Igor: Objective Uikokahonia»', 'Wikipedia (en español), «Pendulo Studios»'])

ficha('hollywood-monsters', 'Hollywood Monsters', 'Los monstruos también tienen agente', '1997', 'Windows', 'Pendulo Studios · edita Dinamic Multimedia', '🧟',
      'En unos años 50 alternativos, los monstruos del cine clásico son estrellas de Hollywood. En una gala de premios, alguien descuartiza al monstruo de Frankenstein '
      'y secuestra a la periodista Sue Bergman. Su compañero Ron Ashman recorre el mundo recuperando los trozos de Frankie: se los han quedado la Momia, el Hombre Lobo y Drácula.',
      ['Lo editó <strong>Dinamic Multimedia</strong> en <strong>diciembre de 1997</strong>, y después FX Interactive lo reeditó varias veces.',
       'Vendió unas <strong>250.000 copias en España</strong>, según HobbyConsolas: un éxito enorme para la época. También triunfó en Italia.',
       'El tema principal de la banda sonora es del grupo <strong>La Unión</strong>.',
       'Micromanía le puso un <strong>88</strong> y MeriStation un <strong>8</strong>.',
       'En 2011 tuvo un sucesor espiritual, <em>Hollywood Monsters 2</em> (<em>The Next Big Thing</em> fuera de España), con otros protagonistas.'],
      'Monstruos famosos, premios y un escándalo en la gala. Esto es básicamente una noche de los Goya.',
      [WP + '«Hollywood Monsters (video game)»', 'Computer Emuzone (ficha de Hollywood Monsters)'])

ficha('drascula', 'Dráscula: The Vampire Strikes Back', 'El vampiro más gamberro', '1996', 'MS-DOS (gratis desde 2008)', 'Alcachofa Soft', '🧛',
      'John Hacker, un agente inmobiliario, viaja a Transilvania para venderle una propiedad al conde Dráscula. Lo que podía salir mal, sale peor. '
      'Humor gamberro y políticamente incorrecto del de los 90, primer juego de Alcachofa Soft, que después haría varias aventuras de <strong>Mortadelo y Filemón</strong>.',
      ['Fue un <strong>fracaso comercial</strong>, en parte por una mala distribución.',
       'En <strong>2008</strong> Alcachofa regaló el código al equipo de ScummVM y lo liberó como <strong>juego gratuito</strong>.',
       'HobbyConsolas lo eligió en 2017 entre las <strong>nueve mejores aventuras gráficas españolas</strong> y lo llamó pionero.',
       'Alcachofa Soft también hizo <em>Mortadelo y Filemón: El sulfato atómico</em> (1998) y <em>Una aventura de cine</em> (2000), que en 2019 volvió en edición especial.'],
      'Un agente inmobiliario intentando venderle algo a un vampiro. Lo de chupar la sangre lo hacen los dos.',
      [WP + '«Dráscula: The Vampire Strikes Back»', WP + '«Mortadelo y Filemón: Una Aventura de Cine»'])

ficha('runaway', 'Runaway: A Road Adventure', 'El último de Dinamic Multimedia', '2001', 'Windows (y más tarde iOS)', 'Pendulo Studios · edita Dinamic Multimedia', '🛣️',
      'Brian Basco, un estudiante de Nueva York, atropella sin querer a Gina, que huye de unos mafiosos. Juntos acaban metidos en una persecución por todo Estados Unidos '
      'detrás de un crucifijo misterioso y 20 millones de dólares. El juego que hizo famoso a Pendulo en todo el mundo.',
      ['Salió en España el <strong>6 de julio de 2001</strong>, editado por <strong>Dinamic Multimedia</strong>.',
       'El <strong>24 de septiembre de 2001</strong>, Dinamic anunció su liquidación. Pendulo pasó <strong>un año peleando por los derechos</strong> y los recuperó en julio de 2002.',
       'FX Interactive lo reeditó en 2003 y, con <em>El Mundo</em>, se vendieron unas <strong>100.000 copias en un solo fin de semana</strong>.',
       'Empezó a dibujarse a mano, pero animar así salía carísimo: acabaron usando personajes en 3D con aspecto de cómic.',
       'Llegó a unas <strong>600.000 copias en Europa</strong> en 2006, y la trilogía sumaba <strong>1,5 millones</strong> en 2010.'],
      'Un juego sobrevive a que quiebre su editora y encima vende más. Eso es tener más vidas que yo en Trollaco Run.',
      [WP + '«Runaway: A Road Adventure»'])

# ── Muerte y resurrección ──
ficha('machinarium', 'Machinarium', 'Un robot sin palabras', '2009', 'Windows, Mac, Linux (y consolas y móviles después)', 'Amanita Design · Jakub Dvorský', '🤖',
      'Josef es un robot al que han tirado a un vertedero. Vuelve a su ciudad para frustrar los planes de una banda de matones y rescatar a su novia, Berta. '
      'Todo dibujado a mano por un pequeño estudio checo, y sin una sola línea de diálogo: los personajes se comunican con bocadillos animados.',
      ['Vendió más de <strong>4 millones de copias</strong> hasta 2016.',
       'Ganó el premio a la excelencia en arte visual del <strong>Independent Games Festival</strong>.',
       'La música es de <strong>Tomáš Dvořák</strong> (Floex) y es una maravilla.'],
      'Un juego sin palabras que se entiende mejor que las instrucciones de un mueble sueco.',
      [WP + '«Machinarium»'])

ficha('walking-dead', 'The Walking Dead', 'La aventura que te rompe el corazón', '2012', 'PC, Mac, PlayStation, Xbox, Switch, móviles…', 'Telltale Games', '🧟‍♂️',
      'Lee Everett, un hombre con un pasado complicado, se encuentra con Clementine, una niña sola en pleno apocalipsis zombi, y decide protegerla. Pocos puzles y muchas decisiones '
      'difíciles que cambian la historia. Telltale reinventó la aventura gráfica para una generación nueva.',
      ['Salió en <strong>cinco episodios</strong> entre abril y noviembre de 2012.',
       'Vendió <strong>8,5 millones de episodios</strong> a finales de 2012, y más de <strong>28 millones de copias</strong> en 2024.',
       'Se llevó <strong>varios premios al mejor juego del año</strong>.',
       'Está basado en el cómic de <strong>Robert Kirkman</strong>, no en la serie de televisión.'],
      'Juego de zombis en el que lo más duro no son los zombis. Llevad pañuelos.',
      [WP + '«The Walking Dead (video game)»'])

ficha('broken-age', 'Broken Age', 'El Kickstarter que lo cambió todo', '2014–2015', 'Windows, Mac, Linux, PS4, Switch…', 'Double Fine · Tim Schafer', '🚀',
      'En 2012, Tim Schafer pidió a los fans dinero para hacer una aventura gráfica clásica, de las que ya ninguna editora quería pagar. Pidió 400.000 dólares. '
      'Lo que pasó después fue historia de la financiación de los videojuegos.',
      ['La campaña («Double Fine Adventure») arrancó en <strong>febrero de 2012</strong> y recaudó más de <strong>3,45 millones de dólares</strong> de más de <strong>87.000 personas</strong> en un mes.',
       'Demostró que el <strong>micromecenazgo</strong> podía sustituir a las editoras para juegos de nicho, y detrás llegaron muchos más.',
       'El primer acto salió el <strong>28 de enero de 2014</strong>; el juego completo, el <strong>28 de abril de 2015</strong>.'],
      'Pidió 400.000 y le dieron 3,45 millones. Yo pido 20 euros a mis colegas y me ignoran en el grupo.',
      [WP + '«Broken Age»'])

ficha('thimbleweed-park', 'Thimbleweed Park', 'Volver a 1987', '2017', 'PC, Mac, Linux, Xbox One, PS4, Switch, móviles', 'Terrible Toybox · Ron Gilbert y Gary Winnick', '🔎',
      'Año 1987: dos agentes del FBI llegan al pueblo de Thimbleweed Park para investigar un asesinato. Cinco personajes jugables, pixel art y verbos en pantalla, '
      'como en los tiempos de Maniac Mansion. Lo hicieron, de hecho, los mismos que hicieron Maniac Mansion.',
      ['Pidieron <strong>375.000 dólares</strong> en Kickstarter y consiguieron <strong>626.250</strong> de <strong>15.623 personas</strong>.',
       'Salió el <strong>30 de marzo de 2017</strong>.',
       'Ron Gilbert y Gary Winnick, los creadores de <strong>Maniac Mansion</strong>, volvieron a firmar juntos una aventura treinta años después.'],
      'Un juego nuevo que parece de 1987 a propósito. Como mi forma de vestir.',
      [WP + '«Thimbleweed Park»'])

ficha('return-to-monkey-island', 'Return to Monkey Island', 'La vuelta de Gilbert', '2022', 'PC, Mac, Switch, PS5, Xbox Series, móviles', 'Terrible Toybox · edita Devolver Digital', '🏝️',
      'Treinta y un años después de <em>LeChuck\'s Revenge</em>, Ron Gilbert vuelve a la saga que creó y continúa la historia justo donde la dejó aquel final tan raro. '
      'Con Dave Grossman de guionista y Dominic Armato otra vez como Guybrush.',
      ['Gilbert lo anunció en su blog el <strong>1 de abril de 2022</strong>. Y no, no era una broma.',
       'Salió el <strong>19 de septiembre de 2022</strong>, el Día Internacional de Hablar como un Pirata.',
       'Su estilo de libro ilustrado causó polémica antes de salir… y la crítica lo alabó cuando por fin se jugó.',
       'En su primer mes en Steam vendió unas <strong>100.000 copias</strong>: el lanzamiento más rápido de la saga.'],
      'Treinta años esperando para saber qué pasaba. Ni la cola del médico de cabecera.',
      [WP + '«Return to Monkey Island»'])

# ───────────────────────── bloques especiales ─────────────────────────
DINAMIC = '''
<p>Si te suena <strong>Dinamic</strong> es por <a href="/especiales/juegos-de-futbol/#pc-futbol">PC Fútbol</a>, pero los hermanos Ruiz también tuvieron mucho que ver con las
aventuras en España. Lo explicamos en tres actos:</p>
<h3>1. Las aventuras de texto: Aventuras AD</h3>
<p>En el verano de <strong>1988</strong>, el médico y aventurero <strong>Andrés Samudio</strong> se presentó en la sede de Dinamic con su juego y nació
<strong>Aventuras AD</strong>, en Valencia: un sello filial de Dinamic dedicado solo a aventuras conversacionales, las de escribir órdenes con el teclado.
De ahí salieron <em>La aventura original</em>, <em>Jabato</em>, <em>La aventura espacial</em>, <em>La diosa de Cozumel</em> y <em>Chichén Itzá</em>, su último juego, en 1992.</p>
<h3>2. Dinamic Multimedia y Pendulo</h3>
<p>Ya en los 90, <strong>Dinamic Multimedia</strong> fue la casa de las aventuras de Pendulo Studios: reeditó <em>Igor: Objetivo Uikokahonia</em> en CD-ROM en 1998,
lanzó <strong>Hollywood Monsters</strong> en diciembre de 1997 (unas 250.000 copias en España) y estrenó <strong>Runaway</strong> el 6 de julio de 2001.</p>
<h3>3. La caída y FX Interactive</h3>
<p>El <strong>24 de septiembre de 2001</strong>, Dinamic Multimedia anunció su liquidación, con Runaway recién salido. Pendulo pasó un año peleando por los derechos del juego.
Mientras tanto, parte del equipo original de Dinamic ya había fundado <strong>FX Interactive</strong> en 1999, y fue FX quien reeditó Runaway en 2003, editó <em>Runaway 2</em> y <em>Hollywood Monsters 2</em>
y reeditó el Hollywood Monsters original. Una historia muy de aquí: el juego sobrevivió a su editora y acabó vendiendo más que nunca.</p>
'''

MUERTES = '''
<p>En los 80 y principios de los 90 había dos formas de entender una aventura gráfica, y se notaba en cuanto la pifiabas:</p>
<div class="cifras dos">
  <div><b>Sierra: aquí se muere</b><span>En King's Quest o Space Quest podías morir de mil maneras, a veces por dar un paso en falso. En Space Quest lo hicieron a propósito: querían que cada muerte fuera tan graciosa que la gente buscara más.</span></div>
  <div><b>LucasArts: aquí no</b><span>Desde Monkey Island, en los juegos de Ron Gilbert y compañía casi nunca podías morir ni quedarte atascado para siempre. Igor, la primera aventura española, siguió la misma filosofía.</span></div>
</div>
<p>¿Y los duelos de insultos? Gilbert no quería meter peleas de reflejos en Monkey Island, así que convirtió los duelos de espada en un concurso de ingenio:
cada insulto tiene su respuesta, y las vas aprendiendo a base de perder. Más de treinta y cinco años después, sigue siendo uno de los momentos más recordados de la historia del videojuego.</p>
'''

VOCES = '''<h2 id="voces">🎬 Voces de Hollywood</h2>
<p>Cuando llegó el CD-ROM, las aventuras empezaron a hablar. Y algunas fueron a buscar voces muy conocidas (en la versión original en inglés):</p>
<ul class="lista-nombres">
  <li><strong>Mark Hamill</strong>, Luke Skywalker, hace de malo en <em>Full Throttle</em>.</li>
  <li><strong>Robert Patrick</strong>, el T-1000 de <em>Terminator 2</em>, es el comandante de <em>The Dig</em>.</li>
  <li><strong>Tim Curry</strong> es Gabriel Knight en la versión en CD de <em>Sins of the Fathers</em>.</li>
  <li><strong>Chris Barrie</strong> pone voz a Simon en <em>Simon the Sorcerer</em>.</li>
  <li><strong>Dominic Armato</strong> es Guybrush Threepwood desde <em>The Curse of Monkey Island</em> (1997) hasta <em>Return to Monkey Island</em> (2022).</li>
</ul>
<p class="fu">Fuentes: Wikipedia (en inglés), fichas de cada juego.</p>'''

ORIGENES = '''
<p>Antes de los dibujos, las aventuras eran texto. En <strong>1976</strong>, Will Crowther, aficionado a la espeleología, escribió en un ordenador central
un juego basado en las cuevas de Mammoth Cave (Kentucky) y en sus partidas de rol. Empezaba con un «WELCOME TO ADVENTURE!!» y el archivo se llamaba ADVENT:
de ahí viene el nombre del género. En 1977 Don Woods lo amplió, y ese mismo año unos estudiantes del MIT empezaron <strong>Zork</strong>.</p>
<p>Tenía hasta una palabra mágica, <strong>«xyzzy»</strong>, que te teletransportaba. Crowther la metió a petición de su hermana para saltarse el principio.
Muchos programas todavía la esconden como homenaje.</p>
<p class="fu">Fuente: Wikipedia (en inglés), «Colossal Cave Adventure».</p>
'''

FUENTES = sorted({f for x in F for f in x['fuentes']} | {WP + '«Colossal Cave Adventure»', 'Valencia Plaza, «Aventuras AD: videojuegos conversacionales en la edad dorada del software español»'})

# ───────────────────────── página ─────────────────────────
g = open('gta-6/index.html', encoding='utf-8').read()
style = g[g.find('<style>'):g.find('</style>') + 8]
foot = g[g.find('<footer>'):g.find('</footer>') + 9]
fut = open('_fuentes/generadores/especial_futbol.py', encoding='utf-8').read()
extra = fut[fut.find("extra = '''") + 11:fut.find("</style>'''", fut.find("extra = '''"))]
style2 = style.replace('</style>', extra + '.intro{font-size:19px;line-height:1.65;margin:1em 0}.saga{margin:10px 0 0;padding-left:20px}.saga li{font-size:18px;margin-bottom:8px}.saga b{color:var(--yellow)}\n@media(max-width:700px){.intro{font-size:18px}.saga li{font-size:17px}}</style>')

def portada(x):
    p = f'{IMG}/{x["slug"]}.webp'
    if os.path.exists(p):
        return f'<div class="port"><img src="/{p}" alt="Portada de {esc(x["titulo"])}" width="220" height="293" loading="lazy"></div>'
    return f'<div class="port" aria-hidden="true">{x["icono"]}</div>'

def html_ficha(x):
    datos = ''.join(f'<li>{d}</li>' for d in x['datos'])
    fu = ' · '.join(esc(f) for f in x['fuentes'])
    pie = '<p class="fu">Portada © sus titulares.</p>' if os.path.exists(f'{IMG}/{x["slug"]}.webp') else ''
    return f'''<section class="ficha-j" id="{x['slug']}">
<div class="cab">{portada(x)}<div><span class="sub">&gt; {esc(x['sub'].upper())}_</span><h3>{esc(x['titulo'])}</h3>
<dl><dt>AÑO</dt><dd>{x['anio']}</dd><dt>DÓNDE</dt><dd>{esc(x['plataformas'])}</dd><dt>QUIÉN</dt><dd>{esc(x['estudio'])}</dd></dl></div></div>
{('<div class="intro">' + x['intro'] + '</div>') if '<ul' in x['intro'] else '<p>' + x['intro'] + '</p>'}
<div class="flipar"><b class="t">🤯 DATOS PARA FLIPAR</b><ul>{datos}</ul></div>
<div class="nota"><img src="/img/trollaco.png" alt=""><p><b>EL TROLLACO OPINA:</b> {esc(x['troll'])}</p></div>
{pie}<p class="fu">Fuentes: {fu}.</p>
</section>'''

def tl_item(a, t, d, ancla):
    return f'<li><a href="#{ancla}"><span class="a">{a}</span><b>{esc(t)}</b><span>{esc(d)}</span></a></li>'
tl = ''.join(tl_item(*t) for t in TIEMPO)
ERAS = [
    ('pioneras', '📜 Las pioneras: de escribir órdenes a ver dibujos', 'Teclado, mucha paciencia y un parser que no entendía nada. Aquí Sierra se inventó la aventura gráfica.',
     ['mystery-house', 'kings-quest', 'space-quest']),
    ('lucasarts', '🏴‍☠️ La edad de oro de LucasArts', 'Del SCUMM al GrimE: diez años en los que LucasArts hizo las aventuras más queridas de la historia.',
     ['maniac-mansion', 'monkey-island', 'monkey-island-2', 'indiana-jones-atlantis', 'day-of-the-tentacle', 'sam-and-max', 'full-throttle', 'the-dig', 'curse-of-monkey-island', 'grim-fandango']),
    ('rivales', '🗡️ Sierra, Europa y la isla misteriosa', 'LucasArts no estaba sola: Sierra se puso seria, los británicos sacaron su humor y una isla sin nadie vendió millones.',
     ['gabriel-knight', 'simon-the-sorcerer', 'myst', 'broken-sword', 'the-longest-journey']),
    ('espana', '🇪🇸 Hecho en España', 'Abadías, monstruos de Hollywood, vampiros gamberros y una carretera: la aventura gráfica española tuvo su propia edad de oro.',
     ['abadia-del-crimen', 'igor', 'hollywood-monsters', 'drascula', 'runaway']),
    ('renacer', '🌱 Muerte y resurrección', 'A finales de los 90 las editoras dieron el género por muerto. Luego llegaron los estudios independientes, Telltale y Kickstarter.',
     ['machinarium', 'walking-dead', 'broken-age', 'thimbleweed-park', 'return-to-monkey-island']),
]
usadas = [s for e in ERAS for s in e[3]]
assert sorted(usadas) == sorted(x['slug'] for x in F), set(x['slug'] for x in F) ^ set(usadas)
assert all(t[3] in usadas + ['origenes', 'espana'] for t in TIEMPO)
indice = ''.join(f'<a href="#{i}">{t}</a>' for i, t in [('linea', '🕰️ Línea del tiempo'), ('origenes', '⌨️ Antes de los dibujos')] + [(e[0], e[1].split(':')[0]) for e in ERAS] +
    [('dinamic', '💾 Dinamic'), ('morir', '💀 ¿Se puede morir?'), ('voces', '🎬 Voces'), ('numeros', '📊 Los números')])
FIRMA = ('<div class="firma"><img src="/img/danna.jpg?v=4" alt="Danna" width="56" height="56"><div><b>Por Danna</b>'
         f'<span>Tu reportera del otro lado de la pantalla · <a href="https://www.instagram.com/dannapixel/" target="_blank" rel="noopener">📸 @dannapixel</a> · <a href="/danna/">¿Quién es?</a> · {FECHA}</span></div></div>')
def html_era(e):
    fichas = ''.join(html_ficha(next(x for x in F if x['slug'] == sl)) for sl in e[3])
    extra_esp = ''
    if e[0] == 'espana':
        extra_esp = f'''<section class="bloque-pcf" id="dinamic"><p class="k">&gt; DE DINAMIC A FX_</p><h2 style="margin-top:4px">💾 Dinamic y las aventuras: la historia completa</h2>
{DINAMIC}
<div class="nota"><img src="/img/trollaco.png" alt=""><p><b>EL TROLLACO OPINA:</b> De Dinamic salieron PC Fútbol, Hollywood Monsters y Runaway. Media infancia de este país cabe en su logo.</p></div>
<p class="fu">Fuentes: Valencia Plaza, «Aventuras AD: videojuegos conversacionales en la edad dorada del software español»; Wikipedia (en inglés), «Runaway: A Road Adventure», «Hollywood Monsters (video game)» e «Igor: Objective Uikokahonia».</p></section>'''
    return f'<h2 id="{e[0]}">{e[1]}</h2><p class="era-intro">{e[2]}</p>{fichas}{extra_esp}'
eras_html = ''.join(html_era(e) for e in ERAS)
fuentes = ''.join(f'<li>{esc(f)}</li>' for f in FUENTES)

titulo = 'De Monkey Island a Runaway: la historia de las aventuras gráficas'
desc = 'El especial de aventuras gráficas de Trollacos: 28 juegos, de Mystery House y King\'s Quest a Monkey Island, Grim Fandango, Broken Sword, Hollywood Monsters, Runaway y Return to Monkey Island. Con Dinamic, Pendulo y la aventura española.'
cuerpo = f'''<p class="migas"><a href="/">Portada</a> › <a href="/especiales/">Especiales</a> › Aventuras gráficas</p>
<div class="hero-f"><p class="k">&gt; ESPECIAL TROLLACOS_</p><h1>De Monkey Island a Runaway: la historia de las aventuras gráficas</h1>
<p>Usar el pollo de goma con la polea, hablar con todo el mundo dos veces y frotar cada objeto del inventario con todo lo demás. Cuarenta y tantos años de puzles,
risas y algún que otro atasco de semanas, de Sierra y LucasArts a Pendulo, Dinamic y los Kickstarter.</p></div>
{FIRMA}
<p>Este especial va para quienes se pasaron una tarde entera atascados en una pantalla y no se rindieron. Y para quienes acabaron llamando a la línea de pistas de una revista.
Datos con su fuente, opinión nuestra y mucha nostalgia. Coge el ratón, que empezamos. 🖱️</p>
<nav class="indice" aria-label="Índice">{indice}</nav>
<h2 id="linea">🕰️ La línea del tiempo</h2>
<ul class="tl">{tl}</ul>
<h2 id="origenes">⌨️ Antes de los dibujos: las aventuras de texto</h2>
{ORIGENES}
<div class="nota pri"><img src="/img/princesa.png" alt=""><p><b>LA PRINCESA NEÓN OPINA:</b> A mí me secuestran cada dos por tres y nadie me deja un inventario. Si me dejaran un pollo de goma con polea, me rescataba yo sola.</p></div>
{eras_html}
<h2 id="morir">💀 ¿Se puede morir? Sierra contra LucasArts</h2>
{MUERTES}
<p class="fu">Fuentes: Wikipedia (en inglés), «Space Quest», «Igor: Objective Uikokahonia»; GamesRadar+ (reportaje sobre el origen de los duelos de insultos).</p>
{VOCES}
<h2 id="numeros">📊 Los números</h2>
<div class="cifras">
  <div><b>6,3 M</b><span>copias de Myst hasta el año 2000: el juego de PC más vendido de los 90</span></div>
  <div><b>+28 M</b><span>copias de The Walking Dead de Telltale en 2024</span></div>
  <div><b>+4 M</b><span>copias de Machinarium en 2016</span></div>
  <div><b>+1 M</b><span>copias de Indiana Jones and the Fate of Atlantis, récord de LucasArts</span></div>
  <div><b>1,5 M</b><span>copias de la trilogía Runaway en 2010</span></div>
  <div><b>250.000</b><span>copias de Hollywood Monsters en España (HobbyConsolas)</span></div>
  <div><b>3,45 M $</b><span>recaudados por Double Fine Adventure en Kickstarter, de 87.000 personas</span></div>
  <div><b>58.600</b><span>copias de Grim Fandango en EE. UU. en 1998: la obra maestra que no vendió</span></div>
  <div><b>&lt;400.000</b><span>pesetas costó hacer Igor, la primera aventura gráfica española</span></div>
</div>
<div class="reto-f"><p>¿Más de pulsar que de pensar? Pues ayuda al Trollaco a rescatar a la Princesa Neón 🕹️</p><a class="btn" href="/arcade/">JUEGA A TROLLACO RUN</a></div>
<h2>📚 Fuentes de los datos</h2>
<p style="font-size:16px">Los datos salen de estas fuentes, citadas por su nombre. La opinión, las bromas y la nostalgia son nuestras.</p>
<ul class="fuentes-l">{fuentes}</ul>
<p class="fu">Monkey Island, Grim Fandango, King's Quest, Broken Sword, Runaway, Hollywood Monsters y el resto de nombres y marcas citados son de sus respectivos dueños. Trollacos no tiene relación con ellos.</p>
<p class="aviso-c">🧯 Aquí no enlazamos descargas ni copias de juegos. Muchos de estos clásicos se venden hoy en tiendas digitales, y algunos (como Igor o Dráscula) los liberaron sus propios creadores.</p>'''

ld = {'@context': 'https://schema.org', '@type': 'Article', 'headline': titulo, 'datePublished': '2026-11-10',
      'author': {'@type': 'Person', 'name': 'Danna', 'url': 'https://trollacos.com/danna/'},
      'publisher': {'@type': 'Organization', 'name': 'Trollacos'}, 'description': desc}

def pagina(titulo, desc, u, cuerpo, ld=None, volver=('/', '‹ PORTADA')):
    j = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ''
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)} | Trollacos</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="https://trollacos.com{u}">
<meta property="og:title" content="{esc(titulo)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:image" content="https://trollacos.com/img/danna-setup.webp?v=4">
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

os.makedirs('especiales/aventuras-graficas', exist_ok=True)
open('especiales/aventuras-graficas/index.html', 'w', encoding='utf-8').write(pagina(titulo, desc, URL, cuerpo, ld, volver=('/especiales/', '‹ ESPECIALES')))

exec(open('_fuentes/generadores/especiales_hub.py', encoding='utf-8').read())
print(f'especial aventuras: {len(F)} fichas, {len(TIEMPO)} hitos, {len(FUENTES)} fuentes')
