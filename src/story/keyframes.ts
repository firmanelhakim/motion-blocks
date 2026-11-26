import * as THREE from 'three';
import { CharacterKeyframe } from '../types/schema';

/**
 * Shortest-path (wrap-aware) lerp for angles in radians: +3.0 -> -3.0
 * turns ~16 deg through PI, not ~344 deg the long way around. Plain lerp
 * on rotationY spun characters nearly a full turn on such keyframes.
 */
export function lerpAngle(a: number, b: number, t: number): number {
  let d = (b - a) % (Math.PI * 2);
  if (d > Math.PI) d -= Math.PI * 2;
  if (d < -Math.PI) d += Math.PI * 2;
  return a + d * t;
}

/**
 * Frame at which the character's current `anim` began — the start of the
 * run of consecutive keyframes carrying that anim. One-shot clips (wave,
 * jump) play from this frame so they start at their beginning even when
 * the keyframe begins mid-story; cyclic clips ignore it and stay on
 * global time so they never restart at a keyframe boundary.
 */
export function animStartFrame(keyframes: CharacterKeyframe[], frame: number): number {
  if (keyframes.length === 0) return frame;
  if (frame <= keyframes[0].frame) return keyframes[0].frame;
  const last = keyframes[keyframes.length - 1];
  if (frame >= last.frame) {
    let i = keyframes.length - 1;
    while (i > 0 && keyframes[i - 1].anim === last.anim) i--;
    return keyframes[i].frame;
  }
  for (let i = 0; i < keyframes.length - 1; i++) {
    if (frame >= keyframes[i].frame && frame <= keyframes[i + 1].frame) {
      let j = i;
      while (j > 0 && keyframes[j - 1].anim === keyframes[i].anim) j--;
      return keyframes[j].frame;
    }
  }
  return last.frame;
}

/**
 * Interpolates a character's keyframes at a frame. Position/rotation lerp
 * between the bracketing keyframes; anim/expression/prop/chatBubble come
 * from the earlier keyframe (they are stepwise, not lerped). Shared by the
 * 3D composition (which renders the character) and the 2D HUD (which needs
 * the same position to place a chat bubble above the speaker's head).
 */
export function evaluateCharacterKeyframes(keyframes: CharacterKeyframe[], frame: number): CharacterKeyframe {
  if (keyframes.length === 1 || frame <= keyframes[0].frame) {
    return keyframes[0];
  }
  const last = keyframes[keyframes.length - 1];
  if (frame >= last.frame) {
    return last;
  }

  for (let i = 0; i < keyframes.length - 1; i++) {
    const k0 = keyframes[i];
    const k1 = keyframes[i + 1];
    if (frame >= k0.frame && frame <= k1.frame) {
      const span = Math.max(1, k1.frame - k0.frame);
      const t = (frame - k0.frame) / span;
      return {
        frame,
        position: [
          THREE.MathUtils.lerp(k0.position[0], k1.position[0], t),
          THREE.MathUtils.lerp(k0.position[1], k1.position[1], t),
          THREE.MathUtils.lerp(k0.position[2], k1.position[2], t),
        ],
        rotationY: lerpAngle(k0.rotationY, k1.rotationY, t),
        rotationX: lerpAngle(k0.rotationX ?? 0, k1.rotationX ?? 0, t),
        rotationZ: lerpAngle(k0.rotationZ ?? 0, k1.rotationZ ?? 0, t),
        anim: k0.anim,
        expression: k0.expression,
        prop: k0.prop,
        chatBubble: k0.chatBubble,
        bubbleAnchor: k0.bubbleAnchor,
      };
    }
  }

  return last;
}
