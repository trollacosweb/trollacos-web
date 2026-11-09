"""Sección de Cine de Héctor «El Caimán» Varga: /cine/, /cine/<sección>/, /cine/<slug>/ y la ficha /cine/hector-varga/.
Críticas en _fuentes/generadores/cine.json. También pone el bloque de portada (<!--CINE:INICIO--> … <!--CINE:FIN-->) y el sitemap.
Uso: python3 _fuentes/generadores/cine.py"""
import os, re, json, html
RAIZ = os.environ.get('TROLLACOS_RAIZ', '/home/claude/trollacos-web'); os.chdir(RAIZ)
CR = json.load(open('_fuentes/generadores/cine.json', encoding='utf-8'))
CR.sort(key=lambda c: c['fecha'], reverse=True)
SEC = {
    'hechos': ('basado-en-hechos-muy-sueltos', 'Basado en hechos muy sueltos', '🕵️',
               'Películas que juran que «esto pasó de verdad». El Caimán coge la lupa y separa lo que ocurrió de lo que se inventó el guionista.'),
    'road': ('road-movies-y-cine-de-culto', 'Road movies y cine de culto', '🛣️',
             'Carreteras, huidas y joyas que fracasaron en su día y hoy se veneran. Gasolina, polvo y sesiones dobles.'),
    'genero': ('cine-de-genero-y-serie-b', 'Cine de género y serie B', '🧟',
               'Terror, ciencia ficción y películas hechas con cuatro duros que le dan sopas con honda a muchas superproducciones.'),
    'espanol': ('cine-espanol-y-culto-nacional', 'Cine español y culto nacional', '🥘',
                'De Delibes a las Torres KIO: las películas españolas que se citan en la barra del bar y que no han caducado (o sí, y el Caimán te lo dice).'),
    'clasicos': ('clasicos-y-maestros-del-septimo-arte', 'Clásicos y maestros del séptimo arte', '🏛️',
                 'Coppola, Scorsese, Kubrick, Leone, Wenders… Las películas de las que todo el mundo habla. El Caimán comprueba si se las merecen.'),
    'scifi': ('ciencia-ficcion-y-mundos-distopicos', 'Ciencia ficción y mundos distópicos', '🚀',
              'Replicantes, monolitos, agujeros negros y futuros que no apetece vivir. Ciencia ficción de la buena y alguna que vende humo.'),
    'drama': ('drama-supervivencia-e-identidad', 'Drama, supervivencia e identidad', '🧭',
              'Gente que se pierde, que se escapa, que naufraga o que baila contra todo. Historias para salir del cine con un nudo en la garganta.'),
    'culto': ('cine-de-genero-culto-e-influencia-moderna', 'Cine de género, culto e influencia moderna', '🔪',
              'Tarantino, los Coen, Fincher, Spielberg y compañía: las películas que copió todo el mundo después. Unas aguantan; otras, no tanto.'),
    'series': ('ficcion-televisiva', 'Ficción televisiva', '📺',
               'El Caimán despreciaba la tele hasta que llegaron ciertas series. Aquí reconoce sus errores. Con café solo.'),
}
MESES = 'enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre'.split()
def ftxt(f): return f'{int(f[8:10])} de {MESES[int(f[5:7]) - 1]} de {f[:4]}'
def esc(t): return html.escape(t, quote=True)
def caimanes(n): return '🐊' * n + f'<span class="off">{"🐊" * (5 - n)}</span>'
def url(c): return f'/cine/{c["slug"]}/'
def serie(c): return c.get('tipo') == 'serie'

