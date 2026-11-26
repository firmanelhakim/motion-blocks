"""Chunked render for motion-blocks Shorts.

Renders a story in N frame-range chunks (Remotion --frames + --muted),
concatenates the video-only chunks with ffmpeg, then muxes the full
soundtrack once at the end. Each frame is rendered independently from
its frame number, so chunks join with no seam.

Usage:
    python scripts/render_chunks.py stories/<slug>.py --chunks 10
    python scripts/render_chunks.py stories/<slug>.py --chunks 10 --workers 4 --out out/<slug>.mp4
    python scripts/render_chunks.py stories/<slug>.py --chunks 10 --dry-run   # print the plan, render nothing
    python scripts/render_chunks.py stories/<slug>.py --chunks 10 --plan      # print chunk commands to run elsewhere
    python scripts/render_chunks.py stories/<slug>.py --chunk-index 3         # render one chunk only (farm out)
    python scripts/render_chunks.py --assemble-only --chunk-dir out/chunks/<slug> --out out/<slug>.mp4
    python scripts/render_chunks.py stories/<slug>.py --chunks 10 --resume    # skip chunks already rendered

Why chunk at all: it only helps when there is more CPU to spread across.
On this VM (1.5 shared CPUs, ~1 frame per 40 s) ten chunks just take
turns on the same CPUs and ten Chromes would blow the 6 GB RAM, so keep
--workers 1 there. Chunking pays on a many-CPU machine, or across
machines: render chunks on the VM and on the Instabox box in parallel,
then --assemble here. A 60 s Short is ~21 h on the VM alone, ~10 h on
the Instabox box alone, ~7 h split across both.

STALENESS RULE: by default this script reuses the existing soundtrack
(make_short.py --skip-tts). A story whose BEATS/SFX/MUSIC changed
since that audio was built would render scenes against stale timings,
so before reusing audio this script checks public/.soundtrack-inputs.json
(the sha256 of the story file the audio was built from, written by
make_short.py on every fresh TTS build). If the story changed — or no
fingerprint exists because the audio predates fingerprinting — it
refuses to render and tells you to re-run with --regen-tts. Pass
--regen-tts to rebuild the audio (and the fingerprint) from the
current story.

KRAKEN POLICY (the maintainer, 2026-11-17): when rendering on the Instabox
box, stop the Kraken Slam game server first and restart it after the
render. Turning it off does NOT speed the render (the idle server uses
~no CPU); it only stops players hitting a laggy game. The watchdog may
auto-restart the game — check before the first fallback render.

The script refuses to render when rule checks fail (unless --force),
and verifies every chunk's duration before concatenating, so a short
chunk fails loudly instead of silently producing a short video.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

REMOTION = ["node", os.path.join("node_modules", "@remotion", "cli", "remotion-cli.js")]
BUNDLE = os.path.join("out", "bundle")
CHROMIUM_FLAGS = '{"enable-unsafe-swiftshader": true}'
FPS = 30


def run(cmd, **kw):
    print("$", " ".join(str(c) for c in cmd), flush=True)
    return subprocess.run(cmd, check=True, **kw)


def ffprobe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def total_frames():
    cues_path = os.path.join("public", "kokoro-cues.json")
    if os.path.exists(cues_path):
        cues = json.load(open(cues_path, encoding="utf-8"))
        return int(cues["durationInFrames"])
    wav = os.path.join("public", "soundtrack.wav")
    if os.path.exists(wav):
        return int(round(ffprobe_duration(wav) * FPS))
    sys.exit("No public/kokoro-cues.json or public/soundtrack.wav — run make_short.py first.")


def chunk_ranges(total, n):
    """Split `total` frames into n contiguous ranges; returns [(start, end), ...] with end exclusive.
    n is clamped to total: asking for more chunks than frames would
    produce zero-size chunks (and a zero-frame render)."""
    n = max(1, min(n, total))
    base, rem = divmod(total, n)
    ranges, start = [], 0
    for i in range(n):
        size = base + (1 if i < rem else 0)
        ranges.append((start, start + size))
        start += size
    return ranges


STATE_FILE = "chunk-plan.json"


def write_chunk_plan(chunk_dir, slug, total, ranges):
    os.makedirs(chunk_dir, exist_ok=True)
    with open(os.path.join(chunk_dir, STATE_FILE), "w", encoding="utf-8") as f:
        json.dump({"slug": slug, "total": total, "chunks": len(ranges),
                   "ranges": ranges}, f, indent=2)


def resolve_chunk_count(chunk_dir, explicit):
    """Chunk count for --assemble-only: the explicit --chunks flag wins,
    else the count remembered in chunk-plan.json (written at render
    time), else the number of chunk-*.mp4 files on disk. Raises
    SystemExit when none of those can answer."""
    if explicit is not None:
        return explicit
    plan_path = os.path.join(chunk_dir, STATE_FILE)
    if os.path.exists(plan_path):
        with open(plan_path, encoding="utf-8") as f:
            return int(json.load(f)["chunks"])
    found = ([n for n in os.listdir(chunk_dir) if n.startswith("chunk-") and n.endswith(".mp4")]
             if os.path.isdir(chunk_dir) else [])
    if found:
        return len(found)
    sys.exit(f"Cannot determine the chunk count for --assemble-only: no --chunks given, "
             f"no {STATE_FILE} in {chunk_dir}, and no chunk-*.mp4 files there. "
             f"Pass --chunks explicitly.")


def check_audio_freshness(story_path):
    """Refuse to reuse a soundtrack built from different story inputs.
    Compares the story file's sha256 against public/.soundtrack-inputs.json
    (written by make_short.py on every fresh TTS build). Exits with a
    clear error when the inputs changed or no fingerprint exists.
    Skipped when there is no existing audio to reuse (a fresh build
    happens anyway)."""
    cues_path = os.path.join("public", "kokoro-cues.json")
    wav_path = os.path.join("public", "soundtrack.wav")
    if not (os.path.exists(cues_path) and os.path.exists(wav_path)):
        return
    fp_path = os.path.join("public", ".soundtrack-inputs.json")
    with open(story_path, "rb") as f:
        current = hashlib.sha256(f.read()).hexdigest()
    if not os.path.exists(fp_path):
        sys.exit("STALE AUDIO: public/soundtrack.wav exists but there is no "
                 "public/.soundtrack-inputs.json fingerprint, so the audio cannot "
                 "be verified against the current story. Re-run with --regen-tts "
                 "to rebuild the audio (and its fingerprint) from the current story.")
    with open(fp_path, encoding="utf-8") as f:
        fp = json.load(f)
    if fp.get("sha256") != current or fp.get("story") != os.path.basename(story_path):
        sys.exit("STALE AUDIO: the story file changed since public/soundtrack.wav "
                 "was built — reusing it would render scenes against old timings. "
                 "Re-run with --regen-tts to rebuild the audio from the current story.")


def render_chunk(idx, start, end, chunk_dir, workers):
    """Render one chunk (frames [start, end)) muted, video-only."""
    out = os.path.join(chunk_dir, f"chunk-{idx:03d}.mp4")
    cmd = REMOTION + ["render", BUNDLE, "MotionBlocks", out,
                      f"--frames={start}-{end - 1}", "--muted",
                      "--gl=angle", f"--chromium-flags={CHROMIUM_FLAGS}"]
    if workers > 1:
        cmd += ["--concurrency=1"]
    run(cmd, stdout=subprocess.DEVNULL)
    got = ffprobe_duration(out)
    want = (end - start) / FPS
    if abs(got - want) > 0.15:
        raise RuntimeError(f"chunk {idx}: {got:.2f}s rendered, expected {want:.2f}s")
    print(f"chunk {idx}: frames {start}-{end - 1} ({got:.2f}s) OK")
    return out


def assemble(chunk_files, out_path, total):
    """Concat video-only chunks, mux the full soundtrack once, verify."""
    wav = os.path.join("public", "soundtrack.wav")
    if not os.path.exists(wav):
        sys.exit("public/soundtrack.wav missing — cannot mux audio.")
    list_path = out_path + ".concat.txt"
    with open(list_path, "w", encoding="utf-8") as f:
        for p in chunk_files:
            f.write(f"file '{os.path.abspath(p)}'\n")
    video_only = out_path + ".video-only.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", list_path, "-c", "copy", video_only])
    run(["ffmpeg", "-y", "-v", "error", "-i", video_only, "-i", wav,
         "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", out_path])
    os.remove(video_only)
    got = ffprobe_duration(out_path)
    want = total / FPS
    if abs(got - want) > 0.2:
        sys.exit(f"FINAL: {got:.2f}s, expected {want:.2f}s — refusing to call this done.")
    h = hashlib.sha256()
    with open(out_path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    print(f"FINAL: {out_path}  {got:.2f}s  {os.path.getsize(out_path)} bytes  sha256={h.hexdigest()}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("story", nargs="?", help="stories/<slug>.py (not needed for --assemble-only)")
    ap.add_argument("--chunks", type=int, default=None,
                    help="number of chunks (default 10; --assemble-only reuses the count from chunk-plan.json when omitted)")
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--out", default="")
    ap.add_argument("--chunk-dir", default="")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--assemble-only", action="store_true")
    ap.add_argument("--only-chunks", action="store_true")
    ap.add_argument("--chunk-index", type=int, default=-1)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--skip-bundle", action="store_true")
    ap.add_argument("--regen-tts", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--python", default="")
    args = ap.parse_args()

    if args.chunks is not None and args.chunks < 1:
        sys.exit("--chunks must be >= 1")
    if args.workers < 1:
        sys.exit("--workers must be >= 1")
    # Chunk count for everything except --assemble-only (which resolves
    # it from the remembered plan below); chunk_ranges clamps it to the
    # frame total, so --chunks > total never makes zero-size chunks.
    n_chunks = args.chunks if args.chunks is not None else 10

    slug = None
    if args.story:
        slug = os.path.splitext(os.path.basename(args.story))[0]
    out_path = args.out or (os.path.join("out", f"{slug}.mp4") if slug else "")
    chunk_dir = args.chunk_dir or (os.path.join("out", "chunks", slug) if slug else "")
    if not out_path or not chunk_dir:
        sys.exit("Need a story (for slug) or explicit --out and --chunk-dir.")

    if args.assemble_only:
        n_chunks = resolve_chunk_count(chunk_dir, args.chunks)
        files = [os.path.join(chunk_dir, f"chunk-{i:03d}.mp4") for i in range(n_chunks)]
        missing = [p for p in files if not os.path.exists(p)]
        if missing:
            sys.exit(f"Missing chunk files: {missing}")
        assemble(files, out_path, total_frames())
        return

    if not args.story:
        sys.exit("A story file is required (unless --assemble-only).")

    # Dry-run / plan read the existing cues only — they must not
    # regenerate currentStory.ts (another job may own it right now).
    if args.dry_run or args.plan:
        total = total_frames()
        ranges = chunk_ranges(total, n_chunks)
        print(f"{slug}: {total} frames ({total / FPS:.1f}s) in {len(ranges)} chunks, {args.workers} worker(s)")
        for i, (s, e) in enumerate(ranges):
            print(f"  chunk {i:03d}: frames {s}-{e - 1} ({(e - s) / FPS:.1f}s)")
        if args.plan:
            for i, (s, e) in enumerate(ranges):
                out = os.path.join(chunk_dir, f"chunk-{i:03d}.mp4")
                print(" ".join(REMOTION + ["render", BUNDLE, "MotionBlocks", out,
                                            f"--frames={s}-{e - 1}", "--muted", "--gl=angle",
                                            f"--chromium-flags={CHROMIUM_FLAGS}"]))
            print(f"# then assemble: python scripts/render_chunks.py --assemble-only --chunk-dir {chunk_dir} --out {out_path}")
        return

    # 1. Regenerate currentStory.ts + cues (+ soundtrack unless reusing), gate on rule checks.
    # With --skip-tts (the default), refuse to reuse audio built from
    # different story inputs — see check_audio_freshness.
    if not args.regen_tts:
        check_audio_freshness(args.story)
    venv_python = os.path.join(ROOT, "venv", "bin", "python")
    py = args.python or (venv_python if os.path.exists(venv_python) else sys.executable)
    mk = [py, os.path.join("scripts", "make_short.py"), args.story]
    if not args.regen_tts:
        mk.append("--skip-tts")
    r = subprocess.run(mk, capture_output=True, text=True)
    print(r.stdout, end="")
    if r.returncode != 0:
        print(r.stderr, end="")
        sys.exit("make_short.py failed — fix the story first.")
    if "Rule checks: OK" not in r.stdout and not args.force:
        sys.exit("Rule checks did not pass — fix the story (or pass --force).")

    total = total_frames()
    ranges = chunk_ranges(total, n_chunks)
    if len(ranges) < n_chunks:
        print(f"--chunks {n_chunks} clamped to {len(ranges)} (story has only {total} frames)")
    # Remember the plan next to the chunks so --assemble-only does not
    # need --chunks repeated.
    write_chunk_plan(chunk_dir, slug, total, ranges)
    print(f"{slug}: {total} frames ({total / FPS:.1f}s) in {len(ranges)} chunks, {args.workers} worker(s)")
    for i, (s, e) in enumerate(ranges):
        print(f"  chunk {i:03d}: frames {s}-{e - 1} ({(e - s) / FPS:.1f}s)")

    # 2. Bundle once.
    if not args.skip_bundle:
        run(REMOTION + ["bundle", "src/index.ts", f"--out-dir={BUNDLE}"], stdout=subprocess.DEVNULL)

    # 3. Render chunks (in parallel up to --workers).
    os.makedirs(chunk_dir, exist_ok=True)
    if args.chunk_index >= len(ranges):
        sys.exit(f"--chunk-index {args.chunk_index} out of range (0-{len(ranges) - 1}).")
    todo = ranges if args.chunk_index < 0 else [ranges[args.chunk_index]]
    idxs = range(len(ranges)) if args.chunk_index < 0 else [args.chunk_index]
    todo_files = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = {}
        for i, (s, e) in zip(idxs, todo):
            out = os.path.join(chunk_dir, f"chunk-{i:03d}.mp4")
            if args.resume and os.path.exists(out) and os.path.getsize(out) > 0:
                print(f"chunk {i}: exists, skipping (--resume)")
                todo_files.append(out)
                continue
            futs[pool.submit(render_chunk, i, s, e, chunk_dir, args.workers)] = out
        for fut in concurrent.futures.as_completed(futs):
            todo_files.append(fut.result())
    if args.chunk_index >= 0 or args.only_chunks:
        print("Chunks rendered; assembly skipped.")
        return

    # 4. Assemble in chunk order.
    files = [os.path.join(chunk_dir, f"chunk-{i:03d}.mp4") for i in range(len(ranges))]
    assemble(files, out_path, total)


if __name__ == "__main__":
    main()
