const { chromium } = require('playwright');const fs=require('fs');
const R='file:///home/claude/trollacos-web/', M='file:///home/claude/merch/';
const base=`@font-face{font-family:V;src:url(${R}fuentes/vt323.woff2)}*{margin:0;box-sizing:border-box}body{background:transparent;position:relative;overflow:hidden}`;
const P={
 'logo-trollacos-horizontal':[2400,400,`<img src="${M}logo-trollacos.png" style="position:absolute;left:30px;top:30px;width:2340px;filter:drop-shadow(0 0 2px rgba(255,255,255,.9))">`],
 'logo-trollacos-cuadrado':[1200,1200,`<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 40%,#2a0b4a,#07021a 70%)"></div>
  <div style="position:absolute;left:250px;top:120px;width:700px;height:700px;border-radius:50%;background:linear-gradient(180deg,#ffe45c,#ff9d3c 45%,#ff2bd6 85%);-webkit-mask:repeating-linear-gradient(180deg,#000 0 34px,transparent 34px 46px)"></div>
  <img src="${M}tr-cabeza.png" style="position:absolute;left:260px;top:240px;width:680px;image-rendering:pixelated">
  <img src="${M}logo-trollacos.png" style="position:absolute;left:100px;top:890px;width:1000px">`]
};
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
for(const k of Object.keys(P)){const [w,h,html]=P[k];const p=await b.newPage({viewport:{width:w,height:h}});
 fs.writeFileSync(`/home/claude/merch/logos/${k}.html`,`<!doctype html><html><head><meta charset="utf-8"><style>${base}body{width:${w}px;height:${h}px}</style></head><body>${html}</body></html>`);
 await p.goto(`file:///home/claude/merch/logos/${k}.html`);await p.waitForTimeout(700);
 await p.screenshot({path:`/home/claude/merch/logos/${k}.png`,omitBackground:true});await p.close()}
await b.close()})();
