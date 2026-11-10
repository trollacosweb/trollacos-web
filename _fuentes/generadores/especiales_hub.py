# Portada /especiales/ con todos los especiales. Se ejecuta (exec) al final de cada generador de especiales:
# usa pagina() y esc() del script que lo llama. Para añadir un especial: añadirlo a ESPECIALES (el más nuevo primero).
import os as _os
ESPECIALES = [
    ('/especiales/aventuras-graficas/', '🖱️', 'De Monkey Island a Runaway: la historia de las aventuras gráficas',
     '28 aventuras gráficas, de Mystery House y King\'s Quest a Monkey Island, Grim Fandango, Broken Sword, Hollywood Monsters y Runaway. Con Dinamic, Pendulo y la aventura española.'),
    ('/especiales/juegos-de-futbol/', '⚽', 'De ISS a EA Sports FC: la historia de los juegos de fútbol',
     'Más de 25 juegos de fútbol, de Emilio Butragueño Fútbol y Kick Off a PES 6, PC Fútbol, Oliver y Benji, FIFA, Football Manager, eFootball y EA FC.'),
]
_ESP = [e for e in ESPECIALES if _os.path.exists(e[0].strip('/') + '/index.html')]
_tarjetas = ''.join(f'''<section class="ficha-j"><div class="cab"><div class="port" aria-hidden="true">{i}</div><div><span class="sub">&gt; {'NUEVO' if n == 0 else 'ESPECIAL'}_</span><h2><a href="{u}" style="color:#fff">{esc(t)}</a></h2>
<p style="margin:6px 0 0;font-size:17px">{esc(d)}</p><p style="margin:12px 0 0"><a class="btn" href="{u}">LEER EL ESPECIAL</a></p></div></div></section>''' for n, (u, i, t, d) in enumerate(_ESP))
_hub = f'''<p class="migas"><a href="/">Portada</a> › Especiales</p>
<div class="hero-f"><p class="k">&gt; ESPECIALES TROLLACOS_</p><h1>Especiales</h1><p>Contenido largo, nostálgico y con datos: para leer con calma y con el mando cerca.</p></div>
{_tarjetas}'''
_os.makedirs('especiales', exist_ok=True)
open('especiales/index.html', 'w', encoding='utf-8').write(pagina('Especiales de Trollacos', 'Especiales largos y nostálgicos de Trollacos sobre videojuegos: juegos de fútbol, aventuras gráficas y más.', '/especiales/', _hub))
_sm = open('sitemap.xml', encoding='utf-8').read()
_nuevas = ''.join(f'  <url><loc>https://trollacos.com{u}</loc><changefreq>monthly</changefreq></url>\n' for u in ['/especiales/'] + [e[0] for e in _ESP] if f'https://trollacos.com{u}<' not in _sm)
if _nuevas: open('sitemap.xml', 'w', encoding='utf-8').write(_sm.replace('</urlset>', _nuevas + '</urlset>'))
