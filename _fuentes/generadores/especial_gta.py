"""Especial «De Liberty City a Leonida: la historia de GTA» → /especiales/historia-gta/ (+ portada /especiales/ y sitemap).
Firma Danna. Datos en especial_gta_datos.py, con fuente citada por su nombre; la opinión es nuestra.
Portadas: /img/especiales/gta/<slug>.webp (si no existe, sale un icono).
Uso: python3 _fuentes/generadores/especial_gta.py"""
import os, html, json, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(RAIZ)
sys.path.insert(0, os.path.join(RAIZ, '_fuentes', 'generadores'))
from especial_gta_datos import TIEMPO, F, ROCKSTAR, RADIO, FUENTES_EXTRA, VIDEOS
URL = '/especiales/historia-gta/'
FECHA = '11 de noviembre de 2026'
IMG = 'img/especiales/gta'
def esc(t): return html.escape(t, quote=True)

# ───────────────────────── página ─────────────────────────
g = open('gta-6/index.html', encoding='utf-8').read()
style = g[g.find('<style>'):g.find('</style>') + 8]
foot = g[g.find('<footer>'):g.find('</footer>') + 9]
fut = open('_fuentes/generadores/especial_futbol.py', encoding='utf-8').read()
extra = fut[fut.find("extra = '''") + 11:fut.find("</style>'''", fut.find("extra = '''"))]
style2 = style.replace('</style>', extra + '.vids-esp{display:grid;gap:14px;margin:16px 0}.vids-esp.dos{grid-template-columns:1fr 1fr}@media(max-width:700px){.vids-esp.dos{grid-template-columns:1fr}}' + '.intro{font-size:19px;line-height:1.65;margin:1em 0}.saga{margin:10px 0 0;padding-left:20px}.saga li{font-size:18px;margin-bottom:8px}.saga b{color:var(--yellow)}\n@media(max-width:700px){.intro{font-size:18px}.saga li{font-size:17px}}</style>')

def portada(x):
    p = f'{IMG}/{x["slug"]}.webp'
    if os.path.exists(p):
        return f'<div class="port"><img src="/{p}" alt="Portada de {esc(x["titulo"])}" width="220" height="293" loading="lazy"></div>'
    return f'<div class="port" aria-hidden="true">{x["icono"]}</div>'

def videos_de(slug):
    vs = VIDEOS.get(slug, [])
    if not vs: return ''
    t = ''.join(f'''<div class="vid"><button type="button" class="vid-play" data-id="{i}" aria-label="Ver {esc(n)}"><img src="https://i.ytimg.com/vi/{i}/hqdefault.jpg" alt="{esc(n)}" loading="lazy" referrerpolicy="no-referrer"><span>▶</span></button>
<div class="vid-txt"><span class="rol">🎬 VÍDEO</span><h3 style="margin:2px 0 0;font-size:19px">{esc(n)}</h3><p>{esc(p)}</p><a class="yt" href="https://www.youtube.com/watch?v={i}" target="_blank" rel="noopener">¿No se ve? Ábrelo en YouTube ↗</a></div></div>''' for i, n, p in vs)
    return f'<div class="vids-esp{" dos" if len(vs) > 1 else ""}">{t}</div>'

def html_ficha(x):
    datos = ''.join(f'<li>{d}</li>' for d in x['datos'])
    fu = ' · '.join(esc(f) for f in x['fuentes'])
    pie = '<p class="fu">Portada © sus titulares.</p>' if os.path.exists(f'{IMG}/{x["slug"]}.webp') else ''
    return f'''<section class="ficha-j" id="{x['slug']}">
<div class="cab">{portada(x)}<div><span class="sub">&gt; {esc(x['sub'].upper())}_</span><h3>{esc(x['titulo'])}</h3>
<dl><dt>AÑO</dt><dd>{x['anio']}</dd><dt>DÓNDE</dt><dd>{esc(x['plataformas'])}</dd><dt>QUIÉN</dt><dd>{esc(x['estudio'])}</dd></dl></div></div>
{('<div class="intro">' + x['intro'] + '</div>') if '<ul' in x['intro'] else '<p>' + x['intro'] + '</p>'}
{videos_de(x['slug'])}
<div class="flipar"><b class="t">🤯 DATOS PARA FLIPAR</b><ul>{datos}</ul></div>
<div class="nota"><img src="/img/trollaco.png" alt=""><p><b>EL TROLLACO OPINA:</b> {esc(x['troll'])}</p></div>
{pie}<p class="fu">Fuentes: {fu}.</p>
</section>'''


