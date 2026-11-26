import React, {useMemo} from 'react';
import * as THREE from 'three';
import {RBox, type V3, useCanvasTexture} from '../kit/kit';

/**
 * BlockyBrain.tsx: Deterministic Roblox-style pink rounded-block human brain
 * with clean fold lines, a glowing blue cleansing wash flowing over the right side,
 * and falling glowing droplets.
 * Ported from new-assets/blocky-brain/src/BlockyBrain.tsx.
 * DROPPED: PointingBoy scaffolding (+ useBoyFaceTexture and the boy-only colours
 * skin/hair/shirt/pants/shoe).
 */
export const COLORS = {
  brainPink: '#e07a96',
  brainMid: '#d66a88',
  brainFold: '#c9627e',
  // FIX ROUND 2 (2026-11-23, second pass): the old core was a small dark
  // rose box (#b85a74) that left deep slots between the ridges — the
  // grooves read as a dark grid and the outer gaps showed sky. The core
  // is now a large rounded form in brainMid (only slightly darker than
  // the ridges) that fills every gap, so grooves are shallow pink
  // valleys. brainCore removed; the core below uses brainMid.
  washBlue: '#5bc8eb',
  washGlow: '#36b5e0',
};

const useBrainTexture = () =>
  useCanvasTexture(
    (g, size) => {
      // FIX ROUND 2: the old texture drew 360 small dots (the polka-dot
      // that made the brain read as a waffle) plus a dark border rect
      // that outlined every block. Now smooth only: a soft top-light
      // gradient and a few large, very faint organic blotches — no
      // dots, no hard edges. The folds come from the geometry.
      g.fillStyle = '#ffffff';
      g.fillRect(0, 0, size, size);
      const grad = g.createRadialGradient(size * 0.5, size * 0.32, size * 0.05, size * 0.5, size * 0.5, size * 0.75);
      grad.addColorStop(0, 'rgba(255, 236, 242, 0.35)');
      grad.addColorStop(1, 'rgba(190, 90, 120, 0.18)');
      g.fillStyle = grad;
      g.fillRect(0, 0, size, size);
      for (let i = 0; i < 6; i++) {
        const x = ((i * 37) % 100) / 100 * size;
        const y = ((i * 61) % 100) / 100 * size;
        const r = size * (0.16 + (i % 3) * 0.07);
        const blob = g.createRadialGradient(x, y, 0, x, y, r);
        blob.addColorStop(0, i % 2 === 0 ? 'rgba(255, 228, 236, 0.10)' : 'rgba(175, 72, 102, 0.07)');
        blob.addColorStop(1, 'rgba(255, 255, 255, 0)');
        g.fillStyle = blob;
        g.beginPath();
        g.arc(x, y, r, 0, Math.PI * 2);
        g.fill();
      }
    },
    512
  );

const useBrainBumpTexture = () =>
  useCanvasTexture(
    (g, size) => {
      // FIX ROUND 2: the old bump drew 240 dots. Now smooth wavy
      // horizontal grooves (soft sine bands, low contrast) that follow
      // the gyri rows — no dots, no speckle.
      g.fillStyle = '#808080';
      g.fillRect(0, 0, size, size);
      for (let r = 0; r < 5; r++) {
        const y0 = size * (0.12 + r * 0.19);
        g.beginPath();
        for (let x = 0; x <= size; x += 8) {
          const y = y0 + Math.sin((x / size) * Math.PI * 2 + r * 1.7) * size * 0.03;
          if (x === 0) g.moveTo(x, y);
          else g.lineTo(x, y);
        }
        g.strokeStyle = r % 2 === 0 ? 'rgba(255, 255, 255, 0.20)' : 'rgba(0, 0, 0, 0.20)';
        g.lineWidth = size * 0.045;
        g.stroke();
      }
    },
    512
  );

