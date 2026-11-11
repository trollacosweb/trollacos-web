"""Páginas propias de cada caso: /misterio/<id>/ con el expediente completo.
Usa el CSS de /misterio/index.html (generado antes por generar.py) y el texto largo de casos_largos.py.
Uso: python3 expedientes.py   (lo llama generar.py al final)"""
import os, re, sys, json, html
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import casos as C
from casos_largos import L
RAIZ = '/home/claude/trollacos-web'
base = open(f'{RAIZ}/misterio/index.html', encoding='utf-8').read()
style = base[base.find('<style>'):base.find('</style>') + 8]
foot = base[base.find('<footer>'):base.find('</footer>') + 9]
REG = [('Madrid', '/misterio/', C.CASOS + C.SIERRA), ('España', '/misterio/espana/', C.ESPANA), ('Latinoamérica', '/misterio/latinoamerica/', C.LATAM), ('El mundo', '/misterio/mundo/', C.MUNDO)]
todos = [(c, r, u) for r, u, Ls in REG for c in Ls]

extra = '''
.exp{max-width:820px;margin:0 auto;padding:0 16px}
.exp .caso{margin-top:24px}
.exp h1{font-family:'Righteous',sans-serif;font-weight:400;font-size:clamp(32px,6vw,52px);line-height:1.08;color:#eafff3;text-shadow:0 0 18px rgba(124,255,178,.5);margin:12px 0 6px}
.exp h2{font-family:'Righteous',sans-serif;font-weight:400;font-size:clamp(23px,4vw,30px);color:var(--verde);margin:34px 0 10px;text-shadow:0 0 10px rgba(124,255,178,.4)}
.exp .relato p,.exp .sec p{font-size:19px;line-height:1.65}
.exp .sec p{margin:0 0 16px}.exp .sec strong{color:#fff}
.lect{font-family:'VT323',monospace;font-size:20px;color:var(--muted);margin:0 0 10px}
.crono{list-style:none;margin:10px 0 0;padding:0;border-left:3px solid var(--verde)}
.crono li{position:relative;padding:4px 0 12px 22px;font-size:17.5px}
.crono li::before{content:'';position:absolute;left:-9px;top:10px;width:14px;height:14px;border-radius:50%;background:#07021a;border:3px solid var(--verde)}
.crono b{display:block;font-family:'VT323',monospace;font-weight:400;font-size:21px;color:var(--verde)}
.flipa{margin:12px 0 0;padding:16px 18px 6px;border:2px solid #ffd23f;border-radius:12px;background:rgba(255,210,63,.07)}
.flipa ul{margin:0;padding-left:20px}.flipa li{margin:0 0 10px;font-size:18px}.flipa strong{color:#ffd23f}
.visita{padding:14px 16px;border-left:4px solid var(--verde);background:rgba(124,255,178,.06);border-radius:6px}
.visita p{margin:0;font-size:18px}
.fuentes{font-size:15px;color:var(--muted);margin-top:22px}
.comp a{display:inline-block;margin:4px 8px 4px 0;padding:7px 14px;border:1px solid var(--verde);border-radius:6px;color:#eafff3;text-decoration:none}
.navexp{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:30px 0 10px}
.navexp a{display:block;padding:12px 14px;border:1px solid rgba(124,255,178,.45);border-radius:10px;text-decoration:none;color:#eafff3;background:rgba(124,255,178,.04)}
.navexp a:hover{border-color:var(--verde)}.navexp small{display:block;font-family:'VT323',monospace;font-size:18px;color:var(--verde)}
.navexp a.sig{text-align:right}
.migas{font-family:'VT323',monospace;font-size:19px;margin:18px 0 0}.migas a{color:var(--verde)}
@media(max-width:560px){.navexp{grid-template-columns:1fr}.navexp a.sig{text-align:left}}
.tucaso{display:flex;gap:16px;align-items:center;margin:0 0 28px;padding:16px 18px;border:3px dashed #ffd23f;border-radius:16px;background:rgba(255,210,63,.07);text-decoration:none;color:#fff}
.tucaso:hover{background:rgba(255,210,63,.14)}.tucaso>span{font-size:44px;flex:none}
.tucaso small{font-family:'VT323',monospace;font-size:19px;color:#ffd23f}.tucaso b{display:block;font-family:'Righteous',sans-serif;font-weight:400;font-size:25px}
.tucaso p{margin:4px 0 0;font-size:16px;color:#e9e3c4}
.form-caso{display:grid;gap:14px;margin:18px 0}.form-caso label{display:grid;gap:6px;font-size:17px;font-weight:700}
.form-caso label span{font-weight:400;font-size:15px;color:var(--muted)}
.form-caso input[type=text],.form-caso input[type=email],.form-caso textarea{width:100%;box-sizing:border-box;padding:12px 14px;border:2px solid rgba(124,255,178,.5);border-radius:10px;background:#0b0430;color:#fff;font:inherit;font-size:17px}
.form-caso textarea{min-height:220px;resize:vertical}.form-caso input:focus,.form-caso textarea:focus{outline:none;border-color:var(--verde);box-shadow:0 0 12px rgba(124,255,178,.4)}
.form-caso .dos{display:grid;grid-template-columns:2fr 1fr;gap:14px}
.form-caso .chk{display:flex;gap:10px;align-items:flex-start;font-weight:400;font-size:16px}.form-caso .chk input{width:22px;height:22px;flex:none;margin-top:2px}
.form-caso .trampa{position:absolute;left:-9999px}
.form-caso button{justify-self:start;cursor:pointer;padding:14px 26px;border:0;border-radius:12px;background:linear-gradient(90deg,#7cffb2,#1ff2ff);color:#07021a;font-weight:700;font-size:20px;font-family:inherit}
.form-caso button:disabled{opacity:.6;cursor:wait}
.res-caso{padding:14px 16px;border-radius:10px;font-size:17px}.res-caso.ok{border:2px solid var(--verde);background:rgba(124,255,178,.1)}.res-caso.mal{border:2px solid #ff5c7a;background:rgba(255,92,122,.1)}
@media(max-width:560px){.form-caso .dos{grid-template-columns:1fr}.tucaso{flex-direction:column;text-align:center}}
.firma-a{display:flex;align-items:center;gap:12px;margin:4px 0 14px}
.firma-a img{width:58px;height:58px;border-radius:50%;border:3px solid var(--verde);box-shadow:0 0 12px rgba(124,255,178,.5);object-fit:cover}
.firma-a b{display:block;font-family:'Righteous',sans-serif;font-weight:400;font-size:20px;color:#fff}
.firma-a span{font-size:15px;color:var(--muted)}.firma-a a{color:var(--verde)}
.autor-a{display:flex;gap:18px;align-items:center;margin:28px 0;padding:18px;border:3px solid var(--verde);border-radius:16px;background:linear-gradient(135deg,rgba(124,255,178,.14),rgba(7,2,26,.6))}
.autor-a img{width:100px;height:100px;border-radius:50%;border:4px solid var(--verde);flex:none;object-fit:cover}
.autor-a small{font-family:'VT323',monospace;font-size:19px;color:var(--verde)}
.autor-a b{display:block;font-family:'Righteous',sans-serif;font-weight:400;font-size:26px;color:#fff}
.autor-a p{margin:4px 0 8px;font-size:16px;color:#cfe9db}.autor-a a{color:var(--verde);font-weight:700}
@media(max-width:520px){.autor-a{flex-direction:column;text-align:center}}
</style>'''

