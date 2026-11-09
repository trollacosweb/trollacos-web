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
    ('1988', 'Emilio Butragueño Fútbol', 'Topo Soft pone al Buitre en los ordenadores de 8 bits.', 'emilio-butragueno'),
    ('1988', 'Captain Tsubasa', 'Tecmo convierte a Oliver y Benji en juego de NES (en Europa, Tecmo Cup).', 'captain-tsubasa'),
    ('1989', 'Kick Off', 'Dino Dini despega el balón del pie. Amiga y Atari ST arden.', 'kick-off'),
    ('1992', 'Simulador Profesional de Fútbol', 'Dinamic lanza en PC el abuelo de PC Fútbol.', 'pcfutbol'),
    ('1992', 'Sensible Soccer y Championship Manager', 'Llegan Sensi y el primer mánager de los hermanos Collyer.', 'sensible-soccer'),
    ('1992', 'Super Sidekicks', 'SNK mete el fútbol en las recreativas Neo Geo.', 'super-sidekicks'),
    ('1993', 'FIFA International Soccer', 'EA estrena la saga en Mega Drive el 15 de diciembre, con la licencia de la FIFA.', 'fifa'),
    ('1994', 'International Superstar Soccer', 'Konami (estudio de Osaka) saca el primer ISS en Super Nintendo.', 'iss'),
    ('1994', 'Virtua Striker', 'Sega AM2 lleva el fútbol en 3D a los salones recreativos.', 'virtua-striker'),
    ('1995', 'J.League Jikkyou Winning Eleven', 'El estudio de Konami en Tokio lanza en Japón el primer Winning Eleven.', 'we'),
    ('1997', 'PC Fútbol 5.0', 'Temporada 96/97: 305.000 copias y el primero para Windows 95.', 'pcfutbol'),
    ('1997', 'ISS Pro, ISS 64 y FIFA 98', 'El año de la guerra total: Konami por partida doble y el FIFA de Raúl.', 'fifa-98'),
    ('1998', 'UEFA Champions League 98-99', 'Silicon Dreams y Eidos ponen el himno de la Champions en tu PlayStation.', 'champions'),
    ('1999', 'This Is Football e ISS Pro Evolution', 'Sony entra en la pelea y Konami prepara la revolución.', 'tif'),
    ('2000', 'Ronaldo V-Football', 'El Fenómeno pone cara y nombre a un juego de Infogrames.', 'ronaldo'),
    ('2001', 'Pro Evolution Soccer', 'Nace el PES (en Japón, Winning Eleven 5). Empieza la edad de oro.', 'pes'),
    ('2002', 'RedCard', 'Fútbol con entradas a lo bestia y jugadas especiales.', 'redcard'),
    ('2004', 'Football Kingdom y Football Manager', 'Namco prueba en Japón; Sports Interactive renace con Sega.', 'fk'),
    ('2005', 'FIFA Street, Mario Strikers y PES 5', 'Filigranas en la calle, caparazones y el PES más redondo.', 'fifa-street'),
    ('2006', 'PES 6', 'El PES que todavía se juega con parches veinte años después.', 'pes-5-y-6'),
    ('2007', 'PES 2008', 'Konami cambia el número por el año para no parecer más viejo que FIFA.', 'pes-2008'),
    ('2008', 'FIFA 09 y PES 2009', 'Nace Ultimate Team y PES consigue la Champions.', 'fifa-09'),
    ('2011', 'FIFA 12', 'Más de 3,2 millones de copias en su primera semana: récord de juego deportivo.', 'fifa'),
    ('2012', 'PES 2013', 'El último gran PES para muchos; sigue vivo gracias a los fans.', 'pes-2013'),
    ('2021', 'eFootball', 'Konami cambia PES por un free-to-play… y se estrella el día del estreno.', 'efootball'),
    ('2022', 'Adiós, FIFA', 'EA y la FIFA anuncian el 10 de mayo el fin de 30 años juntos.', 'ea-sports-fc'),
    ('2023', 'EA Sports FC 24', 'El 29 de septiembre llega el primer juego de fútbol de EA sin «FIFA» en la portada.', 'eafc'),
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
       '<em>ISS Deluxe</em> (1995) salió primero en Super Nintendo y luego en Mega Drive y PlayStation; en Japón se llamó <em>Jikkyou World Soccer 2: Fighting Eleven</em>.',
       'Al final ganó la línea de Tokio: de ella salieron ISS Pro y, después, el PES.'],
      'Yo aprendí a jugar con ISS 64. Bueno, aprendí a darle al botón de tiro muy fuerte y rezar.',
      ['Wikipedia (en inglés), «International Superstar Soccer», «International Superstar Soccer Deluxe» e «International Superstar Soccer 64»'])

