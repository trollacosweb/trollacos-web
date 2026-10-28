"""Genera las tres páginas del Expediente Trollaco a partir de la plantilla pagina.py."""
import re
BASE = open('/home/claude/trollaco/misterio/pagina.py').read()

TABS = '''<nav class="tabs" aria-label="Expedientes">
  <a href="/misterio/"{m}>📍 MADRID</a><a href="/misterio/espana/"{e}>🇪🇸 ESPAÑA</a><a href="/misterio/mundo/"{w}>🌍 EL MUNDO</a>
</nav>'''

REGIONES = [
 dict(var='CASOS + SIERRA', out='/home/claude/trollacos-web/misterio/index.html', url='https://trollacos.com/misterio/', tab='m',
  title='Lugares encantados de Madrid: 9 casos paranormales con mapa | Expediente Trollaco',
  desc='El Palacio de Linares, la Casa de las Siete Chimeneas, el Ángel Caído, Chamberí, Ummo, el caso Vallecas y los sanatorios de La Barranca y la Marina. Los misterios de Madrid, con mapa interactivo.',
  ogt='Expediente Trollaco: el Madrid que da miedo', ogd='9 lugares de Madrid con historia oscura, en un mapa interactivo. ¿Te atreves?', ogi='https://trollacos.com/misterio/portada.jpg',
  headline='Lugares encantados de Madrid: 9 casos paranormales con mapa',
  h1='EXPEDIENTE TROLLACO<br>El Madrid que da miedo',
  ent='Nueve lugares de Madrid, de Cibeles a la sierra. Nueve historias que nadie te contó en el colegio. Algunas son leyenda. Otras dejaron informes policiales. <strong>Tú decides cuáles creerte.</strong>',
  aviso='⚠️ Contamos cada caso como lo cuenta la leyenda y, al final, lo que dicen los escépticos. En el mapa solo marcamos lugares públicos o visibles desde fuera; el caso Vallecas va solo por barrio, por respeto a sus vecinos. Los sanatorios abandonados son peligrosos: no entres.',
  mapa='Pincha en cada icono para abrir su expediente. Haz zoom, muévete y apunta: algunos los tienes más cerca de lo que crees. Aleja el mapa para ver los de la sierra.'),
 dict(var='ESPANA', out='/home/claude/trollacos-web/misterio/espana/index.html', url='https://trollacos.com/misterio/espana/', tab='e',
  title='Casos paranormales de España: Manises, Bélmez, Canarias y más | Expediente Trollaco',
  desc='Los misterios más sonados de España: el incidente ovni de Manises, las caras de Bélmez, la esfera de Canarias y el Hospital del Tórax. Con mapa interactivo y lo que dicen los escépticos.',
  ogt='Expediente Trollaco: la España del misterio', ogd='Manises, Bélmez, Canarias y el Tórax. Los grandes casos de España, en un mapa. ¿Te atreves?', ogi='https://trollacos.com/misterio/espana/portada.jpg',
  headline='Casos paranormales de España: Manises, Bélmez, Canarias y el Hospital del Tórax',
  h1='EXPEDIENTE TROLLACO<br>La España del misterio',
  ent='Un avión que tuvo que huir de unas luces. Caras que salían del suelo de una cocina. Una esfera que vio medio archipiélago. <strong>Los casos que paralizaron España.</strong>',
  aviso='⚠️ Contamos cada caso como lo cuenta la leyenda y, al final, lo que dicen los escépticos. Si visitas algún lugar, respeta a los vecinos y la propiedad privada.',
  mapa='Pincha en cada icono para abrir su expediente. De Valencia a Canarias, pasando por Jaén y Terrassa.'),
 dict(var='MUNDO', out='/home/claude/trollacos-web/misterio/mundo/index.html', url='https://trollacos.com/misterio/mundo/', tab='w',
  title='Los casos ovni más famosos del mundo: Roswell, Rendlesham, el Tic Tac y Phoenix | Expediente Trollaco',
  desc='Roswell, el bosque de Rendlesham, el "Tic Tac" de la Marina de EE. UU. y las luces de Phoenix. Los grandes casos ovni del mundo, contados con intriga y con mapa interactivo.',
  ogt='Expediente Trollaco: ovnis del mundo', ogd='Roswell, Rendlesham, el Tic Tac del Pentágono y las luces de Phoenix, en un mapa. ¿Te atreves?', ogi='https://trollacos.com/misterio/mundo/portada.jpg',
  headline='Los casos ovni más famosos del mundo: Roswell, Rendlesham, el Tic Tac y Phoenix',
  h1='EXPEDIENTE TROLLACO<br>Ovnis del mundo',
  ent='Un "platillo" que el ejército anunció y luego negó. Militares persiguiendo luces en un bosque. Un vídeo publicado por el Pentágono. <strong>Los casos que siguen sin cerrarse.</strong>',
  aviso='⚠️ Contamos cada caso como lo cuenta la leyenda y, al final, lo que dicen los escépticos.',
  mapa='Pincha en cada icono para abrir su expediente. Mueve el mapa: estos casos están repartidos por el planeta.'),
]

def rep(s, a, b):
    assert s.count(a) >= 1, a[:70]
    return s.replace(a, b)

