# Datos del especial «De Liberty City a Leonida: la historia de GTA» (lo usa especial_gta.py).
WP = 'Wikipedia (en inglés), '

TIEMPO = [
    ('1997', 'Grand Theft Auto', 'DMA Design, un estudio de Dundee (Escocia), convierte un juego de policías aburrido en uno de criminales.', 'gta-1'),
    ('1998', 'Nace Rockstar Games', 'Los hermanos Sam y Dan Houser fundan en Nueva York el sello que se quedará con la saga.', 'rockstar'),
    ('1999', 'GTA: London y GTA 2', 'Dos expansiones en el Londres de los 60 y una ciudad del futuro donde las bandas te respetan… o no.', 'gta-2'),
    ('2001', 'Grand Theft Auto III', 'El salto al 3D. Liberty City cambia los videojuegos para siempre.', 'gta-3'),
    ('2002', 'Vice City', 'Neones, trajes de colores y 1986. El juego más vendido del año.', 'vice-city'),
    ('2004', 'San Andreas', 'Tres ciudades, un estado entero y el juego más vendido de la historia de PS2.', 'san-andreas'),
    ('2005', 'Liberty City Stories', 'GTA en el bolsillo: el juego más vendido de PSP.', 'portatiles'),
    ('2008', 'Grand Theft Auto IV', 'Niko Bellic llega a Liberty City y GTA bate tres récords Guinness en 24 horas.', 'gta-4'),
    ('2013', 'Grand Theft Auto V y GTA Online', 'Mil millones de dólares en tres días. Y más de 230 millones de copias después.', 'gta-5'),
    ('2021', 'The Trilogy – Definitive Edition', 'GTA III, Vice City y San Andreas vuelven remasterizados por su 20.º aniversario.', 'gta-3'),
    ('2023', 'Tráiler 1 de GTA VI', '90 millones de visitas en 24 horas: récord Guinness.', 'gta-6'),
    ('2026', 'Grand Theft Auto VI', 'Lucía y Jason, Vice City y el estado de Leonida. Sale el 19 de noviembre.', 'gta-6'),
]

F = []
def ficha(slug, titulo, sub, anio, plataformas, estudio, icono, intro, datos, troll, fuentes):
    F.append(dict(slug=slug, titulo=titulo, sub=sub, anio=anio, plataformas=plataformas, estudio=estudio, icono=icono,
                  intro=intro, datos=datos, troll=troll, fuentes=fuentes))

ficha('gta-1', 'Grand Theft Auto', 'Donde empezó todo', '1997', 'MS-DOS, Windows, PlayStation (y Game Boy Color en 1999)', 'DMA Design · edita BMG Interactive', '🚓',
      'Vista desde arriba, tres ciudades inventadas (Liberty City, San Andreas y Vice City, que ya sonaban) y un objetivo muy simple: hacer encargos para la mafia '
      'hasta juntar millones de puntos. Gráficos sencillos, libertad total y una polémica enorme antes incluso de salir.',
      ['Empezó siendo un juego de <strong>policías</strong> llamado <em>Race \'n\' Chase</em>. Al equipo le parecía aburrido… así que te pasaron al otro lado de la ley.',
       'Antes de salir ya era tan polémico que <strong>la Cámara de los Lores británica</strong> llegó a hablar de prohibirlo.',
       'Salió en <strong>noviembre de 1997</strong> en PC y en diciembre en PlayStation.',
       'Las críticas fueron regulares (gráficos y controles), pero vendió bien y hoy se considera uno de los grandes juegos de la historia.',
       'En 1999 tuvo dos expansiones en el Londres de los 60: <em>London 1969</em> y <em>London 1961</em>.'],
      'Lo de que empezara siendo un juego de policías es la mayor plot twist de la historia del videojuego.',
      [WP + '«Grand Theft Auto (video game)»'])

