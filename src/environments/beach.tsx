import React from 'react';
import { Ball, Box, studTex, V3 } from './kit';
import { RoundTree } from './town/props';
import { ScienceFx } from '../types/schema';
import { ScienceFxMesh } from './fx';

/**
 * Minimal night beach for moon_off: sand shore, sea at the back, foam line.
 * Standalone environment (not the town map): fx render inside it directly,
 * in stage space — the same arrangement as ClassroomEnvironment.
 * Actors stand on the sand around x ∈ [-6, 6], z ∈ [-3, 4]; the sea starts
 * at z ≈ -14, so the shoreline reads behind them.
 */
export const BeachEnvironment: React.FC<{ night?: boolean; fx?: ScienceFx[] }> = ({
  night = false,
  fx,
}) => {
  const sand = studTex('#E8C97A', '#C9A227', 60, 60);
  const seaColor = night ? '#1E3A8A' : '#0EA5E9';
  const seaGlow = night ? '#1D4ED8' : '#0369A1';
  return (
    <group>
      {/* sand baseplate */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[260, 260]} />
        <meshStandardMaterial map={sand} roughness={0.9} />
      </mesh>

      {/* sea: a flat slab from the shoreline back to the horizon */}
      <Box p={[0, 0.28, -38]} s={[260, 0.55, 48]} c={seaColor} e={seaGlow} ei={night ? 0.35 : 0.15} rough={0.25} />
      {/* foam line where the waves meet the sand */}
      <Box p={[0, 0.32, -13.6]} s={[260, 0.12, 0.9]} c="#F8FAFC" e="#E0F2FE" ei={0.25} rough={0.4} />
      {/* a second, fainter foam line further out */}
      <Box p={[0, 0.30, -20]} s={[260, 0.08, 0.6]} c="#E0F2FE" e="#BFDBFE" ei={0.2} rough={0.4} />

      {/* palms / shore trees at the sides, clear of the stage */}
      <RoundTree p={[-13, 0, -6]} scale={1.25} leaf="#16A34A" />
      <RoundTree p={[13, 0, -8]} scale={1.1} leaf="#15803D" />
      <RoundTree p={[-16, 0, 4]} scale={1.0} leaf="#22C55E" />

      {/* rocks at the water's edge */}
      <Ball p={[-9, 0.4, -12.5]} rad={1.1} c="#64748B" rough={0.9} />
      <Ball p={[10, 0.3, -12.8]} rad={0.8} c="#475569" rough={0.9} />

      {/* distant dunes on the horizon */}
      <Ball p={[-70, -14, -70]} rad={32} c="#D9A441" rough={0.95} />
      <Ball p={[60, -16, -80]} rad={38} c="#C9A227" rough={0.95} />

      {fx?.map((f) => (
        <ScienceFxMesh key={f.id} fx={f} />
      ))}
    </group>
  );
};
