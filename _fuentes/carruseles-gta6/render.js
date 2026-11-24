// node render.js datos.json salida/  → una PNG por diapositiva (1080x1350)
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const D=JSON.parse(fs.readFileSync(process.argv[2]));const out=process.argv[3];fs.mkdirSync(out,{recursive:true});
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await b.newPage({viewport:{width:1080,height:1350}});
await p.goto('file://'+path.join(__dirname,'plantilla.html'));await p.evaluate(()=>document.fonts.ready);
for(const s of D){await p.evaluate(d=>pinta(d),s);await p.waitForTimeout(80);
 const h=await p.evaluate(()=>{const c=document.getElementById('cards').getBoundingClientRect();return c.bottom});
 if(h>1135)console.log('DEMASIADO ALTO',s.file,Math.round(h));
 await p.screenshot({path:path.join(out,s.file)});}
await b.close()})();
