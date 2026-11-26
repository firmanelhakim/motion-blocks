/**
 * kit.tsx — shared building blocks for procedural 3D characters in the
 * engine (@remotion/three). Everything is a pure function of props/time so
 * each frame renders deterministically.
 * Conventions: 1 unit ~ 1 stud, feet on y = 0, character faces +z, up is +y.
 *
 * This is the engine's copy of the casualman project's kit.tsx (the
 * character-to-remotion kit from Claude's work with the maintainer). Keep the Pose /
 * clip / RootMotion / timeline logic in sync between the two. Two deliberate
 * engine divergences, both for the engine's house style:
 *  - RBox meshes set castShadow + receiveShadow, so characters cast the
 *    engine's ground shadow (R6Character does the same).
 *  - Stage takes an optional `shadows` prop that adds the shadow-casting
 *    light and the shadow-catcher ground plane.
 *
 * V3 POSE (2026-11-20, the maintainer approved): every joint is a V3
 * [x, y, z] — swing, twist, spread — ported from Claude's
 * character-to-remotion update. The old Pose was 14 scalars (one x-rotation
 * per limb); V3 adds a y-twist and a z-spread to every limb, plus a full
 * root and torso. What this unlocks: arms that spread outward on a wave,
 * a shrug that actually lifts the shoulders out, a clap whose hands meet,
 * a torso that can roll. See RIG_CONTRACT.md for the mapping.
 * Behaviour-preserving: every clip that existed before V3 produces the
 * same visual motion — the x-swings, the signs, and the side mapping are
 * unchanged. Only the z-spreads are new, and only where noted.
 */
