import React from 'react';
import {RBox, type V3} from '../kit/kit';

/**
 * BlankPhone.tsx: a big blocky smartphone standing upright, its screen
 * completely black and blank — the "screens go black" visual for
 * no_internet ("What if the internet disappeared for a day?").
 * Follows the month-props doc prompt 14 (giant phone, blank black screen).
 *
 * The screen is DEAD black on purpose: no emissive, no glow, no reflection
 * stripe — it must read as a screen with nothing on it, next to the
 * bedroom's glowing green monitor and the living room's glowing blue TV.
 * Origin is the phone centre; the phone is ~6 studs tall at scale 1, so
 * place its centre at y ≈ 3.2 to stand it on the floor.
 */
export const BlankPhone: React.FC<{
  t?: number;
  duration?: number;
  position?: V3;
  rotation?: V3;
  scale?: number;
}> = ({position = [0, 0, 0], rotation = [0, 0, 0], scale = 1}) => {
  return (
    <group position={position} rotation={rotation} scale={scale}>
      {/* Charcoal body */}
      <RBox size={[3.4, 6.0, 0.42]} color="#1F2937" position={[0, 0, 0]} radius={0.1} rough={0.45} />
      {/* Dead-black screen, set just proud of the body face */}
      <RBox size={[3.02, 5.5, 0.08]} color="#030303" position={[0, 0.08, 0.2]} radius={0.04} rough={0.25} />
      {/* Earpiece slot (unlit) */}
      <RBox size={[0.9, 0.12, 0.04]} color="#0B0F14" position={[0, 2.62, 0.24]} radius={0.02} rough={0.5} />
      {/* Home indicator bar (unlit) */}
      <RBox size={[1.1, 0.09, 0.04]} color="#111827" position={[0, -2.5, 0.24]} radius={0.02} rough={0.5} />
    </group>
  );
};