def ilus(img):
    return f'/misterio/img/{img}.webp' if os.path.exists(f'{RAIZ}/misterio/img/{img}.webp') else f'/misterio/img/{img}.svg'

def nivel(n):
    return ''.join('<span class="on">👽</span>' if i < n else '<span class="off">👽</span>' for i in range(5))

def gancho(c):
    # primer párrafo del relato corto como entrada; el resto lo cuentan las secciones largas
    if c['id'] == 'caso-vallecas': return ''
    m = re.search(r'<p>.*?</p>', c['texto'], re.S); return m.group(0) if m else ''

def limpio(t): return re.sub(r'<[^>]+>', '', t)

def palabras(c, x):
    t = c['texto'] + ' '.join(h for _, h in x['secciones']) + x['esceptico'] + x['visitar'] + ' '.join(x['flipar'])
    return len(limpio(t).split())

for i, (c, reg, ureg) in enumerate(todos):
    x = L[c['id']]; url = f'https://trollacos.com/misterio/{c["id"]}/'
    ant = todos[i - 1][0]; sig = todos[(i + 1) % len(todos)][0]
    mins = max(3, round(palabras(c, x) / 200))
    secs = ''.join(f'<h2>{t}</h2><div class="sec">{h}</div>' for t, h in x['secciones'])
    crono = ''.join(f'<li><b>{f}</b>{t}</li>' for f, t in x['cronologia'])
    flipa = ''.join(f'<li>{t}</li>' for t in x['flipar'])
    share = html.escape(f'{c["titulo"]}: {c["sub"]} {url}')
    desc = html.escape(f'{c["sub"]}. Todo el expediente: la historia, la leyenda, la cronología y lo que dicen los escépticos, contado por Trollacos.')
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": f'{limpio(c["titulo"])}: {limpio(c["sub"])}',
          "image": "https://trollacos.com" + ilus(c['img']), "inLanguage": "es", "datePublished": "2026-11-02", "dateModified": "2026-11-02",
          "author": {"@type": "Organization", "name": "Trollacos"}, "mainEntityOfPage": url,
          "publisher": {"@type": "Organization", "name": "Trollacos", "logo": {"@type": "ImageObject", "url": "https://trollacos.com/icono-512.png"}}}
    page = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(limpio(c["titulo"]))}: {html.escape(limpio(c["sub"]))} | Archivos Secretos</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(limpio(c['titulo']))} · Archivos Secretos">
