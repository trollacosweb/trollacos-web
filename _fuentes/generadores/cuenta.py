import os
os.chdir('/home/claude/trollacos-web')
g = open('gta-6/index.html').read()
style = g[g.find('<style>'):g.find('</style>') + 8]
foot = g[g.find('<footer>'):g.find('</footer>') + 9]
extra = r"""
.panel{margin:26px 0 0;padding:18px;border:2px solid var(--cyan);border-radius:12px;background:rgba(31,242,255,.06)}
.panel h2{margin:0 0 10px}
.pestanas{display:flex;gap:8px;margin-bottom:12px}
.pestanas button{flex:1;font-family:'VT323',monospace;font-size:22px;padding:6px;border:2px solid rgba(31,242,255,.4);border-radius:8px;background:none;color:#fff;cursor:pointer}
.pestanas button.on{background:rgba(31,242,255,.18);border-color:var(--cyan)}
.campo{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:8px 0}
.campo input{font-family:'VT323',monospace;font-size:24px;padding:6px 10px;border-radius:6px;border:2px solid var(--cyan);background:#120530;color:#fff;width:min(260px,100%);text-transform:uppercase;letter-spacing:.15em}
.boton{font-family:'VT323',monospace;font-size:22px;padding:7px 16px;border-radius:8px;border:2px solid var(--pink);background:var(--pink);color:#07021a;cursor:pointer;text-decoration:none;display:inline-block}
.boton.sec{background:none;color:#fff;border-color:rgba(255,255,255,.4)}
.msg{min-height:1.3em;font-size:17px;margin-top:6px}.msg.err{color:#ff8b8b}.msg.ok{color:#9dffb5}
.codigo{margin:10px 0;padding:14px;border:3px dashed var(--yellow);border-radius:10px;text-align:center;background:rgba(255,210,63,.08)}
.codigo b{display:block;font-family:'VT323',monospace;font-size:46px;letter-spacing:.25em;color:var(--yellow)}
.ficha-jug{display:flex;gap:18px;align-items:center;flex-wrap:wrap;padding:18px;border:3px solid var(--pink);border-radius:14px;
  background:linear-gradient(135deg,rgba(255,43,214,.18),rgba(31,242,255,.08));box-shadow:0 0 24px rgba(255,43,214,.35)}
.ficha-jug img{width:72px;height:auto;image-rendering:pixelated}
.ficha-jug .nom{font-family:'VT323',monospace;font-size:52px;line-height:1;color:#fff;letter-spacing:.12em;text-shadow:0 0 12px var(--pink)}
.ficha-jug .sub2{font-size:16px;color:var(--muted)}
.ficha-jug .acc{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap}
.cifras{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-top:14px}
.cifra{border:1px solid rgba(31,242,255,.35);border-radius:10px;padding:10px 12px;background:rgba(31,242,255,.05)}
.cifra b{display:block;font-family:'VT323',monospace;font-weight:400;font-size:36px;line-height:1.1;color:var(--yellow)}
.cifra span{font-size:15px;color:var(--muted)}
.modos-t{width:100%;border-collapse:collapse}
.modos-t td,.modos-t th{padding:8px 10px;border-bottom:1px dashed rgba(233,230,255,.15);text-align:left;font-size:17px}
.modos-t th{font-family:'VT323',monospace;font-size:20px;color:var(--cyan);font-weight:400}
.modos-t td.n{font-family:'VT323',monospace;font-size:24px;color:var(--yellow)}
.modos-t .no{color:var(--muted)}
.caps{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}
.capi{border:2px solid rgba(255,255,255,.15);border-radius:10px;padding:10px;text-align:center;font-size:15px;color:var(--muted)}
.capi b{display:block;font-size:30px}
.capi.ok{border-color:#9dffb5;background:rgba(157,255,181,.08);color:#fff}
.insignias{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px}
.ins{text-align:center;padding:10px 6px;border-radius:10px;border:1px solid rgba(255,210,63,.5);background:rgba(255,210,63,.08)}
.ins i{display:block;font-style:normal;font-size:34px}
.ins b{display:block;font-family:'VT323',monospace;font-weight:400;font-size:20px;color:var(--yellow)}
.ins span{font-size:13px;color:var(--muted)}
.ins.no{opacity:.35;filter:grayscale(1);border-color:rgba(255,255,255,.2);background:none}
.barra-p{height:10px;border-radius:5px;background:rgba(255,255,255,.1);overflow:hidden;margin-top:6px}.barra-p i{display:block;height:100%;background:linear-gradient(90deg,var(--pink),var(--cyan))}
</style>"""
style2 = style.replace('</style>', extra)
hw = "<script>(function(){var d=new Date(),m=d.getMonth(),n=d.getDate();if((m===9&&n>=15)||(m===10&&n<=2))document.documentElement.className+=' halloween'})()</script>"

