# Rig contract — how a character plugs into the movement system

The character owns the MODEL. The kit (`src/kit/kit.tsx`) owns the MOVEMENT.
A character takes a `pose?: Pose` and maps its fields to group pivots. No
animation math lives in the character file. This contract is the rulebook for
writing a new character or a new clip. (Ported from Claude's
character-to-remotion `references/rig-contract.md`, 2026-11-20, adapted to
this kit. V3 Pose since 2026-11-20, the maintainer approved.)

## The Pose (V3)

```ts
type V3 = [number, number, number];
interface Pose {
  y: number;            // body height offset (crouch < 0, jump > 0)
  rootPos: V3;          // extra translation of the whole body
  root: V3;             // extra rotation of the whole body (y = spin/turn)
  torso: V3;            // [lean, twist, roll]
  head: V3;             // [pitch, yaw, tilt]
  armL: V3; armR: V3;   // shoulder joints [swing, twist, spread]
  legL: V3; legR: V3;   // hip joints [swing, twist, spread]
  liftL: number; liftR: number; // foot lift, studs
  hair: number;         // secondary motion: hair / accessory bounce
  flap: number;         // wing-root angle (winged characters only)
}
```

Conventions (all in the kit header, repeated here because they are the
contract):

- 1 unit ~ 1 stud. Feet rest on y = 0. The character faces +z. Up is +y.
- **V3 joint = [x, y, z] radians.**
  - Hanging limbs (arms, legs): x = swing, **NEGATIVE = forward / up**,
    positive = backward. y = twist. z = outward spread (>0 = away from
    the body, <0 = toward the centre).
  - Upright parts (torso, head, root): x = lean / nod FORWARD (positive),
    y = turn, z = tilt / roll.
  - A raised arm is a large negative `armR[0]` (≈ −2.4). A forward kick is
    a negative `legR[0]` (−1.4 ≈ 80°).
- **Sides (ours — read this carefully):** `legL` / `armL` drive the **−x**
  limb, `legR` / `armR` the **+x** limb. Anatomically the −x limb is the
  character's own right (he faces +z), so our `legL` is really his right
  leg — the labels are swapped versus anatomy, and versus Claude. Claude's
  skill labels the +x limb L and the −x limb R, so **his `legL` is our
  `legR` and vice versa**. When porting a clip from his motion.ts, swap L/R
  on the limbs (his legL → our legR, his armL → our armR) and keep the
  numbers. The motion is identical either way; only the name differs.
- `legLength = 2.3` studs. Clips that drop the body (walk, run) use this
  length. Pass it to `walkPose`/`runPose` for a taller or shorter character.
- `pose()` builds a Pose from a partial (anything not given is the rest
  pose). `restPose()` is the neutral pose. `lerpPose` blends two poses
  (V3 joints component-wise). `layerPose` layers one pose over another on
  listed joints.

## How the fields map to the rig

| Pose field | Group | Pivot | Applied as |
|---|---|---|---|
| `root` | wrapper around the whole body | y = 0 | `rotation={root}` (y = turn) |
| `rootPos` | wrapper around the whole body | y = 0 | `position={rootPos}` |
| `y` | body group | y = 0 | `position={[0, y, 0]}` |
| `legL` / `legR` | leg groups | hip, y = 2.3 | `rotation={[leg[0], leg[1], side * leg[2]]}` |
| `liftL` / `liftR` | leg groups | hip | `position.y = 2.3 + lift` |
| `torso` | torso group | **waist, y = 2.3** | `rotation={torso}` |
| `armL` / `armR` | arm groups | shoulder, y = 4.2 | `rotation={[arm[0], arm[1], side * (0.07 + arm[2])]}` |
| `head` | head group | head centre, y = 5.17 | `rotation={head}` |
| `hair` | hair group | head | `rotation.x = hair` |
| `flap` | wing roots | y = 3.5, z = −0.72 | wing-root y-rotation |

Notes on the mapping:
- The arm's z-spread is added to a resting 0.07 outward angle and
  multiplied by `side`, so a positive spread moves the arm outward on both
  sides. The leg's z-spread is multiplied by `side` the same way (no
  resting angle).