<meta property="og:description" content="{html.escape(limpio(c['sub']))}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://trollacos.com{ilus(c['img'])}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/icono.png">
{style.replace('</style>', extra)}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<nav class="top">
  <a href="/"><img class="px" src="/logo.webp" alt="Trollacos" width="1600" height="161"></a>
  <a href="{ureg}">‹ {({"Latinoamérica": "LATAM"}).get(reg, reg.upper())}</a>
</nav>
<main class="exp">
<p class="migas"><a href="/misterio/">Archivos Secretos</a> › <a href="{ureg}">{reg}</a> ›</p>
<article class="caso" id="{c['id']}">
  <div class="sello">EXPEDIENTE {i + 1:02d}/{len(todos)}</div>
  <h1>{c['titulo']}</h1>
  <p class="subt">{c['sub']}</p>
  <div class="firma-a"><img src="/img/aris.jpg" alt="Dr. Aris V. Torres" width="58" height="58"><div><b>Por el Dr. Aris V. Torres</b><span>Investigador de los misterios · <a href="/misterio/aris-v-torres/">¿Quién es?</a> · ⏱️ {mins} min</span></div></div>
  <figure class="ilus"><img src="{ilus(c['img'])}" alt="Ilustración de {html.escape(limpio(c['titulo']))}" width="600" height="340"></figure>
  <ul class="ficha">
    <li><b>📍 Dónde</b>{c['lugar']}</li>
    <li><b>🕰️ Cuándo</b>{c['cuando']}</li>
    {'' if c['metro'] in ('—', '') else '<li><b>🚇 Cómo llegar</b>' + c['metro'] + '</li>'}
    <li><b>Nivel de misterio</b><span class="nivel" aria-label="{c['nivel']} de 5">{nivel(c['nivel'])}</span></li>
  </ul>
  <div class="relato">{gancho(c)}</div>
  {secs}
  <h2>🕰️ Cronología</h2>
  <ul class="crono">{crono}</ul>
  <h2>🤯 Datos para flipar</h2>
  <div class="flipa"><ul>{flipa}</ul></div>
  <h2>🔬 Lo que dicen los escépticos</h2>
  <div class="esceptico">{x['esceptico']}</div>
  <div class="opina"><img class="px" src="/img/trollaco.png" alt=""><p><b>EL TROLLACO OPINA:</b> {c['trollaco']}</p></div>
  <h2>📍 Cómo visitarlo</h2>
  <div class="visita">{x['visitar']}</div>
  <p class="comp"><a href="https://wa.me/?text={share}" target="_blank" rel="noopener">Compartir por WhatsApp</a><a href="https://t.me/share/url?url={url}" target="_blank" rel="noopener">Telegram</a></p>
  <div class="autor-a"><img src="/img/aris.jpg" alt="Dr. Aris V. Torres" width="100" height="100"><div><small>&gt; ESTE EXPEDIENTE LO HA INVESTIGADO_</small><b>Dr. Aris V. Torres</b><p>Investigador de los misterios de los Archivos Secretos. Llega del otro lado para contarnos los casos que la historia todavía no ha resuelto.</p><a href="/misterio/aris-v-torres/">Conoce al doctor ›</a></div></div>
  <a class="tucaso" href="/misterio/tu-caso/"><span>📨</span><div><small>&gt; ¿TE HA PASADO ALGO RARO?_</small><b>Cuéntanos tu caso</b><p>Casas que crujen, luces en el cielo, cosas que nadie supo explicar. El Dr. Aris lee todos y publica los mejores.</p></div></a>
  <p class="fuentes">Fuentes consultadas: {x['fuentes']}. Texto e ilustración de Trollacos. Contamos la leyenda como leyenda y, al final, lo que dicen los escépticos.</p>
