# Motion-Blocks Engine — Agent Instructions

Whenever the user asks to create, write, or render a motion-blocks Short video (or gives a story topic/rule):

1. Read and follow the [`motion-blocks-director`](./.agents/skills/motion-blocks-director/SKILL.md) skill.
2. Write one story file `stories/<slug>.py` (copy `stories/_template.py`; full example: `stories/hair_color.py`) from the catalogs in the skill: beats, music, SFX, cast, scenes.
3. Run the pipeline end-to-end without asking unnecessary permission questions
   (use the venv Python `venv/bin/python` — Kokoro TTS lives in the venv;
   the system `python3` has no Kokoro and fails at the TTS step with
   `No module named 'kokoro_onnx'`):
   - `venv/bin/python scripts/make_short.py stories/<slug>.py --stills`
     - Fix every `RULE CHECKS FAILED` line.
     - Inspect `out/preview/<slug>/sheet-*.png`.
   - `venv/bin/python scripts/make_short.py stories/<slug>.py --skip-tts --render` → `out/<slug>.mp4`
     (legacy Remotion video-render path — kept as fallback only)
   - Story videos use stills + ffmpeg, never the Remotion video renderer (proven
     to drift deterministically and glitch with blank/tiled frames):
     `node scripts/render.mjs story <slug> --port 3051` → `out/<slug>.mp4`
     (renders all frames as stills via renderStill, assembles with ffmpeg at
     30fps / libx264 / CRF 18 / yuv420p / faststart, muxes
     `public/soundtrack.wav`; `--start/--end` for ranges, existing stills are
     skipped on re-runs, `--assemble-only` to re-assemble rendered stills)

Hard rules, enforced by the skill and the build checks:
- The script opens with the big "What if …?" question (the title question, e.g. "What if gravity was half as strong?"), then the "In this town," / "In this world," setup follows. (Channel rule, the maintainer 2026-11-22 — the "What if" question must be asked in the narration, not carried by the title alone.)
- A camera cut every 2–3 s; no shot longer than 3.5 s.
- Narrator voice `af_heart`.
- Music from `public/music/`.
- Soft SFX presets only.
- Actors at least 4.5 studs apart.

Never edit `src/story/currentStory.ts` by hand; it is generated.
