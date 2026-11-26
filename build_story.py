"""Build a story module into src/story/currentStory.ts with FAKE no-TTS
timings (test/fixture only — real builds need kokoro_onnx for real cues).

Usage (from the repo root):
    python3 build_story.py stories/<slug>.py

Prints the rule-check problems returned by write_story.

The fixture also writes public/soundtrack.wav so downstream steps that
expect audio (e.g. render.mjs story, which errors on a missing
soundtrack) can run. The wav is generated placeholder SILENCE — not
narration — of exactly the fake story's duration (24 kHz mono, matching
the real soundtrack format), because no TTS model is available on this
path. Do not ship a video assembled from it as a real Short.
"""
import importlib.util
import os
import sys
import wave

sys.path.insert(0, "scripts")
from shorts.scene import FPS, write_story  # noqa: E402
from make_short import Timing  # noqa: E402

SR = 24000


def fake_cues(beat_ids, beat_len=90, first_len=150):
    """Hand-set beat timings: the first beat is longer (hook), the rest
    beat_len frames. Beat ids come from the story's own BEATS list —
    real stories use non-sequential ids (e.g. b9b), so assuming b1..bN
    breaks them. Each beat carries startSec/endSec as well as frames:
    stories using T.f() / resolve_time() read the seconds fields.
    """
    timings = {}
    t = 0
    for i, bid in enumerate(beat_ids):
        length = first_len if i == 0 else beat_len
        timings[bid] = {
            "startFrame": t, "endFrame": t + length,
            "startSec": round(t / FPS, 3), "endSec": round((t + length) / FPS, 3),
            "text": "",
        }
        t += length
    return {"beatTimings": timings, "durationInFrames": t, "captions": []}


def write_placeholder_soundtrack(duration_frames, out_path="public/soundtrack.wav"):
    """Silence wav of exactly duration_frames / FPS seconds (see module docstring)."""
    n_samples = int(round(duration_frames / FPS * SR))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with wave.open(out_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(b"\x00\x00" * n_samples)
    print(f"Placeholder soundtrack (silence, {n_samples / SR:.2f}s): {out_path}")


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 build_story.py stories/<slug>.py")
    path = sys.argv[1]
    if not os.path.isfile(path):
        sys.exit(f"Story file not found: {path}")
    spec = importlib.util.spec_from_file_location("story", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for name in ("TITLE", "BEATS", "CAST", "scenes"):
        if not hasattr(mod, name):
            sys.exit(f"{path}: missing {name}")
    cues = fake_cues([b["id"] for b in mod.BEATS])
    scenes = mod.scenes(Timing(cues))
    problems = write_story(mod.TITLE, scenes, mod.CAST, cues)
    write_placeholder_soundtrack(cues["durationInFrames"])
    if problems:
        print("RULE CHECKS FAILED:")
        for p in problems:
            print("  -", p)
    else:
        print("Rule checks: OK")


if __name__ == "__main__":
    main()
