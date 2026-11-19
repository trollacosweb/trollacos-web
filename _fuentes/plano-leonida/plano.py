# Genera plano.html (plano de Leonida estilo Trollacos) a partir de las máscaras m-tierra.png y m-urb.png
# sacadas del mapa oficial «Visit Leonida» (solo la silueta de costa, lago y zonas urbanas, simplificadas).
# python3 plano.py && node render.js
import cv2, numpy as np, json, html
K = 1652 / 1462          # escala de las coordenadas «de pantalla» que usamos para nombres y carreteras
OX = OY = 53             # borde del recuadro del mapa original
W, H = 1544, 2154
EXCL = [(135, 118, 373, 424), (214, 1514, 340, 1656), (1218, 1766, 1405, 1955), (1130, 1983, 1492, 2102)]

def fuera(x, y, w, h):
    cx, cy = x + w / 2, y + h / 2
    return any(a <= cx <= c and b <= cy <= d for a, b, c, d in EXCL)

def caminos(mask, minarea, eps):
    cs, jer = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    d = []
    for i, c in enumerate(cs):
        x, y, w, h = cv2.boundingRect(c)
        if cv2.contourArea(c) < minarea or fuera(x, y, w, h):
            continue
        es_hueco = jer[0][i][3] != -1
        if es_hueco and cv2.contourArea(c) < minarea * 3:
            continue
        a = cv2.approxPolyDP(c, eps, True)
        if len(a) < 3:
            continue
        d.append('M' + 'L'.join(f'{p[0][0]-OX:.0f} {p[0][1]-OY:.0f}' for p in a) + 'Z')
    return ''.join(d)

tierra = cv2.imread('m-tierra.png', 0)
urb = cv2.imread('m-urb.png', 0)
d_tierra = caminos(tierra, 140, 1.6)
d_urb = caminos(urb, 900, 2.5)

def P(x, y):
    return (x * K - OX, y * K - OY)

CARRETERAS = {  # nombre: puntos en coordenadas de pantalla
    '35': [(855, 337), (830, 420), (815, 500), (812, 588), (806, 700), (803, 788), (800, 900), (803, 1025), (840, 1120), (870, 1210), (897, 1322), (890, 1450), (880, 1560)],
    '1A': [(880, 1560), (862, 1630), (820, 1690), (760, 1728), (720, 1742), (650, 1772), (590, 1755), (550, 1742), (470, 1720)],
    '97': [(950, 480), (1010, 530), (1052, 583), (1080, 660), (1093, 760), (1062, 850), (1010, 925), (990, 966), (990, 1050), (1010, 1110), (970, 1150), (945, 1205), (920, 1270), (897, 1322)],
    '297': [(440, 570), (520, 560), (610, 543), (720, 535), (830, 533), (900, 505), (950, 480)],
    '404': [(470, 600), (480, 680), (480, 758), (474, 880), (478, 985), (470, 1030), (600, 1045), (731, 1043), (803, 1025), (900, 1048), (990, 1050)],
    '183': [(460, 1070), (530, 990), (615, 898), (690, 850), (760, 815)],
    '62': [(517, 825), (600, 805), (700, 800), (859, 812), (960, 810), (1050, 815)],
    '628': [(606, 447), (700, 400), (790, 360), (855, 337), (960, 300)],
    '82': [(470, 1100), (585, 1215), (700, 1290), (790, 1340)],
    '397': [(1010, 1110), (1080, 1112), (1150, 1110)],
    'c1': [(1040, 1052), (1120, 1060), (1210, 1050)],
    'c2': [(1075, 892), (1150, 884), (1225, 880)],
}
ESCUDOS = [('35', 812, 588), ('35', 803, 788), ('35', 803, 1025), ('35', 897, 1322), ('97', 1052, 583), ('97', 1093, 760), ('97', 990, 966), ('97', 945, 1205),
           ('297', 610, 543), ('297', 830, 533), ('404', 480, 758), ('404', 478, 985), ('404', 731, 1043), ('183', 615, 898), ('183', 460, 1070),
           ('62', 517, 825), ('62', 859, 812), ('628', 606, 447), ('628', 855, 337), ('82', 585, 1215), ('397', 1022, 1112), ('1A', 1012, 1382), ('1A', 720, 1742), ('1A', 550, 1742)]

