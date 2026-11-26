# Contributing

## Before you change anything

Read `AGENTS.md` (the working rules) and `RIG_CONTRACT.md` (the rig
contract). Read `ARCHITECTURE.md` if you are touching the render
pipeline or the composition. The short version:

- Story videos use **stills + ffmpeg, never the Remotion video
  renderer**. Do not reintroduce `renderMedia` / `remotion render`
  for stories — it drifts and glitches (see README).
- **Never hand-edit `src/story/currentStory.ts`.** It is generated
  by `scripts/make_short.py` (or `build_story.py` for tests).
- The narration opens with the big "What if …?" question; a camera
  cut every 2–3 s, no shot longer than 3.5 s; narrator voice
  `af_heart`; actors at least 4.5 studs apart.

## Setup

```bash
npm ci
npx tsc --noEmit
```

For the story pipeline you also need the Python venv and the synced
assets (`public/`, `models/` — see README "What is NOT in this
repo"). On a fresh machine:

```bash
python3 -m venv venv
venv/bin/pip install kokoro-onnx==0.6.1 onnxruntime==1.32.0 numpy Pillow
# then sync models/kokoro-v1.0.onnx + models/voices-v1.0.bin (338 MB,
# NOT in git) and public/music/ from the shared drive.
```

Note: `Pillow` is required by `make_short.py` (contact sheets) but
was not listed in the old setup docs — install it. There is no
`requirements.txt` yet; the versions above are the ones recorded in
the old README.

## Adding a story

1. Copy `stories/_template.py` to `stories/<slug>.py`.
2. Fill in `TITLE`, `BEATS`, `SFX`, `MUSIC`, `CAST`, `scenes(T)`
   following `.agents/skills/motion-blocks-director/SKILL.md`
   (`stories/hair_color.py` is a complete example).
3. Run the pipeline and fix rule checks before rendering:
   ```bash
   venv/bin/python scripts/make_short.py stories/<slug>.py --stills
   ```
   Inspect `out/preview/<slug>/sheet-*.png` at full size.
4. Render:
   ```bash
   node scripts/render.mjs story <slug> --port 3051
   ```
5. Check the assembled video at full size / in motion before
   uploading. A clean exit code is not a clean video.

## Adding a character / scene / location

- New character rig: add the component under `src/components/`,
  wire it in `MotionBlocksComposition.tsx` (actor → component map)
  and `src/characters/look.ts` if it needs a look/kit/scale entry.
  Kit characters need clips in `src/kit/kit.tsx`; anims with no
  clip fall back to `idle` (see `STORY_ANIM_TO_CLIP`).
- New location: add the set under `src/environments/`, register it
  in `EnvironmentSwitch`, and add its flags to
  `src/environments/locations.ts` (exterior/interior drives
  sky colour and fog).
- New verification stills: add a preset to
  `scripts/render_presets.mjs` and check it with
  `node scripts/render.mjs preset <name>`. Do not add another
  one-off `render-*.mjs` at the repo root — the 52 archived ones
  in `archive/root-render-scripts/` are the reason this rule
  exists.

## Checks before submitting

```bash
npx tsc --noEmit                                   # must exit 0
node scripts/render.mjs list                       # presets still load
node scripts/render.mjs still --comp MotionBlocks --frames 300 \
  --out-dir out/test-still --port 3051             # one still renders, non-blank
```

For story changes, also run the story pipeline's rule checks
(`make_short.py --stills`) and look at the preview sheets.
For render-pipeline changes, re-run a short range render
(`story <slug> --start 0 --end 29`) and verify the assembled
segment with ffprobe (frame count + duration).

## What not to commit

See `.gitignore`: `node_modules/`, `out/`, `public/`, `models/`,
`references/`, `*.mp4`, logs, `__pycache__/`, venvs. Do not commit
secrets — there are none in this repo and there must never be any.
Do not commit `src/story/currentStory.ts` changes by hand; it is
tracked only so a fresh clone builds, and `make_short.py` owns it.
