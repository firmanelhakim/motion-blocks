# public/ — fixture audio for the committed story

This folder holds the soundtrack and narration cues for the story
currently loaded in `src/story/currentStory.ts` (ice_floats, 1742
frames at 30 fps). They are committed fixture files, not production
audio: they exist so a fresh clone can render the loaded story with
audio and so the automated test can mux a soundtrack without the
voice models or the music library.

- `soundtrack.wav` — 2,786,908 bytes, 58.06 s, mono 24 kHz PCM.
  Narration (Kokoro TTS, voice `af_heart`) + music + SFX for
  ice_floats.
- `kokoro-cues.json` — 11,896 bytes. Beat timings (13 beats) and
  caption timings (101 captions) matching `currentStory.ts`
  exactly; `durationSeconds` 58.06, `durationInFrames` 1742.

Everything else under `public/` stays out of git (see `.gitignore`):
in particular `public/music/` (~167 MB) is synced separately and is
not in this repo.

Regenerating real audio: run the story pipeline with the voice
models synced — `venv/bin/python scripts/make_short.py
stories/<slug>.py --stills` rebuilds `soundtrack.wav` +
`kokoro-cues.json` and overwrites these fixture files (and
`currentStory.ts`) for that story. See the README, "Making a story,
end to end".
