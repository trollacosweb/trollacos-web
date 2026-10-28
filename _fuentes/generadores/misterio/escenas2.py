import random, sys
sys.path.insert(0,'.')
from escenas import base, ventanas, S, OUT
G='<g fill="%s" stroke="#3d2d6e" stroke-width="2">'%S
def pinos(xs,y=280,h=70,seed=0):
    r=random.Random(seed);o=f'<g fill="#07130e" stroke="#1d3b2b" stroke-width="1.5">'
    for x in xs:
        hh=h*r.uniform(.7,1.2);o+=f'<path d="M{x} {y-hh} L{x-hh*.32} {y} L{x+hh*.32} {y}Z"/>'
    return o+'</g>'
esc={}
# La Barranca: edificio de 6 plantas entre pinos, medio derruido, una ventana encendida
esc['barranca']=base(G+'<rect x="170" y="80" width="260" height="200"/><path d="M430 80 L470 120 L470 280 L430 280Z"/><rect x="0" y="275" width="600" height="65"/></g>'
 +ventanas(186,96,8,6,30,30,14,18,0,21)+'<rect x="276" y="186" width="14" height="18" fill="#e8f2ff"/>'
 +'<path d="M440 120 l18 30 l-10 20 l14 40" stroke="#04020c" stroke-width="4" fill="none"/>'
 +pinos([30,70,110,140,480,510,550,590],seed=1)+pinos([20,90,520,580],y=290,h=110,seed=2),cielo=('#020a08','#0c2a20'),luna=(110,60,24),seed=21)
# Sanatorio de la Marina: edificio alargado con galerías (balcones corridos) de 4 plantas
gal=''.join(f'<rect x="90" y="{120+i*36}" width="420" height="4" fill="#5a4a8a"/>' for i in range(4))
esc['marina']=base(G+'<rect x="90" y="110" width="420" height="170"/><path d="M80 112 L520 112 L500 96 L100 96Z"/><rect x="0" y="275" width="600" height="65"/></g>'
 +gal+ventanas(100,126,14,4,29,36,16,22,.06,22)+pinos([20,50,560,590],seed=3),cielo=('#03060f','#14203a'),luna=(470,58,26),seed=22)
# Manises: avión de noche con luces rojas alrededor
esc['manises']=base('''<g transform="translate(240 150) rotate(-6)"><path d="M0 0 h160 q22 0 26 8 q-4 8 -26 8 h-160 q-10 -8 0 -16z" fill="#d6dbea"/>
<path d="M70 8 l-40 50 h16 l54 -50z" fill="#aeb4c8"/><path d="M70 6 l-30 -40 h14 l46 40z" fill="#aeb4c8"/><path d="M4 2 l-14 -28 h10 l16 26z" fill="#aeb4c8"/>
'''+''.join(f'<rect x="{30+i*12}" y="5" width="5" height="4" fill="#ffe08a"/>' for i in range(11))+'''</g>
<g fill="#ff2a2a">'''+''.join(f'<circle cx="{x}" cy="{y}" r="7"/><circle cx="{x}" cy="{y}" r="20" opacity=".2"/>' for x,y in ((470,96),(500,120),(180,110)))+'''</g>
<path d="M0 300 Q300 270 600 300 V340 H0Z" fill="#060410"/>'''+''.join(f'<circle cx="{x}" cy="{305+(x%7)}" r="1.6" fill="#ffcf5a"/>' for x in range(20,600,23)),cielo=('#02010a','#120a30'),luna=(80,50,18),seed=23)
# Bélmez: suelo de cocina con caras borrosas
caras=''
for cx,cy,s in ((180,170,1.2),(380,140,.9),(300,250,1.4),(470,250,.8),(120,280,.7)):
    caras+=f'<g transform="translate({cx} {cy}) scale({s})" fill="none" stroke="#2a1a10" stroke-width="3" opacity=".55"><ellipse rx="34" ry="44"/><ellipse cx="-12" cy="-8" rx="7" ry="9" fill="#2a1a10"/><ellipse cx="12" cy="-8" rx="7" ry="9" fill="#2a1a10"/><path d="M-2 0 l2 10"/><ellipse cy="24" rx="7" ry="9" fill="#2a1a10"/></g>'
