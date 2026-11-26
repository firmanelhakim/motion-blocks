import React, {useMemo} from 'react';
import * as THREE from 'three';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {RBox, useCanvasTexture, type V3} from '../kit/kit';
import {ScienceFx} from '../types/schema';
import {ScienceFxMesh} from './fx';

/**
 * Ice street (ported from new-assets/ice-street SlipperyStreet.tsx):
 * deterministic Roblox-style 3D icy town street for the no-friction topic —
 * procedural ice road texture + bump map, planar mirror reflection layer of
 * the houses/trees/lamps beneath the semi-transparent ice, frozen sidewalks
 * with stepped snowbanks, lamps, houses, pine trees, blocky clouds.
 *
 * Standalone environment (not the town map): fx render inside it directly,
 * in stage space — the same arrangement as UnderseaEnvironment /
 * DrySeabedEnvironment. Actors stand on the ice around x in [-6, 6],
 * z in [-3, 4]; the road runs along Z from z ≈ 16 down to z ≈ -30.
 * Scenes should set skyColor '#BFDBFE' (pale icy blue).
 *
 * The SlidingBoy demo figure from the source is NOT part of the location —
 * the story cast supplies actors. It is exported separately (below) for the
 * still check only.
 */
export const COLORS = {
  ice: '#8ecae8',
  iceUnder: '#72b0d4',
  skidLine: '#edf7fd',
  sidewalk: '#bfd6e6',
  curb: '#8ea9be',
  snow: '#e4f1fa',
  snowMid: '#c4deef',
  snowShadow: '#9bc0d9',
  cloud: '#e6f2fa',
  houseYellow: '#d6cf8b',
  houseGreen: '#6da182',
  houseRed: '#c6555c',
  houseBlue: '#6595c7',
  houseTan: '#c8b694',
  roofTrim: '#8b99a8',
  chimney: '#7b6258',
  door: '#6a5248',
  windowFrame: '#4a535e',
  windowGlass: '#688ea8',
  pine: '#2d5e47',
  trunk: '#6a5042',
  lampPost: '#8a99a8',
  lampGlow: '#eef7ff',
  smoke: '#dfeef8',
  skin: '#f1c29b',
  hair: '#5a3b25',
  beanieBlue: '#2b6cb0',
  beanieRed: '#d62839',
  pomPom: '#6e4e3a',
  jacket: '#d62839',
  jacketDark: '#9e1b28',
  collar: '#a4c639',
  cuff: '#e8c547',
  glove: '#3a4048',
  pants: '#1e73d8',
  shoe: '#2c3038',
  shoeSole: '#8a95a5',
};

const useIceTexture = () =>
  useCanvasTexture(
    (g, size) => {
      const grad = g.createLinearGradient(0, 0, size, 0);
      grad.addColorStop(0, '#7cb8da');
      grad.addColorStop(0.12, '#99d1ed');
      grad.addColorStop(0.5, '#b8e2f6');
      grad.addColorStop(0.88, '#99d1ed');
      grad.addColorStop(1, '#7cb8da');
      g.fillStyle = grad;
      g.fillRect(0, 0, size, size);

      // Longitudinal icy polish streaks & frost patches
      for (let i = 0; i < 60; i++) {
        const x = ((i * 73) % 100) / 100 * size;
        const y = ((i * 37) % 100) / 100 * size;
        const w = 14 + (i % 5) * 10;
        const h = 140 + (i % 7) * 55;
        g.fillStyle = i % 2 === 0 ? 'rgba(235, 248, 255, 0.22)' : 'rgba(110, 172, 210, 0.16)';
        g.fillRect(x, y, w, h);
      }

      // Fine white skate / ice scratches
      g.strokeStyle = 'rgba(245, 252, 255, 0.5)';
      for (let i = 0; i < 42; i++) {
        g.lineWidth = 1.5 + (i % 3);
        const x1 = ((i * 97) % 92 + 4) / 100 * size;
        const y1 = ((i * 53) % 100) / 100 * size;
        const cx = x1 + ((i % 2 === 0 ? 1 : -1) * (25 + (i % 4) * 18));
        const y2 = y1 + 110 + (i % 5) * 35;
        g.beginPath();
        g.moveTo(x1, y1);
        g.quadraticCurveTo(cx, (y1 + y2) / 2, x1 + (i % 3 - 1) * 20, y2);
        g.stroke();
      }
    },
    1024,
    [1, 6]
  );

