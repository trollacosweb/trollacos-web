from PIL import Image
import sys
P={'.':None,'K':(26,11,46),'G':(76,199,106),'g':(47,143,78),'L':(142,240,143),
   'H':(255,43,214),'h':(160,31,255),'V':(10,10,32),'C':(31,242,255),'M':(255,43,214),
   'W':(255,255,255),'R':(58,10,26),'P':(59,10,92),'p':(90,20,130),'Y':(255,210,63),'c':(20,140,170)}
rows=[
"................................",
"...........H.....H....H.........",
"..........HH....HH...HH.........",
".........KHHK..KHHK.KHHK........",
"........KHHHHKKHHHHKHHHHK.......",
".......KHHhHHHHHhHHHHHhHHK......",
"......KGHHHHHHHHHHHHHHHHHGK.....",
"......KGGHHhHHHHHhHHHHHHGGK.....",
".....KGGGGHHGGGGGGGGHHGGGGGK....",
".....KGLLGGGGGGGGGGGGGGGLLGK....",
"K....KGGGGGGGGGGGGGGGGGGGGGK...K",
"KGK.KKVVVVVVVVVVVVVVVVVVVVVKK.KG",
"KGGKVVCCCCCCCCCWWCCCCCCCCCCCVKGG",
"KGgGVcCCCCCCCCCCCCCCCCCCCCCcVGgG",
".KgGVMMMMMMMMMMMMMMMMMMMMMMMVGgK",
"..KGKVVVVVVVVVVVVVVVVVVVVVVVKGK.",
"...KKGGGGGGGGGGGGGGGGGGGGGGGKK..",
".....KGGGGGGGGGgGGgGGGGGGGGGK...",
".....KGGGGGGGGGGGGGGGGGGGGGGK...",
".....KGGRRRRRRRRRRRRRRRRRRGGK...",
".....KGGRWWWWWWWWWWWWWWWWRGGK...",
".....KGGGRWRRRRRRRRRRRRRRGGGK...",
"......KGGGRRRRRRRRRRRRRRGGGK....",
"......KGGGGGGGGGGGGGGGGGGGGK....",
".......KGGGGGGGGGGGGGGGGGGK.....",
"........KKGGGGGGGGGGGGGGKK......",
"..........KKKKKKKKKKKKKK........",
"............KgGGGGGGgK..........",
".......KKKKKKKGGGGGGKKKKKKK.....",
".....KPPPPPPPKKGGGGKKPPPPPPPK...",
"....KPPPPPPPPPCKKKKCPPPPPPPPPK..",
"...KPPPPPPPPPPCppppCPPPPPPPPPPK.",
]
for i,r in enumerate(rows):
    if len(r)!=32: print('fila',i,len(r))
W=32;H=len(rows)
im=Image.new('RGBA',(W,H),(0,0,0,0))
for y,r in enumerate(rows):
    for x,ch in enumerate(r[:32].ljust(32,'.')):
        c=P[ch]
        if c: im.putpixel((x,y),c+(255,))
im.save('trollaco-32.png')
im.resize((W*20,H*20),Image.NEAREST).save('trollaco-grande.png')
