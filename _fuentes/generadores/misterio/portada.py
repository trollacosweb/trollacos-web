"""Bloque «Expediente Trollaco» de la portada (entre <!--MIS:INICIO--> y <!--MIS:FIN-->).
Caso de la semana (cambia solo cada lunes), accesos a Madrid, España y el mundo y un «caso al azar».
Uso: python3 _fuentes/generadores/misterio/portada.py   (lo llama también generar.py)"""
import os, re, sys, json, html
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = '/home/claude/trollacos-web'  # rutas fijas, como el resto de generadores
sys.path.insert(0, AQUI)
import casos as C

def ilus(img):
    return f'/misterio/img/{img}.webp' if os.path.exists(os.path.join(RAIZ, 'misterio/img', img + '.webp')) else f'/misterio/img/{img}.svg'

def limpio(t): return re.sub(r'<[^>]+>', '', t).strip()

REG = [('📍 MADRID', '/misterio/', C.CASOS + C.SIERRA, 'Palacios malditos, ovnis en Aluche y una estación fantasma en la línea 1.'),
       ('🇪🇸 ESPAÑA', '/misterio/espana/', C.ESPANA, 'Las caras de Bélmez, el avión que huyó de unas luces en Manises y la esfera de Canarias.'),
       ('🌍 EL MUNDO', '/misterio/mundo/', C.MUNDO, 'Roswell, el «Tic Tac» que grabó la Marina de EE. UU. y las luces de Phoenix.')]
todos = []
for nombre, url, L, _ in REG:
    for c in L:
        todos.append(dict(u=f'{url}#{c["id"]}', i=ilus(c["img"]), t=c['titulo'], s=c['sub'],
                          l=limpio(c['lugar']), c=limpio(c['cuando']), n=c['nivel'], tr=limpio(c['trollaco']), r=nombre[2:].strip().title()))
total = len(todos)
c0 = todos[0]

def miedo(n): return '👻' * n + '<span class="mi-off">' + '👻' * (5 - n) + '</span>'

regiones = ''.join(
    f'<a class="mi-reg" href="{url}"><img src="{ilus(L[0]["img"])}" alt="" loading="lazy">'
    f'<span><b>{nombre}</b><small>{len(L)} casos</small><em>{d}</em></span></a>'
    for nombre, url, L, d in REG)

bloque = f'''<!--MIS:INICIO-->
<section class="block mis" id="misterio">
  <div class="mis-cab">
    <img class="px mis-tr" src="/misterio/img/trollaco-linterna.png" alt="El Trollaco con una linterna" width="64" height="64">
    <div><span class="mis-k">&gt; ARCHIVO CLASIFICADO · {total} CASOS_</span><h2>Expediente Trollaco</h2>
    <p class="mis-int">Fantasmas, ovnis y sucesos que nadie supo explicar, de Madrid al resto del planeta. Te contamos cada caso como lo cuenta la leyenda… y luego lo que dicen los escépticos. <b>Tú decides qué creerte.</b></p></div>
  </div>
  <a class="mis-caso" id="mis-caso" href="{c0['u']}">
    <div class="mis-img"><img id="mis-i" src="{c0['i']}" alt="" width="600" height="340"><span class="mis-sello">CASO DE LA SEMANA</span></div>
    <div class="mis-txt">
      <span class="mis-meta" id="mis-m">{html.escape(c0['r'])} · {html.escape(c0['c'])}</span>
      <b id="mis-t">{html.escape(c0['t'])}</b>
      <em id="mis-s">{html.escape(c0['s'])}</em>
      <span class="mis-lugar" id="mis-l">📍 {html.escape(c0['l'])}</span>
      <span class="mis-niv">NIVEL DE MIEDO: <span id="mis-n">{miedo(c0['n'])}</span></span>
      <span class="mis-dice" id="mis-d">«{html.escape(c0['tr'])}»</span>
      <span class="mis-btn">🔦 ABRIR EXPEDIENTE ›</span>
    </div>
  </a>
  <div class="mis-regs">{regiones}</div>
  <p class="mis-pie"><button type="button" class="mis-azar" id="mis-azar">🎲 Ábreme un caso al azar</button> <a href="/misterio/#mapa">🗺️ Ver el mapa de Madrid</a></p>
</section>
<script>
(function(){{var C={json.dumps(todos, ensure_ascii=False)};
function esc(t){{return t.replace(/[&<>"]/g,function(c){{return{{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]}})}}
function pon(c,sello){{var g=function(i){{return document.getElementById(i)}};g('mis-caso').href=c.u;g('mis-i').src=c.i;g('mis-t').textContent=c.t;g('mis-s').textContent=c.s;
g('mis-l').textContent='📍 '+c.l;g('mis-m').textContent=c.r+' · '+c.c;g('mis-d').textContent='«'+c.tr+'»';
g('mis-n').innerHTML='👻'.repeat(c.n)+'<span class="mi-off">'+'👻'.repeat(5-c.n)+'</span>';
if(sello)document.querySelector('.mis-sello').textContent=sello;}}
var sem=Math.floor((Date.now()/864e5+3)/7);pon(C[sem%C.length]);
document.getElementById('mis-azar').addEventListener('click',function(){{location.href=C[Math.floor(Math.random()*C.length)].u}});
}})();
</script>
<!--MIS:FIN-->'''

