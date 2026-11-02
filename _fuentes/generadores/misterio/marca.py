"""Pone la marca de agua de Trollacos a una ilustración propia del Expediente y la guarda en misterio/img/<caso>.webp.
Uso: python3 marca.py <imagen_original> <img_del_caso>      p. ej.  python3 marca.py linares.jpg linares
El original se guarda en _fuentes/misterio-originales/ (no se sube a la web)."""
import sys, os, shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter
RAIZ = '/home/claude/trollacos-web'
TEXTO = 'TROLLACOS.COM/MISTERIO'
FUENTE = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'

def marca(src, nombre):
    os.makedirs(f'{RAIZ}/_fuentes/misterio-originales', exist_ok=True)
    shutil.copy(src, f'{RAIZ}/_fuentes/misterio-originales/{nombre}{os.path.splitext(src)[1]}')
    im = Image.open(src).convert('RGB')
    im.thumbnail((1200, 1200), Image.LANCZOS)
    W, H = im.size
    t = max(14, round(min(W, H) * 0.028))           # tamaño de letra: pequeño pero legible
    f = ImageFont.truetype(FUENTE, t)
    tw = f.getbbox(TEXTO)[2]
    tro = Image.open(f'{RAIZ}/img/trollaco.png').convert('RGBA')
    th = round(t * 1.5); tro = tro.resize((round(tro.width * th / tro.height), th), Image.NEAREST)
    m = round(t * 0.9); gap = round(t * 0.4)
    x = W - m - tw; y = H - m - t
    capa = Image.new('RGBA', im.size, (0, 0, 0, 0))
    sombra = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sombra).text((x + 1, y + 1), TEXTO, font=f, fill=(0, 0, 0, 200))
    sombra = sombra.filter(ImageFilter.GaussianBlur(max(1, t // 8)))
    d = ImageDraw.Draw(capa)
    d.text((x, y), TEXTO, font=f, fill=(255, 255, 255, 190))
    tro.putalpha(tro.getchannel('A').point(lambda a: a * 0.85))
    capa.alpha_composite(tro, (x - gap - tro.width, y + t - th + round(t * 0.25)))
    out = Image.alpha_composite(Image.alpha_composite(im.convert('RGBA'), sombra), capa).convert('RGB')
    out.save(f'{RAIZ}/misterio/img/{nombre}.webp', 'WEBP', quality=82)
    print(nombre, out.size)

if __name__ == '__main__':
    marca(sys.argv[1], sys.argv[2])