ficha('winning-eleven', 'Winning Eleven e ISS Pro', 'El origen del PES', '1995–2001', 'PlayStation',
      'Konami (estudio de Tokio)', '🇯🇵',
      'El 21 de julio de 1995 salió en Japón <em>J.League Jikkyou Winning Eleven</em> para la primera PlayStation, con los 14 clubes de la J.League de aquel año. '
      'Aquí lo conocimos con otros nombres: <em>Goal Storm</em> y, sobre todo, <em>ISS Pro</em> (1997), el juego que hizo que media Europa '
      'se olvidara un rato de los demás.',
      ['En Japón la saga mantuvo siempre el nombre de <strong>Winning Eleven</strong>; en Europa pasó de ISS Pro a Pro Evolution Soccer.',
       'El primer PES de 2001 era, en Japón, <em>World Soccer: Winning Eleven 5</em>.',
       '<em>ISS Pro Evolution</em> (1999), la tercera entrega de ISS Pro, salió solo para PlayStation y lo hizo el estudio de Konami en Tokio.',
       'Para muchos, ISS Pro Evolution fue el juego que convirtió el fútbol de Konami en un culto en los patios de colegio.'],
      'Lo de leer «Winning Eleven» en una revista japonesa importada era como enterarte de un secreto de Estado.',
      ['Wikipedia (en inglés), «Pro Evolution Soccer» e «ISS Pro Evolution»'])

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
       'El primero solo salió en Europa, con licencia FIFPro para 30.000 jugadores reales y comentarios en inglés de Clive Tyldesley.',
       'En 2010 la marca volvió como juego de gestión, <em>This Is Football Management</em>.'],
      'This Is Football venía en tantas demos de revista que me lo sabía de memoria sin haberlo comprado nunca.',
      ['Wikipedia (en inglés), «This Is Football» y «This Is Football (video game)»'])

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
       'Las licencias de equipos y jugadores no eran de la FIFA, así que siguieron en el juego.',
       'Salió el 29 de septiembre de 2023, hecho por EA Vancouver y EA Romania: la entrega número 31 del fútbol de EA Sports.'],
      'Cambiaron el nombre y yo seguí diciendo «echamos un FIFA». Hay cosas que no se cambian por contrato.',
      ['Game Developer, noviembre de 2023 (cifras de EA)', 'Wikipedia (en inglés), «FIFA (video game series)» y «EA Sports FC 24»'])


# ───────────────────────── fichas nuevas (ampliación 5 nov) ─────────────────────────
ficha('emilio-butragueno', 'Emilio Butragueño Fútbol', 'El Buitre en 8 bits', '1988', 'ZX Spectrum, MSX, Amstrad CPC, Commodore 64 y PC',
      'Topo Soft', '🇪🇸',
      'Mucho antes de las licencias millonarias, un estudio madrileño puso a un jugador del Real Madrid en la portada de un juego de fútbol. '
      '<em>Emilio Butragueño Fútbol</em> lo hizo <strong>Topo Soft</strong> y salió en 1988 para los ordenadores de 8 bits de la época y para PC. '
      'Es de los años de la llamada edad de oro del software español, cuando los juegos se cargaban de una cinta de casete con paciencia y fe.',
      ['Salió para cinco sistemas a la vez: ZX Spectrum, MSX, Amstrad CPC, Commodore 64 y PC.',
       'Llevaba el nombre de una de las grandes estrellas del fútbol español de aquellos años.',
       'Topo Soft era uno de los grandes estudios españoles de los 80, junto a Dinamic y Opera Soft.'],
      'Cargar un juego de cinta duraba más que un partido entero. Y si fallaba, vuelta a empezar. Eso sí que era fútbol de resistencia.',
      ['Wikipedia (en español), «Emilio Butragueño Fútbol»'])