esc['belmez']=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340" role="img"><defs><radialGradient id="v"><stop offset=".3" stop-color="#b9a58a"/><stop offset="1" stop-color="#3a2c20"/></radialGradient>
<filter id="r"><feTurbulence baseFrequency=".9" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 .3 0 0 0 0 .22 0 0 0 0 .15 0 0 0 .35 0"/><feComposite in2="SourceGraphic" operator="in"/></filter></defs>
<filter id="bl"><feGaussianBlur stdDeviation="2.2"/></filter><rect width="600" height="340" fill="url(#v)"/><rect width="600" height="340" fill="#fff" filter="url(#r)"/><g filter="url(#bl)">{caras}</g>
<path d="M0 120 L600 100 M0 230 L600 215 M200 0 L215 340 M420 0 L410 340" stroke="#2a1a10" stroke-width="2" opacity=".35"/>
<rect width="600" height="340" fill="#000" opacity=".15"/></svg>'''
# Canarias 1976: mar, islas y una esfera translúcida enorme
esc['canarias']=base('''<path d="M0 230 Q80 200 160 228 Q220 190 290 226 Z" fill="#0a0418" stroke="#3d2d6e" stroke-width="2"/><path d="M380 236 Q460 206 520 232 Q560 220 600 236Z" fill="#0a0418" stroke="#3d2d6e" stroke-width="2"/>
<rect y="230" width="600" height="110" fill="#070c22"/>'''+''.join(f'<path d="M{x} {250+(x*7)%60} h18" stroke="#3a4a8a" stroke-width="2" opacity=".6"/>' for x in range(10,600,37))+'''
<defs><radialGradient id="e"><stop offset="0" stop-color="#e8fbff" stop-opacity=".9"/><stop offset=".08" stop-color="#bff4ff" stop-opacity=".5"/><stop offset=".7" stop-color="#7fd8ff" stop-opacity=".12"/><stop offset="1" stop-color="#7fd8ff" stop-opacity="0"/></radialGradient></defs>
<circle cx="330" cy="120" r="110" fill="url(#e)"/><circle cx="330" cy="120" r="108" fill="none" stroke="#bff4ff" stroke-opacity=".35" stroke-width="2"/>
<path d="M330 128 L310 230 L350 230Z" fill="#bff4ff" opacity=".08"/><path d="M200 300 h260" stroke="#bff4ff" stroke-width="3" opacity=".25"/>''',cielo=('#02030c','#0d1530'),luna=(540,40,0),seed=24)
# Tórax: torre de hospital en la ladera de una montaña
esc['torax']=base('<path d="M0 240 Q160 120 300 170 Q420 90 600 200 V340 H0Z" fill="#0b0716" stroke="#3d2d6e" stroke-width="2"/>'+G+'<rect x="250" y="60" width="110" height="220"/><rect x="200" y="200" width="210" height="80"/><rect x="0" y="275" width="600" height="65"/></g>'
 +ventanas(260,72,4,10,26,20,12,12,.12,25)+'<text x="305" y="54" text-anchor="middle" font-family="Georgia,serif" font-size="13" fill="#7a6aa8">IX</text>',cielo=('#030210','#1a0f33'),luna=(90,60,26),seed=25)
# Roswell: desierto, rancho y restos brillantes
esc['roswell']=base('<path d="M0 250 Q150 230 300 248 Q450 236 600 250 V340 H0Z" fill="#1a0f10"/>'+G+'<rect x="60" y="210" width="70" height="44"/><path d="M52 212 L95 186 L138 212Z"/><rect x="150" y="196" width="10" height="58"/><circle cx="155" cy="190" r="14" fill="none"/></g>'
 +''.join(f'<path d="M{x} {y} l{8+(x%5)} {-3+(y%4)} l-3 6z" fill="#cfd6ea" opacity=".85"/>' for x,y in ((330,270),(360,282),(390,276),(420,290),(452,280),(300,292),(480,296)))
 +'<g transform="translate(410 262) rotate(-14)"><ellipse rx="54" ry="12" fill="#8a92b4"/><ellipse cy="-6" rx="22" ry="11" fill="#b4bcdc"/></g><path d="M380 250 q30 -40 70 -10" stroke="#555" stroke-width="2" fill="none" opacity=".5"/>',cielo=('#05020c','#2a1428'),luna=(500,60,24),seed=26)
# Rendlesham: bosque con luces entre los árboles y el faro al fondo
esc['rendlesham']=base('<rect y="250" width="600" height="90" fill="#050a08"/>'
 +pinos(range(0,600,30),y=290,h=130,seed=7)
 +'<path d="M540 260 L540 205 L548 205 L548 260Z" fill="#0a0418"/><path d="M544 207 L600 190 L600 224Z" fill="#fff6c8" opacity=".35"/><circle cx="544" cy="207" r="5" fill="#fff6c8"/>'
 +'<circle cx="270" cy="232" r="10" fill="#ff3b3b"/><circle cx="270" cy="232" r="30" fill="#ff3b3b" opacity=".22"/><circle cx="314" cy="240" r="7" fill="#3bc6ff"/><circle cx="314" cy="240" r="20" fill="#3bc6ff" opacity=".2"/><circle cx="232" cy="244" r="7" fill="#ffd23f"/>'
 +pinos([10,60,110,470,520,580],y=340,h=220,seed=8),cielo=('#02040a','#0c1a28'),luna=(90,50,18),seed=27)
# Nimitz: océano, un caza y un "tic tac" blanco
esc['nimitz']=base('<rect y="220" width="600" height="120" fill="#06122a"/>'+''.join(f'<path d="M{x} {235+(x*11)%90} h22" stroke="#2a4a8a" stroke-width="2" opacity=".5"/>' for x in range(0,600,29))
 +'<ellipse cx="200" cy="250" rx="60" ry="10" fill="#9ad4ff" opacity=".25"/><rect x="330" y="120" width="96" height="34" rx="17" fill="#f4f8ff"/><rect x="330" y="120" width="96" height="34" rx="17" fill="none" stroke="#9ad4ff" stroke-width="4" opacity=".4"/>'
 +'<g transform="translate(120 90) rotate(8)" fill="#5a6488"><path d="M0 10 L90 6 L110 10 L90 14Z"/><path d="M40 10 L20 30 L36 30 L60 10Z"/><path d="M40 10 L20 -10 L36 -10 L60 10Z"/><path d="M6 10 L-4 0 L4 0 L14 10Z"/></g>',cielo=('#0a1638','#3a5a8a'),luna=(520,50,0),seed=28)
# Phoenix: luces en V sobre la ciudad y las montañas
esc['phoenix']=base('<path d="M0 230 L80 190 L140 220 L220 170 L300 215 L380 180 L470 210 L540 175 L600 200 V260 H0Z" fill="#0d0718" stroke="#3d2d6e" stroke-width="2"/>'
 +'<rect y="255" width="600" height="85" fill="#08040f"/>'+''.join(f'<rect x="{x}" y="{258+(x*3)%20}" width="3" height="3" fill="#ffcf5a" opacity=".8"/>' for x in range(5,600,11))
 +''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="#ffd9a0"/><circle cx="{x}" cy="{y}" r="16" fill="#ffd9a0" opacity=".25"/>' for x,y in ((300,150),(255,120),(210,92),(345,120),(390,92))),cielo=('#04030c','#1a1030'),luna=(80,48,16),seed=29)
for n,s in esc.items(): open(OUT+f'{n}.svg','w').write(s)
print(list(esc))
