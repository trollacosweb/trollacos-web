from PIL import Image
OUT='/home/claude/trollacos-web/img/'
import os; os.makedirs(OUT,exist_ok=True)
base=Image.open('/home/claude/mural/trollaco-cuerpo.png').convert('RGBA')  # 32x54
K=(22,8,40,255); VERDE=(86,204,108,255)
def malvado(im):
    im=im.copy(); px=im.load()
    mapa={(31,242,255):(255,40,20),(90,190,255):(255,90,20),(170,110,255):(255,140,0),(255,43,214):(255,200,40)}
    for y in range(10,15):
        for x in range(im.width):
            r,g,b,a=px[x,y]
            if a and (r,g,b) in mapa: px[x,y]=mapa[(r,g,b)]+(255,)
    return im
def contorno(im):
    px=im.load(); out=im.copy(); op=out.load()
    for y in range(im.height):
        for x in range(im.width):
            if px[x,y][3]==0:
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    X,Y=x+dx,y+dy
                    if 0<=X<im.width and 0<=Y<im.height and px[X,Y][3]: op[x,y]=K; break
    return out
def calabaza(w=16,h=12):
    im=Image.new('RGBA',(w,h+2),(0,0,0,0)); px=im.load()
    O,o,Y=(255,140,20,255),(220,90,10,255),(255,230,90,255)
    cx=(w-1)/2
    for y in range(2,h+2):
        for x in range(w):
            nx=(x-cx)/(w/2); ny=(y-2-(h-1)/2)/(h/2)
            if nx*nx+ny*ny<=1.0:
                px[x,y]=o if (x in (int(cx-4),int(cx+5)) or abs(x-cx)<0.6) else O
    for (x,y) in ((int(cx),0),(int(cx),1),(int(cx)+1,1)): px[x,y]=(60,120,40,255)
    for x,y in ((4,5),(5,5),(4,6),(10,5),(11,5),(11,6),(7,7),(8,7),(3,9),(4,9),(5,9),(6,10),(7,9),(8,9),(9,10),(10,9),(11,9),(12,9),(4,10),(11,10)):
        if px[x,y][3]: px[x,y]=Y
    return contorno(im)
def con_calabaza(c):
    im=Image.new('RGBA',(34,56),(0,0,0,0)); im.alpha_composite(c,(1,0)); im.alpha_composite(calabaza(),(9,32))
    for x,y in ((8,38),(8,39),(9,38),(9,39),(25,38),(25,39),(24,38),(24,39)): im.putpixel((x,y),VERDE)
    return im
def con_mando(c):
    im=Image.new('RGBA',(34,56),(0,0,0,0)); im.alpha_composite(c,(1,0))
    G,g=(60,60,80,255),(30,30,44,255)
    for y in range(36,41):
        for x in range(8,26):
            if (y==36 and x in (8,25)) or (y==40 and 13<=x<=20): continue
            im.putpixel((x,y),g if y in (36,40) or x in (8,25) else G)
    for x,y in ((11,38),(10,38),(12,38),(11,37),(11,39)): im.putpixel((x,y),(200,200,220,255))
    for x,y,cc in ((21,37,(255,43,214,255)),(23,38,(31,242,255,255)),(21,39,(255,210,63,255)),(19,38,VERDE)): im.putpixel((x,y),cc)
    for x,y in ((7,38),(7,39),(26,38),(26,39)): im.putpixel((x,y),VERDE)
    return im
def asomado(c):
    im=Image.new('RGBA',(32,28),(0,0,0,0)); im.alpha_composite(c.crop((0,0,32,25)),(0,0))
    for hx in (4,23):
        for y in range(23,28):
            for x in range(hx,hx+5):
                im.putpixel((x,y),K if (x in (hx,hx+4) or y==23) else VERDE)
        im.putpixel((hx+2,24),K)
    return im
for suf,c in (('',base),('-hw',malvado(base))):
    c.save(OUT+f'trollaco{suf}.png')
    con_mando(c).save(OUT+f'trollaco-mando{suf}.png')
    asomado(c).save(OUT+f'trollaco-asomado{suf}.png')
    c.rotate(180).save(OUT+f'trollaco-colgado{suf}.png')
con_calabaza(malvado(base)).save(OUT+'trollaco-calabaza-hw.png')
calabaza().save(OUT+'calabaza.png')
bat=["......K..K......","KK....KKKK....KK","KKK..KKKKKK..KKK","KKKKKKKRKRKKKKKK",".KKKKKKKKKKKKKK.","..KK.KKKKKK.KK..",".......KK......."]
im=Image.new('RGBA',(16,7),(0,0,0,0))
for y,r in enumerate(bat):
    for x,ch in enumerate(r):
        if ch=='K': im.putpixel((x,y),(20,6,30,255))
        if ch=='R': im.putpixel((x,y),(255,60,40,255))
im.save(OUT+'murcielago.png')
