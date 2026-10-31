"""Synthesize the steam locomotive chuff sounds (ogg) with numpy + soundfile."""
import numpy as np
import soundfile as sf
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "src", "main", "resources", "assets", "steamcurios", "sounds")
os.makedirs(OUT, exist_ok=True)
SR = 22050


def chuff(seed, pitch=1.0, length=0.55):
    rng = np.random.default_rng(seed)
    n = int(SR * length)
    t = np.linspace(0, length, n, endpoint=False)
    # burst envelope: fast attack, exponential decay, slight second puff
    env = np.exp(-t * 14 * pitch) + 0.35 * np.exp(-((t - 0.22) ** 2) / 0.004)
    # steam: filtered noise (one-pole lowpass), brighter at the start
    noise = rng.standard_normal(n)
    lp = np.zeros(n)
    alpha = 0.18
    acc = 0.0
    for i in range(n):
        acc += alpha * (noise[i] - acc)
        lp[i] = acc
    # low boiler thump
    thump = 0.55 * np.sin(2 * np.pi * 62 * pitch * t) * np.exp(-t * 10)
    sig = 0.8 * lp * env + thump
    # gentle clip
    sig = np.tanh(sig * 1.6)
    return (sig * 0.85).astype(np.float32)


sf.write(os.path.join(OUT, "chuff1.ogg"), chuff(7, 1.0), SR, format="OGG", subtype="VORBIS")
sf.write(os.path.join(OUT, "chuff2.ogg"), chuff(23, 0.85, 0.6), SR, format="OGG", subtype="VORBIS")
print("wrote chuff1.ogg, chuff2.ogg")