const useIceBumpTexture = () =>
  useCanvasTexture(
    (g, size) => {
      g.fillStyle = '#808080';
      g.fillRect(0, 0, size, size);
      for (let i = 0; i < 90; i++) {
        const x = ((i * 67) % 100) / 100 * size;
        const y = ((i * 41) % 100) / 100 * size;
        g.strokeStyle = i % 2 === 0 ? '#b8b8b8' : '#585858';
        g.lineWidth = 2 + (i % 3);
        g.beginPath();
        g.moveTo(x, y);
        g.lineTo(x + (i % 5 - 2) * 12, y + 90 + (i % 4) * 40);
        g.stroke();
      }
    },
    512,
    [1, 6]
  );

const useWorriedFaceTexture = () =>
  useCanvasTexture((g) => {
    g.strokeStyle = '#3b2416';
    g.lineWidth = 10;
    g.beginPath();
    g.moveTo(128, 165);
    g.quadraticCurveTo(168, 148, 206, 128);
    g.stroke();
    g.beginPath();
    g.moveTo(384, 165);
    g.quadraticCurveTo(344, 148, 306, 128);
    g.stroke();

    for (const x of [175, 337]) {
      g.fillStyle = '#141418';
      g.beginPath();
      g.ellipse(x, 222, 16, 29, 0, 0, Math.PI * 2);
      g.fill();
      g.fillStyle = '#ffffff';
      g.beginPath();
      g.arc(x - 4, 208, 6, 0, Math.PI * 2);
      g.fill();
    }

    g.beginPath();
    g.moveTo(175, 375);
    g.quadraticCurveTo(256, 362, 337, 375);
    g.quadraticCurveTo(318, 302, 256, 300);
    g.quadraticCurveTo(194, 302, 175, 375);
    g.closePath();
    g.fillStyle = '#16161c';
    g.fill();
    g.fillStyle = '#ffffff';
    g.fillRect(212, 355, 88, 14);
  });

const SkidLines: React.FC = () => {
  const curves = useMemo(() => {
    const ptsList: [number, number][][] = [
      [[-2.2, 12.5], [-1.3, 9.2], [-0.2, 6.2], [0.8, 3.8], [1.2, 1.5]],
      [[-0.9, 13.0], [-0.4, 9.5], [0.2, 6.5], [0.9, 4.2], [1.9, 2.2]],
      [[2.4, 12.2], [1.5, 9.0], [0.5, 6.0], [-0.6, 3.5], [-1.8, 1.8]],
      [[0.9, 13.2], [0.5, 9.8], [0.0, 6.8], [-0.9, 4.5], [-2.1, 2.9]],
      [[-2.0, 5.2], [-1.2, 4.0], [0.2, 3.3], [1.6, 3.8]],
      [[-1.6, 0.5], [-0.8, -3.5], [0.4, -8.5], [0.9, -14.0]],
      [[1.5, -1.5], [0.9, -6.0], [-0.3, -11.5], [-1.0, -18.0]],
    ];
    return ptsList.map((pts) => {
      const curve = new THREE.CatmullRomCurve3(pts.map(([x, z]) => new THREE.Vector3(x, 0.015, z)));
      return new THREE.TubeGeometry(curve, 28, 0.032, 4, false);
    });
  }, []);

  return (
    <group>
      {curves.map((geo, i) => (
        <mesh key={i} geometry={geo} scale={[1, 0.18, 1]}>
          <meshStandardMaterial color={COLORS.skidLine} roughness={0.18} transparent opacity={0.88} />
        </mesh>
      ))}
    </group>
  );
};

