import React from 'react';
import * as THREE from 'three';
import {RBox, type V3, useCanvasTexture} from '../kit/kit';

/**
 * BlockyRobot.tsx — friendly white/blue boxy robot for the
 * "What if robots did all the homework?" Short.
 *
 * Built in code from the Gemini reference
 * ~/workspace/user/files/1000374845_6_aif2.jpg (reference only — the image
 * is never pasted into the video): square white head, dark screen face
 * with two glowing cyan oval eyes, blue ear discs, red-ball antenna on a
 * blue base, blue torso, white arms and legs, blue feet, holding a stack
 * of three books (red, green, blue) in front of the torso.
 *
 * Feet sit at y = 0 (like the plant fx), total height ~6.6 studs; use
 * fx scale ~0.9 next to kid characters (~5.9 studs). Animation is a
 * seamless 3 s loop: gentle bob, head sway, antenna wobble, eye blink,
 * books bob. All deterministic from t.
 */
export const COLORS = {
  white: '#f2f5f8',
  blue: '#2e7de1',
  blueDark: '#1e63c4',
  screen: '#0b1220',
  eye: '#39e6ff',
  eyeGlow: '#19c8f0',
  red: '#e53935',
  grey: '#9aa5b1',
  bookRed: '#e53935',
  bookGreen: '#43a047',
  bookBlue: '#1e88e5',
  pages: '#f5f5f0',
};

const useFaceTexture = () =>
  useCanvasTexture(
    (g, size) => {
      // Very subtle top-light on the white shell so the big flat faces
      // don't read as blank paper: a faint cool gradient, no dots, no
      // hard edges.
      g.fillStyle = '#ffffff';
      g.fillRect(0, 0, size, size);
      const grad = g.createRadialGradient(size * 0.5, size * 0.3, size * 0.05, size * 0.5, size * 0.5, size * 0.8);
      grad.addColorStop(0, 'rgba(255, 255, 255, 0.30)');
      grad.addColorStop(1, 'rgba(120, 140, 170, 0.12)');
      g.fillStyle = grad;
      g.fillRect(0, 0, size, size);
    },
    512
  );

