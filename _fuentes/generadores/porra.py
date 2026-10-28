import os, json
os.chdir('/home/claude/trollacos-web')
g = open('gta-6/index.html').read()
style = g[g.find('<style>'):g.find('</style>') + 8]
foot = g[g.find('<footer>'):g.find('</footer>') + 9]
extra = r"""
.legal{text-align:center;font-family:'VT323',monospace;font-size:20px;color:#9dffb5;margin-top:10px}
.panel{margin:26px 0 0;padding:18px;border:2px solid var(--cyan);border-radius:12px;background:rgba(31,242,255,.06)}
.panel h2{margin:0 0 10px}
.pestanas{display:flex;gap:8px;margin-bottom:12px}
.pestanas button{flex:1;font-family:'VT323',monospace;font-size:22px;padding:6px;border:2px solid rgba(31,242,255,.4);border-radius:8px;background:none;color:#fff;cursor:pointer}
.pestanas button.on{background:rgba(31,242,255,.18);border-color:var(--cyan)}
.campo{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:8px 0}
.campo input{font-family:'VT323',monospace;font-size:24px;padding:6px 10px;border-radius:6px;border:2px solid var(--cyan);background:#120530;color:#fff;width:min(260px,100%);text-transform:uppercase;letter-spacing:.15em}
.boton{font-family:'VT323',monospace;font-size:22px;padding:7px 16px;border-radius:8px;border:2px solid var(--pink);background:var(--pink);color:#07021a;cursor:pointer}
.boton.sec{background:none;color:#fff;border-color:rgba(255,255,255,.4)}
.boton:disabled{opacity:.5;cursor:default}
.msg{min-height:1.3em;font-size:17px;margin-top:6px}.msg.err{color:#ff8b8b}.msg.ok{color:#9dffb5}
.codigo{margin:10px 0;padding:14px;border:3px dashed var(--yellow);border-radius:10px;text-align:center;background:rgba(255,210,63,.08)}
.codigo b{display:block;font-family:'VT323',monospace;font-size:46px;letter-spacing:.25em;color:var(--yellow)}
.saldo{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.saldo .f{font-family:'VT323',monospace;font-size:34px;color:var(--yellow)}
.saldo .n{font-family:'Righteous',sans-serif;font-size:24px;color:#fff}
.partido{margin:12px 0;padding:14px;border:1px solid rgba(255,43,214,.4);border-radius:10px;background:rgba(255,43,214,.05)}
.partido .cab-p{display:flex;justify-content:space-between;font-family:'VT323',monospace;font-size:18px;color:var(--muted)}
.equipos{display:grid;grid-template-columns:1fr auto 1fr;gap:10px;align-items:center;margin:8px 0}
.eq{display:flex;align-items:center;gap:8px;font-weight:700;color:#fff;font-size:18px}.eq.v{justify-content:flex-end;text-align:right}
.eq img{width:30px;height:30px;object-fit:contain}
.marc{font-family:'VT323',monospace;font-size:30px;color:var(--yellow);text-align:center;min-width:70px}
.op{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.op button{font-family:'VT323',monospace;font-size:20px;padding:6px 4px;border-radius:8px;border:2px solid rgba(31,242,255,.45);background:rgba(31,242,255,.06);color:#fff;cursor:pointer}
.op button b{display:block;font-size:24px;color:var(--yellow)}
.op button.sel{background:var(--cyan);color:#07021a}.op button.sel b{color:#07021a}
.jugar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:10px}
.jugar input{width:90px;font-family:'VT323',monospace;font-size:22px;padding:4px 8px;border-radius:6px;border:2px solid var(--yellow);background:#120530;color:#fff}
.jugar input.g{width:52px;text-align:center}
.jugar label{font-size:16px;color:var(--muted)}
details.exacto{margin-top:8px}details.exacto summary{font-size:16px;color:var(--cyan);cursor:pointer}
.estado-p{font-family:'VT323',monospace;font-size:20px;color:var(--muted);text-align:center;margin-top:6px}
.mios td,.mios th{font-size:16px;padding:6px 8px}
.e-ganada{color:#9dffb5}.e-perdida{color:#ff8b8b}.e-pendiente{color:var(--yellow)}.e-devuelta{color:var(--cyan)}
.ranking ol{list-style:none;counter-reset:p;max-width:520px;margin:0 auto}
.ranking li{display:flex;gap:10px;font-family:'VT323',monospace;font-size:24px;padding:4px 8px;border-bottom:1px dashed rgba(233,230,255,.15);counter-increment:p}
.ranking li::before{content:counter(p) ".";width:2em;color:var(--cyan)}
.ranking li .n{flex:1;color:#fff}.ranking li .p{color:var(--yellow)}
.vacio{text-align:center;color:var(--muted);padding:14px}
.check{padding-left:0;list-style:none}.check li{position:relative;padding:6px 0 6px 30px;font-size:18px}.check li::before{content:'▶';position:absolute;left:4px;color:var(--pink)}
.cancelar{margin-left:6px;font-family:'VT323',monospace;font-size:17px;padding:1px 8px;border-radius:6px;border:1px solid #ff8b8b;background:none;color:#ff8b8b;cursor:pointer}
.jornada-sel{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0 4px}
.jornada-sel button{font-family:'VT323',monospace;font-size:19px;padding:3px 10px;border-radius:6px;border:1px solid rgba(255,255,255,.3);background:none;color:#fff;cursor:pointer}
.jornada-sel button.on{background:rgba(255,43,214,.3);border-color:var(--pink)}
</style>"""
style2 = style.replace('</style>', extra)
hw = "<script>(function(){var d=new Date(),m=d.getMonth(),n=d.getDate();if((m===9&&n>=15)||(m===10&&n<=2))document.documentElement.className+=' halloween'})()</script>"

