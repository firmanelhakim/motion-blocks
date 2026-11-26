import React, {useMemo} from 'react';
import {type V3} from '../kit/kit';
import {Box} from '../environments/kit';

/**
 * Rainfall.tsx: Deterministic blocky 3D rain — thin slanted streaks
 * falling in a loop over the street, for the lightning Short.
 * Reference: ~/workspace/user/files/1000374699_5_a8gc.jpg
 * (thin rain streaks slanting across a dark storm sky).
 *
 * 90 streaks, each a thin translucent box, falling ~20 studs over one
 * seamless 3 s loop (t = frame/fps, duration 3). Streaks fade in at the
 * top of their fall and out near the ground so none pops in or out.
 * The whole sheet is slanted (rz ~0.16) so the rain reads as wind-blown.
 *
 * Position = centre of the rain sheet at ground level; scale sizes it.
 */
export const COLORS = {
  rain: '#DBEAFE',
};

export const Rainfall: React.FC<{
  t?: number;
  duration?: number;
  position?: V3;
  rotation?: V3;
  scale?: number;
}> = ({t = 0, duration = 3, position = [0, 0, 0], rotation = [0, 0, 0], scale = 1}) => {
  const streaks = useMemo(
    () =>
      Array.from({length: 90}).map((_, i) => {
        const seed1 = Math.sin(i * 12.9898) * 43758.5453;
        const r1 = seed1 - Math.floor(seed1);
        const seed2 = Math.sin(i * 78.233) * 43758.5453;
        const r2 = seed2 - Math.floor(seed2);
        const seed3 = Math.sin(i * 39.425) * 43758.5453;
        const r3 = seed3 - Math.floor(seed3);
        return {
          offset: i / 90,
          baseX: (r1 - 0.5) * 34,
          baseZ: (r2 - 0.5) * 20,
          len: 0.9 + r3 * 0.7,
          slant: 0.14 + r1 * 0.08,
        };
      }),
    []
  );

  return (
    <group position={position} rotation={rotation} scale={scale}>
      {streaks.map((s, i) => {
        const p = ((t / duration) + s.offset) % 1;
        const y = 19 - p * 20;
        const fade = p < 0.06 ? p / 0.06 : p > 0.92 ? (1 - p) / 0.08 : 1;
        return (
          <Box
            key={i}
            p={[s.baseX, y, s.baseZ]}
            s={[0.07, s.len, 0.07]}
            r={[0, 0, s.slant]}
            c={COLORS.rain}
            rough={0.3}
            opacity={0.5 * fade}
          />
        );
      })}
    </group>
  );
};
