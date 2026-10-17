# Trollacos.com

Web retro de Trollacos con noticias de videojuegos y cine que se actualizan solas.

- `index.html` — la web. Las noticias van entre `<!--NOTICIAS:INICIO-->` y `<!--NOTICIAS:FIN-->` (no tocar a mano).
- `fuentes.json` — los medios de los que salen las noticias. Se pueden quitar o añadir.
- `scripts/actualizar_noticias.py` — el programa que lee los RSS y rellena la web.
- `.github/workflows/actualizar-noticias.yml` — lo ejecuta solo a las 07:00 y 19:00 (hora de Madrid).
  Para lanzarlo a mano: pestaña **Actions** → *Actualizar noticias* → **Run workflow**.

Netlify publica la web automáticamente cada vez que cambia algo aquí.