import React, {useEffect, useLayoutEffect, useMemo} from 'react';
import * as THREE from 'three';
import {RoundedBoxGeometry} from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';
import {AbsoluteFill, useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';

export type V3 = [number, number, number];

// Module-level pools shared across all kit characters & environments so
// identical limbs/boxes reuse GPU vertex buffers and shader materials instead
// of re-allocating and leaking them on every mount/scene cut.
// (Ported from Gemini Neon 2026-11-22, with Neon's segments 3→2 cut
// reverted: the default here stays 3, as before.)
const rboxGeoPool = new Map<string, RoundedBoxGeometry>();
const rboxMatPool = new Map<string, THREE.MeshStandardMaterial>();

export function getRoundedBoxGeometry(
  w: number,
  h: number,
  d: number,
  segments = 3,
  radius = 0.08,
): RoundedBoxGeometry {
  const key = `${w}|${h}|${d}|${segments}|${radius}`;
  let geo = rboxGeoPool.get(key);
  if (!geo) {
    geo = new RoundedBoxGeometry(w, h, d, segments, radius);
    rboxGeoPool.set(key, geo);
  }
  return geo;
}

function getPooledRBoxMaterial(
  color: string,
  rough: number,
  metal: number,
  transparent: boolean,
  opacity: number,
  emissive: string,
  emissiveIntensity: number,
  doubleSide: boolean,
): THREE.MeshStandardMaterial {
  const key = `${color}|${rough}|${metal}|${transparent ? 1 : 0}|${opacity}|${emissive}|${emissiveIntensity}|${doubleSide ? 1 : 0}`;
  let mat = rboxMatPool.get(key);
  if (!mat) {
    mat = new THREE.MeshStandardMaterial({
      color,
      roughness: rough,
      metalness: metal,
      transparent,
      opacity,
      emissive,
      emissiveIntensity,
      side: doubleSide ? THREE.DoubleSide : THREE.FrontSide,
    });
    rboxMatPool.set(key, mat);
  }
  return mat;
}

/** Rounded box: the workhorse for torsos, limbs, shoes, hair chunks.
 * Extended 2026-11-22 for the new-asset ports: the source zips'
 * RBox carries map / bumpMap / transparent / opacity / emissive / metal /
 * doubleSide / castShadow, and the ported assets use them (ice + sand
 * textures, brain glow, blue-sun emissive, reflection layer). All new props
 * are optional; defaults preserve the old behaviour exactly. */
export const RBox: React.FC<{size: V3; color: string; position?: V3; rotation?: V3; radius?: number; segments?: number; rough?: number; map?: THREE.Texture; bumpMap?: THREE.Texture; bumpScale?: number; transparent?: boolean; opacity?: number; emissive?: string; emissiveIntensity?: number; metal?: number; doubleSide?: boolean; castShadow?: boolean; receiveShadow?: boolean; children?: React.ReactNode}> = React.memo(({size, color, position = [0, 0, 0] as V3, rotation = [0, 0, 0] as V3, radius = 0.08, segments = 3, rough = 0.7, map, bumpMap, bumpScale = 1, transparent = false, opacity = 1, emissive = '#000000', emissiveIntensity = 0, metal = 0, doubleSide = false, castShadow = true, receiveShadow = true, children}) => {
  const geo = getRoundedBoxGeometry(size[0], size[1], size[2], segments, radius);
  const sharedMat = !map && !bumpMap
    ? getPooledRBoxMaterial(color, rough, metal, transparent, opacity, emissive, emissiveIntensity, doubleSide)
    : undefined;
  if (sharedMat) {
    return <mesh geometry={geo} material={sharedMat} position={position} rotation={rotation} castShadow={castShadow} receiveShadow={receiveShadow}>{children}</mesh>;
  }
  return <mesh geometry={geo} position={position} rotation={rotation} castShadow={castShadow} receiveShadow={receiveShadow}><meshStandardMaterial color={color} roughness={rough} metalness={metal} map={map} bumpMap={bumpMap} bumpScale={bumpScale} transparent={transparent} opacity={opacity} emissive={emissive} emissiveIntensity={emissiveIntensity} side={doubleSide ? THREE.DoubleSide : THREE.FrontSide} />{children}</mesh>;
});

/** Draw on a 2D canvas and use it as a texture (faces, logos, stripes). Put the result on a <planeGeometry>.
 * `repeat` (2026-11-22, new-asset ports): tiles the texture like the source
 * zips' kit — ice street [1,6], volcano [3,3], underwater sand [2,2]. */
export const useCanvasTexture = (draw: (g: CanvasRenderingContext2D, size: number) => void, size = 512, repeat?: [number, number]) => {
  const tex = useMemo(() => {
    const c = document.createElement('canvas'); c.width = c.height = size;
    const g = c.getContext('2d')!; g.clearRect(0, 0, size, size); g.lineCap = 'round';
    draw(g, size);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    if (repeat) { t.wrapS = THREE.RepeatWrapping; t.wrapT = THREE.RepeatWrapping; t.repeat.set(repeat[0], repeat[1]); }
    t.needsUpdate = true;
    return t;
  }, []);
  // Ported from Neon: dispose the texture on unmount instead of leaking it.
  // (Neon's anisotropy 8→2 cut reverted — stays 8, as before.)
  useEffect(() => () => { tex.dispose(); }, [tex]);
  return tex;
};

// ---------------------------------------------------------------------------
// Pose contract + clip library (V3)
// ---------------------------------------------------------------------------
/**
 * A Pose is the complete set of joint values a humanoid character applies
 * in one frame. Every clip is a pure function (t) => Pose, so any animation
 * works on any character that applies a Pose — the character file never
 * changes when a clip is added. Units: rotations in radians, lifts in studs.
 *
 * V3 joint = [x, y, z] radians (Claude's convention, see
 * references/rig-contract.md in his skill):
 *  - Hanging limbs (arms, legs): x = swing, NEGATIVE = forward / up,
 *    positive = backward. y = twist. z = outward spread (>0 = away from
 *    the body, <0 = toward the centre).
 *  - Upright parts (torso, head, root): x = lean / nod FORWARD (positive),
 *    y = turn, z = tilt / roll.
 *  - `y` = body height offset (crouch < 0, jump > 0).
 *  - `hair` = secondary motion (hair / accessory bounce, x-rotation).
 *  - `flap` = wing-root angle (WingedBoy only; the rest ignore it).
 *
 * SIDES (ours, unchanged from the scalar Pose — do NOT mix with Claude's
 * labels): `legL`/`armL` drive the -x limb, `legR`/`armR` the +x limb.
 * Claude's skill labels the +x limb L and the -x limb R, so his `legL`
 * is our `legR` and vice versa. The rig applies the same limb to the same
 * side either way; only the NAME differs. When porting a clip from his
 * motion.ts, swap L/R on the limbs (his legL → our legR, his armL → our
 * armR) and keep the numbers, OR keep his numbers and accept the phase
 * flips a half-cycle apart. This file keeps OUR labels and OUR signs, so
 * every pre-V3 clip looks identical.
 */
export interface Pose {
  y: number;            // body height offset (crouch < 0, jump > 0)
  rootPos: V3;          // extra translation of the whole body
  root: V3;             // extra rotation of the whole body (y = spin/turn)
  torso: V3;            // [lean, twist, roll]
  head: V3;             // [pitch, yaw, tilt]
  armL: V3; armR: V3;   // shoulder joints [swing, twist, spread]
  legL: V3; legR: V3;   // hip joints [swing, twist, spread]
  liftL: number; liftR: number; // extra foot lift in studs (swing phase)
  hair: number;         // secondary motion: hair/accessory bounce (x rotation)
  /** Wing flap (y-rotation of the wing roots, radians): 0 = folded against
   * the back, ~1 = spread wide. Only characters with wings read it; the
   * rest ignore it. */
  flap: number;
}

export const restPose = (): Pose => ({
  y: 0, rootPos: [0, 0, 0], root: [0, 0, 0], torso: [0, 0, 0], head: [0, 0, 0],
  armL: [0, 0, 0], armR: [0, 0, 0], legL: [0, 0, 0], legR: [0, 0, 0],
  liftL: 0, liftR: 0, hair: 0, flap: 0,
});

/** Build a Pose from a partial: anything not given is the rest pose. */
export const pose = (p: Partial<Pose>): Pose => ({...restPose(), ...p});

export const NEUTRAL_POSE: Pose = restPose();

const lerp = (a: number, b: number, w: number) => a + (b - a) * w;
const lerp3 = (a: V3, b: V3, w: number): V3 => [lerp(a[0], b[0], w), lerp(a[1], b[1], w), lerp(a[2], b[2], w)];

/** Blend two poses: w = 0 gives a, w = 1 gives b. V3 joints blend
 * component-wise; scalars blend directly. */
export const lerpPose = (a: Pose, b: Pose, k: number): Pose => {
  const out: any = {};
  (Object.keys(NEUTRAL_POSE) as (keyof Pose)[]).forEach((key) => {
    const av: any = a[key], bv: any = b[key];
    out[key] = Array.isArray(av) ? lerp3(av as V3, bv as V3, k) : lerp(av, bv, k);
  });
  return out as Pose;
};

/** Layer one pose over another: the `overlay` wins on the listed joints,
 * the `base` supplies everything else. This is how movements combine
 * simultaneously — e.g. fly for the body, legs, head and wings, plus wave
 * for the right arm only:
 *   layerPose(flyPose(t), wavePose(t), ['armR'])
 * Any joints, any two clips. */
export const layerPose = (base: Pose, overlay: Pose, keys: (keyof Pose)[]): Pose => {
  const out: any = {...base};
  keys.forEach((k) => {
    out[k] = overlay[k];
  });
  return out as Pose;
};

/**
 * Walk-cycle driver. One full cycle = left + right step, so with cycle=1 and
 * a clip length that is a whole number of seconds the animation loops
 * seamlessly. This is the original walk math, now returning a V3 Pose.
 * `strength` (Claude's name for the old `walk` option, kept as an alias):
 * 1 = full walk, 0 = standing sway — blend toward idle by lowering it.
 * Sides: our legL/armL drive the -x limb (see the Pose comment above), so
 * the signs here are OURS, not Claude's — his walk has the same shape with
 * L/R swapped. The torso twist is stored negated (torso[1] = -twist) because
 * that is the rotation the rig was applying under the scalar Pose.
 */
export const walkPose = (t: number, o: {cycle?: number; walk?: number; strength?: number; legLength?: number; legAmp?: number; armAmp?: number} = {}): Pose => {
  const {cycle = 1, legLength = 2.3, legAmp = 0.46, armAmp = 0.465} = o;
  const walk = o.strength ?? o.walk ?? 1;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph) * walk;
  const twist = Math.sin(ph) * 0.09 * walk;
  return pose({
    legL: [-s * legAmp, 0, 0],
    legR: [s * legAmp, 0, 0],
    liftL: walk * 0.14 * Math.max(0, Math.cos(ph)),
    liftR: walk * 0.14 * Math.max(0, -Math.cos(ph)),
    armL: [s * armAmp, 0, 0],
    armR: [-s * armAmp, 0, 0],
    y: legLength * (Math.cos(legAmp * Math.abs(s)) - 1) + Math.sin(t * 2.2) * 0.02 * (1 - walk),
    torso: [0.04 * walk, -twist, 0],
    head: [Math.sin(ph * 2) * 0.025 * walk, twist * 1.6, 0],
    hair: Math.sin(ph * 2 + 0.8) * 0.035 * walk,
    // Wings ride the walk with a small flap, exactly as WingedBoy did
    // before the Pose system (sin(ph) * 0.055 * walk).
    flap: Math.sin(ph) * 0.055 * walk,
  });
};

/** Faster, bigger walk: longer stride, higher lift, forward lean, airborne bob.
 * Ported from Claude's character-to-remotion update (2026-11-20): lean 0.2,
 * legAmp 0.85, armAmp 0.95, and an explicit flight phase. Note: Claude's
 * run lifts the body as the legs SPREAD (y = -0.08 + 0.25*|s|); that is
 * inverted from real running (the body is highest mid-flight, when the legs
 * pass), so this keeps our correct direction — up when the legs pass,
 * down at foot strike — and takes only his lean and amplitudes. The arms
 * carry his small outward spread (z 0.1). */
