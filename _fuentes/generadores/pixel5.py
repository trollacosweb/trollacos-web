from PIL import Image
P={'.':None,'K':(22,8,40),'G':(140,84,255),'g':(92,46,190),'L':(196,160,255),'d':(60,26,130),
   'H':(31,242,255),'h':(20,150,200),'V':(10,10,32),'1':(31,242,255),'2':(90,190,255),'3':(170,110,255),'4':(255,43,214),
   'W':(255,255,255),'R':(60,8,30),'r':(120,20,60),'P':(40,12,60),'p':(80,20,110),'C':(255,43,214),'Y':(255,210,63)}
# mitad izquierda (16 columnas); se refleja para hacer la cara simétrica
L=[
"................",  #0
".............H..",  #1
"..........H..HH.",  #2
".........KHHKHHH",  #3
"........KHHHHHHh",  #4
".......KHHhHHHHH",  #5
"K.....KGHHHHHhHH",  #6
"KK....KGGHHHHHHH",  #7
"KGK..KGGGGGHHGGG",  #8
"KGGK.KGLLGGGGGGG",  #9
"KGgGKKGGGGGGGGGG",  #10
".KGGKVVVVVVVVVVV",  #11
".KGGV11111111111",  #12 (gradiente se pinta luego)
"..KgV11111111111",  #13
"..KgKVVVVVVVVVVV",  #14
"...KKGGGGGGGGGGG",  #15
".....KGGGGGGGGGG",  #16
".....KGGGGGGGGGG",  #17
".....KGGGGGGGGGG",  #18
".....KGGGGGGGGGG",  #19
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
nose={16:{14:'g',15:'G',16:'G',17:'g'},17:{13:'g',14:'G',15:'L',16:'G',17:'G',18:'g'},18:{13:'g',14:'G',15:'G',16:'G',17:'G',18:'g'},19:{14:'d',15:'g',16:'g',17:'d'}}
for y,d in nose.items():
    for x,ch in d.items(): rows[y][x]=ch
mouth={
20:"......KGRGGGGGGGGGGGGGGGRRK.....",
21:"......KGGRRRRRRRRRRRRRRRRGK.....",
22:"......KGGGRWWWWWWWWWWWWRRGK.....",
23:"......KGGGGRRWRRRRRRRRGGGGK.....",
}
for y,s in mouth.items():
    s=s.ljust(32,'.')
    for x,ch in enumerate(s):
        if 6<=x<=26 and ch!='.' : rows[y][x]=ch
# limpiar bordes de la mandibula

im=Image.new('RGBA',(32,32),(0,0,0,0))
for y,r in enumerate(rows):
    for x,ch in enumerate(r):
        c=P.get(ch)
        if c: im.putpixel((x,y),c+(255,))
im.save('trollaco-c-32.png')
big=im.resize((640,640),Image.NEAREST); big.save('trollaco-c-grande.png')
bg=Image.new('RGBA',big.size,(20,6,58,255)); bg.alpha_composite(big); bg.convert('RGB').save('/tmp/claude-0/-home-claude/074a85cb-bf8f-5cf1-801a-ef5ae6c1a692/scratchpad/troll4.png')
