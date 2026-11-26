---
name: motion-blocks-director
description: >-
  End-to-end pipeline for 9:16 3D blocky storytelling Shorts ("In this town / In this world, <absurd rule>...")
  built with Remotion + Three.js. A video is assembled from ready-made parts: a script of beats, the character
  constructor (hair/clothes/accessories), town locations, animations, props, camera helpers, SFX presets and a music
  track. All of it goes into one story file that one command turns into an MP4.
  Activate whenever the user asks to create, write, or render a motion-blocks Short or gives a story topic/rule.
---

# Motion-Blocks Director

A Short is **one Python file** in `stories/<slug>.py`. It holds the script, music, SFX, cast and scenes, all picked from the catalogs below. One command does the rest:

```powershell
python scripts/make_short.py stories/<slug>.py --stills            # voice+music+SFX -> scenes -> rule checks -> typecheck -> preview stills
python scripts/make_short.py stories/<slug>.py --skip-tts --render # final 1080x1920 30fps MP4 -> out/<slug>.mp4
```

Run the whole pipeline end-to-end without asking unnecessary permission questions. Start from `stories/_template.py`. `stories/hair_color.py` is a complete working example.

---

## 0. Hard rules (taken from `references/*.mp4`)

| Rule | Value |
|---|---|
| **Opening** | The very first words are **"In this town, …"** or **"In this world, …"** followed by the absurd rule. No intro, no title card. |
| **Length** | 35–45 s, 14–16 beats, English. |
| **Cuts** | A new camera shot every **2–3 s** (the references average 1.2–1.6 s per shot). The build fails any shot longer than **3.5 s** or shorter than **1.0 s**. Cut on beat boundaries and big words. |
| **Voice** | Narrator `af_heart`, speed 1.18 (default; 1.16–1.22 is fine). This voice was measured as the closest Kokoro match to the reference narrator: median pitch ≈ 200 Hz, ≈ 5.8 syllables/s. No dead air: 0.06–0.10 s pauses, 0.12–0.30 s only before a reveal or the final line. |
| **Shouts** | Climax shout words are separate beats with `"shout": True`, one word each ("GINGER!" / "IS!" / "MAYOR!"). Use a contrasting voice (`am_michael`, `am_adam`, `af_bella`). |
| **Music** | `public/music/fallen-down.mp3` by default (any file in `public/music/`). It is automatically levelled and ducked under the voice. Drop it out before the big reveal (`dropouts`). |
| **SFX** | Soft presets only (section 5). Never raw square/saw beeps. |
| **Captions** | Generated automatically from the beats: 1–2 words, white, black outline, at 68 % height. No other HUD: no leaderboards, chat bubbles or title bars. |
| **Spacing** | Actor centers ≥ **4.5** studs apart at every frame (scaled actors: 4.5 × average scale). No overlapping, no noclipping into each other, furniture or walls. |
| **Framing** | Faces visible. Never cut a character in half at the frame edge in a 2-shot. Three actors side by side need a wide shot (camera z ≈ 20–23, fov 58–60). |

---

## 1. Story formula

1. **Hook (0–6 s)**: "In this town, [absurd rule]." + the consequence. Visual: `town_overview` aerial shot.
2. **World-building (6–16 s)**: 2–3 concrete, visual ways people live with the rule. Each one gets its own location or shot.
3. **Personal stakes (16–26 s)**: the narrator ("I/me"), a sibling, a friend or a parent, and an exception to the rule. Add a bully or another antagonist.
4. **Climax + twist (26–42 s)**: crisis → shout words → payoff → a last-line twist ("But last night…").

Write every beat as something you can **show** with the parts below: an actor + animation + expression + prop in a location. The rule should be visible in 3D, for example hair color, a crown, a floating counter, a halo or a chalkboard text.

---

## 2. Story file anatomy (`stories/<slug>.py`)