ficha('kick-off', 'Kick Off', 'El balón que no se pegaba al pie', '1989', 'Atari ST, Amiga y más',
      'Dino Dini · Anco Software', '🦶',
      'Creado por <strong>Dino Dini</strong> y publicado por Anco Software en 1989 para Atari ST y Amiga, <em>Kick Off</em> fue un bombazo. '
      'Su gran idea: el balón no iba pegado al pie del jugador. Tenías que llevarlo tú, con vista desde arriba y a toda velocidad. '
      'Difícil al principio, adictivo para siempre.',
      ['Ganó premios en su época y tuvo varias secuelas.',
       'Lo publicó Anco Software, la editora de Anil Gupta.',
       'Su vista cenital y su ritmo endiablado marcaron a toda una generación de juegos de fútbol de ordenador.'],
      'Yo con Kick Off aprendí lo que es correr detrás del balón sin alcanzarlo nunca. Como en el fútbol de verdad, vamos.',
      ['Wikipedia (en inglés), «Kick Off (video game)»'])

ficha('captain-tsubasa', 'Captain Tsubasa (Oliver y Benji)', 'Campos de 20 kilómetros', '1988', 'NES (Nintendo)',
      'Tecmo', '🌟',
      'Sí, el de <strong>Oliver y Benji</strong>. En Japón, Tecmo lo lanzó como <em>Captain Tsubasa</em> para la NES, y en Europa llegó como '
      '<em>Tecmo Cup Football Game</em>, sin los personajes del anime. No era un juego de fútbol normal: elegías la jugada en un menú, '
      'como en un juego de rol, y veías la acción en escenas animadas. El objetivo: subir desde la liga infantil hasta la final del Mundial.',
      ['En Estados Unidos se llamó <em>Tecmo Cup Soccer Game</em>.',
       'Los partidos se jugaban por turnos, con menús de pase, regate y tiro.',
       'La saga de Captain Tsubasa ha tenido muchos más juegos después.'],
      'Un tiro de Oliver tardaba tres capítulos en llegar a la portería. En el juego, menos. Pero poco menos.',
      ['Wikipedia (en inglés), «Tecmo Cup Soccer Game»'])

ficha('sensible-soccer', 'Sensible Soccer', 'Sensi, el de los jugadores diminutos', '1992', 'Amiga, Atari ST, PC y más',
      'Sensible Software', '🔭',
      '<em>Sensible Soccer</em>, «Sensi» para los amigos, salió en 1992 para Amiga, Atari ST y PC. Lo crearon <strong>Jon Hare y Chris Yates</strong> '
      'en Sensible Software, y era la evolución de su <em>MicroProse Soccer</em> de 1988. Jugadores diminutos, cámara muy alejada y una '
      'jugabilidad tan rápida y limpia que sigue teniendo fans hoy.',
      ['Su antecesor, <em>MicroProse Soccer</em> (1988), se inspiraba en la recreativa <em>Tehkan World Cup</em> de 1985.',
       'Fue de los más populares de principios de los 90 y todavía conserva seguidores.',
       'Con la cámara tan alejada veías medio campo de un vistazo, y eso cambiaba la forma de jugar.'],
      'Los jugadores de Sensi medían cuatro píxeles. Yo igual, pero en habilidad.',
      ['Wikipedia (en inglés), «Sensible Soccer»'])

ficha('super-sidekicks', 'Super Sidekicks', 'El fútbol de los salones recreativos', '1992', 'Neo Geo (recreativa y consola)',
      'SNK', '🕹️',
      'SNK llevó el fútbol a sus máquinas Neo Geo con <em>Super Sidekicks</em> en 1992. Era fútbol de recreativa puro: dos botones, '
      'partidos rápidos y tiros que hacían temblar el mueble. Fue el segundo juego de fútbol de la Neo Geo, tras <em>Soccer Brawl</em> (1991), '
      'y abrió una saga entera.',
      ['Se jugaba con solo dos botones, pensado para echar la moneda y jugar ya.',
       'Salió en recreativa y después en las consolas Neo Geo AES y Neo Geo CD.',
       'Se ha vuelto a publicar en recopilatorios y tiendas digitales.'],
      'Veinte duros, dos botones y un pique con el chaval de al lado. Eso es un Mundial.',
      ['Wikipedia (en inglés), «Super Sidekicks (video game)»'])