- `torso[1]` (twist) is stored negated relative to the old scalar `twist`:
  the scalar rig applied `[lean, -twist, 0]`, so a V3 clip sets
  `torso: [lean, -twist, 0]` to produce the same motion. See the clip
  conversion note in kit.tsx.
- The torso's x (lean) is positive forward. The head's x (pitch) is
  positive down (nod forward = head tips down).

Two pivots that have bitten us before (do not move them):

- **Torso pivots at the WAIST (y 2.3), not the floor.** The lean/twist
  group sits at `[0, 2.3, 0]` with an inner wrapper at `[0, -2.3, 0]` that
  re-bases the children so no coordinates change. Pivoting at the floor
  throws the torso forward off the legs on a deep lean (the bow read as
  disconnected). Verified by the side-profile BowCheck, 2026-11-20.
- **Torso bottom ends exactly at the WAIST (y 2.3) — do not extend it down
  over the pants.** The 0.3 extension (torso `[2, 2.3, 1]` at y 3.15) was
  added with the bow fix, but it made the shirt visibly overlap the pants
  at rest — the maintainer caught it against Claude's render, where the shirt ends
  cleanly at the waist. The waist pivot above, not the extension, is what
  keeps the bow connected; the hem band (BoltBoy/WingedBoy: `[2.06, 0.24,
  1.06]` at y 2.42) covers the seam. Correct torso: `[2, 2, 1]` at y 3.3
  (hoodies) / `[1.96, 2, 1]` at y 3.3 (shirts). Verified 2026-11-20 by the
  walk still (clean waist) and BowCheck v2 (bow still connects).
- **Shoes pivot at the ANKLE (y −2.2 in the leg group), not the hip.** The
  shoe group sits at `[0, -2.2, 0]` with `rotation={[-leg[0] * 0.45, 0, 0]}`
  and the shoe boxes re-based +2.2 so nothing moves at rest. Pivoting at
  the hip makes the shoe separate from the leg on a big kick (the shoe
  rotates around the hip while the leg rotates around the hip too, but at
  different rates). Verified by the KickCheck side view, 2026-11-20.

Feet: counter-rotate the shoe by `−leg[0] * 0.45` so the foot stays flat
while the leg swings.

## Clips

A clip is a pure function `(t) => Pose`. It loops cleanly over its `cycle`
(pose at t = cycle equals pose at t = 0), except `wave`, which is a one-shot
by design (it raises, then waves; starts arm-down, ends arm-up — see
`wavePose`). Every clip's duration in `CLIPS` is a whole number of cycles.
43 clips (2026-11-20): walk, run, idle, wave, jump, dance, fly, sprint,
march, hop, skip, sidestep, sneak, bow, nod, shrug, point, cheer, salute,
look-around, think, celebrate, scared-cower, proud, punch, kick, throw,
push, pull, shake-head, clap, shy, laugh-shake, angry-stomp, cry-hunch,
confused-shrug, climb, swim, catch, high-five, hug, dig, hammer.

- `clipPose(name, t)` — the Pose for a clip at time t.
- `layerPose(base, overlay, keys)` — the overlay wins on the listed joints,
  the base supplies the rest. This is how movements combine simultaneously
  (fly body + wave arm).
- `withTurn(pose, t, duration)` — spins any pose around the vertical axis,
  one full turn per `duration` seconds (a turntable). Sets `root[1]`.
- `timelinePose(segments, t, crossfade)` — runs clips in sequence with a
  smoothstep crossfade (0.25s) at every boundary, **including the wrap**
  from the last segment back to the first, so joints never snap.
- `performanceFace` / `performanceDuration` (engine only, in
  `src/kit/expressions.tsx`) — the face lane that runs in parallel with the
  body lane in a Performance.

## RootMotion

Whole-object motion, works on anything (a character, a prop, a mascot) —
it only moves the root transform:

| kind | motion |
|---|---|
| `spin` | one full turn over `duration` |
| `bounce` | hop + squash at the bottom |
| `float` | gentle vertical sine |
| `squash` | scale squash and stretch |
| `shake` | fast sideways shake (x) |
| `pulse` | uniform scale breathe |
| `wobble` | roll side to side |
| `fall-over` | tips over to the side and drops (one-shot) |
| `pop-in` | scales up from nothing with a small overshoot |
| `slide-in` | slides in from the left (−3 studs) to centre |