CSS = '''<!--MISCSS:INICIO--><style>
.mis{padding-top:10px}
.mis-cab{display:flex;gap:16px;align-items:center;max-width:980px;margin:0 auto 18px}
.mis-tr{width:72px;flex:none;image-rendering:pixelated;filter:drop-shadow(0 0 10px rgba(124,255,178,.6))}
.mis-k{font-family:'VT323',monospace;font-size:20px;color:#7cffb2}
.mis h2{text-align:left;margin:2px 0 6px;color:#eafff3;text-shadow:0 0 14px rgba(124,255,178,.7)}
.mis-int{margin:0;font-size:17px;color:#cfe9db}
.mis-caso{display:grid;grid-template-columns:1.15fr 1fr;max-width:980px;margin:0 auto;text-decoration:none;border:2px solid #7cffb2;border-radius:16px;overflow:hidden;background:linear-gradient(135deg,rgba(124,255,178,.12),rgba(7,2,26,.85));box-shadow:0 0 26px rgba(124,255,178,.3);transition:box-shadow .2s}
.mis-caso:hover{box-shadow:0 0 40px rgba(124,255,178,.6)}
.mis-img{position:relative;background:#05010f}.mis-img img{display:block;width:100%;height:100%;object-fit:cover;min-height:220px}
.mis-sello{position:absolute;top:12px;left:12px;padding:4px 10px;background:#b8001f;color:#fff;font-family:'VT323',monospace;font-size:19px;letter-spacing:1px;border:2px solid #fff;transform:rotate(-4deg);box-shadow:3px 3px 0 rgba(0,0,0,.5)}
.mis-txt{display:flex;flex-direction:column;gap:6px;padding:18px 20px}
.mis-meta{font-family:'VT323',monospace;font-size:18px;color:#7cffb2}
.mis-txt b{font-family:'Righteous',sans-serif;font-weight:400;font-size:26px;line-height:1.15;color:#fff}
.mis-txt em{font-style:normal;color:#ffd23f;font-weight:700;font-size:17px}
.mis-lugar{font-size:15px;color:#cfe9db}
.mis-niv{font-family:'VT323',monospace;font-size:18px;color:#cfe9db}.mi-off{opacity:.2}
.mis-dice{font-size:15px;color:#e9e6ff;font-style:italic;border-left:3px solid #7cffb2;padding-left:10px}
.mis-btn{align-self:flex-start;margin-top:4px;padding:8px 14px;border:2px solid #7cffb2;border-radius:8px;color:#7cffb2;font-weight:700;font-size:15px}
.mis-regs{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:980px;margin:14px auto 0}
.mi-reg{display:flex;flex-direction:column;text-decoration:none;border:1px solid rgba(124,255,178,.45);border-radius:12px;overflow:hidden;background:rgba(124,255,178,.05)}
.mi-reg:hover{border-color:#7cffb2;box-shadow:0 0 16px rgba(124,255,178,.35)}
.mi-reg img{width:100%;height:110px;object-fit:cover;display:block;filter:saturate(.9) brightness(.85)}
.mi-reg span{padding:10px 12px}.mi-reg b{display:block;font-family:'Righteous',sans-serif;font-weight:400;font-size:18px;color:#fff}
.mi-reg small{font-family:'VT323',monospace;font-size:17px;color:#7cffb2}.mi-reg em{display:block;font-style:normal;font-size:14px;color:#cfe9db;margin-top:4px}
.mis-pie{max-width:980px;margin:14px auto 0;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
.mis-pie a{color:#7cffb2}
.mis-azar{cursor:pointer;padding:9px 16px;border-radius:10px;border:2px dashed #7cffb2;background:transparent;color:#eafff3;font:700 16px inherit;font-family:inherit}
.mis-azar:hover{background:rgba(124,255,178,.12)}
@media(max-width:760px){.mis-caso{grid-template-columns:1fr}.mis-img img{min-height:0;aspect-ratio:600/340}.mis-regs{grid-template-columns:1fr}.mi-reg{flex-direction:row}.mi-reg img{width:110px;height:auto;min-height:100%}.mis-tr{width:56px}.mis-txt b{font-size:23px}}
</style><!--MISCSS:FIN-->'''

p = os.path.join(RAIZ, 'index.html')
s = open(p, encoding='utf-8').read()
if '<!--MIS:INICIO-->' in s:
    s = re.sub(r'<!--MIS:INICIO-->.*?<!--MIS:FIN-->', lambda m: bloque, s, flags=re.S)
else:  # primera vez: quita el banner viejo y pone el bloque justo después del especial de GTA VI
    s = re.sub(r'\n<section class="block" id="misterio">.*?</section>\n', '\n', s, count=1, flags=re.S)
    i = s.find('<section class="block gta" id="gta">'); j = s.find('</section>', i) + len('</section>')
    s = s[:j] + '\n\n' + bloque + s[j:]
if '<!--MISCSS:INICIO-->' in s:
    s = re.sub(r'<!--MISCSS:INICIO-->.*?<!--MISCSS:FIN-->', lambda m: CSS, s, flags=re.S)
else:
    s = s.replace('</head>', CSS + '\n</head>', 1)
open(p, 'w', encoding='utf-8').write(s)
print(f'portada: Expediente Trollaco con {total} casos')