export const runPose = (t: number, o: {cycle?: number; legLength?: number; lean?: number} = {}): Pose => {
  const {cycle = 0.6, legLength = 2.3, lean = 0.2} = o;
  const legAmp = 0.85;
  const armAmp = 0.95;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  const twist = Math.sin(ph) * 0.14;
  return pose({
    legL: [-s * legAmp, 0, 0],
    legR: [s * legAmp, 0, 0],
    liftL: 0.3 * Math.max(0, Math.cos(ph)),
    liftR: 0.3 * Math.max(0, -Math.cos(ph)),
    armL: [s * armAmp, 0, 0.1],
    armR: [-s * armAmp, 0, 0.1],
    y: 0.4 * legLength * (Math.cos(legAmp * Math.abs(s)) - 1) + 0.12 * (1 - Math.abs(s)),
    torso: [lean, -twist, 0],
    head: [-0.05, twist * 1.2, 0],
    hair: Math.sin(ph * 2 + 0.8) * 0.05,
  });
};

/** Breathing idle. Slow look-around. Loops cleanly over `cycle` (default 2.8s).
 * The arms carry a small outward spread that breathes with the body. */
export const idlePose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 2.8} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const b = Math.sin(ph);
  return pose({
    y: b * 0.02,
    torso: [0, 0, Math.sin(ph) * 0.02],
    head: [Math.sin(ph * 2) * 0.01, b * 0.1, 0],
    hair: Math.sin(ph * 2) * 0.005,
    armL: [b * 0.02, 0, 0.03 + b * 0.02],
    armR: [-b * 0.02, 0, 0.03 + b * 0.02],
  });
};

/** Wave: one-shot. The arm raises over 0.5s (smoothstep), then waves.
 * Ported from Claude's character-to-remotion update (2026-11-20). It layers
 * on the idle pose so the body keeps breathing, and the head turns toward
 * the waving arm. `arm` picks the side ('R' = the old default, matching
 * the previous wavePose). NOTE: this is a one-shot, not a loop — it starts
 * arm-down and ends arm-up, by design (Claude's animations.md says the
 * same). In a timeline the crossfade into the next clip hides the reset.
 * V3: the wobble now lives on the arm's z-spread (as Claude wrote it),
 * not folded into the x-pump — the hand sweeps outward as it waves. */
export const wavePose = (t: number, o: {arm?: 'L' | 'R'; speed?: number} = {}): Pose => {
  const {arm = 'R', speed = 9} = o;
  const u = Math.min(1, Math.max(0, t / 0.5));
  const smooth = u * u * (3 - 2 * u);
  const sw = Math.sin(t * speed) * 0.35 * smooth;
  const base = idlePose(t);
  // Raised arm: swings up (-2.7) and spreads outward as it waves.
  const raised: V3 = [-2.7 * smooth, 0, 0.25 * smooth + sw];
  return {
    ...base,
    head: [base.head[0], (arm === 'L' ? 0.2 : -0.2) * smooth, 0],
    armL: arm === 'L' ? raised : base.armL,
    armR: arm === 'R' ? raised : base.armR,
  };
};

/** Jump: three phases — crouch (18%), launch with arms up and legs tucked
 * (64%), land (18%). Ported from Claude's character-to-remotion update
 * (2026-11-20). `period` is one full jump (default 1.2s), `height` the peak
 * body rise. Default height is 1.5, not Claude's 2.4: 2.4 puts the head
 * above the standard PoseLab framing (camera tops out at ~7.5, head peaks
 * at ~9.5). Pass `height: 2.4` for a bigger jump when the camera allows it.
 * The old jump was a single parabolic arc with a symmetric tuck; this one
 * has anticipation (crouch) and a real landing, so it reads as a jump
 * instead of a bounce. V3: the arms and legs spread as they rise. */
export const jumpPose = (t: number, o: {period?: number; height?: number} = {}): Pose => {
  const {period = 1.2, height = 1.5} = o;
  const u = ((((t / period) % 1) + 1) % 1);
  let y = 0, air = 0;
  if (u < 0.18) y = -0.45 * Math.sin(Math.PI * u / 0.18);
  else if (u < 0.82) { air = Math.sin(Math.PI * (u - 0.18) / 0.64); y = height * air; }
  else y = -0.35 * Math.sin(Math.PI * (u - 0.82) / 0.18);
  const crouch = y < 0 ? -y : 0;
  return pose({
    y,
    torso: [0.6 * crouch, 0, 0],
    head: [-0.2 * crouch, 0, 0],
    hair: -0.12 * air + 0.1 * crouch,
    armL: [-2.3 * air + 1.2 * crouch, 0, 0.5 * air],
    armR: [-2.3 * air + 1.2 * crouch, 0, 0.5 * air],
    legL: [-0.3 * air, 0, 0.1 * air],
    legR: [0.2 * air, 0, 0.1 * air],
  });
};

/** Bouncy dance on the beat. Ported from Claude's character-to-remotion
 * update (2026-11-20): beat-based, so it syncs to music — `bpm` sets the
 * beat, one full cycle = one beat. Both arms stay raised and alternate; the
 * torso sways on a half-beat. Default bpm is 150 (raised from Claude's 120
 * — the maintainer: the dance still read a bit slow at 120). At 150 the beat is
 * 0.4s, so the 2s CLIPS duration holds exactly 5 beats and loops cleanly.
 * The old dance used a fixed 2s cycle with arms alternating up/down.
 * V3: the arms and legs carry Claude's spreads, so the dance opens out
 * instead of pumping straight up and down. */
export const dancePose = (t: number, o: {bpm?: number} = {}): Pose => {
  const {bpm = 150} = o;
  const beat = 60 / bpm;
  const ph = (t / beat) * Math.PI * 2;
  const s = Math.sin(ph);
  const h = Math.sin(ph / 2);
  return pose({
    y: -0.1 + 0.3 * Math.abs(s),
    torso: [0.05, h * 0.3, h * 0.06],
    head: [s * 0.12, -h * 0.2, 0],
    hair: s * 0.06,
    armL: [-1.3 + 0.7 * s, 0, 0.35 + 0.25 * s],
    armR: [-1.3 - 0.7 * s, 0, 0.35 - 0.25 * s],
    legL: [0.15 * s, 0, 0.12 + 0.08 * s],
    legR: [-0.15 * s, 0, 0.12 - 0.08 * s],
    liftL: 0.12 * Math.max(0, s),
    liftR: 0.12 * Math.max(0, -s),
  });
};

/** Flying: hover ~1.2 studs up with a bob on each downstroke, legs trailing
 * behind, arms slightly back, forward lean, and the wings beating on a 1s
 * flap cycle. `flap` is the wing-root angle: ~0.1 at the bottom of the
 * beat, ~1.0 at the top. Loops cleanly over `duration` (default 2s = 2
 * flaps). Wingless characters fly the same way, minus the wings. */
export const flyPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1} = o;
  const ph = (t / cycle) * Math.PI * 2;
  return pose({
    y: 1.2 + Math.sin(ph * 2) * 0.12,
    flap: 0.55 + Math.sin(ph) * 0.45,
    legL: [0.3 + Math.sin(ph) * 0.05, 0, 0],
    legR: [0.25 - Math.sin(ph) * 0.05, 0, 0],
    armL: [0.2, 0, 0],
    armR: [0.2, 0, 0],
    torso: [0.12, 0, 0],
    head: [-0.06, 0, 0],
    hair: Math.sin(ph * 2) * 0.02,
  });
};

