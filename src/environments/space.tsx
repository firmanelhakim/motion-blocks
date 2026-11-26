import React, { useMemo } from 'react';
import { useCurrentFrame } from 'remotion';
import { Ball, Box, V3 } from './kit';
import { ScienceFx } from '../types/schema';
import { ScienceFxMesh } from './fx';

/**
 * Minimal space void for black_hole: a dark floor for actors to stand on,
 * a deterministic starfield, and a small blue Earth far behind the stage.
 * Standalone environment (not the town map): fx render inside it directly,
 * in stage space — the same arrangement as ClassroomEnvironment.
 * Scenes should set skyColor '#000000' (the default night sky is dark blue,
 * space is black). Stars sit within the exterior fog range (55–190) so they
 * stay visible.
 */
export const SpaceEnvironment: React.FC<{ fx?: ScienceFx[] }> = ({ fx }) => {
  const frame = useCurrentFrame();
  // Deterministic starfield: seeded LCG, same stars every frame and render.
  const stars = useMemo(() => {
    let seed = 20261117;
    const rnd = () => {
      seed = (seed * 16807) % 2147483647;
      return (seed - 1) / 2147483646;
    };
    return Array.from({ length: 70 }, (_, i) => {
      const p: V3 = [-45 + rnd() * 90, 6 + rnd() * 38, -52 + rnd() * 44];
      const rad = 0.12 + rnd() * 0.2;
      const tint = rnd();
      const c = tint < 0.7 ? '#F8FAFC' : tint < 0.85 ? '#BFDBFE' : '#FDE68A';
      const ph = rnd() * Math.PI * 2; // seeded twinkle phase per star
      return { key: i, p, rad, c, ph };
    });
  }, []);

  return (
    <group>
      {/* dark floor so actors have something to stand on — pure black
          (was #111827) so it vanishes against the black sky: at #111827
          it read as a navy band across the bottom of every space shot
          (half_gravity moon-drifts, 2026-11-23). Actors standing on it
          still read — they are lit, the floor is not. */}
      <Box p={[0, -0.15, 0]} s={[140, 0.3, 140]} c="#000000" rough={0.95} />

      {/* starfield — each star twinkles gently on its own seeded phase: a slow
          sine of frame + phase, so it is deterministic and reads as a twinkle,
          never a flicker (no jumps, no per-frame randomness). */}
      {stars.map((s) => {
        // Twinkle: each star fades in/out on its own seeded phase — opacity,
        // not emissiveIntensity, because the strong scene lighting washes out
        // any emissive change (diagnostic: ei 0.05 still rendered at 229).
        // Opacity 0.25–1.0 against the black sky is unmistakable, and the
        // slow sine (period ~52 frames) reads as a twinkle, never a flicker.
        const tw = 0.25 + 0.75 * (0.5 + 0.5 * Math.sin(frame * 0.12 + s.ph));
        return <Ball key={s.key} p={s.p} rad={s.rad} c={s.c} e={s.c} ei={1.4} rough={0.4} opacity={tw} />;
      })}

      {/* Earth, small and far behind the stage: the home the hero fell from */}
      <Ball p={[-22, 24, -48]} rad={2.6} c="#38BDF8" e="#1D4ED8" ei={0.5} rough={0.7} />
      <Ball p={[-21.2, 24.8, -45.6]} rad={0.9} c="#22C55E" rough={0.8} />

      {fx?.map((f) => (
        <ScienceFxMesh key={f.id} fx={f} />
      ))}
    </group>
  );
};