ficha('virtua-striker', 'Virtua Striker', 'Polígonos en la recreativa', '1994–', 'Recreativas (Sega)',
      'Sega AM2 (después Amusement Vision)', '💥',
      'Sega llevó el fútbol a los polígonos en los salones recreativos. <em>Virtua Striker</em> nació en Sega AM2, el estudio de <em>Virtua Fighter</em>, '
      'que lo desarrolló de 1994 a 1999. Después la saga pasó a Amusement Vision con <em>Virtua Striker 3</em> y, más tarde, a otro equipo de Sega con <em>Virtua Striker 4</em>.',
      ['Fue de los juegos que llevaron el fútbol en 3D a las recreativas.',
       'Lo empezó el mismo estudio que hizo Virtua Fighter.',
       'La saga siguió hasta Virtua Striker 4, ya con otro equipo de Sega.'],
      'Virtua Striker era el juego al que ibas cuando el de las peleas estaba ocupado. Y acababas quedándote.',
      ['Wikipedia (en inglés), «Virtua Striker»'])

ficha('championship-manager', 'Championship Manager y Football Manager', 'Los mánagers que te robaban la vida', '1992–hoy', 'Amiga, Atari ST, PC, Mac…',
      'Sports Interactive', '📋',
      'Dos hermanos, Paul y Oliver Collyer, programaron en su habitación de Shropshire (Inglaterra) un mánager de fútbol. Salió en 1992 como '
      '<em>Championship Manager</em> y se convirtió en el rey de los mánagers a finales de los 90. En 2003, tras el fiasco de <em>Championship Manager 4</em>, '
      'rompieron con su editora, Eidos: Sports Interactive se quedó el motor y los datos, perdió el nombre y renació en 2004 como '
      '<strong>Football Manager</strong>, ya con Sega.',
      ['<em>Championship Manager 01/02</em> vendió más de 300.000 copias en Reino Unido, se liberó gratis en 2008 y la comunidad lo sigue actualizando.',
       'El primer Football Manager, <em>FM 2005</em>, salió el 4 de noviembre de 2004.',
       'En Norteamérica, Football Manager se llamó durante años <em>Worldwide Soccer Manager</em>.'],
      'Football Manager es el único juego que te hace mirar las estadísticas de un lateral de la Segunda de Bélgica a las tres de la mañana.',
      ['Wikipedia (en inglés), «Championship Manager», «Championship Manager 01/02», «Football Manager» y «Football Manager 2005»'])

ficha('fifa-98', 'FIFA: Rumbo al Mundial 98', 'El FIFA de Raúl', '1997', 'PlayStation, PC, Nintendo 64, Saturn, Mega Drive, Super Nintendo…',
      'EA Canada · EA Sports', '🇫🇷',
      'Para muchos, el primer FIFA que de verdad enamoraba. <em>FIFA: Road to World Cup 98</em> salió en 1997 y la crítica lo recibió como la vuelta '
      'a la buena forma de la saga. Clasificación para el Mundial de Francia, fútbol sala en pista cubierta y un detalle muy nuestro: '
      'en la portada española salía <strong>Raúl</strong>.',
      ['Cada país tenía su portada: Raúl en España y Portugal, Beckham en Reino Unido, Maldini en Italia, Ginola en Francia, Möller en Alemania.',
       'Fue el último FIFA que salió para Mega Drive, Saturn y Super Nintendo.',
       'Era la quinta entrega de la saga y la segunda en 3D en las consolas de su generación.'],
      'Jugar la fase de clasificación con Islas Feroe solo para sufrir. Todos lo hicimos. No mintáis.',
      ['Wikipedia (en inglés), «FIFA: Road to World Cup 98»'])

ficha('pes-5-y-6', 'PES 5 y PES 6', 'El pico de la montaña', '2005–2006', 'PlayStation 2, PC, Xbox 360, PSP, Nintendo DS',
      'Konami', '🏔️',
      'Si hay dos PES que salen siempre en las conversaciones de bar, son estos. <em>Pro Evolution Soccer 5</em> (2005, en Japón <em>Winning Eleven 9</em>) '
      'y <em>Pro Evolution Soccer 6</em> (2006) son para muchos el punto más alto de la saga en la era de PS2. El fútbol de Konami en estado puro.',
      ['PES 6 fue el primer PES en Xbox 360 y en Nintendo DS.',
       'En Estados Unidos PES 6 se llamó <em>Winning Eleven: Pro Evolution Soccer 2007</em>.',
       'Desde PES 6 venía una liga de equipos genéricos totalmente editable.',
       'PES 6 se sigue jugando hoy con parches y plantillas hechas por fans.'],
      'PES 6 no es un juego, es un patrimonio. Que lo declare la UNESCO ya, que yo firmo.',
      ['Wikipedia (en inglés), «Pro Evolution Soccer 5», «Pro Evolution Soccer 6» y «Pro Evolution Soccer»'])