// ---------------------------------------------------------------------------
// Catalog clips — the works-now moves from CATALOG.md. All are pure joint
// math on the V3 rig, and every one loops cleanly over its cycle, so every
// CLIPS duration is a whole number of cycles. Negative y is kept small
// (≤0.2) so rigid legs never sink through the floor.
// Conversion note (V3, 2026-11-20): the x-swings, signs, and side mapping
// are the scalar Pose's — behaviour-preserving. The z-spreads are new:
// 0 unless noted. torso = [lean, -twist, 0] (twist stored negated, as the
// scalar rig applied it), head = [headPitch, headYaw, 0], hair = bounce.
// ---------------------------------------------------------------------------

/** Sprint: faster, longer stride than run, deeper lean, arms pumping hard. */
export const sprintPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 0.45} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    legL: [-s * 0.9, 0, 0],
    legR: [s * 0.9, 0, 0],
    liftL: 0.35 * Math.max(0, Math.cos(ph)),
    liftR: 0.35 * Math.max(0, -Math.cos(ph)),
    armL: [s * 1.1, 0, 0],
    armR: [-s * 1.1, 0, 0],
    y: 0.12 * (1 - Math.abs(s)),
    torso: [0.25, -s * 0.18, 0],
    head: [-0.05, s * 0.15, 0],
    hair: Math.sin(ph * 2) * 0.06,
  });
};

/** March: stiff high knees, arms swinging straight and opposite. */
export const marchPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 0.9} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    legL: [s * 0.6, 0, 0],
    legR: [-s * 0.6, 0, 0],
    liftL: 0.45 * Math.max(0, s),
    liftR: 0.45 * Math.max(0, -s),
    armL: [-s * 0.5, 0, 0],
    armR: [s * 0.5, 0, 0],
    y: -0.02,
    torso: [0.05, -s * 0.05, 0],
    hair: Math.sin(ph * 2) * 0.01,
  });
};

/** Hop: both feet together, body rising and falling, legs tucking in the air. */
export const hopPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 0.7} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  const up = Math.max(0, s);
  return pose({
    legL: [0.3 * up, 0, 0],
    legR: [0.3 * up, 0, 0],
    liftL: 0.25 * up,
    liftR: 0.25 * up,
    armL: [0.2 + s * 0.1, 0, 0],
    armR: [0.2 + s * 0.1, 0, 0],
    y: 0.3 * up - 0.1 * Math.max(0, -s),
    torso: [0.05, 0, 0],
  });
};

/** Skip: alternating hop-steps, two bounces per cycle, arms swinging. */
export const skipPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 0.8} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    legL: [s * 0.5, 0, 0],
    legR: [-s * 0.5, 0, 0],
    liftL: 0.35 * Math.max(0, s),
    liftR: 0.35 * Math.max(0, -s),
    armL: [-s * 0.4, 0, 0],
    armR: [s * 0.4, 0, 0],
    y: 0.12 * Math.abs(s),
    torso: [0.06, -s * 0.08, 0],
    hair: Math.sin(ph * 2) * 0.02,
  });
};

/** Sidestep: a sideways shuffle, legs alternating out, body swaying. */
export const sidestepPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    legL: [0.3 + s * 0.3, 0, 0],
    legR: [0.3 - s * 0.3, 0, 0],
    liftL: 0.2 * Math.max(0, s),
    liftR: 0.2 * Math.max(0, -s),
    armL: [-s * 0.3, 0, 0],
    armR: [s * 0.3, 0, 0],
    y: 0.05 * Math.sin(ph * 2),
    torso: [0.03, -s * 0.1, 0],
  });
};

/** Sneak: crouched slow walk, arms held forward and low. */
export const sneakPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1.4} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    legL: [s * 0.35, 0, 0],
    legR: [-s * 0.35, 0, 0],
    liftL: 0.1 * Math.max(0, Math.cos(ph)),
    liftR: 0.1 * Math.max(0, -Math.cos(ph)),
    armL: [-0.5, 0, 0],
    armR: [-0.5, 0, 0],
    y: -0.2,
    torso: [0.2, -s * 0.06, 0],
    head: [-0.05, s * 0.1, 0],
  });
};

/** Bow: bend forward from the waist and back, head down, arms hanging.
 * Lean pushed 0.55 → 0.75 (2026-11-20, the maintainer: the bow read as a head bow
 * from the front 3/4 camera — the deeper lean makes the torso bend read
 * from the front too). Side view unchanged (it was already correct). */
export const bowPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1.6} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const b = Math.max(0, Math.sin(ph));
  return pose({
    torso: [0.75 * b, 0, 0],
    head: [0.35 * b, 0, 0],
    armL: [0.1 * b, 0, 0],
    armR: [0.1 * b, 0, 0],
    y: -0.1 * b,
  });
};

/** Nod: head pitches down and up, twice per cycle. */
export const nodPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1} = o;
  const ph = (t / cycle) * Math.PI * 2;
  return pose({
    head: [0.25 * Math.sin(ph), 0, 0],
  });
};

/** Shrug: arms rise forward a little, head tilts, small lift. V3: the
 * arms now spread outward as they rise (the scalar rig had no lateral
 * joint, so the old shrug read only through the head tilt). */
export const shrugPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1.2} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  const up = Math.max(0, s);
  return pose({
    armL: [-0.35 * up, 0, 0.3 * up],
    armR: [-0.35 * up, 0, 0.3 * up],
    head: [0.05 * s, 0.15 * s, 0],
    y: 0.05 * up,
    torso: [0.05 * up, 0, 0],
  });
};

/** Point: right arm straight out in front, head turned toward it. */
export const pointPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1.2} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    armR: [-1.5 + s * 0.08, 0, 0],
    armL: [0.2, 0, 0],
    head: [-0.05, -0.2 + s * 0.05, 0],
    torso: [0.08, 0, 0],
    y: 0.01 * s,
  });
};

/** Cheer: both arms up, small jumps on the beat. */
export const cheerPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 0.8} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    armL: [-2.2, 0, 0.15],
    armR: [-2.2, 0, 0.15],
    y: 0.15 * Math.max(0, s),
    torso: [-0.05, 0, 0],
    head: [-0.1, 0, 0],
    hair: 0.02 * s,
  });
};

/** Salute: right arm sweeps up to the head and back down. */
export const salutePose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1.2} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const up = Math.max(0, Math.sin(ph));
  return pose({
    armR: [-2.6 * up, 0, 0.1 * up],
    armL: [0.1 * up, 0, 0],
    head: [0.05 * up, 0, 0],
    torso: [0.02 * up, 0, 0],
  });
};

/** Look around: head sweeps left and right, slow, with a small dip. */
export const lookAroundPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 2.4} = o;
  const ph = (t / cycle) * Math.PI * 2;
  return pose({
    head: [0.08 * Math.sin(ph * 2), 0.6 * Math.sin(ph), 0],
    y: 0.01 * Math.sin(ph),
  });
};