g = open('gta-6/index.html', encoding='utf-8').read()
style = g[g.find('<style>'):g.find('</style>') + 8]
foot = g[g.find('<footer>'):g.find('</footer>') + 9]
extra = '''.cn{max-width:860px;margin:0 auto;padding:0 16px}
.cn .k{font-family:'VT323',monospace;font-size:22px;color:#ffb347}
.cn h1{margin:6px 0 8px;text-shadow:0 0 16px rgba(255,179,71,.6)}
.cn p,.cn li{font-size:19px;line-height:1.65}
.cn h2{margin-top:32px}.cn h3{font-family:'Righteous',sans-serif;font-weight:400;font-size:24px;color:#ffb347;margin:30px 0 8px}
.cn a{color:#ffb347}
.foto-h{margin:18px 0;border:3px solid #ffb347;border-radius:14px;overflow:hidden;box-shadow:0 0 28px rgba(255,179,71,.35)}
.foto-h img{display:block;width:100%;height:auto}
.firma-h{display:flex;gap:12px;align-items:center;margin:12px 0 18px;font-size:16px;color:#e8dcc8}
.firma-h img{width:56px;height:56px;border-radius:50%;border:2px solid #ffb347;object-fit:cover;flex:none}
.firma-h b{display:block;color:#fff;font-size:17px}
.ficha-p{margin:18px 0;padding:16px 18px;border:2px solid #ffb347;border-radius:14px;background:linear-gradient(135deg,rgba(255,179,71,.12),rgba(7,2,26,.8));display:grid;grid-template-columns:1fr auto;gap:10px 18px;align-items:center}
.ficha-p dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:4px 12px;font-size:16px}
.ficha-p dt{font-family:'VT323',monospace;font-size:18px;color:#ffb347}.ficha-p dd{margin:0;color:#f3ead9}
.nota-c{text-align:center;font-family:'VT323',monospace;font-size:18px;color:#ffb347}
.nota-c span{display:block;font-size:30px;letter-spacing:2px}.off{opacity:.2}
.veredicto{margin:26px 0;padding:16px 18px;border-left:5px solid #ffb347;background:rgba(255,179,71,.08);border-radius:0 12px 12px 0;font-size:19px}
.veredicto b{display:block;font-family:'VT323',monospace;font-weight:400;font-size:22px;color:#ffb347}
.nota{display:flex;gap:14px;align-items:flex-start;margin:22px 0;padding:14px 16px;border:2px dashed var(--yellow);border-radius:12px;background:rgba(255,210,63,.07)}
.nota img{width:44px;image-rendering:pixelated;flex:none}.nota p{margin:0;font-size:17px}.nota b{color:var(--yellow)}
.fuentes{font-size:15px;color:#bdb3d9}.fuentes li{font-size:15px;line-height:1.5}
.autor-h{display:flex;gap:16px;align-items:center;margin:30px 0;padding:18px;border:2px solid #ffb347;border-radius:16px;background:rgba(255,179,71,.07)}
.autor-h img{width:96px;height:96px;border-radius:50%;border:3px solid #ffb347;object-fit:cover;flex:none}
.autor-h span{font-family:'VT323',monospace;font-size:18px;color:#ffb347}.autor-h b{display:block;font-family:'Righteous',sans-serif;font-weight:400;font-size:24px;color:#fff}
.autor-h p{margin:4px 0 0;font-size:16px}
.lista-c{display:grid;gap:14px;margin:14px 0}
.tarj-c{display:block;padding:16px 18px;border:1px solid rgba(255,179,71,.55);border-radius:14px;text-decoration:none;color:#fff;background:rgba(255,179,71,.05)}
.tarj-c:hover{border-color:#ffb347;box-shadow:0 0 16px rgba(255,179,71,.35)}
.tarj-c small{display:block;font-family:'VT323',monospace;font-size:18px;color:#ffb347}
.tarj-c b{display:block;font-family:'Righteous',sans-serif;font-weight:400;font-size:22px;line-height:1.2;margin:4px 0}
.tarj-c em{display:block;font-style:normal;font-size:16px;color:#d9d0c0}
.tarj-c .cm{font-size:18px}
.secs{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:16px 0}
.sec-c{display:block;padding:16px;border:2px solid rgba(255,179,71,.5);border-radius:14px;text-decoration:none;color:#fff;background:rgba(255,179,71,.06)}
.sec-c:hover{border-color:#ffb347}.sec-c i{font-style:normal;font-size:30px}.sec-c b{display:block;font-family:'Righteous',sans-serif;font-weight:400;font-size:20px;margin:4px 0}
.sec-c span{font-size:15px;color:#d9d0c0}
.ficha-d{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px 16px;list-style:none;padding:14px 16px;margin:16px 0;border:2px dashed #ffb347;border-radius:12px;background:rgba(255,179,71,.06)}
.ficha-d li{font-size:17px}.ficha-d b{display:block;font-family:'VT323',monospace;font-weight:400;font-size:19px;color:#ffb347}
.ficha-p.con-cartel{grid-template-columns:150px 1fr auto}
.cartel-p{margin:0}.cartel-p img{display:block;width:150px;height:auto;border-radius:8px;border:2px solid #ffb347;box-shadow:0 0 18px rgba(255,179,71,.3)}
.cartel-p figcaption{font-size:11px;color:#9b91b8;margin-top:4px;line-height:1.3}
.tarj-c.con-cartel{display:grid;grid-template-columns:72px 1fr;gap:14px;align-items:start}
.tarj-c.con-cartel img{width:72px;height:auto;border-radius:6px;border:1px solid rgba(255,179,71,.6)}
.secs-mas{text-align:center;margin:10px 0 0}
.migas{font-family:'VT323',monospace;font-size:18px;color:#bdb3d9}.migas a{color:#bdb3d9}
@media(max-width:760px){.secs{grid-template-columns:1fr}.ficha-p,.ficha-p.con-cartel{grid-template-columns:1fr}.cartel-p{display:flex;gap:12px;align-items:flex-end}.cartel-p img{width:120px}.cn p,.cn li{font-size:18px}.autor-h{flex-direction:column;text-align:center}}
</style>'''
style2 = style.replace('</style>', extra)