```python
from shorts.scene import HALF, OFF, hold, kf, shot, face, close_up, medium, wide, cover, split_shots

TITLE = "HAIR COLOR DECIDES YOUR LIFE"
BEATS = [  # one beat ≈ one sentence; ids are referenced by SFX, MUSIC and scenes
    {"id": "b1", "text": "In this town, your hair color decides your whole life.", "pause": 0.08},
    {"id": "w1", "text": "GINGER!", "voice": "am_michael", "shout": True, "pause": 0.12},
]
MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05,
         "dropouts": [("b10+0.3", "w3.end")]}
SFX = [("b1", "whoosh"), ("b2+0.15", "pop", {"f": 600}), ("w3", "reveal")]
CAST = {"hero": {"extends": "kid_boy", "hair": {"color": "ginger"}, "freckles": True}}

def scenes(T):          # T.B["b3"] = start frame of beat b3, T.E["b3"] = end frame, T.END, T.f("b3+0.5")
    S2 = T.B["b2"] - 1
    return [
        {"id": "hook", "location": "town_overview", "startFrame": 0, "endFrame": S2,
         "cameraShots": [shot(0, S2, [-10, 62, 74], [-2, 46, 56], [8, 0, -6], [6, 2, -8], 55)],
         "characters": {}},
        ...
    ]
```

**Time references** in `SFX` / `MUSIC.dropouts` / `T.f()`:
- `"b3"` = start of beat b3;
- `"b3.end"` = end of beat b3;
- `"b3+0.4"` / `"b3.end-0.2"` = offset in seconds.

**Scene dict**:

| Key | Meaning |
|---|---|
| `id` | Unique scene name. |
| `location` | One of the locations in section 4. |
| `startFrame`, `endFrame` | Scenes must be contiguous from frame 0 to `T.END`. |
| `cameraShots` | List of shots covering the whole scene, each 1–3.5 s. |
| `characters` | `{actorId: [keyframes]}`. |
| `variant` | House / home colour (optional). |
| `isNight` | Night lighting (optional). |
| `boardText` | Classroom chalkboard lines (optional). |
| `schoolName` | Name on the school sign (optional). |
| `skyColor` | Sky colour override (optional). |

Start a new scene at `T.B[beat] - 1`, so the cut lands just before the line about the new place.

---

## 3. Characters — constructor (`src/characters/look.ts`)

Every actor id used in a scene must be in `CAST`, or be a preset name. A cast entry is either a preset name (`"bully"`) or an override:

```python
"hero": {"extends": "kid_boy",                       # start from a preset (optional)
         "skin": "light",
         "hair": {"style": "messyFringe", "color": "ginger", "ombre": None},
         "top": {"style": "hoodie", "color": "green", "secondary": "white", "sleeves": "long"},
         "bottom": {"style": "jeans", "color": "denim", "legs": None},
         "shoes": {"style": "sneakers", "color": "white", "sole": "white"},
         "accessories": ["crown", {"type": "cap", "color": "navy"}],
         "facialHair": "mustache", "freckles": True, "blush": False,
         "scale": 1.0}                                # 0.55 baby, 0.75 small kid, 1.2 giant
```

