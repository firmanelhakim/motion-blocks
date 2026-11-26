import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { RobloxShortStory, CharacterId, CharacterKeyframe } from '../types/schema';
import { evaluateCharacterKeyframes } from '../story/keyframes';
import { CameraState, cameraStateForFrame, projectToScreen } from '../story/camera';
import { kitForActor, scaleForActor } from '../characters/look';

// Head-top height in studs, for the bubble anchor above the speaker.
// Kit characters (BoltBoy) are ~7 studs; R6 presets are ~5.9. These are the
// head-top heights (measured from the renders), not the total heights.
const HEAD_HEIGHT: Record<string, number> = { boltboy: 6.6, casualman: 6.6, wingedboy: 6.6, classicnoob: 6.6 };
const DEFAULT_HEAD_HEIGHT = 5.6;
const BUBBLE_LIFT = 0.6; // studs above the head top
const MAX_BUBBLE_WIDTH = 520;
const MIN_BUBBLE_TOP = 180; // px — never let the bubble run off the top
const OFFSCREEN_MARGIN = 80; // px — hide the bubble when the head is this far off-screen

// ---- Narration caption width clamp ---------------------------------------
// The caption is one centred line at fontSize 76 / weight 900 inside a
// left:60/right:60 band. Long two-word chunks can measure wider than the
// band, so the text runs off both frame edges (seen on "ground, her").
// Measure each chunk with the same font stack in an off-screen canvas and
// shrink the font until the ink (fill + 15px text stroke) fits the band,
// with headroom for the pop-in spring's ~1.2% overshoot. Applies to every
// narration caption; position, colour and chunk timing are untouched.
const CAPTION_BASE_FONT_SIZE = 76;
const CAPTION_STROKE_PX = 15; // WebkitTextStroke width: ~half extends each side
const CAPTION_SIDE_MARGIN = 60; // matches the caption band's left/right: 60
const CAPTION_POP_OVERSHOOT = 1.02; // spring scale peaks ~1.012x

// ---- Narration caption face avoidance ------------------------------------
// The caption used to sit at a fixed 68% of frame height, which lands
// across faces in close-ups (round-0 fails: rainbow "sun has" on the
// hero's mouth/chin, no_internet "cables to a" on Sam's forehead,
// robot_homework "the homework?" on Robo's face plate, internet_sea
// across the hero's forehead in all four face close-ups). The slot is
// now decided per SHOT from the visible faces, projected with the same
// camera the 3D scene uses:
//   * lowest visible chin across the shot -> caption top just below it
//     (the chest/torso anchor; in a normal close-up this lands the
//     caption on the chest, clear of the face);
//   * if the chin is too low for the caption to fit underneath (extreme
//     close-up, chin at/below the bottom edge) -> caption goes above the
//     highest hairline instead;
//   * if no face is on screen in a close-up -> caption drops to the lower
//     band, which also clears non-character faces (Robo's face plate is
//     an fx shape, not a character, so no chin is ever computed for it).
// The slot is sampled across the whole active shot (not per frame), so
// the caption never jumps mid-shot while the camera dollies in. When no
// face overlaps the default band — every wide/medium — the caption stays
// at exactly 68%, so the established wide-shot look is untouched.
const CAPTION_DEFAULT_TOP_FRAC = 0.68;
const CAPTION_GAP_FRAC = 0.02; // gap below a chin / above a hairline, as a fraction of frame height
const CAPTION_BOTTOM_MARGIN_PX = 12;
const CAPTION_TOP_MARGIN_PX = 12;
// The chin model is only accurate to ~3% of frame height (it over-reads
// in wides — rainbow f30 models a 68-70% chin where the true chin is
// ~65% — and under-reads in the tightest close-ups). So the caption only
// moves when the modelled chin is unambiguously inside the default band;
// a modelled chin merely grazing the band leaves the caption exactly
// where it was, which is what keeps wides and mediums pixel-identical.
const CAPTION_OVERLAP_TOL_FRAC = 0.03;
// A close-up is a short camera distance (the failing CUs were dist 5.8-13).
const CLOSE_UP_DIST = 14;
// Lower band for close-ups with no face on screen (prop close-ups).
const CLOSE_UP_NO_FACE_TOP_FRAC = 0.8;
// Head height in studs from the head top down to the chin (jaw bottom).
// Kit heads: box 1.48 + hair above the box; R6 heads: lathe 1.15 + hair.
// Deliberately generous: the true chin sits a touch lower than the model
// in the tightest CUs (projected vs measured on the v1 frames: rainbow
// 71.3% vs ~71%, no_internet 88.5% vs ~92%), and a caption a little low
// on the chest is fine while a caption on a chin is a fail.
const CHIN_DROP_KIT = 2.6;
const CHIN_DROP_R6 = 1.6;
// Characters parked off-screen sit at y <= -50 (OFF = [0, -80, 0]); they
// have no visible face. Same threshold as RobloxShortComposition.
const OFFSCREEN_Y = -50;
// Frames sampled across the active shot when deciding the caption slot.
const CAPTION_SHOT_SAMPLES = 5;

