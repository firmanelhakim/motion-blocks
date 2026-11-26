import * as THREE from 'three';
import { interpolate } from 'remotion';
import { CameraShot } from '../types/schema';

export interface CameraState {
  position: [number, number, number];
  target: [number, number, number];
  fov: number;
}

/**
 * Pure camera math, shared by the 3D CameraRig (which applies it to the
 * real camera) and the 2D HUD (which needs the same camera to project a
 * character's head position onto the screen for chat bubbles). One source
 * of truth so the two can never drift apart.
 *
 * Replicates CameraRig exactly: straight lerp between from/to, or a
 * true-circle orbit when the shot has an `arc`, plus the per-frame shake.
 */
export function cameraStateForFrame(shots: CameraShot[], frame: number): CameraState {
  if (!shots || shots.length === 0) {
    throw new Error(
      'cameraStateForFrame: scene has no camera shots (cameraShots is missing or empty) — a scene needs at least one shot to place the camera.'
    );
  }
  const activeShot =
    shots.find((s) => frame >= s.startFrame && frame <= s.endFrame) ||
    shots[shots.length - 1];

  const progress = interpolate(
    frame,
    [activeShot.startFrame, Math.max(activeShot.startFrame + 1, activeShot.endFrame)],
    [0, 1],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  const shakeAmp = activeShot.shake ?? 0;
  const shakeX = shakeAmp ? Math.sin(frame * 1.9) * shakeAmp : 0;
  const shakeY = shakeAmp ? Math.cos(frame * 2.3) * shakeAmp : 0;

  const arc = activeShot.arc;
  const arcAngle = arc ? THREE.MathUtils.lerp(arc.startAngle, arc.endAngle, progress) : 0;
  const camX = arc
    ? arc.center[0] + arc.radius * Math.sin(arcAngle) + shakeX
    : THREE.MathUtils.lerp(activeShot.fromPos[0], activeShot.toPos[0], progress) + shakeX;
  const camY = arc
    ? arc.height + shakeY
    : THREE.MathUtils.lerp(activeShot.fromPos[1], activeShot.toPos[1], progress) + shakeY;
  const camZ = arc
    ? arc.center[2] + arc.radius * Math.cos(arcAngle)
    : THREE.MathUtils.lerp(activeShot.fromPos[2], activeShot.toPos[2], progress);

  const targetX = THREE.MathUtils.lerp(activeShot.fromTarget[0], activeShot.toTarget[0], progress);
  const targetY = THREE.MathUtils.lerp(activeShot.fromTarget[1], activeShot.toTarget[1], progress);
  const targetZ = THREE.MathUtils.lerp(activeShot.fromTarget[2], activeShot.toTarget[2], progress);

  return {
    position: [camX, camY, camZ],
    target: [targetX, targetY, targetZ],
    fov: activeShot.fov ?? 46,
  };
}

/**
 * Projects a world-space point onto screen pixels (origin top-left).
 * Returns null when the point is behind the camera.
 */
export function projectToScreen(
  worldPos: [number, number, number],
  cameraState: CameraState,
  width: number,
  height: number
): { x: number; y: number } | null {
  const camera = new THREE.PerspectiveCamera(cameraState.fov, width / height, 0.1, 500);
  camera.position.set(cameraState.position[0], cameraState.position[1], cameraState.position[2]);
  camera.lookAt(cameraState.target[0], cameraState.target[1], cameraState.target[2]);
  camera.updateMatrixWorld();

  const v = new THREE.Vector3(worldPos[0], worldPos[1], worldPos[2]).project(camera);
  if (v.z > 1) return null; // behind the camera

  return {
    x: ((v.x + 1) / 2) * width,
    y: ((1 - v.y) / 2) * height,
  };
}
