/**
 * KitPoseLab — the engine's clip-library demo: BoltBoy running every clip
 * in sequence on the kit timeline, with the engine's ground shadow.
 *
 * Timeline (23.2s, 696 frames @ 30fps):
 *   walk 2s → run 2s → wave 2s → jump 1.2s → dance 2s
 *   → sprint 2s → march 2s → cheer 2s → punch 2s → bow 2s → kick 2s
 *   → turntable 2s (idle pose + RootMotion spin).
 * The label shows the current clip. The character file is untouched — the
 * Scene picks the clip, the clip returns a Pose, the character applies it.
 */
import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {Stage, timelinePose, TimelineSegment} from './kit/kit';
import {BoltBoy} from './components/BoltBoy';

export const KIT_POSE_LAB_SEGMENTS: TimelineSegment[] = [
  {clip: 'walk', duration: 2},
  {clip: 'run', duration: 2},
  {clip: 'wave', duration: 2},
  {clip: 'jump', duration: 1.2},
  {clip: 'dance', duration: 2},
  {clip: 'sprint', duration: 2},
  {clip: 'march', duration: 2},
  {clip: 'cheer', duration: 2},
  {clip: 'punch', duration: 2},
  {clip: 'bow', duration: 2},
  {clip: 'kick', duration: 2},
  {clip: 'idle', duration: 2, root: 'spin', rootDuration: 2},
];

const LABEL: React.CSSProperties = {
  position: 'absolute',
  bottom: 28,
  left: 40,
  fontFamily: 'Inter, sans-serif',
  fontSize: 22,
  fontWeight: 700,
  color: '#475569',
  letterSpacing: 1,
};

/** Kick segment runs t 19.2–21.2. The camera swings to the side profile
 * for the kick (same angle as KickCheck: [14, 4, 0] / [0, 3, 0]) so the
 * raised thigh never crosses in front of the shirt — from the front 3/4
 * it covers the pocket area (frames 582/612/636 in v9). 0.5s smoothstep
 * in and out; the kick itself is unchanged. (2026-11-21, the maintainer kept.) */
const KICK_START = 19.2;
const KICK_END = 21.2;
const CAM_BLEND = 0.5;
const CAM_FRONT: [number, number, number] = [7, 5, 16];
const CAM_SIDE: [number, number, number] = [14, 4, 0];
const LOOK_FRONT: [number, number, number] = [0, 4.2, 0];
const LOOK_SIDE: [number, number, number] = [0, 3, 0];

const smooth = (x: number) => {
  const c = Math.max(0, Math.min(1, x));
  return c * c * (3 - 2 * c);
};

const kickCamBlend = (t: number) =>
  smooth((t - KICK_START) / CAM_BLEND) * (1 - smooth((t - (KICK_END - CAM_BLEND)) / CAM_BLEND));

const lerp3 = (a: [number, number, number], b: [number, number, number], u: number): [number, number, number] => [
  a[0] + (b[0] - a[0]) * u,
  a[1] + (b[1] - a[1]) * u,
  a[2] + (b[2] - a[2]) * u,
];

export const KitPoseLab: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const state = timelinePose(KIT_POSE_LAB_SEGMENTS, t);
  const camU = kickCamBlend(t);
  const cameraPosition = lerp3(CAM_FRONT, CAM_SIDE, camU);
  const lookAt = lerp3(LOOK_FRONT, LOOK_SIDE, camU);
  return (
    <AbsoluteFill>
      {/* Camera pulled back and raised so the jump peak (head ~8.6) stays
          in frame: default camera tops out at ~7.5, cutting the head at the
          jump peak. See jumpPose — height 1.5 fits this framing. */}
      <Stage shadows cameraPosition={cameraPosition} lookAt={lookAt}>
        <group rotation={[0, state.root.yaw, 0]} position={[0, state.root.y, 0]} scale={[state.root.scaleXZ, state.root.scaleY, state.root.scaleXZ]}>
          <BoltBoy pose={state.pose} />
        </group>
      </Stage>
      <div style={LABEL}>KIT POSE LAB · {state.clip.toUpperCase()}</div>
    </AbsoluteFill>
  );
};