</article>
<nav class="navexp" aria-label="Más expedientes">
  <a href="/misterio/{ant['id']}/"><small>‹ EXPEDIENTE ANTERIOR</small>{ant['titulo']}</a>
  <a class="sig" href="/misterio/{sig['id']}/"><small>SIGUIENTE EXPEDIENTE ›</small>{sig['titulo']}</a>
</nav>
<p class="volver"><a href="{ureg}#mapa">🗺️ Ver todos los casos de {reg} en el mapa</a></p>
</main>
{foot}
</body>
</html>
'''
    os.makedirs(f'{RAIZ}/misterio/{c["id"]}', exist_ok=True)
    open(f'{RAIZ}/misterio/{c["id"]}/index.html', 'w', encoding='utf-8').write(page)

# enlaces «Leer el expediente completo» en las páginas de región
for _, ureg, Ls in REG:
    p = f'{RAIZ}{ureg}index.html'; s = open(p, encoding='utf-8').read()
    for c in Ls:
        btn = f'<p class="leer"><a href="/misterio/{c["id"]}/">📂 LEER EL EXPEDIENTE COMPLETO ›</a></p>'
        if btn in s: continue
        k = s.find(f'id="{c["id"]}"'); j = s.find('<p class="volver">', k)
        s = s[:j] + btn + '\n  ' + s[j:]
    if '.leer a{' not in s:
        s = s.replace('</style>', '.leer{margin:16px 0 4px}.leer a{display:inline-block;padding:11px 18px;border:2px solid var(--verde);border-radius:10px;color:#eafff3;font-family:\'VT323\',monospace;font-size:22px;text-decoration:none;background:rgba(124,255,178,.08);box-shadow:0 0 14px rgba(124,255,178,.25)}.leer a:hover{background:rgba(124,255,178,.18)}\n</style>', 1)
    open(p, 'w', encoding='utf-8').write(s)

# sitemap
sm = open(f'{RAIZ}/sitemap.xml', encoding='utf-8').read()
nuevos = ''.join(f'  <url><loc>https://trollacos.com/misterio/{c["id"]}/</loc><changefreq>monthly</changefreq></url>\n'
                 for c, _, _ in todos if f'/misterio/{c["id"]}/' not in sm)
if nuevos:
    open(f'{RAIZ}/sitemap.xml', 'w', encoding='utf-8').write(sm.replace('</urlset>', nuevos + '</urlset>'))
print(f'expedientes: {len(todos)} páginas')

# ---------- ficha del Dr. Aris V. Torres ----------
bio = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dr. Aris V. Torres, investigador de los misterios | Archivos Secretos</title>
<meta name="description" content="Quién es el Dr. Aris V. Torres, el personaje que firma los expedientes de misterio de Trollacos: arqueología, ovnis y enigmas paranormales.">
<link rel="canonical" href="https://trollacos.com/misterio/aris-v-torres/">
<meta property="og:image" content="https://trollacos.com/misterio/img/aris-despacho.webp">
<link rel="icon" href="/icono.png">
{style.replace('</style>', extra)}
</head><body>
<nav class="top"><a href="/"><img class="px" src="/logo.webp" alt="Trollacos" width="1600" height="161"></a><a href="/misterio/">‹ ARCHIVOS SECRETOS</a></nav>
<main class="exp">
<article class="caso">
  <div class="sello">FICHA DEL INVESTIGADOR</div>
  <h1>Dr. Aris V. Torres</h1>
  <p class="subt">Investigación y fronteras del misterio</p>
  <figure class="ilus"><img src="/misterio/img/aris-despacho.webp" alt="El Dr. Aris V. Torres en su despacho" width="1200" height="544"></figure>
  <div class="sec">
  <p>El <strong>Dr. Aris V. Torres</strong> encabeza la sección de investigación de Trollacos y firma todos los casos de los <a href="/misterio/">Archivos Secretos</a>. Aporta rigor y una mirada abierta al análisis de los grandes enigmas que han desconcertado a la humanidad, convencido de que tanto los vestigios del pasado como los fenómenos más extraños de la realidad guardan respuestas que la historia convencional aún no ha descifrado del todo.</p>
  <h2>Rigor ante todo</h2>
  <p>Su trayectoria se mueve entre la Historia Antigua, la Antropología y la Arqueología. Su norma es sencilla: <strong>primero las fuentes, después las conclusiones</strong>. Antes de opinar sobre cualquier hecho anómalo examina con lupa los documentos, los testimonios y las pruebas físicas. Por eso cada expediente termina con lo que dicen los escépticos: el doctor cree que un buen misterio aguanta cualquier pregunta.</p>
  <h2>Áreas de investigación</h2>
  <ul class="crono" style="border-left-color:var(--verde)">
   <li><b>Arqueología y civilizaciones antiguas</b>Estructuras monumentales, vestigios precolombinos y enigmas arquitectónicos repartidos por todo el planeta.</li>
   <li><b>Ufología y fenómenos anómalos</b>Los registros sobre fenómenos aéreos no identificados, de Manises a Bariloche y Roswell, y los límites de la exploración espacial.</li>
   <li><b>Enigmas paranormales</b>Sucesos insólitos y manifestaciones que escapan a la explicación científica tradicional, del Palacio de Linares a las caras de Bélmez.</li>
  </ul>
  <h2>Divulgación</h2>
  <p>Combina el trabajo de archivo con el de campo. Sus expedientes buscan acercar al lector a una comprensión más profunda y crítica de los grandes misterios, desafiando dogmas y manteniendo viva la curiosidad por lo que habita en las sombras del conocimiento. Dicen que <strong>llega del otro lado</strong> para contarnos las historias más interesantes y los casos todavía sin resolver de la historia de la humanidad.</p>
  </div>
  <div class="opina"><img class="px" src="/img/trollaco.png" alt=""><p><b>EL TROLLACO OPINA:</b> Le pregunté al doctor si había visto un fantasma de verdad. Se quitó las gafas, me miró fijamente y dijo: «Depende de qué entiendas por "de verdad"». Desde entonces duermo con la luz encendida.</p></div>
  <p class="fuentes">Los casos que firma el doctor están documentados con sus fuentes al final de cada expediente.</p>
  <h2>Sus últimos expedientes</h2>
  <nav class="navexp" style="grid-template-columns:1fr">{"".join(f'<a href="/misterio/{c["id"]}/"><small>{r.upper()}</small>{c["titulo"]}</a>' for c, r, u in todos[:6])}</nav>
</article>
</main>
{foot}
</body></html>'''
os.makedirs(f'{RAIZ}/misterio/aris-v-torres', exist_ok=True)
open(f'{RAIZ}/misterio/aris-v-torres/index.html', 'w', encoding='utf-8').write(bio)
sm = open(f'{RAIZ}/sitemap.xml', encoding='utf-8').read()
if '/misterio/aris-v-torres/' not in sm:
    open(f'{RAIZ}/sitemap.xml', 'w', encoding='utf-8').write(sm.replace('</urlset>', '  <url><loc>https://trollacos.com/misterio/aris-v-torres/</loc><changefreq>yearly</changefreq></url>\n</urlset>'))
