"""Genera /privacidad/ y /aviso-legal/ con el estilo de la guía.
Uso: python3 _fuentes/generadores/legal.py   (desde cualquier sitio)"""
import os
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(RAIZ)
g = open('gta-6/index.html', encoding='utf-8').read()
style = g[g.find('<style>'):g.find('</style>') + 8]
foot = g[g.find('<footer>'):g.find('</footer>') + 9]
TITULAR = 'José Guillermo Fernández Rey'
CONTACTO = 'info@trollacos.com'
ACTUALIZADO = '2 de noviembre de 2026'

def pagina(ruta, titulo, desc, cuerpo):
    html = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} | Trollacos</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://trollacos.com/{ruta}/">
<link rel="icon" href="/icono.png">
{style.replace('</style>', '.legal{max-width:780px;margin:0 auto}.legal h2{margin-top:30px}.legal p,.legal li{font-size:17px}.legal table{border-collapse:collapse;width:100%;font-size:15px}.legal td,.legal th{border:1px solid rgba(233,230,255,.2);padding:8px;text-align:left;vertical-align:top}</style>')}
</head>
<body>
<div class="scan"></div>
<nav class="top">
  <a href="/"><img class="px" src="/logo.webp" alt="Trollacos" width="1600" height="161"></a>
  <a href="/">‹ PORTADA</a>
</nav>
<header class="cab"><div class="etq">&gt; LA LETRA PEQUEÑA_</div><h1>{titulo}</h1>
<p class="entradilla">Última actualización: {ACTUALIZADO}.</p></header>
<main class="legal">
{cuerpo}
</main>
{foot}
</body>
</html>
'''
    os.makedirs(ruta, exist_ok=True)
    open(f'{ruta}/index.html', 'w', encoding='utf-8').write(html)

privacidad = f'''
<p>En Trollacos nos tomamos tus datos en serio, aunque nos tomemos poco en serio todo lo demás. Aquí te contamos, sin rodeos, qué guardamos, para qué y cómo puedes borrarlo.</p>

<h2>Quién es el responsable</h2>
<p><strong>{TITULAR}</strong>, titular de trollacos.com. Para cualquier cosa sobre tus datos: <a href="mailto:{CONTACTO}">{CONTACTO}</a>.</p>

<h2>Qué datos guardamos y para qué</h2>
<table>
<tr><th>Dato</th><th>Para qué</th><th>Base legal</th><th>Cuánto tiempo</th></tr>
<tr><td>Tu <b>cuenta de jugador</b>: nombre de 2 a 5 letras, código secreto (guardado cifrado, nunca en claro), fichas, partidas, récords y pronósticos de La Porra</td><td>Que puedas jugar, guardar tu progreso y salir en los rankings</td><td>Prestarte el servicio que pides al crear la cuenta</td><td>Mientras tengas la cuenta</td></tr>
<tr><td>Tu <b>email</b> (opcional), guardado <b>cifrado</b></td><td>Confirmar que es tuyo y mandarte enlaces para entrar en tu cuenta</td><td>Prestarte el servicio que pides al añadirlo</td><td>Hasta que lo quites de tu cuenta o nos pidas borrarlo</td></tr>
<tr><td>Tu email, si marcas la casilla del <b>boletín</b>, y la fecha en que te apuntaste</td><td>Mandarte el boletín de Trollacos: noticias de GTA VI y videojuegos, novedades de la web y ofertas que nos parezcan interesantes</td><td>Tu consentimiento, que puedes retirar cuando quieras</td><td>Hasta que te des de baja</td></tr>
<tr><td>Un <b>resumen cifrado y temporal de la conexión</b> (no guardamos tu IP)</td><td>Evitar trampas y abusos: demasiados intentos de entrada, cuentas en masa o envíos de correos</td><td>Interés legítimo en proteger la web</td><td>Entre una hora y un día</td></tr>
</table>
<p>Los datos de juego que ves en los rankings (nombre de jugador, puntos y fichas) son públicos dentro de la web. Tu email nunca se muestra a nadie.</p>

<h2>Lo que se guarda en tu navegador</h2>
<p>Usamos el almacenamiento local de tu navegador para recordar tu récord, tu progreso en el modo historia, tu nombre de jugador, tu sesión y si has quitado el sonido. No usamos cookies de publicidad ni de analítica, y no seguimos lo que haces en otras webs. Puedes borrarlo cuando quieras desde los ajustes del navegador.</p>
<p>Algunos contenidos de terceros, como el mapa interactivo de la guía de GTA VI o los vídeos, se cargan desde sus propias webs, que tienen sus propias políticas. Los enlaces a Amazon son de afiliado: al pulsarlos pasas a Amazon, que aplica su propia política de privacidad.</p>

<h2>Menores</h2>
<p>Para añadir un email a la cuenta o apuntarte al boletín tienes que tener <b>14 años o más</b>. Si tienes menos, puedes jugar con tu cuenta de jugador sin email.</p>

<h2>Con quién compartimos tus datos</h2>
<p>Con nadie. No vendemos ni cedemos datos. La web está alojada en DonDominio (España), que guarda los ficheros por cuenta nuestra, y los correos salen desde nuestro propio dominio.</p>