for R in REGIONES:
    s = BASE
    s = rep(s, 'from casos import CASOS, PROXIMOS', 'from casos import *\nCASOS = ' + R['var'])
    s = rep(s, 'src="img/', 'src="/misterio/img/')
    s = rep(s, '<title>Lugares encantados de Madrid: 7 casos paranormales con mapa | Expediente Trollaco</title>', f'<title>{R["title"]}</title>')
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{R["desc"]}">', s, count=1)
    s = rep(s, '<link rel="canonical" href="https://trollacos.com/misterio/">', f'<link rel="canonical" href="{R["url"]}">')
    s = rep(s, '<meta property="og:title" content="Expediente Trollaco: el Madrid que da miedo">', f'<meta property="og:title" content="{R["ogt"]}">')
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{R["ogd"]}">', s, count=1)
    s = rep(s, '<meta property="og:url" content="https://trollacos.com/misterio/">', f'<meta property="og:url" content="{R["url"]}">')
    s = rep(s, '<meta property="og:image" content="https://trollacos.com/misterio/portada.jpg">', f'<meta property="og:image" content="{R["ogi"]}">')
    s = rep(s, '"headline": "Lugares encantados de Madrid: 7 casos paranormales con mapa"', f'"headline": "{R["headline"]}"')
    s = rep(s, '"mainEntityOfPage": "https://trollacos.com/misterio/"', f'"mainEntityOfPage": "{R["url"]}"')
    s = rep(s, '<h1>EXPEDIENTE TROLLACO<br>El Madrid que da miedo</h1>', f'<h1>{R["h1"]}</h1>')
    s = re.sub(r'<p class="ent">.*?</p>', f'<p class="ent">{R["ent"]}</p>', s, count=1, flags=re.S)
    s = re.sub(r'<p class="aviso">.*?</p>', f'<p class="aviso">{R["aviso"]}</p>', s, count=1, flags=re.S)
    s = rep(s, '<p>Pincha en cada icono para abrir su expediente. Haz zoom, muévete y apunta: algunos los tienes más cerca de lo que crees.</p>', f'<p>{R["mapa"]}</p>')
    # pestañas entre expedientes
    tabs = TABS.format(m=' class="on"' if R['tab'] == 'm' else '', e=' class="on"' if R['tab'] == 'e' else '', w=' class="on"' if R['tab'] == 'w' else '')
    s = rep(s, '<main>\n', '<main>\n  ' + tabs.replace('{', '{{').replace('}', '}}') + '\n')
    s = rep(s, '.aviso{{', '.tabs{{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:22px 0 0}}\n.tabs a{{font-family:\'VT323\',monospace;font-size:22px;text-decoration:none;color:#fff;padding:6px 16px;border:2px solid rgba(124,255,178,.4);border-radius:8px}}\n.tabs a.on,.tabs a:hover{{background:rgba(124,255,178,.18);border-color:var(--verde)}}\n.aviso{{')
    # en lugar de "próximos expedientes": enlaces a los otros dos archivos
    otros = {'m': [('/misterio/espana/', '🇪🇸 La España del misterio', 'Manises, Bélmez, la esfera de Canarias y el Hospital del Tórax.'), ('/misterio/mundo/', '🌍 Ovnis del mundo', 'Roswell, Rendlesham, el Tic Tac del Pentágono y las luces de Phoenix.')],
             'e': [('/misterio/', '📍 El Madrid que da miedo', 'Linares, Siete Chimeneas, Chamberí, Ummo, La Barranca y más.'), ('/misterio/mundo/', '🌍 Ovnis del mundo', 'Roswell, Rendlesham, el Tic Tac del Pentágono y las luces de Phoenix.')],
             'w': [('/misterio/', '📍 El Madrid que da miedo', 'Linares, Siete Chimeneas, Chamberí, Ummo, La Barranca y más.'), ('/misterio/espana/', '🇪🇸 La España del misterio', 'Manises, Bélmez, la esfera de Canarias y el Hospital del Tórax.')]}[R['tab']]
    bloque = ''.join(f'<a class="prox" href="{u}"><b>{t}</b><span>{d}</span></a>' for u, t, d in otros)
    s = re.sub(r'  <h2 class="sec" id="proximamente">.*?\{prox\}\n  </div>\n', '  <h2 class="sec" id="proximamente">🛸 Más expedientes</h2>\n  <div class="prox-wrap">' + bloque.replace('{', '{{').replace('}', '}}') + '</div>\n', s, count=1, flags=re.S)
    s = rep(s, '.prox{{padding:10px 14px;', '.prox{{display:block;text-decoration:none;color:var(--text);padding:12px 16px;')
    # compartir: enlace de la página actual
    s = s.replace('https%3A%2F%2Ftrollacos.com%2Fmisterio%2F', R['url'].replace(':', '%3A').replace('/', '%2F'))
    s = s.replace("navigator.clipboard.writeText('https://trollacos.com/misterio/')", f"navigator.clipboard.writeText('{R['url']}')")
    s = rep(s, "open('/home/claude/trollacos-web/misterio/index.html', 'w')", f"import os; os.makedirs(os.path.dirname('{R['out']}'), exist_ok=True); open('{R['out']}', 'w')")
    exec(compile(s, 'pagina-' + R['tab'], 'exec'), {'__name__': '__main__'})
