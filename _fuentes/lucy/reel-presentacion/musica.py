import numpy as np, wave, sys
SR = 44100; DUR = 16.5; BPM = 128; neg = 60 / BPM
N = int(SR * DUR); mix = np.zeros(N)
f = lambda m: 440 * 2 ** ((m - 69) / 12)
def sq(fr, d, duty=.5): t = np.arange(int(SR * d)) / SR; return np.where((t * fr) % 1 < duty, 1., -1.)
def tri(fr, d): t = np.arange(int(SR * d)) / SR; return 2 * np.abs(2 * ((t * fr) % 1) - 1) - 1
def env(x, a=.005, r=.08):
    n = len(x); e = np.ones(n); ai = int(a * SR); ri = min(n, int(r * SR))
    e[:ai] = np.linspace(0, 1, ai); e[n - ri:] *= np.linspace(1, 0, ri); return x * e
def pon(x, t, v):
    i = int(t * SR); j = min(N, i + len(x));
    if i < N: mix[i:j] += v * x[:j - i]
# progresión synthwave: Am F C G (2 compases cada uno... 1 compás cada uno)
acordes = [(57, [69, 72, 76]), (53, [65, 69, 72]), (48, [64, 67, 72]), (55, [62, 67, 71])]
comp = 4 * neg; ncomp = int(DUR / comp) + 1
for c in range(ncomp):
    raiz, ac = acordes[c % 4]; t0 = c * comp
    for k in range(8):  # bajo en corcheas
        pon(env(tri(f(raiz - 12 + (12 if k % 2 else 0)), neg / 2 * .9)), t0 + k * neg / 2, .35)
    for k in range(16):  # arpegio en semicorcheas
        pon(env(sq(f(ac[k % 3] + (12 if k >= 8 else 0)), neg / 4 * .8, .25), r=.03), t0 + k * neg / 4, .07)
    for k in range(4):  # bombo y caja
        kick = np.sin(2 * np.pi * np.cumsum(np.linspace(150, 40, int(SR * .15))) / SR) * np.linspace(1, 0, int(SR * .15))
        pon(kick, t0 + k * neg, .55)
        if k % 2: pon(np.random.uniform(-1, 1, int(SR * .1)) * np.linspace(1, 0, int(SR * .1)) ** 2, t0 + k * neg, .22)
        pon(np.random.uniform(-1, 1, int(SR * .03)) * np.linspace(1, 0, int(SR * .03)), t0 + k * neg + neg / 2, .08)
# melodía a partir del segundo 4.5
mel = [76, 0, 74, 76, 79, 0, 76, 74, 72, 0, 74, 72, 69, 0, 0, 0, 72, 74, 76, 0, 79, 81, 79, 76, 74, 0, 76, 74, 71, 0, 0, 0]
for r in range(2):
    for i, m in enumerate(mel):
        if m: pon(env(sq(f(m), neg / 2 * .9, .5), r=.06), 4.5 + r * 16 * neg + i * neg / 2, .11)
# subida y golpe en el 19 NOV (12.4 s)
pon(np.random.uniform(-1, 1, int(SR * 1.0)) * np.linspace(0, 1, int(SR * 1.0)) ** 2, 11.4, .15)
pon(env(sq(f(45), 1.2, .5), r=1.0), 12.4, .25)
mix[-int(SR * .8):] *= np.linspace(1, 0, int(SR * .8))
mix = mix / np.max(np.abs(mix)) * .85
w = wave.open(sys.argv[1], 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()