js = r"""
<script>
(function(){
var API='/api/porra.php',yo=null;
try{yo=JSON.parse(localStorage.getItem('porraCuenta')||'null')}catch(e){}
function $(id){return document.getElementById(id)}
function esc(t){return String(t==null?'':t).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function post(accion,cuerpo){return fetch(API+'?accion='+accion,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(cuerpo)}).then(function(r){return r.json()})}
function msg(id,t,ok){var m=$(id);m.textContent=t||'';m.className='msg '+(ok?'ok':'err')}
function guarda(c){yo=c;try{c?localStorage.setItem('porraCuenta',JSON.stringify(c)):localStorage.removeItem('porraCuenta')}catch(e){}}
document.querySelectorAll('.pestanas button').forEach(function(b){b.onclick=function(){
  document.querySelectorAll('.pestanas button').forEach(function(x){x.classList.toggle('on',x===b)});
  $('f-crear').hidden=b.dataset.t!=='crear';$('f-entrar').hidden=b.dataset.t!=='entrar';}});
function limpia(inp){inp.addEventListener('input',function(){var v=inp.value.replace(/[^0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ]/g,'').slice(0,5);if(v!==inp.value)inp.value=v})}
limpia($('c-nombre'));limpia($('e-nombre'));
$('f-crear').onsubmit=function(e){e.preventDefault();msg('m-crear','Creando...',true);
  post('registrar',{nombre:$('c-nombre').value}).then(function(j){
    if(!j.ok){msg('m-crear',j.mensaje||'No se ha podido crear.');return}
    guarda({nombre:j.nombre,codigo:j.codigo});$('nuevo-codigo').textContent=j.codigo;$('aviso-codigo').hidden=false;
    try{localStorage.setItem('trollacoRunNombre',j.nombre)}catch(e){}carga();
  }).catch(function(){msg('m-crear','Error de conexión.')})};
$('f-entrar').onsubmit=function(e){e.preventDefault();msg('m-entrar','Entrando...',true);
  var c={nombre:$('e-nombre').value.toUpperCase(),codigo:$('e-codigo').value.toUpperCase().trim()};
  post('perfil',c).then(function(j){if(!j.ok){msg('m-entrar',j.mensaje||'No se ha podido entrar.');return}guarda(c);pinta(j)}).catch(function(){msg('m-entrar','Error de conexión.')})};
$('salir').onclick=function(e){e.preventDefault();guarda(null);pinta(null)};
$('ver-codigo').onclick=function(e){e.preventDefault();var s=$('mi-codigo');s.textContent=s.textContent?'':' · Código: '+yo.codigo};
$('cerrar-aviso').onclick=function(){$('aviso-codigo').hidden=true};

var NOMBRES={run:'🔥 Supera el récord',c1:'1 · La noche Trolloween',c2:'2 · Bar La Verja',c3:'3 · Trollaco Club',c4:'4 · El edificio abandonado'};
var CAPS=[['🧟','La noche Trolloween'],['🍺','Bar La Verja'],['🪩','Trollaco Club'],['🔦','El edificio abandonado']];
function n(x){return Number(x||0).toLocaleString('es-ES')}
function pinta(j){
  $('sin-cuenta').hidden=!!j;$('con-cuenta').hidden=!j;$('stats').hidden=!j;
  if(!j)return;
  var caps=Math.max(j.capitulos||0,parseInt(localStorage.getItem('trollacoHistoria')||'0',10)||0);
  try{if(caps>(parseInt(localStorage.getItem('trollacoHistoria')||'0',10)||0))localStorage.setItem('trollacoHistoria',String(caps))}catch(e){}
  $('yo-n').textContent=j.nombre;
  $('yo-alta').textContent='Jugador desde el '+new Date(j.alta+'T12:00:00').toLocaleDateString('es-ES',{day:'numeric',month:'long',year:'numeric'});
  var pr=j.porra,res=pr.ganada+pr.perdida,pct=res?Math.round(pr.ganada*100/res):0;
  var mejorPuesto=99;Object.keys(j.arcade).forEach(function(m){if(j.arcade[m]&&j.arcade[m].puesto<mejorPuesto)mejorPuesto=j.arcade[m].puesto});
  $('cifras').innerHTML=[
    [n(j.fichas),'🪙 fichas en el monedero'],[j.puesto_fichas+'º','de '+j.jugadores+' en el ranking de fichas'],
    [n(j.partidas),'🕹️ partidas jugadas'],[n(j.fichas_arcade),'fichas ganadas en el arcade'],
    [caps+'/4','📖 capítulos superados'],[mejorPuesto<99?mejorPuesto+'º':'—','🏆 mejor puesto en el arcade']
  ].map(function(c){return '<div class="cifra"><b>'+c[0]+'</b><span>'+c[1]+'</span></div>'}).join('');
  // arcade por modo
  $('t-arcade').innerHTML='<tr><th>Modo</th><th>Mejor marca</th><th>Puesto</th><th>Partidas</th></tr>'+Object.keys(NOMBRES).map(function(m){
    var a=j.arcade[m],p=(j.partidas_modo&&j.partidas_modo[m])||0;
    return '<tr><td>'+NOMBRES[m]+'</td>'+(a?'<td class="n">'+n(a.puntos)+'</td><td>'+(a.puesto===1?'🔥 1º':a.puesto<=3?['','🥇','🥈','🥉'][a.puesto]+' '+a.puesto+'º':a.puesto+'º')+'</td>':'<td class="no">—</td><td class="no">—</td>')+'<td>'+p+'</td></tr>'}).join('');
  // capítulos
  $('caps').innerHTML=CAPS.map(function(c,i){var ok=caps>i;return '<div class="capi'+(ok?' ok':'')+'"><b>'+(ok?c[0]:'🔒')+'</b>'+(i+1)+' · '+c[1]+(ok?'<br>✔ Superado':'')+'</div>'}).join('');
  $('barra-caps').style.width=(caps*25)+'%';
  // porra
  $('cifras-porra').innerHTML=[
    [n(pr.total),'⚽ pronósticos'],[n(pr.ganada),'✔ aciertos'],[pct+'%','de acierto'],[n(pr.mayor),'💰 mayor premio (fichas)'],
    [n(pr.exactos),'🎯 resultados exactos'],[n((j.jornadas||[]).length),'jornadas jugadas']
  ].map(function(c){return '<div class="cifra"><b>'+c[0]+'</b><span>'+c[1]+'</span></div>'}).join('');
  // insignias
  var top10=Object.keys(j.arcade).some(function(m){return j.arcade[m]&&j.arcade[m].puesto<=10});
  var uno=Object.keys(j.arcade).some(function(m){return j.arcade[m]&&j.arcade[m].puesto===1});
  var ins=[
    ['🎟️','Fundador','Cuenta creada en 2026',j.alta<'2027-01-01'],
    ['🧟','Cazazombis','Supera el capítulo 1',caps>=1],['🍺','Sin gritar','Supera el capítulo 2',caps>=2],
    ['🪩','Rey de la pista','Supera el capítulo 3',caps>=3],['🔦','Sin miedo','Supera el capítulo 4',caps>=4],
    ['🕹️','Viciado','Juega 50 partidas',j.partidas>=50],['🪙','Hucha','Llega a 100 fichas',j.fichas>=100],['💰','Ricachón','Llega a 100.000 fichas',j.fichas>=100000],
    ['🏆','Top 10','Entra en un top 10 del arcade',top10],['🔥','Número 1','Sé el primero en un ranking',uno],
    ['⚽','Primer gol','Acierta un pronóstico',pr.ganada>=1],['🔮','Adivino','Acierta 10 pronósticos',pr.ganada>=10],['🎯','Francotirador','Acierta un resultado exacto',pr.exactos>=1]
  ];
  var conseguidas=ins.filter(function(i){return i[3]}).length;
  $('n-ins').textContent=conseguidas+' de '+ins.length;
  $('insignias').innerHTML=ins.map(function(i){return '<div class="ins'+(i[3]?'':' no')+'" title="'+esc(i[2])+'"><i>'+i[0]+'</i><b>'+i[1]+'</b><span>'+i[2]+'</span></div>'}).join('');
  // últimos pronósticos
  var ult=(j.pronosticos||[]).slice(0,5);
  $('ultimos').innerHTML=ult.length?'<table class="modos-t"><tr><th>Jornada</th><th>Pronóstico</th><th>Fichas</th><th>Estado</th></tr>'+ult.map(function(a){
    return '<tr><td>J'+a.jornada+'</td><td>'+esc(a.tipo==='1x2'?a.seleccion:'Exacto '+a.seleccion)+' (x'+Number(a.cuota).toFixed(2)+')</td><td>'+a.cantidad+'</td><td>'+a.estado+(a.estado==='ganada'?' +'+a.premio:'')+'</td></tr>'}).join('')+'</table>'
    :'<p style="color:var(--muted)">Aún no has hecho pronósticos. <a href="/porra/">Ir a La Porra ›</a></p>';
}
function carga(){
  if(!yo){pinta(null);return}
  post('perfil',yo).then(function(j){if(j.ok)pinta(j);else{guarda(null);pinta(null)}}).catch(function(){$('cifras').innerHTML='<p>No se han podido cargar tus datos.</p>'});
}
carga();
if(document.documentElement.className.indexOf('halloween')>-1){document.querySelectorAll('img.troll[data-hw]').forEach(function(i){i.src=i.getAttribute('data-hw')})}
})();
</script>"""

