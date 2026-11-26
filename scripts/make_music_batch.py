"""Batch music synthesis for the five storyboards (2026-11-17).

Each track: ~75 s, peak normalised to 0.5, 2 s fade in / 5 s fade out.
Same recipe family as solar-drift.wav (pads + sub-bass + sparse bells),
with a different mood per story so no two videos share a track.

Run: ~/workspace/downloads/engine-drive/venv/bin/python scripts/make_music_batch.py
Writes public/music/{moon-tide,black-hole,earth-stopped,ant-size,sky-blue}.wav
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


# 1. moon-tide — gentle, slow, tide-like swell. D major, bells D pentatonic.
build("moon-tide.wav",
      chords=[[62, 66, 69], [57, 62, 66], [59, 62, 66], [55, 59, 62]],
      roots=[50, 45, 47, 43],
      bell_scale=[74, 76, 78, 81, 83, 86],
      bell_times=[6, 11, 17, 23, 30, 36, 42, 49, 55, 62, 68],
      bell_amp=0.09, pulse_every=8.0)

# 2. black-hole — dark drone, deep sub, sparse high bells. A minor.
build("black-hole.wav",
      chords=[[57, 60, 64], [53, 57, 60], [50, 53, 57], [52, 55, 59]],
      roots=[45, 41, 38, 40],
      bell_scale=[81, 84, 88, 91, 93],
      bell_times=[8, 18, 29, 40, 52, 63],
      bell_amp=0.07, pulse_every=4.0, sub_amp=0.20)

# 3. earth-stopped — driving, tense. D minor, 100 BPM pulse + wind swell.
track = np.zeros(int(DUR * SR))
chords = [[62, 65, 69], [58, 62, 65], [60, 63, 67], [62, 65, 69]]
roots = [50, 46, 48, 50]
seg = DUR / len(chords)
for i, (ch, rt) in enumerate(zip(chords, roots)):
    pad_chord(track, i * seg, seg + 3.0, ch, amp=0.09)
    sub_bass(track, i * seg, seg + 3.0, rt, amp=0.18)
rng = np.random.default_rng(1234)
for when in [5, 12, 20, 27, 35, 43, 50, 58, 66]:
    bell(track, when, midi([76, 79, 81, 84][rng.integers(0, 4)]), amp=0.08)
pulse(track, 0.6, freq=48.0, amp=0.06, decay=0.22)
# wind: slow rising lowpassed noise
noise = rng.standard_normal(len(track))
k = 0.02
wind = np.zeros(len(track))
for i in range(1, len(track)):
    wind[i] = wind[i - 1] + k * (noise[i] - wind[i - 1])
wind *= np.linspace(0.015, 0.05, len(track))
track += wind
finish("earth-stopped.wav", track)

# 4. ant-size — playful, plucky, bright. C major, bouncy eighth-note arpeggio.
track = np.zeros(int(DUR * SR))
chords = [[60, 64, 67], [55, 59, 62], [57, 60, 64], [60, 64, 67]]
roots = [48, 43, 45, 48]
for i, (ch, rt) in enumerate(zip(chords, roots)):
    pad_chord(track, i * seg, seg + 3.0, ch, amp=0.08)
    sub_bass(track, i * seg, seg + 3.0, rt, amp=0.12)
rng = np.random.default_rng(777)
t = 2.0
scale = [72, 74, 76, 79, 81, 84, 86]
while t < DUR - 2:
    bell(track, t, midi(scale[rng.integers(0, len(scale))]), amp=0.10, decay=0.35)
    t += 0.5
finish("ant-size.wav", track)

# 5. sky-blue — warm, bright major. C-G-Am-F, gentle bells, warmer second half.
build("sky-blue.wav",
      chords=[[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]],
      roots=[48, 43, 45, 41],
      bell_scale=[72, 76, 79, 81, 84],
      bell_times=[5, 10, 16, 22, 28, 35, 41, 47, 54, 60, 67, 71],
      bell_amp=0.09, pulse_every=8.0)

print("done")