function captionFontSize(text: string, maxWidth: number): number {
  if (typeof document === 'undefined') return CAPTION_BASE_FONT_SIZE;
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  if (!ctx) return CAPTION_BASE_FONT_SIZE;
  ctx.font = `900 ${CAPTION_BASE_FONT_SIZE}px Inter, 'Segoe UI', 'Arial Black', sans-serif`;
  // measureText ignores CSS letter-spacing, so apply the -1.5px per gap
  // between characters arithmetically.
  const spaced = ctx.measureText(text).width + (text.length - 1) * -1.5;
  const ink = spaced + CAPTION_STROKE_PX;
  const limit = maxWidth / CAPTION_POP_OVERSHOOT;
  if (ink <= limit) return CAPTION_BASE_FONT_SIZE;
  return Math.max(24, Math.floor((CAPTION_BASE_FONT_SIZE * limit) / ink));
}

/** Frame at which the bubble currently shown at `frame` first appeared. */
function bubbleStartFrame(keyframes: CharacterKeyframe[], frame: number): number {
  let start = keyframes[0].frame;
  for (const k of keyframes) {
    if (k.frame <= frame && k.chatBubble) start = k.frame;
    if (k.frame > frame) break;
  }
  return start;
}

/**
 * Screen-space face band of one character at one frame: the hairline
 * (head top) and the chin (jaw bottom), in pixels from the top of the
 * frame. Returns null when the character has no visible face — parked
 * off-screen, behind the camera, or with its head out of frame. The
 * chin is the head top minus the head's height (kit 2.6 / R6 1.6 studs,
 * deliberately generous — see the constants above), times the actor's
 * scale, projected with the same camera as the 3D scene.
 */
function faceBandAtFrame(
  charId: CharacterId,
  keyframes: CharacterKeyframe[],
  frame: number,
  cam: CameraState,
  story: RobloxShortStory,
  width: number,
  height: number
): { headTopY: number; chinY: number } | null {
  const state = evaluateCharacterKeyframes(keyframes, frame);
  if (state.position[1] <= OFFSCREEN_Y) return null;
  const kitId = kitForActor(charId, story.cast);
  const scale = scaleForActor(charId, story.cast);
  const headH = ((kitId && HEAD_HEIGHT[kitId]) || DEFAULT_HEAD_HEIGHT) * scale;
  const chinDrop = (kitId ? CHIN_DROP_KIT : CHIN_DROP_R6) * scale;
  const headPos: [number, number, number] = [
    state.position[0],
    state.position[1] + headH,
    state.position[2],
  ];
  const chinPos: [number, number, number] = [
    state.position[0],
    state.position[1] + headH - chinDrop,
    state.position[2],
  ];
  const headPt = projectToScreen(headPos, cam, width, height);
  const chinPt = projectToScreen(chinPos, cam, width, height);
  if (!headPt && !chinPt) return null; // behind the camera
  const onScreen = (pt: { x: number; y: number } | null) =>
    !!pt &&
    pt.x >= -OFFSCREEN_MARGIN &&
    pt.x <= width + OFFSCREEN_MARGIN &&
    pt.y >= -OFFSCREEN_MARGIN &&
    pt.y <= height + OFFSCREEN_MARGIN;
  if (!onScreen(headPt) && !onScreen(chinPt)) return null;
  // One end may be cut by the frame edge; fall back to the visible end.
  const topY = headPt ? headPt.y : chinPt!.y;
  const bottomY = chinPt ? chinPt.y : headPt!.y;
  return { headTopY: Math.min(topY, bottomY), chinY: Math.max(topY, bottomY) };
}

