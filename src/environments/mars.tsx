import React from 'react';
import { Ball, Box, Facet, studTex } from './kit';
import { ScienceFx } from '../types/schema';
import { ScienceFxMesh } from './fx';

/**
 * Mars surface for "What if you lived on Mars?", refined to the Gemini
 * reference (terraced red mountains, faceted grey rocks, white astronaut,
 * pale square sun): red desert ground, grey faceted rocks, stepped red
 * mountains under a pale pink-orange sky. Standalone environment (not the
 * town map): fx render inside it directly, in stage space — the same
 * arrangement as BeachEnvironment / SpaceEnvironment.
 * Actors stand on the sand around x ∈ [-6, 6], z ∈ [-3, 4]; the astronaut
 * stands on the right ledge at [7.2, 3, -1] (top of the first step).
 * Scenes should set skyColor '#FDBA74' (pale pink-orange, not the blue
 * default) so the sky reads as Mars, not Earth.
 */

/** Voxel-style stepped pyramid: stacked boxes, each tier smaller than the
 *  last — the terraced mountains of the Mars reference. p = ground centre;
 *  a small offset peak block gives the jagged crest. */
const Terrace: React.FC<{ p: [number, number, number]; base: number; tiers: number; step: number; c: string; c2: string }> = ({
  p,
  base,
  tiers,
  step,
  c,
  c2,
}) => {
  const boxes: React.ReactNode[] = [];
  let w = base;
  for (let i = 0; i < tiers; i++) {
    if (w <= 0) break;
    boxes.push(
      <Box key={i} p={[p[0], p[1] + step / 2 + i * step, p[2]]} s={[w, step, w * 0.85]} c={i % 2 === 0 ? c : c2} />
    );
    w -= step * 2;
  }
  const topY = p[1] + tiers * step;
  const lastW = base - (tiers - 1) * step * 2;
  boxes.push(
    <Box key="peak" p={[p[0] + 2, topY + step / 2, p[2] - 1]} s={[Math.max(4, lastW * 0.5), step, Math.max(4, lastW * 0.4)]} c={c} />
  );
  return <group>{boxes}</group>;
};

export const MarsEnvironment: React.FC<{ fx?: ScienceFx[] }> = ({ fx }) => {
  const sand = studTex('#C2571F', '#8A3B12', 60, 60);
  return (
    <group>
      {/* red desert baseplate */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[260, 260]} />
        <meshStandardMaterial map={sand} roughness={0.95} />
      </mesh>

      {/* terraced red mountains on the horizon (stepped pyramids, spaced
          apart with sky between them — not one flat wall) */}
      <Terrace p={[-28, 0, -100]} base={36} tiers={4} step={5} c="#C2410C" c2="#9A3412" />
      <Terrace p={[26, 0, -110]} base={40} tiers={4} step={6} c="#B45309" c2="#7C2D12" />
      <Terrace p={[2, 0, -125]} base={32} tiers={3} step={6} c="#C2410C" c2="#9A3412" />

      {/* faceted grey rocks: background ones near the horizon, foreground
          ones close to the camera (as in the reference) */}
      <Facet p={[-11, 0.65, -9]} rad={1.3} detail={0} c="#78716C" r={[0.3, 0.8, 0.1]} rough={0.95} />
      <Facet p={[12, 0.45, -10]} rad={0.9} detail={0} c="#57534E" r={[0.2, 0.4, 0.9]} rough={0.95} />
      <Facet p={[-15, 0.35, 3]} rad={0.7} detail={0} c="#78716C" r={[0.9, 0.2, 0.4]} rough={0.95} />
      <Facet p={[15, 0.4, 5]} rad={0.8} detail={0} c="#57534E" r={[0.5, 1.1, 0.3]} rough={0.95} />
      <Facet p={[-8, 0.3, -13]} rad={0.6} detail={0} c="#78716C" r={[0.1, 0.6, 0.2]} rough={0.95} />
      <Facet p={[8, 0.25, -13.5]} rad={0.5} detail={0} c="#57534E" r={[0.7, 0.3, 0.8]} rough={0.95} />
      <Facet p={[-6, 0.45, 6]} rad={0.9} detail={0} c="#78716C" r={[0.4, 0.9, 0.2]} rough={0.95} />
      <Facet p={[4, 0.35, 7]} rad={0.7} detail={0} c="#57534E" r={[0.8, 0.3, 0.6]} rough={0.95} />

      {/* stepped ledge on the right — the astronaut stands on its first tier */}
      <Box p={[8, 1.5, -1]} s={[5, 3, 5]} c="#B45309" />
      <Box p={[9.5, 4, -1.5]} s={[3, 2, 3]} c="#9A3412" />
      {/* low step at the left edge for foreground balance */}
      <Box p={[-7.5, 0.75, 3]} s={[3, 1.5, 4]} c="#B45309" />

      {/* a low dune ridge behind the stage for depth */}
      <Ball p={[-25, -6, -45]} rad={14} c="#A84A1C" rough={0.95} />
      <Ball p={[28, -7, -50]} rad={16} c="#8A3B12" rough={0.95} />

      {/* pale square sun high in the sky (glowing box, as in the reference) */}
      <Box p={[18, 38, -60]} s={[5, 5, 0.5]} c="#FEF3C7" e="#FDE68A" ei={2.5} rough={0.4} />

      {fx?.map((f) => (
        <ScienceFxMesh key={f.id} fx={f} />
      ))}
    </group>
  );
};
