# motion-blocks

A Remotion + three.js engine that renders blocky 3D animated science
Shorts for a YouTube channel: portrait **1080×1920, 30 fps**,
roughly 45–60 seconds each. A story is a Python file (`stories/<slug>.py`)
describing beats, cast, scenes and camera shots; the pipeline turns it
into narration, a soundtrack, preview stills, and finally a video.

Every Short opens with a big **"What if …?"** question in the narration
and answers it with real science, in plain language. See `AGENTS.md` for
the channel rules the pipeline enforces.

## Why stills + ffmpeg, not the Remotion video renderer

Story videos are **never** rendered with Remotion's video renderer
(`remotion render` / `renderMedia`). That path was measured to drift
deterministically — frame 0 exact, ~RMSE 157 by frame 299 — and to
glitch with blank-white / tiled frames. Instead every frame is rendered
individually with `renderStill`, then assembled with ffmpeg
(30 fps, libx264, CRF 18, yuv420p, faststart) and the soundtrack is
muxed in. The assembly step verifies the result with ffprobe (exact
frame count, duration, audio stream present) and fails loudly instead
of silently producing a short or silent video.

The one exception is `make_short.py --render`, which still calls the
legacy video renderer. Treat it as a fallback only — the supported
story path is `node scripts/render.mjs story <slug>`.

## Quickstart (fresh clone)

Prerequisites — all verified on the cleanup machine (Node v24.22.1,
npm 10.9.4, ffmpeg 8.1.2):

- **Node.js 20+** and npm. No `engines` field is set in `package.json`;
  the cleanup was verified on Node v24.22.1.
- **ffmpeg + ffprobe** on `PATH`. The assembly and verification steps
  shell out to them; without ffmpeg, stills render but no video is
  produced. (Ubuntu: `sudo apt install ffmpeg`.)
- **Python 3.10+** for the story pipeline (`make_short.py`). The TTS
  and music steps need the separately synced assets below.
- **Chrome.** Renders run headless with SwiftShader software WebGL
  (`swangle`). If a Playwright Chromium is present at
  `~/.cache/ms-playwright/chromium-1181/chrome-linux/chrome` it is
  used; otherwise Remotion downloads its Chrome Headless Shell on
  first render. `CHROME_BIN` overrides the browser path.

```bash
git clone <repo> motion-blocks
cd motion-blocks
npm ci            # installs 317 packages (verified: 16 s on the cleanup VM)
npx tsc --noEmit  # typecheck — must exit 0 before rendering
```

Render one test still of the story currently loaded in
`src/story/currentStory.ts` (ice_floats, 1742 frames):

```bash
node scripts/render.mjs still --comp MotionBlocks --frames 300 \
  --out-dir out/test-still --port 3051
# → out/test-still/frame-0300.png (1080×1920; ~42 s on a 1.5-CPU VM,
#   most of it the one-time bundle — a real render machine is far faster)
```

## Making a story, end to end

1. **Write the story.** Copy `stories/_template.py` to
   `stories/<slug>.py` and fill in `TITLE`, `BEATS`, `SFX`, `MUSIC`,
   `CAST` and `scenes(T)`. The skill in
   `.agents/skills/motion-blocks-director/SKILL.md` is the full
   reference (beats, music, SFX, cast, scenes, camera catalog).
   `stories/hair_color.py` is a complete example.
2. **Build it** (needs the Python venv + synced assets — see below):
   ```bash
   venv/bin/python scripts/make_short.py stories/<slug>.py --stills
   ```
   This builds the soundtrack (Kokoro TTS narration, voice `af_heart`,
   + music + SFX), writes `src/story/currentStory.ts`, runs the rule
   checks (scenes contiguous, camera cuts every 1–3.5 s, actors at
   least 4.5 studs apart) and the typecheck, then renders one preview
   still per camera shot plus contact sheets into
   `out/preview/<slug>/`. Fix every `RULE CHECKS FAILED` line and
   inspect the sheets at full size before rendering.
   `--skip-tts` reuses `public/soundtrack.wav` +
   `public/kokoro-cues.json` when beats/SFX/music did not change.
   Use the venv Python — the system `python3` has no Kokoro and fails
   with `No module named 'kokoro_onnx'`.
3. **Render the story** (stills + ffmpeg — the supported path):
   ```bash
   node scripts/render.mjs story <slug> --port 3051
   # → out/<slug>.mp4 (1080×1920, 30 fps, audio muxed)
   ```
   A frame range renders only that range:
   `node scripts/render.mjs story <slug> --start 0 --end 299
   --out out/<slug>-f0-299.mp4 --port 3051`.
   Existing stills are skipped on re-runs (resume); `--overwrite`
   re-renders them. `--stills-only` renders without assembling;
   `--assemble-only` assembles already-rendered stills.
4. **Check the result** at full size / in motion before uploading —
   the review gate is a human looking at frames, not the exit code.

## Render CLI reference (`scripts/render.mjs`)

