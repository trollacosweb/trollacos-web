/* Fiesta de las Leyendas Trollacas: confeti cuando entra alguien que lo ha conseguido todo */
(function(){
var LEYENDAS={JAM85:{n:1,f:'27 de noviembre de 2026'}};
window.LEYENDAS_TROLLACAS=LEYENDAS;
var COL=['#ff2bd6','#1ff2ff','#ffd23f','#7cff4f','#ffffff','#a35bff'];
function fiesta(nombre,forzar){
  var L=LEYENDAS[nombre];
  var clave='fiestaLeyenda_'+nombre;
  try{if(!forzar&&sessionStorage.getItem(clave))return;sessionStorage.setItem(clave,'1')}catch(e){}
  if(document.getElementById('fiesta-ley'))return;
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cv=document.createElement('canvas');cv.id='fiesta-ley';
  cv.style.cssText='position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:9998';
  document.body.appendChild(cv);
  var ban=document.createElement('div');
  ban.style.cssText='position:fixed;left:50%;top:18%;transform:translateX(-50%) scale(.6);opacity:0;z-index:9999;background:#07021a;border:3px solid #ffd23f;box-shadow:0 0 0 3px #ff2bd6,0 0 40px rgba(255,210,63,.6);padding:18px 22px;text-align:center;font-family:VT323,monospace;color:#fff;max-width:92vw;width:440px;transition:all .5s cubic-bezier(.2,1.6,.4,1);cursor:pointer';
  ban.innerHTML='<img src="/img/trollaco.png" alt="" width="34" height="56" style="image-rendering:pixelated;width:51px;height:84px;display:block;margin:0 auto 6px">'+
    '<div style="font-size:20px;color:#1ff2ff;letter-spacing:2px">&gt; ¡HA ENTRADO UNA LEYENDA!_</div>'+
    '<div style="font-size:44px;line-height:1;color:#ffd23f;text-shadow:0 0 12px rgba(255,210,63,.7);margin:6px 0">👑 '+nombre+'</div>'+
    '<div style="font-size:24px;line-height:1.1">LEYENDA TROLLACA'+(L?' Nº '+L.n:'')+'</div>'+
    '<div style="font-size:18px;color:#ff2bd6;margin-top:6px">'+(L&&L.n===1?'El primero en conseguir todas las insignias. Respeto máximo.':'Todas las insignias conseguidas. Respeto máximo.')+'</div>'+
    '<div style="font-size:15px;color:#9a8fc0;margin-top:8px">(toca para cerrar)</div>';
  document.body.appendChild(ban);
  requestAnimationFrame(function(){ban.style.opacity='1';ban.style.transform='translateX(-50%) scale(1)'});
  function cerrar(){ban.style.opacity='0';ban.style.transform='translateX(-50%) scale(.6)';setTimeout(function(){ban.remove()},500)}
  ban.onclick=cerrar;setTimeout(cerrar,9000);
  if(reduce){setTimeout(function(){cv.remove()},100);return}
  var c=cv.getContext('2d'),W,H,dpr=Math.min(window.devicePixelRatio||1,2),P=[],t0=performance.now();
  function tam(){W=innerWidth;H=innerHeight;cv.width=W*dpr;cv.height=H*dpr;c.setTransform(dpr,0,0,dpr,0,0)}
  tam();addEventListener('resize',tam);
  function rafaga(x,n){for(var i=0;i<n;i++)P.push({x:x,y:H+10,vx:(Math.random()-.5)*9+(x<W/2?3:-3),vy:-(Math.random()*14+10),s:Math.random()*6+5,
    c:COL[i%COL.length],r:Math.random()*6,vr:(Math.random()-.5)*.3,tipo:Math.random()<.2?'*':'q'})}
  function lluvia(n){for(var i=0;i<n;i++)P.push({x:Math.random()*W,y:-20-Math.random()*H*.5,vx:(Math.random()-.5)*2,vy:Math.random()*2+2,s:Math.random()*6+5,
    c:COL[i%COL.length],r:Math.random()*6,vr:(Math.random()-.5)*.3,tipo:Math.random()<.2?'*':'q'})}
  rafaga(0,90);rafaga(W,90);lluvia(120);
  setTimeout(function(){rafaga(0,60);rafaga(W,60)},1400);
  setTimeout(function(){lluvia(140)},2600);
  function paso(t){
    c.clearRect(0,0,W,H);
    for(var i=P.length-1;i>=0;i--){var p=P[i];p.vy+=.25;p.vy=Math.min(p.vy,4.5);p.vx*=.985;p.x+=p.vx+Math.sin((t/300)+i)*.6;p.y+=p.vy;p.r+=p.vr;
      if(p.y>H+30){P.splice(i,1);continue}
      c.save();c.translate(p.x,p.y);c.rotate(p.r);c.fillStyle=p.c;
      if(p.tipo==='*'){c.fillRect(-p.s/2,-1.5,p.s,3);c.fillRect(-1.5,-p.s/2,3,p.s)}
      else c.fillRect(-p.s/2,-p.s/4,p.s,p.s/2*Math.abs(Math.cos(p.r*2))+1);
      c.restore()}
    if(P.length||t-t0<3000)requestAnimationFrame(paso);else cv.remove();
  }
  requestAnimationFrame(paso);
}
window.fiestaTrollaca=fiesta;
// Si quien navega es una leyenda, fiesta una vez por sesión
try{var yo=JSON.parse(localStorage.getItem('porraCuenta')||'null');
  if(yo&&LEYENDAS[yo.nombre]&&!/\/cuenta\//.test(location.pathname)){
    if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){fiesta(yo.nombre)});else fiesta(yo.nombre)}
}catch(e){}
})();