def tl_item(a, t, d, ancla):
    return f'<li><a href="#{ancla}"><span class="a">{a}</span><b>{esc(t)}</b><span>{esc(d)}</span></a></li>'
tl = ''.join(tl_item(*t) for t in TIEMPO)
ERAS = [
    ('era-2d', '🗺️ La era 2D: desde arriba', 'Cámara cenital, ciudades inventadas y mucha polémica. Así empezó todo en un estudio de Escocia.', ['gta-1', 'gta-2']),
    ('era-ps2', '📀 La trilogía de PS2', 'Tres juegos en cuatro años que convirtieron a GTA en el fenómeno que es hoy.', ['gta-3', 'vice-city', 'san-andreas']),
    ('era-portatil', '🎮 GTA en el bolsillo', 'Mientras tanto, la saga también se coló en las portátiles.', ['portatiles']),
    ('era-hd', '💎 La era HD', 'Más realismo, más dinero y récords que ninguna película ha superado.', ['gta-4', 'gta-5']),
    ('era-vi', '🌴 Y ahora, Leonida', 'Trece años después, la vuelta a Vice City.', ['gta-6']),
]
usadas = [s for e in ERAS for s in e[3]]
assert sorted(usadas) == sorted(x['slug'] for x in F)
indice = ''.join(f'<a href="#{i}">{t}</a>' for i, t in [('linea', '🕰️ Línea del tiempo'), ('rockstar', '⭐ Rockstar')] + [(e[0], e[1].split(':')[0]) for e in ERAS] +
    [('radio', '📻 La radio'), ('numeros', '📊 Los números')])
FIRMA = ('<div class="firma"><img src="/img/danna.jpg?v=4" alt="Danna" width="56" height="56"><div><b>Por Danna</b>'
         f'<span>Tu reportera del otro lado de la pantalla · <a href="https://www.instagram.com/dannapixel/" target="_blank" rel="noopener">📸 @dannapixel</a> · <a href="/danna/">¿Quién es?</a> · {FECHA}</span></div></div>')
def html_era(e):
    return f'<h2 id="{e[0]}">{e[1]}</h2><p class="era-intro">{e[2]}</p>' + ''.join(html_ficha(next(x for x in F if x['slug'] == sl)) for sl in e[3])
