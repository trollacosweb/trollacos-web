# Reel vertical «Expediente Trollaco»: fotogramas con PIL -> ffmpeg
import sys, subprocess, re, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0,'/home/claude/trollacos-web/_fuentes/generadores/misterio'); import casos as C
D='/tmp/claude-0/-home-claude/074a85cb-bf8f-5cf1-801a-ef5ae6c1a692/scratchpad/reel'; WEB='/home/claude/trollacos-web'
W,H,FPS=1080,1920,30; INTRO,CASO,OUTRO=2.5,1.5,3.5
B='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'; M='/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
F=lambda p,s:ImageFont.truetype(p,s)
VERDE=(124,255,178); AMAR=(255,210,63); ROSA=(255,43,214)
REG={**{c['id']:'MADRID' for c in C.CASOS+C.SIERRA},**{c['id']:'ESPAÑA' for c in C.ESPANA},**{c['id']:'EL MUNDO' for c in C.MUNDO}}
todos={c['id']:c for c in C.CASOS+C.SIERRA+C.ESPANA+C.MUNDO}
orden=['palacio-de-linares','roswell','estacion-chamberi','manises','tic-tac-nimitz','teatro-eslava','caras-de-belmez','rendlesham',
 'casa-de-las-siete-chimeneas','ovni-de-canarias','angel-caido','luces-de-phoenix','caso-ummo','sanatorio-de-la-marina','hospital-del-torax','la-barranca','caso-vallecas']
tro=Image.open(f'{WEB}/misterio/img/trollaco-linterna.png').convert('RGBA')
def limpio(t): return re.sub('<[^>]+>','',t)
def wrap(d,txt,font,maxw):
    out=[];l=''
    for w in txt.split():
        p=(l+' '+w).strip()
        if d.textlength(p,font=font)<=maxw: l=p
        else: out.append(l); l=w
    out.append(l); return out
def centro(d,y,txt,font,fill,sombra=True):
    w=d.textlength(txt,font=font)
    if sombra: d.text(((W-w)/2+3,y+3),txt,font=font,fill=(0,0,0))
    d.text(((W-w)/2,y),txt,font=font,fill=fill)
def estrellas(seed=1):
    r=np.random.default_rng(seed); a=np.zeros((H,W,3),np.uint8); a[:]= (7,2,26)
    for _ in range(500): x,y=r.integers(0,W),r.integers(0,H); a[y,x]=(r.integers(120,255),)*3
    return Image.fromarray(a)
FONDO=estrellas()
def sprite(s): return tro.resize((tro.width*s,tro.height*s),Image.NEAREST)
cache={}
def prep(cid):
    if cid in cache: return cache[cid]
    c=todos[cid]; im=Image.open(f'{WEB}/misterio/img/{c["img"]}.webp').convert('RGB')
    bg=im.copy(); r=max(W/bg.width,H/bg.height); bg=bg.resize((int(bg.width*r)+2,int(bg.height*r)+2)).crop((0,0,W,H)).filter(ImageFilter.GaussianBlur(28))
    bg=Image.blend(bg,Image.new('RGB',(W,H),(5,1,15)),.6)
    cache[cid]=(c,im,bg); return cache[cid]
