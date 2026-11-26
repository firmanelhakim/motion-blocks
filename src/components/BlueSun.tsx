import React from 'react';
import {useCanvasTexture, type V3} from '../kit/kit';

/**
 * Blue sun (ported from new-assets/blue-sun BlueSunScene.tsx — sun only).
 * Glowing saturated-blue sphere (radius 2.1) + radial glow plane + point
 * light, with a gentle pulse driven by t/duration. The source's town,
 * houses, trees and shielding boy are scaffolding and were dropped.
 *
 * The disc must read BLUE, not pale cyan/white: the core and emissive are
 * saturated blues (#2563EB / #1D4ED8) and the emissive intensity is kept
 * low (0.8) so the disc does not wash out to near-white. Sky colour is
 * owned elsewhere and is untouched here.
 *
 * The sun sits at the source's offset [0, 7.2, -13] inside the component,
 * so dropping it at the origin of a scene reproduces the source framing;
 * use `position` to move the whole thing.
 */
export const COLORS = {
  sunCore: '#2563EB',
  sunEmissive: '#1D4ED8',
};

const useSunGlowTexture = () =>
  useCanvasTexture((g, size) => {
    const c = size / 2;
    const grad = g.createRadialGradient(c, c, c * 0.15, c, c, c);
    grad.addColorStop(0, 'rgba(96, 165, 250, 0.9)');
    grad.addColorStop(0.4, 'rgba(37, 99, 235, 0.45)');
    grad.addColorStop(1, 'rgba(30, 64, 175, 0)');
    g.fillStyle = grad;
    g.fillRect(0, 0, size, size);
  });

export const BlueSun: React.FC<{
  t?: number;
  duration?: number;
  position?: V3;
  rotation?: V3;
  scale?: number;
}> = ({t = 0, duration = 3, position = [0, 0, 0], rotation = [0, 0, 0], scale = 1}) => {
  const glowTex = useSunGlowTexture();
  const ph = (t / duration) * Math.PI * 2;
  const sunPulse = 1 + Math.sin(ph) * 0.035;

  return (
    <group position={position} rotation={rotation} scale={scale}>
      {/* Big Glowing Blue Sun High in the Deep Blue Sky */}
      <group position={[0, 7.2, -13]} scale={sunPulse}>
        <mesh>
          <sphereGeometry args={[2.1, 32, 32]} />
          <meshStandardMaterial color={COLORS.sunCore} emissive={COLORS.sunEmissive} emissiveIntensity={0.8} roughness={0.2} />
        </mesh>
        <mesh position={[0, 0, 0.1]}>
          <planeGeometry args={[9.5, 9.5]} />
          <meshBasicMaterial map={glowTex} transparent opacity={0.9} depthWrite={false} />
        </mesh>
        <pointLight color={COLORS.sunEmissive} intensity={3.5} distance={28} />
      </group>
    </group>
  );
};