def pagina(titulo, desc, u, cuerpo, jsonld=None, og='https://trollacos.com/img/hector-despacho.webp', volver=('/cine/', '‹ CINE')):
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ''
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)} | Trollacos</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="https://trollacos.com{u}">
<meta property="og:title" content="{esc(titulo)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/icono.png">
{style2}
{ld}
</head><body>
<div class="scan"></div>
<nav class="top"><a href="/"><img class="px" src="/logo.webp" alt="Trollacos" width="1600" height="161"></a><a href="{volver[0]}">{volver[1]}</a></nav>
<main class="cn">
{cuerpo}
</main>
{foot}
</body></html>'''

def guarda(ruta, txt):
    os.makedirs(ruta, exist_ok=True)
    open(os.path.join(ruta, 'index.html'), 'w', encoding='utf-8').write(txt)

FIRMA = ('<div class="firma-h"><img src="/img/hector.jpg" alt="Héctor Varga" width="56" height="56"><div>'
         '<b>Por Héctor «El Caimán» Varga</b>Crítico de cine · Muerde, pero con razón · <a href="/cine/hector-varga/">¿Quién es?</a></div></div>')
AUTOR = ('<div class="autor-h"><img src="/img/hector.jpg" alt="Héctor Varga" width="96" height="96"><div><span>&gt; ESTA CRÍTICA LA HA FIRMADO_</span>'
         '<b>Héctor «El Caimán» Varga</b><p>Cuarenta años en butacas que crujen. No se casa con nadie, no regala estrellas y no ha visto un tráiler entero desde 1994.</p>'
         '<p><a href="/cine/hector-varga/">Conoce al Caimán ›</a></p></div></div>')

def tarjeta(c):
    s = SEC[c['seccion']]
    txt = (f'<small>{s[2]} {s[1].upper()} · {c["anio"]}</small><b>{esc(c["titulo"])}</b>'
           f'<span class="cm">{caimanes(c["nota"])}</span><em>{esc(c["resumen"])}</em>')
    if c.get('cartel'):
        return (f'<a class="tarj-c con-cartel" href="{url(c)}"><img src="{c["cartel"]}" alt="Cartel de {esc(c["pelicula"])}" '
                f'width="72" height="108" loading="lazy"><span>{txt}</span></a>')
    return f'<a class="tarj-c" href="{url(c)}">{txt}</a>'

# críticas
sm_urls = ['/cine/', '/cine/hector-varga/']
for c in CR:
    s = SEC[c['seccion']]
    fuentes = ''.join(f'<li>{esc(f)}</li>' for f in c['fuentes'])
    palabras = len(re.sub(r'<[^>]+>', ' ', c['cuerpo']).split())
    cartel = (f'<figure class="cartel-p"><img src="{c["cartel"]}" alt="Cartel de {esc(c["pelicula"])}" width="150" height="225">'
              f'<figcaption>Cartel © sus titulares. Imagen vía TMDB.</figcaption></figure>') if c.get('cartel') else ''
    otras = [o for o in CR if o is not c and o['seccion'] == c['seccion']][:6]
    if len(otras) < 4: otras += [o for o in CR if o is not c and o not in otras][:6 - len(otras)]
    cuerpo = f'''<p class="migas"><a href="/cine/">Cine</a> › <a href="/cine/{s[0]}/">{s[1]}</a></p>
