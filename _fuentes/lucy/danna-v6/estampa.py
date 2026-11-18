import sys
from PIL import Image, ImageFilter, ImageEnhance, ImageChops
import numpy as np
foto, salida, cx, top, ancho = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
im = Image.open(foto).convert('RGB')
cab = Image.open('tr-cabeza.png').convert('RGBA'); cab = cab.crop(cab.getbbox())
txt = Image.open('logo-trollacos.png').convert('RGBA'); txt = txt.crop(txt.getbbox())
wc = int(ancho*0.68); cab = cab.resize((wc, int(cab.height*wc/cab.width)), Image.NEAREST)
txt = txt.resize((ancho, int(txt.height*ancho/txt.width)), Image.LANCZOS)
gap = int(ancho*0.06)
est = Image.new('RGBA', (ancho, cab.height+gap+txt.height), (0,0,0,0))
est.alpha_composite(cab, ((ancho-wc)//2, 0)); est.alpha_composite(txt, (0, cab.height+gap))
rgb = ImageEnhance.Color(est.convert('RGB')).enhance(0.85); rgb = ImageEnhance.Brightness(rgb).enhance(0.88)
est = Image.merge('RGBA', (*rgb.split(), est.split()[3]))
est = est.filter(ImageFilter.GaussianBlur(0.7))
x0, y0 = cx-ancho//2, top
zona = np.asarray(im.crop((x0, y0, x0+est.width, y0+est.height)).convert('L').filter(ImageFilter.GaussianBlur(6)), dtype=float)
luz = np.clip(zona/ max(zona.mean(),1), 0.6, 1.35)[..., None]
a = np.asarray(est, dtype=float)
a[..., :3] = np.clip(a[..., :3]*luz, 0, 255)
a[..., 3] *= 0.9
est = Image.fromarray(a.astype('uint8'), 'RGBA')
base = im.convert('RGBA'); base.alpha_composite(est, (x0, y0))
base.convert('RGB').save(salida, quality=95)
base.crop((x0-120, y0-80, x0+est.width+120, y0+est.height+80)).convert('RGB').save(salida.replace('.jpg','-zoom.jpg'))
