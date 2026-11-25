import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
im=cv2.imread('trineo-original.jpg')
# (rect texto, lineas nuevas, centro x, centro y, alto letra, tracking)
B=[((57,365,133,478),['TROLLACOS'],95,425,64,1),
   ((171,390,237,480),['TROLLACOS','.COM'],203,428,54,0.5),
   ((630,443,746,513),['TROLLACOS'],687,466,96,1.5),
   ((626,762,768,832),['TROLLACOS','.COM'],688,797,118,1.5)]
g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
mask=np.zeros(g.shape,np.uint8)
for (x0,y0,x1,y1),*_ in B:
    z=g[y0:y1,x0:x1]; m=(z>z.mean()+25).astype(np.uint8)*255
    mask[y0:y1,x0:x1]=m
mask=cv2.dilate(mask,np.ones((5,5),np.uint8),2)
out=cv2.inpaint(im,mask,5,cv2.INPAINT_TELEA)
pil=Image.fromarray(cv2.cvtColor(out,cv2.COLOR_BGR2RGB)).convert('RGBA')
F='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
for (r,lines,cx,cy,W,tr) in B:
    capa=Image.new('RGBA',pil.size,(0,0,0,0));d=ImageDraw.Draw(capa)
    sz=40
    while True:
        f=ImageFont.truetype(F,sz); w=sum(d.textlength(c,font=f)+tr for c in 'TROLLACOS')-tr
        if w<=W: break
        sz-=1
    h=sz*0.78
    tot=len(lines)*h*1.25; y=cy-tot/2
    for ln in lines:
        w=sum(d.textlength(c,font=f)+tr for c in ln)-tr; x=cx-w/2
        for c in ln:
            d.text((x,y),c,font=f,fill=(215,215,215,235)); x+=d.textlength(c,font=f)+tr
        y+=h*1.25
    capa=capa.filter(ImageFilter.GaussianBlur(0.9 if h<20 else 0.7))
    pil.alpha_composite(capa)
pil.convert('RGB').save('trineo-sin-carteles.jpg',quality=96)
