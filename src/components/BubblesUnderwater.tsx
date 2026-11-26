import React, {useMemo} from 'react';
import {type V3} from '../kit/kit';

/**
 * BubblesUnderwater.tsx: Deterministic blocky 3D stream of shiny air bubbles
 * rising in a loose column.
 * Ported from new-assets/bubbles/src/BubblesUnderwater.tsx.
 * DROPPED: slanting light rays, sandy seabed (+ sand/caustic textures), seaweed blades
 * (the engine's undersea location already provides those).
 */
export const COLORS = {
  bubble: '#c4efff',
  bubbleHighlight: '#ffffff',
};

export const BubblesUnderwater: React.FC<{
  t?: number;
  duration?: number;
  position?: V3;
  rotation?: V3;
  scale?: number;
}> = ({t = 0, duration = 3, position = [0, 0, 0], rotation = [0, 0, 0], scale = 1}) => {
  // Deterministic loose column of 36 shiny round bubbles
  const bubbles = useMemo(
    () =>
      Array.from({length: 36}).map((_, i) => {
        const seed1 = Math.sin(i * 12.9898) * 43758.5453;
        const r1 = seed1 - Math.floor(seed1);
        const seed2 = Math.sin(i * 78.233) * 43758.5453;
        const r2 = seed2 - Math.floor(seed2);
        const seed3 = Math.sin(i * 39.425) * 43758.5453;
        const r3 = seed3 - Math.floor(seed3);
        return {
          offset: i / 36,
          baseX: (r1 - 0.5) * 1.45,
          baseZ: (r2 - 0.5) * 1.1,
          radius: 0.065 + r3 * 0.145,
          wobbleAmp: 0.1 + r1 * 0.18,
          wobbleFreq: 1 + (i % 3),
        };
      }),
    []
  );

  return (
    <group position={position} rotation={rotation} scale={scale}>
      {/* Rising Loose Column of Shiny Round Bubbles */}
      {bubbles.map((b, i) => {
        const p = ((t / duration) + b.offset) % 1;
        const y = -3.3 + p * 8.4;
        const spread = 0.35 + p * 0.85;
        const x = b.baseX * spread + Math.sin(p * Math.PI * 2 * b.wobbleFreq + i) * b.wobbleAmp;
        const z = b.baseZ * spread + Math.cos(p * Math.PI * 2 + i) * 0.1;
        const fade = p < 0.08 ? p / 0.08 : p > 0.9 ? (1 - p) / 0.1 : 1;

        return (
          <group key={i} position={[x, y, z]}>
            <mesh>
              <sphereGeometry args={[b.radius, 18, 18]} />
              <meshStandardMaterial
                color={COLORS.bubble}
                roughness={0.05}
                metalness={0.2}
                transparent
                opacity={0.72 * fade}
              />
            </mesh>
            {/* Crisp specular highlight dot */}
            <mesh position={[b.radius * 0.35, b.radius * 0.35, b.radius * 0.72]}>
              <sphereGeometry args={[b.radius * 0.24, 8, 8]} />
              <meshBasicMaterial color={COLORS.bubbleHighlight} transparent opacity={0.9 * fade} />
            </mesh>
          </group>
        );
      })}
    </group>
  );
};