ficha('fifa-street', 'FIFA Street', 'Filigranas en la calle', '2005', 'PlayStation 2, Xbox, GameCube',
      'EA Canada · EA Sports BIG', '🛹',
      'EA sacó el fútbol del estadio y lo llevó a la calle. <em>FIFA Street</em> salió en febrero de 2005: partidos pequeños, paredes, '
      'trucos imposibles y cero árbitros. En la portada, el rey de las filigranas de aquellos años: <strong>Ronaldinho</strong>.',
      ['Lo publicó EA Sports BIG, la marca de EA para sus juegos de deporte más locos.',
       'Lo comentaba MC Harvey, del grupo británico So Solid Crew.',
       'Tuvo varias secuelas y la idea acabó entrando en los FIFA como modo Volta.'],
      'En FIFA Street yo hacía una rabona, me la quitaban y me metían gol. Pero la rabona fue preciosa.',
      ['Wikipedia (en inglés), «FIFA Street (2005 video game)»'])

ficha('redcard', 'RedCard', 'Fútbol sin reglas (casi)', '2002', 'PlayStation 2, Xbox, GameCube',
      'Point of View', '🟥',
      'Imagina un partido de fútbol donde las entradas a lo bestia están permitidas. Eso era <em>RedCard</em> (en EE. UU., <em>RedCard 2003</em>), de 2002. '
      'Respetaba casi todas las reglas del fútbol, pero te dejaba repartir a lo loco y cargar una barra para hacer jugadas especiales.',
      ['En Europa se llamó simplemente <em>RedCard</em>.',
       'Las entradas brutales eran parte del juego, no una falta.',
       'Al llenar el medidor de especiales se desbloqueaban tiros y jugadas imposibles.'],
      'RedCard es lo que pasa cuando el árbitro se va a por un bocadillo. Yo lo vi en un partido de barrio. Literal.',
      ['Wikipedia (en inglés), «RedCard 2003»'])

ficha('mario-strikers', 'Super Mario Strikers', 'Fútbol con caparazones', '2005', 'GameCube (y la secuela en Wii)',
      'Next Level Games · Nintendo', '🍄',
      'Nintendo puso a Mario y compañía a jugar al fútbol a cinco, con vallas eléctricas, caparazones, plátanos y supertiros. '
      '<em>Super Mario Strikers</em> salió en Europa el 18 de noviembre de 2005 para GameCube. Rápido, físico y perfecto para pique de sofá.',
      ['Lo hizo Next Level Games, que antes había trabajado en un juego de hockey, y se nota en lo físico de los choques.',
       'Fue el último juego de Mario que salió en GameCube en Japón y Norteamérica.',
       'Su secuela, <em>Mario Strikers Charged</em>, llegó a Wii en 2007.'],
      'Lanzarle un caparazón al portero rival. No sé por qué la FIFA no lo ha aprobado todavía.',
      ['Wikipedia (en inglés), «Super Mario Strikers» y «Mario Strikers Charged»'])

ficha('pes-2008', 'PES 2008', 'El año del cambio de nombre', '2007', 'PS3, Xbox 360, PS2, PC, Wii, PSP, DS',
      'Konami', '📅',
      'Con <em>PES 2008</em>, Konami cambió el número por el año. ¿Motivo? Los FIFA ya usaban el año en el título y, con números, '
      'parecía que el PES iba un año por detrás. Fue también el primer PES de la nueva generación de consolas para muchos jugadores.',
      ['Se anunció el 18 de junio de 2007.',
       'Fue el primer juego con el nombre «PES» en Estados Unidos, donde antes se usaba el nombre japonés.',
       'En la versión española, <strong>Julio Maldonado «Maldini»</strong> se unió a Juan Carlos Rivero en los comentarios.'],
      'Cambiaron el número por el año para no parecer más viejos que el FIFA. Yo hago lo mismo con mi edad.',
      ['Wikipedia (en inglés), «Pro Evolution Soccer 2008»', '3DJuegos, noticia sobre Maldini en PES 2008'])

