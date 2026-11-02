# Trollacos.com — manual del proyecto

Web de Guillermo (marca Trollacos, nacida en 2012 y relanzada en 2026). Humor, videojuegos, GTA VI, arcade, misterio y La Porra.
Estilo **synthwave** (rosa #ff2bd6, cian #1ff2ff, amarillo #ffd23f, fondo #07021a) con la mascota pixel art **el Trollaco**.
Hablar con Guillermo en **español de España**, con humor y trato directo y honesto.

## Cómo funciona
- Repositorio: `trollacosweb/trollacos-web` (GitHub). Web estática + algo de PHP en `api/`.
- Hosting: DonDominio (PHP), dominio trollacos.com con SSL de pago. FTP: `ftp.trollacos.com`.
- **Despliegue automático:** `.github/workflows/actualizar-noticias.yml` se lanza en cada push a `main`, por cron y a mano (`workflow_dispatch`):
  partidos de LaLiga → commit → subida por FTPS (con reintento) → aviso IndexNow → comprobación de los rankings (sale como `::notice::`).
  Para ver resultados: anotaciones del run (`gh api repos/trollacosweb/trollacos-web/check-runs/<job>/annotations`).
- Secretos de GitHub (los pone Guillermo, **nunca** pegarlos en el chat): `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`, `FOOTBALL_DATA_KEY` (ya no hace falta).
- Excluidos del FTP: `.github/`, `scripts/`, `_fuentes/`, `CLAUDE.md`, `api/datos/`, `node_modules`.

## Secciones
| Ruta | Qué es | Se genera con |
|---|---|---|
| `/` | Portada (noticias propias firmadas por Danna, tienda Amazon, banners) | a mano + `noticias_gta.py` (bloques GTA y NOTICIAS + rss.xml) |
| `/gta-6/` | Guía GTA VI (mapa, novedades, tráilers, FAQ) | a mano |
| `/gta-6/musica/` | Música con enlaces a Spotify | `_fuentes/generadores/musica.py` |
| `/gta-6/que-comprar/` | Guía de compra (afiliados Amazon) | `_fuentes/generadores/compra.py` |
| `/arcade/` | Trollaco Run: Modo historia (5 capítulos con diálogos) + "Supera el récord" | a mano (canvas JS) |
| `/porra/` | La Porra Trollaca (pronósticos LaLiga con fichas, sin dinero) | `_fuentes/generadores/porra.py` |
| `/cuenta/` | Mi cuenta: estadísticas, insignias | `_fuentes/generadores/cuenta.py` |
| `/misterio/` (+ `espana/`, `mundo/`) | Expediente Trollaco, mapas Leaflet | `_fuentes/generadores/misterio/generar.py` |
| `/redes/` | Imágenes y textos para Instagram (no indexado) | `_fuentes/generadores/redes.py` |
| `/privacidad/`, `/aviso-legal/` | Textos legales (titular, info@trollacos.com, afiliados, RGPD) | `_fuentes/generadores/legal.py` |

Los generadores tienen rutas fijas: copiar `_fuentes/generadores/` a `/home/claude/trollaco/` y el repo en `/home/claude/trollacos-web/`.
Capturas y renders con Playwright: `chromium.launch({executablePath:'/opt/pw-browsers/chromium'})`. Probar PHP en local con `php -S 127.0.0.1:8099 -t .`.

## API (PHP, en `api/`)
- `comun.php`: cabeceras, secreto HMAC autogenerado, filtro de nombres (2-5 caracteres, una palabra, lista de palabras prohibidas + `bloqueados.php`), fichas de partida firmadas.
- `arcade_lib.php`: modos `run, c1..c5`, `TEMPORADA` (cambiarla borra rankings), jugadores de relleno (solo en "run", nunca echan a reales; JAM85 debe seguir 1º), `marca_jugador()`.
- `marcadores.php?accion=lista|empezar|enviar&modo=…`: rankings del arcade (una marca por nombre).
- `porra.php?accion=partidos|ranking|registrar|yo|perfil|arcade|apostar|cancelar`: cuentas (nombre + código de 8), fichas, pronósticos 1X2 y exacto (x8), bono 10 por alta y 10 por jornada, liquidación automática, cancelar hasta 5 min antes.
- **Emails (opcionales) y boletín** (`correo.php` + acciones `email_vincular|email_entrar|email_token|email_quitar|boletin|baja` en `porra.php`): sin contraseñas, enlaces mágicos de un solo uso (30 min) a `/cuenta/?t=…`; email cifrado AES-256-GCM + huella HMAC; casilla 14+ obligatoria y boletín con casilla aparte (se guarda la fecha del consentimiento); entrar por email crea un código extra solo para ese dispositivo (`hx`). Correos con `mail()` desde no-reply@trollacos.com (Reply-To info@trollacos.com, alias que llega al Gmail de Guillermo); en local se apuntan en `api/datos/correos-prueba.log`. Límite: 5/h por conexión, 3/h por email, 150/día. Administrador = cuenta con email cuya huella SHA-256 está en `ADMIN_HUELLAS` (el Gmail de Guillermo): panel en Mi cuenta + todos los capítulos del arcade.
- **Boletín**: noticias propias de GTA VI y videojuegos, novedades de la web, la tienda. Enlaces siempre a trollacos.com (p. ej. /gta-6/que-comprar/), **nunca enlaces de afiliado de Amazon directos en el correo** (lo prohíben las normas de Amazon). Cada envío lleva el enlace de baja `/cuenta/?baja=NOMBRE.TOKEN` (`token_baja()`). Pendiente: herramienta para enviar los boletines.
- Datos en `api/datos/*.php` (protegidos, fuera de git). **Nunca se guardan IPs**, solo un resumen cifrado.
- `api/partidos.json` lo genera `scripts/actualizar_partidos.py` desde **TheSportsDB** (gratis, sin clave; guarda jornadas en `scripts/liga_cache.json`; pocas consultas por el límite).

## La guía de GTA VI (objetivo: la más completa en español)
- Toda noticia nueva de GTA VI entra en la guía: primero en "Últimas novedades" y luego en su sección (personajes, cómo se juega, mapa, música, versiones, FAQ + su JSON-LD).
- Solo datos oficiales o que salgan en al menos dos medios fiables; los rumores, en el recuadro de "Rumores sin confirmar".
- Toque Trollacos: cajas "EL TROLLACO OPINA" (`.nota`) con humor, sin inventar datos.
- **Noticias propias:** cada noticia se redacta con nuestras palabras en `_fuentes/generadores/noticias_gta.json` y se genera con `python3 _fuentes/generadores/noticias_gta.py` → `/gta-6/noticias/<slug>/` (+ portada de noticias y sitemap). Sin enlaces a otras webs (tampoco en portada: el feed RSS externo `scripts/actualizar_noticias.py` está retirado desde el 31 oct): la fuente se cita por su nombre. Cada noticia lleva su "EL TROLLACO OPINA" y un enlace a su sección de la guía; en "Últimas novedades" de la guía, cada punto enlaza a su noticia ("Leer la noticia ›").
- Redes: las publicaciones de noticias mandan a trollacos.com (enlace de la bio), nunca a otras webs. Se dejan como borrador en Metricool para que Guillermo las apruebe.
- Objetivo final: un PDF descargable, "La Guía Trollacos de GTA VI", cuando el juego salga y la guía esté completa.

## Reglas que Guillermo ha fijado
- No manejar nunca sus contraseñas. Los secretos los mete él.
- Publicar en sus redes solo con su OK explícito para cada publicación. Instagram y TikTok (ambos @trollacostv) van por **Metricool** (conector, marca 7708546, zona Europe/Madrid). Antes de programar, mirar `getScheduledPosts` para no duplicar. TikTok exige `tiktokData.title`. Lo que más alcance da: Reels/TikToks verticales (vídeos en `redes/reels/`, hechos con Playwright fotograma a fotograma + ffmpeg + música 8-bit propia en numpy); stories y fotos solo llegan a los seguidores.
- Semana 44 (29 oct – 3 nov) ya programada en Metricool: 6 publicaciones + 6 stories.
- Guillermo quiere llevar todo Trollacos en un único chat.
- Afiliado Amazon: etiqueta `trollacos-21`. No poner enlaces de afiliado en correos, y él no compra con su propio enlace.
- Las fichas **no tienen valor real**: no se compran ni se canjean. Nada de premios ligados a la Porra (ley del juego). Si hay premios, que sean de habilidad en el arcade, con bases legales.
- Merch: sin diseños de Halloween. Diseños finales en `_fuentes/merch/` (`spread2/` prenda oscura, `spread-blanca/` y la espalda "celeste" para prendas claras; máximo 4000 px para Spreadshop). Logo solo "TROLLACOS", sin ".com".
- **Danna** (antes Lucy Lag; Guillermo la renombró el 31 oct): reportera de Trollacos, personaje ficticio y siempre declarado como tal (nunca hacerla pasar por una persona real). Versión pixel antigua (Lucy): unos 30 años, divertida, cascos gamer con micro, gafas retro, pelo morado, chaqueta rosa con acreditación. Sprite y foto de perfil en `_fuentes/lucy/`. Cuenta de Instagram propia de Guillermo.
  Versión realista: Guillermo la ha generado 100 % con IA (no es ninguna persona real). Declarada como IA en la bio ("🤖 Reportera virtual IA") + etiqueta "Información de IA" de Instagram al subir; Guillermo no quiere repetirlo en el texto/vídeo de cada post. Las sube él a mano a su cuenta. Reels en `_fuentes/lucy/reel-presentacion/` (`reel.html` presentación, `noticia.html#n` plantilla «Danna informa»: `node render2.js 'noticia.html#0' 15 carpeta` + `musica.py salida.wav 15 transporte 12.6` + ffmpeg). Firma todas las noticias de la web («Por Danna · Tu reportera del otro lado de la pantalla · ¿Quién es?», que lleva a la nota #danna de /gta-6/noticias/; avatar `img/danna.jpg`); Instagram @dannapixel (`DANNA_IG` en `noticias_gta.py`): enlace en la firma, en la portada y en la tarjeta grande «Esta noticia te la ha contado» al final de cada noticia. Misma cara siempre, nada de logos de marcas reales en la ropa, nada sexual. Habla cercana, gamer, con humor y piques con el Trollaco; sus posts mandan a trollacos.com/gta-6/noticias/.
- Nada de contenido sexual (descartada la chica de la barra). La **Princesa Neón** del arcade tiene preparada una versión en bikini de playa para el gran final (lo pidió Guillermo el 1 nov): pixel, cómica (corona, gafas neón, flotador de pato), sin poses ni nada insinuante.
- **Historia del arcade** (`HISTORIA` en `arcade/index.html`, diálogos al empezar y al acabar cada capítulo; se saltan con SALTAR o Esc): Míster Glitch secuestra a la Princesa Neón en Trolloween → nota «me la llevo al Bar La Verja» → el camarero «¡NO GRITÉIS!» y las bravas sin pagar → Trollaco Club → edificio abandonado (fantasma pide un cargador) → huida por la M-30 (cap. 5: coches y bots se pisan, las motos de la Policía Municipal no) → Glitch se escapa otra vez con la princesa (suspense). **La historia sigue abierta: Guillermo no quiere final todavía; cada capítulo nuevo continúa la trama sin adelantar el desenlace.** El rescate y la fiesta en la «playa» de Madrid Río (`playaFinal`, `princesa()`) están hechos pero sin usar, para el último capítulo.
- **Modo administrador del arcade**: `/arcade/?admin=CÓDIGO` abre todos los capítulos en ese dispositivo (localStorage `trollacoAdmin`), `?admin=off` lo quita. En el código solo está la huella SHA-256; el código se lo di a Guillermo en el chat (no apuntarlo en el repo).
- Modo Halloween de la web: del 15 de octubre al 1 de noviembre a las 23:00 (hora del visitante).
- Antes de publicar algo nuevo: probarlo en local (móvil 390 px y PC) y comprobar el despliegue.

## Pendiente (a 28 oct 2026)
- Cuando Guillermo pase el nombre de su tienda de Spreadshop: crear `/merch/` con la tienda integrada, botón en portada y menú, y story de lanzamiento.
- 19 nov 2026, sale GTA VI: ampliar la guía (misiones, consejos, música completa).
- Imágenes nuevas del tráiler de lanzamiento de GTA VI (arte "Lock and Load", hidroavión) si Guillermo las pasa.
- Si lo pide: subir la Hucha a 10.000 fichas (Ricachón ya está en 100.000).