`rootTransform(mode, t, duration)` returns `{yaw, y, scaleY, scaleXZ, x,
roll}`. The `RootMotion` component applies it. `shake` / `pulse` /
`wobble` were ported from Claude's update (2026-11-20); `fall-over` /
`pop-in` / `slide-in` were added 2026-11-20 (the maintainer: "Let's do them all").

## What a new character needs

- A `pose?: Pose` prop (default: `walkPose(t, ...)` or `restPose()`).
- The mapping table above, applied to its own pivots. Missing parts are
  fine — a mascot with no legs ignores `legL` / `legR`; a wingless
  character ignores `flap`.
- `root` / `rootPos` applied to a wrapper group around the whole body
  (needed for `withTurn`).
- `expression?: ExpressionName` (engine only) — the face. Default must
  reproduce the character's original face pixel-identically.

## What a new clip needs

- A pure `(t) => Pose` function. Use `pose({...})` so unspecified joints
  are the rest pose. No new joints unless the rig gains them.
- A `cycle` (seconds for one full loop) and a `duration` in `CLIPS` that is
  a whole number of cycles.
- Negative `y` kept ≤ 0.2 so rigid legs never sink through the floor.
- A loop-closure check: `node check-loops.mjs` must show max |Δ| ≈ 0
  (≤ 1e-15) for the new clip at t = duration vs t = 0. One-shots (like
  `wave`) are the exception and must be marked as such in `CLIPS` and in
  the check.

## Pants / waist rule (the maintainer, 2026-11-20)

The shirt ends exactly at the waist (y 2.3) and the pants are visible
below it — that clean waist is what the maintainer compared against Claude's
render, and the shirt must NOT extend down over the pants at rest.
But the pants box must run 0.3 UP INSIDE the torso (top y 2.6, hidden
inside the shirt), NOT end at the waist. Reason: when a leg swings, the
pants top face tilts and its front edge rises above y 2.3 — with the top
at the waist the dark top face showed over the shirt in walk / run /
sprint / march / punch / kick (the maintainer caught it in PoseLab v4). With
the top inside the torso the tilted corners stay hidden behind the
shirt. Pants are slightly narrower than the torso (0.9 wide / 0.94
deep vs torso 2 / 1) so the corners stay inside the torso's silhouette.
The visible pants length is unchanged: bottom stays at y 0.5 (0.54 for
CasualMan/ClassicNoob), shoe and ankle pivot untouched.

## Waistband rule (the maintainer, 2026-11-20 — the pants/shirt overlap, round 2)

The pants-up fix (top y 2.6 inside the torso) was NOT enough on its own:
at the steep 3/4 camera the pants top still showed over the shirt at
certain phases. A red-pants diagnostic proved it: the pants top face
tilts when a leg swings, and the torso TWIST (±0.18 in sprint) rotates
the shirt away from the pants top corner, exposing it at the waist edge.
The torso and leg rotate independently, so no pants-top position stays
hidden by geometry alone.

The fix that works at ANY camera angle: a TALLER ribbed waistband, part
of the TORSO (so it twists/leans with the shirt and stays over the seam).
The hem band is 0.45 tall (spans y 2.30-2.75) instead of 0.24, in the
dark trim colour (hoodieDark / shirtDark). It covers the pants top face
as it rises to 2.68 (sprint) and 2.79 (kick). It reads as a wide ribbed
hem / waistband, a normal garment feature — the light shirt still ends
at the waist, and at rest the waist looks the same as before. Pocket
moved up to clear it (BoltBoy 2.88→3.05, WingedBoy 2.86→3.03);
CasualMan's lowest button (2.55) dropped (4 buttons now). Combined with
the pants-up fix, the waist is clean at walk/run/sprint/march/punch/kick
even at the steep 3/4 camera (verified with zoomed stills + v7 video).

## Side-sliver rule (the maintainer, 2026-11-20 — the pants/shirt overlap, round 4)