| Part | Options |
|---|---|
| **Presets** | `kid_boy`, `kid_girl`, `little_brother`, `schoolboy`, `schoolgirl`, `nerd`, `bully`, `cool_kid`, `teen_girl`, `dad`, `real_mom`, `teacher_woman`, `teacher_man`, `principal`, `grandpa`, `grandma`, `classic_noob`, `noob`, `bacon`, `guest`, `teacher`, `builderman`, `mom` |
| **hair.style** | `bacon`, `messyFringe`, `sidePart`, `fluffySwept`, `slickBack`, `spikyAnime`, `curly`, `buzz`, `bob`, `wavyLong`, `ponytail`, `bun`, `pigtails`, `grandpa`, `none` |
| **hair.color** | `black`, `darkBrown`, `brown`, `lightBrown`, `blonde`, `goldenBlonde`, `platinum`, `ginger`, `auburn`, `gray`, `white`, `pink`, `blue`, `purple` (or hex). `ombre` = tip colour for long hair. |
| **skin** | `porcelain`, `fair`, `light`, `medium`, `tan`, `brown`, `dark`, `deep`, `classic` (yellow noob) |
| **top.style** (`secondary` = accent) | `tshirt` (secondary → chest logo), `hoodie` (inner tee), `pullover`, `plaid`, `polo`, `blouse`, `sweater` (stripe), `vest` (shirt + sleeves), `jacket` (stripes), `uniform` (blazer + crest, secondary = tie), `suit` (tie), `dress`, `tank` · `sleeves`: `long` / `short` / `none` |
| **bottom.style** | `pants`, `jeans`, `shorts`, `skirt` · `legs` = tights/socks colour |
| **shoes.style** | `sneakers`, `boots`, `formal` |
| **accessories** | `cap`, `backwardsCap`, `beanie`, `glasses`, `sunglasses`, `headphones`, `bow`, `crown` |
| **face** | `facialHair`: `mustache` / `beard` / `stubble`, `facialHairColor`, `freckles`, `blush` |
| **cloth colours** | `white`, `cream`, `lightGray`, `gray`, `charcoal`, `black`, `red`, `darkRed`, `maroon`, `pink`, `rose`, `orange`, `mustard`, `yellow`, `lime`, `green`, `darkGreen`, `olive`, `teal`, `cyan`, `sky`, `blue`, `royal`, `navy`, `purple`, `lavender`, `brown`, `tan`, `khaki`, `denim`, `darkDenim` (or hex) |

- **One look per hero** and keep it for the whole video. Every hero must be recognisable by hair colour and outfit.
- **Changing a look mid-story** (dyed hair, a crown, new clothes) means a second cast entry, e.g. `hero_mayor = {**HERO, "accessories": ["crown"]}`. Swap the two with the parking trick in section 6.
- **Check all parts visually** with the lineup render:
  ```powershell
  npx.cmd remotion render src/index.ts CharacterLineup out/lineup --sequence --image-format=png --gl=angle
  ```

---

## 4. Locations — one persistent town (`src/environments/`)

The stage of every location is the local origin. Put actors at x ∈ [-6, 6], z ∈ [-3, 5], y = 0. The camera stands on +Z and looks toward −Z (z ≈ 11–23). Default establishing cameras are in `LOCATION_INFO` (`src/environments/locations.ts`).

| `location` | What is there | Extra keys |
|---|---|---|
| `town_overview` | Aerial view of the whole town for the hook. Camera ≈ `[-10, 62, 74]` → `[8, 0, -6]`, fov 55. No actors. | – |
| `street` | Main St sidewalk in front of the blue house; road toward the camera, crossroads to the right. Clear zone for actors: x ∈ [-10, 2], z ≈ 0.5. There is a hydrant at x ≈ -5.5 and a traffic light at x ≳ 4, so keep actors and cameras away from them. | – |
| `crossroads` | Crosswalk at Main × Maple, school on the right | – |
| `school_exterior` | Schoolyard before the entrance (sign, clock, columns, flagpole, bike rack, bus); the steps are far back (z ≈ -13) | `schoolName` |
| `house` | Front yard of a hero house; front wall at z ≈ -4. One-storey `yellow` / `green` have a porch: actors stand at z ≈ -2.6 between the columns (x = ±2, ±5, z ≈ -1.1). | `variant`: `blue` (2 floors), `yellow` (porch), `red` (brick), `white` (modern + garage), `green` (porch + garage) |
| `shop` | Sidewalk in front of RoMart (awning, vending machine) | – |
| `playground` | Town park: slide tower, swings, sandbox, seesaw | – |
| `classroom` | Chalkboard (back), teacher desk at x -8..-3, z -5.6..-3.2. Student desks at x ±5.5, ±9.5 / z 0.5, 4.5. Free aisle x ∈ [-3, 3]. | `boardText` (≤ 4 lines) |
| `hallway` | Lockers on the back wall, ROOM 101 door, banner, trophy case | – |
| `living_room` | Sofa against the back wall, TV on the left wall, coffee table at z ≈ -1.4 | `variant` |
| `kitchen` | Counters, sink and stove on the back wall, fridge back-left, dining table at x ≈ 8 | `variant` |
| `bedroom` | Bed back-left (mattress top y ≈ 2.1 at x ≈ -7, z ≈ -4.4), gaming desk back-right, wardrobe | `variant` |

