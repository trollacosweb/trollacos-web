// node render.js  → mapa-leonida.pdf, mapa-leonida.png (oscuro) y mapa-leonida-claro.pdf/png (ahorro de tinta)
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
for(const [suf,h] of [['',''],['-claro','#claro']]){
 const p=await b.newPage({viewport:{width:1123,height:1587},deviceScaleFactor:Number(process.argv[2]||2.2)});
 await p.goto('file://'+__dirname+'/mapa.html'+h);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
 await p.screenshot({path:`${__dirname}/mapa-leonida${suf}.png`});
 await p.pdf({path:`${__dirname}/mapa-leonida${suf}.pdf`,width:'297mm',height:'420mm',printBackground:true,preferCSSPageSize:true});
 await p.close();}
await b.close()})();