The waistband (round 3) fixed the FRONT of the waist, but the maintainer's phone
screenshots (15 shots, video times 00:00-00:19) showed a thin dark sliver
still appearing at the TORSO'S SIDE EDGE, just above the waistband, at the
pocket level — in the march (frames 355, 370, 385), alternating sides as
the cycle progressed. The mechanism: the march lifts the leg (lift 0.45)
AND swings it (0.6), which raises the pants top corner to y ~3.0 — above
the waistband (top 2.75) and into the torso, where the torso is only 2.0
wide and the pants outer edge (0.97) sits 0.03 inside it. Any torso twist
exposes the corner at the side edge. THE FIX: narrow the pants (BoltBoy/
WingedBoy 0.9 -> 0.8 wide, CasualMan/ClassicNoob 0.88 -> 0.78; outer edge
0.97 -> 0.92) AND widen the waistband (hoodie 2.06 -> 2.2, shirt 2.0 ->
2.14; x margin 0.06 -> 0.13). Verified: march frames 340/355/370/385
clean, pants do not read as skinny, waistband reads as a normal ribbed
hem. LESSON: a stills check must cover the FULL cycle of every clip, not
just one extreme frame per clip — the sliver appeared at frames 355/370/
385, not at the 365 I had checked.

## Dance-wedge rule (the maintainer, 2026-11-21 — the pants/shirt overlap, round 5)

the maintainer on v8 (7 phone screenshots, Run/Dance/Sprint/Kick): still overlaps.
A red-pants diagnostic (84 frames, every 3rd frame across all four clips)
proved the DANCE has a real waist defect the earlier checks missed: the
dance legs roll outward (z-spread up to ~0.2, plus swing and torso twist),
which pushes the pants top corner up OVER the waistband's side edge, once
per 12-frame dance cycle (frames 222/234/246/258...), alternating sides.
Run and sprint waist seams were CLEAN in the same diagnostic (the red
showed the pants meeting the waistband cleanly). THE FIX: waistband wider
AND taller — hoodie [2.2, 0.45, 1.16] -> [2.34, 0.6, 1.24] at y 2.6
(spans 2.30-2.90), shirt [2.14, 0.45, 1.14] -> [2.28, 0.6, 1.2] — and
pants narrower again (hoodie 0.8 -> 0.74, shirt 0.78 -> 0.72; outer edge
0.92 -> 0.89). VERIFIED in PoseLab v9: contact sheets of the waist every
6 frames across walk/run/dance/sprint/march/punch/kick (77 frames) all
clean — no wedge, no sliver. NOTE on the KICK: the waist seam is clean,
but the kicking thigh still comes up IN FRONT of the shirt during a
forward kick (frames 582/612/636) — that is the leg's position from the
front 3/4 camera, not a seam defect; a side kick or a side camera would
be needed to keep the thigh off the shirt, and that is the maintainer's call.

## R6 presets use the kit Pose (the maintainer, 2026-11-21 — "make a better engine")