def frame_caso(i,cid,t):
    c,im,bg=prep(cid); fr=bg.copy(); d=ImageDraw.Draw(fr)
    # imagen con zoom lento (Ken Burns), caja de 1000 de ancho
    bw=1000; bh=min(900,int(bw*im.height/im.width)) if im.width>=im.height else 900
    z=1.0
    r=max(bw/im.width,bh/im.height)*z; sm=im.resize((int(im.width*r),int(im.height*r)),Image.LANCZOS)
    ox,oy=(sm.width-bw)//2,(sm.height-bh)//2; sm=sm.crop((ox,oy,ox+bw,oy+bh))
    x0,y0=(W-bw)//2,650-bh//2+90
    glow=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(glow).rounded_rectangle((x0-10,y0-10,x0+bw+10,y0+bh+10),24,fill=(*VERDE,140))
    fr.paste(Image.alpha_composite(fr.convert('RGBA'),glow.filter(ImageFilter.GaussianBlur(18))).convert('RGB'))
    d=ImageDraw.Draw(fr); d.rounded_rectangle((x0-4,y0-4,x0+bw+4,y0+bh+4),18,outline=VERDE,width=4)
    fr.paste(sm,(x0,y0))
    # sello
    s=Image.new('RGBA',(330,74),(0,0,0,0)); sd=ImageDraw.Draw(s); sd.rectangle((2,2,327,71),fill=(184,0,31),outline=(255,255,255),width=4)
    sd.text((22,12),f'CASO {i+1:02d}/17',font=F(M,40),fill=(255,255,255)); s=s.rotate(5,expand=True,resample=Image.BICUBIC)
    fr.paste(s,(x0-14,y0-44),s)
    d=ImageDraw.Draw(fr)
    centro(d,150,'> EXPEDIENTE TROLLACO_',F(M,46),VERDE)
    y=y0+bh+50
    centro(d,y,REG[cid]+' · '+limpio(c['cuando']).upper()[:24],F(M,34),VERDE); y+=62
    for l in wrap(d,c['titulo'],F(B,72),980): centro(d,y,l,F(B,72),(255,255,255)); y+=88
    for l in wrap(d,c['sub'],F(B,42),960): centro(d,y+6,l,F(B,42),AMAR); y+=56
    y+=26; txt='NIVEL DE MIEDO '; fm=F(M,34); w=d.textlength(txt,font=fm)+5*44; xx=(W-w)/2
    d.text((xx,y),txt,font=fm,fill=(220,230,225)); xx+=d.textlength(txt,font=fm)
    for k in range(5): d.rounded_rectangle((xx+k*44,y+4,xx+k*44+34,y+38),6,fill=VERDE if k<c['nivel'] else (50,60,70))
    # pie
    sp=sprite(3); fr.paste(sp,(110,H-250),sp); d.text((110+sp.width+24,H-205),'trollacos.com/misterio',font=F(B,46),fill=(255,255,255))
    # destello / glitch al entrar
    if t<0.12:
        a=np.asarray(fr).astype(np.int16); sh=int(40*(1-t/0.12)); a=np.roll(a,sh,axis=1); a[...,0]=np.roll(a[...,0],-sh//2,axis=1)
        a=np.clip(a+int(110*(1-t/0.12)),0,255); fr=Image.fromarray(a.astype(np.uint8))
    return fr
def frame_intro(t):
    fr=FONDO.copy(); d=ImageDraw.Draw(fr)
    # haz de linterna
    sp=sprite(7); px,py=(W-sp.width)//2,1050
    sx,sy=px+sp.width-10,py+int(sp.height*0.45)
    beam=Image.new('L',(W,H),0); bd=ImageDraw.Draw(beam)
    ang=-1.05+0.45*np.sin(t*1.8); L=1700
    bd.polygon([(sx,sy),(sx+L*np.cos(ang-.2),sy+L*np.sin(ang-.2)),(sx+L*np.cos(ang+.2),sy+L*np.sin(ang+.2))],fill=170)
    fr=Image.composite(Image.new('RGB',(W,H),(200,255,220)),fr,beam.filter(ImageFilter.GaussianBlur(28))); d=ImageDraw.Draw(fr)
    fr.paste(sp,(px,py),sp)
    a=min(1,t/0.6)
    col=tuple(int(v*a) for v in VERDE)
    centro(d,330,'EXPEDIENTE',F(B,140),(int(234*a),int(255*a),int(243*a))); centro(d,480,'TROLLACO',F(B,160),col)
    if t>0.9: centro(d,730,'17 casos que nadie',F(B,62),AMAR); centro(d,805,'supo explicar',F(B,62),AMAR)
    if t>1.6: centro(d,1560,'¿Cuál te da más miedo?',F(B,52),(255,255,255))
    return fr
def frame_outro(t):
    fr=FONDO.copy(); d=ImageDraw.Draw(fr)
    # mosaico de fondo con todas las imágenes
    for k,cid in enumerate(orden[:12]):
        _,im,_=prep(cid); th=im.copy(); th.thumbnail((360,300)); th=th.resize((360,240)) 
        x,y=(k%3)*360,(k//3)*240+60; fr.paste(Image.blend(th,Image.new('RGB',th.size,(5,1,15)),.72),(x,y))
    d=ImageDraw.Draw(fr)
    esc=min(1,t/0.35); f1=F(B,int(150*(0.6+0.4*esc)))
    centro(d,620,'¿TE',f1,(255,255,255)); centro(d,790,'ATREVES?',f1,VERDE)
    if t>0.6:
        d.rounded_rectangle((120,1100,W-120,1250),30,fill=(7,2,26),outline=VERDE,width=6)
        centro(d,1132,'trollacos.com/misterio',F(B,64),(255,255,255),sombra=False)
    if t>1.1: centro(d,1310,'Enlace en la bio 👆'.replace(' 👆',''),F(M,46),AMAR)
    if t>1.4: centro(d,1400,'Cada lunes, un caso nuevo de la semana',F(B,40),(220,230,225))
    sp=sprite(5); fr.paste(sp,((W-sp.width)//2,1560),sp)
    return fr
total=INTRO+CASO*17+OUTRO; n=int(total*FPS)
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',f'{D}/musica.wav',
  '-c:v','libx264','-pix_fmt','yuv420p','-crf','21','-preset','medium','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',f'{D}/expediente-trollaco.mp4'],stdin=subprocess.PIPE)
for k in range(n):
    t=k/FPS
    if t<INTRO: fr=frame_intro(t)
    elif t<INTRO+CASO*17:
        i=int((t-INTRO)//CASO); fr=frame_caso(i,orden[i],(t-INTRO)-i*CASO)
    else: fr=frame_outro(t-INTRO-CASO*17)
    p.stdin.write(fr.convert('RGB').tobytes())
    if k in (40,200,900): fr.save(f'{D}/f{k}.png')
p.stdin.close(); p.wait(); print('ok',n)
