# no_friction test fixture

Used by `.github/workflows/render-test.yml` to render the no_friction Short
("The Day Friction Disappeared", 1,434 frames, 47.80 s) on GitHub Actions
and compare it against the v4 ground truth.

## Files

- `currentStory.ts` — the loaded story, regenerated from
  `stories/no_friction.py` with the real Kokoro cues
  (`fix1/kokoro-cues.json`, 17 beats, 1,434 frames) using the repo's own
  generator (`scripts/shorts/scene.py` via `write_story`). It is the v4
  story: the current story source was re-staged after fix1, so the older
  saved story file (1,395 frames) does NOT reproduce v4.
- `soundtrack.wav` — the real narration audio (47.799 s), copied from the
  fix1 render. The stitch job muxes it onto the concatenated segments.

## Known difference vs v4 (measured locally, 2026-11-26)

Frames rendered locally from this fixture match the v4 video at
x264-compression noise level (mean absolute difference ~2–6 per channel)
everywhere except one shot, roughly frames 1211–1283, where the camera
push-in sits a couple of frames ahead of v4 (mean absolute difference
~14.5, same shot, same pose, same caption). That offset is in the
fixture itself, not in the Actions run: any Actions-vs-v4 comparison
should expect it there and treat it as a known baseline difference,
not a render defect.