- A family keeps **one `variant`** for its `house`, `living_room`, `kitchen` and `bedroom`.
- `isNight: True` works everywhere: windows glow, lamps light up.
- **See every location** with the gallery render:
  ```powershell
  npx.cmd remotion render src/index.ts LocationGallery out/locations --sequence --image-format=png --gl=angle
  ```
- **New buildings and props** go in `environments/town/buildings.tsx` / `props.tsx` and are placed in `TownMap.tsx`. Reusable helpers are in `environments/kit.tsx`.

---

## 5. Animation, expression, prop, SFX catalogs

| Kind | Values |
|---|---|
| `anim` | `idle`, `walk`, `sprint`, `jump`, `wave`, `point`, `dance`, `celebrate`, `panting`, `knocked` (lying down), `sleep` |
| `expression` | `smile`, `laugh`, `shocked`, `panic`, `angry`, `cool`, `deadpan`, `sleeping` |
| `prop` (in hand / on body) | `none`, `backpack`, `bloxy_cola`, `pointer`, `pan`, `clipboard` (also "rule book"), `hammer`, `wood_plank`, `binoculars`, `mouth_tape`, `halo_gold`, `halo_red`, `creepy_shadow` |
| rule counters (floating badge) | `counter_high` (912,450), `counter_mid` (42,810), `counter_bully` (614,200), `counter_3`, `counter_2`, `counter_1`, `counter_0` |
| **SFX presets** `(time, name, {opts})` | `whoosh` (transition, `dur`), `swish` (broom / brush / wave), `pop` (list item / comedic, `f` pitch), `pop_down` (thrown away), `bubbles` (washing, magic), `laugh` (crowd laughs), `sparkle` (magic / rich / shiny), `ding_dong` (school bell / doorbell), `bell_low` (ominous line), `sad` (lonely / failure), `thud` (drop / door / fall), `impact` (shout word / hit), `riser` (tension, `dur`), `reveal` (payoff chord), `twist` (dark final twist). Every preset takes `vol`. |

- **SFX density**: about one accent per beat, placed on the word it illustrates.
- **Before the reveal**: a `riser` into the shouts, `impact` on each shout word, `reveal` on the last one.
- **Ending**: `twist` on the final line.

**Music options**: `file` (relative to `public/`), `start` (skip seconds of the track), `under_voice` (≈ 0.02), `gaps` (≈ 0.05), `dropouts` [(from, to), …], `fade_out`.

---

## 6. Choreography & camera helpers (`scripts/shorts/scene.py`)

**Keyframe helpers**

| Helper | What it does |
|---|---|
| `kf(frame, pos, rotY, anim, expr, prop=None)` | One keyframe. Position and rotation interpolate to the next keyframe; anim, expression and prop switch at the keyframe. |
| `hold(a, b, pos, rotY, anim, expr, prop)` | Stand still from frame `a` to `b`. |
| `face(src, dst)` | The `rotY` that turns an actor at `src` to look at `dst`. |
| `HALF` | `rotY` for facing screen-right. `0` faces the camera, `-HALF` faces left, `±π` turns the back to the camera. |
| `OFF` | Parking spot `[0, -80, 0]` for swapped-out actors. |

- **Walking**: keyframe A (`walk`) → keyframe B (`walk`) at the destination, then a keyframe a few frames later with `idle` and the final `rotY`.
- **Swapping a look** (e.g. the crown appears): at frame `F`, actor A has `kf(F, pos)` and `kf(F+1, OFF)`; actor B has `kf(F, OFF)` and `kf(F+1, pos)`.

**Camera helpers**

