const {chromium}=require('playwright');const fs=require('fs');const T=JSON.parse(fs.readFileSync(__dirname+'/textos.json'));
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/capa.html');await p.evaluate(()=>document.fonts.ready);fs.mkdirSync(__dirname+'/capas',{recursive:true});
for(let i=0;i<T.length;i++){await p.evaluate(s=>pon(s),T[i]);await p.screenshot({path:`${__dirname}/capas/t${String(i).padStart(2,'0')}.png`,omitBackground:true});}
await p.evaluate(()=>marca());await p.screenshot({path:__dirname+'/capas/marca.png',omitBackground:true});await b.close()})();
