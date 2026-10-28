from PIL import Image
OUT='/home/claude/trollacos-web/misterio/img/'
base=Image.open('/home/claude/mural/trollaco-cuerpo.png').convert('RGBA')  # 32x54
K=(22,8,40,255);G=(86,204,108,255);g=(46,140,76,255);U=(122,43,255,255);u=(80,20,180,255);P=(255,43,214,255)
W=(245,245,250,255);Y=(255,210,63,255);GR=(60,60,80,255);DG=(30,30,44,255)
def lienzo(): 
    c=Image.new('RGBA',(64,64),(0,0,0,0)); return c
def sin_brazos(im):
    im=im.copy();px=im.load()
    for y in range(27,41):
        for x in list(range(3,9))+list(range(23,29)):
            if 0<=x<32: px[x,y]=(0,0,0,0)
    return im
def contorno(im):
    px=im.load();out=im.copy();op=out.load()
    for y in range(im.height):
        for x in range(im.width):
            if px[x,y][3]==0:
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    X,Y_=x+dx,y+dy
                    if 0<=X<im.width and 0<=Y_<im.height and px[X,Y_][3] and px[X,Y_]!=K: op[x,y]=K;break
    return out
def put(px,pts,c):
    for x,y in pts: px[x,y]=c
def rect(px,x0,y0,x1,y1,c):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1): px[x,y]=c
OX,OY=16,8  # donde va el cuerpo en el lienzo 64x64
def cuerpo(arms=False):
    c=lienzo(); c.alpha_composite(base if arms else sin_brazos(base),(OX,OY)); return c
# brazo colgando (original) helper: dibuja brazo izq/der colgando
def brazo_colgando(px,lado):
    xs=(OX+5,OX+6,OX+7) if lado=='i' else (OX+24,OX+25,OX+26)
    for y in range(OY+28,OY+38):
        for x in xs: px[x,y]=U
    for x in xs: px[x,OY+37]=P
    for y in (OY+38,OY+39):
        for x in xs: px[x,y]=G
def brazo_horizontal(px,lado,y=OY+30,largo=8):
    if lado=='d':
        x0=OX+23; rect(px,x0,y,x0+largo,y+2,U); rect(px,x0+largo-1,y,x0+largo-1,y+2,P); rect(px,x0+largo,y-1,x0+largo+2,y+3,G); return (x0+largo+2,y+1)
    else:
        x0=OX+8; rect(px,x0-largo,y,x0,y+2,U); rect(px,x0-largo+1,y,x0-largo+1,y+2,P); rect(px,x0-largo-3,y-1,x0-largo-1,y+3,G); return (x0-largo-3,y+1)
def brazo_arriba(px,lado):
    if lado=='d': xs=range(OX+24,OX+27)
    else: xs=range(OX+5,OX+8)
    for y in range(OY+16,OY+30):
        for x in xs: px[x,y]=U
    for x in xs: px[x,OY+17]=P
    for y in (OY+13,OY+14,OY+15):
        for x in xs: px[x,y]=G
poses={}
# 1) linterna
c=cuerpo();px=c.load();brazo_colgando(px,'i');mx,my=brazo_horizontal(px,'d')
rect(px,mx,my-1,mx+5,my+1,GR);rect(px,mx+5,my-2,mx+6,my+2,(200,200,220,255));
haz=Image.new('RGBA',(64,64),(0,0,0,0));hp=haz.load()
for x in range(mx+7,64):
    h=int((x-mx-7)*0.45)+2
    for y in range(my-h,my+h+1):
        if 0<=y<64: hp[x,y]=(255,236,120,max(60,200-(x-mx)*6))
