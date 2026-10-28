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
<div class="c" style="top:4330px;font-family:V;font-size:330px;letter-spacing:40px;color:#1ff2ff;-webkit-text-stroke:14px #3a0a7a;paint-order:stroke fill;text-shadow:8px 8px 0 #3a0a7a">EST. 2012 · RELOADED</div>`,
};
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:4500,height:5400}});
for(const k of Object.keys(D)){require('fs').writeFileSync(`/home/claude/merch/celeste/${k}.html`,`<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${D[k]}</body></html>`);await p.goto(`file:///home/claude/merch/celeste/${k}.html`);
 await p.waitForTimeout(900);await p.screenshot({path:`/home/claude/merch/celeste/${k}.png`,omitBackground:true});}
await b.close()})();