/**
 * Top edge (px) of the narration caption band for this frame. Decided
 * per active shot (sampled across the shot, so the slot is stable while
 * the camera dollies). See the constants above for the rules. Returns the
 * default 68% band whenever no face overlaps it, so wides and mediums
 * keep their current caption position and look exactly.
 *
 * Corner case: in an extreme close-up the caption may go above the
 * hairline, where a chat bubble could also sit — a caption over a bubble
 * is accepted there (bubbles live in dialogue scenes, extreme close-ups
 * with a top-slot caption are rarer, and a face overlap is the fail).
 */
function captionTopPx(
  story: RobloxShortStory,
  currentScene: RobloxShortStory['scenes'][number] | undefined,
  frame: number,
  cam: CameraState | null,
  width: number,
  height: number,
  captionHeightPx: number
): number {
  const defaultTop = CAPTION_DEFAULT_TOP_FRAC * height;
  const gap = CAPTION_GAP_FRAC * height;
  const maxTop = height - captionHeightPx - CAPTION_BOTTOM_MARGIN_PX;
  if (!currentScene || !cam) return defaultTop;

  const shots = currentScene.cameraShots;
  if (!shots || shots.length === 0) return defaultTop;
  const activeShot =
    shots.find((s) => frame >= s.startFrame && frame <= s.endFrame) ||
    shots[shots.length - 1];

  let anyFace = false;
  let lowestChin = -Infinity;
  let highestTop = Infinity;
  const n: number = CAPTION_SHOT_SAMPLES;
  for (let i = 0; i < n; i++) {
    const sampleFrame =
      n === 1
        ? activeShot.startFrame
        : Math.round(
            activeShot.startFrame +
              ((activeShot.endFrame - activeShot.startFrame) * i) / (n - 1)
          );
    const sampleCam = cameraStateForFrame(shots, sampleFrame);
    for (const [charId, keyframes] of Object.entries(currentScene.characters) as [
      CharacterId,
      CharacterKeyframe[]
    ][]) {
      if (!keyframes || keyframes.length === 0) continue;
      const band = faceBandAtFrame(
        charId,
        keyframes,
        sampleFrame,
        sampleCam,
        story,
        width,
        height
      );
      if (!band) continue;
      anyFace = true;
      lowestChin = Math.max(lowestChin, band.chinY);
      highestTop = Math.min(highestTop, band.headTopY);
    }
  }

  if (!anyFace) {
    // No visible face: in a close-up drop to the lower band (covers
    // non-character faces such as Robo's face plate and prop close-ups);
    // otherwise the default band is untouched.
    const dist = Math.hypot(
      cam.position[0] - cam.target[0],
      cam.position[1] - cam.target[1],
      cam.position[2] - cam.target[2]
    );
    if (dist <= CLOSE_UP_DIST) {
      return Math.min(CLOSE_UP_NO_FACE_TOP_FRAC * height, maxTop);
    }
    return defaultTop;
  }

  // Fits below the lowest chin? Then the caption sits on the chest — but
  // only when the chin is unambiguously inside the default band (see the
  // tolerance above); a chin merely grazing the band leaves the caption
  // exactly at 68%, which is what keeps wides/mediums pixel-identical.
  if (lowestChin <= defaultTop + CAPTION_OVERLAP_TOL_FRAC * height) {
    return defaultTop;
  }
  if (lowestChin + gap + captionHeightPx <= height - CAPTION_BOTTOM_MARGIN_PX) {
    return Math.min(Math.max(defaultTop, lowestChin + gap), maxTop);
  }
  // Chin too low for the caption to fit underneath (extreme close-up):
  // put it above the highest hairline.
  const aboveTop = highestTop - gap - captionHeightPx;
  return Math.max(CAPTION_TOP_MARGIN_PX, Math.min(aboveTop, maxTop));
}

