import React, {useMemo} from 'react';
import {type V3} from '../kit/kit';
import {Box} from '../environments/kit';

/**
 * LightningBolt.tsx: Deterministic Roblox-style jagged lightning bolt,
 * built for the lightning Short ("Why do we see
 * lightning before we hear thunder?").
 *
 * Reference: ~/workspace/user/files/1000374699_5_a8gc.jpg — a bright
 * jagged yellow pixel bolt striking from a dark blocky storm cloud down
 * to a wet street. The bolt is a chain of emissive yellow boxes following
 * a fixed zigzag path (main channel + two small side branches), so it
 * reads as blocky pixels, not a smooth line.
 *
 * Flash cycle (seamless 3 s loop, t = frame/fps): a hard strike at the
 * loop start, a quick second flicker, then a low glow — the bolt never
 * goes fully dark, so no frame is ever bolt-less. Emissive intensity is
 * animated every frame, so every Box passes `noPool` (see the leak guard
 * in kit.tsx: pooled materials are keyed on raw emissiveIntensity).
 *
 * Position = the ground strike point; the bolt rises ~19 studs above it.
 * Scale sizes the whole bolt (default 1).
 */
export const COLORS = {
  bolt: '#FEF08A',
  boltCore: '#FEFCE8',
  branch: '#FDE047',
};

type Seg = {
  mid: V3;
  len: number;
  rz: number;
  thick: number;
  core: boolean;
};

/** Fixed zigzag path: [x offset, y] from the strike point upward. */
const PATH: Array<[number, number]> = [
  [0, 0],
  [0.7, 1.6],
  [-0.6, 3.4],
  [0.9, 5.2],
  [-0.9, 7.0],
  [0.5, 8.8],
  [-0.7, 10.6],
  [0.8, 12.4],
  [-0.5, 14.2],
  [0.6, 16.0],
  [-0.4, 17.6],
  [0.2, 19.0],
];

/** Side branches: [startPathIndex, dx, dy, length] — short zigzag spurs. */
const BRANCHES: Array<{from: number; dx: number; dy: number}> = [
  {from: 4, dx: -2.2, dy: 1.4},
  {from: 7, dx: 2.4, dy: 1.2},
];

function segmentsForPath(path: Array<[number, number]>, thick: number): Seg[] {
  const segs: Seg[] = [];
  for (let i = 0; i < path.length - 1; i++) {
    const [x0, y0] = path[i];
    const [x1, y1] = path[i + 1];
    const dx = x1 - x0;
    const dy = y1 - y0;
    const len = Math.hypot(dx, dy);
    segs.push({
      mid: [(x0 + x1) / 2, (y0 + y1) / 2, 0],
      len: len + thick * 0.9, // overlap the joints so no gaps at the kinks
      rz: Math.atan2(dx, dy),
      thick,
      core: true,
    });
  }
  return segs;
}

export const LightningBolt: React.FC<{
  t?: number;
  duration?: number;
  position?: V3;
  rotation?: V3;
  scale?: number;
}> = ({t = 0, duration = 3, position = [0, 0, 0], rotation = [0, 0, 0], scale = 1}) => {
  const segs = useMemo(() => {
    const main = segmentsForPath(PATH, 0.55);
    const branchSegs: Seg[] = [];
    for (const b of BRANCHES) {
      const [bx, by] = PATH[b.from];
      const tip: [number, number] = [bx + b.dx, by + b.dy];
      const mid: [number, number] = [(bx + tip[0]) / 2, (by + tip[1]) / 2];
      const dx = tip[0] - bx;
      const dy = tip[1] - by;
      branchSegs.push({
        mid: [mid[0], mid[1], 0],
        len: Math.hypot(dx, dy) + 0.3,
        rz: Math.atan2(dx, dy),
        thick: 0.3,
        core: false,
      });
    }
    return [...main, ...branchSegs];
  }, []);

  // Flash envelope over one 3 s loop: hard strike, second flicker, low glow.
  const phase = ((t % duration) + duration) % duration / duration;
  const strike = Math.exp(-phase * 14);
  const flicker = 0.75 * Math.exp(-Math.abs(phase - 0.16) * 30);
  const glow = 0.22;
  const env = Math.min(1, strike + flicker + glow);
  const ei = 0.7 + 3.4 * env;

  return (
    <group position={position} rotation={rotation} scale={scale}>
      {segs.map((s, i) => (
        <React.Fragment key={i}>
          {/* Outer glow slab */}
          <Box
            p={s.mid}
            s={[s.thick * 1.7, s.len, s.thick * 1.7]}
            r={[0, 0, s.rz]}
            c={COLORS.branch}
            e={COLORS.branch}
            ei={ei * 0.55}
            rough={0.4}
            opacity={0.55}
            noPool
          />
          {/* Bright core */}
          <Box
            p={s.mid}
            s={[s.thick, s.len, s.thick]}
            r={[0, 0, s.rz]}
            c={s.core ? COLORS.boltCore : COLORS.bolt}
            e={COLORS.bolt}
            ei={ei}
            rough={0.3}
            noPool
          />
        </React.Fragment>
      ))}
    </group>
  );
};