ficha('fifa-09', 'FIFA 09 y el nacimiento de Ultimate Team', 'Los sobres que cambiaron el negocio', '2008', 'PS3, Xbox 360, PS2, PC, Wii, PSP, DS',
      'EA Canada · EA Sports', '🃏',
      '<em>FIFA 09</em> salió en octubre de 2008 y trajo algo que cambiaría la industria: <strong>Ultimate Team</strong>, el modo en el que montas '
      'un equipo de estrellas abriendo sobres de jugadores. Hoy es el corazón económico de los juegos de fútbol de EA.',
      ['Ultimate Team se estrenó con FIFA 09 y hoy sigue en EA Sports FC.',
       'Permite mezclar jugadores de cualquier equipo para jugar contra otros o contra la máquina.',
       'FIFA 09 salió para ocho plataformas, de PS3 y Xbox 360 a Nintendo DS.'],
      'Ultimate Team: la forma más cara de que te salga un central de Segunda en un sobre.',
      ['Wikipedia (en inglés), «FIFA 09» y «FIFA Ultimate Team»'])

ficha('pes-2013', 'PES 2013', 'El último gran PES (y sigue vivo)', '2012', 'PS3, Xbox 360, PC, PS2, Wii, PSP',
      'Konami', '💚',
      'Para muchos, el último gran PES antes del cambio de motor. <em>PES 2013</em> se anunció el 18 de abril de 2012 y llegó con la Champions, '
      'la Europa League y, por primera vez, los 20 equipos de la liga brasileña. Fue el último PES en Wii.',
      ['Fue el primero con los 20 equipos del Brasileirão.',
       'Tenía las licencias de la Champions League y la Europa League.',
       'Más de una década después, la comunidad lo sigue actualizando con parches y plantillas nuevas.'],
      'PES 2013 tiene más temporadas jugadas que muchos entrenadores de LaLiga. Y con mejores resultados.',
      ['Wikipedia (en inglés), «Pro Evolution Soccer 2013»'])

# ───────────────────────── PC Fútbol ─────────────────────────
PCF = '''
<figure class="port-pcf"><img src="/img/especiales/futbol/pc-futbol.webp" alt="Portada de PC Fútbol 5.0" width="300" height="298" loading="lazy"><figcaption>PC Fútbol 5.0 · Portada © sus titulares</figcaption></figure>
<p>Si eres de aquí y tuviste un PC en los noventa, esto no hace falta explicártelo. <strong>PC Fútbol</strong> no era un juego: era una forma de
vivir la temporada. Fichajes, entrenamientos, la base de datos con todos los jugadores de la Liga, las finanzas del club… y Michael Robinson
como cara visible de todo.</p>
<div class="cifras">
  <div><b>1992</b><span>Simulador Profesional de Fútbol, el abuelo</span></div>
  <div><b>305.000</b><span>copias de PC Fútbol 5.0 (temporada 96/97)</span></div>
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
<h3>PC Fútbol 5.0, el más mítico</h3>
<p>Salió en enero de 1997 para la temporada 96/97. Fue el primero hecho para Windows 95 y el primero con funciones de Internet. Y no era solo un juego:
traía una base de datos con los jugadores de Primera, Segunda y Segunda B, un asistente para la quiniela (<strong>Proquinielas</strong>), un boletín de
fútbol en línea (<strong>Infofútbol</strong>) y hasta un anuario impreso de la temporada anterior dentro de la caja.</p>
<h3>El final y lo que vino después</h3>
<p>En marzo de 1999 el equipo original vendió su parte y se marchó a fundar <strong>FX Interactive</strong>. <em>PC Fútbol 2000</em> fue la primera
entrega sin ellos, y <em>PC Fútbol 2001</em> se retrasó hasta marzo y subió de precio. Años más tarde, el espíritu volvió con
<em>FX Fútbol</em> (2013) y con <em>Football Club Simulator 19</em> (2019), presentado como su sucesor espiritual.</p>
<p>Entre medias, la marca PC Fútbol siguió viva: las versiones de 2005 a 2007 las hizo <strong>Gaelco Multimedia</strong> y las distribuyó Planeta DeAgostini,
y en 2018 salió una versión para móviles Android e iOS, la primera que no apareció en PC.</p>
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

FUENTES = sorted({f for x in F for f in x['fuentes']} | {'Xataka, «PC Fútbol cumple 25 años» (18 de enero de 2019)', 'Wikipedia (en inglés), «PC Fútbol 5.0»', 'Wikipedia (en español), «PC Fútbol»', '3DJuegos (comentaristas de PES 2008 y de FIFA)', 'Foro Evo-Web («The Retro-PES Corner») y Reddit (r/WEPES)'})

VOCES = '''<h2 id="voces">🎙️ Las voces que nos acompañaron</h2>
<p>Un juego de fútbol no es nada sin quien lo cuenta. En España, dos parejas de comentaristas se quedaron para siempre en nuestra memoria:</p>
<div class="cifras dos">
  <div><b>FIFA</b><span><strong>Manolo Lama y Paco González</strong> pusieron voz a los FIFA durante unos 25 años, un cuarto de siglo de frases míticas, y se despidieron con la llegada de EA Sports FC.</span></div>
  <div><b>PES</b><span><strong>Juan Carlos Rivero</strong> narraba el PES desde hacía años cuando, en PES 2008, se le unió <strong>Julio Maldonado «Maldini»</strong>.</span></div>
