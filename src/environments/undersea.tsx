import React, { useMemo } from 'react';
import { Box, Facet, studTex, V3 } from './kit';
import { ScienceFx } from '../types/schema';
import { ScienceFxMesh } from './fx';

/**
 * Seabed for "How does the internet travel under the sea?" (Gemini undersea
 * reference): sandy floor with light patches (the reference's caustics,
 * simplified — no true caustic texture, just lighter sand), light rays from
 * above, green seaweed, grey rocks, and the black fibre-optic cable snaking
 * across the floor in an S-curve. Standalone environment (not the town map):
 * fx render inside it directly, in stage space — the same arrangement as
 * BeachEnvironment / SpaceEnvironment.
 *
 * The cable is a chain of short boxes following the S-curve (not one smooth
 * tube): the joints read as segments, which matches the reference's segmented
 * cable. Actors stand on the sand around x in [-6, 6], z in [-3, 4].
 * Scenes should set skyColor '#1D6FB8' (ocean blue).
 */

interface CableSeg {
  key: number;
  p: V3;
  ry: number;
  c: string;
}

interface Patch {
  key: number;
  p: V3;
  s: V3;
  op: number;
}

interface Blade {
  key: number;
  p: V3;
  s: V3;
  c: string;
}

const GREENS = ['#16A34A', '#22C55E', '#15803D', '#4ADE80'];

export const UnderseaEnvironment: React.FC<{ fx?: ScienceFx[] }> = ({ fx }) => {
  const sand = studTex('#DEC088', '#BFA05E', 60, 60);

  // Cable: S-curve from foreground-left [-24, 10] to background-right
  // [24, -12], 26 overlapping boxes rotated to the curve tangent.
  const cable = useMemo<CableSeg[]>(() => {
    const out: CableSeg[] = [];
    const N = 26;
    for (let i = 0; i < N; i++) {
      const t = (i + 0.5) / N;
      const x = -24 + 48 * t;
      const z = 6 - 22 * t + 8 * Math.sin(t * Math.PI * 2.2);
      const dx = 48;
      const dz = -22 + 8 * 2.2 * Math.PI * Math.cos(t * Math.PI * 2.2);
      out.push({
        key: i,
        p: [x, 0.6, z],
        ry: Math.atan2(dx, dz),
        c: i % 2 === 0 ? '#0F172A' : '#1E293B',
      });
    }
    return out;
  }, []);

  // Light patches on the sand (simplified caustics) + seaweed blades,
  // both seeded so they are identical every frame and render.
  const { patches, blades } = useMemo(() => {
    let seed = 20261117;
    const rnd = () => {
      seed = (seed * 16807) % 2147483647;
      return (seed - 1) / 2147483646;
    };
    const patches: Patch[] = Array.from({ length: 10 }, (_, i) => ({
      key: i,
      p: [-20 + rnd() * 40, 0.05, -12 + rnd() * 20],
      s: [5 + rnd() * 3, 0.08, 4 + rnd() * 2],
      op: 0.6 + rnd() * 0.15,
    }));
    const clusters: V3[] = [
      [-14, 0, 2],
      [-12, 0, -7],
      [13, 0, 3],
      [15, 0, -5],
    ];
    const blades: Blade[] = [];
    clusters.forEach((c, ci) => {
      for (let j = 0; j < 6; j++) {
        const h = 2.5 + rnd() * 3.5;
        blades.push({
          key: ci * 10 + j,
          p: [c[0] + (rnd() - 0.5) * 3, h / 2, c[2] + (rnd() - 0.5) * 2.5],
          s: [0.7 + rnd() * 0.4, h, 0.7 + rnd() * 0.4],
          c: GREENS[Math.floor(rnd() * GREENS.length)],
        });
      }
    });
    return { patches, blades };
  }, []);

  return (
    <group>
      {/* sandy baseplate */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[260, 260]} />
        <meshStandardMaterial map={sand} roughness={0.9} />
      </mesh>

      {/* light patches — simplified caustics */}
      {patches.map((p) => (
        <Box key={p.key} p={p.p} s={p.s} c="#FFF7D6" e="#FDE68A" ei={0.3} rough={0.9} opacity={p.op} />
      ))}

      {/* light rays from the surface, slanting from upper-right */}
      {[-14, -9, -4, 1, 6, 11].map((x, i) => (
        <Box
          key={i}
          p={[x, 15, -10]}
          s={[2.2, 30, 0.5]}
          r={[0, 0, -0.3]}
          c="#BFDBFE"
          e="#DBEAFE"
          ei={0.6}
          rough={0.4}
          opacity={0.22 + (i % 3) * 0.06}
        />
      ))}

      {/* the cable, snaking across the sand */}
      {cable.map((s) => (
        <Box key={s.key} p={s.p} s={[1.6, 1.4, 3.2]} r={[0, s.ry, 0]} c={s.c} rough={0.35} />
      ))}

      {/* seaweed clusters at the sides, clear of the stage */}
      {blades.map((b) => (
        <Box key={b.key} p={b.p} s={b.s} c={b.c} rough={0.8} />
      ))}

      {/* grey rocks at the sand's edge */}
      <Facet p={[-10, 0.4, -8]} rad={1.0} detail={0} c="#64748B" r={[0.3, 0.8, 0.1]} rough={0.95} />
      <Facet p={[11, 0.3, -10]} rad={0.8} detail={0} c="#475569" r={[0.2, 0.4, 0.9]} rough={0.95} />

      {fx?.map((f) => (
        <ScienceFxMesh key={f.id} fx={f} />
      ))}
    </group>
  );
};
