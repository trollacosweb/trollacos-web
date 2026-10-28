from PIL import Image
head=Image.open('trollaco-32.png').crop((0,0,32,27))   # cabeza + cuello
W,H=32,54
im=Image.new('RGBA',(W,H),(0,0,0,0)); im.paste(head,(0,0))
px=im.load()
C={'T':(31,209,193),'t':(18,140,140),'P':(255,43,214),'U':(122,43,255),'u':(80,20,180),'Z':(240,240,255),
   'G':(86,204,108),'g':(46,140,76),'J':(127,179,255),'j':(80,130,214),'w':(245,245,250),'s':(60,40,80),'y':(255,210,63)}
def put(x,y,k):
    if 0<=x<W and 0<=y<H: px[x,y]=C[k]+(255,)
# chaqueta cortavientos (filas 27-39)
for y in range(27,40):
    x0,x1=(9,22) if y>28 else (8,23)
    for x in range(x0,x1+1):
        k='T'
        d=(x-x0)-(y-27)            # franja diagonal rosa y morada
        if 2<=d<=4: k='P'
        elif 5<=d<=6: k='U'
        if x in (15,16): k='Z' if y%2 else 'w'
        if y>=38: k='t'            # bajo elastico
        put(x,y,k)
    # cuello levantado
put(13,27,'U');put(18,27,'U');put(12,27,'U');put(19,27,'U')
# mangas moradas
for y in range(28,38):
    for x in (5,6,7): put(x+ (1 if y<30 else 0),y,'U' if x!=7 else 'u')
    for x in (24,25,26): put(x- (1 if y<30 else 0),y,'U' if x!=24 else 'u')
for x in (5,6,7,24,25,26): put(x,37,'P')            # punos rosas
for y in (38,39):                                    # manos verdes
    for x in (5,6,7,24,25,26): put(x,y,'G')
put(5,39,'g');put(26,39,'g')
# walkman amarillo en la cintura
for y in (37,38):
    for x in (20,21): put(x,y,'y')
# vaqueros lavados (40-49)
for y in range(40,50):
    for x in range(10,22):
        if y>=43 and x in (15,16): continue
        k='J'
        if (x+y)%5==0: k='j'
        if x in (10,21): k='j'
        put(x,y,k)
# zapatillas altas blancas con raya rosa (50-53)
for y in range(50,54):
    for x in list(range(8,15))+list(range(17,24)):
        k='w'
        if y==51 and x not in (8,23): k='P'
        if y==53: k='s'
        put(x,y,k)
# contorno automatico
out=im.copy(); op=out.load()
for y in range(26,H):
    for x in range(W):
        if px[x,y][3]==0:
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                X,Y=x+dx,y+dy
                if 0<=X<W and 0<=Y<H and Y>=27 and px[X,Y][3]:
                    op[x,y]=(22,8,40,255); break
out.save('trollaco-cuerpo.png')
big=out.resize((W*16,H*16),Image.NEAREST)
bg=Image.new('RGBA',big.size,(20,6,58,255)); bg.alpha_composite(big); bg.convert('RGB').save('/tmp/claude-0/-home-claude/074a85cb-bf8f-5cf1-801a-ef5ae6c1a692/scratchpad/cuerpo.png')