const HemisphereBlocks: React.FC<{side: 1 | -1; map: THREE.Texture; bumpMap: THREE.Texture}> = ({side, map, bumpMap}) => {
  // FIX ROUND 2 (2026-11-23, third pass): unifying the colour and filling
  // the gaps helped (no more dark slots / see-through bars), but the five
  // PERFECTLY PARALLEL horizontal ridges still read as a stack of bars —
  // real gyri wind, tilt and stagger, they never run in parallel lines.
  // So each row is now tilted (rotation.z, alternating + / -) and the
  // left hemisphere's rows sit 0.14 higher than the right's, so the folds
  // no longer align across the midline into a grid. The ridges stay one
  // pink (brainPink) on the slightly darker brainMid core, so the
  // surface is a single folded mass, not banded bars.
  // Rows: [y, tilt] — tilt in radians about z (in the x-y plane).
  const rows: {y: number; tilt: number; h: number}[] = [
    {y: 1.25, tilt: 0.16, h: 0.65},
    {y: 0.7, tilt: -0.11, h: 0.68},
    {y: 0.1, tilt: 0.07, h: 0.7},
    {y: -0.5, tilt: -0.16, h: 0.68},
    {y: -1.05, tilt: 0.11, h: 0.6},
  ];
  // Left hemisphere rows sit 0.14 higher (brick-stagger across the
  // midline); right hemisphere rows sit at the base y.
  const yOff = side === -1 ? 0.14 : 0;
  const blocks: {pos: V3; size: V3; rot: V3; color: keyof typeof COLORS}[] = [];
  // Per-row z-centres and widths (the ridge winds slightly in z).
  const zSets: {z: number; w: number}[][] = [
    [{z: 0.55, w: 1.15}, {z: -0.5, w: 1.15}],
    [{z: 0.9, w: 1.05}, {z: 0.0, w: 1.05}, {z: -0.9, w: 1.05}],
    [{z: 0.95, w: 1.1}, {z: 0.05, w: 1.1}, {z: -0.85, w: 1.1}],
    [{z: 0.85, w: 1.05}, {z: -0.05, w: 1.05}, {z: -0.95, w: 1.05}],
    [{z: 0.45, w: 1.15}, {z: -0.55, w: 1.15}],
  ];
  const xCentres = [0.85, 0.88, 0.9, 0.88, 0.8];
  const widths = [1.5, 1.55, 1.6, 1.55, 1.45];
  rows.forEach((row, ri) => {
    zSets[ri].forEach((zs, zi) => {
      // Slight x wander per box so no two ridges share an edge line.
      const xWander = ((ri * 2 + zi) % 3 - 1) * 0.08;
      blocks.push({
        pos: [side * (xCentres[ri] + xWander), row.y + yOff, zs.z],
        size: [widths[ri], row.h, zs.w],
        rot: [0, 0, side * row.tilt],
        color: 'brainPink',
      });
    });
  });
  // Bottom tip
  blocks.push({
    pos: [side * 0.7, -1.35 + yOff, 0.0],
    size: [1.2, 0.4, 0.9],
    rot: [0, 0, side * 0.05],
    color: 'brainPink',
  });

  return (
    <group>
      {blocks.map((b, i) => (
        <RBox
          key={i}
          size={b.size}
          color={COLORS[b.color]}
          position={b.pos}
          rotation={b.rot}
          radius={0.22}
          rough={0.58}
          map={map}
          bumpMap={bumpMap}
          bumpScale={0.045}
        />
      ))}
    </group>
  );
};

export const BlockyBrain: React.FC<{
  t?: number;
  duration?: number;
  position?: V3;
  rotation?: V3;
  scale?: number;
}> = ({t = 0, duration = 3, position = [0, 0, 0], rotation = [0, 0, 0], scale = 1}) => {
  const brainTex = useBrainTexture();
  const brainBump = useBrainBumpTexture();
  const ph = (t / duration) * Math.PI * 2;
  const bobY = Math.sin(ph) * 0.1;

  // Deterministic glowing blue wash droplets cascading down the right side
  const droplets = useMemo(
    () =>
      Array.from({length: 24}).map((_, i) => {
        const s1 = Math.sin(i * 19.31) * 43758.5453;
        const r1 = s1 - Math.floor(s1);
        const s2 = Math.sin(i * 53.71) * 43758.5453;
        const r2 = s2 - Math.floor(s2);
        return {
          offset: i / 24,
          x: 0.25 + r1 * 1.45,
          z: (r2 - 0.5) * 1.85,
          size: 0.12 + (i % 3) * 0.06,
        };
      }),
    []
  );

  return (
    <group position={position} rotation={rotation} scale={scale}>
      {/* Floating Pink Blocky Brain */}
      <group position={[0, 0.25 + bobY, 0]}>
        {/* Core: a large rounded form in brainMid (slightly darker than the
            ridges) that fills every gap behind the gyri. The ridges sit
            ~0.15 proud of it, so the grooves are shallow pink valleys
            (fold shadows), never slots to the sky or a dark cross. The
            core's rounded form gives the brain its ovoid body; the ridges
            give it the folded surface. Second pass 2026-11-23: was a
            small [2.25,2.25,2.15] deep-rose box — too small and too dark,
            which is why the first-pass gyri still read as separate bars. */}
        <RBox size={[3.3, 2.9, 2.7]} color={COLORS.brainMid} position={[0, 0.05, 0]} radius={0.8} rough={0.7} />

        {/* Left & Right Hemispheres */}
        <HemisphereBlocks side={-1} map={brainTex} bumpMap={brainBump} />
        <HemisphereBlocks side={1} map={brainTex} bumpMap={brainBump} />

        {/* Small Blocky Brainstem */}
        <RBox size={[0.56, 0.65, 0.56]} color={COLORS.brainFold} position={[0, -1.42, -0.15]} radius={0.1} rough={0.5} />

        {/* Soft Glowing Blue Wash Blanket Over Right Hemisphere */}
        <RBox
          size={[1.45, 2.35, 2.15]}
          color={COLORS.washBlue}
          emissive={COLORS.washGlow}
          emissiveIntensity={0.45}
          position={[0.82, 0.12, 0.05]}
          radius={0.48}
          rough={0.15}
          transparent
          opacity={0.32 + Math.sin(ph) * 0.05}
        />
        <pointLight position={[1.4, 0.3, 1.1]} color={COLORS.washGlow} intensity={1.2} distance={5} />

        {/* Flowing Glowing Blue Blocky Droplets Cascading Down the Right Side */}
        {droplets.map((d, i) => {
          const p = ((t / duration) + d.offset) % 1;
          const y = 1.65 - p * 3.15;
          const fade = p < 0.15 ? p / 0.15 : p > 0.8 ? (1 - p) / 0.2 : 1;
          return (
            <RBox
              key={i}
              size={[d.size, d.size, d.size]}
              color={COLORS.washBlue}
              emissive={COLORS.washGlow}
              emissiveIntensity={0.65}
              position={[d.x + Math.sin(p * Math.PI * 2 + i) * 0.06, y, d.z]}
              radius={0.03}
              rough={0.1}
              transparent
              opacity={0.85 * fade}
            />
          );
        })}
      </group>
    </group>
  );
};
