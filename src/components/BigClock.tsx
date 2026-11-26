import React, {useMemo} from 'react';
import {RBox, type V3, useCanvasTexture} from '../kit/kit';

/**
 * BigClock.tsx: Deterministic Roblox-style blocky wall clock with bold black numbers,
 * stepped blocky rim, two thick spinning black hands, and a center hub.
 * Ported from new-assets/big-clock/src/BigClock.tsx.
 * DROPPED: plain light-grey wall & floor, LookingBoy scaffolding
 * (and the boy-only colours skin/hair/shirt/pants/shoe).
 */
export const COLORS = {
  rim: '#2d3942',
  dial: '#f4f6f8',
  hand: '#16191e',
};

const useClockDialTexture = () =>
  useCanvasTexture((g, size) => {
    const c = size / 2;
    g.fillStyle = COLORS.dial;
    g.beginPath();
    g.arc(c, c, c, 0, Math.PI * 2);
    g.fill();

    // Subtle concentric motion lines around the center
    g.strokeStyle = 'rgba(130, 142, 155, 0.28)';
    g.lineWidth = 4;
    [155, 195, 225].forEach((r) => {
      g.beginPath();
      g.arc(c, c, r, 0.2, Math.PI * 1.65);
      g.stroke();
    });

    // Bold black numbers 1..12
    g.fillStyle = '#15181c';
    g.font = '900 102px sans-serif';
    g.textAlign = 'center';
    g.textBaseline = 'middle';
    const numR = size * 0.365;
    for (let n = 1; n <= 12; n++) {
      const ang = (n / 12) * Math.PI * 2 - Math.PI / 2;
      const x = c + Math.cos(ang) * numR;
      const y = c + Math.sin(ang) * numR;
      g.fillText(String(n), x, y);
    }
  }, 1024);

const SteppedClockRim: React.FC = () => {
  const blocks = useMemo(() => {
    const arr: V3[] = [];
    const count = 40;
    const R = 2.18;
    for (let i = 0; i < count; i++) {
      const a = (i / count) * Math.PI * 2;
      const gx = Math.round(Math.cos(a) * R * 5) / 5;
      const gy = Math.round(Math.sin(a) * R * 5) / 5;
      if (!arr.some(([px, py]) => Math.abs(px - gx) < 0.05 && Math.abs(py - gy) < 0.05)) {
        arr.push([gx, gy, 0.14]);
      }
    }
    return arr;
  }, []);

  return (
    <group>
      {blocks.map(([x, y, z], i) => (
        <RBox key={i} size={[0.38, 0.38, 0.42]} color={COLORS.rim} position={[x, y, z]} radius={0.03} rough={0.6} />
      ))}
    </group>
  );
};

export const BigClock: React.FC<{
  t?: number;
  duration?: number;
  position?: V3;
  rotation?: V3;
  scale?: number;
}> = ({t = 0, duration = 3, position = [0, 0, 0], rotation = [0, 0, 0], scale = 1}) => {
  const dialTex = useClockDialTexture();
  const ph = (t / duration) * Math.PI * 2;

  // Seamless clockwise spinning hands: minute hand 2 turns, hour hand 1 turn per 3s loop
  const minuteRot = -ph * 2;
  const hourRot = -ph;

  return (
    <group position={position} rotation={rotation} scale={scale}>
      {/* Big Blocky Wall Clock (dial center kept at its source offset [-0.1, 0.45, -0.15]) */}
      <group position={[-0.1, 0.45, -0.15]}>
        {/* White Dial Cylinder */}
        <mesh rotation={[Math.PI / 2, 0, 0]} castShadow receiveShadow>
          <cylinderGeometry args={[2.12, 2.12, 0.24, 48]} />
          <meshStandardMaterial color={COLORS.dial} roughness={0.65} />
        </mesh>
        {/* Crisp Numbers Face */}
        <mesh position={[0, 0, 0.13]}>
          <circleGeometry args={[2.06, 48]} />
          <meshStandardMaterial map={dialTex} roughness={0.6} />
        </mesh>

        {/* Stepped Blocky Rim */}
        <SteppedClockRim />

        {/* Hour Hand (shorter, thick) */}
        <group position={[0, 0, 0.22]} rotation={[0, 0, hourRot]}>
          <RBox size={[0.22, 1.08, 0.08]} color={COLORS.hand} position={[0, 0.42, 0]} radius={0.02} rough={0.4} />
        </group>

        {/* Minute Hand (longer, thick) */}
        <group position={[0, 0, 0.31]} rotation={[0, 0, minuteRot]}>
          <RBox size={[0.18, 1.55, 0.08]} color={COLORS.hand} position={[0, 0.64, 0]} radius={0.02} rough={0.4} />
        </group>

        {/* Center Hub */}
        <RBox size={[0.36, 0.36, 0.18]} color={COLORS.hand} position={[0, 0, 0.32]} radius={0.06} rough={0.35} />
      </group>
    </group>
  );
};
