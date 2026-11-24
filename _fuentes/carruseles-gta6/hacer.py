import json, sys
sys.path.insert(0, '.')
from datos import TEMAS
L = []
for i, t in enumerate(TEMAS, 1):
    N = len(t['slides'])
    for j, cards in enumerate(t['slides'], 1):
        troll = t['troll'] if j == 1 else ('Guárdalo para tu próxima partida 📌' if j == N else 'Desliza, que hay más ➜')
        if N == 1: troll = t['troll']
        L.append({'file': f"{i:02d}-{t['slug']}-{j}.png", 'titulo': t['titulo'], 'sub': t['sub'] if j == 1 else t['sub'],
                  'troll': troll, 'n': f"{j} / {N}" if N > 1 else 'GUÍA GTA VI', 'cards': cards,
                  'fu': ''})
json.dump(L, open('diapos.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(L))
