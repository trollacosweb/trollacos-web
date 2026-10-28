const { chromium } = require('playwright');
const R='file:///home/claude/trollacos-web/', M='file:///home/claude/merch/';
const css=`@font-face{font-family:R;src:url(${R}fuentes/righteous.woff2)}@font-face{font-family:V;src:url(${R}fuentes/vt323.woff2)}
*{margin:0;box-sizing:border-box}body{width:4500px;height:5400px;background:transparent;position:relative;overflow:hidden}
.px{image-rendering:pixelated;position:absolute}.c{position:absolute;left:0;right:0;text-align:center}`;
const D={
'espalda-1-trollacos-clasico':`
<div style="position:absolute;left:600px;top:350px;width:3300px;height:3300px;border-radius:50%;background:linear-gradient(180deg,#ffe45c,#ff9d3c 45%,#ff2bd6 85%);
 -webkit-mask:repeating-linear-gradient(180deg,#000 0 150px,transparent 150px 200px)"></div>
<img class="px" src="${M}tr-cabeza.png" style="left:650px;top:900px;width:3200px">
<div class="c" style="top:3640px"><img src="${M}logo-trollacos.png" style="width:3700px"></div>
<div class="c" style="top:4330px;font-family:V;font-size:330px;letter-spacing:40px;color:#5a12b8;text-shadow:none">EST. 2012 · RELOADED</div>`,
'espalda-2-expediente-trollaco':`
<div class="c" style="top:250px"><span style="display:inline-block;font-family:V;font-size:360px;letter-spacing:30px;color:#ff4a4a;border:28px solid #ff4a4a;padding:0 120px;transform:rotate(-4deg)">ARCHIVO CLASIFICADO</span></div>
<div style="position:absolute;left:2650px;top:1900px;width:1850px;height:1500px;background:linear-gradient(270deg,rgba(255,236,120,0),rgba(255,236,120,.55));clip-path:polygon(0 42%,100% 0,100% 100%,0 58%)"></div>
<img class="px" src="${M}tr-linterna.png" style="left:350px;top:1000px;width:2816px">
<div class="c" style="top:3900px;font-family:R;font-size:560px;line-height:1;color:#0e6b3c;text-shadow:0 0 40px rgba(124,255,178,.6)">EXPEDIENTE<br>TROLLACO</div>`,
'espalda-3-trollaco-run':`
<style>.marco{position:absolute;left:150px;top:1350px;width:4200px;height:1800px;border-radius:120px;padding:100px;background:linear-gradient(180deg,#2a1450,#120530);
 border:40px solid #ff2bd6;box-shadow:0 0 120px rgba(255,43,214,.8),inset 0 0 80px rgba(31,242,255,.4)}
.marco img{width:4000px;height:1600px;display:block;image-rendering:pixelated;border-radius:40px;position:absolute;left:60px;top:60px}
.scan{position:absolute;left:60px;top:60px;width:4000px;height:1600px;border-radius:40px;background:repeating-linear-gradient(0deg,rgba(0,0,0,.18) 0 10px,transparent 10px 25px)}</style>
<div class="c" style="top:250px;font-family:V;font-size:700px;line-height:1;letter-spacing:6px;color:#ff2bd6;text-shadow:12px 12px 0 #1ff2ff,0 0 80px #ff2bd6">TROLLACO RUN</div>
<div class="c" style="top:1050px;font-family:V;font-size:200px;letter-spacing:16px;color:#d2600a;text-shadow:none">★ SALTA EL LAG · COGE LAS FICHAS ★</div>
<div class="marco"><img src="${M}juego.png"><div class="scan"></div></div>
<div class="c" style="top:3450px;font-family:V;font-size:520px;letter-spacing:50px;color:#5a12b8;text-shadow:none">INSERT COIN ▶</div>
<div class="c" style="top:4380px"><img src="${M}logo-trollacos.png" style="width:3100px"></div>`
};
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:4500,height:5400}});
for(const k of Object.keys(D)){require('fs').writeFileSync(`/home/claude/merch/blanca/${k}.html`,`<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${D[k]}</body></html>`);await p.goto(`file:///home/claude/merch/blanca/${k}.html`);
 await p.waitForTimeout(900);await p.screenshot({path:`/home/claude/merch/blanca/${k}.png`,omitBackground:true});}
await b.close()})();
