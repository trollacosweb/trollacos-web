import json, html, sys
sys.path.insert(0, '/home/claude/trollaco/misterio')
from casos import CASOS, PROXIMOS

def nivel(n):
    return ''.join('<span class="on">👽</span>' if i < n else '<span class="off">👽</span>' for i in range(5))

def margen(c):
    lado = c['lado']
    if c['pose'] == 'ovni':
        fig = ('<div class="abduccion"><img class="px ovni" src="img/ovni.png" alt=""><span class="rayo"></span>'
               '<img class="px tr sube" src="img/trollaco-asustado.png" alt=""></div>')
    else:
        extra = {'asustado': ' tiembla', 'fantasma': ' flota', 'camara': ' flash', 'linterna': ' luz', 'lupa': ' mira', 'expediente': ' lee'}[c['pose']]
        fig = f'<img class="px tr{extra}" src="img/trollaco-{c["pose"]}.png" alt="">'
    return f'<div class="margen {lado}" aria-hidden="true">{fig}</div>'

casos_html = []
for i, c in enumerate(CASOS, 1):
    casos_html.append(f'''
<article class="caso" id="{c['id']}">
  {margen(c)}
  <div class="sello">EXPEDIENTE {i:02d}</div>
  <h2>{c['titulo']}</h2>
  <p class="subt">{c['sub']}</p>
  <figure class="ilus"><img src="img/{c['img']}.svg" alt="Ilustración de {html.escape(c['titulo'])}" loading="lazy" width="600" height="340"></figure>
  <ul class="ficha">
    <li><b>📍 Dónde</b>{c['lugar']}</li>
    <li><b>🕰️ Cuándo</b>{c['cuando']}</li>
    {'' if c['metro'] in ('—','') else '<li><b>🚇 Cómo llegar</b>' + c['metro'] + '</li>'}
    <li><b>Nivel de misterio</b><span class="nivel" aria-label="{c['nivel']} de 5">{nivel(c['nivel'])}</span></li>
  </ul>
  <div class="relato">{c['texto']}</div>
  <div class="esceptico"><b>🔬 LO QUE DICEN LOS ESCÉPTICOS</b><p>{c['esceptico']}</p></div>
  <div class="opina"><img class="px" src="/img/trollaco.png" data-hw="/img/trollaco-hw.png" alt=""><p><b>EL TROLLACO OPINA:</b> {c['trollaco']}</p></div>
  <p class="volver"><a href="#mapa">↑ Volver al mapa</a></p>
</article>''')

puntos = [dict(id=c['id'], t=c['titulo'], s=c['sub'], lat=c['lat'], lng=c['lng'], i=c['icono'], aprox=c.get('aprox', False), f=c.get('fuera', False)) for c in CASOS]
indice = '\n'.join(f'      <li><a href="#{c["id"]}"><span>{c["icono"]}</span>{c["titulo"]}</a></li>' for c in CASOS)
prox = '\n'.join(
    f'''    <div class="prox-col"><h3>{zona}</h3>''' + ''.join(f'<div class="prox"><b>{t}</b><span>{d}</span></div>' for t, d in items) + '</div>'
    for zona, items in PROXIMOS)

ld = {"@context": "https://schema.org", "@type": "Article",
      "headline": "Lugares encantados de Madrid: 7 casos paranormales con mapa",
      "datePublished": "2026-10-23", "dateModified": "2026-10-23", "inLanguage": "es",
      "author": {"@type": "Organization", "name": "Trollacos"},
      "publisher": {"@type": "Organization", "name": "Trollacos", "logo": {"@type": "ImageObject", "url": "https://trollacos.com/icono-512.png"}},
      "mainEntityOfPage": "https://trollacos.com/misterio/",
      "about": [c['titulo'] for c in CASOS]}

page = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>(function(){{var d=new Date(),m=d.getMonth(),n=d.getDate();if((m===9&&n>=15)||(m===10&&n<=2))document.documentElement.className+=' halloween'}})()</script>
<title>Lugares encantados de Madrid: 7 casos paranormales con mapa | Expediente Trollaco</title>
<meta name="description" content="El Palacio de Linares, la Casa de las Siete Chimeneas, el Ángel Caído, la estación fantasma de Chamberí, el caso Ummo y el caso Vallecas. Los misterios de Madrid, con mapa interactivo.">
<link rel="canonical" href="https://trollacos.com/misterio/">
<meta property="og:type" content="article">
<meta property="og:title" content="Expediente Trollaco: el Madrid que da miedo">
<meta property="og:description" content="7 lugares de Madrid con historia oscura, en un mapa interactivo. ¿Te atreves?">
<meta property="og:url" content="https://trollacos.com/misterio/">
<meta property="og:image" content="https://trollacos.com/misterio/portada.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/icono.png">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<style>
@font-face{{font-family:'Righteous';src:url(/fuentes/righteous.woff2) format('woff2');font-display:swap}}
@font-face{{font-family:'VT323';src:url(/fuentes/vt323.woff2) format('woff2');font-display:swap}}
@font-face{{font-family:'Rajdhani';src:url(/fuentes/rajdhani-500.woff2) format('woff2');font-weight:500;font-display:swap}}
@font-face{{font-family:'Rajdhani';src:url(/fuentes/rajdhani-700.woff2) format('woff2');font-weight:700;font-display:swap}}
:root{{--bg:#04020c;--verde:#7cffb2;--pink:#ff2bd6;--cyan:#1ff2ff;--yellow:#ffd23f;--orange:#ff9d3c;--text:#e6e3f5;--muted:#9f98c4;--papel:#d9c9a0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--text);font-family:'Rajdhani',sans-serif;font-weight:500;font-size:19.5px;line-height:1.6;overflow-x:hidden}}
body::before{{content:"";position:fixed;inset:0;pointer-events:none;z-index:40;background:repeating-linear-gradient(0deg,rgba(0,0,0,.18) 0 1px,transparent 1px 3px)}}
a{{color:var(--verde)}}
.px{{image-rendering:pixelated;image-rendering:crisp-edges}}
.top{{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:14px 18px;border-bottom:2px solid var(--verde);box-shadow:0 4px 22px rgba(124,255,178,.18);position:relative;z-index:5;background:var(--bg)}}
.top a{{font-family:'VT323',monospace;font-size:22px;text-decoration:none;color:#fff;text-shadow:0 0 6px var(--verde)}}
.top img{{height:26px;width:auto;display:block}}
/* portada */
.cab{{position:relative;text-align:center;padding:70px 16px 60px;overflow:hidden;background:radial-gradient(ellipse at 50% 120%,#173b2c 0%,#081a14 30%,var(--bg) 70%)}}
.niebla{{position:absolute;left:-20%;right:-20%;bottom:-10px;height:160px;background:radial-gradient(ellipse at 30% 60%,rgba(190,220,210,.18),transparent 60%),radial-gradient(ellipse at 75% 70%,rgba(190,220,210,.14),transparent 60%);animation:niebla 18s ease-in-out infinite alternate;pointer-events:none}}
@keyframes niebla{{to{{transform:translateX(8%)}}}}
.cab .k{{font-family:'VT323',monospace;font-size:22px;letter-spacing:.2em;color:var(--verde);text-shadow:0 0 10px var(--verde)}}
.cab h1{{font-family:'Righteous',sans-serif;font-weight:400;font-size:clamp(38px,9vw,74px);line-height:1;margin:12px auto 16px;color:#eafff3;text-shadow:0 0 18px rgba(124,255,178,.55),0 0 40px rgba(124,255,178,.25);animation:parpadeo 7s infinite}}
@keyframes parpadeo{{0%,91%,100%{{opacity:1}}92%{{opacity:.4}}93%{{opacity:1}}95%{{opacity:.6}}96%{{opacity:1}}}}
.cab .ent{{max-width:680px;margin:0 auto;font-size:21px;color:#d8d4ee}}
.cab .tr-cab{{position:absolute;left:6%;bottom:18px;width:120px}}
.cab .ovni-cab{{position:absolute;top:30px;width:90px;animation:sobrevuela 16s linear infinite}}
@keyframes sobrevuela{{0%{{left:-120px;transform:translateY(0)}}50%{{transform:translateY(24px)}}100%{{left:110%;transform:translateY(0)}}}}
@media (max-width:760px){{.cab .tr-cab{{position:static;display:block;margin:20px auto 0;width:84px}}}}
main{{max-width:860px;margin:0 auto;padding:0 18px 60px;position:relative}}
.aviso{{margin:28px 0 0;padding:14px 18px;border-left:4px solid var(--orange);background:rgba(255,157,60,.08);font-size:17px;color:#e8dcc8}}
/* mapa */
h2.sec{{font-family:'Righteous',sans-serif;font-weight:400;font-size:clamp(28px,6vw,40px);color:var(--verde);text-shadow:0 0 12px rgba(124,255,178,.5);margin:46px 0 10px;scroll-margin-top:10px}}
#mapa-madrid{{height:min(70vh,520px);border:2px solid var(--verde);border-radius:12px;box-shadow:0 0 26px rgba(124,255,178,.25);background:#0b0b14}}
.leaflet-container{{font-family:'Rajdhani',sans-serif}}
.leaflet-tile-pane{{filter:invert(1) hue-rotate(180deg) brightness(.8) contrast(.95) saturate(.6)}}
.pin{{font-size:26px;line-height:1;filter:drop-shadow(0 0 6px #7cffb2) drop-shadow(0 2px 2px #000);animation:latido 2.4s ease-in-out infinite}}
@keyframes latido{{50%{{transform:scale(1.15)}}}}
.leaflet-popup-content-wrapper{{background:#0c0a1c;color:var(--text);border:1px solid var(--verde);border-radius:10px}}
.leaflet-popup-tip{{background:#0c0a1c}}
.leaflet-popup-content b{{font-family:'Righteous',sans-serif;font-weight:400;font-size:18px;color:#eafff3;display:block}}
.leaflet-popup-content i{{display:block;color:var(--muted);margin:2px 0 8px}}
.leaflet-popup-content a{{font-family:'VT323',monospace;font-size:20px;color:var(--verde)}}
.indice{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:8px;list-style:none;margin:14px 0 0}}
.indice a{{display:flex;gap:10px;align-items:center;padding:9px 12px;border:1px solid rgba(124,255,178,.3);border-radius:8px;text-decoration:none;color:#fff;background:rgba(124,255,178,.04)}}
.indice a:hover{{background:rgba(124,255,178,.12)}}
/* casos */
.caso{{position:relative;margin:70px 0 0;padding-top:10px;scroll-margin-top:10px}}
.sello{{display:inline-block;font-family:'VT323',monospace;font-size:20px;letter-spacing:.15em;color:#ff5a5a;border:2px solid #ff5a5a;padding:0 10px;transform:rotate(-3deg);opacity:.85}}
.caso h2{{font-family:'Righteous',sans-serif;font-weight:400;font-size:clamp(30px,6.5vw,44px);line-height:1.08;color:#fff;margin:10px 0 2px;text-shadow:0 0 14px rgba(124,255,178,.3)}}
.subt{{font-family:'VT323',monospace;font-size:24px;color:var(--verde);margin-bottom:14px}}
.ilus img{{width:100%;height:auto;display:block;border-radius:10px;border:1px solid rgba(124,255,178,.25);box-shadow:0 10px 30px rgba(0,0,0,.6)}}
.ficha{{list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:8px 16px;margin:16px 0 18px;padding:14px 16px;background:var(--papel);color:#2a1f10;border-radius:4px;box-shadow:4px 4px 0 rgba(0,0,0,.4);font-size:17px}}
.ficha b{{display:block;font-family:'VT323',monospace;font-weight:400;font-size:18px;color:#7a1c1c}}
.nivel .off{{filter:grayscale(1);opacity:.25}}
.relato p{{margin:0 0 16px}}
.relato p:first-child::first-letter{{font-family:'Righteous',sans-serif;float:left;font-size:58px;line-height:.9;margin:6px 10px 0 0;color:var(--verde);text-shadow:0 0 12px rgba(124,255,178,.6)}}
.relato strong{{color:#fff}}
.esceptico{{margin:20px 0 14px;padding:14px 16px;border:1px dashed rgba(31,242,255,.55);border-radius:8px;background:rgba(31,242,255,.05)}}
.esceptico b{{font-family:'VT323',monospace;font-weight:400;font-size:21px;color:var(--cyan)}}
.esceptico p{{margin:6px 0 0;font-size:17.5px;color:#cfd9ea}}
.opina{{display:flex;gap:14px;align-items:center;padding:12px 16px;border:2px dashed rgba(124,255,178,.5);border-radius:8px;background:rgba(124,255,178,.06)}}
.opina img{{width:40px;height:auto;flex:none}}
.opina p{{margin:0;font-family:'VT323',monospace;font-size:21px;line-height:1.15;color:#c9ffd4}}
.volver{{text-align:right;margin-top:10px;font-family:'VT323',monospace;font-size:20px}}
.volver a{{text-decoration:none}}
/* Trollaco en los márgenes */
.margen{{position:absolute;top:130px;width:140px;z-index:2;pointer-events:none}}
.margen.izq{{left:-200px}}.margen.der{{right:-200px}}
.margen img.tr{{width:140px;height:auto;display:block}}
@media (max-width:1300px){{.margen{{position:relative;top:auto;left:auto!important;right:auto!important;float:right;width:72px;margin:0 0 6px 12px}}.margen img.tr{{width:72px}}.margen.izq{{float:left;margin:0 12px 6px 0}}}}
.tiembla{{animation:tiembla .25s linear infinite}}
@keyframes tiembla{{25%{{transform:translate(-1px,1px)}}50%{{transform:translate(1px,-1px)}}75%{{transform:translate(-1px,-1px)}}}}
.flota{{animation:flota 3s ease-in-out infinite}}
@keyframes flota{{50%{{transform:translateY(-12px)}}}}
.mira{{animation:mira 4s ease-in-out infinite}}
@keyframes mira{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(-6px) rotate(-3deg)}}}}
.lee{{animation:lee 5s ease-in-out infinite}}
@keyframes lee{{0%,80%,100%{{transform:none}}85%{{transform:translateY(-3px)}}}}
.flash{{animation:flash 3.5s infinite}}
@keyframes flash{{0%,88%,100%{{filter:none}}90%{{filter:brightness(2.4) drop-shadow(0 0 20px #fff)}}}}
.luz{{filter:drop-shadow(0 0 8px rgba(255,236,120,.6))}}
.margen.der .luz{{transform:scaleX(-1)}}
.margen.der:has(.luz)::after{{content:"";position:absolute;top:34%;right:100%;width:160px;height:90px;transform:translateY(-30%);
  background:linear-gradient(270deg,rgba(255,236,120,.35),rgba(255,236,120,0));clip-path:polygon(100% 42%,0 0,0 100%,100% 58%);animation:linterna 3s ease-in-out infinite}}
@keyframes linterna{{50%{{opacity:.5}}}}
@media (max-width:1300px){{.margen.der:has(.luz)::after{{display:none}}}}
.abduccion{{position:relative;width:140px;height:250px}}
.abduccion .ovni{{position:absolute;top:0;left:0;width:140px;z-index:1}}
.abduccion .rayo{{position:absolute;top:56px;left:32px;width:76px;height:190px;background:linear-gradient(180deg,rgba(159,246,255,.55),rgba(159,246,255,.05));clip-path:polygon(35% 0,65% 0,100% 100%,0 100%)}}
.abduccion .sube{{position:absolute;left:24px;bottom:0;width:92px;animation:sube 4s ease-in-out infinite}}
@keyframes sube{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-60px) rotate(8deg)}}}}
@media (max-width:1300px){{.abduccion{{width:72px;height:140px}}.abduccion .ovni{{width:72px}}.abduccion .rayo{{top:28px;left:16px;width:40px;height:110px}}.abduccion .sube{{width:54px;left:9px}}}}
/* próximamente */
.prox-wrap{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-top:10px}}
.prox-col h3{{font-family:'VT323',monospace;font-weight:400;font-size:24px;color:var(--orange);margin-bottom:8px}}
.prox{{padding:10px 14px;margin-bottom:8px;border:1px solid rgba(255,157,60,.35);border-radius:8px;background:rgba(255,157,60,.05)}}
.prox b{{display:block;color:#fff}}.prox span{{font-size:16px;color:var(--muted)}}
.compartir{{margin:40px 0 0;padding:16px;border:2px solid var(--verde);border-radius:8px;text-align:center;background:rgba(124,255,178,.05)}}
.compartir b{{display:block;font-family:'VT323',monospace;font-weight:400;font-size:21px;color:var(--verde);margin-bottom:10px}}
.compartir a,.compartir button{{display:inline-block;margin:4px;padding:7px 14px;border:1px solid var(--verde);border-radius:6px;color:#fff;text-decoration:none;background:none;font:inherit;font-size:17px;cursor:pointer}}
.nota{{font-size:15px;color:var(--muted);margin-top:30px;border-top:1px solid rgba(233,230,255,.12);padding-top:14px}}
footer{{border-top:2px solid var(--verde);text-align:center;padding:26px 16px 36px;color:var(--muted);font-size:16px}}
footer a{{font-family:'VT323',monospace;font-size:22px;color:var(--verde);text-decoration:none;margin:0 8px}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<nav class="top">
  <a href="/"><img class="px" src="/logo.webp" alt="Trollacos" width="1600" height="161"></a>
  <a href="/">‹ PORTADA</a>
</nav>

<header class="cab">
  <img class="px ovni-cab" src="img/ovni.png" alt="" aria-hidden="true">
  <div class="k">&gt; ARCHIVO CLASIFICADO_</div>
  <h1>EXPEDIENTE TROLLACO<br>El Madrid que da miedo</h1>
  <p class="ent">Siete lugares por los que pasas cada día. Siete historias que nadie te contó en el colegio. Algunas son leyenda. Otras dejaron informes policiales. <strong>Tú decides cuáles creerte.</strong></p>
  <img class="px tr-cab" src="img/trollaco-linterna.png" alt="El Trollaco con una linterna">
  <div class="niebla"></div>
</header>

<main>
  <p class="aviso">⚠️ Contamos cada caso como lo cuenta la leyenda y, al final, lo que dicen los escépticos. Todos los lugares del mapa son públicos o visitables, salvo el caso Vallecas, que marcamos solo por barrio por respeto a sus vecinos.</p>

  <h2 class="sec" id="mapa">🗺️ El mapa del miedo</h2>
  <p>Pincha en cada icono para abrir su expediente. Haz zoom, muévete y apunta: algunos los tienes más cerca de lo que crees.</p>
  <div id="mapa-madrid" role="application" aria-label="Mapa de Madrid con los lugares de cada caso"></div>
  <ul class="indice">
{indice}
  </ul>

{''.join(casos_html)}

  <h2 class="sec" id="proximamente">🛸 Próximos expedientes</h2>
  <p>El archivo no termina en Madrid. Estamos preparando los casos más sonados de España y del resto del mundo:</p>
  <div class="prox-wrap">
{prox}
  </div>

  <div class="compartir">
    <b>&gt; ¿TIENES UN AMIGO QUE NO CREE EN NADA? MÁNDASELO_</b>
    <a href="https://wa.me/?text=Expediente%20Trollaco%3A%20los%20lugares%20encantados%20de%20Madrid%2C%20con%20mapa%20%F0%9F%91%BB%20https%3A%2F%2Ftrollacos.com%2Fmisterio%2F" target="_blank" rel="noopener">WhatsApp</a>
    <a href="https://t.me/share/url?url=https%3A%2F%2Ftrollacos.com%2Fmisterio%2F&amp;text=Expediente%20Trollaco%3A%20el%20Madrid%20que%20da%20miedo" target="_blank" rel="noopener">Telegram</a>
    <a href="https://twitter.com/intent/tweet?url=https%3A%2F%2Ftrollacos.com%2Fmisterio%2F&amp;text=Expediente%20Trollaco%3A%20el%20Madrid%20que%20da%20miedo%20%F0%9F%91%BB" target="_blank" rel="noopener">X</a>
    <button type="button" id="copiar">Copiar enlace</button>
  </div>

  <p class="nota">Textos e ilustraciones de Trollacos, basados en la historia documentada y en las leyendas populares de cada lugar. Si vas a visitar algún sitio, respeta horarios y propiedad privada. Mapa: © colaboradores de OpenStreetMap.</p>
</main>

<footer>
  <a href="/">PORTADA</a><a href="/arcade/">ARCADE</a><a href="/gta-6/">GUÍA GTA VI</a><br><br>
  © 2012–2026 TROLLACOS
</footer>

<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script>
(function(){{
  var PUNTOS={json.dumps(puntos, ensure_ascii=False)};
  if(document.documentElement.className.indexOf('halloween')>-1){{document.querySelectorAll('img[data-hw]').forEach(function(i){{i.src=i.getAttribute('data-hw')}})}}
  var b=document.getElementById('copiar');b.onclick=function(){{try{{navigator.clipboard.writeText('https://trollacos.com/misterio/').then(function(){{b.textContent='¡Copiado!'}})}}catch(e){{}}}};
  if(!window.L){{document.getElementById('mapa-madrid').innerHTML='<p style="padding:20px">No se ha podido cargar el mapa. Usa la lista de abajo.</p>';return}}
  var mapa=L.map('mapa-madrid',{{scrollWheelZoom:false,zoomControl:true}});
  mapa.attributionControl.setPrefix('<a href="https://leafletjs.com">Leaflet</a>');
  L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{maxZoom:19,
    attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}}).addTo(mapa);
  var grupo=[];
  PUNTOS.forEach(function(p){{
    var ic=L.divIcon({{className:'',html:'<div class="pin">'+p.i+'</div>',iconSize:[30,30],iconAnchor:[15,15]}});
    var m=L.marker([p.lat,p.lng],{{icon:ic,title:p.t}}).addTo(mapa);
    if(p.aprox)L.circle([p.lat,p.lng],{{radius:900,color:'#7cffb2',weight:1,fillOpacity:.06,dashArray:'4 6'}}).addTo(mapa);
    m.bindPopup('<b>'+p.t+'</b><i>'+p.s+(p.aprox?' (zona aproximada)':'')+'</i><a href="#'+p.id+'">Abrir expediente ↓</a>');
    if(!p.f)grupo.push([p.lat,p.lng]);
  }});
  if(!grupo.length)PUNTOS.forEach(function(p){{grupo.push([p.lat,p.lng])}});
  if(grupo.length===1)mapa.setView(grupo[0],12);else mapa.fitBounds(grupo,{{padding:[30,30]}});
  mapa.on('click',function(){{mapa.scrollWheelZoom.enable()}});
  document.getElementById('mapa-madrid').addEventListener('mouseleave',function(){{mapa.scrollWheelZoom.disable()}});
}})();
</script>
</body>
</html>
'''
open('/home/claude/trollacos-web/misterio/index.html', 'w').write(page)
print('ok', len(page))