<p class="k">&gt; {s[2]} {s[1].upper()}_</p>
<h1>{esc(c['titulo'])}</h1>
{FIRMA.replace('</div></div>', f' · {ftxt(c["fecha"])} · {max(1, round(palabras / 220))} min de lectura</div></div>')}
<div class="ficha-p{' con-cartel' if c.get('cartel') else ''}">{cartel}<dl><dt>{'SERIE' if serie(c) else 'PELÍCULA'}</dt><dd>{esc(c['pelicula'])} ({c['anio']})</dd><dt>ORIGINAL</dt><dd>{esc(c['original'])}</dd>
<dt>{'CREADOR' if serie(c) else 'DIRECCIÓN'}</dt><dd>{esc(c['direccion'])}</dd><dt>REPARTO</dt><dd>{esc(c['reparto'])}</dd></dl>
<div class="nota-c"><span>{caimanes(c['nota'])}</span>NOTA DEL CAIMÁN: {c['nota']}/5</div></div>
{c['cuerpo']}
<div class="veredicto"><b>🐊 EN UNA LÍNEA:</b>{esc(c['veredicto'])}</div>
<div class="nota"><img src="/img/trollaco.png" alt=""><p><b>EL TROLLACO OPINA:</b> {esc(c['trollaco'])}</p></div>
<p class="fuentes"><b>Fuentes de los datos</b> (la opinión es solo del Caimán):</p><ul class="fuentes">{fuentes}</ul>
{AUTOR}
<h2>Más del Caimán</h2><div class="lista-c">{''.join(tarjeta(o) for o in otras)}</div>
<p class="secs-mas"><a class="btn alt" href="/cine/{s[0]}/" style="border-color:#ffb347;color:#ffb347">{s[2]} TODA LA SECCIÓN «{s[1].upper()}»</a></p>'''
    ld = {'@context': 'https://schema.org', '@type': 'Review', 'name': c['titulo'], 'datePublished': c['fecha'],
          'author': {'@type': 'Person', 'name': 'Héctor Varga', 'url': 'https://trollacos.com/cine/hector-varga/'},
          'publisher': {'@type': 'Organization', 'name': 'Trollacos'},
          'itemReviewed': ({'@type': 'TVSeries', 'name': c['pelicula'], 'startDate': str(c['anio'])[:4], 'creator': {'@type': 'Person', 'name': c['direccion']}}
                           if serie(c) else
                           {'@type': 'Movie', 'name': c['pelicula'], 'dateCreated': str(c['anio']), 'director': {'@type': 'Person', 'name': c['direccion'].split(' (')[0]}}),
          'reviewRating': {'@type': 'Rating', 'ratingValue': c['nota'], 'bestRating': 5, 'worstRating': 1},
          'reviewBody': c['resumen']}
    if c.get('cartel'): ld['itemReviewed']['image'] = 'https://trollacos.com' + c['cartel']
    guarda(f'cine/{c["slug"]}', pagina(c['titulo'], c['resumen'], url(c), cuerpo, ld))
    sm_urls.append(url(c))

# secciones
for k, (slug, nombre, ico, desc) in SEC.items():
    L = [c for c in CR if c['seccion'] == k]
    lista = ''.join(tarjeta(c) for c in L) or '<p>El Caimán está viendo películas para esta sección. Dale tiempo, que es mayor.</p>'
    cuerpo = f'''<p class="migas"><a href="/cine/">Cine</a> › {nombre}</p>
