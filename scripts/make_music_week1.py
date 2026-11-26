"""Week 1 music synthesis for the seven Week 1 storyboards (2026-11-17).

Each track: ~75 s, peak normalised to 0.5, 2 s fade in / 5 s fade out.
Same recipe family as make_music_batch.py (pads + sub-bass + sparse bells),
with a different mood/key per story so no two videos share a track — and
none of these reuse the batch tracks (moon-tide, black-hole, earth-stopped,
ant-size, sky-blue), fallen-down.mp3 or solar-drift.wav.

Run: ~/workspace/downloads/roblox-engine-drive/venv/bin/python scripts/make_music_week1.py
Writes public/music/{two-moons,mars-life,ringed-earth,fall-into-sun,stars-twinkle,light-speed,comet-hits}.wav
"""
import os
import numpy as np
from scipy.io import wavfile

SR = 44100
DUR = 75.0
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)


def pad_chord(track, start, length, notes, amp=0.10):
    """Slow-attack chord of detuned sines, raised-cosine attack/release."""
    n = int(length * SR)
    t = np.arange(n) / SR
    env = np.minimum(1.0, t / 3.0) * np.minimum(1.0, (length - t) / 3.0)
    env = np.clip(env, 0, 1) ** 1.5
    sig = np.zeros(n)
    for m in notes:
        f = midi(m)
        sig += np.sin(2 * np.pi * f * t) + 0.6 * np.sin(2 * np.pi * f * 1.003 * t)
        sig += 0.3 * np.sin(2 * np.pi * f * 2.0 * t)
    sig *= env * amp
    s0 = int(start * SR)
    e = min(n, len(track) - s0)
    if e > 0:
        track[s0:s0 + e] += sig[:e]


def sub_bass(track, start, length, root_midi, amp=0.16):
    n = int(length * SR)
    t = np.arange(n) / SR
    env = np.minimum(1.0, t / 2.0) * np.minimum(1.0, (length - t) / 2.0)
    env = np.clip(env, 0, 1)
    sig = np.sin(2 * np.pi * midi(root_midi - 12) * t) * env * amp
    s0 = int(start * SR)
    e = min(n, len(track) - s0)
    if e > 0:
        track[s0:s0 + e] += sig[:e]


def bell(track, when, freq, amp=0.10, decay=1.4):
    n = int(decay * 4 * SR)
    t = np.arange(n) / SR
    sig = (np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * freq * 2.0 * t)) * np.exp(-t / decay)
    sig *= amp
    s0 = int(when * SR)
    e = min(n, len(track) - s0)
    if e > 0:
        track[s0:s0 + e] += sig[:e]


def pulse(track, every, freq=55.0, amp=0.05, decay=0.35):
    t = 0.0
    while t < DUR:
        n = int(decay * 4 * SR)
        tt = np.arange(n) / SR
        sig = np.sin(2 * np.pi * freq * tt) * np.exp(-tt / decay) * amp
        s0 = int(t * SR)
        e = min(n, len(track) - s0)
        if e > 0:
            track[s0:s0 + e] += sig[:e]
        t += every


def finish(name, track):
    n = len(track)
    t = np.arange(n) / SR
    track *= np.clip(t / 2.0, 0, 1) * np.clip((DUR - t) / 5.0, 0, 1)
    peak = np.max(np.abs(track))
    track *= 0.5 / max(peak, 1e-9)
    stereo = np.stack([track, track], axis=1)
    out = os.path.join(ROOT, "public", "music", name)
    wavfile.write(out, SR, (stereo * 32767).astype(np.int16))
    print(f"{name}: {os.path.getsize(out)} bytes, peak 0.50")


def build(name, chords, roots, bell_scale, bell_times, bell_amp, pulse_every, sub_amp=0.16):
    track = np.zeros(int(DUR * SR))
    seg = DUR / len(chords)
    for i, (ch, rt) in enumerate(zip(chords, roots)):
        start = i * seg
        pad_chord(track, start, seg + 3.0, ch)
        sub_bass(track, start, seg + 3.0, rt, amp=sub_amp)
    rng = np.random.default_rng(abs(hash(name)) % 10000)
    for when in bell_times:
        note = bell_scale[rng.integers(0, len(bell_scale))]
        bell(track, when, midi(note), amp=bell_amp * rng.uniform(0.7, 1.2))
    if pulse_every:
        pulse(track, pulse_every)
    finish(name, track)


