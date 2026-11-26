import React from 'react';
import {RBox, type V3} from '../kit/kit';

/**
 * GiantFerns.tsx — ported from new-assets/giant-ferns.
 * Fern cluster only: 3 stems + 6 arching fronds + low ground ferns + rocks.
 * DROPPED (source scene scaffolding): the grass/dirt ground slabs, the
 * soft green daylight rays, the distant jungle silhouettes, and the
 * ScaleBoy figure (with his face texture). Already ground-based (y = 0),
 * so no re-basing was needed.
 */
export const COLORS = {
  rock: '#8f979e',
  rockDark: '#737c85',
  stemDark: '#2f6e2e',
  stemMid: '#4d8c38',
  frondDark: '#3e8732',
  frondMid: '#59ab3d',
  frondLight: '#7ec94b',
};

const FernFrond: React.FC<{
  position: V3;
  rotationY: number;
  tiltX: number;
  length?: number;
  sway: number;
  color: string;
}> = ({position, rotationY, tiltX, length = 7, sway, color}) => (
  <group position={position} rotation={[0, rotationY, 0]}>
    <group rotation={[tiltX + sway, 0, 0]}>
      {Array.from({length}).map((_, i) => {
        const arch = i * 0.14;
        const z = i * 0.42;
        const y = Math.sin(i * 0.15) * 0.12 - i * i * 0.035;
        const leafW = Math.max(0.28, 0.95 - i * 0.09);
        return (
          <group key={i} position={[0, y, z]} rotation={[arch, 0, 0]}>
            {/* Rachis spine */}
            <RBox size={[0.14, 0.12, 0.45]} color={COLORS.stemMid} radius={0.02} />
            {/* Left & Right flat blocky frond blades */}
            <RBox size={[leafW, 0.08, 0.28]} color={color} position={[-(leafW / 2 + 0.08), 0, 0]} rotation={[0, 0.15, -0.08]} radius={0.02} rough={0.65} />
            <RBox size={[leafW, 0.08, 0.28]} color={color} position={[leafW / 2 + 0.08, 0, 0]} rotation={[0, -0.15, 0.08]} radius={0.02} rough={0.65} />
          </group>
        );
      })}
    </group>
  </group>
);

export const GiantFerns: React.FC<{
  t?: number;
  duration?: number;
  position?: V3;
  rotation?: V3;
  scale?: number;
}> = ({t = 0, duration = 3, position = [0, 0, 0], rotation = [0, 0, 0], scale = 1}) => {
  const ph = (t / duration) * Math.PI * 2;

  return (
    <group position={position} rotation={rotation} scale={scale}>
      {/* Giant Clustered Fern Stems & Tall Arching Fronds */}
      <group position={[-0.35, 0, -0.2]}>
        <RBox size={[0.62, 3.2, 0.62]} color={COLORS.stemDark} position={[0, 1.6, 0]} radius={0.04} />
        <RBox size={[0.52, 2.6, 0.52]} color={COLORS.stemMid} position={[0.48, 1.3, 0.28]} rotation={[0.05, 0, -0.08]} radius={0.04} />
        <RBox size={[0.48, 2.2, 0.48]} color={COLORS.stemDark} position={[-0.45, 1.1, -0.25]} rotation={[-0.04, 0, 0.08]} radius={0.04} />

        <FernFrond position={[0, 3.2, 0]} rotationY={0.2} tiltX={-0.65} length={8} sway={Math.sin(ph) * 0.045} color={COLORS.frondMid} />
        <FernFrond position={[0, 3.15, 0]} rotationY={1.45} tiltX={-0.55} length={7} sway={Math.sin(ph + 1.0) * 0.045} color={COLORS.frondLight} />
        <FernFrond position={[0, 3.1, 0]} rotationY={2.7} tiltX={-0.6} length={8} sway={Math.sin(ph + 2.0) * 0.045} color={COLORS.frondDark} />
        <FernFrond position={[0, 3.15, 0]} rotationY={-1.2} tiltX={-0.5} length={7} sway={Math.sin(ph + 3.0) * 0.045} color={COLORS.frondMid} />
        <FernFrond position={[0.52, 2.55, 0.3]} rotationY={0.6} tiltX={-0.4} length={6} sway={Math.sin(ph + 4.0) * 0.045} color={COLORS.frondLight} />
        <FernFrond position={[-0.48, 2.15, -0.25]} rotationY={-2.2} tiltX={-0.45} length={6} sway={Math.sin(ph + 5.0) * 0.045} color={COLORS.frondDark} />
      </group>

      {/* Small Low Ground Ferns */}
      <group position={[0.55, 0.1, 0.65]} scale={0.4}>
        <FernFrond position={[0, 0.2, 0]} rotationY={0.4} tiltX={-0.4} length={4} sway={Math.sin(ph) * 0.05} color={COLORS.frondMid} />
        <FernFrond position={[0, 0.2, 0]} rotationY={2.2} tiltX={-0.45} length={4} sway={Math.sin(ph + 2) * 0.05} color={COLORS.frondLight} />
        <FernFrond position={[0, 0.2, 0]} rotationY={-1.5} tiltX={-0.4} length={4} sway={Math.sin(ph + 4) * 0.05} color={COLORS.frondDark} />
      </group>

      {/* Grey Rocks at the Base */}
      <RBox size={[1.1, 0.85, 0.95]} color={COLORS.rock} position={[-1.05, 0.4, 0.6]} radius={0.05} rough={0.85} />
      <RBox size={[0.72, 0.55, 0.68]} color={COLORS.rockDark} position={[-0.45, 0.25, 1.05]} radius={0.04} rough={0.85} />
      <RBox size={[0.85, 0.62, 0.78]} color={COLORS.rock} position={[0.75, 0.28, -0.75]} radius={0.05} rough={0.85} />
    </group>
  );
};