<p class="k">&gt; {ico} SECCIÓN_</p><h1>{nombre}</h1><p>{desc}</p>{FIRMA}
<div class="lista-c">{lista}</div>'''
    guarda(f'cine/{slug}', pagina(f'{nombre}: críticas de cine', desc, f'/cine/{slug}/', cuerpo))
    sm_urls.append(f'/cine/{slug}/')

# portada de cine
secs = ''.join(f'<a class="sec-c" href="/cine/{s[0]}/"><i>{s[2]}</i><b>{s[1]}</b><span>{s[3]}</span></a>' for s in SEC.values())
cuerpo = f'''<p class="k">&gt; EL TROLLACO CINEMA_</p>
<h1>Cine: las críticas del Caimán</h1>
<p>Aquí no se hacen notas de prensa ni se aplaude porque sí. <strong>Héctor «El Caimán» Varga</strong> ve la película, se toma un café solo y te dice lo que piensa. Si es buena, lo dirá. Si es mala, también, y con más gracia.</p>
<figure class="foto-h"><img src="/img/hector-despacho.webp" alt="Héctor Varga en su despacho de El Trollaco Cinema" width="1366" height="616"></figure>
{FIRMA}
<h2>Las secciones</h2><div class="secs">{secs}</div>
<h2>Últimas críticas</h2><div class="lista-c">{''.join(tarjeta(c) for c in CR[:12])}</div>
<p class="secs-mas">Hay {len(CR)} críticas en total: el resto, en cada sección de arriba.</p>
<div class="nota"><img src="/img/trollaco.png" alt=""><p><b>EL TROLLACO OPINA:</b> Le he pedido que reseñe Trollaco Run. Me ha puesto un caimán. Uno. Dice que «por la música». Estoy estudiando denunciarle.</p></div>'''
guarda('cine', pagina('Cine: críticas sin anestesia de Héctor «El Caimán» Varga', 'Críticas de cine con colmillo: cine español, clásicos, ciencia ficción, drama, cine de culto, road movies, serie B y series. Por Héctor «El Caimán» Varga.', '/cine/', cuerpo, volver=('/', '‹ PORTADA')))

# ficha de Héctor
cuerpo = f'''<p class="k">&gt; FICHA DE LA REDACCIÓN_</p>
<h1>Héctor «El Caimán» Varga</h1>
<p class="k" style="color:var(--yellow)">Crítico de cine · Muerde, pero con razón</p>
<figure class="foto-h"><img src="/img/hector-despacho.webp" alt="Héctor Varga en su despacho" width="1366" height="616"></figure>
<p>Héctor Varga lleva más de cuarenta años sentado en la oscuridad, viendo películas que a veces merecían la pena y muchas veces no. Le llaman <strong>«El Caimán»</strong> porque se queda quieto, en silencio, con cara de no estar enterándose de nada… y cuando abre la boca, muerde. No hay estreno, director de moda ni saga millonaria que se libre.</p>
<p>Escribe a máquina (dice que el ordenador «no tiene alma, y además se cuelga»), apunta todo en un cuaderno que pone «CRÍTICAS – HÉCTOR V.» y no ha visto un tráiler entero desde 1994, porque «te cuentan la película y encima te la cuentan mal».</p>
<ul class="ficha-d">
  <li><b>📍 Base de operaciones</b>El Trollaco Cinema: un despacho con proyector, carretes y un cenicero que ya solo guarda clips</li>
  <li><b>☕ Combustible</b>Café solo. Sin azúcar. Como sus críticas</li>
  <li><b>🎬 Le encanta</b>Las carreteras vacías, el cine negro y las películas hechas con cuatro duros y mucho talento</li>
  <li><b>😤 No soporta</b>Las secuelas de secuelas, los finales que explican el final y la gente que mira el móvil en el cine</li>