ficha('gta-2', 'Grand Theft Auto 2', 'El GTA más raro', '1999', 'Windows, PlayStation, Dreamcast, Game Boy Color', 'DMA Design · Rockstar Games', '🏙️',
      'Anywhere City, una ciudad «de algún momento del futuro» con coches de los años 50 con toque futurista y un ambiente bastante deprimente. '
      'Sigue con la cámara desde arriba, pero añade algo que se quedaría en la saga: <strong>las bandas</strong>.',
      ['Siete bandas controlan los barrios, y según los trabajos que hagas cada una te <strong>respeta más o menos</strong>. Las mejores misiones exigen el respeto máximo.',
       'El nivel de búsqueda llegaba a <strong>seis cabezas</strong>: policía, SWAT, agentes especiales… y al final, el ejército.',
       'La intro usaba un <strong>cortometraje de imagen real</strong> rodado en Nueva York para promocionar el juego.',
       'Vendió menos de lo esperado y las críticas fueron regulares. Pero era el paso previo a algo muy gordo.'],
      'Una ciudad del futuro con coches de los 50. Básicamente la M-30 un lunes a las ocho.',
      ['PC Gamer, «Revisiting Grand Theft Auto 2, the weirdest GTA of them all»'])

ficha('gta-3', 'Grand Theft Auto III', 'El salto al 3D', '2001', 'PS2, Windows, Xbox, Mac, móviles (Definitive Edition en 2021)', 'DMA Design (hoy Rockstar North) · Rockstar Games', '🌉',
      'Claude, un criminal que no dice ni una palabra, es traicionado por su novia durante un atraco y acaba en Liberty City buscando venganza. '
      'Por primera vez la ciudad era en 3D, podías ir a cualquier parte y hacer lo que te diera la gana. Cambió los videojuegos para siempre.',
      ['Salió en PS2 el <strong>23 de octubre de 2001</strong>, en Norteamérica.',
       'Tras los atentados del 11-S, Rockstar lo <strong>retrasó tres semanas</strong> y cambió cosas: los colores de los coches de policía, la ruta de un avión, una misión y hasta <strong>la portada</strong>.',
       'Tiene unas <strong>tres horas y media de radio</strong>, con una emisora entera solo de tertulia, Chatterbox FM.',
       'Fue el juego más vendido de 2001 en Estados Unidos y superó los <strong>14,5 millones de copias</strong>.',
       'El nombre del protagonista, Claude, no se supo oficialmente hasta <em>San Andreas</em>.'],
      'El protagonista no habla en todo el juego. Como yo los lunes antes del café.',
      [WP + '«Grand Theft Auto III»'])

ficha('vice-city', 'Grand Theft Auto: Vice City', 'Neones y 1986', '2002', 'PS2, Windows, Xbox (Definitive Edition en 2021)', 'Rockstar North · Rockstar Games', '🌴',
      'Tommy Vercetti sale de la cárcel, un negocio sale mal y le toca abrirse camino en Vice City, una versión de Miami en pleno 1986. '
      'Camisas hawaianas, coches deportivos y música ochentera. La ciudad a la que vuelve GTA VI veinticuatro años después.',
      ['Fue el <strong>juego más vendido de 2002</strong> y superó los <strong>17,5 millones de copias</strong>.',
       'Se inspira en el Miami real de los 80 y, sobre todo, en <em>El precio del poder</em> (<em>Scarface</em>) y <em>Corrupción en Miami</em>.',
       'Salió en PS2 en <strong>octubre de 2002</strong>, un año después de GTA III.',
       'También tuvo su polémica: algunos grupos protestaron por cómo retrataba la violencia y a algunas comunidades, y hubo demandas.'],
      'Vice City en 2002 y Vice City otra vez en 2026. Rockstar sabe lo que nos gusta: el neón.',
      [WP + '«Grand Theft Auto: Vice City»'])

