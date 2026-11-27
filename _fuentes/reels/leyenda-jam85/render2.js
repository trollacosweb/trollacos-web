// node render2.js <pagina#n> <duracion> <carpeta_salida> [tiempos_preview]
const {chromium}=require('playwright');
const [pag,dur,out,prev]=process.argv.slice(2);const fs=require('fs');fs.mkdirSync(out,{recursive:true});
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 const p=await b.newPage({viewport:{width:540,height:960},deviceScaleFactor:2});
 await p.goto('file://'+__dirname+'/'+pag);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
 const ts=prev?prev.split(',').map(Number):[...Array(Math.round(dur*30)).keys()].map(i=>i/30);
 for(let i=0;i<ts.length;i++){await p.evaluate(t=>pinta(t),ts[i]);
  await p.screenshot({path:`${out}/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}
 await b.close()})();