`R6Character` takes an optional `pose?: Pose` (V3). When given, it drives
every body joint and `anim` is ignored; `anim` is now optional (defaults
to `idle`), so all existing stories render identically. The mapping is the
same as the kit characters (BoltBoy Arm/Leg): armL/legL drive the −x limb
(the R6's right side), armR/legR the +x limb (left side).

- torso y = 3.0 + pose.y; torso rotation = pose.torso; head = pose.head
- right arm (−x): [armL[0], armL[1], −(0.07 + armL[2])]
- left arm (+x): [armR[0], armR[1], 0.07 + armR[2]]
- right leg (−x): [legL[0], legL[1], −legL[2]], group y = −1.0 + liftL
- left leg (+x): [legR[0], legR[1], legR[2]], group y = −1.0 + liftR
- root: pose.rootPos added to position, pose.root added to rotation
- The R6 face stays on the R6 expression system (`expression` prop). The
  kit's 27 expressions are NOT wired to R6 faces.
- The R6 Leg counter-rotates the shoe at the ankle (pivot y −1.68,
  −hipX * 0.45, boxes re-based +1.68) so the foot stays flatter on high
  kicks, same as the kit characters. `hipX` is passed as a Leg prop.
- The R6 rig is shorter than the kit rig (~5.9 vs ~7.1 studs), so R6
  framings sit lower (lookAt y ~2.8, camera y ~4 instead of 4.2/5).
- `R6KitCheck` composition (inputProps preset + clip + side) verifies any
  preset doing any kit clip. Story-pipeline wiring (a `clip` field in
  story files) is NOT done — `MotionBlocksComposition` still drives actors
  by `anim` only.

## Circle showcase (the maintainer, 2026-11-21)

`CircleShowcase` (900f/30s, 1280x720): all 27 characters (4 kit +
23 R6 presets) in a circle (R 17, ~4 studs apart), camera orbits once at
20 studs from the featured character, looking at the circle point in
front of it (smooth, no jump between characters). Each character faces
the camera (rotationY tracks it) and waves as the camera passes
(lerpPose idle→wave, wave window ±0.45 rad). `wavePose` is a one-shot
that ends arm-UP (ramps over 0.5s, then wobbles) — offset wave time by
+0.5s so the first character is already waving at frame 0. Framing
lesson: camera at radius 24 (7 studs from the nearest character) filled
the frame with faces — use 20 studs from the featured character instead.
WingedBoy's wings span wide and overlap neighbours when he is near the
camera; that is his design, not a bug. The Astronaut is NOT in the
circle — he lives in the separate Mars project, not the engine kit.

## Kit characters in story Shorts (the maintainer, 2026-11-21 — "Wire in BlockBoy first")

The story pipeline (`MotionBlocksComposition`) renders R6 presets by
default, but a cast entry can now point at a kit character instead:
`{"kit": "boltboy"}`. The composition checks `kitForActor(charId, cast)`
first; when it returns a kit id it renders that kit component
(`BoltBoy.tsx`) with the canonical look and the V3 clip system, and
`anim` is ignored for the R6 path. The story's `anim` (AnimationMode)
is mapped to a kit clip by `STORY_ANIM_TO_CLIP` and evaluated with
`clipPose(clip, frame / fps)` — global frame time, so cyclic clips
(walk/idle/dance) stay continuous across keyframes; one-shots (wave)
end arm-up, which reads as waving for the whole keyframe. The story's
`expression` (ExpressionId) passes straight through — all 9 R6
expressions are valid kit ExpressionNames. `prop` is NOT supported on
kit characters yet (the hero in `bolt_boy_first` holds none). The three
AnimationModes with no kit clip (sleep, knocked, panting) fall back to
idle — the character stays standing, a known gap, not a crash.
`scale` from the cast entry (`{"kit": "boltboy", "scale": 1}`) sizes the
kit character; at scale 1 BoltBoy is ~9% taller than the R6 cast, which
reads as a natural hero height. `buildLook` returns the fallback preset
for a kit marker (a kit character has no R6 look). Verified by
`KitStoryCheck` (test composition, 90f portrait): kit hero walks and
waves beside an R6 friend, both branches render, tsc clean.
`bolt_boy_first.py` casts its hero as `{"kit": "boltboy"}`. Do NOT run
`make_short.py` on it until sky_blue has shipped (currentStory.ts is
still sky_blue) — and back up
currentStory.ts first.

All four kit characters can now lead a story (the maintainer, 2026-11-21 —
"You need to make all characters available to lead a story"):
`KitCharacterId` is `'boltboy' | 'casualman' | 'wingedboy' |
'classicnoob'`; cast any of them as `{"kit": "<id>"}`. The composition
picks the component by kit id (BoltBoy / CasualMan / WingedBoy /
ClassicNoob) and renders it with the same pose/expression/scale props.
`ShortsHUD` bubble anchors use head height 6.6 for all four kit
characters (they are all ~7 studs tall; R6 stays 5.6). Story
`expression` must be one of the 9 story ExpressionIds (smile, grin,
shocked, sleeping, panic, angry, cool, laugh, deadpan) — a kit-only
expression such as WingedBoy's default 'smirk' is NOT a valid story
ExpressionId and fails tsc (use 'cool' for WingedBoy in stories).
Verified by `stories/kit_heroes_test.py` (test story, 510f): all four
walk in a row across the crossroads and wave, rule checks OK, tsc
clean, stills `kitheroes-f200.png` (walk) + `kitheroes-f400.png`
(wave). Note: in portrait 1080x1920 a 4-person row at 6-stud spacing
spans 18 studs, wider than a default wide shot (dist 20) shows — use
dist ~35 for a 4-wide row. The Astronaut is NOT in the engine kit
(he lives in the Mars project) and cannot lead a story until his rig
is ported to V3 and his component is brought into the engine.

## Chat bubbles / dialogue (the maintainer, 2026-11-21 — "is it possible to use the engine to generate animation but with a dialogue between characters?")

Yes. A story keyframe takes `bubble="..."` (`kf(..., bubble="Hi!")`), which
sets `CharacterKeyframe.chatBubble`. The field existed in the schema and in
`scene.py` but nothing ever drew it — the bubble data flowed into the
character state and was silently ignored. As of 2026-11-21 `ShortsHUD`
renders it: a white rounded 2D speech bubble with a tail, positioned above
the speaking character's head, with a pop-in spring.

How it works: `ShortsHUD` evaluates each character's keyframes at the
current frame (shared `src/story/keyframes.ts`), projects the head-top
anchor through the same camera the 3D scene uses (shared
`src/story/camera.ts` — `cameraStateForFrame` + `projectToScreen`, one
source of truth, also used by the refactored `CameraRig`), and draws the
bubble at that screen position. Head heights: kit BoltBoy 6.6 studs, R6
5.6, plus a 0.6-stud lift. The bubble is clamped to stay on screen; its
tail is offset horizontally so it keeps pointing at the speaker even when
the bubble was pulled inward. The bubble is HIDDEN when the speaker's head
is off-screen (e.g. the camera is in a close-up on the other character) —
showing it anyway would put a stranger's line over the wrong face. So a
dialogue story should cut to the speaker when they talk; `cover()` cycling
to a close-up on the listener will hide that line's bubble (the caption /
narration still carries it).

