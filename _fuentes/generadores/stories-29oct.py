import subprocess
R='/home/claude/trollacos-web';F='file://'+R
SP='/tmp/claude-0/-home-claude/074a85cb-bf8f-5cf1-801a-ef5ae6c1a692/scratchpad'
css=f"""@font-face{{font-family:'Righteous';src:url({F}/fuentes/righteous.woff2)}}@font-face{{font-family:'VT323';src:url({F}/fuentes/vt323.woff2)}}
@font-face{{font-family:'Rajdhani';src:url({F}/fuentes/rajdhani-700.woff2);font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1080px;height:1920px;overflow:hidden;position:relative;font-family:'Rajdhani';color:#fff;background:linear-gradient(180deg,#07021a 0%,#1a0640 60%,#3b0a5c 100%)}}
.est{{position:absolute;inset:0;height:1300px;background-image:radial-gradient(#fff 1.2px,transparent 1.8px);background-size:53px 61px;opacity:.3}}
.suelo{{position:absolute;left:-200px;right:-200px;top:1560px;bottom:0;background:#07021a;background-image:linear-gradient(#ff2bd6 2px,transparent 2px),linear-gradient(90deg,#ff2bd6 2px,transparent 2px);background-size:70px 40px;transform:perspective(320px) rotateX(58deg);transform-origin:top;opacity:.7}}
.hz{{position:absolute;left:0;right:0;top:1558px;height:4px;background:#ff2bd6;box-shadow:0 0 20px #ff2bd6}}
.c{{position:absolute;left:70px;right:70px;text-align:center}}
.etq span{{display:inline-block;font-family:'VT323';font-size:54px;padding:6px 30px;border:3px solid #1ff2ff;color:#1ff2ff;border-radius:12px;text-shadow:0 0 10px #1ff2ff;background:rgba(7,2,26,.6)}}
.tit{{font-family:'Righteous';line-height:.95;text-shadow:0 0 30px rgba(255,43,214,.7),6px 6px 0 #160828}}
.v{{font-family:'VT323';text-shadow:4px 4px 0 #160828}}
.lista{{position:absolute;left:80px;right:80px;border:3px solid #ff2bd6;border-radius:20px;background:rgba(7,2,26,.8);padding:24px 34px;box-shadow:0 0 30px rgba(255,43,214,.45)}}
.lista div{{font-size:44px;padding:10px 0;border-bottom:2px dashed rgba(255,255,255,.12)}}.lista div:last-child{{border:0}}
.lista b{{color:#ffd23f}}
.troll{{position:absolute;image-rendering:pixelated;filter:drop-shadow(0 0 26px rgba(31,242,255,.5))}}
.pie{{position:absolute;left:0;right:0;bottom:90px;text-align:center}}.pie img{{width:560px}}.pie div{{font-family:'VT323';font-size:46px;color:#1ff2ff;letter-spacing:.1em;text-shadow:0 0 10px #1ff2ff}}
"""
pie=f'<div class="pie"><img src="{F}/redes/logo-trollacos.png"><div>GUÍA COMPLETA EN TROLLACOS.COM</div></div>'
base='<div class="est"></div><div class="suelo"></div><div class="hz"></div>'
P={
'gta6-edge':base+f'''<div class="c etq" style="top:120px"><span>&gt; GTA VI · EXCLUSIVA EDGE_</span></div>
<div class="c tit" style="top:250px;font-size:120px;color:#ffd23f">EL MAPA ES<br>BRUTAL</div>
<div class="c v" style="top:520px;font-size:62px;color:#fff">LEONIDA ≈ GTA IV + GTA V<br>+ RED DEAD 2 JUNTOS 🤯</div>
<div class="lista" style="top:760px">
<div>🚆 <b>Trenes y buses</b> que funcionan</div>
<div>🐕 <b>Policía con perros</b> en las persecuciones</div>
<div>😈 <b>Perfil criminal:</b> de Profesional a Irredimible</div>
<div>💑 <b>Jason y Lucía:</b> cambias entre los dos</div>
<div>☕ <b>El café da aguante</b> y los batidos, vida</div></div>
<img class="troll" src="{F}/img/trollaco-mando.png" style="left:470px;top:1320px;width:140px">'''+pie,
'gta6-southpark':base+f'''<div class="c etq" style="top:120px"><span style="border-color:#ffd23f;color:#ffd23f;text-shadow:0 0 10px #ffd23f">&gt; ÚLTIMA HORA_</span></div>
<div class="c tit" style="top:250px;font-size:112px;color:#fff">GTA VI SALE<br>EN <span style="color:#ff9d3c">SOUTH PARK</span></div>
<div class="c" style="top:560px;font-size:220px">💩</div>
<div class="c v" style="top:850px;font-size:66px;color:#ffd23f">GAMEPLAY REAL:</div>
<div class="c" style="top:940px;font-size:58px;line-height:1.15">Jason tirándole <b style="color:#ff9d3c">caca de perro</b><br>a la gente en la playa<br>de Vice City</div>
<div class="c v" style="top:1200px;font-size:46px;color:#1ff2ff">"FOOTAGE COURTESY OF ROCKSTAR GAMES"</div>
<img class="troll" src="{F}/img/trollaco.png" style="left:480px;top:1300px;width:120px">'''+pie,
}
js="const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1080,height:1920}});\n"
for k,h in P.items():
    f=f'{SP}/st-{k}.html';open(f,'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{h}</body></html>')
    js+=f"await p.goto('file://{f}');await p.waitForTimeout(700);await p.screenshot({{path:'{R}/redes/stories/{k}.jpg',type:'jpeg',quality:90}});\n"
js+="await b.close()})();";open(f'{SP}/st.js','w').write(js);subprocess.run(['node',f'{SP}/st.js'],check=True)
from PIL import Image
a=Image.open(f'{R}/redes/stories/gta6-edge.jpg').resize((405,720));b=Image.open(f'{R}/redes/stories/gta6-southpark.jpg').resize((405,720))
o=Image.new('RGB',(810,720));o.paste(a,(0,0));o.paste(b,(405,0));o.save(f'{SP}/st-prev.jpg')