All commands take `--port` (pinned; defaults: 3050, or 3051 for
`story`) and `--log error`. Run `node scripts/render.mjs help` for
the full usage text, `node scripts/render.mjs list` for presets.

| Command | What it does |
|---|---|
| `still --comp <id> --frames 0,60,120 --out-dir <dir> [--pattern frame-{frame:4}.png] [--scale 0.5] [--bundle out/bundle]` | Render individual stills of any composition. `--scale 0.5` is the preview scale used by `make_short.py --stills`. |
| `range --comp <id> --start 0 --end 100 --out-dir <dir>` | Render a contiguous frame range of any composition as stills. |
| `story [slug] [--start 0] [--end <last>] [--out out/<slug>.mp4] [--stills-dir out/stills/<slug>] [--audio <wav> \| --no-audio] [--port 3051] [--overwrite] [--stills-only] [--assemble-only]` | Render the loaded story as stills, assemble with ffmpeg + soundtrack. The slug only names the output — the story rendered is whatever is loaded in `src/story/currentStory.ts`. |
| `preset <name> [--preview]` | Render a named verification preset (see `list`). Video outputs listed in a preset are deliberately skipped. |
| `list` | List the 10 presets and their descriptions. |

Presets (verified via `node scripts/render.mjs list`): `kickcheck`,
`kit-fly`, `kit-flywave`, `kit-poselab`, `circle-stills`, `r6kit`,
`facelab`, `dialogue-test`, `asset-stills`, `wide`. Preset stills
are written under `~/workspace/videos/noob-compare` by default
(`defaultOutDir` in `scripts/render_lib.mjs`); set `REMOTION_OUT`
to redirect them, e.g. `REMOTION_OUT=out/presets node
scripts/render.mjs preset kickcheck`. `CHROME_BIN` overrides the
browser executable used for rendering.

Related tools (not the render CLI):

- `python scripts/render_chunks.py stories/<slug>.py --chunks 10`
  — an older chunked renderer: renders a story in N frame ranges
  with the Remotion CLI, concatenates the video-only chunks with
  ffmpeg, muxes the soundtrack once. `--chunk-index N` renders one
  chunk only (for farming out), `--plan` prints the chunk commands,
  `--assemble-only` stitches existing chunks. It is the prior art
  for the GitHub Actions 10-way split; the Actions workflow should
  use `scripts/render.mjs story --start/--end --stills-only` per
  shard instead (same stills+ffmpeg path as a normal render).
- `python build_story.py stories/<slug>.py` — test helper: builds
  `currentStory.ts` with fake beat timings (no TTS). Test only.

## Repo layout

| Path | What it is |
|---|---|
| `src/` | Engine code: `MotionBlocksComposition.tsx` (the Short), `Root.tsx` + `index.ts` (all demo compositions), `short-entry.tsx` (MotionBlocks only), `components/` (characters, `ShortsHUD` captions/bubbles), `kit/` (kit-character clips), `characters/` (looks), `environments/` (sets), `story/` (camera, keyframes, loaded `currentStory.ts`), `types/schema.ts` |
| `stories/` | 44 story files + `_template.py`. `dialogue_test.py` and `kit_heroes_test.py` are verification stories referenced by `RIG_CONTRACT.md`. `gravity_off_v1.py` is the superseded v1, kept deliberately (see its header + `gravity_off.py`). |
| `scripts/` | `make_short.py` (story pipeline), `render.mjs` + `render_lib.mjs` + `render_presets.mjs` (render CLI), `render_chunks.py` (older chunked renderer), `make_music_*.py` (music generation), `shorts/` (`audio.py`, `scene.py`) |
| `.agents/skills/motion-blocks-director/` | The director skill: story format, catalogs, rules |
| `archive/` | Superseded code kept for reference, not used: `root-render-scripts/` (52 one-off `render-*.mjs` scripts from Nov 20–22, all superseded by `scripts/render.mjs`), `test-stories/` (5 `_test_*.py` prop/camera fixtures). See `CLEANUP.md`. |
| `AGENTS.md`, `RIG_CONTRACT.md` | Agent instructions + rig contract (read both before changing characters, poses or scenes) |
| `CONTRIBUTING.md`, `ARCHITECTURE.md` | How to contribute; how the pieces fit together |
| `package.json`, `package-lock.json` | Deps, exact-pinned: Remotion 4.0.544, three 0.163, React 18, TypeScript 5.4 |
| `remotion.config.ts`, `tsconfig.json` | SwiftShader/Chrome flags + concurrency; TS config (`include: src` only) |

## What is NOT in this repo (read before you clone)

**In the repo — fixture audio for the committed story.** `public/`
contains two committed fixture files that belong to the ice_floats
story loaded in `src/story/currentStory.ts`: `soundtrack.wav`
(2,786,908 bytes, 58.06 s, mono 24 kHz PCM — narration + music +
SFX) and `kokoro-cues.json` (11,896 bytes — 13 beat timings and
101 caption timings matching `currentStory.ts` exactly). They are a
fixture for fresh clones and the automated test, so a clone can
render the loaded story with audio and mux a soundtrack without the
voice models or the music library — not production audio. Do not
treat them as the soundtrack for any other story: if you load a
different story, regenerate its audio (see below) or audio and
video will not match. Everything else under `public/` stays out of
git (see `.gitignore`).

