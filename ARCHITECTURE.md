# Architecture

How a story file becomes a video, and how the pieces fit together.
For the day-to-day workflow see `README.md`; for the rules see
`AGENTS.md` and `RIG_CONTRACT.md`.

## The two halves

The repo has two halves that meet at exactly two generated files:

```
stories/<slug>.py            (source of truth: beats, cast, scenes)
        │  scripts/make_short.py
        ▼
src/story/currentStory.ts    (generated story data: scenes, keyframes, captions)
public/soundtrack.wav        (generated audio: narration + music + SFX)
public/kokoro-cues.json      (beat timings + captions, from the TTS)
        │  scripts/render.mjs story
        ▼
out/<slug>.mp4               (stills + ffmpeg)
```

- **Story pipeline (Python):** `scripts/make_short.py` loads a story
  `.py`, builds the soundtrack with `scripts/shorts/audio.py`
  (Kokoro TTS narration, voice `af_heart`, plus music from
  `public/music/` and SFX), converts the story's `scenes(T)` into
  concrete scenes with `scripts/shorts/scene.py` (`write_story`),
  runs the rule checks, typechecks, and writes
  `src/story/currentStory.ts`. Preview stills go through
  `scripts/render.mjs still` at half scale.
- **Render pipeline (Node):** `scripts/render.mjs` bundles
  `src/short-entry.tsx` (RobloxShort only), renders every frame as
  a PNG still with Remotion's `renderStill`, and assembles with
  ffmpeg (`scripts/render_lib.mjs: assembleStillsToVideo`).

Neither half knows about the other except through those two files —
which is why they must always be generated together. A stale
`currentStory.ts` with a fresh `soundtrack.wav` (or vice versa)
produces a video whose audio does not match its pictures, and
nothing in the pipeline detects that.

## Composition tree

`src/Root.tsx` registers every composition (RobloxShort, BoltBoy
showcases, KitPoseLab, KitFly, FaceLab, KickCheck, BowCheck,
ClipCheck, R6KitCheck, KitStoryCheck, CircleShowcase, WaistCheck,
TurnCheck, PerformanceLab, CharacterLineup, LocationGallery,
AssetCheck, …). Two entry points exist:

- `src/short-entry.tsx` — registers **only** `RobloxShort`. This is
  what the story render bundles: smaller, faster, and the only
  composition the story path needs.
- `src/index.ts` — registers everything in `Root.tsx`. Used by the
  `still` / `range` / `preset` commands and by Remotion Studio.

`RobloxShortComposition` (one frame) does, in order:

1. Finds the current scene for the frame (`frame` in
   `[startFrame, endFrame)`, else the last scene).
2. Computes the camera once via `cameraStateForFrame`
   (`src/story/camera.ts`) and shares it with the HUD, so the 2D
   bubbles and the 3D camera can never drift apart.
3. Renders the 3D scene in `<ThreeCanvas>` (three.js via
   `@react-three/fiber`): sky/fog, lights, the location set
   (`EnvironmentSwitch`), then one component per actor —
   `R6Character` for R6 rigs, `BoltBoy` / `CasualMan` / `WingedBoy` /
   `ClassicNoob` / `BlockyTRex` for kit characters. A character's
   `anim` is mapped to a kit clip (`STORY_ANIM_TO_CLIP`); the four
   anims with no kit clip (`sleep`, `knocked`, `panting`, `sit`)
   fall back to `idle` — a known gap, documented in the file.
   Actors parked at `y <= -50` (the OFF park at `[0, -80, 0]`) are
   not rendered in 3D.
4. Overlays `ShortsHUD`: narration captions (two-word chunks, font
   shrunk by canvas measurement until the ink fits the band) and
   chat bubbles projected from the speaker's head position with the
   same camera. Bubbles are hidden when the speaker is off-screen.
5. Plays `staticFile('soundtrack.wav')` unless muted.

## How a frame is determined (determinism)