js = r"""
<script>
(function(){
var API='/api/porra.php',yo=null,datos=null,jornadaVista=null;
try{yo=JSON.parse(localStorage.getItem('porraCuenta')||'null')}catch(e){}
function guardaCuenta(c){yo=c;try{c?localStorage.setItem('porraCuenta',JSON.stringify(c)):localStorage.removeItem('porraCuenta')}catch(e){}}
function $(id){return document.getElementById(id)}
function esc(t){return String(t==null?'':t).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function post(accion,cuerpo){return fetch(API+'?accion='+accion,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(cuerpo)}).then(function(r){return r.json()})}
function msg(id,t,ok){var m=$(id);m.textContent=t||'';m.className='msg '+(ok?'ok':'err')}

// ---------- cuenta ----------
document.querySelectorAll('.pestanas button').forEach(function(b){b.onclick=function(){
  document.querySelectorAll('.pestanas button').forEach(function(x){x.classList.toggle('on',x===b)});
  $('f-crear').hidden=b.dataset.t!=='crear';$('f-entrar').hidden=b.dataset.t!=='entrar';}});
function limpiaNombre(inp){inp.addEventListener('input',function(){var v=inp.value.replace(/[^0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ]/g,'').slice(0,5);if(v!==inp.value)inp.value=v})}
limpiaNombre($('c-nombre'));limpiaNombre($('e-nombre'));
$('f-crear').onsubmit=function(e){e.preventDefault();msg('m-crear','Creando...',true);
  post('registrar',{nombre:$('c-nombre').value}).then(function(j){
    if(!j.ok){msg('m-crear',j.mensaje||'No se ha podido crear.');return}
    guardaCuenta({nombre:j.nombre,codigo:j.codigo});
    $('nuevo-codigo').textContent=j.codigo;$('aviso-codigo').hidden=false;cargaYo();
  }).catch(function(){msg('m-crear','Error de conexión.')})};
$('f-entrar').onsubmit=function(e){e.preventDefault();msg('m-entrar','Entrando...',true);
  var c={nombre:$('e-nombre').value.toUpperCase(),codigo:$('e-codigo').value.toUpperCase().trim()};
  post('yo',c).then(function(j){if(!j.ok){msg('m-entrar',j.mensaje||'No se ha podido entrar.');return}guardaCuenta(c);pintaYo(j)}).catch(function(){msg('m-entrar','Error de conexión.')})};
$('salir').onclick=function(){if(confirmaSalir()){guardaCuenta(null);pintaYo(null)}};
function confirmaSalir(){return true}
$('ver-codigo').onclick=function(){var s=$('mi-codigo');s.textContent=s.textContent?'':' Tu código: '+yo.codigo}
$('cerrar-aviso').onclick=function(){$('aviso-codigo').hidden=true};
$('copiar-codigo').onclick=function(){try{navigator.clipboard.writeText(yo.codigo);$('copiar-codigo').textContent='¡Copiado!'}catch(e){}};

function pintaYo(j){
  $('sin-cuenta').hidden=!!j;$('con-cuenta').hidden=!j;
  if(!j){pintaPartidos();pintaMios(null);return}
  $('yo-n').textContent=j.nombre;$('yo-f').textContent='🪙 '+j.fichas+' fichas';$('yo-a').textContent=j.aciertos+' aciertos';
  pintaMios(j);pintaPartidos(j);
}
var ultimoYo=null;
function cargaYo(){if(!yo){pintaYo(null);return}
  post('yo',yo).then(function(j){if(j.ok){ultimoYo=j;pintaYo(j)}else{guardaCuenta(null);pintaYo(null)}}).catch(function(){})}

// ---------- partidos ----------
function fecha(iso){try{return new Date(iso).toLocaleString('es-ES',{weekday:'short',day:'numeric',month:'short',hour:'2-digit',minute:'2-digit',timeZone:'Europe/Madrid'})}catch(e){return iso}}
function abierto(p){return (p.estado==='SCHEDULED'||p.estado==='TIMED')&&new Date(p.fecha).getTime()-300000>Date.now()}
function estadoTxt(p){return {FINISHED:'Final',IN_PLAY:'En juego',PAUSED:'Descanso',POSTPONED:'Aplazado',SUSPENDED:'Suspendido',CANCELLED:'Cancelado'}[p.estado]||'Cerrado'}
function pintaPartidos(j){
  j=j||ultimoYo;var cont=$('partidos');
  if(!datos||!datos.partidos||!datos.partidos.length){cont.innerHTML='<p class="vacio">Los partidos de LaLiga aparecerán aquí en cuanto se conecte el calendario. ¡Vuelve pronto!</p>';$('jornadas').innerHTML='';return}
  var js=[];datos.partidos.forEach(function(p){if(js.indexOf(p.j)<0)js.push(p.j)});js.sort(function(a,b){return a-b});
  if(jornadaVista==null)jornadaVista=datos.jornada;
  $('jornadas').innerHTML=js.map(function(n){return '<button type="button" data-j="'+n+'" class="'+(n===jornadaVista?'on':'')+'">Jornada '+n+'</button>'}).join('');
  $('jornadas').querySelectorAll('button').forEach(function(b){b.onclick=function(){jornadaVista=+b.dataset.j;pintaPartidos()}});
  var mias={};if(j&&j.pronosticos)j.pronosticos.forEach(function(a){(mias[a.partido]=mias[a.partido]||[]).push(a)});
  cont.innerHTML=datos.partidos.filter(function(p){return p.j===jornadaVista}).map(function(p){
    var ab=abierto(p),res=(p.gl!=null&&p.gv!=null)?p.gl+' - '+p.gv:'vs',m=mias[p.id]||[];
    var hecho=m.map(function(a){return '<div class="estado-p">Tu pronóstico: <b>'+esc(a.tipo==='1x2'?(a.seleccion==='1'?p.local.n:a.seleccion==='2'?p.visit.n:'Empate'):'exacto '+a.seleccion)+'</b> · '+a.cantidad+' fichas · <span class="e-'+a.estado+'">'+a.estado+(a.estado==='ganada'?' (+'+a.premio+')':'')+'</span>'+((ab&&a.estado==='pendiente')?' <button type="button" class="cancelar" data-cancel="'+esc(a.id)+'">✖ Cancelar</button>':'')+'</div>'}).join('');
    var tiene1=m.some(function(a){return a.tipo==='1x2'}),tieneE=m.some(function(a){return a.tipo==='exacto'});
    var form='';
    if(ab&&yo){form=(tiene1?'':'<div class="op">'+['1','X','2'].map(function(s){return '<button type="button" data-s="'+s+'">'+(s==='1'?esc(p.local.n):s==='2'?esc(p.visit.n):'Empate')+'<b>x'+p.cuotas[s].toFixed(2)+'</b></button>'}).join('')+'</div>')+
      (tieneE?'':'<details class="exacto"'+(tiene1?' open':'')+'><summary>¿Te atreves con el resultado exacto? (paga x8)</summary><div class="jugar"><input class="g" type="number" min="0" max="15" placeholder="'+esc(p.local.tla||'L')+'" data-gl> - <input class="g" type="number" min="0" max="15" placeholder="'+esc(p.visit.tla||'V')+'" data-gv></div></details>')+
      ((tiene1&&tieneE)?'':'<div class="jugar"><label>Fichas</label><input type="number" min="1" value="10" data-c><button type="button" class="boton" data-ir>PRONOSTICAR</button></div><p class="msg" data-m></p>');}
    else if(ab&&!yo){form='<p class="estado-p">Crea tu cuenta arriba para participar.</p>'}
    else{form='<p class="estado-p">'+estadoTxt(p)+'</p>'}
    return '<div class="partido" data-id="'+p.id+'"><div class="cab-p"><span>'+fecha(p.fecha)+'</span><span>'+(ab?'Abierto':estadoTxt(p))+'</span></div>'+
      '<div class="equipos"><div class="eq">'+(p.local.c?'<img src="'+esc(p.local.c)+'" alt="" loading="lazy" referrerpolicy="no-referrer">':'')+esc(p.local.n)+'</div><div class="marc">'+res+'</div><div class="eq v">'+esc(p.visit.n)+(p.visit.c?'<img src="'+esc(p.visit.c)+'" alt="" loading="lazy" referrerpolicy="no-referrer">':'')+'</div></div>'+form+hecho+'</div>'}).join('');
  cont.querySelectorAll('.partido').forEach(function(card){
    var sel=null;card.querySelectorAll('.op button').forEach(function(b){b.onclick=function(){sel=sel===b.dataset.s?null:b.dataset.s;card.querySelectorAll('.op button').forEach(function(x){x.classList.toggle('sel',x.dataset.s===sel)})}});
    var ir=card.querySelector('[data-ir]');if(!ir)return;
    ir.onclick=function(){
      var m=card.querySelector('[data-m]'),c=+card.querySelector('[data-c]').value,gl=card.querySelector('[data-gl]'),gv=card.querySelector('[data-gv]');
      var exacto=gl&&gv&&gl.value!==''&&gv.value!=='';
      if(!sel&&!exacto){m.className='msg err';m.textContent='Elige 1, X o 2, o pon un resultado exacto.';return}
      if(!(c>=1)){m.className='msg err';m.textContent='Pon cuántas fichas juegas.';return}
      var pedidos=[];if(sel)pedidos.push({tipo:'1x2',seleccion:sel});if(exacto)pedidos.push({tipo:'exacto',seleccion:(+gl.value)+'-'+(+gv.value)});
      ir.disabled=true;m.className='msg ok';m.textContent='Guardando...';
      var cadena=Promise.resolve(null),ultimo=null,bono=0;
      pedidos.forEach(function(pd){cadena=cadena.then(function(){return post('apostar',{nombre:yo.nombre,codigo:yo.codigo,partido:card.dataset.id,tipo:pd.tipo,seleccion:pd.seleccion,cantidad:c}).then(function(j){if(!j.ok)throw new Error(j.mensaje||'No se ha podido guardar.');ultimo=j;bono+=j.bono||0})})});
      cadena.then(function(){ultimoYo=ultimo;pintaYo(ultimo);cargaRanking();if(bono)alertaBono(bono)}).catch(function(err){ir.disabled=false;m.className='msg err';m.textContent=err.message;cargaYo()});
    };
  });
}
document.addEventListener('click',function(ev){var b=ev.target.closest&&ev.target.closest('[data-cancel]');if(!b||!yo)return;
  b.disabled=true;b.textContent='Cancelando...';
  post('cancelar',{nombre:yo.nombre,codigo:yo.codigo,id:b.dataset.cancel}).then(function(j){
    if(!j.ok){b.disabled=false;b.textContent='✖ Cancelar';alert(j.mensaje||'No se ha podido cancelar.');return}
    ultimoYo=j;pintaYo(j);cargaRanking();var a=$('bono');a.textContent='↩️ Pronóstico cancelado: te devolvemos '+j.devueltas+' fichas';a.hidden=false;setTimeout(function(){a.hidden=true},4000);
  }).catch(function(){b.disabled=false;b.textContent='✖ Cancelar'})});
function alertaBono(b){var a=$('bono');a.textContent='🎁 +'+b+' fichas por participar en esta jornada';a.hidden=false;setTimeout(function(){a.hidden=true},5000)}

// ---------- mis pronósticos y ranking ----------
function nombrePartido(id){if(!datos)return id;for(var i=0;i<datos.partidos.length;i++){var p=datos.partidos[i];if(String(p.id)===String(id))return p.local.n+' - '+p.visit.n}return 'Partido '+id}
function pintaMios(j){var t=$('mios');
  if(!j){t.innerHTML='<p class="vacio">Entra con tu cuenta para ver tus pronósticos.</p>';return}
  if(!j.pronosticos.length){t.innerHTML='<p class="vacio">Aún no has hecho ningún pronóstico. ¡Elige un partido!</p>';return}
  t.innerHTML='<div class="tabla"><table class="mios"><tr><th>Partido</th><th>Pronóstico</th><th>Fichas</th><th>Estado</th></tr>'+j.pronosticos.map(function(a){
    return '<tr><td>J'+a.jornada+' · '+esc(nombrePartido(a.partido))+'</td><td>'+esc(a.tipo==='1x2'?a.seleccion:'Exacto '+a.seleccion)+' (x'+Number(a.cuota).toFixed(2)+')</td><td>'+a.cantidad+'</td><td class="e-'+a.estado+'">'+a.estado+(a.estado==='ganada'?' +'+a.premio:'')+'</td></tr>'}).join('')+'</table></div>'}
function cargaRanking(){fetch(API+'?accion=ranking',{cache:'no-store'}).then(function(r){return r.json()}).then(function(j){
  var ol=$('ranking');if(!j.top||!j.top.length){ol.innerHTML='<li class="vacio" style="list-style:none">Todavía no hay jugadores. ¡Sé el primero!</li>';return}
  ol.innerHTML=j.top.map(function(u){return '<li><span class="n">'+esc(u.nombre)+'</span><span class="p">'+u.fichas+' 🪙</span></li>'}).join('');
  $('jugadores').textContent=j.jugadores+(j.jugadores===1?' jugador':' jugadores')+' en la Porra';}).catch(function(){})}

fetch('/api/partidos.json',{cache:'no-store'}).then(function(r){return r.json()}).then(function(j){datos=j;cargaYo();pintaPartidos()}).catch(function(){datos=null;cargaYo();pintaPartidos()});
cargaRanking();
if(document.documentElement.className.indexOf('halloween')>-1){document.querySelectorAll('img.troll[data-hw]').forEach(function(i){i.src=i.getAttribute('data-hw')})}
})();
</script>"""

