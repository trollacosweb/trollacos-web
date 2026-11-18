# python3 montar.py <video> <salida> [mudo]
import subprocess,sys
v,out=sys.argv[1],sys.argv[2]; mudo=len(sys.argv)>3
F=0.45
slots=[]; a,b=0.6,47.2; n=15; d=(b-a)/n
for i in range(n): slots.append((a+i*d, a+(i+1)*d-0.25))
a,b=47.7,55.3; d=(b-a)/3
for i in range(3): slots.append((a+i*d, a+(i+1)*d-(0.2 if i<2 else 0)))
cmd=['ffmpeg','-v','error','-y','-i',v,'-loop','1','-i','capas/marca.png']
for i in range(len(slots)): cmd+=['-loop','1','-i',f'capas/t{i:02d}.png']
fl=['[0:v]scale=1080:1920:flags=lanczos,setsar=1[b0]','[1:v]format=rgba,fade=t=in:st=0.2:d=0.8:alpha=1[m]','[b0][m]overlay=0:0:shortest=1[b1]']
cur='b1'
for i,(s,e) in enumerate(slots):
    fl.append(f'[{i+2}:v]format=rgba,fade=t=in:st={s:.2f}:d={F}:alpha=1,fade=t=out:st={e-F:.2f}:d={F}:alpha=1[x{i}]')
    fl.append(f"[{cur}][x{i}]overlay=0:0:shortest=1:enable='between(t,{s:.2f},{e:.2f})'[c{i}]"); cur=f'c{i}'
cmd+=['-filter_complex',';'.join(fl),'-map',f'[{cur}]']
cmd+=(['-an'] if mudo else ['-map','0:a','-c:a','aac','-b:a','192k'])
cmd+=['-t','55.3','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-r','30','-movflags','+faststart',out]
subprocess.run(cmd,check=True); print('ok',out)