/** Think: head tilted, right arm raised toward the chin (no elbow, so the
 * arm only reaches chest height — the head tilt carries it). */
export const thinkPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 2} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    armR: [-0.8, 0, 0],
    head: [0.1 + s * 0.03, 0.25, 0],
    torso: [0.06, 0, 0],
    y: 0.01 * s,
  });
};

/** Celebrate: both arms up, bouncing, twist — the big win. */
export const celebratePose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    armL: [-2.4, 0, 0.2],
    armR: [-2.4, 0, 0.2],
    y: 0.3 * Math.max(0, s),
    torso: [-0.05, -s * 0.15, 0],
    head: [-0.08, 0, 0],
    hair: 0.03 * s,
  });
};

/** Scared cower: crouched, arms up guarding the face, leaning back. */
export const scaredCowerPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1.4} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    y: -0.2,
    armL: [-1.2 + s * 0.05, 0, 0.1],
    armR: [-1.2 - s * 0.05, 0, 0.1],
    legL: [0.2, 0, 0],
    legR: [0.2, 0, 0],
    torso: [0.25, 0, 0],
    head: [0.15, 0, 0],
    hair: 0.01 * s,
  });
};

/** Proud: chest out, chin up, arms slightly back. */
export const proudPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 2} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    torso: [-0.12, 0, 0],
    head: [-0.08, 0, 0],
    armL: [0.4, 0, 0.1],
    armR: [0.4, 0, 0.1],
    y: 0.02 + 0.01 * s,
    hair: 0.005 * s,
  });
};

/** Punch: right arm thrusts forward on the beat, torso twisting into it. */
export const punchPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 0.7} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    armR: [-1.4 - 0.3 * Math.max(0, s), 0, 0],
    armL: [0.3, 0, 0],
    torso: [0.1, -0.15 * s, 0],
    legL: [0.3, 0, 0],
    legR: [-0.2, 0, 0],
    y: 0.01 * s,
  });
};

/** Kick: right leg swings forward and up, arms counter-swinging. */
export const kickPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 0.9} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  const k = Math.max(0, s);
  return pose({
    // Forward kick: negative x-rotation swings the leg FORWARD (positive
    // would swing it backward — the original code had the sign wrong and
    // the kick went behind him). 1.4 rad (~80°) — nearly horizontal, foot
    // at chest height — so the thrust reads as forward even from the
    // PoseLab's front 3/4 camera, where a 57° kick foreshortens into a
    // leg going up and down in place (the maintainer: "still looks backward",
    // 2026-11-20; the 57° peak still looked right but the motion didn't).
    legR: [-1.4 * k, 0, 0],
    liftR: 0.5 * k,
    legL: [-0.1, 0, 0],
    armL: [-0.4 * s, 0, 0],
    armR: [0.4 * s, 0, 0],
    torso: [-0.05, -0.1 * s, 0],
    y: -0.02 * k,
  });
};

/** Throw: right arm winds back then swings forward, torso following. */
export const throwPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    armR: [-0.5 - 0.9 * s, 0, 0],
    armL: [0.3 * s, 0, 0],
    torso: [0.1 + 0.05 * s, -0.2 * s, 0],
    legL: [0.25, 0, 0],
    legR: [-0.25, 0, 0],
    head: [0, 0.1 * s, 0],
  });
};

/** Push: both arms forward, leaning into a lunge stance. */
export const pushPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1.2} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    armL: [-1.2, 0, 0.1],
    armR: [-1.2, 0, 0.1],
    torso: [0.15 + 0.05 * s, 0, 0],
    legL: [0.3, 0, 0],
    legR: [-0.3, 0, 0],
    y: -0.05,
    head: [-0.03, 0, 0],
  });
};

/** Pull: both arms back, leaning away, braced stance. */
export const pullPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1.2} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    armL: [0.5, 0, 0],
    armR: [0.5, 0, 0],
    torso: [-0.15, 0, 0],
    legL: [-0.25, 0, 0],
    legR: [0.25, 0, 0],
    y: -0.02,
    head: [0.05 * s, 0, 0],
  });
};

/** Shake-head: head swings side to side (no = head shake). Two shakes per
 * 2s. Uses head yaw only — no new joints needed. */
export const shakeHeadPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1} = o;
  const ph = (t / cycle) * Math.PI * 2;
  return pose({
    head: [0.05, 0.5 * Math.sin(ph), 0],
  });
};

/** Clap: both arms pump forward together, fast. V3: the arms angle INWARD
 * (negative spread) as they pump, so the hands can actually meet in the
 * middle — the scalar rig had no lateral joint, so the old clap read only
 * at speed. Cycle is short (0.5s, 4 claps in 2s). */
export const clapPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 0.5} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const c = 0.5 + 0.5 * Math.sin(ph);
  return pose({
    armL: [-1.2 * c, 0, -0.4 * c],
    armR: [-1.2 * c, 0, -0.4 * c],
    y: 0.05 * c,
    torso: [0.05 * c, 0, 0],
  });
};

/** Shy: head down, shoulders in, slight crouch, gentle sway. A held pose
 * with a slow breathing sway, not a repeating action. V3: the shoulders
 * angle inward (negative spread) — the shy read. */
export const shyPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 2} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    head: [0.4 + 0.05 * s, 0, 0],
    armL: [0.25, 0, -0.1],
    armR: [0.25, 0, -0.1],
    torso: [0.15, 0, 0],
    y: -0.1,
  });
};

/** Laugh-shake: whole body shakes with laughter — fast vertical bounce,
 * slight lean wobble, head tipped back. */
export const laughShakePose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 0.5} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    y: 0.08 * s,
    torso: [0.1 * s, 0, 0],
    head: [-0.2, 0, 0],
    armL: [-0.3, 0, 0],
    armR: [-0.3, 0, 0],
  });
};

/** Angry-stomp: one leg lifts and slams down, arms tense at the sides,
 * leaning forward, head down. Two stomps per 2s. */
export const angryStompPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const k = Math.max(0, Math.sin(ph));
  return pose({
    legR: [-0.5 * k, 0, 0],
    liftR: 0.4 * k,
    armL: [0.3, 0, 0],
    armR: [0.3, 0, 0],
    torso: [0.2, 0, 0],
    head: [0.2, 0, 0],
    y: -0.05 * k,
  });
};

/** Cry-hunch: hunched over, head down, both arms raised to cover the face,
 * shoulders shaking gently. The arms reach only chest height (no elbow),
 * so the hands hover in front of the face rather than covering it. V3:
 * the arms angle inward toward the face. */
export const cryHunchPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1.4} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    torso: [0.4, 0, 0],
    head: [0.4, 0, 0],
    armL: [-1.5, 0, -0.2],
    armR: [-1.5, 0, -0.2],
    y: -0.15 + 0.03 * s,
  });
};