body = """
<main>
  <p class="legal">⚠️ JUEGO SIN DINERO REAL · Las fichas se ganan jugando y no se compran ni se canjean por nada</p>

  <section class="panel" id="cuenta">
    <div id="sin-cuenta">
      <h2>Tu monedero de fichas</h2>
      <div class="pestanas"><button type="button" class="on" data-t="crear">CREAR CUENTA</button><button type="button" data-t="entrar">YA TENGO CUENTA</button></div>
      <form id="f-crear">
        <p>Elige un nombre de 2 a 5 letras o números, estilo recreativa. Te regalamos <b>10 fichas</b> para empezar.</p>
        <div class="campo"><input id="c-nombre" maxlength="5" placeholder="AAAAA" autocomplete="nickname" aria-label="Nombre"><button class="boton" type="submit">CREAR</button></div>
        <p class="msg" id="m-crear"></p>
      </form>
      <form id="f-entrar" hidden>
        <p>Pon tu nombre y tu código secreto para entrar desde este dispositivo.</p>
        <div class="campo"><input id="e-nombre" maxlength="5" placeholder="NOMBRE" aria-label="Nombre"><input id="e-codigo" maxlength="8" placeholder="CÓDIGO" aria-label="Código secreto" autocomplete="off"><button class="boton" type="submit">ENTRAR</button></div>
        <p class="msg" id="m-entrar"></p>
      </form>
    </div>
    <div id="con-cuenta" hidden>
      <div class="codigo" id="aviso-codigo" hidden>
        <p>🔑 Este es tu <strong>código secreto</strong>. Apúntalo: lo necesitas para entrar desde otro móvil u ordenador. Si lo pierdes, no hay forma de recuperarlo.</p>
        <b id="nuevo-codigo"></b>
        <button type="button" class="boton sec" id="copiar-codigo">Copiar</button> <button type="button" class="boton" id="cerrar-aviso">Ya lo he apuntado</button>
      </div>
      <div class="saldo"><div><span class="n" id="yo-n"></span> · <span id="yo-a"></span><span id="mi-codigo"></span></div><div class="f" id="yo-f"></div></div>
      <p style="margin-top:8px">¿Quieres más fichas? <a href="/arcade/">Juega a Trollaco Run</a>: cada ficha que cojas va a tu monedero. · <a href="#" id="ver-codigo" onclick="return false">Ver mi código</a> · <a href="#" id="salir" onclick="return false">Salir</a></p>
    </div>
    <p class="msg ok" id="bono" hidden></p>
  </section>

  <h2 id="jornada">⚽ La jornada de LaLiga</h2>
  <div class="jornada-sel" id="jornadas"></div>
  <div id="partidos"><p class="vacio">Cargando partidos...</p></div>

  <h2 id="mis">📋 Mis pronósticos</h2>
  <div id="mios"></div>

  <h2 id="clasificacion">🏆 Los más ricos en fichas</h2>
  <div class="ranking"><ol id="ranking"></ol><p class="vacio" id="jugadores"></p></div>

  <h2 id="como">¿Cómo funciona?</h2>
  <ul class="check">
    <li>Creas tu cuenta con un nombre de 5 letras y te damos <b>10 fichas</b>. Guarda tu código secreto para entrar desde otros dispositivos.</li>
    <li><b>Ganas fichas jugando a <a href="/arcade/">Trollaco Run</a></b>: cada ficha que recoges en una partida va a tu monedero.</li>
    <li>Por <b>participar en cada jornada</b> te llevas <b>10 fichas extra</b> con tu primer pronóstico.</li>
    <li>En cada partido puedes jugar fichas al <b>1, X o 2</b> y, si te atreves, al <b>resultado exacto</b>, que paga x8.</li>
    <li>¿Te has arrepentido? Puedes <b>cancelar un pronóstico</b> y recuperar tus fichas hasta 5 minutos antes del partido.</li>
    <li>Los pronósticos se cierran 5 minutos antes de cada partido. Cuando termina, las fichas se reparten solas.</li>
    <li>Las cuotas las calculamos nosotros según la clasificación. No son de ninguna casa de apuestas.</li>
  </ul>
  <p class="ojo">La Porra Trollaca es un juego de pronósticos para pasar el rato. <strong>No se juega dinero</strong>: las fichas no se pueden comprar, vender ni cambiar por premios, y no tienen ningún valor fuera de esta web. Trollacos no tiene relación con LaLiga ni con ningún club. Datos de partidos: TheSportsDB.</p>
</main>"""

page = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{hw}
<title>La Porra Trollaca: pronósticos de LaLiga con fichas (sin dinero) | Trollacos</title>
<meta name="description" content="Juega a pronosticar los partidos de LaLiga con las fichas que ganas en nuestro arcade. Sin dinero real: solo por el pique y el ranking.">
<link rel="canonical" href="https://trollacos.com/porra/">
<meta property="og:title" content="La Porra Trollaca: ¿cuánto sabes de LaLiga?">
<meta property="og:description" content="Gana fichas en el arcade y pronostica la jornada. Sin dinero real, solo por el pique.">
<meta property="og:url" content="https://trollacos.com/porra/">
<meta property="og:image" content="https://trollacos.com/porra/portada.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/icono.png">
{style2}
</head>
<body>
<div class="scan"></div>
<nav class="top">
  <a href="/"><img class="px" src="/logo.webp" alt="Trollacos" width="1600" height="161"></a>
  <a href="/cuenta/">👤 MI CUENTA</a>
</nav>
<header class="cab">
  <div class="etq">&gt; PRONÓSTICOS · LALIGA_</div>
  <h1>La Porra Trollaca</h1>
  <p class="entradilla">Gana fichas en el arcade, pronostica la jornada y presume en el ranking. Sin dinero de por medio: aquí solo se juega el orgullo.</p>
  <div class="troll-cab" aria-hidden="true"><img class="px troll" src="/img/trollaco-mando.png" data-hw="/img/trollaco-mando-hw.png" alt=""></div>
</header>
{body}
{foot}
{js}
</body>
</html>
'''
os.makedirs('porra', exist_ok=True)
open('porra/index.html', 'w').write(page)
print('ok', len(page))
