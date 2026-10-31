from PIL import Image, ImageDraw
W=40
im=Image.new('RGBA',(W,W),(0,0,0,0));d=ImageDraw.Draw(im)
K=(22,8,40,255);SK=(232,178,138,255);SKs=(201,143,106,255)
H=(157,77,255,255);Hs=(106,43,192,255);Hh=(196,140,255,255)
CY=(31,242,255,255);CYs=(12,138,149,255);PK=(255,43,214,255);PKs=(184,29,154,255);YE=(255,210,63,255);WH=(250,250,255,255)
# chaqueta
d.rounded_rectangle((5,31,34,40),radius=5,fill=PK)
d.polygon([(16,31),(23,31),(19.5,37)],fill=YE)
d.line([(14,32),(17,38)],fill=PKs);d.line([(25,32),(22,38)],fill=PKs)
# acreditación de prensa
d.rectangle((26,34,30,38),fill=WH);d.line([(27,36),(29,36)],fill=PK);d.point((28,33),fill=K)
# cuello
d.rectangle((17,25,22,31),fill=SK);d.line([(17,30),(22,30)],fill=SKs)
# pelo (detrás)
d.ellipse((8,4,31,22),fill=H);d.rectangle((8,12,13,27),fill=H);d.rectangle((26,12,31,27),fill=H)
d.line([(9,26),(13,26)],fill=Hs);d.line([(26,26),(30,26)],fill=Hs)
# cara
d.ellipse((12,10,27,27),fill=SK)
# flequillo asimétrico
d.polygon([(11,9),(29,9),(28,13),(24,12),(21,15),(18,12),(14,14),(12,12)],fill=H)
d.line([(15,7),(23,6)],fill=Hh);d.point((13,10),fill=Hs);d.point((26,11),fill=Hs)
# gafas retro
d.rectangle((14,16,18,19),outline=CY);d.rectangle((21,16,25,19),outline=CY);d.line([(19,17),(20,17)],fill=CY)
# ojos
d.rectangle((16,17,17,18),fill=K);d.point((16,17),fill=WH);d.rectangle((22,17,23,18),fill=K);d.point((22,17),fill=WH)
# mofletes y sonrisa
d.point((14,21),fill=(240,120,150,255));d.point((25,21),fill=(240,120,150,255))
d.line([(18,23),(21,23)],fill=(200,50,100,255));d.point((17,22),fill=(200,50,100,255));d.point((22,22),fill=(200,50,100,255))
d.line([(19,24),(20,24)],fill=(240,110,140,255))
# cascos gamer con micro
d.arc((8,2,31,24),start=190,end=350,fill=CY,width=2)
d.rectangle((6,13,10,20),fill=CY);d.rectangle((7,14,9,19),fill=CYs)
d.rectangle((29,13,33,20),fill=CY);d.rectangle((30,14,32,19),fill=CYs)
d.line([(9,20),(15,25)],fill=K);d.rectangle((15,24,16,25),fill=PK)
# contorno automático
px=im.load();out=im.copy();po=out.load()
for y in range(W):
    for x in range(W):
        if px[x,y][3]==0 and any(0<=x+dx<W and 0<=y+dy<W and px[x+dx,y+dy][3]>0 and px[x+dx,y+dy]!=K for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):
            po[x,y]=K
out.save('lucy-40.png')
big=out.resize((W*24,W*24),Image.NEAREST);big.save('lucy-grande.png')
# foto de perfil 1080 con fondo synthwave
bg=Image.new('RGBA',(1080,1080))
dg=ImageDraw.Draw(bg)
for y in range(1080):
    t=y/1080;c=(int(7+40*t),int(2+8*t),int(26+70*t),255);dg.line([(0,y),(1080,y)],fill=c)
sol=Image.new('RGBA',(1080,1080),(0,0,0,0));ds=ImageDraw.Draw(sol)
for y in range(150,700):
    t=(y-150)/550;col=(255,int(228-150*t),int(92+120*t),255)
    if (y//22)%4==3 and y>350: continue
    r=270;cy=420;dy=y-cy
    if abs(dy)<=r:
        w=int((r*r-dy*dy)**.5);ds.line([(540-w,y),(540+w,y)],fill=col)
bg.alpha_composite(sol)
b2=out.resize((W*24,W*24),Image.NEAREST);bg.alpha_composite(b2,(60,120))
bg.convert('RGB').save('lucy-perfil.jpg',quality=92)
print('ok')
