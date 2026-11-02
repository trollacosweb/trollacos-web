# Ilustración original: suelo de cemento con caras que «salen» de las manchas (todo generado por código)
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
W,H=1200,680; R=np.random.default_rng(1971)
S='/tmp/claude-0/-home-claude/074a85cb-bf8f-5cf1-801a-ef5ae6c1a692/scratchpad/belmez'
def ruido(esc):
    n=R.random((max(2,H//esc),max(2,W//esc)))
    return np.asarray(Image.fromarray((n*255).astype('uint8')).resize((W,H),Image.BICUBIC)).astype(float)/255
fbm=sum(ruido(e)*w for e,w in((160,.3),(60,.2),(20,.2),(6,.15),(2,.15)))
base=np.array([0.72,0.66,0.55])
a=base*(0.8+0.6*(fbm[...,None]-0.5))
# manchas de humedad
def manchas(n,rmin,rmax,blur,col,fuerza):
    z=Image.new('L',(W,H),0);d=ImageDraw.Draw(z)
    for _ in range(n):
        x,y=R.integers(0,W),R.integers(0,H);r=R.integers(rmin,rmax)
        d.ellipse((x-r,y-r*R.uniform(.5,1),x+r,y+r*R.uniform(.5,1)),fill=int(R.integers(80,255)))
    m=np.asarray(z.filter(ImageFilter.GaussianBlur(blur))).astype(float)/255*(0.6+0.8*ruido(30))
    return m.clip(0,1)[...,None]*fuerza,np.array(col)
for n,r1,r2,bl,col,f in((14,40,160,40,[0.35,0.27,0.18],.45),(30,10,50,12,[0.3,0.22,0.15],.35),(8,60,200,60,[0.2,0.22,0.25],.4)):
    m,c=manchas(n,r1,r2,bl,col,f); a=a*(1-m)+c*m
# grietas
z=Image.new('L',(W,H),0);d=ImageDraw.Draw(z)
for _ in range(5):
    x,y=float(R.integers(0,W)),float(R.integers(0,H));ang=R.uniform(0,6.28)
    pts=[(x,y)]
    for _ in range(R.integers(40,120)):
        ang+=R.normal(0,.35);x+=np.cos(ang)*6;y+=np.sin(ang)*6;pts.append((x,y))
    d.line(pts,fill=255,width=2)
gr=np.asarray(z.filter(ImageFilter.GaussianBlur(.6))).astype(float)/255
a=a*(1-gr[...,None]*.55)+np.array([0.15,0.12,0.1])*gr[...,None]*.55
a+=np.asarray(z.filter(ImageFilter.GaussianBlur(1.6)).transform((W,H),Image.AFFINE,(1,0,-1,0,1,-1))).astype(float)[...,None]/255*np.array([.12,.11,.1])
# caras: sombras difusas (cuencas, nariz, boca) que se funden con el cemento
def cara(cx,cy,s,rot,fuerza):
    z=Image.new('L',(400,400),0);d=ImageDraw.Draw(z)
    d.ellipse((120,80,280,320),fill=70)                       # óvalo de la cabeza
    d.ellipse((150,165,190,195),fill=255);d.ellipse((210,165,250,195),fill=255)   # cuencas
    d.ellipse((160,172,180,188),fill=255);d.ellipse((220,172,240,188),fill=255)
    d.polygon([(200,190),(188,245),(212,245)],fill=150)      # nariz
    d.ellipse((172,262,228,290),fill=235)                     # boca abierta
    d.arc((140,140,200,175),200,340,fill=200,width=6);d.arc((200,140,260,175),200,340,fill=200,width=6)  # cejas
    z=z.rotate(rot,resample=Image.BICUBIC).resize((int(400*s),int(400*s)),Image.BICUBIC).filter(ImageFilter.GaussianBlur(4.5*s))
    m=np.zeros((H,W));x0,y0=int(cx-200*s),int(cy-200*s)
    arr=np.asarray(z).astype(float)/255
    ys,xs=slice(max(0,y0),min(H,y0+arr.shape[0])),slice(max(0,x0),min(W,x0+arr.shape[1]))
    m[ys,xs]=arr[ys.start-y0:ys.stop-y0,xs.start-x0:xs.stop-x0]
    return m*fuerza*(0.75+0.5*ruido(40))
caras=cara(450,300,1.25,-12,1.0)+cara(880,260,.85,18,.85)+cara(720,540,.6,-30,.7)+cara(180,500,.55,8,.5)
caras=caras.clip(0,1)[...,None]
a=a*(1-caras*.85)+np.array([0.16,0.1,0.07])*caras*.85
# luz de bombilla desde arriba y viñeta fría
yy,xx=np.mgrid[0:H,0:W]
luz=np.exp(-(((xx-560)/700)**2+((yy-280)/520)**2))
a=a*(0.25+1.0*luz[...,None])*np.array([1.05,0.95,0.78])+(1-luz[...,None])*np.array([0.0,0.01,0.04])
out=Image.fromarray((a.clip(0,1)*255).astype('uint8')).filter(ImageFilter.GaussianBlur(.5))
g=R.normal(0,7,(H,W,1));out=Image.fromarray(np.clip(np.asarray(out).astype(float)+g,0,255).astype('uint8'))
out.save(f'{S}/belmez.png')
