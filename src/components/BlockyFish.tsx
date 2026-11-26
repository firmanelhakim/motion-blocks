import React from 'react';
import {RBox, type V3} from '../kit/kit';

/**
 * BlockyFish.tsx: Deterministic blocky 3D clownfish.
 * Facing +z, up +y. Pure function of t and props.
 * Ported from new-assets/blocky-fish/src/BlockyFish.tsx.
 * Standalone prop — no scene scaffolding to drop.
 */
export const COLORS = {
  body: '#df6414',
  bodyAccent: '#b94c0c',
  stripe: '#f4f6f8',
  pupil: '#151a1e',
  highlight: '#ffffff',
  finGroove: '#9e3d08',
};

const Eye: React.FC<{side: 1 | -1}> = ({side}) => (
  <group position={[side * 0.86, 0.12, 0.72]} rotation={[0, side * (Math.PI / 2), 0]}>
    {/* Slight square base pad like reference */}
    <RBox size={[0.66, 0.66, 0.06]} color={COLORS.body} position={[0, 0, 0]} radius={0.03} rough={0.55} />
    {/* White circular sclera */}
    <mesh position={[0, 0, 0.05]} rotation={[Math.PI / 2, 0, 0]} castShadow>
      <cylinderGeometry args={[0.3, 0.3, 0.07, 28]} />
      <meshStandardMaterial color={COLORS.stripe} roughness={0.4} />
    </mesh>
    {/* Big dark pupil */}
    <mesh position={[0, 0, 0.095]} rotation={[Math.PI / 2, 0, 0]}>
      <cylinderGeometry args={[0.19, 0.19, 0.05, 24]} />
      <meshStandardMaterial color={COLORS.pupil} roughness={0.25} />
    </mesh>
    {/* Specular white highlight dot */}
    <mesh position={[side * 0.07, 0.07, 0.125]} rotation={[Math.PI / 2, 0, 0]}>
      <cylinderGeometry args={[0.055, 0.055, 0.02, 16]} />
      <meshStandardMaterial color={COLORS.highlight} roughness={0.1} />
    </mesh>
  </group>
);

export const BlockyFish: React.FC<{
  t?: number;
  duration?: number;
  position?: V3;
  rotation?: V3;
  scale?: number;
}> = ({t = 0, duration = 3, position = [0, 0, 0], rotation = [0, 0, 0], scale = 1}) => {
  const ph = (t / duration) * Math.PI * 2;
  const bobY = Math.sin(ph) * 0.14;
  const pitchX = Math.cos(ph) * 0.05;
  const bodyYaw = Math.sin(ph * 2) * 0.06;
  const tailYaw = Math.sin(ph * 2 - 0.5) * 0.36;
  const finPaddle = Math.sin(ph * 2) * 0.25;
  const finTilt = Math.cos(ph * 2) * 0.12;

  return (
    <group position={position} rotation={rotation} scale={scale}>
      <group position={[0, bobY, 0]} rotation={[pitchX, bodyYaw, 0]}>
        {/* Main Blocky Orange Body */}
        <RBox size={[1.7, 1.55, 2.75]} color={COLORS.body} position={[0, 0.1, 0.15]} radius={0.07} rough={0.55} />

        {/* Two White Wrap-Around Stripes */}
        <RBox size={[1.78, 1.63, 0.36]} color={COLORS.stripe} position={[0, 0.1, 0.05]} radius={0.04} rough={0.45} />
        <RBox size={[1.78, 1.63, 0.36]} color={COLORS.stripe} position={[0, 0.1, -0.78]} radius={0.04} rough={0.45} />

        {/* Small Blocky Mouth on Front (+z) */}
        <RBox size={[0.36, 0.18, 0.16]} color={COLORS.bodyAccent} position={[0, -0.18, 1.55]} radius={0.03} rough={0.6} />

        {/* Big Friendly Eyes */}
        <Eye side={-1} />
        <Eye side={1} />

        {/* Top Dorsal Fin */}
        <RBox size={[0.2, 0.56, 0.72]} color={COLORS.body} position={[0, 1.08, -0.32]} radius={0.04} rough={0.55} />

        {/* Bottom Ventral Fin */}
        <RBox size={[0.2, 0.32, 0.62]} color={COLORS.bodyAccent} position={[0, -0.78, -0.22]} radius={0.04} rough={0.6} />

        {/* Left & Right Pectoral Fins */}
        {([-1, 1] as const).map((side) => (
          <group key={side} position={[side * 0.88, -0.12, 0.15]} rotation={[0, -side * (0.35 + finPaddle), side * finTilt]}>
            <RBox size={[0.56, 0.44, 0.16]} color={COLORS.body} position={[side * 0.25, 0, 0]} radius={0.04} rough={0.55} />
          </group>
        ))}

        {/* Square Tail Fin (pivoting at rear of body) */}
        <group position={[0, 0.08, -1.25]} rotation={[0, tailYaw, 0]}>
          {/* Tail stem */}
          <RBox size={[0.34, 0.76, 0.36]} color={COLORS.bodyAccent} position={[0, 0, -0.16]} radius={0.04} rough={0.55} />
          {/* Square Tail Blade */}
          <RBox size={[0.22, 1.06, 0.86]} color={COLORS.body} position={[0, 0, -0.68]} radius={0.05} rough={0.55} />
          {/* White vertical tail accent stripe */}
          <RBox size={[0.25, 1.04, 0.16]} color={COLORS.stripe} position={[0, 0, -0.96]} radius={0.03} rough={0.45} />
          {/* Subtle fin-ray groove lines */}
          {[-0.22, 0.22].map((gy, idx) => (
            <RBox key={idx} size={[0.24, 0.04, 0.72]} color={COLORS.finGroove} position={[0, gy, -0.66]} radius={0.01} rough={0.6} />
          ))}
        </group>
      </group>
    </group>
  );
};