Limits (still true): the pipeline has ONE narrator voice (`af_heart`) for
the whole story — no per-character voices, and no lip sync (expressions
change, the mouth does not move with speech). Dialogue is bubbles +
expressions, not spoken character voices. The director skill's "No other
HUD: no leaderboards, chat bubbles or title bars" rule is overridden by
the maintainer's explicit bubble request — bubbles are now a supported HUD element.

Test: `stories/dialogue_test.py` (Bolt Boy + kid_girl, 4 bubble lines,
back-and-forth). Verified by stills at frames 195/285/375/480
(`~/workspace/videos/noob-compare/dialogue/`): the two close-ups read
perfectly (bubble centred above the speaker, tail on the head); the medium
2-shot reads well (tail points at the speaker); the off-screen speaker's
bubble is correctly hidden. The test was built with fake no-TTS timings
(Kokoro `kokoro_onnx` is not installed on this VM, so `make_short.py
--stills` fails at the TTS step) — see `/tmp/build_dialogue_test.py`.
`currentStory.ts` was restored to sky_blue after the test.

### Position-anchored bubbles — a voice from an invisible / off-screen character (2026-11-21, Invisible Day "HELP!")

A normal bubble is anchored to the speaker's head, and hidden when the
head is off-screen. That breaks for a character who is invisible (parked
OFF at `[0, -80, 0]`): their head is never on screen, so the bubble would
never show. Fix: `kf(..., bubble="HELP!", bubble_anchor=[x, y, z])` sets
`CharacterKeyframe.bubbleAnchor` — a world position the bubble floats
above instead of the head. `ShortsHUD` treats the anchor as the voice's
origin: the bubble sits 0.6 studs above the anchor, the tail points down
at it, and the off-screen hide applies to the anchor itself. Set the
anchor where the voice comes from — head height above the empty spot for
a standing speaker, or lower (just above a ground marker such as the
ball) so the bubble hovers in clear air instead of over a tree canopy.
Invisible Day anchors "HELP!" at `[-2.5, 3.4, 0.5]`, just above the
orange ball at `[-2.5, 1.0, 0.5]`. The bubble shows exactly while the
keyframe carrying it is active (stepwise, like `chatBubble`) — put a plain
keyframe at the next beat to clear it. Pair it with a visible marker at
the same spot (Invisible Day drifts the orange ball fx to the anchor's
feet) so the viewer connects the floating words to a place. A close-up
on another character still hides it, so the camera during an anchored
bubble must frame the anchor — check the stills.