eras_html = ''.join(html_era(e) for e in ERAS)
FUENTES = sorted({f for x in F for f in x['fuentes']} | set(FUENTES_EXTRA))
fuentes = ''.join(f'<li>{esc(f)}</li>' for f in FUENTES)
titulo = 'De Liberty City a Leonida: la historia de GTA'
desc = 'El especial de la saga Grand Theft Auto: de GTA 1 (1997) a GTA III, Vice City, San Andreas, GTA IV, GTA V y GTA VI. Récords, ventas, curiosidades y cómo hemos llegado hasta Leonida.'
cuerpo = f'''<p class="migas"><a href="/">Portada</a> › <a href="/especiales/">Especiales</a> › Historia de GTA</p>
<div class="hero-f"><p class="k">&gt; ESPECIAL TROLLACOS_</p><h1>De Liberty City a Leonida: la historia de GTA</h1>
<p>Casi treinta años robando coches, huyendo de la poli y cambiando de emisora. De un juego de policías que no hacía gracia en Escocia
al lanzamiento más esperado de la historia. Repasamos toda la saga antes de que llegue GTA VI.</p></div>
{FIRMA}
<p>Este especial va para quienes jugaron al primero en un PC con Windows 95, para quienes se pasaron San Andreas en la PS2 del primo y para quienes llevan
trece años esperando a GTA VI. Datos con su fuente, opinión nuestra y mucha nostalgia. Abróchate el cinturón (o no, que esto es GTA). 🚗</p>
<nav class="indice" aria-label="Índice">{indice}</nav>
<h2 id="linea">🕰️ La línea del tiempo</h2>
<ul class="tl">{tl}</ul>
<h2 id="rockstar">⭐ De DMA Design a Rockstar</h2>
{ROCKSTAR}
<p class="fu">Fuentes: Wikipedia (en inglés), «Rockstar Games», «Grand Theft Auto (video game)» y «Grand Theft Auto III».</p>
<div class="nota pri"><img src="/img/princesa.png" alt=""><p><b>LA PRINCESA NEÓN OPINA:</b> ¿Treinta años de GTA y nadie ha hecho una misión para rescatar a una princesa? Pues que sepáis que en Trollaco Run me rescatan cada dos por tres. Bueno, lo intentan.</p></div>
{eras_html}
<h2 id="radio">📻 La radio: el alma de GTA</h2>
{RADIO}
<p class="fu">Fuente: Wikipedia (en inglés), «Grand Theft Auto III».</p>
<h2 id="numeros">📊 Los números</h2>
<div class="cifras">
  <div><b>+230 M</b><span>copias de GTA V (Take-Two, agosto de 2026)</span></div>
  <div><b>1.000 M $</b><span>recaudó GTA V en solo tres días</span></div>
  <div><b>+27,5 M</b><span>copias de San Andreas, el más vendido de PS2</span></div>
  <div><b>+25 M</b><span>copias de GTA IV en 2013</span></div>
  <div><b>+17,5 M</b><span>copias de Vice City</span></div>
  <div><b>+14,5 M</b><span>copias de GTA III</span></div>
  <div><b>+8 M</b><span>copias de Liberty City Stories, el más vendido de PSP</span></div>
  <div><b>90 M</b><span>visitas del tráiler 1 de GTA VI en 24 horas</span></div>
  <div><b>10</b><span>récords Guinness entre GTA IV (3) y GTA V (7)</span></div>
</div>
<div class="reto-f"><p>¿Te sabes todo esto? Pues ahora a ver si te sabes lo de GTA VI 🌴</p><a class="btn" href="/gta-6/">LA GUÍA DE GTA VI</a></div>
<h2>📚 Fuentes de los datos</h2>
<p style="font-size:16px">Los datos salen de estas fuentes, citadas por su nombre. La opinión, las bromas y la nostalgia son nuestras.</p>
<ul class="fuentes-l">{fuentes}</ul>
<p class="fu">Los vídeos son de YouTube y se cargan solo si los pulsas. © sus titulares.</p>
<script>
document.querySelectorAll('.vid-play').forEach(function(b){{b.addEventListener('click',function(){{
  var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+b.getAttribute('data-id')+'?autoplay=1&rel=0';
  f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';f.allowFullscreen=true;f.title=b.getAttribute('aria-label');b.replaceWith(f)}})}});
</script>
<p class="fu">Grand Theft Auto, Rockstar Games y el resto de nombres y marcas citados son de sus respectivos dueños. Trollacos no tiene relación con ellos.</p>'''
ld = {'@context': 'https://schema.org', '@type': 'Article', 'headline': titulo, 'datePublished': '2026-11-11',
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


os.makedirs('especiales/historia-gta', exist_ok=True)
open('especiales/historia-gta/index.html', 'w', encoding='utf-8').write(pagina(titulo, desc, URL, cuerpo, ld, volver=('/especiales/', '‹ ESPECIALES')))
exec(open('_fuentes/generadores/especiales_hub.py', encoding='utf-8').read())
print(f'especial GTA: {len(F)} fichas, {len(TIEMPO)} hitos, {len(FUENTES)} fuentes')
