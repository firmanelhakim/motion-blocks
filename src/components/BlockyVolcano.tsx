import React, {useMemo} from 'react';
import {RBox, useCanvasTexture, type V3} from '../kit/kit';

/**
 * BlockyVolcano.tsx — ported from new-assets/volcano.
 * Volcano only: the cone (9 tiers of voxel blocks, ~3.6 tall) + glowing
 * crater pool + smoke wisp.
 * DROPPED (source scene scaffolding): the grass/dirt island, the trees
 * and base rocks, and the drifting clouds (with them went the grass
 * texture and the `ph` camera-drift phase — the smoke runs on t/duration).
 * Already ground-based (layer 0 spans y = 0..0.4), so no re-basing.
 */
export const COLORS = {
  greyDark: '#363a3f',
  greyMid: '#4f555c',
  brownDark: '#423328',
  brownMid: '#5c4838',
  lavaOrange: '#ff6a00',
  lavaBright: '#ffbc24',
  smoke: '#c4cdd6',
  rock: '#6c747d',
};

const useRockTexture = () =>
  useCanvasTexture((g, size) => {
    g.fillStyle = '#ffffff';
    g.fillRect(0, 0, size, size);
    for (let i = 0; i < 280; i++) {
      const x = ((i * 73) % 100) / 100 * size;
      const y = ((i * 41) % 100) / 100 * size;
      g.fillStyle = i % 2 === 0 ? 'rgba(0, 0, 0, 0.16)' : 'rgba(255, 255, 255, 0.1)';
      g.fillRect(x, y, 6 + (i % 4) * 4, 6 + (i % 3) * 4);
    }
    g.strokeStyle = 'rgba(0, 0, 0, 0.28)';
    g.lineWidth = 10;
    g.strokeRect(5, 5, size - 10, size - 10);
  }, 256);

const useRockBumpTexture = () =>
  useCanvasTexture((g, size) => {
    g.fillStyle = '#808080';
    g.fillRect(0, 0, size, size);
    for (let i = 0; i < 240; i++) {
      const x = ((i * 67) % 100) / 100 * size;
      const y = ((i * 53) % 100) / 100 * size;
      g.fillStyle = i % 2 === 0 ? '#b2b2b2' : '#525252';
      g.fillRect(x, y, 8 + (i % 3) * 4, 8 + (i % 3) * 4);
    }
  }, 256);

export const BlockyVolcano: React.FC<{
  t?: number;
  duration?: number;
  position?: V3;
  rotation?: V3;
  scale?: number;
}> = ({t = 0, duration = 3, position = [0, 0, 0], rotation = [0, 0, 0], scale = 1}) => {
  const rockTex = useRockTexture();
  const rockBump = useRockBumpTexture();

  // Strictly non-overlapping voxel cone blocks (exact 0.40 layer height, 0.48 grid pitch)
  const volcanoBlocks = useMemo(() => {
    const blocks: {pos: V3; size: V3; color: string}[] = [];
    const palette = [COLORS.greyDark, COLORS.greyMid, COLORS.brownDark, COLORS.brownMid];
    const tiers = 9;
    const step = 0.48;
    const layerH = 0.4;
    for (let layer = 0; layer < tiers; layer++) {
      const y = layer * layerH + layerH / 2;
      const rOuter = 3.1 - layer * 0.25;
      const rInner = Math.max(0.72, rOuter - 0.56);
      const grid = Math.ceil(rOuter / step);
      for (let gx = -grid; gx <= grid; gx++) {
        for (let gz = -grid; gz <= grid; gz++) {
          const x = gx * step;
          const z = gz * step;
          const dist = Math.hypot(x, z);
          if (dist <= rOuter && dist >= rInner) {
            blocks.push({
              pos: [x, y, z],
              size: [step * 0.96, layerH * 0.98, step * 0.96],
              color: palette[Math.abs(gx * 3 + gz * 5 + layer) & 3],
            });
          }
        }
      }
    }
    return blocks;
  }, []);

  return (
    <group position={position} rotation={rotation} scale={scale}>
      {/* Stacked Dark Grey & Brown Textured Cone Volcano */}
      {volcanoBlocks.map((b, i) => (
        <RBox
          key={i}
          size={b.size}
          color={b.color}
          map={rockTex}
          bumpMap={rockBump}
          bumpScale={0.045}
          position={b.pos}
          radius={0.02}
          rough={0.86}
        />
      ))}

      {/* Glowing Orange Crater Pool cleanly seated inside top rim */}
      <group position={[0, 3.35, 0]}>
        <RBox size={[1.18, 0.16, 1.18]} color={COLORS.lavaOrange} emissive={COLORS.lavaOrange} emissiveIntensity={1.45} radius={0.02} />
        <RBox size={[0.62, 0.08, 0.62]} color={COLORS.lavaBright} emissive={COLORS.lavaBright} emissiveIntensity={1.8} position={[0, 0.12, 0]} radius={0.02} />
        <pointLight position={[0, 0.6, 0]} color={COLORS.lavaOrange} intensity={2.4} distance={5} />
      </group>

      {/* Thin Wisp of Grey Smoke Rising */}
      {Array.from({length: 12}).map((_, i) => {
        const p = ((t / duration) + i / 12) % 1;
        const s = 0.25 * (1 - p * 0.35);
        return (
          <RBox
            key={i}
            size={[s, s, s]}
            color={COLORS.smoke}
            position={[Math.sin(p * Math.PI * 3) * 0.3, 3.85 + p * 3.4, Math.cos(p * Math.PI * 2) * 0.14]}
            radius={0.03}
            rough={0.95}
            transparent
            opacity={0.78 * (1 - p)}
          />
        );
      })}
    </group>
  );
};
