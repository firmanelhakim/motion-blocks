import React from 'react';
import {RBox, type V3} from '../kit/kit';

/**
 * BlankMonitor.tsx: a desktop computer monitor on a stand, its screen
 * completely black and blank — the "computer" half of the month-props
 * doc's "phone / computer with a black blank screen" asset for
 * no_internet ("What if the internet disappeared for a day?").
 *
 * The screen is DEAD black on purpose: no emissive, no glow — it must
 * read as a computer with nothing on it. Origin is the screen centre;
 * the whole unit spans y −2.7..+1.5 at scale 1, so place its centre at
 * y ≈ 3.9 to stand it on a student desk (top y ≈ 2.3) at scale 0.6,
 * or y ≈ 2.7 to stand it on the floor at scale 1.
 */
export const BlankMonitor: React.FC<{
  t?: number;
  duration?: number;
  position?: V3;
  rotation?: V3;
  scale?: number;
}> = ({position = [0, 0, 0], rotation = [0, 0, 0], scale = 1}) => {
  return (
    <group position={position} rotation={rotation} scale={scale}>
      {/* Dark bezel */}
      <RBox size={[4.8, 3.0, 0.28]} color="#0F172A" position={[0, 0, 0]} radius={0.06} rough={0.5} />
      {/* Dead-black screen, set just proud of the bezel face */}
      <RBox size={[4.4, 2.6, 0.08]} color="#030303" position={[0, 0, 0.15]} radius={0.03} rough={0.25} />
      {/* Power dot (unlit) */}
      <RBox size={[0.12, 0.12, 0.04]} color="#111827" position={[2.0, -1.35, 0.15]} radius={0.02} rough={0.5} />
      {/* Stand neck */}
      <RBox size={[0.4, 1.1, 0.35]} color="#1F2937" position={[0, -2.0, -0.05]} radius={0.03} rough={0.5} />
      {/* Stand base */}
      <RBox size={[1.8, 0.18, 1.1]} color="#1F2937" position={[0, -2.6, 0.05]} radius={0.03} rough={0.5} />
    </group>
  );
};