export const BlockyRobot: React.FC<{
  t?: number;
  duration?: number;
  position?: V3;
  rotation?: V3;
  scale?: number;
}> = ({t = 0, duration = 3, position = [0, 0, 0], rotation = [0, 0, 0], scale = 1}) => {
  const shellTex = useFaceTexture();
  const ph = (t / duration) * Math.PI * 2;
  const bobY = Math.sin(ph) * 0.05;
  const headYaw = Math.sin(ph) * 0.06;
  const headTilt = Math.sin(ph + 0.9) * 0.02;
  const antennaSway = Math.sin(ph * 1.3) * 0.08;
  const booksBob = Math.sin(ph + 0.6) * 0.04;
  // Eye blink: one quick dip per 3 s loop (phase 1.2–1.35 s in).
  const blinkPhase = (t % duration) - 1.2;
  const blink = blinkPhase >= 0 && blinkPhase <= 0.15 ? 0.12 : 1;
  const armSway = Math.sin(ph) * 0.02;

  const books: {y: number; color: string}[] = [
    {y: 2.19, color: COLORS.bookBlue},
    {y: 2.51, color: COLORS.bookGreen},
    {y: 2.83, color: COLORS.bookRed},
  ];

  return (
    <group position={position} rotation={rotation} scale={scale}>
      <group position={[0, bobY, 0]}>
        {/* Feet — blue */}
        <RBox size={[0.85, 0.45, 1.15]} color={COLORS.blue} position={[-0.55, 0.225, 0.05]} radius={0.12} rough={0.55} />
        <RBox size={[0.85, 0.45, 1.15]} color={COLORS.blue} position={[0.55, 0.225, 0.05]} radius={0.12} rough={0.55} />
        {/* Legs — white */}
        <RBox size={[0.8, 1.25, 0.8]} color={COLORS.white} position={[-0.55, 1.07, 0]} radius={0.15} rough={0.6} map={shellTex} />
        <RBox size={[0.8, 1.25, 0.8]} color={COLORS.white} position={[0.55, 1.07, 0]} radius={0.15} rough={0.6} map={shellTex} />
        {/* Torso — blue */}
        <RBox size={[2.3, 1.6, 1.45]} color={COLORS.blue} position={[0, 2.5, 0]} radius={0.3} rough={0.55} />
        {/* Chest status light */}
        <RBox
          size={[0.34, 0.34, 0.08]}
          color={COLORS.eye}
          emissive={COLORS.eyeGlow}
          emissiveIntensity={0.9}
          position={[0, 2.95, 0.74]}
          radius={0.12}
          rough={0.2}
        />
        {/* Arms — white, angled forward to hold the books */}
        <group position={[-1.15, 2.9, 0.45]} rotation={[-0.7 + armSway, 0, 0.22]}>
          <RBox size={[0.62, 1.5, 0.62]} color={COLORS.white} position={[0, -0.35, 0]} radius={0.18} rough={0.6} map={shellTex} />
        </group>
        <group position={[1.15, 2.9, 0.45]} rotation={[-0.7 - armSway, 0, -0.22]}>
          <RBox size={[0.62, 1.5, 0.62]} color={COLORS.white} position={[0, -0.35, 0]} radius={0.18} rough={0.6} map={shellTex} />
        </group>
        {/* Hands — blue, resting on the book stack */}
        <RBox size={[0.5, 0.4, 0.5]} color={COLORS.blueDark} position={[-0.78, 2.32, 0.95]} radius={0.14} rough={0.5} />
        <RBox size={[0.5, 0.4, 0.5]} color={COLORS.blueDark} position={[0.78, 2.32, 0.95]} radius={0.14} rough={0.5} />
        {/* Book stack — three books held in front of the torso */}
        <group position={[0, booksBob, 0]}>
          {books.map((b, i) => (
            <group key={i}>
              <RBox size={[1.5, 0.32, 1.05]} color={b.color} position={[0, b.y, 0.95]} radius={0.06} rough={0.55} />
              <RBox size={[1.42, 0.22, 0.98]} color={COLORS.pages} position={[-0.04, b.y, 0.95]} radius={0.03} rough={0.8} />
            </group>
          ))}
        </group>
        {/* Head — white, with dark screen face */}
        <group position={[0, 4.4, 0]} rotation={[0, headYaw, headTilt]}>
          <RBox size={[2.5, 2.15, 2.2]} color={COLORS.white} position={[0, 0, 0]} radius={0.35} rough={0.55} map={shellTex} />
          {/* Screen */}
          <RBox size={[2.1, 1.75, 0.1]} color={COLORS.screen} position={[0, 0, 1.08]} radius={0.25} rough={0.25} />
          {/* Glowing cyan oval eyes (blink via group scale) */}
          <group scale={[1, blink, 1]}>
            <RBox
              size={[0.36, 0.72, 0.08]}
              color={COLORS.eye}
              emissive={COLORS.eyeGlow}
              emissiveIntensity={1.4}
              position={[-0.48, 0.08, 1.14]}
              radius={0.18}
              rough={0.15}
            />
            <RBox
              size={[0.36, 0.72, 0.08]}
              color={COLORS.eye}
              emissive={COLORS.eyeGlow}
              emissiveIntensity={1.4}
              position={[0.48, 0.08, 1.14]}
              radius={0.18}
              rough={0.15}
            />
          </group>
          <pointLight position={[0, 0.1, 2.4]} color={COLORS.eyeGlow} intensity={0.7} distance={4} />
          {/* Ear discs — blue */}
          <RBox size={[0.14, 0.85, 0.85]} color={COLORS.blue} position={[-1.29, 0, 0]} radius={0.07} rough={0.5} />
          <RBox size={[0.14, 0.85, 0.85]} color={COLORS.blue} position={[1.29, 0, 0]} radius={0.07} rough={0.5} />
          {/* Antenna: blue base, grey rod, red ball */}
          <RBox size={[0.55, 0.18, 0.55]} color={COLORS.blue} position={[0, 1.16, 0]} radius={0.08} rough={0.5} />
          <group position={[0, 1.25, 0]} rotation={[0, 0, antennaSway]}>
            <RBox size={[0.12, 0.65, 0.12]} color={COLORS.grey} position={[0, 0.32, 0]} radius={0.05} rough={0.4} metal={0.4} />
            <RBox size={[0.48, 0.48, 0.48]} color={COLORS.red} position={[0, 0.85, 0]} radius={0.22} rough={0.35} />
          </group>
        </group>
      </group>
    </group>
  );
};