Rendering is a pure function of `(frame, currentStory, props)`:

- Camera, character keyframes and captions are interpolated from
  the story data for that exact frame (`cameraStateForFrame`,
  `evaluateCharacterKeyframes`, caption lookup by frame range).
- Cyclic clips (walk/idle/dance) use global frame time
  (`frame / fps`), so they stay continuous across keyframes.
- No `Date.now`, `Math.random`, network fetch or wall-clock input
  exists in `src/` (verified by grep, 2026-11-26). The only
  `Date.now` uses are elapsed-time logging in `scripts/render.mjs`.
- The remaining cross-machine variance is the **caption font**:
  `Inter` is named in the font stack but not bundled or installed
  on stock Linux, so the fallback font's metrics apply. Identical
  machines render identical frames; machines with different fonts
  may not.

## Render path in detail

`scripts/render.mjs` subcommands (see README for the table):

- `still` / `range`: `renderStillBatch` (`render_lib.mjs`) opens
  **one** warm Chromium browser and reuses it across all stills,
  caching compositions by `(id, inputProps)`. Stills are skipped
  when the output file already exists (`skipIfExists`) — resume
  is by file existence only, with no content check.
- `story`: opens a browser once to read the composition's
  `durationInFrames`/fps, then `renderStillBatch` renders the
  requested range as `frame-%05d.png` stills into
  `out/stills/<slug>/`, then `assembleStillsToVideo` runs ffmpeg
  (`-framerate 30 -start_number <start>`, libx264 CRF 18,
  yuv420p, faststart; audio seeked to `start / fps` for ranges)
  and verifies with ffprobe: exact frame count, duration within
  0.15 s, audio stream present when audio was given.
- `preset`: renders the stills listed in `render_presets.mjs`.
  Presets may also list videos; those are deliberately skipped
  with a log line (video rendering is not ported into this CLI).

Concurrency is ~50% of vCPUs, RAM-capped at ~2 GB per SwiftShader
tab (`safeConcurrency` in `render_lib.mjs`, same rule in
`remotion.config.ts`), overridable with `REMOTION_CONCURRENCY`.
On a 2-vCPU runner that is 1 browser tab.

`remotion.config.ts` pins the software-GL setup for every Remotion
invocation: `swangle`, `chrome-for-testing`, `--enable-unsafe-swiftshader`,
`--disable-dev-shm-usage`, 1024 MB GPU-memory budget, JPEG image
format at quality 82 (video path only — stills are PNG).

## The older chunked renderer

`scripts/render_chunks.py` predates `render.mjs story`. It renders a
story in N frame ranges using the Remotion CLI (`--frames`, muted),
concatenates the video-only chunks with ffmpeg, and muxes the full
soundtrack once. It understands `--chunks`, `--workers`,
`--chunk-index` (one chunk only), `--plan`, `--resume` and
`--assemble-only`. It is kept because it is the proven pattern for
splitting a render across machines; the GitHub Actions test uses
the newer `render.mjs story --start/--end --stills-only` per shard
instead, because that stays on the stills+ffmpeg path.

## What lives where (code map)

- `src/types/schema.ts` — the story data model (`RobloxShortStory`,
  scenes, keyframes, captions, cast).
- `src/story/camera.ts` — camera interpolation + 3D→screen
  projection (shared by the 3D rig and the HUD).
- `src/story/keyframes.ts` — character keyframe interpolation.
- `src/characters/look.ts` — actor → look/kit/scale resolution.
- `src/kit/kit.tsx` — kit-character clips and poses.
- `src/components/R6Character.tsx` — the R6 rig.
- `src/environments/` — location sets + `locations.ts`
  (exterior/interior flags the composition uses for sky/fog).
- `scripts/shorts/scene.py` — story `.py` → scenes + rule checks.
- `scripts/shorts/audio.py` — soundtrack + cue timings (Kokoro).
- `scripts/render_presets.mjs` — the 10 named verification presets.
