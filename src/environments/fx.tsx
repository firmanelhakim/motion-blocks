import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { ScienceFx } from '../types/schema';
import { Ball, Box, Crescent, Dome, Facet, Ring, V3 } from './kit';
import { BlockyFish } from '../components/BlockyFish';
import { BubblesUnderwater } from '../components/BubblesUnderwater';
import { BlockyBrain } from '../components/BlockyBrain';
import { BigClock } from '../components/BigClock';
import { BlueSun } from '../components/BlueSun';
import { BlueLightPlant } from '../components/BlueLightPlant';
import { GiantFerns } from '../components/GiantFerns';
import { BlockyVolcano } from '../components/BlockyVolcano';
import { BlankPhone } from '../components/BlankPhone';
import { BlankMonitor } from '../components/BlankMonitor';
import { LightningBolt } from '../components/LightningBolt';
import { Rainfall } from '../components/Rainfall';
import { BlockyRobot } from '../components/BlockyRobot';

/** Linear interpolation of an fx prop's position at a frame (clamped at the ends). */
export function fxPositionAt(fx: ScienceFx, frame: number): V3 {
  const kfs = fx.keyframes;
  if (kfs.length === 0) return [0, 0, 0];
  if (frame <= kfs[0].frame) return kfs[0].position;
  if (frame >= kfs[kfs.length - 1].frame) return kfs[kfs.length - 1].position;
  for (let i = 0; i < kfs.length - 1; i++) {
    const a = kfs[i];
    const b = kfs[i + 1];
    if (frame >= a.frame && frame <= b.frame) {
      const t = (frame - a.frame) / Math.max(1, b.frame - a.frame);
      return [
        a.position[0] + (b.position[0] - a.position[0]) * t,
        a.position[1] + (b.position[1] - a.position[1]) * t,
        a.position[2] + (b.position[2] - a.position[2]) * t,
      ];
    }
  }
  return kfs[0].position;
}

/** Renders one animated science prop at the current frame.
 * Ported-asset shapes (2026-11-22): full components whose
 * animation is a seamless 3s loop, so t = frame/fps with duration 3.
 * Scale comes from fx.scale, falling back to fx.radius (default 1) —
 * a radius on a ported shape acts as its uniform scale. */
export const ScienceFxMesh: React.FC<{ fx: ScienceFx }> = ({ fx }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = fxPositionAt(fx, frame);
  const t = frame / fps;
  const scale = fx.scale ?? fx.radius ?? 1;
  const rotation = fx.rotation ?? [0, 0, 0];
  if (fx.shape === 'fish') {
    return <BlockyFish t={t} duration={3} position={p} rotation={rotation} scale={scale} />;
  }
  if (fx.shape === 'bubbles') {
    return <BubblesUnderwater t={t} duration={3} position={p} rotation={rotation} scale={scale} />;
  }
  if (fx.shape === 'brain') {
    return <BlockyBrain t={t} duration={3} position={p} rotation={rotation} scale={scale} />;
  }
  if (fx.shape === 'clock') {
    return <BigClock t={t} duration={3} position={p} rotation={rotation} scale={scale} />;
  }
  if (fx.shape === 'blue-sun') {
    return <BlueSun t={t} duration={3} position={p} rotation={rotation} scale={scale} />;
  }
  if (fx.shape === 'plant') {
    return <BlueLightPlant t={t} duration={3} position={p} rotation={rotation} scale={scale} />;
  }
  if (fx.shape === 'ferns') {
    return <GiantFerns t={t} duration={3} position={p} rotation={rotation} scale={scale} />;
  }
  if (fx.shape === 'volcano') {
    return <BlockyVolcano t={t} duration={3} position={p} rotation={rotation} scale={scale} />;
  }
  if (fx.shape === 'blank-phone') {
    return <BlankPhone t={t} duration={3} position={p} rotation={rotation} scale={scale} />;
  }
  if (fx.shape === 'blank-monitor') {
    return <BlankMonitor t={t} duration={3} position={p} rotation={rotation} scale={scale} />;
  }
  if (fx.shape === 'robot') {
    return <BlockyRobot t={t} duration={3} position={p} rotation={rotation} scale={scale} />;
  }
  if (fx.shape === 'lightning') {
    return <LightningBolt t={t} duration={3} position={p} rotation={rotation} scale={scale} />;
  }
  if (fx.shape === 'rain') {
    return <Rainfall t={t} duration={3} position={p} rotation={rotation} scale={scale} />;
  }
  if (fx.shape === 'box') {
    return (
      <Box
        p={p}
        s={fx.size ?? [2, 2, 2]}
        r={fx.rotation}
        c={fx.color}
        e={fx.emissive}
        ei={fx.emissiveIntensity ?? 1}
        rough={fx.roughness ?? 0.6}
        opacity={fx.opacity}
      />
    );
  }
  if (fx.shape === 'facet') {
    return (
      <Facet
        p={p}
        rad={fx.radius ?? 2}
        detail={fx.detail ?? 1}
        c={fx.color}
        r={fx.rotation}
        e={fx.emissive}
        ei={fx.emissiveIntensity ?? 1}
        rough={fx.roughness ?? 0.6}
        opacity={fx.opacity}
      />
    );
  }
  if (fx.shape === 'ring') {
    return (
      <Ring
        p={p}
        rad={fx.radius ?? 2}
        tube={fx.tube}
        c={fx.color}
        e={fx.emissive}
        ei={fx.emissiveIntensity ?? 1}
        rough={fx.roughness ?? 0.5}
        arc={fx.arc}
        r={fx.rotation}
      />
    );
  }
  if (fx.shape === 'dome') {
    return (
      <Dome
        p={p}
        rad={fx.radius ?? 2}
        c={fx.color}
        r={fx.rotation}
        e={fx.emissive}
        ei={fx.emissiveIntensity ?? 1}
        rough={fx.roughness ?? 0.5}
        opacity={fx.opacity}
      />
    );
  }
  if (fx.shape === 'crescent') {
    return (
      <Crescent
        p={p}
        rad={fx.radius ?? 2}
        c={fx.color}
        r={fx.rotation}
        e={fx.emissive}
        ei={fx.emissiveIntensity ?? 1}
        rough={fx.roughness ?? 0.5}
        opacity={fx.opacity}
      />
    );
  }
  // Default shape is the Ball: 'sphere' has no branch of its own and
  // renders as a Ball by design. Anything else reaching here is an unknown
  // shape (a typo in generated story data) — say so loudly instead of
  // silently rendering the wrong prop.
  if (fx.shape !== 'sphere') {
    console.warn(`ScienceFxMesh: unknown fx shape "${fx.shape}" — rendering as Ball (sphere).`);
  }
  return (
    <Ball
      p={p}
      rad={fx.radius ?? 2}
      c={fx.color}
      e={fx.emissive}
      ei={fx.emissiveIntensity ?? 1}
      rough={fx.roughness ?? 0.6}
      opacity={fx.opacity}
    />
  );
};
