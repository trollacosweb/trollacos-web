from PIL import Image
P={'.':None,'K':(22,8,40),'G':(86,204,108),'g':(46,140,76),'L':(150,240,150),'d':(30,100,56),
   'H':(255,43,214),'h':(170,30,255),'V':(10,10,32),'1':(31,242,255),'2':(90,190,255),'3':(170,110,255),'4':(255,43,214),
   'W':(255,255,255),'R':(60,8,30),'r':(120,20,60),'P':(59,10,92),'p':(100,24,140),'C':(31,242,255),'Y':(255,210,63)}
# mitad izquierda (16 columnas); se refleja para hacer la cara simétrica
L=[
"................",  #0
".............H..",  #1
"..........H..HH.",  #2
".........KHHKHHH",  #3
"........KHHHHHHh",  #4
".......KHHhHHHHH",  #5
"......KGHHHHHhHH",  #6
"K.....KGGHHHHHHH",  #7
"KK...KGGGGGHHGGG",  #8
"KGK..KGLLGGGGGGG",  #9
"KGGK.KGGGGGGGGGG",  #10
".KGGKVVVVVVVVVVV",  #11
".KGGV11111111111",  #12 (gradiente se pinta luego)
"..KgV11111111111",  #13
"..KgKVVVVVVVVVVV",  #14
"...KKGGGGGGGGGGG",  #15
".....KGGGGGGGgGG",  #16
".....KGGGGGGgLGG",  #17
".....KGGGGGGgGGG",  #18
".....KGGGGGGGgGG",  #19
".....KGGGGGGGGGG",  #20
".....KGGGGGGGGGG",  #21
"......KGGGGGGGGG",  #22
".......KGGGGGGGG",  #23
"........KKGGGGGG",  #24
"..........KKKKKK",  #25
"............KgGG",  #26
".......KKKKKKKGG",  #27
".....KPPPPPPPKKG",  #28
"....KPPPPPPPPPCK",  #29
"...KPPPPPPPPPPCp",  #30
"..KPPPPPPPPPPPCp",  #31
]
rows=[]
for r in L:
    assert len(r)==16,(r,len(r))
    rows.append(list(r+r[::-1]))
# visor: degradado cian -> violeta -> rosa de izquierda a derecha
grad=['1','1','1','2','2','2','2','3','3','3','3','4','4','4','4','4']
for y in (12,13):
    for x in range(5,27):
        rows[y][x]=grad[min(15,int((x-5)/22*16))]
rows[12][9]='W';rows[12][10]='W';rows[13][8]='W'   # reflejo
rows[11][4]='V';rows[11][27]='V'
# boca: sonrisa picara asimetrica (mas alta a la derecha) con colmillo
mouth={
19:"......KGGGGGGGGGGGGGGGGGRR.K....",
20:"......KGRRGGGGGGGGGGGGGRRrK.....",
21:"......KGGRRRRRRRRRRRRRRRRGK.....",
22:"......KGGGRWWWWWWWWWWWRRGK......",
23:"......KGGGGRRWRRRRRRRRGGK.......",
}
for y,s in mouth.items():
    s=s.ljust(32,'.')
    for x,ch in enumerate(s):
        if 6<=x<=26 and ch!='.' : rows[y][x]=ch
# limpiar bordes de la mandibula
for y in (19,20,21,22,23):
    rows[y][26]= 'K' if y<22 else rows[y][26]
im=Image.new('RGBA',(32,32),(0,0,0,0))
for y,r in enumerate(rows):
    for x,ch in enumerate(r):
        c=P.get(ch)
        if c: im.putpixel((x,y),c+(255,))
im.save('trollaco-32.png')
big=im.resize((640,640),Image.NEAREST); big.save('trollaco-grande.png')
bg=Image.new('RGBA',big.size,(20,6,58,255)); bg.alpha_composite(big); bg.convert('RGB').save('/tmp/claude-0/-home-claude/074a85cb-bf8f-5cf1-801a-ef5ae6c1a692/scratchpad/troll2.png')