print('ficha del doctor ok')


# ---------- «Cuéntanos tu caso» ----------
tucaso = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cuéntanos tu caso: tu historia de misterio | Archivos Secretos</title>
<meta name="description" content="¿Te ha pasado algo que nadie supo explicar? Mándanos tu historia de misterio, fantasmas u ovnis. El Dr. Aris V. Torres las lee todas y publica las mejores en los Archivos Secretos.">
<link rel="canonical" href="https://trollacos.com/misterio/tu-caso/">
<meta property="og:image" content="https://trollacos.com/misterio/img/aris-despacho.webp">
<link rel="icon" href="/icono.png">
{style.replace('</style>', extra)}
</head><body>
<nav class="top"><a href="/"><img class="px" src="/logo.webp" alt="Trollacos" width="1600" height="161"></a><a href="/misterio/">‹ ARCHIVOS SECRETOS</a></nav>
<main class="exp">
<article class="caso">
  <div class="sello">BUZÓN DEL DOCTOR</div>
  <h1>Cuéntanos tu caso</h1>
  <p class="subt">Los Archivos Secretos también los escribís vosotros</p>
  <div class="sec">
  <p>¿Una casa en la que pasaban cosas raras? ¿Unas luces en el cielo que no eran un avión? ¿Una historia que se cuenta en tu pueblo desde siempre? El <strong>Dr. Aris V. Torres</strong> lee todos los casos que le llegan, los investiga y <strong>publica los mejores</strong> en los Archivos Secretos.</p>
  <p>Cuéntalo con tus palabras y con todos los detalles que recuerdes: cuándo fue, dónde, quién estaba y qué pasó. Si se publica, saldrá con el alias que elijas (o sin firma) y <strong>sin nombres de nadie</strong>, ni direcciones, ni nada que permita identificar a una persona.</p>
  </div>
  <form class="form-caso" id="form-caso" novalidate>
    <div class="dos">
      <label>¿Dónde pasó? *<span>Pueblo, ciudad, provincia o país. No pongas direcciones exactas.</span><input type="text" name="lugar" maxlength="100" required placeholder="Ej.: un pueblo de Cuenca"></label>
      <label>¿Cuándo?<span>Año o época</span><input type="text" name="anio" maxlength="30" placeholder="Ej.: verano de 1998"></label>
    </div>
    <label>Tu historia *<span>Mínimo un par de frases. Máximo 4.000 caracteres.</span><textarea name="relato" maxlength="4000" required placeholder="Era una noche de agosto y…"></textarea></label>
    <div class="dos">
      <label>Alias para firmar<span>Opcional. Si lo dejas vacío, se publica sin firma.</span><input type="text" name="alias" maxlength="40" placeholder="Ej.: El de Cuenca"></label>
      <label>Tu email<span>Opcional, por si el doctor quiere preguntarte algo. No se publica nunca.</span><input type="email" name="email" maxlength="120" placeholder="tu@email.com"></label>
    </div>
    <label class="trampa" aria-hidden="true">No rellenes esto<input type="text" name="web" tabindex="-1" autocomplete="off"></label>
    <label class="chk"><input type="checkbox" name="acepto" required><span style="color:inherit;font-size:16px">Tengo <b>14 años o más</b>, la historia es mía (o me la han contado y la cuento con mis palabras), y acepto que Trollacos la publique editada, con mi alias o sin firma. He leído la <a href="/privacidad/" style="color:var(--verde)">política de privacidad</a>.</span></label>
    <button type="submit">📨 MANDAR MI CASO AL DOCTOR</button>
    <div class="res-caso" id="res-caso" hidden></div>
  </form>
  <div class="opina"><img class="px" src="/img/trollaco.png" alt=""><p><b>EL TROLLACO OPINA:</b> Yo le mandé lo del calcetín que desaparece en la lavadora y me dijo que eso no es paranormal, que es estadística. Vosotros mandad cosas serias.</p></div>
  <p class="fuentes">Antes de publicar un caso lo revisamos y lo editamos. No publicamos nada que pueda hacer daño a personas reales ni datos que permitan identificar a nadie. Si mandas un caso y luego quieres retirarlo, escríbenos a info@trollacos.com.</p>