<h2>Tus derechos</h2>
<p>Puedes pedir en cualquier momento <b>ver, corregir o borrar</b> tus datos, oponerte a su uso, limitarlo o llevártelos. Muchas cosas las puedes hacer tú mismo:</p>
<ul>
<li>Quitar tu email o borrarte del boletín: desde <a href="/cuenta/">Mi cuenta</a>.</li>
<li>Darte de baja del boletín: con el enlace que va al final de cada boletín.</li>
<li>Para todo lo demás, incluido borrar tu cuenta entera: escribe a <a href="mailto:{CONTACTO}">{CONTACTO}</a> desde el email de tu cuenta o diciéndonos tu nombre de jugador.</li>
</ul>
<p>Si crees que no hemos tratado bien tus datos, puedes reclamar ante la Agencia Española de Protección de Datos (aepd.es).</p>

<h2>Seguridad</h2>
<p>Los códigos de las cuentas se guardan cifrados y los emails, encriptados. Para entrar con el email no hay contraseñas: mandamos enlaces de un solo uso que caducan a los 30 minutos.</p>
'''

aviso = f'''
<h2>Titular de la web</h2>
<p>trollacos.com es una web de <b>{TITULAR}</b>. Contacto: <a href="mailto:{CONTACTO}">{CONTACTO}</a>.</p>

<h2>Qué es Trollacos</h2>
<p>Una web de entretenimiento: humor, videojuegos, la guía de GTA VI, el arcade Trollaco Run, el Expediente Trollaco y La Porra Trollaca.</p>

<h2>Enlaces de afiliado</h2>
<p>Como Afiliado de Amazon, Trollacos obtiene ingresos por las compras adscritas que cumplen los requisitos aplicables. Si compras desde nuestros enlaces, a ti no te cuesta nada más.</p>

<h2>La Porra y el arcade: sin dinero real</h2>
<p>Las fichas del arcade y de La Porra Trollaca son <b>solo de juego</b>: no se compran, no se venden y no se canjean por dinero ni por premios. La Porra no es una casa de apuestas ni un juego de azar con dinero. Las cuotas son nuestras, calculadas a partir de la clasificación, y no son de ninguna casa de apuestas.</p>

<h2>Propiedad intelectual: todo esto es nuestro</h2>
<p>Todos los contenidos de trollacos.com son propiedad de <b>{TITULAR}</b> (Trollacos) o se usan con permiso, y están protegidos por la Ley de Propiedad Intelectual (Real Decreto Legislativo 1/1996) y por el resto de normas españolas e internacionales. Esto incluye, entre otras cosas:</p>
<ul>
<li>La marca y el nombre <b>Trollacos</b>, el logotipo, el estilo y el diseño de la web.</li>
<li>Los personajes: <b>el Trollaco</b>, <b>Danna</b>, la Princesa Neón, Míster Glitch y todos los demás.</li>
<li>Los juegos: <b>Trollaco Run</b> (el modo «Supera el récord» y el modo historia, con sus capítulos, guiones, diálogos, gráficos, música y efectos), <b>La Porra Trollaca</b> y su sistema de fichas, y el <b>Expediente Trollaco</b>.</li>
<li>Los textos, las noticias, la guía de GTA VI, las ilustraciones, los vídeos, la música y el código fuente de la web.</li>
</ul>
<p><b>Queda prohibido</b> copiar, reproducir, distribuir, publicar, transformar o usar con fines comerciales cualquiera de estos contenidos, total o parcialmente, sin nuestro permiso por escrito. Si quieres usar algo (por ejemplo, citar una noticia o compartir una captura del juego), puedes enlazar a la página original citando a Trollacos. Para cualquier otra cosa, pídenos permiso en <a href="mailto:{CONTACTO}">{CONTACTO}</a>.</p>
<p>Si vemos copias de nuestros contenidos, juegos o diseños, nos reservamos el derecho a pedir su retirada y a emprender las acciones legales que correspondan.</p>

<h2>Marcas de terceros</h2>
<p>Grand Theft Auto, GTA VI y todo lo relacionado son marcas de Rockstar Games y Take-Two Interactive. Trollacos no tiene ninguna relación con ellas: es una web de fans que cuenta las noticias con sus propias palabras. Los escudos y nombres de los equipos de fútbol son de sus clubes y competiciones. Danna, nuestra reportera, es un personaje digital creado por Trollacos.</p>

<h2>Responsabilidad</h2>
<p>Intentamos que todo lo que publicamos sea correcto y citamos siempre las fuentes por su nombre, pero los datos de juegos que aún no han salido pueden cambiar. Los nombres de jugador los eligen los usuarios: si ves alguno ofensivo, escríbenos y lo quitamos.</p>

<h2>Privacidad</h2>
<p>Todo sobre tus datos, en la <a href="/privacidad/">política de privacidad</a>.</p>
'''

pagina('privacidad', 'Política de privacidad', 'Qué datos guarda Trollacos, para qué y cómo borrarlos.', privacidad)
pagina('aviso-legal', 'Aviso legal', 'Titular de trollacos.com, enlaces de afiliado y condiciones de uso.', aviso)
print('ok')
