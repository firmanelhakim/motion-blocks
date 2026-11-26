import React from 'react';
import {RBox} from '../kit/kit';

/**
 * Gills accessory (ported from new-assets/boy-gills UnderwaterBoy.tsx):
 * 6 thin pink slits, 3 per side, on the lower cheek/neck.
 *
 * Adapted from the source to the R6 head (see src/components/R6Character.tsx
 * buildBeveledHeadGeometry: lathe cylinder, radius 0.62, height 1.15,
 * bevel 0.16 — straight cylindrical band y in [-0.415, +0.415] at full
 * radius; face toward +Z; accessories render in head-center space).
 *
 * Source (flat 1.45-wide cube head, half-width 0.725): gill groups at
 * x = +/-0.74, y = -0.32, z = -0.05; slits 0.08 x 0.08 x 0.68 with
 * y-offsets -0.16 / 0 / +0.16.
 *
 * R6 adaptation (scaled by head size, 0.62/0.725 = 0.855 in x/z and
 * 0.575/0.725 = 0.79 in y): groups at x = +/-0.63, y = -0.25, z = -0.03;
 * slits 0.07 x 0.07 x 0.52 with y-offsets -0.13 / 0 / +0.13 (slit ys
 * -0.38 / -0.25 / -0.12 — all inside the straight band, so every slit
 * sits over the full-radius surface). Slit x-span 0.595–0.665: embedded
 * 0.025 into the surface at the slit centre, proud 0.045.
 *
 * Caveat: the R6 head is a cylinder, not a flat cube face, so a straight
 * slit cannot sit flush along its whole length — the cylinder curves away
 * from the slit ends. Slits were shortened 0.68 -> 0.52 to keep the gap
 * small (max ~0.05 studs at the back tip, ~0.02 at the front tip); the
 * tips hover a hair off the surface instead of touching it.
 */
export const Gills: React.FC<{color?: string}> = ({color = '#F472B6'}) => (
  <>
    {([-1, 1] as const).map((side) => (
      <group key={side} position={[side * 0.63, -0.25, -0.03]}>
        {[-0.13, 0, 0.13].map((gy, gi) => (
          <RBox key={gi} size={[0.07, 0.07, 0.52]} color={color} position={[0, gy, 0]} radius={0.02} rough={0.45} />
        ))}
      </group>
    ))}
  </>
);