</article>
</main>
{foot}
<script>
(function(){{var f=document.getElementById('form-caso'),r=document.getElementById('res-caso');
f.addEventListener('submit',function(e){{e.preventDefault();var b=f.querySelector('button');
var d={{lugar:f.lugar.value,anio:f.anio.value,relato:f.relato.value,alias:f.alias.value,email:f.email.value,web:f.web.value,acepto:f.acepto.checked}};
function msg(t,ok){{r.hidden=false;r.className='res-caso '+(ok?'ok':'mal');r.textContent=t;}}
if(!d.acepto){{msg('Tienes que marcar la casilla para mandarlo.',false);return;}}
if(d.relato.trim().length<80){{msg('Cuéntanos un poco más: al menos un par de frases.',false);return;}}
b.disabled=true;b.textContent='Enviando…';
fetch('/api/casos.php',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(d)}}).then(function(x){{return x.json()}}).then(function(j){{
if(j.ok){{f.querySelectorAll('input,textarea').forEach(function(i){{if(i.type!=='checkbox')i.value='';else i.checked=false}});msg('📂 ¡Recibido! Tu caso ya está en la mesa del Dr. Aris. Si se publica, lo verás en los Archivos Secretos.',true);}}
else msg(j.mensaje||'No se ha podido mandar. Prueba otra vez en un rato.',false);
}}).catch(function(){{msg('No se ha podido mandar. Revisa la conexión y prueba otra vez.',false)}}).finally(function(){{b.disabled=false;b.textContent='📨 MANDAR MI CASO AL DOCTOR'}});
}});}})();
</script>
</body></html>'''
os.makedirs(f'{RAIZ}/misterio/tu-caso', exist_ok=True)
open(f'{RAIZ}/misterio/tu-caso/index.html', 'w', encoding='utf-8').write(tucaso)
sm = open(f'{RAIZ}/sitemap.xml', encoding='utf-8').read()
if '/misterio/tu-caso/' not in sm:
    open(f'{RAIZ}/sitemap.xml', 'w', encoding='utf-8').write(sm.replace('</urlset>', '  <url><loc>https://trollacos.com/misterio/tu-caso/</loc><changefreq>yearly</changefreq></url>\n</urlset>'))
print('cuéntanos tu caso ok')
