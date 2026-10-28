import os, json, subprocess
R='/home/claude/trollacos-web'
OUT=R+'/redes/semana-44'
os.makedirs(OUT,exist_ok=True)
F='file://'+R
css=f"""@font-face{{font-family:'Righteous';src:url({F}/fuentes/righteous.woff2)}}
@font-face{{font-family:'VT323';src:url({F}/fuentes/vt323.woff2)}}
@font-face{{font-family:'Rajdhani';src:url({F}/fuentes/rajdhani-700.woff2);font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;overflow:hidden;position:relative;font-family:'Rajdhani';color:#fff;background:#07021a}}
.fondo{{position:absolute;inset:0;background:linear-gradient(180deg,#07021a 0%,#1a0640 55%,#3b0a5c 100%)}}
.estrellas{{position:absolute;inset:0;height:850px;background-image:radial-gradient(#fff 1.2px,transparent 1.8px);background-size:53px 61px;opacity:.35}}
.sol{{position:absolute;left:290px;top:480px;width:500px;height:500px;border-radius:50%;background:linear-gradient(180deg,#ffd23f,#ff9d3c 35%,#ff2bd6 75%,#9d1aff);
 -webkit-mask:repeating-linear-gradient(180deg,#000 0 30px,transparent 30px 40px);clip-path:inset(0 0 34% 0)}}
.suelo{{position:absolute;left:-200px;right:-200px;top:1010px;bottom:0;background:#07021a;background-image:linear-gradient(#ff2bd6 2px,transparent 2px),linear-gradient(90deg,#ff2bd6 2px,transparent 2px);
 background-size:70px 40px;transform:perspective(320px) rotateX(58deg);transform-origin:top;opacity:.75}}
.hz{{position:absolute;left:0;right:0;top:1008px;height:4px;background:#ff2bd6;box-shadow:0 0 20px #ff2bd6}}
.etq{{position:absolute;top:60px;left:0;right:0;text-align:center}}
.etq span{{display:inline-block;font-family:'VT323';font-size:44px;letter-spacing:.08em;padding:4px 26px;border:3px solid #1ff2ff;color:#1ff2ff;border-radius:10px;background:rgba(7,2,26,.6);text-shadow:0 0 10px #1ff2ff}}
.tit{{position:absolute;left:40px;right:40px;top:150px;text-align:center;font-family:'Righteous';line-height:.95;text-shadow:0 0 30px rgba(255,43,214,.7),6px 6px 0 #160828}}
.sub{{position:absolute;left:60px;right:60px;text-align:center;font-family:'VT323';font-size:56px;line-height:1.05;color:#ffd23f;text-shadow:4px 4px 0 #160828}}
.troll{{position:absolute;image-rendering:pixelated;filter:drop-shadow(0 0 26px rgba(31,242,255,.55))}}
.pie{{position:absolute;left:0;right:0;bottom:46px;text-align:center}}
.pie img{{width:520px}}
.pie div{{font-family:'VT323';font-size:40px;color:#1ff2ff;letter-spacing:.1em;margin-top:6px;text-shadow:0 0 10px #1ff2ff}}
.caja{{position:absolute;left:70px;right:70px;border:3px solid #ff2bd6;border-radius:18px;background:rgba(7,2,26,.78);padding:18px 26px;box-shadow:0 0 30px rgba(255,43,214,.45)}}
.fila{{display:flex;justify-content:space-between;font-family:'VT323';font-size:44px;padding:4px 0;border-bottom:2px dashed rgba(255,255,255,.12)}}
.fila b{{color:#ffd23f;font-weight:400}}
"""
def pie(txt='TROLLACOS.COM'): return f'<div class="pie"><img src="{F}/redes/logo-trollacos.png"><div>{txt}</div></div>'
BASE='<div class="fondo"></div><div class="estrellas"></div><div class="sol"></div><div class="suelo"></div><div class="hz"></div>'
P={
'1-gta6-210gb':BASE+f'''<div class="etq"><span>&gt; GTA VI · ÚLTIMA HORA_</span></div>
<div class="tit" style="font-size:250px;color:#ffd23f">210 GB</div>
<div class="sub" style="top:405px">LO QUE OCUPARÁ GTA VI EN PS5</div>
<img class="troll" src="{F}/img/trollaco.png" style="left:420px;top:560px;width:240px">
<div class="sub" style="top:960px;font-size:48px;color:#fff;background:rgba(7,2,26,.7);left:150px;right:150px;border-radius:12px;padding:6px">Tu PS5 al enterarse: 😱</div>'''+pie('GUÍA DE COMPRA EN TROLLACOS.COM'),
'2-porra-jornada11':BASE+f'''<div class="etq"><span>&gt; LALIGA · JORNADA 11_</span></div>
<div class="tit" style="font-size:118px;color:#fff">LA PORRA<br><span style="color:#ff2bd6">TROLLACA</span></div>
<img class="troll" src="{F}/img/trollaco-mando.png" style="left:860px;top:150px;width:150px">
<div class="caja" style="top:430px">
<div class="fila"><span>BARCELONA - ALAVÉS</span><b>SÁB 21:00</b></div>
<div class="fila"><span>RACING - REAL MADRID</span><b>DOM 16:15</b></div>
<div class="fila"><span>LEVANTE - ATLÉTICO</span><b>SÁB 14:00</b></div>
<div class="fila"><span>ATHLETIC - REAL SOCIEDAD</span><b>DOM 21:00</b></div>
<div class="fila" style="border:0"><span>BETIS - MÁLAGA</span><b>SÁB 18:30</b></div></div>
<div class="sub" style="top:850px;font-size:50px;color:#1ff2ff">GANA FICHAS EN EL ARCADE<br>Y PRONOSTICA LA JORNADA</div>
<div class="sub" style="top:990px;font-size:40px;color:#fff">SIN DINERO REAL · SOLO POR EL PIQUE</div>'''+pie('TROLLACOS.COM/PORRA'),
'3-halloween-capitulo1':BASE.replace('#3b0a5c','#6a1f1a').replace('#1a0640','#2b0b3a')+f'''<div class="etq"><span style="border-color:#ff7a1a;color:#ff7a1a;text-shadow:0 0 10px #ff7a1a">&gt; ESTA NOCHE ES TROLLOWEEN_</span></div>
<div class="tit" style="font-size:130px;color:#ff7a1a;text-shadow:0 0 34px rgba(255,122,26,.8),6px 6px 0 #160828">LA NOCHE<br>TROLLOWEEN</div>
<img class="troll" src="{F}/img/murcielago.png" style="left:120px;top:470px;width:170px">
<img class="troll" src="{F}/img/murcielago.png" style="left:800px;top:420px;width:130px">
<img class="troll" src="{F}/img/trollaco-hw.png" style="left:400px;top:520px;width:270px;filter:drop-shadow(0 0 30px rgba(255,122,26,.7))">
<img class="troll" src="{F}/img/calabaza.png" style="left:720px;top:820px;width:150px">
<img class="troll" src="{F}/img/calabaza.png" style="left:200px;top:850px;width:120px">
<div class="sub" style="top:1040px;font-size:46px;color:#fff">CAPÍTULO 1 DEL ARCADE · ZOMBIS, CALABAZAS<br>Y UNA MANSIÓN ENCANTADA 🎃</div>'''+pie('JUEGA GRATIS EN TROLLACOS.COM/ARCADE').replace('bottom:46px','bottom:30px'),
'4-reto-jam85':BASE+f'''<div class="etq"><span style="border-color:#ff9d3c;color:#ff9d3c;text-shadow:0 0 10px #ff9d3c">&gt; SUPERA EL RÉCORD_</span></div>
<div class="tit" style="font-size:120px;color:#fff">¿ALGUIEN PUEDE<br>CON <span style="color:#ff9d3c">JAM85</span>?</div>
<img class="troll" src="{F}/img/trollaco.png" style="left:410px;top:470px;width:260px;filter:drop-shadow(0 0 40px #ff5a00) drop-shadow(0 -20px 30px #ff9d3c)">
<div class="sub" style="top:900px;font-size:90px;color:#ffd23f">🔥 4.586 PUNTOS 🔥</div>
<div class="sub" style="top:1010px;font-size:44px;color:#fff">El número 1 del arcade lleva días sin rival</div>'''+pie('TROLLACOS.COM/ARCADE'),
'5-cuenta-atras-17':BASE+f'''<div class="etq"><span>&gt; GTA VI · 19 NOV_</span></div>
<div class="sub" style="top:170px;font-size:80px;color:#fff">FALTAN</div>
<div class="tit" style="top:230px;font-size:420px;color:#ff2bd6">17</div>
<div class="sub" style="top:640px;font-size:90px;color:#ffd23f">DÍAS</div>
<img class="troll" src="{F}/img/trollaco-mando.png" style="left:470px;top:745px;width:140px">
<div class="sub" style="top:1020px;font-size:42px;color:#fff;background:rgba(7,2,26,.75);left:180px;right:180px;border-radius:10px">La guía completa de GTA VI en español</div>'''+pie('TROLLACOS.COM/GTA-6'),
'6-misterio':BASE.replace('#3b0a5c','#0e2a22').replace('#1a0640','#0b1a2a')+f'''<div class="etq"><span style="border-color:#7cffb2;color:#7cffb2;text-shadow:0 0 10px #7cffb2">&gt; ARCHIVO CLASIFICADO_</span></div>
<div class="tit" style="font-size:120px;color:#eafff3;text-shadow:0 0 34px #7cffb2,6px 6px 0 #160828">EXPEDIENTE<br>TROLLACO</div>
<img class="troll" src="{F}/misterio/img/trollaco-linterna.png" style="left:380px;top:470px;width:300px;filter:drop-shadow(0 0 30px rgba(124,255,178,.6))">
<div class="sub" style="top:900px;font-size:52px;color:#fff">OVNIS, CASAS ENCANTADAS<br>Y SUCESOS DE MADRID</div>
<div class="sub" style="top:1030px;font-size:42px;color:#7cffb2">¿Te atreves a abrir el archivo?</div>'''+pie('TROLLACOS.COM/MISTERIO').replace('bottom:46px','bottom:26px'),
}
os.makedirs('/tmp/claude-0/-home-claude/074a85cb-bf8f-5cf1-801a-ef5ae6c1a692/scratchpad/redes',exist_ok=True)
js="const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1080,height:1350}});\n"
for k,html in P.items():
    f=f'/tmp/claude-0/-home-claude/074a85cb-bf8f-5cf1-801a-ef5ae6c1a692/scratchpad/redes/{k}.html'
    open(f,'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{html}</body></html>')
    js+=f"await p.goto('file://{f}');await p.waitForTimeout(700);await p.screenshot({{path:'{OUT}/{k}.jpg',type:'jpeg',quality:90}});\n"
js+="await b.close()})();"
open('/tmp/claude-0/-home-claude/074a85cb-bf8f-5cf1-801a-ef5ae6c1a692/scratchpad/redes/r.js','w').write(js)
subprocess.run(['node','/tmp/claude-0/-home-claude/074a85cb-bf8f-5cf1-801a-ef5ae6c1a692/scratchpad/redes/r.js'],check=True)
print(sorted(os.listdir(OUT)))
