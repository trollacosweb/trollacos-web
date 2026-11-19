// node render.js [escala] → plano-leonida(.pdf/.png) y plano-leonida-claro(.pdf/.png)
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
for(const [suf,h] of [['',''],['-claro','#claro']]){
 const p=await b.newPage({viewport:{width:1123,height:1587},deviceScaleFactor:Number(process.argv[2]||1)});
 await p.goto('file://'+__dirname+'/plano.html'+h);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
 await p.screenshot({path:`${__dirname}/plano-leonida${suf}.png`,fullPage:true,clip:{x:0,y:0,width:1123,height:1587}});
 await p.screenshot({path:`${__dirname}/plano-leonida${suf}-indice.png`,fullPage:true,clip:{x:0,y:1587,width:1123,height:1587}});
 await p.pdf({path:`${__dirname}/plano-leonida${suf}.pdf`,width:'297mm',height:'420mm',printBackground:true,preferCSSPageSize:true});
 await p.close();}
await b.close()})();