ficha('san-andreas', 'Grand Theft Auto: San Andreas', 'El más grande de PS2', '2004', 'PS2, Windows, Xbox (y móviles y Definitive Edition después)', 'Rockstar North · Rockstar Games', '🏜️',
      'Carl «CJ» Johnson vuelve a casa tras la muerte de su madre y se encuentra su barrio hecho polvo y su banda en las últimas. '
      'Un estado entero con tres ciudades, campo, desierto y montañas. Para muchos, el mejor GTA de la historia.',
      ['Sus tres ciudades son <strong>Los Santos, San Fierro y Las Venturas</strong>, inspiradas en Los Ángeles, San Francisco y Las Vegas.',
       'Superó los <strong>27,5 millones de copias</strong>: fue el más vendido de 2004 y es <strong>el juego más vendido de PS2</strong>.',
       'La historia se inspira en hechos reales de principios de los 90 en Los Ángeles: la rivalidad entre bandas, la epidemia del crack y los <strong>disturbios de 1992</strong>.',
       'Tuvo su polémica gorda en Estados Unidos por un minijuego oculto en el código que los fans desbloquearon.'],
      'Pasé más horas en el gimnasio de San Andreas que en uno de verdad. Y en el de verdad no me suben las barras de estadísticas.',
      [WP + '«Grand Theft Auto: San Andreas»'])

ficha('portatiles', 'Los GTA de bolsillo', 'Advance, Stories y Chinatown Wars', '2004–2009', 'Game Boy Advance, PSP, PS2, Nintendo DS, PSP, móviles', 'Rockstar Leeds y otros estudios · Rockstar Games', '🎮',
      'GTA también fue portátil. Primero <em>Grand Theft Auto Advance</em> (2004) en Game Boy Advance, luego los dos <em>Stories</em> para PSP, que llevaban Liberty City y Vice City en el bolsillo, '
      'y por último <em>Chinatown Wars</em> (2009), que volvió a la cámara desde arriba en la Nintendo DS.',
      ['<strong>Liberty City Stories</strong> salió en PSP en <strong>octubre de 2005</strong> y en PS2 en junio de 2006. Lo protagoniza <strong>Toni Cipriani</strong>, un mafioso que ya salía en GTA III.',
       'Superó los <strong>8 millones de copias</strong> en 2008: <strong>el juego más vendido de PSP</strong>.',
       'Está ambientado en la Liberty City de <strong>1998</strong>, tres años antes de GTA III.',
       '<strong>Vice City Stories</strong> llegó en octubre de 2006, también en PSP y luego en PS2.'],
      'Un GTA entero en una PSP. En 2005 eso era magia. Y vaciaba la batería en dos horas.',
      [WP + '«Grand Theft Auto: Liberty City Stories»'])

ficha('gta-4', 'Grand Theft Auto IV', 'El sueño americano de Niko', '2008', 'PS3, Xbox 360, Windows', 'Rockstar North · Rockstar Games', '🗽',
      'Niko Bellic, un veterano de guerra de Europa del Este, llega a Liberty City para empezar de cero con su primo Roman… y para buscar al hombre que traicionó a su unidad. '
      'Más realista, más serio y con una Liberty City nueva, ahora muy parecida a Nueva York.',
      ['Vendió unos <strong>6 millones de copias y más de 500 millones de dólares</strong> en su primera semana; <strong>3,6 millones</strong> solo el primer día.',
       'Guinness le dio <strong>tres récords</strong>: el juego que más recaudó en 24 horas, el producto de entretenimiento con más ingresos en 24 horas y el juego que más rápido se vendió.',
       'Costó <strong>más de 100 millones de dólares</strong>, uno de los juegos más caros de la historia hasta entonces.',
       'Para recrear la ciudad hicieron <strong>más de 100.000 fotos</strong> en Nueva York (el director de arte calculaba que unas 250.000).',
       'Tuvo dos episodios en 2009: <em>The Lost and Damned</em> y <em>The Ballad of Gay Tony</em>. Y superó los <strong>25 millones de copias</strong> en 2013.'],
      'El primo Roman llamando para ir a los bolos. Ningún jefe final ha sido nunca tan insistente.',
      [WP + '«Grand Theft Auto IV»'])