/** Confused-shrug: the shrug's arm raise plus a big head tilt to one side
 * and a slow questioning sway. V3: the arms spread outward as they rise,
 * so the shrug reads without needing the exaggerated head tilt — the tilt
 * is kept (0.35 rad) because it still helps. */
export const confusedShrugPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 2} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  const up = Math.max(0, s);
  return pose({
    armL: [-0.4 * up, 0, 0.35 * up],
    armR: [-0.4 * up, 0, 0.35 * up],
    head: [0.1 * up, 0.35 * up, 0],
    y: 0.05 * up,
    torso: [0.08 * up, 0, 0],
  });
};

// ---------------------------------------------------------------------------
// New clips (2026-11-20, the maintainer: "Let's do them all"). All V3-native —
// they use the z-spread from the start, which the scalar rig could not.
// ---------------------------------------------------------------------------

/** Climb: alternating arms reaching up to grab the next hold, legs stepping
 * up, body leaning into the wall, head looking up. */
export const climbPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1.2} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    armL: [-1.2 - 0.8 * Math.max(0, s), 0, 0.25],
    armR: [-1.2 - 0.8 * Math.max(0, -s), 0, 0.25],
    legL: [-0.5 * Math.max(0, s), 0, 0],
    legR: [-0.5 * Math.max(0, -s), 0, 0],
    liftL: 0.4 * Math.max(0, s),
    liftR: 0.4 * Math.max(0, -s),
    torso: [0.15, 0, 0],
    head: [-0.1, 0, 0],
    y: 0.05 * Math.sin(ph * 2),
  });
};

/** Swim: freestyle — arms sweeping in opposite phases, legs kicking fast,
 * body leaning forward toward horizontal. */
export const swimPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    armL: [-1.0 - 0.8 * s, 0, 0.15],
    armR: [-1.0 + 0.8 * s, 0, 0.15],
    legL: [0.3 * Math.sin(ph * 2), 0, 0],
    legR: [-0.3 * Math.sin(ph * 2), 0, 0],
    torso: [0.35, 0, 0],
    head: [-0.1, 0, 0],
    y: 0.05 * Math.sin(ph * 2),
  });
};

/** Catch: both arms up and forward, ready, then closing in as if catching
 * a ball. Legs braced. */
export const catchPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const c = 0.5 + 0.5 * Math.sin(ph);
  return pose({
    // v2 (2026-11-21): amplitude pushed up so the reach reads from the
    // front 3/4 camera — open: arms up-forward past horizontal, wide apart;
    // closed: arms forward, together (the catch).
    armL: [-1.6 + 0.8 * c, 0, 0.7 - 0.5 * c],
    armR: [-1.6 + 0.8 * c, 0, 0.7 - 0.5 * c],
    legL: [0.15, 0, 0],
    legR: [-0.15, 0, 0],
    torso: [0.1, 0, 0],
    head: [-0.05, 0, 0],
    y: 0.02 * Math.sin(ph),
  });
};

/** High-five: right arm up high, palm out, left arm down, head turned
 * toward the raised hand, small bounce. */
export const highFivePose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1.2} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    armR: [-2.4, 0, 0.3],
    armL: [0.2, 0, 0],
    head: [-0.05, -0.2, 0],
    torso: [-0.03, -0.1 * s, 0],
    y: 0.05 * Math.max(0, s),
  });
};

/** Hug: arms wide open, then closing in for the embrace. Legs together,
 * slight lean in, head tilted. */
export const hugPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1.6} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const b = Math.max(0, Math.sin(ph));
  return pose({
    armL: [-0.3 - 0.7 * b, 0, 0.8 - 0.9 * b],
    armR: [-0.3 - 0.7 * b, 0, 0.8 - 0.9 * b],
    torso: [0.1, 0, 0],
    head: [0.05, 0, 0],
    y: -0.02 * b,
  });
};

/** Dig: both arms down and forward, scooping, body leaning into it, legs
 * in a lunge, head down watching the dig. */
export const digPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 1} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  return pose({
    // v2 (2026-11-21): amplitude pushed up so the scoop reads from the
    // front 3/4 camera — deeper lean, deeper lunge, arms swinging further
    // forward on the scoop (past horizontal) and back on the return.
    armL: [-1.3 + 0.5 * s, 0, 0.25],
    armR: [-1.3 + 0.5 * s, 0, 0.25],
    legL: [0.45, 0, 0],
    legR: [-0.45, 0, 0],
    torso: [0.45, 0, 0],
    head: [0.15, 0, 0],
    y: -0.08 + 0.04 * s,
  });
};

/** Hammer: right arm raised up, then swinging down to strike, torso
 * twisting into the swing, legs braced. */
export const hammerPose = (t: number, o: {cycle?: number} = {}): Pose => {
  const {cycle = 0.8} = o;
  const ph = (t / cycle) * Math.PI * 2;
  const s = Math.sin(ph);
  const up = Math.max(0, s);
  return pose({
    armR: [-0.5 - 1.7 * up, 0, 0.1],
    armL: [0.2, 0, 0],
    torso: [0.15, -0.2 * s, 0],
    legL: [0.2, 0, 0],
    legR: [-0.2, 0, 0],
    head: [0.1, 0, 0],
    y: -0.02 * up,
  });
};

export type ClipName = 'walk' | 'run' | 'idle' | 'wave' | 'jump' | 'dance' | 'fly'
  | 'sprint' | 'march' | 'hop' | 'skip' | 'sidestep' | 'sneak'
  | 'bow' | 'nod' | 'shrug' | 'point' | 'cheer' | 'salute' | 'look-around' | 'think'
  | 'celebrate' | 'scared-cower' | 'proud'
  | 'punch' | 'kick' | 'throw' | 'push' | 'pull'
  | 'shake-head' | 'clap' | 'shy' | 'laugh-shake' | 'angry-stomp' | 'cry-hunch'
  | 'confused-shrug'
  | 'climb' | 'swim' | 'catch' | 'high-five' | 'hug' | 'dig' | 'hammer';
export interface Clip { name: ClipName; cycle: number; duration: number; pose: (t: number) => Pose; }

