# Música 8-bit de misterio propia (numpy). Uso: python3 musica_misterio.py salida.wav DURACION
import numpy as np, wave, sys
SR=44100; DUR=float(sys.argv[2]); N=int(SR*DUR); mix=np.zeros(N); BPM=120; neg=60/BPM
f=lambda m:440*2**((m-69)/12)
def sq(fr,d,duty=.5): t=np.arange(int(SR*d))/SR; return np.where((t*fr)%1<duty,1.,-1.)
def tri(fr,d): t=np.arange(int(SR*d))/SR; return 2*np.abs(2*((t*fr)%1)-1)-1
def env(x,a=.005,r=.08):
    n=len(x); e=np.ones(n); ai=max(1,int(a*SR)); ri=min(n,int(r*SR)); e[:ai]=np.linspace(0,1,ai); e[n-ri:]*=np.linspace(1,0,ri); return x*e
def pon(x,t,v):
    i=int(t*SR); j=min(N,i+len(x))
    if 0<=i<N: mix[i:j]+=v*x[:j-i]
INTRO=2.5; CASO=1.5; NC=17; OUT=INTRO+CASO*NC
# dron grave (re menor) con trémolo
t=np.arange(N)/SR
dron=(tri(f(38),DUR)[:N]*.6+tri(f(45),DUR)[:N]*.4)*(0.7+0.3*np.sin(2*np.pi*.5*t))
mix+=dron*.16
# arpegio inquietante: Dm  Bb  Gm  A (con la 2ª menor de tensión)
acordes=[[62,65,69,74],[58,62,65,70],[55,58,62,67],[57,61,64,69]]
comp=4*neg
for c in range(int(DUR/comp)+1):
    ac=acordes[c%4]; t0=c*comp
    if t0<INTRO-0.01: continue
    for k in range(16):
        nota=ac[[0,2,1,3,2,1,3,2][k%8]]+(12 if k>=8 else 0)
        pon(env(sq(f(nota),neg/4*.85,.125),r=.04),t0+k*neg/4,.06)
    for k in range(4):   # latido
        for dt,v in((0,.55),(.18,.35)):
            kick=np.sin(2*np.pi*np.cumsum(np.linspace(110,38,int(SR*.16)))/SR)*np.linspace(1,0,int(SR*.16))
            pon(kick,t0+k*neg+dt,v)
        pon(np.random.uniform(-1,1,int(SR*.025))*np.linspace(1,0,int(SR*.025)),t0+k*neg+neg/2,.05)
# golpe en cada caso nuevo
for i in range(NC):
    t0=INTRO+i*CASO
    pon(env(sq(f(86-(i%4)),.12,.25),r=.1),t0,.08)
    pon(np.random.uniform(-1,1,int(SR*.08))*np.linspace(1,0,int(SR*.08))**2,t0,.12)
# intro: subida de ruido y nota que se tuerce
pon(np.random.uniform(-1,1,int(SR*2.3))*np.linspace(0,1,int(SR*2.3))**3,0.1,.12)
x=np.arange(int(SR*2.2))/SR; pon(np.sign(np.sin(2*np.pi*np.cumsum(np.linspace(f(74),f(73),len(x)))/SR))*np.linspace(.2,1,len(x)),0.2,.06)
# final: golpe grave y cola
pon(env(tri(f(26),2.5),r=2.3),OUT,.6); pon(env(sq(f(50),2.5,.5),r=2.3),OUT,.12); pon(env(sq(f(57),2.5,.5),r=2.3),OUT,.08)
mix[-int(SR*.8):]*=np.linspace(1,0,int(SR*.8))
mix=mix/np.max(np.abs(mix))*.85
w=wave.open(sys.argv[1],'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes()); w.close()
