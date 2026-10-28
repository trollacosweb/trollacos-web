import random
OUT='/home/claude/trollacos-web/misterio/img/'
def base(cont, cielo=('#05010f','#1a0b3a'), luna=(470,70,34), seed=1):
    r=random.Random(seed)
    est=''.join(f'<circle cx="{r.randint(0,600)}" cy="{r.randint(0,200)}" r="{r.choice([0.8,1,1.3])}" fill="#fff" opacity="{r.uniform(.3,.9):.2f}"/>' for _ in range(60))
    lx,ly,lr=luna
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340" role="img">
<defs><linearGradient id="c" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{cielo[0]}"/><stop offset="1" stop-color="{cielo[1]}"/></linearGradient>
<radialGradient id="l"><stop offset=".6" stop-color="#f4f1d9"/><stop offset="1" stop-color="#f4f1d9" stop-opacity="0"/></radialGradient>
<radialGradient id="h"><stop offset="0" stop-color="#cfd8ff" stop-opacity=".22"/><stop offset="1" stop-color="#cfd8ff" stop-opacity="0"/></radialGradient>
<linearGradient id="n" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9aa6d6" stop-opacity="0"/><stop offset="1" stop-color="#9aa6d6" stop-opacity=".35"/></linearGradient>
<filter id="b"><feGaussianBlur stdDeviation="2.5"/></filter></defs>
<rect width="600" height="340" fill="url(#c)"/>{est}
<circle cx="{lx}" cy="{ly}" r="{lr*3}" fill="url(#h)"/><circle cx="{lx}" cy="{ly}" r="{lr}" fill="url(#l)"/>
{cont}
<rect y="250" width="600" height="90" fill="url(#n)"/>
<ellipse cx="150" cy="300" rx="260" ry="26" fill="#c9d1ff" opacity=".08" filter="url(#b)"/><ellipse cx="460" cy="312" rx="240" ry="22" fill="#c9d1ff" opacity=".07" filter="url(#b)"/>
</svg>'''
S='#0a0418'
def ventanas(x0,y0,cols,filas,dx,dy,w,h,enc,seed):
    r=random.Random(seed);o=''
    for f in range(filas):
        for c in range(cols):
            col='#ffcf5a' if r.random()<enc else '#1b0f33'
            o+=f'<rect x="{x0+c*dx}" y="{y0+f*dy}" width="{w}" height="{h}" fill="{col}"/>'
    return o
esc={}
# Palacio de Linares: cuerpo central, dos torres con tejado amansardado, cúpula; una ventana con silueta de niña
esc['linares']=base(f'''<g fill="{S}" stroke="#3d2d6e" stroke-width="2">
<rect x="120" y="150" width="360" height="130"/><rect x="95" y="120" width="70" height="160"/><rect x="435" y="120" width="70" height="160"/>
<path d="M90 122 L130 80 L170 122Z"/><path d="M430 122 L470 80 L510 122Z"/><path d="M240 150 Q300 90 360 150Z"/><rect x="296" y="78" width="8" height="20"/>
<rect x="0" y="275" width="600" height="65"/></g>
{ventanas(140,170,8,3,42,34,18,22,.25,3)}{ventanas(108,140,2,4,26,32,14,20,.2,4)}{ventanas(448,140,2,4,26,32,14,20,.2,5)}
<rect x="476" y="140" width="14" height="20" fill="#ffefb0"/><path d="M480 160 v-9 a3 3 0 1 1 6 0 v9z" fill="{S}"/>''',seed=1)
# Siete Chimeneas: casa con 7 chimeneas y una figura blanca con antorcha en el tejado
chim=''.join(f'<rect x="{150+i*44}" y="96" width="16" height="44"/><rect x="{147+i*44}" y="92" width="22" height="6"/>' for i in range(7))
esc['chimeneas']=base(f'''<g fill="{S}" stroke="#3d2d6e" stroke-width="2"><rect x="130" y="140" width="320" height="140"/><path d="M120 142 L460 142 L440 128 L140 128Z"/>{chim}<rect x="0" y="275" width="600" height="65"/></g>
{ventanas(150,165,7,3,44,36,16,24,.3,7)}
<g><path d="M318 128 q4 -26 8 0z" fill="#f2f2ff" opacity=".9"/><circle cx="322" cy="99" r="4" fill="#f2f2ff" opacity=".9"/><path d="M328 104 l10 -12" stroke="#f2f2ff" stroke-width="2"/><circle cx="339" cy="90" r="5" fill="#ffb347"/><circle cx="339" cy="90" r="12" fill="#ffb347" opacity=".25"/></g>''',luna=(110,60,28),seed=2)
# Teatro Eslava: fachada con marquesina y luces, foco
bombillas=''.join(f'<circle cx="{180+i*20}" cy="168" r="3" fill="#ffd23f"/>' for i in range(13))
esc['eslava']=base(f'''<g fill="{S}" stroke="#3d2d6e" stroke-width="2"><rect x="140" y="80" width="320" height="200"/><path d="M140 82 L300 40 L460 82Z"/><rect x="0" y="275" width="600" height="65"/></g>
<rect x="170" y="150" width="260" height="34" fill="#2a0a3a" stroke="#ff2bd6" stroke-width="2"/>{bombillas}
<text x="300" y="146" text-anchor="middle" font-family="Georgia,serif" font-size="30" fill="#ff8be9" letter-spacing="8">ESLAVA</text>
<rect x="260" y="200" width="80" height="80" fill="#1b0f33"/><path d="M300 200 v80" stroke="{S}" stroke-width="3"/>
{ventanas(170,100,6,1,46,0,20,26,.5,9)}
<path d="M300 280 L230 340 L370 340Z" fill="#fff6c8" opacity=".12"/>''',luna=(520,58,26),seed=3)
# Ángel Caído: fuente con pedestal, ángel con alas cayendo y serpiente; árboles del Retiro
arb=''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x,y,r in ((40,210,60),(110,190,55),(520,200,65),(580,220,50),(470,220,45)))
esc['angel']=base(f'''<g fill="{S}" stroke="#3d2d6e" stroke-width="2">{arb}<rect x="0" y="262" width="600" height="80"/>
<ellipse cx="300" cy="268" rx="150" ry="16"/><rect x="250" y="200" width="100" height="62"/><rect x="236" y="190" width="128" height="14"/>
<path d="M282 190 L300 150 L320 190Z"/></g><g fill="#1a0d33" stroke="#8a6ac0" stroke-width="2">
<path d="M300 150 q-8 -10 -4 -26 q2 -8 10 -8 q8 2 6 12 q-2 10 -12 22z"/>
<path d="M300 132 q-60 -40 -78 -84 q34 18 58 52 q-8 -40 4 -70 q12 34 24 74z"/>
<path d="M312 150 q30 -6 40 10 q-16 -2 -26 4" stroke="{S}" stroke-width="6" fill="none"/></g>
<text x="300" y="242" text-anchor="middle" font-family="Georgia,serif" font-size="18" fill="#5a2a6a">666</text>''',luna=(440,64,30),seed=4)
# Chamberí: andén de metro abovedado con azulejos, farola y una silueta al fondo
azul=''.join(f'<rect x="{x}" y="{y}" width="18" height="10" fill="{"#1c3d8f" if (x//20+y//12)%2 else "#e8ecf8"}" opacity=".85"/>' for x in range(60,540,20) for y in range(150,250,12))
esc['chamberi']=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340" role="img"><defs><radialGradient id="f"><stop offset="0" stop-color="#ffeaa0" stop-opacity=".55"/><stop offset="1" stop-color="#ffeaa0" stop-opacity="0"/></radialGradient></defs>
<rect width="600" height="340" fill="#05020c"/><path d="M40 260 L40 150 Q300 -10 560 150 L560 260Z" fill="#0d0820"/>{azul}
<path d="M40 150 Q300 -10 560 150" fill="none" stroke="#e8ecf8" stroke-width="3" opacity=".6"/>
<rect x="40" y="250" width="520" height="16" fill="#3a3550"/><rect x="0" y="266" width="600" height="74" fill="#05020c"/>
<rect x="0" y="300" width="600" height="4" fill="#5c5670"/><rect x="0" y="322" width="600" height="4" fill="#5c5670"/>
<rect x="200" y="160" width="120" height="44" fill="#d9c9a0" opacity=".85"/><text x="260" y="188" text-anchor="middle" font-family="Georgia,serif" font-size="13" fill="#4a3018">CHAMBERÍ</text>
<circle cx="430" cy="110" r="60" fill="url(#f)"/><circle cx="430" cy="110" r="7" fill="#fff4c4"/>
<path d="M468 250 v-34 a8 8 0 1 1 16 0 v34z" fill="#000" opacity=".9"/><circle cx="476" cy="208" r="7" fill="#000" opacity=".9"/></svg>'''
# Ummo: bloques de pisos y un platillo con el símbolo )+(
bloques=f'<g fill="{S}" stroke="#3d2d6e" stroke-width="2"><rect x="40" y="170" width="120" height="110"/><rect x="190" y="150" width="110" height="130"/><rect x="330" y="185" width="130" height="95"/><rect x="480" y="160" width="100" height="120"/><rect x="0" y="275" width="600" height="65"/></g>'
esc['ummo']=base(bloques+ventanas(52,182,5,4,22,24,12,14,.35,11)+ventanas(202,162,4,5,26,24,14,14,.3,12)+ventanas(342,196,5,3,25,24,13,14,.3,13)+ventanas(492,172,4,4,24,24,12,14,.3,14)+'''
<g transform="translate(300 78)"><ellipse rx="70" ry="16" fill="#9aa3c4"/><ellipse cy="-8" rx="30" ry="16" fill="#c8d0ee"/><ellipse cy="6" rx="64" ry="7" fill="#6c7496"/>
<g stroke="#1a0b3a" stroke-width="3" fill="none"><path d="M-12 -2 q-6 8 0 16"/><path d="M12 -2 q6 8 0 16"/><path d="M0 -3 v18"/><path d="M-5 6 h10"/></g>
<path d="M-40 18 L-90 260 L90 260 L40 18Z" fill="#9ff6ff" opacity=".07"/></g>''',luna=(80,50,22),seed=5)
# Vallecas: bloque de viviendas de noche, una sola ventana encendida con luz fría
esc['vallecas']=base(f'''<g fill="{S}" stroke="#3d2d6e" stroke-width="2"><rect x="150" y="70" width="300" height="210"/><rect x="0" y="275" width="600" height="65"/><rect x="40" y="170" width="90" height="110"/><rect x="470" y="150" width="100" height="130"/></g>
{ventanas(170,90,7,7,40,26,22,16,.0,15)}<rect x="290" y="168" width="22" height="16" fill="#bfe6ff"/><rect x="286" y="164" width="30" height="24" fill="#bfe6ff" opacity=".18"/>''',cielo=('#020208','#12122a'),luna=(520,50,20),seed=6)
for n,s in esc.items(): open(OUT+f'{n}.svg','w').write(s)
print(list(esc))
