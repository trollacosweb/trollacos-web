const { chromium } = require('playwright');const fs=require('fs');
const R='file:///home/claude/trollacos-web/', M='file:///home/claude/merch/';
const css=`@font-face{font-family:R;src:url(${R}fuentes/righteous.woff2)}@font-face{font-family:V;src:url(${R}fuentes/vt323.woff2)}
*{margin:0;box-sizing:border-box}body{width:4500px;height:5400px;background:transparent;position:relative;overflow:hidden}
.px{image-rendering:pixelated;position:absolute}.c{position:absolute;left:0;right:0;text-align:center}`;
const D={
'1-trollacos-clasico':`
<div style="position:absolute;left:600px;top:350px;width:3300px;height:3300px;border-radius:50%;background:linear-gradient(180deg,#ffe45c,#ff9d3c 45%,#ff2bd6 85%);
 -webkit-mask:repeating-linear-gradient(180deg,#000 0 150px,transparent 150px 200px)"></div>
<img class="px" src="${M}tr-cabeza.png" style="left:650px;top:900px;width:3200px">
<img src="${R}logo.webp" style="position:absolute;left:250px;top:3650px;width:4000px">
<div class="c" style="top:4250px;font-family:V;font-size:330px;letter-spacing:40px;color:#1ff2ff;text-shadow:0 0 40px #1ff2ff">EST. 2012 · RELOADED</div>`,
'2-expediente-trollaco':`
<div class="c" style="top:250px"><span style="display:inline-block;font-family:V;font-size:360px;letter-spacing:30px;color:#ff4a4a;border:28px solid #ff4a4a;padding:0 120px;transform:rotate(-4deg)">ARCHIVO CLASIFICADO</span></div>
<div style="position:absolute;left:2650px;top:1900px;width:1850px;height:1500px;background:linear-gradient(270deg,rgba(255,236,120,0),rgba(255,236,120,.55));clip-path:polygon(0 42%,100% 0,100% 100%,0 58%)"></div>
<img class="px" src="${M}tr-linterna.png" style="left:350px;top:1000px;width:2816px">
<div class="c" style="top:3900px;font-family:R;font-size:560px;line-height:1;color:#eafff3;text-shadow:0 0 60px #7cffb2,0 0 140px #7cffb2">EXPEDIENTE<br>TROLLACO</div>
<div class="c" style="top:5050px;font-family:V;font-size:220px;letter-spacing:20px;color:#7cffb2">TROLLACOS.COM/MISTERIO</div>`,
'3-trolloween':`
<img class="px" src="${M}bat.png" style="left:250px;top:500px;width:900px;filter:drop-shadow(0 0 60px #ff7a1a)">
<img class="px" src="${M}bat.png" style="left:3300px;top:300px;width:700px;filter:drop-shadow(0 0 60px #ff7a1a)">
<img class="px" src="${M}bat.png" style="left:3550px;top:1500px;width:520px;filter:drop-shadow(0 0 60px #ff7a1a)">
<img class="px" src="${M}tr-calabaza.png" style="left:1230px;top:450px;width:2040px">
<div class="c" style="top:3980px;font-family:R;font-size:600px;line-height:1;background:linear-gradient(90deg,#ffd23f,#ff7a1a 50%,#e0203a);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 0 50px rgba(255,122,26,.8))">TRUCO O<br>TROLLEO</div>`
};
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:4500,height:5400}});
for(const [n,h] of Object.entries(D)){fs.writeFileSync(n+'.html',`<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${h}</body></html>`);
 await p.goto('file://'+__dirname+'/'+n+'.html');await p.waitForTimeout(800);await p.screenshot({path:n+'.png',omitBackground:true});}
await b.close();})();