const BlockHouse: React.FC<{
  position: V3;
  rotationY?: number;
  wallColor: string;
  width?: number;
  height?: number;
  depth?: number;
  t?: number;
  duration?: number;
  smokePhase?: number;
  isReflection?: boolean;
}> = ({
  position,
  rotationY = 0,
  wallColor,
  width = 4.2,
  height = 3.4,
  depth = 4.6,
  t = 0,
  duration = 3,
  smokePhase = 0,
  isReflection = false,
}) => {
  const gableGeo = useMemo(() => {
    const s = new THREE.Shape();
    s.moveTo(-width / 2, 0);
    s.lineTo(width / 2, 0);
    s.lineTo(0, 1.75);
    s.closePath();
    return new THREE.ExtrudeGeometry(s, {depth, bevelEnabled: false});
  }, [width, depth]);

  const roofSlope = Math.atan2(1.75, width / 2);
  const roofHalfLen = Math.hypot(width / 2, 1.75) + 0.35;

  return (
    <group position={position} rotation={[0, rotationY, 0]}>
      <RBox size={[width, height, depth]} color={wallColor} position={[0, height / 2, 0]} radius={0.08} rough={0.72} doubleSide={isReflection} castShadow={!isReflection} />

      <mesh geometry={gableGeo} position={[0, height, -depth / 2]} castShadow={!isReflection} receiveShadow>
        <meshStandardMaterial color={wallColor} roughness={0.72} side={isReflection ? THREE.DoubleSide : THREE.FrontSide} />
      </mesh>

      <RBox
        size={[roofHalfLen, 0.14, depth + 0.46]}
        color={COLORS.snowShadow}
        position={[-width / 4 - 0.05, height + 0.8, 0]}
        rotation={[0, 0, roofSlope]}
        radius={0.04}
        rough={0.65}
        doubleSide={isReflection}
        castShadow={!isReflection}
      />
      <RBox
        size={[roofHalfLen, 0.14, depth + 0.46]}
        color={COLORS.snowShadow}
        position={[width / 4 + 0.05, height + 0.8, 0]}
        rotation={[0, 0, -roofSlope]}
        radius={0.04}
        rough={0.65}
        doubleSide={isReflection}
        castShadow={!isReflection}
      />

      <RBox
        size={[roofHalfLen, 0.24, depth + 0.52]}
        color={COLORS.snow}
        position={[-width / 4 - 0.05, height + 0.96, 0]}
        rotation={[0, 0, roofSlope]}
        radius={0.06}
        rough={0.55}
        doubleSide={isReflection}
        castShadow={!isReflection}
      />
      <RBox
        size={[roofHalfLen, 0.24, depth + 0.52]}
        color={COLORS.snow}
        position={[width / 4 + 0.05, height + 0.96, 0]}
        rotation={[0, 0, -roofSlope]}
        radius={0.06}
        rough={0.55}
        doubleSide={isReflection}
        castShadow={!isReflection}
      />

      <group position={[width * 0.24, height + 1.15, -depth * 0.18]}>
        <RBox size={[0.68, 1.1, 0.68]} color={COLORS.chimney} radius={0.05} rough={0.8} doubleSide={isReflection} castShadow={!isReflection} />
        <RBox size={[0.78, 0.16, 0.78]} color={COLORS.snow} position={[0, 0.58, 0]} radius={0.04} rough={0.6} doubleSide={isReflection} castShadow={!isReflection} />
        {!isReflection &&
          [0, 0.33, 0.66].map((off, idx) => {
            const p = ((t / duration) + smokePhase + off) % 1;
            const s = 0.28 * (1 - p * 0.45);
            return (
              <RBox
                key={idx}
                size={[s, s, s]}
                color={COLORS.smoke}
                position={[Math.sin(p * Math.PI * 2) * 0.12, 0.85 + p * 1.9, 0]}
                radius={0.04}
                rough={0.9}
              />
            );
          })}
      </group>

      <RBox size={[0.82, 1.45, 0.14]} color={COLORS.door} position={[0, 0.75, depth / 2 + 0.03]} radius={0.04} rough={0.75} doubleSide={isReflection} castShadow={!isReflection} />

      {[
        [-1.15, 1.15],
        [1.15, 1.15],
        [-1.1, 2.55],
        [1.1, 2.55],
      ].map(([wx, wy], i) => (
        <group key={i} position={[wx, wy, depth / 2 + 0.03]}>
          <RBox size={[0.76, 0.76, 0.1]} color={COLORS.windowFrame} radius={0.03} rough={0.65} doubleSide={isReflection} castShadow={!isReflection} />
          <RBox size={[0.56, 0.56, 0.12]} color={COLORS.windowGlass} radius={0.02} rough={0.25} doubleSide={isReflection} castShadow={!isReflection} />
        </group>
      ))}
    </group>
  );
};