# 1. two-moons — dreamy, slow swell, two moons in the sky. G major.
build("two-moons.wav",
      chords=[[55, 59, 62], [50, 55, 59], [53, 57, 62], [55, 59, 62]],
      roots=[43, 38, 41, 43],
      bell_scale=[71, 74, 76, 79, 83],
      bell_times=[7, 13, 20, 27, 34, 41, 48, 56, 63, 70],
      bell_amp=0.09, pulse_every=10.0)

# 2. mars-life — dusty, sparse, lonely frontier. E minor.
build("mars-life.wav",
      chords=[[52, 55, 59], [48, 52, 55], [50, 53, 57], [52, 55, 59]],
      roots=[40, 36, 38, 40],
      bell_scale=[76, 79, 81, 84, 88],
      bell_times=[9, 19, 31, 43, 55, 66],
      bell_amp=0.07, pulse_every=6.0, sub_amp=0.18)

# 3. ringed-earth — bright, shimmering, rings catching the light. A major.
build("ringed-earth.wav",
      chords=[[57, 61, 64], [52, 57, 61], [54, 57, 61], [57, 61, 64]],
      roots=[45, 40, 42, 45],
      bell_scale=[73, 76, 78, 81, 85],
      bell_times=[5, 11, 18, 25, 32, 39, 46, 53, 60, 67],
      bell_amp=0.10, pulse_every=8.0)

# 4. fall-into-sun — hot, intense, rising heat. F minor, deep sub.
build("fall-into-sun.wav",
      chords=[[53, 56, 60], [48, 53, 56], [50, 53, 58], [53, 56, 60]],
      roots=[41, 36, 38, 41],
      bell_scale=[77, 80, 84, 87, 89],
      bell_times=[8, 17, 26, 35, 44, 53, 62, 70],
      bell_amp=0.08, pulse_every=4.0, sub_amp=0.20)

# 5. stars-twinkle — gentle, plucky, a clear night. C major.
build("stars-twinkle.wav",
      chords=[[60, 64, 67], [57, 60, 64], [59, 62, 65], [60, 64, 67]],
      roots=[48, 45, 47, 48],
      bell_scale=[72, 74, 76, 79, 81, 84],
      bell_times=[4, 9, 14, 20, 26, 32, 38, 44, 50, 56, 62, 68],
      bell_amp=0.10, pulse_every=0)

# 6. light-speed — driving, fast, warp. D minor, 0.5 s pulse + wind swell.
track = np.zeros(int(DUR * SR))
chords = [[62, 65, 69], [60, 63, 67], [58, 62, 65], [62, 65, 69]]
roots = [50, 48, 46, 50]
seg = DUR / len(chords)
for i, (ch, rt) in enumerate(zip(chords, roots)):
    pad_chord(track, i * seg, seg + 3.0, ch, amp=0.09)
    sub_bass(track, i * seg, seg + 3.0, rt, amp=0.18)
rng = np.random.default_rng(2027)
for when in [6, 13, 21, 29, 37, 45, 53, 61, 69]:
    bell(track, when, midi([76, 79, 81, 84, 86][rng.integers(0, 5)]), amp=0.08)
pulse(track, 0.5, freq=52.0, amp=0.06, decay=0.22)
noise = rng.standard_normal(len(track))
k = 0.02
wind = np.zeros(len(track))
for i in range(1, len(track)):
    wind[i] = wind[i - 1] + k * (noise[i] - wind[i - 1])
wind *= np.linspace(0.01, 0.04, len(track))
track += wind
finish("light-speed.wav", track)

# 7. comet-hits — ominous, deep, a rock from the dark. B minor.
build("comet-hits.wav",
      chords=[[59, 62, 66], [54, 59, 62], [55, 59, 62], [57, 60, 64]],
      roots=[47, 42, 43, 45],
      bell_scale=[78, 81, 83, 86, 90],
      bell_times=[10, 22, 34, 46, 58, 69],
      bell_amp=0.07, pulse_every=5.0, sub_amp=0.20)

print("done")
