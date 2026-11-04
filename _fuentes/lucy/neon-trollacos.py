"""Cambia el neón «GG» de la foto de Danna por «TROLLACOS.COM» (rosa + .COM cian).
righteous.ttf: convertir fuentes/righteous.woff2 con fontTools (+ brotli)."""
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

SRC = '_fuentes/lucy/danna-setup-gg-anterior.png'  # foto original con el «GG»
im = np.asarray(Image.open(SRC).convert('RGB')).astype(np.float32) / 255
H, W, _ = im.shape
yy, xx = np.mgrid[0:H, 0:W]

# 1) Borrar el «GG»: pared modelada con un polinomio ajustado alrededor
cx, cy = 812, 180
def ell(rx, ry): return ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2
zona = ell(235, 165) < 1
anillo = (ell(300, 215) < 1) & ~zona & (xx > 640) & (yy < 395)
g = im[..., 1]; r = im[..., 0]
anillo &= ~((g > r + 0.05))  # fuera hojas verdes
def base(x, y):
    x = (x - 900) / 300; y = (y - 200) / 200
    return np.stack([np.ones_like(x), x, y, x * x, x * y, y * y, x ** 3, y ** 3], -1)
A = base(xx[anillo].astype(np.float32), yy[anillo].astype(np.float32))
fit = np.zeros_like(im)
B = base(xx.astype(np.float32), yy.astype(np.float32))
for c in range(3):
    coef, *_ = np.linalg.lstsq(A, im[..., c][anillo], rcond=None)
    fit[..., c] = B @ coef
rng = np.random.default_rng(1)
ruido = cv2.GaussianBlur(rng.normal(0, 0.012, (H, W)).astype(np.float32), (0, 0), 0.8)[..., None]
pared = fit + ruido
# máscara suave para fundir
m = np.clip((1 - ell(235, 165)) / 0.25, 0, 1)
m = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 6)[..., None]
out = im * (1 - m) + pared * m

# 2) Neón «TROLLACOS.COM» con la Righteous de la web
TXT = 'TROLLACOS.COM'
font = ImageFont.truetype('righteous.ttf', 70)
tmp = Image.new('L', (W, H)); d = ImageDraw.Draw(tmp)
bx = d.textbbox((0, 0), TXT, font=font)
tw, th = bx[2] - bx[0], bx[3] - bx[1]
X0 = 655 + (1230 - 655 - tw) // 2 - bx[0]; Y0 = 175 - th // 2 - bx[1]
d.text((X0, Y0), TXT, font=font, fill=255)
lleno = np.asarray(tmp).astype(np.float32) / 255
# tubo = contorno de las letras
k = np.ones((3, 3), np.uint8)
ero = cv2.erode((lleno > 0.5).astype(np.uint8), k, iterations=4)
tubo = np.clip(lleno - ero.astype(np.float32), 0, 1)
tubo = cv2.GaussianBlur(tubo, (0, 0), 1.1)
tubo = tubo / tubo.max()

col_nucleo = np.array([1.0, 0.92, 0.98])
col_brillo = np.array([1.0, 0.17, 0.84])
# «.COM» en cian
corte = X0 + d.textbbox((X0, Y0), 'TROLLACOS', font=font)[2] - X0
cian = (xx >= corte).astype(np.float32)
g1 = cv2.GaussianBlur(tubo, (0, 0), 4)
g2 = cv2.GaussianBlur(tubo, (0, 0), 16)
g3 = cv2.GaussianBlur(tubo, (0, 0), 60)
mix = cv2.GaussianBlur(cian, (0, 0), 25)[..., None]
cb = col_brillo * (1 - mix) + np.array([0.12, 0.95, 1.0]) * mix
glow = (g1 * 1.6 + g2 * 2.4 + g3 * 5.0)[..., None] * cb
out = 1 - (1 - out) * (1 - np.clip(glow * 0.55, 0, 1))  # screen
cn = col_nucleo * (1 - cian[..., None]) + np.array([0.88, 1.0, 1.0]) * cian[..., None]
out = out * (1 - tubo[..., None]) + cn * tubo[..., None]
out = np.clip(out, 0, 1)
Image.fromarray((out * 255).astype(np.uint8)).save('_fuentes/lucy/danna-setup-trollacos.png')
print(tw, th, X0, Y0)