const PineTree: React.FC<{position: V3; scale?: number; isReflection?: boolean}> = ({position, scale = 1, isReflection = false}) => (
  <group position={position} scale={scale}>
    <RBox size={[0.45, 1.3, 0.45]} color={COLORS.trunk} position={[0, 0.65, 0]} radius={0.05} rough={0.85} doubleSide={isReflection} castShadow={!isReflection} />
    {[
      {y: 1.45, w: 2.0, h: 0.7},
      {y: 2.2, w: 1.55, h: 0.68},
      {y: 2.9, w: 1.05, h: 0.65},
      {y: 3.5, w: 0.55, h: 0.55},
    ].map((tier, i) => (
      <group key={i} position={[0, tier.y, 0]}>
        <RBox size={[tier.w, tier.h, tier.w]} color={COLORS.pine} radius={0.06} rough={0.8} doubleSide={isReflection} castShadow={!isReflection} />
        <RBox size={[tier.w * 0.98, 0.1, tier.w * 0.98]} color={COLORS.snowShadow} position={[0, tier.h / 2 + 0.01, 0]} radius={0.03} rough={0.65} doubleSide={isReflection} castShadow={!isReflection} />
        <RBox size={[tier.w * 0.94, 0.14, tier.w * 0.94]} color={COLORS.snow} position={[0, tier.h / 2 + 0.09, 0]} radius={0.04} rough={0.55} doubleSide={isReflection} castShadow={!isReflection} />
      </group>
    ))}
  </group>
);

const StreetLamp: React.FC<{position: V3; side: 1 | -1; isReflection?: boolean}> = ({position, side, isReflection = false}) => (
  <group position={position}>
    <RBox size={[0.2, 3.9, 0.2]} color={COLORS.lampPost} position={[0, 1.95, 0]} radius={0.03} rough={0.5} doubleSide={isReflection} castShadow={!isReflection} />
    <RBox size={[0.95, 0.16, 0.18]} color={COLORS.lampPost} position={[-side * 0.42, 3.88, 0]} radius={0.03} rough={0.5} doubleSide={isReflection} castShadow={!isReflection} />
    <RBox
      size={[0.38, 0.12, 0.24]}
      color={COLORS.lampGlow}
      position={[-side * 0.72, 3.76, 0]}
      radius={0.02}
      rough={0.2}
      emissive={COLORS.lampGlow}
      emissiveIntensity={0.6}
      doubleSide={isReflection}
      castShadow={false}
    />
  </group>
);

const BlockCloud: React.FC<{position: V3; scale?: number}> = ({position, scale = 1}) => (
  <group position={position} scale={scale}>
    <RBox size={[3.2, 0.75, 1.2]} color={COLORS.cloud} position={[0, 0, 0]} radius={0.08} rough={0.9} />
    <RBox size={[1.8, 0.65, 1.1]} color={COLORS.cloud} position={[-0.2, 0.55, 0]} radius={0.08} rough={0.9} />
    <RBox size={[1.2, 0.45, 1.0]} color={COLORS.cloud} position={[1.1, -0.1, 0]} radius={0.08} rough={0.9} />
  </group>
);

/**
 * The source scene's demo figure: a blocky boy sliding on the ice (tilt,
 * flailing arms, worried face). Exported for the still check only — the
 * IceStreetEnvironment location render below does NOT include him.
 */
