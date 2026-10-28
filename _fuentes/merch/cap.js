const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1280,height:900}});
await p.goto('http://localhost:8765/arcade/_captura.html');await p.waitForTimeout(1200);
await p.evaluate(()=>window.__escena());await p.waitForTimeout(600);
const d=await p.evaluate(()=>document.getElementById('juego').toDataURL('image/png'));
require('fs').writeFileSync('juego.png',Buffer.from(d.split(',')[1],'base64'));await b.close();})();