| Missing | Why it matters | Where it comes from |
|---|---|---|
| `public/music/` (~167 MB) | `make_short.py` cannot build a soundtrack without the music library | Synced separately (shared drive), not git. `public/` is gitignored except the two fixture files above. |
| `models/` — Kokoro TTS voice models (~338 MB) | No narration without them; the pipeline fails at the TTS step | Synced separately. See README's Kokoro setup in the old docs / `CLEANUP.md`. |
| `references/` (~352 MB) | Reference frames/sheets for style checks | Kept out entirely. |
| `node_modules/` (2.1 GB) | Rebuilt with `npm ci` | — |
| Any YouTube / API credentials | There are none in this repo (verified by grep, 2026-11-26) | — |

Regenerating real audio: once `models/` and `public/music/` are
synced, run `venv/bin/python scripts/make_short.py
stories/<slug>.py --stills` — it rebuilds `public/soundtrack.wav`
+ `public/kokoro-cues.json` (overwriting the fixture files) and
`src/story/currentStory.ts` for that story. Use the venv Python —
the system `python3` has no Kokoro. `--skip-tts` reuses the
existing wav + cues when beats/SFX/music did not change.

The committed `src/story/currentStory.ts` is the ice_floats story
(1742 frames) so the repo builds and renders out of the box. It is
generated state — `make_short.py` overwrites it on every story build;
never hand-edit it. If you need a different story loaded, run
`make_short.py` for that story (needs the assets above) or
`build_story.py` for a fake-timing test build.

### Verify your clone

From a fresh clone, after `npm ci` and `npx tsc --noEmit`, render
one test still of the loaded ice_floats story (frame 300) with a
pinned port:

```bash
node scripts/render.mjs still --comp MotionBlocks --frames 300 \
  --out-dir out/test-still --port 3051
# → out/test-still/frame-0300.png (1080×1920). A non-blank frame
#   with the kitchen scene and a caption means the clone builds and
#   renders. This still render does not use audio; the fixture
#   soundtrack is exercised by a `story` render, which muxes
#   public/soundtrack.wav (see "Making a story, end to end").
```

## Known limitations / gotchas

- **Software GL is slow.** Headless Chromium has no GPU; three.js
  runs on SwiftShader. On the 1.5-shared-CPU cleanup VM one still
  takes ~40 s; a 60 s Short (1,853 frames) would take ~21 h there.
  Real renders run on 4-CPU boxes (~70–160 min per Short) or, for
  the GitHub Actions test, split across 10 parallel jobs.
- **Pin the port.** Remotion's serve step scans ports 3000–3100;
  always pass `--port` (3050 for stills/presets, 3051 for stories)
  so concurrent renders don't fight over ports. Parallel range
  jobs must each get a distinct port.
- **Parallel story renders must share one prebuilt bundle.**
  `render.mjs story` rebuilds `out/bundle-story` on every
  invocation, so ten parallel shard jobs would race on the same
  directory and corrupt each other. Bundle once
  (`npx remotion bundle src/short-entry.tsx --out-dir=out/bundle-shared`)
  and pass `--bundle out/bundle-shared` to every shard job — the
  `--bundle` flag skips the rebuild entirely (verified in this
  cleanup: a `--bundle` story range rendered correctly).
- **`/tmp` is small on some machines** (512 MB tmpfs on the cleanup
  VM). `render.mjs story` bundles to `out/bundle-story` under the
  repo instead of `/tmp` for exactly this reason; do not
  `rm -rf /tmp/remotion-*` while a render is running.
- **Bundle time is paid per job.** Every `render.mjs` invocation
  re-bundles (~6 s with the webpack cache, longer cold). In
  GitHub Actions each shard job pays this once.
- **Resume skips on existence only.** A still that already exists is
  skipped even if it is blank or corrupt — use `--overwrite` if you
  suspect bad frames, and always spot-check assembled video.
- **The `story` slug does not select the story.** It only names the
  output files. The story rendered is always the one loaded in
  `src/story/currentStory.ts`. Rendering `story no_friction` while
  ice_floats is loaded produces ice_floats content named
  `no_friction.mp4`. Always run `make_short.py` first.
- **Caption font is not bundled.** Captions use the `Inter` font
  stack with system fallbacks; Inter is not in the repo and is not
  installed on a stock Linux runner, so caption metrics come from
  the fallback font. Frames are still deterministic on identical
  machines, but can differ between machines with different fonts.
- **`public/soundtrack.wav` is the audio source of truth at render
  time.** `MotionBlocksComposition` plays it via
  `<Audio src={staticFile('soundtrack.wav')} />`; the ffmpeg
  assembly muxes the same file. If the wav and `currentStory.ts`
  are from different stories, audio and video will not match.
- **GitHub Actions workflow** will live at
  `.github/workflows/` (not yet created — see `CLEANUP.md`).