export const SlidingBoy: React.FC<{t?: number; duration?: number; isReflection?: boolean}> = ({t = 0, duration = 3, isReflection = false}) => {
  const face = useWorriedFaceTexture();
  const ph = (t / duration) * Math.PI * 2;

  const slideX = Math.sin(ph) * 0.38;
  const slideZ = 4.6 + Math.cos(ph) * 0.24;
  const tiltZ = 0.26 + Math.sin(ph) * 0.1;
  const tiltX = -0.14 + Math.cos(ph * 2) * 0.04;
  const leftArmZ = 2.05 + Math.sin(ph * 2) * 0.35;
  const rightArmZ = -2.15 - Math.sin(ph * 2 + 0.7) * 0.35;
  const leftLegX = -0.58 - Math.sin(ph * 2) * 0.18;
  const rightLegX = -0.18 + Math.sin(ph * 2) * 0.14;

  return (
    <group position={[slideX, 0.16, slideZ]} rotation={[tiltX, 0.14, tiltZ]} scale={0.44}>
      <group position={[0.52, 2.3, 0]} rotation={[rightLegX, 0, -0.08]}>
        <RBox size={[0.96, 1.8, 1.0]} color={COLORS.pants} position={[0, -0.9, 0]} radius={0.08} rough={0.65} doubleSide={isReflection} castShadow={!isReflection} />
        <RBox size={[1.02, 0.48, 1.15]} color={COLORS.shoe} position={[0, -1.95, 0.08]} radius={0.08} rough={0.5} doubleSide={isReflection} castShadow={!isReflection} />
        <RBox size={[1.04, 0.16, 1.2]} color={COLORS.shoeSole} position={[0, -2.22, 0.08]} radius={0.05} rough={0.6} doubleSide={isReflection} castShadow={!isReflection} />
      </group>

      <group position={[-0.52, 2.3, 0]} rotation={[leftLegX, 0, 0.24]}>
        <RBox size={[0.96, 1.8, 1.0]} color={COLORS.pants} position={[0, -0.9, 0]} radius={0.08} rough={0.65} doubleSide={isReflection} castShadow={!isReflection} />
        <RBox size={[1.02, 0.48, 1.15]} color={COLORS.shoe} position={[0, -1.95, 0.08]} radius={0.08} rough={0.5} doubleSide={isReflection} castShadow={!isReflection} />
        <RBox size={[1.04, 0.16, 1.2]} color={COLORS.shoeSole} position={[0, -2.22, 0.08]} radius={0.05} rough={0.6} doubleSide={isReflection} castShadow={!isReflection} />
      </group>

      <group rotation={[0.05, Math.sin(ph) * 0.08, 0]}>
        <RBox size={[2.05, 2.0, 1.08]} color={COLORS.jacket} position={[0, 3.3, 0]} radius={0.14} rough={0.65} doubleSide={isReflection} castShadow={!isReflection} />
        <RBox size={[0.1, 1.9, 0.06]} color={COLORS.jacketDark} position={[0, 3.3, 0.55]} radius={0.02} doubleSide={isReflection} castShadow={!isReflection} />
        <RBox size={[1.55, 0.28, 1.16]} color={COLORS.collar} position={[0, 4.28, 0]} radius={0.08} rough={0.7} doubleSide={isReflection} castShadow={!isReflection} />
        <RBox size={[0.72, 0.28, 0.72]} color={COLORS.skin} position={[0, 4.44, 0]} radius={0.06} rough={0.55} doubleSide={isReflection} castShadow={!isReflection} />

        <group position={[-1.48, 4.15, 0]} rotation={[Math.cos(ph * 2) * 0.28, 0, leftArmZ]}>
          <RBox size={[0.94, 1.48, 0.94]} color={COLORS.jacket} position={[0, -0.74, 0]} radius={0.14} rough={0.65} doubleSide={isReflection} castShadow={!isReflection} />
          <RBox size={[1.0, 0.2, 1.0]} color={COLORS.cuff} position={[0, -1.42, 0]} radius={0.05} rough={0.65} doubleSide={isReflection} castShadow={!isReflection} />
          <RBox size={[0.88, 0.56, 0.88]} color={COLORS.glove} position={[0, -1.8, 0]} radius={0.08} rough={0.6} doubleSide={isReflection} castShadow={!isReflection} />
        </group>

        <group position={[1.48, 4.15, 0]} rotation={[-Math.cos(ph * 2) * 0.28, 0, rightArmZ]}>
          <RBox size={[0.94, 1.48, 0.94]} color={COLORS.jacket} position={[0, -0.74, 0]} radius={0.14} rough={0.65} doubleSide={isReflection} castShadow={!isReflection} />
          <RBox size={[1.0, 0.2, 1.0]} color={COLORS.cuff} position={[0, -1.42, 0]} radius={0.05} rough={0.65} doubleSide={isReflection} castShadow={!isReflection} />
          <RBox size={[0.88, 0.56, 0.88]} color={COLORS.glove} position={[0, -1.8, 0]} radius={0.08} rough={0.6} doubleSide={isReflection} castShadow={!isReflection} />
        </group>

        <group position={[0, 5.18, 0]} rotation={[0.08, Math.sin(ph) * 0.1, 0]}>
          <RBox size={[1.4, 1.44, 1.4]} color={COLORS.skin} radius={0.2} rough={0.55} doubleSide={isReflection} castShadow={!isReflection} />
          <mesh position={[0, -0.04, 0.706]}>
            <planeGeometry args={[1.3, 1.3]} />
            <meshStandardMaterial map={face} transparent roughness={0.6} side={isReflection ? THREE.DoubleSide : THREE.FrontSide} />
          </mesh>
          <RBox size={[1.46, 0.26, 0.35]} color={COLORS.hair} position={[0, 0.52, -0.58]} radius={0.06} rough={0.85} doubleSide={isReflection} castShadow={!isReflection} />
          <RBox size={[1.52, 0.26, 1.52]} color={COLORS.beanieRed} position={[0, 0.62, 0]} radius={0.1} rough={0.8} doubleSide={isReflection} castShadow={!isReflection} />
          <RBox size={[1.46, 0.45, 1.46]} color={COLORS.beanieBlue} position={[0, 0.9, 0]} radius={0.16} rough={0.8} doubleSide={isReflection} castShadow={!isReflection} />
          <RBox size={[0.42, 0.36, 0.42]} color={COLORS.pomPom} position={[0, 1.24, 0]} radius={0.14} rough={0.85} doubleSide={isReflection} castShadow={!isReflection} />
        </group>
      </group>
    </group>
  );
};

