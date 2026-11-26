"""Lightning music (2026-11-23).

Stormy mood: D minor low pads, deep sub-bass rumble, slow pulse,
sparse high bells — same recipe family as scripts/make_music_batch.py
(pads + sub-bass + sparse bells), its own track so no two videos share one.

Run: ~/workspace/downloads/engine-drive/venv/bin/python scripts/make_music_lightning.py
Writes public/music/lightning.wav (~75 s, peak normalised to 0.5).
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


# lightning — stormy: D minor, low rumble, slow heartbeat pulse, sparse bells.
track = np.zeros(int(DUR * SR))
chords = [[62, 65, 69], [58, 62, 65], [60, 63, 67], [57, 60, 65]]
roots = [50, 46, 48, 45]
seg = DUR / len(chords)
for i, (ch, rt) in enumerate(zip(chords, roots)):
    pad_chord(track, i * seg, seg + 3.0, ch, amp=0.09)
    sub_bass(track, i * seg, seg + 3.0, rt, amp=0.20)
rng = np.random.default_rng(2316)
for when in [7, 15, 24, 33, 41, 50, 58, 67]:
    note = [74, 77, 79, 81, 84][rng.integers(0, 5)]
    bell(track, when, midi(note), amp=0.07 * rng.uniform(0.7, 1.2))
pulse(track, 6.0, freq=49.0, amp=0.05)
finish("lightning.wav", track)