</ul>
<h2>Qué cubre</h2>
<div class="secs">{secs}</div>
<h2>Cómo puntúa</h2>
<p>Con caimanes, del uno al cinco. <strong>🐊</strong> es «no la veas ni gratis». <strong>🐊🐊🐊🐊🐊</strong> es «deja lo que estés haciendo». Regala muy pocos cinco y no le tiembla el pulso para poner un uno a una película que ha costado doscientos millones. Ha dicho más de una vez que un caimán es «una cortesía».</p>
<h2>Sus reglas</h2>
<p>Critica películas, no personas. Separa siempre los datos (que van con su fuente) de la opinión (que es solo suya). Y nunca destripa el final sin avisar. «El que destripa un final sin avisar», dice, «no merece entrar en una sala de cine. Ni en un ascensor».</p>
<div class="nota"><img src="/img/trollaco.png" alt=""><p><b>EL TROLLACO OPINA:</b> Le dejé un bocadillo de chorizo en la mesa y le dio dos caimanes. Al bocadillo. «Previsible», dijo.</p></div>
<h2>Sus últimas críticas</h2><div class="lista-c">{''.join(tarjeta(c) for c in CR[:6])}</div>'''
guarda('cine/hector-varga', pagina('Héctor «El Caimán» Varga, crítico de cine de Trollacos', 'Quién es Héctor «El Caimán» Varga, el crítico de cine de Trollacos: cine de culto, road movies, serie B y películas basadas en hechos muy sueltos.', '/cine/hector-varga/', cuerpo))

# portada de la web
tarjs = ''.join(f'<a class="arsenal-card" href="{url(c)}"><span class="ico-a">{SEC[c["seccion"]][2]}</span><h3>{esc(c["pelicula"])} ({c["anio"]})</h3>'
                f'<p>{esc(c["resumen"])}</p><span class="ver">{"🐊" * c["nota"]} · LEER ›</span></a>' for c in CR[:4])
bloque = f'''<!--CINE:INICIO-->
<section class="block arsenal" id="cine">
  <h2>Cine</h2>
  <p class="small" style="margin:-14px 0 18px">Críticas sin anestesia. Las firma <a href="/cine/hector-varga/" style="color:#ffb347">Héctor «El Caimán» Varga</a>.</p>
  <a class="cine-cab" href="/cine/"><img src="/img/hector.jpg" alt="Héctor Varga" width="72" height="72"><span><b>«Si es buena, te lo digo. Si es mala, también, y con más gracia.»</b><small>EL TROLLACO CINEMA · HÉCTOR «EL CAIMÁN» VARGA</small></span></a>
  <div class="arsenal-grid">{tarjs}</div>
  <p style="text-align:center;margin-top:16px"><a class="btn alt" href="/cine/" style="border-color:#ffb347;color:#ffb347">🎬 TODO EL CINE</a></p>
</section>
<style>.cine-cab{{display:flex;gap:14px;align-items:center;max-width:760px;margin:0 auto 18px;padding:12px 16px;border:2px solid #ffb347;border-radius:14px;text-decoration:none;background:rgba(255,179,71,.08)}}
.cine-cab img{{width:72px;height:72px;border-radius:50%;border:2px solid #ffb347;object-fit:cover;flex:none}}.cine-cab b{{display:block;color:#fff;font-size:17px}}.cine-cab small{{font-family:'VT323',monospace;font-size:17px;color:#ffb347}}</style>
<!--CINE:FIN-->'''
ix = open('index.html', encoding='utf-8').read()
if '<!--CINE:INICIO-->' in ix:
    ix = re.sub(r'<!--CINE:INICIO-->.*?<!--CINE:FIN-->', lambda m: bloque, ix, flags=re.S)
else:
    i = ix.find('<!--TEC:FIN-->'); j = ix.find('</section>', i) + len('</section>')
    ix = ix[:j] + '\n\n' + bloque + ix[j:]
open('index.html', 'w', encoding='utf-8').write(ix)

sm = open('sitemap.xml', encoding='utf-8').read()
nuevas = ''.join(f'  <url><loc>https://trollacos.com{u}</loc><changefreq>weekly</changefreq></url>\n' for u in sm_urls if f'https://trollacos.com{u}<' not in sm)
if nuevas: open('sitemap.xml', 'w', encoding='utf-8').write(sm.replace('</urlset>', nuevas + '</urlset>'))
print(f'cine: {len(CR)} críticas, {len(SEC)} secciones, ficha de Héctor y portada')
