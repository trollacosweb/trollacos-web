# Trollacos.com — manual del proyecto

Web de Guillermo (marca Trollacos, nacida en 2012 y relanzada en 2026). Humor, videojuegos, GTA VI, arcade, misterio y La Porra.
Estilo **synthwave** (rosa #ff2bd6, cian #1ff2ff, amarillo #ffd23f, fondo #07021a) con la mascota pixel art **el Trollaco**.
Hablar con Guillermo en **español de España**, con humor y trato directo y honesto.

## Cómo funciona
- Repositorio: `trollacosweb/trollacos-web` (GitHub). Web estática + algo de PHP en `api/`.
- Hosting: DonDominio (PHP), dominio trollacos.com con SSL de pago. FTP: `ftp.trollacos.com`.
- **Despliegue automático:** `.github/workflows/actualizar-noticias.yml` se lanza en cada push a `main`, por cron y a mano (`workflow_dispatch`):
  noticias → partidos de LaLiga → commit → subida por FTPS (con reintento) → aviso IndexNow → comprobación de los rankings (sale como `::notice::`).
  Para ver resultados: anotaciones del run (`gh api repos/trollacosweb/trollacos-web/check-runs/<job>/annotations`).
- Secretos de GitHub (los pone Guillermo, **nunca** pegarlos en el chat): `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`, `FOOTBALL_DATA_KEY` (ya no hace falta).
- Excluidos del FTP: `.github/`, `scripts/`, `_fuentes/`, `CLAUDE.md`, `api/datos/`, `node_modules`.

## Secciones
| Ruta | Qué es | Se genera con |
|---|---|---|
| `/` | Portada (noticias automáticas, tienda Amazon, banners) | a mano + `scripts/actualizar_noticias.py` |
| `/gta-6/` | Guía GTA VI (mapa, novedades, tráilers, FAQ) | a mano |
| `/gta-6/musica/` | Música con enlaces a Spotify | `_fuentes/generadores/musica.py` |
| `/gta-6/que-comprar/` | Guía de compra (afiliados Amazon) | `_fuentes/generadores/compra.py` |
| `/arcade/` | Trollaco Run: Modo historia (4 capítulos) + "Supera el récord" | a mano (canvas JS) |
| `/porra/` | La Porra Trollaca (pronósticos LaLiga con fichas, sin dinero) | `_fuentes/generadores/porra.py` |
| `/cuenta/` | Mi cuenta: estadísticas, insignias | `_fuentes/generadores/cuenta.py` |
| `/misterio/` (+ `espana/`, `mundo/`) | Expediente Trollaco, mapas Leaflet | `_fuentes/generadores/misterio/generar.py` |
| `/redes/` | Imágenes y textos para Instagram (no indexado) | `_fuentes/generadores/redes.py` |

Los generadores tienen rutas fijas: copiar `_fuentes/generadores/` a `/home/claude/trollaco/` y el repo en `/home/claude/trollacos-web/`.
Capturas y renders con Playwright: `chromium.launch({executablePath:'/opt/pw-browsers/chromium'})`. Probar PHP en local con `php -S 127.0.0.1:8099 -t .`.

## API (PHP, en `api/`)
- `comun.php`: cabeceras, secreto HMAC autogenerado, filtro de nombres (2-5 caracteres, una palabra, lista de palabras prohibidas + `bloqueados.php`), fichas de partida firmadas.
- `arcade_lib.php`: modos `run, c1..c4`, `TEMPORADA` (cambiarla borra rankings), jugadores de relleno (solo en "run", nunca echan a reales; JAM85 debe seguir 1º), `marca_jugador()`.
- `marcadores.php?accion=lista|empezar|enviar&modo=…`: rankings del arcade (una marca por nombre).
- `porra.php?accion=partidos|ranking|registrar|yo|perfil|arcade|apostar|cancelar`: cuentas (nombre + código de 8), fichas, pronósticos 1X2 y exacto (x8), bono 10 por alta y 10 por jornada, liquidación automática, cancelar hasta 5 min antes.
- Datos en `api/datos/*.php` (protegidos, fuera de git). **Nunca se guardan IPs**, solo un resumen cifrado.
- `api/partidos.json` lo genera `scripts/actualizar_partidos.py` desde **TheSportsDB** (gratis, sin clave; guarda jornadas en `scripts/liga_cache.json`; pocas consultas por el límite).

## La guía de GTA VI (objetivo: la más completa en español)
- Toda noticia nueva de GTA VI entra en la guía: primero en "Últimas novedades" y luego en su sección (personajes, cómo se juega, mapa, música, versiones, FAQ + su JSON-LD).
- Solo datos oficiales o que salgan en al menos dos medios fiables; los rumores, en el recuadro de "Rumores sin confirmar".
- Toque Trollacos: cajas "EL TROLLACO OPINA" (`.nota`) con humor, sin inventar datos.
- **Noticias propias:** cada noticia se redacta con nuestras palabras en `_fuentes/generadores/noticias_gta.json` y se genera con `python3 _fuentes/generadores/noticias_gta.py` → `/gta-6/noticias/<slug>/` (+ portada de noticias y sitemap). Sin enlaces a otras webs: la fuente se cita por su nombre. Cada noticia lleva su "EL TROLLACO OPINA" y un enlace a su sección de la guía; en "Últimas novedades" de la guía, cada punto enlaza a su noticia ("Leer la noticia ›").
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
- Nada de contenido sexual (descartadas la chica de la barra y la del bikini del arcade).
- Antes de publicar algo nuevo: probarlo en local (móvil 390 px y PC) y comprobar el despliegue.

## Pendiente (a 28 oct 2026)
- Cuando Guillermo pase el nombre de su tienda de Spreadshop: crear `/merch/` con la tienda integrada, botón en portada y menú, y story de lanzamiento.
- 19 nov 2026, sale GTA VI: ampliar la guía (misiones, consejos, música completa).
- Arcade: "el gran final" tras el capítulo 4 (fiesta en la playa synthwave o la Trollaca ochentera, a elegir por Guillermo).
- Imágenes nuevas del tráiler de lanzamiento de GTA VI (arte "Lock and Load", hidroavión) si Guillermo las pasa.
- Si lo pide: subir la Hucha a 10.000 fichas (Ricachón ya está en 100.000).