const ReflectedContent: React.FC<{t: number; duration: number; isReflection?: boolean; includeBoy?: boolean}> = ({t, duration, isReflection = false, includeBoy = true}) => (
  <group>
    <BlockHouse position={[-8.8, 0.25, -2.5]} rotationY={Math.PI / 2} wallColor={COLORS.houseYellow} t={t} duration={duration} smokePhase={0.1} isReflection={isReflection} />
    <BlockHouse position={[-8.8, 0.25, -11.5]} rotationY={Math.PI / 2} wallColor={COLORS.houseBlue} width={3.8} height={3.2} t={t} duration={duration} smokePhase={0.45} isReflection={isReflection} />
    <BlockHouse position={[-8.8, 0.25, -19.5]} rotationY={Math.PI / 2} wallColor={COLORS.houseRed} width={4.0} height={3.3} t={t} duration={duration} smokePhase={0.75} isReflection={isReflection} />

    <BlockHouse position={[8.8, 0.25, 2.0]} rotationY={-Math.PI / 2} wallColor={COLORS.houseRed} width={4.0} height={3.2} t={t} duration={duration} smokePhase={0.2} isReflection={isReflection} />
    <BlockHouse position={[8.8, 0.25, -6.5]} rotationY={-Math.PI / 2} wallColor={COLORS.houseGreen} width={4.2} height={3.5} t={t} duration={duration} smokePhase={0.55} isReflection={isReflection} />
    <BlockHouse position={[8.8, 0.25, -15.5]} rotationY={-Math.PI / 2} wallColor={COLORS.houseBlue} width={3.9} height={3.3} t={t} duration={duration} smokePhase={0.85} isReflection={isReflection} />

    <BlockHouse position={[-2.9, 0.2, -26.5]} rotationY={0} wallColor={COLORS.houseGreen} width={3.8} height={3.1} depth={3.8} t={t} duration={duration} smokePhase={0.3} isReflection={isReflection} />
    <BlockHouse position={[2.9, 0.2, -26.5]} rotationY={0} wallColor={COLORS.houseTan} width={3.8} height={3.1} depth={3.8} t={t} duration={duration} smokePhase={0.7} isReflection={isReflection} />

    <PineTree position={[-6.4, 0.2, 3.6]} scale={0.95} isReflection={isReflection} />
    <PineTree position={[6.5, 0.2, -11.0]} scale={0.9} isReflection={isReflection} />
    <PineTree position={[-6.4, 0.2, -15.5]} scale={0.85} isReflection={isReflection} />
    <PineTree position={[0.0, 0.15, -24.5]} scale={0.85} isReflection={isReflection} />

    <StreetLamp position={[-3.85, 0.18, -5.5]} side={-1} isReflection={isReflection} />
    <StreetLamp position={[3.85, 0.18, -12.5]} side={1} isReflection={isReflection} />
    <StreetLamp position={[-3.85, 0.18, -18.5]} side={-1} isReflection={isReflection} />

    {includeBoy && <SlidingBoy t={t} duration={duration} isReflection={isReflection} />}
  </group>
);