/** Every duration is a whole number of cycles, so every clip loops cleanly. */
export const CLIPS: Record<ClipName, Clip> = {
  walk: {name: 'walk', cycle: 1, duration: 2, pose: (t) => walkPose(t)},
  run: {name: 'run', cycle: 0.6, duration: 1.8, pose: (t) => runPose(t)},
  idle: {name: 'idle', cycle: 2.8, duration: 2.8, pose: (t) => idlePose(t)},
  // wave is a one-shot (raises, then waves; starts arm-down, ends arm-up),
  // not a loop — see wavePose. It is excluded from the loop-closure check.
  wave: {name: 'wave', cycle: 1, duration: 2, pose: (t) => wavePose(t)},
  jump: {name: 'jump', cycle: 1.2, duration: 2.4, pose: (t) => jumpPose(t)},
  dance: {name: 'dance', cycle: 0.4, duration: 2, pose: (t) => dancePose(t)},
  fly: {name: 'fly', cycle: 1, duration: 2, pose: (t) => flyPose(t)},
  sprint: {name: 'sprint', cycle: 0.45, duration: 1.8, pose: (t) => sprintPose(t)},
  march: {name: 'march', cycle: 0.9, duration: 1.8, pose: (t) => marchPose(t)},
  hop: {name: 'hop', cycle: 0.7, duration: 1.4, pose: (t) => hopPose(t)},
  skip: {name: 'skip', cycle: 0.8, duration: 1.6, pose: (t) => skipPose(t)},
  sidestep: {name: 'sidestep', cycle: 1, duration: 2, pose: (t) => sidestepPose(t)},
  sneak: {name: 'sneak', cycle: 1.4, duration: 2.8, pose: (t) => sneakPose(t)},
  bow: {name: 'bow', cycle: 1.6, duration: 1.6, pose: (t) => bowPose(t)},
  nod: {name: 'nod', cycle: 1, duration: 2, pose: (t) => nodPose(t)},
  shrug: {name: 'shrug', cycle: 1.2, duration: 2.4, pose: (t) => shrugPose(t)},
  point: {name: 'point', cycle: 1.2, duration: 2.4, pose: (t) => pointPose(t)},
  cheer: {name: 'cheer', cycle: 0.8, duration: 1.6, pose: (t) => cheerPose(t)},
  salute: {name: 'salute', cycle: 1.2, duration: 1.2, pose: (t) => salutePose(t)},
  'look-around': {name: 'look-around', cycle: 2.4, duration: 2.4, pose: (t) => lookAroundPose(t)},
  think: {name: 'think', cycle: 2, duration: 2, pose: (t) => thinkPose(t)},
  celebrate: {name: 'celebrate', cycle: 1, duration: 2, pose: (t) => celebratePose(t)},
  'scared-cower': {name: 'scared-cower', cycle: 1.4, duration: 1.4, pose: (t) => scaredCowerPose(t)},
  proud: {name: 'proud', cycle: 2, duration: 2, pose: (t) => proudPose(t)},
  punch: {name: 'punch', cycle: 0.7, duration: 1.4, pose: (t) => punchPose(t)},
  kick: {name: 'kick', cycle: 0.9, duration: 1.8, pose: (t) => kickPose(t)},
  throw: {name: 'throw', cycle: 1, duration: 2, pose: (t) => throwPose(t)},
  push: {name: 'push', cycle: 1.2, duration: 1.2, pose: (t) => pushPose(t)},
  pull: {name: 'pull', cycle: 1.2, duration: 1.2, pose: (t) => pullPose(t)},
  'shake-head': {name: 'shake-head', cycle: 1, duration: 2, pose: (t) => shakeHeadPose(t)},
  clap: {name: 'clap', cycle: 0.5, duration: 2, pose: (t) => clapPose(t)},
  shy: {name: 'shy', cycle: 2, duration: 2, pose: (t) => shyPose(t)},
  'laugh-shake': {name: 'laugh-shake', cycle: 0.5, duration: 2, pose: (t) => laughShakePose(t)},
  'angry-stomp': {name: 'angry-stomp', cycle: 1, duration: 2, pose: (t) => angryStompPose(t)},
  'cry-hunch': {name: 'cry-hunch', cycle: 1.4, duration: 2.8, pose: (t) => cryHunchPose(t)},
  'confused-shrug': {name: 'confused-shrug', cycle: 2, duration: 2, pose: (t) => confusedShrugPose(t)},
  climb: {name: 'climb', cycle: 1.2, duration: 2.4, pose: (t) => climbPose(t)},
  swim: {name: 'swim', cycle: 1, duration: 2, pose: (t) => swimPose(t)},
  catch: {name: 'catch', cycle: 1, duration: 2, pose: (t) => catchPose(t)},
  'high-five': {name: 'high-five', cycle: 1.2, duration: 2.4, pose: (t) => highFivePose(t)},
  hug: {name: 'hug', cycle: 1.6, duration: 3.2, pose: (t) => hugPose(t)},
  dig: {name: 'dig', cycle: 1, duration: 2, pose: (t) => digPose(t)},
  hammer: {name: 'hammer', cycle: 0.8, duration: 1.6, pose: (t) => hammerPose(t)},
};

export const clipPose = (name: ClipName, t: number): Pose => CLIPS[name].pose(t);

// ---------------------------------------------------------------------------
// RootMotion — whole-object motion, works on anything (even non-humanoids)
// ---------------------------------------------------------------------------
export type RootMotionMode = 'spin' | 'bounce' | 'float' | 'squash' | 'shake' | 'pulse' | 'wobble' | 'fall-over' | 'pop-in' | 'slide-in';
export interface RootTransform { yaw: number; y: number; scaleY: number; scaleXZ: number; x: number; roll: number; }

export const rootTransform = (mode: RootMotionMode, t: number, duration = 3): RootTransform => {
  const smooth = (x: number) => { const c = Math.min(1, Math.max(0, x)); return c * c * (3 - 2 * c); };
  switch (mode) {
    case 'spin': // turntable: one full turn over `duration`
      return {yaw: ((t % duration) / duration) * Math.PI * 2, y: 0, scaleY: 1, scaleXZ: 1, x: 0, roll: 0};
    case 'bounce': {
      const p = Math.abs(Math.sin((t / 0.6) * Math.PI));
      return {yaw: 0, y: 0.3 * p, scaleY: 1 - 0.1 * (1 - p), scaleXZ: 1 + 0.05 * (1 - p), x: 0, roll: 0};
    }
    case 'float':
      return {yaw: 0, y: 0.15 * Math.sin((t / 2) * Math.PI * 2), scaleY: 1, scaleXZ: 1, x: 0, roll: 0};
    case 'squash': {
      const p = Math.abs(Math.sin((t / 0.8) * Math.PI));
      return {yaw: 0, y: 0, scaleY: 1 - 0.12 * p, scaleXZ: 1 + 0.06 * p, x: 0, roll: 0};
    }
    // Ported from Claude's character-to-remotion update (2026-11-20):
    // shake (fast sideways), pulse (scale breathe), wobble (roll side to
    // side). These work on any object — a character, a prop, a mascot —
    // because they only move the root transform.
    case 'shake':
      return {yaw: 0, y: 0, scaleY: 1, scaleXZ: 1, x: 0.15 * Math.sin(t * 45), roll: 0};
    case 'pulse': {
      const k = 1 + 0.08 * Math.sin((Math.PI * 2 * t) / 1);
      return {yaw: 0, y: 0, scaleY: k, scaleXZ: k, x: 0, roll: 0};
    }
    case 'wobble':
      return {yaw: 0, y: 0, scaleY: 1, scaleXZ: 1, x: 0, roll: 0.2 * Math.sin((Math.PI * 2 * t) / 1)};
    // New (2026-11-20, the maintainer: "Let's do them all"):
    case 'fall-over': {
      // Tips over to the side and drops, over `duration`. One-shot: the
      // character ends lying on its side. k = progress 0 → 1.
      const k = smooth(t / duration);
      return {yaw: 0, y: -0.4 * k, scaleY: 1, scaleXZ: 1, x: 0.6 * k, roll: 1.35 * k};
    }
    case 'pop-in': {
      // Pops in from nothing: scales up fast with a small overshoot, then
      // settles. Invisible at t = 0, full size by ~0.6s.
      const up = smooth(t / 0.25);
      const settle = t > 0.25 ? smooth((t - 0.25) / 0.35) : 0;
      const k = 1.15 * up - 0.15 * settle;
      return {yaw: 0, y: 0, scaleY: k, scaleXZ: k, x: 0, roll: 0};
    }
    case 'slide-in': {
      // Slides in from the left (-3 studs) to centre, over `duration`.
      const k = smooth(t / duration);
      return {yaw: 0, y: 0, scaleY: 1, scaleXZ: 1, x: -3 * (1 - k), roll: 0};
    }
  }
};

