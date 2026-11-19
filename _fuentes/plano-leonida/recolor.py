# Versión PERSONAL (no publicar) del mapa oficial con la paleta Trollacos: python3 recolor.py
import cv2, numpy as np
im = cv2.imread('referencia-visit-leonida.jpg').astype(np.float32) / 255
im = cv2.resize(im, None, fx=2, fy=2, interpolation=cv2.INTER_LANCZOS4)
hsv = cv2.cvtColor((im*255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
S, V = hsv[..., 1] / 255, hsv[..., 2] / 255
tierra = cv2.resize(cv2.imread('m-tierra.png', 0), (im.shape[1], im.shape[0]), interpolation=cv2.INTER_LINEAR).astype(np.float32) / 255
tierra = cv2.GaussianBlur(tierra, (5, 5), 0)[..., None]
L = (0.299 * im[..., 2] + 0.587 * im[..., 1] + 0.114 * im[..., 0])[..., None]
def bgr(h): h = h.lstrip('#'); return np.array([int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16)], np.float32) / 255
navy, navy2, cian, morado, lila, rosa, amarillo = bgr('#0a0530'), bgr('#170c52'), bgr('#1ff2ff'), bgr('#1d0d45'), bgr('#7b5cc4'), bgr('#ff2bd6'), bgr('#ffd23f')
# mar: azul marino; lo oscuro (letras, relieve del fondo) sale en cian
Lm = np.clip((0.52 - L) / 0.32, 0, 1)
mar = navy * (1 - Lm) + cian * Lm * 0.9 + navy2 * 0.0
# tierra: rampa morado oscuro -> lila -> rosa claro según luminosidad
t = np.clip((L - 0.3) / 0.75, 0, 1)
tie = np.where(t < 0.55, morado * (1 - t / 0.55) + lila * (t / 0.55), lila * (1 - (t - 0.55) / 0.45) + bgr('#ffc6f0') * ((t - 0.55) / 0.45))
# zonas urbanas (gris poco saturado) con un toque rosa
urb = ((S < 0.18) & (V > 0.55) & (V < 0.92))[..., None].astype(np.float32)
tie = tie * (1 - urb * 0.45) + (rosa * 0.55 + tie * 0.45) * urb * 0.45
# blancos (letras y carreteras) se quedan blancos; amarillos de los escudos, amarillo neón
blanco = ((S < 0.12) & (V > 0.9))[..., None].astype(np.float32)
out = mar * (1 - tierra) + tie * tierra
out = out * (1 - blanco) + np.array([1, 1, 1], np.float32) * blanco
# costa neón rosa
m = (tierra[..., 0] > 0.5).astype(np.uint8) * 255
borde = cv2.morphologyEx(m, cv2.MORPH_GRADIENT, np.ones((5, 5), np.uint8)).astype(np.float32) / 255
glow = cv2.GaussianBlur(borde, (0, 0), 7)
out = out + rosa * (np.clip(glow * 1.6, 0, 1)[..., None]) * 0.55
out = out * (1 - borde[..., None]) + rosa * borde[..., None]
out = np.clip(out, 0, 1)
res = (out * 255).astype(np.uint8)
# marca Trollacos sobre el sello (abajo a la derecha)
from PIL import Image, ImageDraw, ImageFont
pi = Image.fromarray(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
d = ImageDraw.Draw(pi); k = 2
x0, y0, x1, y1 = 1120 * k, 1745 * k, 1598 * k, 2208 * k
d.rectangle((x0, y0, x1, y1), fill=(10, 5, 48))
tr = Image.open('trollaco.png').convert('RGBA'); tr = tr.resize((tr.width * 9, tr.height * 9), Image.NEAREST)
pi.paste(tr, (x0 + (x1 - x0 - tr.width) // 2, y0 + 40), tr)
f1 = ImageFont.truetype('/tmp/claude-0/-home-claude/074a85cb-bf8f-5cf1-801a-ef5ae6c1a692/scratchpad/Righteous.ttf', 92)
txt = 'TROLLACOS'; w1 = d.textlength(txt, font=f1); w2 = d.textlength('.COM', font=f1); xs = x0 + (x1 - x0 - w1 - w2) / 2; ys = y0 + 40 + tr.height + 30
d.text((xs, ys), txt, font=f1, fill=(255, 43, 214)); d.text((xs + w1, ys), '.COM', font=f1, fill=(31, 242, 255))
pi.save('leonida-trollacos-personal.jpg', quality=92)
pi.resize((pi.width // 4, pi.height // 4)).save('/tmp/claude-0/-home-claude/074a85cb-bf8f-5cf1-801a-ef5ae6c1a692/scratchpad/personal-mini.jpg')
print(pi.size)
