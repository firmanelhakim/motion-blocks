import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {Stage, clipPose, lerpPose, V3} from './kit/kit';
import {BoltBoy} from './components/BoltBoy';
import {CasualMan} from './components/CasualMan';
import {ClassicNoob} from './components/ClassicNoob';
import {WingedBoy} from './components/WingedBoy';
import {R6Character} from './components/R6Character';
import {CHARACTER_PRESETS, PRESET_NAMES, PresetName} from './characters/look';

/**
 * CircleShowcase — every character we have, standing in a circle, while the
 * camera orbits once around them (to the right, as in the maintainer's sketch).
 * Each character faces the camera, looks around (idle head sway), and waves
 * as the camera passes them — a travelling wave of waving that follows the
 * camera. (2026-11-21)
 *
 * Cast: the 4 kit characters (BoltBoy, CasualMan, ClassicNoob, WingedBoy)
 * plus all 23 R6 presets — 27 in total. The R6 presets use the kit pose
 * system via the `pose` prop, so they idle and wave exactly like the kit
 * characters. The Astronaut is not here — he lives in the separate Mars
 * project, not the engine kit.
 *
 * 30s / 900 frames, 1280x720.
 */

const RADIUS = 17; // circle radius (studs)
const CAM_DIST = 20; // camera to featured-character distance (studs)
const CAM_Y = 5;
const WAVE_SPREAD = 0.45; // radians either side of the camera where a character waves

const KIT_CAST = ['boltboy', 'casualman', 'classicnoob', 'wingedboy'] as const;
type KitName = (typeof KIT_CAST)[number];

const CAST: Array<{kind: 'kit'; name: KitName} | {kind: 'r6'; name: PresetName}> = [
  {kind: 'kit', name: 'boltboy'},
  {kind: 'kit', name: 'casualman'},
  {kind: 'kit', name: 'classicnoob'},
  {kind: 'kit', name: 'wingedboy'},
  ...PRESET_NAMES.map((n) => ({kind: 'r6' as const, name: n})),
];

const smoothstep = (a: number, b: number, x: number) => {
  const k = Math.min(1, Math.max(0, (x - a) / (b - a)));
  return k * k * (3 - 2 * k);
};

/** Shortest wrapped angular distance between two angles. */
const angDist = (a: number, b: number) => {
  let d = Math.abs(a - b) % (Math.PI * 2);
  if (d > Math.PI) d = Math.PI * 2 - d;
  return d;
};

const KitCharacter: React.FC<{name: KitName; pose: any; position: V3; rotationY: number}> = ({
  name,
  pose,
  position,
  rotationY,
}) => {
  const rot: V3 = [0, rotationY, 0];
  if (name === 'boltboy') return <BoltBoy pose={pose} position={position} rotation={rot} />;
  if (name === 'casualman') return <CasualMan pose={pose} position={position} rotation={rot} />;
  if (name === 'classicnoob') return <ClassicNoob pose={pose} position={position} rotation={rot} />;
  return <WingedBoy pose={pose} position={position} rotation={rot} />;
};

export const CircleShowcase: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const t = frame / fps;
  const progress = frame / durationInFrames; // 0..1 over the orbit
  const phi = progress * Math.PI * 2; // camera angle

  const camX = (RADIUS + CAM_DIST) * Math.sin(phi);
  const camZ = (RADIUS + CAM_DIST) * Math.cos(phi);
  const cameraPosition: V3 = [camX, CAM_Y, camZ];
  // Look at the point on the circle directly in front of the camera (the
  // featured character when the orbit aligns with one). This moves smoothly
  // around the circle with the camera — no jump between characters.

  const idle = clipPose('idle', t);
  // Offset the wave by 0.5s so the raised arm is already up at t=0 —
  // wavePose ramps the arm up over its first 0.5s, and the showcase should
  // open with the first character already waving.
  const wave = clipPose('wave', t + 0.5);

  return (
    <Stage shadows cameraPosition={cameraPosition} lookAt={[RADIUS * Math.sin(phi), 3, RADIUS * Math.cos(phi)]} fov={30}>
      {CAST.map((entry, i) => {
        const theta = (i / CAST.length) * Math.PI * 2;
        const x = RADIUS * Math.sin(theta);
        const z = RADIUS * Math.cos(theta);
        const position: V3 = [x, 0, z];
        // Face the camera.
        const rotationY = Math.atan2(camX - x, camZ - z);
        // Wave as the camera passes: full wave at the camera's angle,
        // fading to idle WAVE_SPREAD radians either side.
        const d = angDist(theta, phi);
        const w = 1 - smoothstep(0, WAVE_SPREAD, d);
        const pose = lerpPose(idle, wave, w);
        if (entry.kind === 'kit') {
          return <KitCharacter key={entry.name} name={entry.name} pose={pose} position={position} rotationY={rotationY} />;
        }
        return (
          <R6Character
            key={entry.name}
            look={CHARACTER_PRESETS[entry.name]}
            position={position}
            rotationY={rotationY}
            expression="smile"
            pose={pose}
          />
        );
      })}
    </Stage>
  );
};