body = """
<main>
  <section class="panel" id="sin-cuenta">
    <h2>Entra o crea tu cuenta</h2>
    <p>Una sola cuenta para todo: el arcade, el modo historia y La Porra. Solo un nombre de 2 a 5 letras y un código secreto. Sin correo ni contraseñas.</p>
    <div class="pestanas"><button type="button" class="on" data-t="crear">CREAR CUENTA</button><button type="button" data-t="entrar">YA TENGO CUENTA</button></div>
    <form id="f-crear">
      <div class="campo"><input id="c-nombre" maxlength="5" placeholder="AAAAA" autocomplete="nickname" aria-label="Nombre"><button class="boton" type="submit">CREAR</button></div>
      <p class="msg" id="m-crear"></p>
    </form>
    <form id="f-entrar" hidden>
      <div class="campo"><input id="e-nombre" maxlength="5" placeholder="NOMBRE" aria-label="Nombre"><input id="e-codigo" maxlength="8" placeholder="CÓDIGO" aria-label="Código secreto" autocomplete="off"><button class="boton" type="submit">ENTRAR</button></div>
      <p class="msg" id="m-entrar"></p>
    </form>
  </section>

  <section id="con-cuenta" hidden>
    <div class="codigo" id="aviso-codigo" hidden>
      <p>🔑 Este es tu <strong>código secreto</strong>. Apúntalo: lo necesitas para entrar desde otro móvil u ordenador. Si lo pierdes, no hay forma de recuperarlo.</p>
      <b id="nuevo-codigo"></b>
      <button type="button" class="boton" id="cerrar-aviso">Ya lo he apuntado</button>
    </div>
    <div class="ficha-jug">
      <img class="troll" src="/img/trollaco-mando.png" data-hw="/img/trollaco-mando-hw.png" alt="">
      <div><div class="nom" id="yo-n"></div><div class="sub2"><span id="yo-alta"></span><span id="mi-codigo"></span></div></div>
      <div class="acc"><a class="boton" href="/arcade/">🕹️ JUGAR</a><a class="boton sec" href="/porra/">⚽ LA PORRA</a></div>
    </div>
    <p style="margin-top:8px;font-size:16px"><a href="#" id="ver-codigo">Ver mi código</a> · <a href="#" id="salir">Cerrar sesión en este dispositivo</a></p>
  </section>

  <div id="stats" hidden>
    <div class="cifras" id="cifras"></div>

    <h2>🏅 Insignias <small style="font-size:.6em;color:var(--muted)" id="n-ins"></small></h2>
    <div class="insignias" id="insignias"></div>

    <h2>📖 Modo historia</h2>
    <div class="caps" id="caps"></div>
    <div class="barra-p"><i id="barra-caps" style="width:0"></i></div>

    <h2>🕹️ Arcade</h2>
    <div class="tabla"><table class="modos-t" id="t-arcade"></table></div>
    <p style="font-size:15px;color:var(--muted);margin-top:6px">Las marcas cuentan cuando juegas con el mismo nombre que tu cuenta.</p>

    <h2>⚽ La Porra</h2>
    <div class="cifras" id="cifras-porra"></div>
    <h3 style="margin-top:18px;font-family:'VT323',monospace;font-weight:400;font-size:24px;color:var(--cyan)">Últimos pronósticos</h3>
    <div class="tabla" id="ultimos"></div>
  </div>

  <p class="ojo">Tu cuenta solo guarda tu nombre de jugador, tus fichas y tus partidas. No pedimos correo ni datos personales. Las fichas son de juego: no se compran ni se canjean por nada.</p>
</main>"""

page = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{hw}
<title>Mi cuenta de jugador | Trollacos</title>
<meta name="description" content="Tus estadísticas en Trollacos: récords del arcade, capítulos del modo historia, fichas, insignias y tus pronósticos de La Porra.">
<meta name="robots" content="noindex">
<link rel="canonical" href="https://trollacos.com/cuenta/">
<meta property="og:title" content="Mi cuenta de jugador | Trollacos">
<meta property="og:image" content="https://trollacos.com/portada.jpg">
<link rel="icon" href="/icono.png">
{style2}
</head>
<body>
<div class="scan"></div>
<nav class="top">
  <a href="/"><img class="px" src="/logo.webp" alt="Trollacos" width="1600" height="161"></a>
  <a href="/arcade/">🕹️ ARCADE</a>
</nav>
<header class="cab">
  <div class="etq">&gt; PLAYER_1 · STATS_</div>
  <h1>Mi cuenta</h1>
  <p class="entradilla">Tus récords, tus capítulos, tus fichas y tus insignias. Todo en un sitio.</p>
</header>
{body}
{foot}
{js}
</body>
</html>
'''
os.makedirs('cuenta', exist_ok=True)
open('cuenta/index.html', 'w').write(page)
print('ok', len(page))
