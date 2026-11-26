import React from 'react';
import { Box } from './kit';
import { ScienceFx } from '../types/schema';
import { ScienceFxMesh } from './fx';
import { HouseVariantId } from '../types/schema';

/**
 * Plain empty studio set for prop close-ups (robot, giant phone):
 * a flat floor, a back wall and side walls, no furniture — the prop is the
 * whole shot. Wall colour follows scene.variant so the backdrop can match
 * the reference: white = light grey, blue = light blue, green = mint,
 * yellow = cream, red = warm grey.
 *
 * Actors stand around x in [-6, 6], z in [-3, 4]; the camera sits on +Z
 * looking toward -Z, as in every other location.
 */
const WALLS: Record<HouseVariantId, { wall: string; floor: string }> = {
  blue: { wall: '#BFDBFE', floor: '#DBEAFE' },
  yellow: { wall: '#FEF3C7', floor: '#FFFBEB' },
  red: { wall: '#E7E5E4', floor: '#F5F5F4' },
  white: { wall: '#E5E7EB', floor: '#F1F5F9' },
  green: { wall: '#D1FAE5', floor: '#ECFDF5' },
};

export const StudioEnvironment: React.FC<{ variant?: HouseVariantId; fx?: ScienceFx[] }> = ({ variant = 'white', fx }) => {
  const { wall, floor } = WALLS[variant];
  return (
    <group>
      {/* flat floor */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 2]} receiveShadow>
        <planeGeometry args={[80, 60]} />
        <meshStandardMaterial color={floor} roughness={0.85} />
      </mesh>
      {/* back wall + side walls */}
      <Box p={[0, 12, -8.4]} s={[40, 24, 0.8]} c={wall} rough={0.85} />
      {[-1, 1].map((s) => (
        <Box key={s} p={[s * 13.4, 12, 1]} s={[0.8, 24, 18]} c={wall} rough={0.85} />
      ))}
      {/* ceiling, so shots looking up never see the void */}
      <Box p={[0, 24.3, -1]} s={[28, 0.6, 16]} c="#F1F5F9" />

      {fx?.map((f) => (
        <ScienceFxMesh key={f.id} fx={f} />
      ))}
    </group>
  );
};