</div>
<div class="nota"><img src="/img/trollaco.png" alt=""><p><b>EL TROLLACO OPINA:</b> Yo me sé más frases de Manolo Lama que de mi profesor de Historia. Y me han servido más.</p></div>
<p class="fu">Fuentes: 3DJuegos (noticia sobre Maldini en PES 2008 y reportaje sobre Manolo Lama y Paco González en EA Sports FC 24).</p>'''

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
.ficha-j .port{background:#0d0628}.ficha-j .port img{width:100%;height:100%;object-fit:contain;display:block}
.ficha-j h3{margin:0;font-family:'Righteous',sans-serif;font-weight:400;font-size:28px;color:#fff;line-height:1.1}.era-intro{font-size:18px;color:#d9d0f0;margin-top:-4px}.ficha-j .sub{font-family:'VT323',monospace;font-size:21px;color:var(--pink)}
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
.port-pcf{float:right;width:180px;margin:0 0 12px 18px}.port-pcf img{width:100%;height:auto;border-radius:10px;border:2px solid var(--yellow);display:block}.port-pcf figcaption{font-size:12px;color:#bdb3d9;margin-top:4px}
.migas{font-family:'VT323',monospace;font-size:18px;color:#bdb3d9}.migas a{color:#bdb3d9}
.fuentes-l li{font-size:15px;line-height:1.5;color:#bdb3d9}
@media(max-width:700px){.port-pcf{width:130px}.cifras{grid-template-columns:1fr}.cifras.dos{grid-template-columns:1fr}.ficha-j .cab{grid-template-columns:84px 1fr;gap:14px}.ficha-j .port{width:84px;font-size:40px}.esp p,.esp li{font-size:18px}}
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
<div class="cab">{portada(x)}<div><span class="sub">&gt; {esc(x['sub'].upper())}_</span><h3>{esc(x['titulo'])}</h3>
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
ERAS = [
    ('pioneros', '🕹️ Los pioneros: 8 y 16 bits', 'Cintas de casete, disquetes y cartuchos. Aquí empezó todo: de un estudio madrileño a Dino Dini, de Oliver y Benji al primer FIFA.',
     ['emilio-butragueno', 'kick-off', 'captain-tsubasa', 'sensible-soccer', 'iss', 'fifa']),
    ('recreativa', '👾 Fútbol de recreativa', 'Monedas de veinte duros, botones gastados y piques con desconocidos. El fútbol de los salones recreativos.',
     ['super-sidekicks', 'virtua-striker']),
    ('managers', '📋 Los mánagers', 'Además de PC Fútbol (más arriba), hubo otro mánager que robó millones de horas de sueño en media Europa.',
     ['championship-manager']),
    ('oro', '🏆 La edad de oro: PlayStation y PS2', 'La época de la gran rivalidad. Konami contra EA, Winning Eleven contra FIFA, y Sony, Infogrames y Eidos metiendo cabeza.',
     ['winning-eleven', 'fifa-98', 'this-is-football', 'champions', 'ronaldo', 'pes', 'pes-5-y-6']),
    ('locura', '🤪 Fútbol loco y rarezas', 'Fútbol de calle, fútbol sin reglas, fútbol con caparazones… y una joya japonesa que casi nadie jugó aquí.',
     ['football-kingdom', 'fifa-street', 'redcard', 'mario-strikers']),
    ('hd', '📺 La era HD', 'Nuevas consolas, modos online y un modo de juego que cambió el negocio para siempre.',
     ['pes-2008', 'fifa-09', 'pes-2013']),
    ('hoy', '🔄 Hoy: eFootball y EA Sports FC', 'El PES se convierte en free-to-play y FIFA cambia de nombre. Así está el partido ahora.',
     ['efootball', 'ea-sports-fc']),
]
usadas = [s for e in ERAS for s in e[3]]
assert sorted(usadas) == sorted(x['slug'] for x in F), set(x['slug'] for x in F) ^ set(usadas)
indice = ''.join(f'<a href="#{i}">{t}</a>' for i, t in [('linea', '🕰️ Línea del tiempo'), ('pc-futbol', '💾 PC Fútbol')] + [(e[0], e[1]) for e in ERAS] +
    [('voces', '🎙️ Las voces'), ('licencias', '🏷️ Licencias'), ('comunidad', '🛠️ Parches y mods'), ('numeros', '📊 Los números')])
FIRMA = ('<div class="firma"><img src="/img/danna.jpg?v=4" alt="Danna" width="56" height="56"><div><b>Por Danna</b>'
         f'<span>Tu reportera del otro lado de la pantalla · <a href="https://www.instagram.com/dannapixel/" target="_blank" rel="noopener">📸 @dannapixel</a> · <a href="/danna/">¿Quién es?</a> · {FECHA}</span></div></div>')
def html_era(e):
    fichas = ''.join(html_ficha(next(x for x in F if x['slug'] == sl)) for sl in e[3])
    return f'<h2 id="{e[0]}">{e[1]}</h2><p class="era-intro">{e[2]}</p>{fichas}'
eras_html = ''.join(html_era(e) for e in ERAS)
fuentes = ''.join(f'<li>{esc(f)}</li>' for f in FUENTES)

titulo = 'De ISS a EA Sports FC: la historia de los juegos de fútbol'
desc = 'El especial más nostálgico de Trollacos: más de 25 juegos de fútbol, de Emilio Butragueño Fútbol y Kick Off a PES 6, PC Fútbol, Oliver y Benji, FIFA, Football Manager, eFootball y EA FC. Portadas, datos, ventas, voces, licencias y parches.'
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
<p class="fu">Fuentes: Xataka, «PC Fútbol cumple 25 años» (18 de enero de 2019); Wikipedia (en inglés), «PC Fútbol 5.0»; Wikipedia (en español), «PC Fútbol».</p></section>
{eras_html}
{VOCES}
<h2 id="licencias">🏷️ La guerra de las licencias</h2>
{LICENCIAS}
<p class="fu">Fuente: Wikipedia (en inglés), «Pro Evolution Soccer» y «FIFA (video game series)».</p>
<h2 id="comunidad">🛠️ Parches, mods y la comunidad que no se rinde</h2>
{COMUNIDAD}
<p class="fu">Fuentes: Wikipedia (en inglés), «Pro Evolution Soccer»; foro Evo-Web («The Retro-PES Corner»); Reddit, r/WEPES.</p>
<h2 id="numeros">📊 Los números que dan vértigo</h2>
<div class="cifras">
  <div><b>+325 M</b><span>copias vendidas de la saga FIFA hasta 2021 (Guinness World Records)</span></div>
  <div><b>111 M</b><span>copias de PES y 400 millones de descargas en móvil a diciembre de 2020 (Konami)</span></div>
  <div><b>3,2 M</b><span>copias de FIFA 12 en su primera semana: récord de juego deportivo</span></div>
  <div><b>370.000</b><span>copias de PC Fútbol 7.0 en España (Xataka)</span></div>
  <div><b>+300.000</b><span>copias de Championship Manager 01/02 en Reino Unido</span></div>
  <div><b>14,5 M</b><span>jugadores de EA Sports FC 24 en sus cuatro primeras semanas (EA)</span></div>
</div>
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