| Helper | Use |
|---|---|
| `shot(a, b, fromPos, toPos, fromTarget, toTarget, fov, shake)` | Manual camera move. Always move a little: a push, drift or rise. |
| `wide(a, b, center)` | Establishing shot, 3 actors side by side. |
| `medium(a, b, center)` | Waist-up shot of 1–2 actors. |
| `close_up(a, b, actorPos, scale=1)` | Face close-up; aims lower for scaled actors. |
| `cover(a, b, [maker, …])` | **Default.** Fills a scene with ~2.5 s cuts and cycles through the makers, e.g. `cover(a, b, [lambda a, b: wide(a, b), lambda a, b: close_up(a, b, HERO_POS)])`. |
| `split_shots(a, b, [maker, …])` | Exactly one cut per maker, split evenly. |

- `shake` 0.04–0.12 is for shouts and impacts only.
- **Cut rhythm**: alternate wide → medium → close-up, and reverse angles with a different camera x. Start each scene with a shot that shows the location. Put a close-up on every emotional word (shocked or laughing faces). Character head height is about y 4.4 (× scale).

**Spacing rules** (checked automatically):
- An R6 actor is about 4 studs wide with arms. Keep centers ≥ 4.5 apart; use 5+ when both actors wave, point, celebrate or dance.
- Three in a row: x = -4.5, 0, 4.5. With more actors, add a second row ≥ 3 studs behind, in the gaps.
- Walking paths must not cross other actors, desks, porch columns, beds or sofas. The check only measures actor-to-actor distance, so look at the stills for props and walls.
- Don't put an actor right in front of another in the camera's line of sight. Offset them in x or move the camera.

---

## 7. Runbook

1. **Write** `stories/<slug>.py`, starting from `stories/_template.py`: TITLE, BEATS (hook "In this town/world…"), MUSIC, SFX, CAST, `scenes(T)`.
2. **Build and preview**:
   ```powershell
   python scripts/make_short.py stories/<slug>.py --stills
   ```
   - It writes `public/soundtrack.wav` + `public/kokoro-cues.json`, `src/story/currentStory.ts` (generated, don't edit), and `out/preview/<slug>/f*.png` + `sheet-*.png` (one still per camera shot).
   - It prints `RULE CHECKS FAILED` lines (`SPACING`, `SHOTS`, `SCENES`). **Fix all of them.**
3. **Inspect the contact sheets** (read the PNGs). Check each frame for:
   - faces visible and nobody cut in half;
   - no overlapping or clipping actors;
   - the action matches the caption;
   - the location reads clearly.

   Fix the story file, then re-run with `--skip-tts`. Only add `--skip-tts` when BEATS, SFX and MUSIC are unchanged; otherwise re-run without it.
4. **Render**:
   ```powershell
   python scripts/make_short.py stories/<slug>.py --skip-tts --render
   ```
   → `out/<slug>.mp4`. Report the path to the user.

**Windows notes**
- Use `npx.cmd`, never bare `npx`, in PowerShell.
- Rendering needs `--gl=angle` (`make_short.py` already passes it).
- If a Bash heredoc with Python fails, write the script to a file and run it.

---

## 8. Project map

| Path | Purpose |
|---|---|
| `stories/*.py` | One file per video (the only thing you write per Short) |
| `scripts/make_short.py` | Pipeline runner |
| `scripts/shorts/audio.py` | Kokoro narration, captions, music bed, SFX presets |
| `scripts/shorts/scene.py` | kf / shot / camera helpers, rule checks, TS writer |
| `src/story/currentStory.ts` | Generated story rendered by the `MotionBlocks` composition |
| `src/characters/` | Constructor: `look.ts` (presets, palettes), `clothing.ts` (textures), `Accessories.tsx` |
| `src/components/` | `R6Character.tsx`, `HairSystem.tsx`, `ShortsHUD.tsx` (captions) |
| `src/environments/` | `TownMap` + buildings / props, `interiors.tsx`, `locations.ts`, `kit.tsx` |
| `public/music/` | Background music tracks |
| `references/` | Reference Shorts (pacing, voice, structure) |
| `models/` | Kokoro v1.0 ONNX + voices |