ficha('gta-5', 'Grand Theft Auto V', 'El juego que no se acaba nunca', '2013', 'PS3, Xbox 360, PS4, Xbox One, Windows, PS5, Xbox Series', 'Rockstar North · Rockstar Games', '💰',
      'Tres protagonistas por primera vez: Michael, un ladrón retirado con una familia que le odia; Franklin, un chaval que quiere salir del barrio; y Trevor, que es… Trevor. '
      'Los Santos vuelve más grande que nunca, con golpes a lo grande y <strong>GTA Online</strong>, que lleva más de una década recibiendo contenido.',
      ['Salió el <strong>17 de septiembre de 2013</strong> en PS3 y Xbox 360.',
       'Recaudó <strong>815,7 millones de dólares</strong> y vendió <strong>11,21 millones</strong> de copias en su primer día, y llegó a <strong>1.000 millones en tres días</strong>.',
       'Guinness le dio <strong>siete récords</strong>, entre ellos el producto de entretenimiento que más rápido ha llegado a los mil millones. Más rápido que cualquier película.',
       'Ha salido en <strong>tres generaciones de consolas</strong>: PS3, PS4 y PS5.',
       'Según Take-Two, en agosto de 2026 ya había vendido <strong>más de 230 millones de copias</strong>.'],
      '230 millones de copias. Hay más GTA V en el mundo que gente en Brasil. Y todavía hay quien no lo ha jugado.',
      ['Guinness World Records (récords de GTA V, octubre de 2013)', 'Outlook Respawn (resultados de Take-Two, agosto de 2026)'])

ficha('gta-6', 'Grand Theft Auto VI', 'La vuelta a Vice City', '2026', 'PS5, Xbox Series X|S (y en la nube de Xbox)', 'Rockstar Games', '🌴',
      'Lucía y Jason, una pareja atrapada en una conspiración criminal, en Vice City y el estado de Leonida, la versión de Rockstar de Florida. '
      'Trece años después de GTA V, el juego más esperado de la historia sale el <strong>19 de noviembre de 2026</strong>.',
      ['El <strong>tráiler 1</strong> salió el 6 de diciembre de 2023 y tuvo <strong>90 millones de visitas en 24 horas</strong>.',
       'Se llevó <strong>tres récords Guinness</strong>: la presentación de un videojuego más vista en YouTube en 24 horas, el tráiler de videojuego con más «me gusta» y el vídeo no musical más visto en 24 horas.',
       'Por primera vez desde que GTA es en 3D, uno de los protagonistas es una mujer: <strong>Lucía</strong>.',
       'Todo lo demás (personajes, mapa, versiones, música y fechas) lo tienes al día en <a href="/gta-6/">nuestra guía de GTA VI</a>.'],
      'Llevo esperándolo desde 2013. He tenido menos paciencia con mi propia vida.',
      ['Push Square (récords del tráiler 1, diciembre de 2023)', 'Rockstar Games'])

ROCKSTAR = '''
<p>En <strong>1998</strong>, los hermanos <strong>Sam y Dan Houser</strong>, dos británicos que trabajaban en BMG Interactive (la editora del primer GTA), fundaron en Nueva York
<strong>Rockstar Games</strong> junto a otros compañeros. DMA Design, el estudio escocés que había creado la saga, acabó formando parte de Rockstar y hoy se llama <strong>Rockstar North</strong>.</p>
<p>Desde entonces, cada GTA ha ido más allá que el anterior: del 2D al 3D con GTA III, del barrio a un estado entero con San Andreas, del realismo de GTA IV a los tres protagonistas de GTA V…
y ahora, a Leonida.</p>
'''

RADIO = '''
<p>Si hay algo que distingue a GTA de cualquier otro juego es <strong>la radio</strong>. Desde el primero, al subirte a un coche suena una emisora, y con el tiempo se convirtieron en
programas completos: música con licencia, anuncios inventados que se ríen de la publicidad de verdad y tertulias absurdas.</p>
<ul class="lista-nombres">
  <li><strong>GTA III</strong> ya tenía unas <strong>tres horas y media</strong> de radio, con una emisora entera de tertulia, <strong>Chatterbox FM</strong>.</li>
  <li><strong>Vice City</strong> convirtió su banda sonora ochentera en parte de la leyenda del juego.</li>
  <li><strong>GTA VI</strong> también tendrá su radio: la música que se sabe de momento la tienes en <a href="/gta-6/musica/">nuestra página de música de GTA VI</a>.</li>
</ul>
'''

FUENTES_EXTRA = [WP + '«Rockstar Games»']