/** Wrap any object (character, prop, anything) in whole-object motion. */
export const RootMotion: React.FC<{mode: RootMotionMode; t: number; duration?: number; children: React.ReactNode}> = ({mode, t, duration = 3, children}) => {
  const r = rootTransform(mode, t, duration);
  return (
    <group rotation={[0, r.yaw, r.roll]} position={[r.x, r.y, 0]} scale={[r.scaleXZ, r.scaleY, r.scaleXZ]}>
      {children}
    </group>
  );
};

/** Spin any pose around the vertical axis (turntable). One full turn every
 * `duration` seconds. Ported from Claude's character-to-remotion update
 * (2026-11-20) — his `withTurn` sets the pose's root yaw; this one sets
 * our `root[1]`, which characters apply to a wrapper group around the body.
 * Example: `withTurn(clips.idle(t), t, 4)` — the character idles while
 * slowly turning, one full turn in 4s. */
export const withTurn = (p: Pose, t: number, duration = 4): Pose => ({...p, root: [p.root[0], (t / duration) * Math.PI * 2, p.root[2]]});

/** Fly (or walk, or run) around a circle: position + heading at time t.
 * The character's Pose (e.g. fly) keeps playing while the path moves it —
 * pose and path are independent tracks, so a character can fly in any
 * direction, or a circle, or any path you write the same way, without the
 * clip changing. `yaw` turns the character to face where it is going. */
export const orbitPath = (t: number, o: {radius?: number; duration?: number; height?: number} = {}): {position: V3; yaw: number} => {
  const {radius = 4, duration = 6, height = 0} = o;
  const th = ((t % duration) / duration) * Math.PI * 2;
  return {position: [radius * Math.cos(th), height, radius * Math.sin(th)], yaw: -th};
};

// ---------------------------------------------------------------------------
// Timeline — sequence clips, crossfade between them, optionally add root motion
// ---------------------------------------------------------------------------
export interface TimelineSegment { clip: ClipName; duration: number; root?: RootMotionMode; rootDuration?: number; }
export interface TimelineState { pose: Pose; clip: ClipName; clipTime: number; root: RootTransform; }

/** Evaluate a looping timeline at time t. Crossfades (smoothstep, 0.25s) at
 * every segment boundary, including the wrap from the last segment back to
 * the first, so joints never snap. */
export const timelinePose = (segments: TimelineSegment[], t: number, crossfade = 0.25): TimelineState => {
  const total = segments.reduce((a, s) => a + s.duration, 0);
  const tt = ((t % total) + total) % total;
  let start = 0;
  let idx = 0;
  for (let i = 0; i < segments.length; i++) {
    if (tt < start + segments[i].duration) { idx = i; break; }
    start += segments[i].duration;
  }
  const seg = segments[idx];
  const lt = tt - start;
  let pose = CLIPS[seg.clip].pose(lt);
  if (lt < crossfade) {
    const prev = idx > 0 ? segments[idx - 1] : segments[segments.length - 1];
    const prevPose = CLIPS[prev.clip].pose(prev.duration);
    const k = lt / crossfade;
    const smooth = k * k * (3 - 2 * k);
    pose = lerpPose(prevPose, pose, smooth);
  }
  const root = seg.root ? rootTransform(seg.root, lt, seg.rootDuration ?? seg.duration) : {yaw: 0, y: 0, scaleY: 1, scaleXZ: 1, x: 0, roll: 0};
  return {pose, clip: seg.clip, clipTime: lt, root};
};

export const timelineDuration = (segments: TimelineSegment[]): number => segments.reduce((a, s) => a + s.duration, 0);

// ---------------------------------------------------------------------------
// Performance — two lanes in parallel: a face track (expressions) and a
// body track (clips). The lanes are independent: any expression over any
// pose, each with its own timing. The face track lives in
// kit/expressions.tsx (performanceFace); the body track is timelinePose.
// A Performance's two lanes should total the same duration (the demo
// loops on the longer lane if they differ).
// ---------------------------------------------------------------------------
export interface Performance {
  /** Face lane: expressions in sequence (see expressions.tsx). */
  face: import('./expressions').FaceSegment[];
  /** Body lane: clips in sequence (timelinePose). */
  body: TimelineSegment[];
}

const Rig: React.FC<{lookAt: V3}> = ({lookAt}) => {
  const {camera} = useThree();
  useLayoutEffect(() => { camera.lookAt(...lookAt); camera.updateProjectionMatrix(); });
  return null;
};

/**
 * Plain studio: soft gradient background, 3-point lighting, fixed 3/4 camera.
 * `shadows` (engine only) adds the shadow-casting light and the shadow-catcher
 * ground plane, matching the engine's showcase compositions.
 *
 * CAMERA (the maintainer, 2026-11-20): the camera is per-shot, not fixed. A Short
 * can take one shot from the front and the next from the side — the shot
 * list picks the angle that shows the move best (a bow reads from the side,
 * a wave from the front, a kick from the side). Every composition sets its
 * own cameraPosition / lookAt; the story pipeline already cuts the camera
 * every 2–3s. Stage just renders whatever angle it is given.
 */
export const Stage: React.FC<{children: React.ReactNode; lookAt?: V3; cameraPosition?: V3; fov?: number; background?: string; shadows?: boolean}> = ({children, lookAt = [0, 3.45, 0], cameraPosition = [6.5, 4.0, 13.5], fov = 30, background = 'radial-gradient(circle at 50% 45%, #f4f6f9 0%, #e6e9ee 100%)', shadows = false}) => {
  const {width, height} = useVideoConfig();
  return (
    <AbsoluteFill style={{background}}>
      <ThreeCanvas width={width} height={height} shadows={shadows} camera={{position: cameraPosition, fov, near: 0.1, far: 100}}>
        <Rig lookAt={lookAt} />
        <hemisphereLight args={['#ffffff', '#d5dcea', 1.35]} />
        <directionalLight position={[6, 10, 8]} intensity={2.0} castShadow={shadows} />
        <directionalLight position={[-6, 4, 4]} intensity={1.3} />
        <directionalLight position={[8, 3, 10]} intensity={0.5} />
        {shadows && (
          <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
            <planeGeometry args={[200, 200]} />
            <shadowMaterial opacity={0.22} />
          </mesh>
        )}
        {children}
      </ThreeCanvas>
    </AbsoluteFill>
  );
};