# (texto, x, y, tipo)  tipo: condado | ciudad | barrio | lugar | isla | agua
L = [
 ('LUMMOX COUNTY', 725, 402, 'condado'), ('KELLY COUNTY', 610, 770, 'condado'), ('LEONARD COUNTY', 1060, 712, 'condado'),
 ('VICE-DALE COUNTY', 1035, 1225, 'condado'), ('MARIANA COUNTY', 600, 1460, 'condado'),
 ('VICE CITY', 978, 1040, 'capital'), ('VICE BEACH', 1245, 978, 'ciudad'), ('PORT GELLHORN', 445, 715, 'ciudad'),
 ('Ambrosia', 790, 713, 'ciudad'), ('Belville', 960, 792, 'ciudad'), ('Capri', 420, 1055, 'ciudad'), ('Hamlet', 818, 1371, 'ciudad'),
 ('Key Lento', 830, 1665, 'ciudad'), ('Grassrivers', 657, 1326, 'ciudad'), ('Watson Bay', 630, 1408, 'ciudad'), ('Southwind', 478, 1708, 'ciudad'),
 ('Draper Island', 358, 599, 'ciudad'), ('Bonanza', 702, 283, 'ciudad'), ('Grayson', 556, 436, 'ciudad'), ('Millport', 962, 460, 'ciudad'),
 ('Waning Sands', 1080, 646, 'ciudad'), ('Gellhorn', 514, 893, 'ciudad'), ('Emerald Springs', 671, 840, 'ciudad'), ('Belpoint', 255, 1098, 'ciudad'),
 ('Downtown', 1052, 1074, 'barrio'), ('Little Cuba', 945, 1074, 'barrio'), ('Ocean Beach', 1258, 1045, 'barrio'), ('Washington Beach', 1263, 888, 'barrio'),
 ('Vinewood Beach', 1155, 670, 'barrio'), ('Port Vice City', 1176, 1112, 'barrio'), ('La Perle', 993, 928, 'barrio'), ('Rockridge', 928, 993, 'barrio'),
 ('Crosstown', 1050, 993, 'barrio'), ('Bayside', 1050, 944, 'barrio'), ('Stockyard', 1056, 898, 'barrio'), ('Southside', 911, 1300, 'barrio'),
 ('Tequesta', 1000, 1180, 'barrio'), ('Peacock Bay', 970, 1279, 'barrio'), ('Frogswater', 647, 687, 'barrio'), ('Moreau', 753, 330, 'barrio'),
 ('VCIA · Aeropuerto', 825, 1140, 'lugar'), ('Mount Kalaga N. P.', 727, 452, 'lugar'), ('Lake Leonida', 884, 627, 'agua'),
 ('Buckskin Swamp', 700, 945, 'lugar'), ('Breakwater Quarry', 605, 1166, 'lugar'), ('Mile Zero Air Station', 403, 1748, 'lugar'),
 ('Hyde Island', 838, 229, 'isla'), ('Frampton Islands', 940, 292, 'isla'), ('Featherstone Islands', 555, 313, 'isla'), ('Zephyr Islands', 365, 509, 'isla'),
 ('Sandbars', 207, 810, 'isla'), ('Crude Islands', 275, 874, 'isla'), ('Riquezas Keys', 318, 1660, 'isla'), ('Permit Keys', 533, 1688, 'isla'),
 ('Maroon Key', 657, 1716, 'isla'), ('Abismo Key', 657, 1790, 'isla'), ('Shoeless Keys', 884, 1515, 'isla'), ('Corsair Key', 987, 1477, 'isla'),
 ('Gloriana Key', 1163, 1251, 'isla'), ('Dalton Island', 1236, 1190, 'isla'), ('Catalan Key', 1065, 1284, 'isla'), ('Leaf Links', 1132, 835, 'isla'),
 ('Bobcat Key', 480, 1283, 'isla'),
 ('OCÉANO ATLÁNTICO', 1290, 600, 'mar'), ('GOLFO DE LEONIDA', 189, 1277, 'mar'), ('ESTRECHO DE LEONIDA', 435, 1875, 'mar'),
 ('Capri Sound', 316, 1013, 'agua'), ('Borrachero Sound', 330, 820, 'agua'), ('Draper Bay', 370, 688, 'agua'), ('Catalan Bay', 1215, 1152, 'agua'), ('Leonida Bay', 550, 1522, 'agua'),
]
COLS, FILAS = 9, 13
def celda(x, y):
    c = min(COLS, int(x / (W / COLS)) + 1); f = 'ABCDEFGHIJKLM'[min(FILAS - 1, int(y / (H / FILAS)))]
    return f'{f}{c}'

