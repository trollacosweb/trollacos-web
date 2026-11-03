// node render.js <html> <segundos> <carpeta_frames>  (30 fps, controla el tiempo de las animaciones CSS)
const {chromium}=require('playwright');const [,,html,seg,dir]=process.argv;const fs=require('fs');fs.mkdirSync(dir,{recursive:true});
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+require('path').resolve(html));await p.waitForTimeout(800);
await p.evaluate(()=>document.getAnimations().forEach(a=>a.pause()));
const n=Math.round(seg*30);for(let i=0;i<n;i++){const t=i*1000/30;await p.evaluate(t=>document.getAnimations().forEach(a=>a.currentTime=t),t);
await p.screenshot({path:`${dir}/f${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}
await b.close();})();