export const IceStreetEnvironment: React.FC<{fx?: ScienceFx[]}> = ({fx}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const t = frame / fps;
  const duration = durationInFrames / fps;
  const ph = (t / duration) * Math.PI * 2;
  const iceTex = useIceTexture();
  const iceBump = useIceBumpTexture();

  return (
    <group>
      {/* Planar Mirror Reflection Layer beneath the semi-transparent ice road */}
      <group position={[0, -0.02, 0]} scale={[1, -1, 1]}>
        <ReflectedContent t={t} duration={duration} isReflection includeBoy={false} />
      </group>

      {/* Textured Glossy Pale-Blue Ice Road */}
      <mesh position={[0, 0, -7]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[7.2, 46]} />
        <meshStandardMaterial
          map={iceTex}
          bumpMap={iceBump}
          bumpScale={0.025}
          roughness={0.06}
          metalness={0.18}
          transparent
          opacity={0.62}
          depthWrite={false}
        />
      </mesh>
      <SkidLines />

      {/* Opaque Sidewalks + Stepped Cool-Blue Snowbanks (naturally frame & mask the reflection) */}
      {[-1, 1].map((sx) => (
        <group key={sx}>
          <RBox size={[2.4, 0.24, 46]} color={COLORS.sidewalk} position={[sx * 4.7, 0.06, -7]} radius={0.04} rough={0.22} metal={0.08} />
          <RBox size={[0.25, 0.28, 46]} color={COLORS.curb} position={[sx * 3.55, 0.07, -7]} radius={0.03} rough={0.4} />
          <RBox size={[3.6, 0.35, 46]} color={COLORS.snowShadow} position={[sx * 7.6, 0.14, -7]} radius={0.06} rough={0.65} />
          <RBox size={[3.2, 0.22, 45]} color={COLORS.snowMid} position={[sx * 7.8, 0.32, -7]} radius={0.05} rough={0.6} />
          <RBox size={[2.2, 0.26, 42]} color={COLORS.snow} position={[sx * 8.4, 0.48, -7]} radius={0.06} rough={0.55} />
        </group>
      ))}

      {/* Main World Geometry (boy excluded: the story cast supplies actors) */}
      <ReflectedContent t={t} duration={duration} includeBoy={false} />

      {/* Blocky Clouds */}
      <BlockCloud position={[-4.2 + Math.sin(ph) * 0.5, 13.5, -22]} scale={1.0} />
      <BlockCloud position={[3.8 + Math.cos(ph) * 0.5, 15.2, -20]} scale={1.25} />

      {fx?.map((f) => (
        <ScienceFxMesh key={f.id} fx={f} />
      ))}
    </group>
  );
};
