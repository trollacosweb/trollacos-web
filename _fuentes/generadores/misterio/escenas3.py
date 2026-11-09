"""Ilustraciones (SVG) de los casos añadidos el 9 nov 2026: Talavera y Latinoamérica."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from escenas import base, ventanas, S, OUT
from escenas2 import pinos
G = '<g fill="%s" stroke="#3d2d6e" stroke-width="2">' % S
def glow(x, y, r, c, o=.22): return f'<circle cx="{x}" cy="{y}" r="{r*3}" fill="{c}" opacity="{o}"/><circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
esc = {}
# Talavera la Real: valla de la base, matorrales y una figura verde altísima de luz
valla = ''.join(f'<rect x="{x}" y="200" width="4" height="80" fill="#2a2244"/>' for x in range(0, 600, 40)) + '<path d="M0 205 H600 M0 230 H600 M0 255 H600" stroke="#2a2244" stroke-width="2"/>'
fig = ('<g opacity=".95"><ellipse cx="420" cy="170" rx="70" ry="110" fill="#5dff8a" opacity=".12"/>'
       '<rect x="405" y="95" width="30" height="120" rx="12" fill="#7dffa2" opacity=".85"/><circle cx="420" cy="82" r="13" fill="#7dffa2"/>'
       '<path d="M407 110 Q370 170 372 240" stroke="#7dffa2" stroke-width="8" fill="none" stroke-linecap="round"/><path d="M433 110 Q470 170 468 240" stroke="#7dffa2" stroke-width="8" fill="none" stroke-linecap="round"/>'
       + ''.join(f'<circle cx="{410+(i*7)%22}" cy="{100+i*11}" r="2" fill="#fff"/>' for i in range(10)) + '</g>')
esc['talavera'] = base(fig + valla + '<path d="M0 280 Q100 262 200 280 Q300 266 400 282 Q500 268 600 280 V340 H0Z" fill="#070512"/>'
    + ''.join(f'<path d="M{x} 282 q8 -26 16 0" fill="#0c1a10"/>' for x in range(0, 600, 34))
    + '<g transform="translate(110 236)" fill="#0a0418"><rect x="-4" y="0" width="8" height="40"/><circle cy="-8" r="8"/><path d="M4 8 L40 -6" stroke="#0a0418" stroke-width="4"/></g>'
    + '<path d="M150 228 L380 170" stroke="#ffd23f" stroke-width="2" stroke-dasharray="6 6" opacity=".7"/>', cielo=('#02030a', '#10203a'), luna=(80, 50, 20), seed=31)
# Varginha: muro bajo la lluvia, criatura de ojos rojos agachada
lluvia = ''.join(f'<path d="M{x} {y} l-6 18" stroke="#9ab4ff" stroke-width="1.4" opacity=".45"/>' for x, y in ((random.Random(i).randint(0, 600), random.Random(i * 7).randint(0, 320)) for i in range(140)))
esc['varginha'] = base('<rect x="60" y="170" width="480" height="110" fill="#1a1230" stroke="#3d2d6e" stroke-width="2"/>'
    + ''.join(f'<path d="M60 {y} H540" stroke="#2a2048" stroke-width="2"/>' for y in range(190, 280, 22))
    + ''.join(f'<path d="M{x} {170+((x//60)%2)*22} V{192+((x//60)%2)*22}" stroke="#2a2048" stroke-width="2"/>' for x in range(90, 540, 60))
    + '<g transform="translate(300 230)"><ellipse cx="0" cy="30" rx="30" ry="22" fill="#5a3a24"/><ellipse cx="0" cy="-8" rx="30" ry="34" fill="#6a4630"/>'
      '<path d="M-26 -30 q-12 -26 4 -30 M26 -30 q12 -26 -4 -30 M0 -40 q0 -26 6 -30" stroke="#6a4630" stroke-width="8" stroke-linecap="round" fill="none"/>'
      + glow(-12, -10, 7, '#ff2a2a', .25) + glow(12, -10, 7, '#ff2a2a', .25) + '</g>'
    + '<rect y="278" width="600" height="62" fill="#0a0612"/>' + lluvia, cielo=('#06060e', '#1a1a2e'), luna=(520, 40, 0), seed=32)
# Colares: río ancho, casas de pescadores en palafitos, hogueras y luces en el cielo
casas = ''.join(f'<g fill="#0a0418" stroke="#3d2d6e" stroke-width="2"><rect x="{x}" y="208" width="54" height="34"/><path d="M{x-6} 210 L{x+27} 190 L{x+60} 210Z"/></g><path d="M{x+6} 242 V262 M{x+48} 242 V262" stroke="#3d2d6e" stroke-width="3"/>' for x in (40, 130, 450, 530))
fuego = ''.join(f'<path d="M{x} 262 q8 -26 16 0z" fill="#ff8a00"/><circle cx="{x+8}" cy="250" r="22" fill="#ff8a00" opacity=".2"/>' for x in (230, 380))
esc['colares'] = base('<rect y="255" width="600" height="85" fill="#060c18"/>' + ''.join(f'<path d="M{x} {270+(x*13)%60} h20" stroke="#2a4a6a" stroke-width="2" opacity=".5"/>' for x in range(0, 600, 31))
    + casas + fuego + pinos([0, 600], y=255, h=60, seed=4)
    + glow(300, 90, 10, '#fff3b0') + '<path d="M300 100 L250 250 L350 250Z" fill="#fff3b0" opacity=".08"/>' + glow(170, 60, 5, '#ff4a4a') + glow(450, 70, 5, '#7fd8ff'), cielo=('#03020c', '#1a1036'), luna=(80, 50, 0), seed=33)
# Noche oficial de los ovnis: pantalla de radar con 21 ecos y un caza
_r = random.Random(86); _m = __import__('math')
eco = ''.join((lambda a, d: f'<circle cx="{300+int(d*_m.cos(a))}" cy="{170+int(d*_m.sin(a))}" r="4" fill="#39ff88"/>')(_r.uniform(0, 6.28), _r.uniform(30, 140)) for i in range(21))
esc['nochebrasil'] = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340" role="img"><rect width="600" height="340" fill="#020a06"/>'
    '<circle cx="300" cy="170" r="150" fill="#03160c" stroke="#1d6b3c" stroke-width="3"/>'
    + ''.join(f'<circle cx="300" cy="170" r="{r}" fill="none" stroke="#1d6b3c" stroke-width="1"/>' for r in (50, 100))
    + '<path d="M150 170 H450 M300 20 V320" stroke="#1d6b3c" stroke-width="1"/>'
    '<path d="M300 170 L440 110 A150 150 0 0 0 420 80 Z" fill="#39ff88" opacity=".18"/>' + eco
    + '<g transform="translate(470 270) rotate(-20)" fill="#8aa0c8"><path d="M0 10 L70 6 L84 10 L70 14Z"/><path d="M30 10 L16 26 L28 26 L46 10Z"/><path d="M30 10 L16 -6 L28 -6 L46 10Z"/></g>'
    '<text x="22" y="34" font-family="monospace" font-size="18" fill="#39ff88">CINDACTA · 19/05/1986</text><text x="22" y="320" font-family="monospace" font-size="18" fill="#39ff88">ECOS: 21</text></svg>')
# La Joya: desierto, volcán y un caza disparando a una esfera con cúpula
esc['lajoya'] = base('<path d="M0 250 L180 120 L240 150 L300 250Z" fill="#1a0f22" stroke="#3d2d6e" stroke-width="2"/><path d="M160 134 L180 120 L200 134Z" fill="#e8ecff" opacity=".5"/>'
    '<rect y="248" width="600" height="92" fill="#2a1a18"/>' + ''.join(f'<rect x="{x}" y="{262+(x*7)%60}" width="10" height="2" fill="#3a2620"/>' for x in range(0, 600, 23))
    + '<g transform="translate(420 90)"><ellipse rx="34" ry="12" fill="#c8ccd8"/><path d="M-22 -4 Q0 -36 22 -4Z" fill="#eef2ff"/><ellipse rx="34" ry="12" fill="none" stroke="#fff" opacity=".4"/></g>'
    + '<g transform="translate(150 170) rotate(-16)" fill="#6a7488"><path d="M0 10 L80 6 L96 10 L80 14Z"/><path d="M36 10 L20 28 L34 28 L56 10Z"/><path d="M36 10 L20 -8 L34 -8 L56 10Z"/></g>'
    + ''.join(f'<rect x="{260+i*22}" y="{150-i*9}" width="10" height="3" fill="#ffd23f" transform="rotate(-22 {260+i*22} {150-i*9})"/>' for i in range(6)), cielo=('#1a3a6a', '#e89a6a'), luna=(520, 50, 0), seed=34)
# Putre: altiplano, cerros, patrulla y una luz violeta ovalada
esc['putre'] = base('<path d="M0 230 Q90 150 180 220 Q270 140 380 215 Q480 150 600 225 V340 H0Z" fill="#120a20" stroke="#3d2d6e" stroke-width="2"/>'
    '<rect y="268" width="600" height="72" fill="#1a1222"/>'
    + '<g transform="translate(410 150)"><ellipse rx="60" ry="20" fill="#b06aff" opacity=".85"/><ellipse rx="160" ry="60" fill="#b06aff" opacity=".12"/>' + glow(-52, 0, 5, '#ff2a2a', .3) + glow(52, 0, 5, '#ff2a2a', .3) + '</g>'
    + glow(140, 100, 5, '#e6c8ff') + '<path d="M410 170 L340 275 L480 275Z" fill="#b06aff" opacity=".1"/>'
    + ''.join(f'<g transform="translate({x} 262)" fill="#05030a"><rect x="-4" y="0" width="8" height="22"/><circle cy="-6" r="6"/></g>' for x in (80, 110, 140, 170, 200))
    + '<g transform="translate(330 262)" fill="#05030a" opacity=".6"><rect x="-4" y="0" width="8" height="22"/><circle cy="-6" r="6"/></g>', cielo=('#030214', '#1e1440'), luna=(70, 50, 18), seed=35)
# Campeche: vista en infrarrojo (blanco y negro) con once puntos y plataformas en el horizonte
puntos = ''.join(f'<circle cx="{x}" cy="{y}" r="7" fill="#fff"/><circle cx="{x}" cy="{y}" r="16" fill="#fff" opacity=".18"/>' for x, y in ((120, 120), (160, 150), (205, 128), (250, 160), (300, 140), (340, 170), (380, 135), (420, 165), (460, 145), (500, 175), (540, 150)))
esc['campeche'] = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340" role="img"><defs><linearGradient id="ir" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#101010"/><stop offset="1" stop-color="#3a3a3a"/></linearGradient></defs>'
    '<rect width="600" height="340" fill="url(#ir)"/>' + puntos
    + '<rect y="250" width="600" height="90" fill="#1a1a1a"/>' + ''.join(f'<g fill="#555"><rect x="{x}" y="232" width="6" height="20"/><rect x="{x-8}" y="248" width="22" height="4"/></g><circle cx="{x+3}" cy="228" r="4" fill="#fff"/>' for x in (90, 260, 470))
    + '<path d="M300 150 m-30 0 h20 m20 0 h20 M300 150 m0 -30 v20 m0 20 v20" stroke="#fff" stroke-width="2" opacity=".7"/>'
    '<text x="18" y="30" font-family="monospace" font-size="17" fill="#fff">FLIR · 05/03/2004 · 11500 FT</text><text x="18" y="322" font-family="monospace" font-size="17" fill="#fff">BLANCOS: 11</text></svg>')
# Bariloche: lago, montañas nevadas, ciudad a oscuras y un avión con un objeto de luces al lado
esc['bariloche'] = base('<path d="M0 210 L90 120 L150 170 L230 90 L310 170 L390 110 L470 180 L540 120 L600 170 V250 H0Z" fill="#141028" stroke="#3d2d6e" stroke-width="2"/>'
    + ''.join(f'<path d="M{x-16} {y+20} L{x} {y} L{x+16} {y+20}Z" fill="#e8ecff" opacity=".55"/>' for x, y in ((90, 120), (230, 90), (390, 110), (540, 120)))
    + '<rect y="245" width="600" height="95" fill="#0a1024"/>' + ''.join(f'<path d="M{x} {262+(x*9)%60} h22" stroke="#24305a" stroke-width="2" opacity=".6"/>' for x in range(0, 600, 33))
    + '<g transform="translate(150 150) rotate(4)"><path d="M0 0 h130 q18 0 22 7 q-4 7 -22 7 h-130 q-8 -7 0 -14z" fill="#d6dbea"/><path d="M60 7 l-32 36 h13 l44 -36z" fill="#aeb4c8"/><path d="M4 2 l-12 -22 h9 l14 20z" fill="#aeb4c8"/></g>'
    + '<g transform="translate(400 130)"><ellipse rx="36" ry="10" fill="#2a2440"/>' + glow(-24, 0, 5, '#fff7c8') + glow(0, 0, 6, '#ff3030') + glow(24, 0, 5, '#fff7c8') + '</g>', cielo=('#02030c', '#141a3a'), luna=(540, 40, 0), seed=36)
for n, s in esc.items(): open(OUT + f'{n}.svg', 'w').write(s)
print(list(esc))
