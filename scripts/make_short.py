"""One-command Roblox Short pipeline.

    python scripts/make_short.py stories/<slug>.py            # voice+music+SFX -> scenes -> checks -> typecheck
    python scripts/make_short.py stories/<slug>.py --stills   # + preview stills (one per camera shot) + contact sheets
    python scripts/make_short.py stories/<slug>.py --render   # + final 1080x1920 MP4 -> out/<slug>.mp4
    --skip-tts      reuse public/soundtrack.wav + kokoro-cues.json (only when BEATS/SFX/MUSIC did not change)
    --frames 120,480  render these stills instead of one per shot
    --log error     Remotion log level (default: error)
    --force         render even if rule checks report problems

A story file defines TITLE, BEATS, SFX, MUSIC, CAST and scenes(T). See .agents/skills/roblox-shorts-director/SKILL.md.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
os.chdir(ROOT)

from shorts.audio import build_soundtrack, resolve_time  # noqa: E402
from shorts.scene import FPS, check_story, write_story  # noqa: E402

REMOTION = ["node", os.path.join("node_modules", "@remotion", "cli", "remotion-cli.js")]
BUNDLE = os.path.join("out", "bundle")
ENTRY_SLIM = os.path.join("src", "short-entry.tsx")
ENTRY_FULL = os.path.join("src", "index.ts")
CHROMIUM_FLAGS = json.dumps({
    "use-angle": "swiftshader",
    "enable-unsafe-swiftshader": True,
    "disable-dev-shm-usage": True,
    "force-gpu-mem-available-mb": "1024",
})


class Timing:
    """Frame lookups for scenes(T): T.B['b3'] start frame, T.E['b3'] end frame, T.END, T.f('b3+0.5')."""

    def __init__(self, cues):
        self.cues = cues
        self.timings = cues["beatTimings"]
        self.B = {k: v["startFrame"] for k, v in self.timings.items()}
        self.E = {k: v["endFrame"] for k, v in self.timings.items()}
        self.END = cues["durationInFrames"]

    def f(self, ref) -> int:
        return int(round(resolve_time(ref, self.timings) * FPS))


def safe_concurrency() -> int:
    # Python port of the canonical rule in scripts/render_lib.mjs
    # safeConcurrency (~50% of vCPUs, RAM-capped at ~2 GiB per
    # SwiftShader tab). It cannot import the JS implementation — keep
    # the two formulas in sync when changing either.
    vcpus = max(1, os.cpu_count() or 1)
    cpu_budget = max(1, vcpus // 2)
    try:
        with open("/proc/meminfo", encoding="utf-8") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    ram_gb = int(line.split()[1]) / (1024 * 1024)
                    return max(1, min(cpu_budget, max(1, int(ram_gb // 2))))
    except OSError:
        pass
    return cpu_budget


def run(cmd, **kw):
    print("$", " ".join(cmd))
    return subprocess.run(cmd, check=True, **kw)


def load_story(path):
    spec = importlib.util.spec_from_file_location("story", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for name in ("TITLE", "BEATS", "CAST", "scenes"):
        if not hasattr(mod, name):
            sys.exit(f"{path}: missing {name}")
    return mod


def still_frames(scenes):
    frames = []
    for sc in scenes:
        for s in sc["cameraShots"]:
            frames.append((s["startFrame"] + s["endFrame"]) // 2)
    return sorted(set(frames))


def contact_sheets(paths, out_dir, per_row=6):
    from PIL import Image

    sheets = []
    for n in range(0, len(paths), per_row * 2):
        chunk = paths[n: n + per_row * 2]
        rows = (len(chunk) + per_row - 1) // per_row
        sheet = Image.new("RGB", (270 * per_row, 480 * rows), "black")
        for i, p in enumerate(chunk):
            sheet.paste(Image.open(p).resize((270, 480)), ((i % per_row) * 270, (i // per_row) * 480))
        out = os.path.join(out_dir, f"sheet-{n // (per_row * 2) + 1}.png")
        sheet.save(out)
        sheets.append(out)
    return sheets


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("story")
    ap.add_argument("--skip-tts", action="store_true")
    ap.add_argument("--stills", action="store_true")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--scale", type=float, default=None, help="explicit render scale (default: 1.0)")
    ap.add_argument("--concurrency", type=int, default=None, help="Remotion concurrency (default: ~50%% vCPUs, RAM-capped)")
    ap.add_argument("--log", default="error", choices=["trace", "verbose", "info", "warn", "error"])
    ap.add_argument("--frames", default="")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    mod = load_story(args.story)
    slug = os.path.splitext(os.path.basename(args.story))[0]

    # 1. Audio: narration + captions + music + SFX
    cues_path = os.path.join("public", "kokoro-cues.json")
    if args.skip_tts and os.path.exists(cues_path):
        cues = json.load(open(cues_path, encoding="utf-8"))
        print(f"Reusing {cues_path} ({cues['durationInFrames']} frames)")
    else:
        cues = build_soundtrack(mod.BEATS, getattr(mod, "SFX", []), getattr(mod, "MUSIC", None))
        # Fingerprint the story inputs the audio was built from, so
        # render_chunks.py can refuse to reuse this audio after the
        # story's BEATS/SFX/MUSIC change (see its header).
        with open(args.story, "rb") as sf:
            story_hash = hashlib.sha256(sf.read()).hexdigest()
        fingerprint = {
            "story": os.path.basename(args.story),
            "sha256": story_hash,
        }
        with open(os.path.join("public", ".soundtrack-inputs.json"), "w", encoding="utf-8") as f:
            json.dump(fingerprint, f, indent=2)

    # 2. Scenes -> rule checks FIRST, then src/story/currentStory.ts.
    # A failing story must never land on disk: --stills/--render exit
    # here, before write_story runs (previously write_story wrote the
    # file and only --render exited afterwards).
    scenes = mod.scenes(Timing(cues))
    problems = check_story(mod.TITLE, scenes, mod.CAST, cues)
    if problems:
        print("\nRULE CHECKS FAILED:")
        for p in problems:
            print("  " + p)
    else:
        print("Rule checks: OK (scenes contiguous, cuts every 1-3.5 s, no overlapping actors)")
    if problems and not args.force and (args.stills or args.render):
        sys.exit("Fix the rule problems above (or pass --force) before rendering.")
    write_story(mod.TITLE, scenes, mod.CAST, cues)

    # 3. Typecheck
    run(["node", os.path.join("node_modules", "typescript", "bin", "tsc"), "-p", "."])

    if not (args.stills or args.render):
        return

    # 4. Bundle once (slim entrypoint for RobloxShort), then stills / render from the bundle
    entry = ENTRY_SLIM if os.path.exists(ENTRY_SLIM) else ENTRY_FULL
    run(REMOTION + ["bundle", entry, f"--out-dir={BUNDLE}", f"--log={args.log}"], stdout=subprocess.DEVNULL)

    if args.stills:
        out_dir = os.path.join("out", "preview", slug)
        os.makedirs(out_dir, exist_ok=True)
        # Clear previous preview stills. The dir may contain
        # subdirectories (e.g. a stray nested folder) — remove those too
        # instead of crashing on os.remove; anything unreadable is left
        # alone with a warning rather than aborting the run.
        for f in os.listdir(out_dir):
            p = os.path.join(out_dir, f)
            try:
                if os.path.isdir(p) and not os.path.islink(p):
                    shutil.rmtree(p)
                else:
                    os.remove(p)
            except OSError as e:
                print(f"WARNING: could not clear preview entry {p}: {e}")
        frames = [int(x) for x in args.frames.split(",") if x.strip()] or still_frames(scenes)
        # Reuse a single warm Chromium browser across all preview stills instead
        # of spawning a fresh Chromium + WebGL process per frame.
        render_script = os.path.join("scripts", "render.mjs")
        if os.path.exists(render_script):
            run([
                "node", render_script, "still",
                "--bundle", BUNDLE,
                "--comp", "RobloxShort",
                "--frames", ",".join(str(fr) for fr in frames),
                "--out-dir", out_dir,
                "--pattern", "f{frame:5}.png",
                "--scale", "0.5",
                "--log", args.log,
            ])
            paths = [os.path.join(out_dir, f"f{fr:05d}.png") for fr in frames]
        else:
            paths = []
            for fr in frames:
                p = os.path.join(out_dir, f"f{fr:05d}.png")
                run(REMOTION + [
                    "still", BUNDLE, "RobloxShort", p, f"--frame={fr}",
                    "--gl=swangle", "--scale=0.5", f"--log={args.log}",
                    f"--chromium-flags={CHROMIUM_FLAGS}",
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                paths.append(p)
        for s in contact_sheets(paths, out_dir):
            print("Contact sheet:", s)

    if args.render:
        conc = args.concurrency if (args.concurrency and args.concurrency >= 1) else safe_concurrency()
        scale = args.scale if args.scale is not None else 1.0
        out = os.path.join("out", f"{slug}.mp4")
        cmd = REMOTION + [
            "render", BUNDLE, "RobloxShort", out,
            "--gl=swangle",
            f"--chromium-flags={CHROMIUM_FLAGS}",
            f"--concurrency={conc}",
            f"--log={args.log}",
        ]
        if scale != 1.0:
            cmd += [f"--scale={scale}"]
        run(cmd)
        print("Rendered:", out)


if __name__ == "__main__":
    main()