export const ShortsHUD: React.FC<{
  story: RobloxShortStory;
  currentScene?: RobloxShortStory['scenes'][number];
  cam?: CameraState | null;
  actorStates?: Partial<Record<CharacterId, CharacterKeyframe>>;
}> = ({ story, currentScene: sceneProp, cam: camProp, actorStates }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // A story with no captions (missing/empty `captions`) simply shows no
  // caption — the HUD is an overlay, so a missing narration track is not
  // fatal here. (Empty `scenes`/`cameraShots` fail loudly upstream in
  // RobloxShortComposition / cameraStateForFrame instead.)
  const currentCaption = (story.captions ?? []).find(
    (c) => frame >= c.startFrame && frame <= c.endFrame
  );

  // Fast pop-in spring for word-by-word / short-phrase subtitle (matching reference shorts)
  const captionLocalFrame = currentCaption ? Math.max(0, frame - currentCaption.startFrame) : 0;
  const pop = spring({
    frame: captionLocalFrame,
    fps,
    config: { damping: 14, stiffness: 280, mass: 0.45 },
  });

  const scale = interpolate(pop, [0, 1], [0.86, 1.0], {
    // Clamp: the spring can peak above 1, and without this the caption
    // would scale past 1.0 and re-overflow the band the font shrink
    // was computed for (cleanup 2026-11-26).
    extrapolateRight: 'clamp',
  });

  // Clamp the caption font so over-wide chunks fit the band (see above).
  const captionMaxWidth = width - CAPTION_SIDE_MARGIN * 2;
  const captionFontSizePx = React.useMemo(
    () =>
      currentCaption
        ? captionFontSize(currentCaption.text, captionMaxWidth)
        : CAPTION_BASE_FONT_SIZE,
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [currentCaption ? currentCaption.text : '', captionMaxWidth]
  );

  // ---- Chat bubbles -------------------------------------------------------
  // The story's `bubble` field (CharacterKeyframe.chatBubble) is carried
  // through the pipeline into each character's state, but nothing drew it
  // until now. Here we project the speaker's head onto the screen with the
  // same camera the 3D scene uses (src/story/camera.ts) and draw a 2D
  // speech bubble above it, so a back-and-forth reads as dialogue.
  const currentScene =
    sceneProp ??
    story.scenes.find((s) => frame >= s.startFrame && frame < s.endFrame) ??
    story.scenes[story.scenes.length - 1];

  const cam = camProp !== undefined ? camProp : (currentScene ? cameraStateForFrame(currentScene.cameraShots, frame) : null);

  const bubbles: { key: string; x: number; y: number; text: string; popScale: number; tailOffsetX: number }[] = [];
  if (currentScene && cam) {
    for (const [charId, keyframes] of Object.entries(currentScene.characters) as [
      CharacterId,
      CharacterKeyframe[]
    ][]) {
      if (!keyframes || keyframes.length === 0) continue;
      const state = actorStates?.[charId] ?? evaluateCharacterKeyframes(keyframes, frame);
      if (!state.chatBubble) continue;
      // Position-anchored bubble (bubbleAnchor): the voice comes from a
      // fixed world spot, not from a visible head — e.g. an invisible
      // character parked OFF. The anchor IS the voice's origin (head
      // height above the empty spot): the bubble floats above it, the tail
      // points at it, and the off-screen hide applies to the anchor
      // itself, not to the (off-screen) speaker. Without an anchor, the
      // bubble sits above the speaker's head as before.
      const anchored = state.bubbleAnchor;
      const kitId = kitForActor(charId, story.cast);
      const headH = anchored
        ? 0
        : ((kitId && HEAD_HEIGHT[kitId]) || DEFAULT_HEAD_HEIGHT) *
          scaleForActor(charId, story.cast);
      const headPos: [number, number, number] = anchored
        ? [anchored[0], anchored[1], anchored[2]]
        : [state.position[0], state.position[1] + headH, state.position[2]];
      // Hide the bubble when the speaker is not on screen (e.g. the camera
      // is in a close-up on the other character). Showing it anyway would
      // put a stranger's line over the wrong face, so we drop it instead of
      // clamping it into view.
      const headPt = projectToScreen(headPos, cam, width, height);
      if (
        !headPt ||
        headPt.x < -OFFSCREEN_MARGIN ||
        headPt.x > width + OFFSCREEN_MARGIN ||
        headPt.y < -OFFSCREEN_MARGIN ||
        headPt.y > height + OFFSCREEN_MARGIN
      ) {
        continue;
      }
      const anchor: [number, number, number] = [
        headPos[0],
        headPos[1] + BUBBLE_LIFT,
        headPos[2],
      ];
      const pt = projectToScreen(anchor, cam, width, height);
      if (!pt) continue; // behind the camera
      // Clamp so the bubble stays on screen. The tail is offset to keep
      // pointing at the speaker's head even when the bubble is pulled inward.
      const x = Math.max(MAX_BUBBLE_WIDTH / 2 + 12, Math.min(width - MAX_BUBBLE_WIDTH / 2 - 12, pt.x));
      const y = Math.max(MIN_BUBBLE_TOP, pt.y);
      const tailOffsetX = Math.max(
        -(MAX_BUBBLE_WIDTH / 2 - 40),
        Math.min(MAX_BUBBLE_WIDTH / 2 - 40, headPt.x - x)
      );
      const localFrame = Math.max(0, frame - bubbleStartFrame(keyframes, frame));
      const bPop = spring({
        frame: localFrame,
        fps,
        config: { damping: 14, stiffness: 280, mass: 0.45 },
      });
      bubbles.push({
        key: String(charId),
        x,
        y,
        text: state.chatBubble,
        popScale: interpolate(bPop, [0, 1], [0.8, 1.0], {
          extrapolateRight: 'clamp', // see caption scale above
        }),
        tailOffsetX,
      });
    }
  }

  // ---- Narration caption slot -------------------------------------------
  // Face-avoiding top edge (per active shot; see captionTopPx). Single
  // line: fontSize * lineHeight + the div's vertical padding.
  const captionHeightPx = captionFontSizePx * 1.15 + 16;
  const captionTop = currentCaption
    ? captionTopPx(story, currentScene, frame, cam, width, height, captionHeightPx)
    : CAPTION_DEFAULT_TOP_FRAC * height;

  return (
    <AbsoluteFill
      style={{
        pointerEvents: 'none',
        fontFamily: "'Inter', 'Segoe UI', 'Arial Black', sans-serif",
      }}
    >
      {bubbles.map((b) => (
        <div
          key={b.key}
          style={{
            position: 'absolute',
            left: b.x,
            top: b.y,
            transform: `translate(-50%, -100%) scale(${b.popScale})`,
            transformOrigin: '50% 100%',
            maxWidth: MAX_BUBBLE_WIDTH,
          }}
        >
          {/* tail — a white diamond whose top half hides behind the bubble.
              Offset so it keeps pointing at the speaker's head even when the
              bubble itself was pulled inward to stay on screen. */}
          <div
            style={{
              position: 'absolute',
              bottom: -11,
              left: `calc(50% + ${b.tailOffsetX}px)`,
              width: 26,
              height: 26,
              background: '#FFFFFF',
              transform: 'translateX(-50%) rotate(45deg)',
              zIndex: 0,
            }}
          />
          <div
            style={{
              position: 'relative',
              zIndex: 1,
              background: '#FFFFFF',
              color: '#111827',
              fontSize: 40,
              fontWeight: 800,
              lineHeight: 1.3,
              letterSpacing: '-0.5px',
              textAlign: 'center',
              borderRadius: 28,
              padding: '18px 28px',
              boxShadow: '0 10px 28px rgba(0, 0, 0, 0.4)',
            }}
          >
            {b.text}
          </div>
        </div>
      ))}
      {currentCaption && (
        <div
          style={{
            position: 'absolute',
            left: 60,
            right: 60,
            top: captionTop,
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            transform: `scale(${scale})`,
          }}
        >
          <div
            style={{
              color: '#FFFFFF',
              fontSize: captionFontSizePx,
              fontWeight: 900,
              textAlign: 'center',
              lineHeight: 1.15,
              letterSpacing: '-1.5px',
              WebkitTextStroke: '15px #000000',
              paintOrder: 'stroke fill',
              textShadow: '0 8px 24px rgba(0, 0, 0, 0.85)',
              padding: '8px 16px',
            }}
          >
            {currentCaption.text}
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};