c=contorno(c);c.alpha_composite(haz);poses['linterna']=c
# 2) lupa
c=cuerpo();px=c.load();brazo_colgando(px,'i');mx,my=brazo_horizontal(px,'d',y=OY+29,largo=4)
# mango y lente delante del ojo derecho
for i in range(7): px[mx-1-i//3,my-1-i]=(140,80,40,255)
cx_,cy_=OX+22,OY+13
for y in range(cy_-8,cy_+9):
    for x in range(cx_-8,cx_+9):
        d=(x-cx_)**2+(y-cy_)**2
        if 0<=x<64 and 0<=y<64:
            if 42<=d<=64: px[x,y]=(90,90,110,255)
            elif d<42: 
                r,g_,b,a=px[x,y]
                px[x,y]=(min(255,r+60),min(255,g_+60),min(255,b+80),255) if a else (190,235,255,255)
put(px,[(cx_-3,cy_-4),(cx_-4,cy_-3),(cx_-2,cy_-4)],(255,255,255,255))
c=contorno(c);poses['lupa']=c
# 3) asustado (brazos arriba, pelo de punta, gotas de sudor)
c=cuerpo();px=c.load();brazo_arriba(px,'i');brazo_arriba(px,'d')
for x in range(OX+10,OX+22,2):
    for y in range(OY-3,OY+1): px[x,y]=P
for (x,y) in ((OX+3,OY+6),(OX+3,OY+7),(OX+29,OY+4),(OX+29,OY+5),(OX+2,OY+10)): px[x,y]=(140,220,255,255)
c=contorno(c);poses['asustado']=c
# 4) disfrazado de fantasma (sábana)
c=lienzo();px=c.load()
cxs=OX+16
for y in range(OY+2,OY+52):
    if y<OY+16: half=int(13*((y-OY-2)/14)**0.5)+1
    else: half=14+ (1 if (y//3)%2 else 0)
    for x in range(cxs-half,cxs+half+1): px[x,y]=W
# borde inferior ondulado
for x in range(cxs-15,cxs+16):
    if (x//4)%2:
        for y in range(OY+50,OY+53): px[x,y]=(0,0,0,0)
# ojos (huecos) con el visor dentro
rect(px,cxs-8,OY+14,cxs-3,OY+17,(31,242,255,255));rect(px,cxs+3,OY+14,cxs+8,OY+17,(255,43,214,255))
# orejas verdes asomando
put(px,[(cxs-15,OY+9),(cxs-16,OY+8),(cxs-14,OY+10),(cxs+15,OY+9),(cxs+16,OY+8),(cxs+14,OY+10)],G)
# cresta rosa por arriba
for x in range(cxs-4,cxs+5,2): put(px,[(x,OY),(x,OY+1)],P)
# zapatillas
rect(px,cxs-8,OY+52,cxs-2,OY+54,W);rect(px,cxs-8,OY+53,cxs-2,OY+53,P);rect(px,cxs+2,OY+52,cxs+8,OY+54,W);rect(px,cxs+2,OY+53,cxs+8,OY+53,P)
c=contorno(c);poses['fantasma']=c
# 5) cámara de fotos con flash
c=cuerpo();px=c.load()
rect(px,OX+8,OY+30,OX+23,OY+31,U)
rect(px,OX+9,OY+32,OX+22,OY+38,DG);rect(px,OX+10,OY+33,OX+21,OY+37,GR);
for y in range(OY+33,OY+38):
    for x in range(OX+13,OX+19):
        if (x-OX-16)**2+(y-OY-35)**2<=6: px[x,y]=(31,242,255,255)
rect(px,OX+19,OY+30,OX+21,OY+31,W)
rect(px,OX+7,OY+33,OX+8,OY+36,G);rect(px,OX+23,OY+33,OX+24,OY+36,G)
c=contorno(c)
fl=c.load();fx,fy=OX+20,OY+27
for i in range(1,7): 
    for (dx,dy) in ((i,-i),(i,0),(0,-i),(-i,-i),(i,i)):
        if 0<=fx+dx<64 and 0<=fy+dy<64 and fl[fx+dx,fy+dy][3]==0: fl[fx+dx,fy+dy]=(255,255,200,255-i*30)
poses['camara']=c
# 6) leyendo expediente secreto
c=cuerpo();px=c.load()
rect(px,OX+6,OY+28,OX+25,OY+40,(214,180,110,255));rect(px,OX+6,OY+28,OX+25,OY+29,(180,140,70,255))
rect(px,OX+9,OY+32,OX+22,OY+35,(200,30,40,255))
rect(px,OX+4,OY+33,OX+5,OY+36,G);rect(px,OX+26,OY+33,OX+27,OY+36,G)
c=contorno(c);poses['expediente']=c
# 7) ovni (para la abducción)
ov=Image.new('RGBA',(40,20),(0,0,0,0));op=ov.load()
for y in range(20):
    for x in range(40):
        dx=(x-19.5)/19.5; dy=(y-12)/5.5
        if dx*dx+dy*dy<=1: op[x,y]=(150,160,190,255) if y<12 else (100,110,140,255)
        if ((x-19.5)/8)**2+((y-6)/6)**2<=1 and y<12: op[x,y]=(31,242,255,200)
for x in (6,13,20,27,34): 
    if op[x,13][3]: op[x,13]=(255,210,63,255)
ov=contorno(ov);poses['ovni']=ov
for n,im in poses.items():
    im.save(OUT+f'trollaco-{n}.png') if n!='ovni' else im.save(OUT+'ovni.png')
prev=Image.new('RGBA',(64*7+20,70),(20,6,58,255));x=0
for n in ['linterna','lupa','asustado','fantasma','camara','expediente']:
    prev.alpha_composite(poses[n],(x,3));x+=66
prev.alpha_composite(poses['ovni'],(x,20))
prev.resize((prev.width*4,prev.height*4),Image.NEAREST).save('/tmp/claude-0/-home-claude/074a85cb-bf8f-5cf1-801a-ef5ae6c1a692/scratchpad/poses.png')