def svg(claro=False):
    o = []
    o.append(f'<svg class="plano" viewBox="-46 -46 {W+92} {H+92}" xmlns="http://www.w3.org/2000/svg">')
    o.append('''<defs><linearGradient id="mar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--mar2)"/><stop offset="1" stop-color="var(--mar1)"/></linearGradient>
 <pattern id="urb" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="10" height="10" fill="var(--urb)"/><path d="M0 0V10" stroke="var(--urb2)" stroke-width="3"/></pattern>
 <filter id="brillo" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>''')
    o.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#mar)"/>')
    for i in range(1, COLS):
        x = i * W / COLS; o.append(f'<line x1="{x:.0f}" y1="0" x2="{x:.0f}" y2="{H}" class="rej"/>')
    for j in range(1, FILAS):
        y = j * H / FILAS; o.append(f'<line x1="0" y1="{y:.0f}" x2="{W}" y2="{y:.0f}" class="rej"/>')
    o.append(f'<path d="{d_tierra}" class="costa" fill-rule="evenodd" filter="url(#brillo)"/>')
    o.append(f'<path d="{d_tierra}" class="tierra" fill-rule="evenodd"/>')
    o.append(f'<path d="{d_urb}" class="urb" fill-rule="evenodd"/>')
    # montañas y pantanos (iconos)
    for x, y in [(650, 470), (700, 455), (760, 470), (590, 500), (820, 480), (690, 510)]:
        X, Y = P(x, y); o.append(f'<path d="M{X-16:.0f} {Y+12:.0f}L{X:.0f} {Y-14:.0f}L{X+16:.0f} {Y+12:.0f}" class="monte"/>')
    for x, y in [(690, 920), (720, 960), (670, 960), (620, 1320), (680, 1300), (700, 1350), (560, 1380)]:
        X, Y = P(x, y); o.append(f'<path d="M{X-12:.0f} {Y:.0f}q6-8 12 0t12 0" class="pantano"/>')
    for nom, pts in CARRETERAS.items():
        d = 'M' + 'L'.join('%.0f %.0f' % P(*p) for p in pts)
        o.append(f'<path d="{d}" class="ctra-f"/><path d="{d}" class="ctra{" cz" if nom.startswith("c") else ""}"/>')
    for x, y in [(825, 1140), (403, 1730)]:
        X, Y = P(x, y); o.append(f'<text x="{X:.0f}" y="{Y-26:.0f}" class="ico">✈</text>')
    for n, x, y in ESCUDOS:
        X, Y = P(x, y); w = 22 + 11 * len(n)
        o.append(f'<g class="escudo"><rect x="{X-w/2:.0f}" y="{Y-15:.0f}" width="{w}" height="30" rx="8"/><text x="{X:.0f}" y="{Y+8:.0f}">{n}</text></g>')
    for t, x, y, tipo in L:
        X, Y = P(x, y)
        o.append(f'<text x="{X:.0f}" y="{Y:.0f}" class="t-{tipo}">{html.escape(t)}</text>')
    for i in range(COLS):
        x = (i + .5) * W / COLS
        o.append(f'<text x="{x:.0f}" y="-14" class="coord">{i+1}</text><text x="{x:.0f}" y="{H+36}" class="coord">{i+1}</text>')
    for j in range(FILAS):
        y = (j + .5) * H / FILAS + 9
        o.append(f'<text x="-24" y="{y:.0f}" class="coord">{"ABCDEFGHIJKLM"[j]}</text><text x="{W+24}" y="{y:.0f}" class="coord">{"ABCDEFGHIJKLM"[j]}</text>')
    o.append(f'<rect x="0" y="0" width="{W}" height="{H}" class="marco"/>')
    # rosa de los vientos en el golfo
    X, Y = P(245, 1400)
    o.append(f'<g transform="translate({X:.0f} {Y:.0f})" class="rosa"><circle r="58"/><path d="M0-54L13 0L0 54L-13 0Z" class="r1"/><path d="M-54 0L0 13L54 0L0-13Z" class="r2"/><text y="-68">N</text></g>')
    # marca Trollacos abajo a la derecha (en el mar)
    X, Y = 1150, 1930
    o.append(f'<g class="marca-mapa"><text x="{X}" y="{Y}" class="mm1">TROLLACOS<tspan class="mm2">.COM</tspan></text><text x="{X}" y="{Y+40}" class="mm3">EL PLANO DE LEONIDA HECHO POR FANS</text>'
             f'<image href="trollaco.png" x="{X+168}" y="{Y-210}" width="96" height="162" style="image-rendering:pixelated"/>'
             f'<g class="boca"><rect x="{X-150}" y="{Y-200}" width="300" height="70" rx="14"/><text x="{X}" y="{Y-170}">¡Ahora sí que no</text><text x="{X}" y="{Y-140}">se pierde ni Jason!</text></g></g>')
    o.append('</svg>')
    return '\n'.join(o)

indice = sorted({(t, celda(*P(x, y)), tipo) for t, x, y, tipo in L if tipo not in ('mar',)}, key=lambda z: z[0].lower())
TIPO_TXT = {'condado': 'condado', 'capital': 'ciudad', 'ciudad': 'ciudad', 'barrio': 'barrio', 'lugar': 'lugar', 'isla': 'isla', 'agua': 'agua'}
filas_idx = ''.join(f'<li><b>{html.escape(t)}</b><i>{tipo_txt}</i><span>{c}</span></li>' for t, c, tipo in indice for tipo_txt in [TIPO_TXT[tipo]])

plantilla = open('plantilla.html', encoding='utf-8').read()
open('plano.html', 'w', encoding='utf-8').write(plantilla.replace('<!--SVG-->', svg()).replace('<!--INDICE-->', filas_idx).replace('<!--N-->', str(len(indice))))
print('ok', len(d_tierra), len(d_urb), len(indice))
