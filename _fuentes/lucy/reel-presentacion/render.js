const {chromium}=require('playwright');
const R=__dirname, DUR=16.5, FPS=30;
const solo=process.argv[2]?process.argv[2].split(',').map(Number):null;
(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const p=await b.newPage({viewport:{width:540,height:960},deviceScaleFactor:2});
  await p.goto('file://'+R+'/reel.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
  const ts=solo||[...Array(Math.round(DUR*FPS)).keys()].map(i=>i/FPS);
  for(let i=0;i<ts.length;i++){
    await p.evaluate(t=>pinta(t),ts[i]);
    await p.screenshot({path:solo?`${R}/prev-${ts[i]}.jpg`:`${R}/fr/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});
  }
  await b.close();
})();
