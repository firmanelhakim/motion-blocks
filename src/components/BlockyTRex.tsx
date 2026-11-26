import React from 'react';
import {RBox, type V3} from '../kit/kit';

/**
 * BlockyTRex.tsx — ported from new-assets/trex.
 * T. rex only: two thick legs, angled torso + chest, tiny two-finger arms,
 * segmented tail, huge square head with hinged jaw and blocky teeth.
 * DROPPED (source scene scaffolding): the grass + hills, the town street
 * (road, sidewalks, centre stripes), the 4 town houses and 4 trees.
 * Re-based so the feet sit on y = 0 (source dino group sat at y = 0.08,
 * standing on its road slab, top y = 0.06); x offset 0.2 kept.
 *
 * WALK (plan's simplest version — added here, source was IDLE ONLY):
 * `walk` 0 = idle (source idle exactly), 1 = full walk, looping cleanly
 * over a 1s cycle. Each leg is now pivoted at the hip (y = 2.2, top of
 * the thigh; inner boxes shifted by -2.2 so the geometry is unchanged at
 * walk = 0) and swings ±0.5 rad in opposite phase. The tail sway grows
 * with walk, the head turns slightly with the walk, and the torso bobs
 * twice per cycle. Legs are single rigid pieces (thigh + shin + foot in
 * one pivot) — no knee bend, no foot lift — so feet may slide a little
 * and the hip can show a small gap at full bob; that is the known limit
 * of this simplest version.
 *
 * NO V3 POSE PORT: this component does NOT take a Pose and does NOT use
 * the kit clip system (walkPose etc.). It stays a hand-built character
 * with its own `walk` prop; the full V3 pose port is still outstanding.
 */
export const COLORS = {
  dinoMain: '#637862',
  dinoDark: '#485947',
  dinoLight: '#859c82',
  teeth: '#f4f6f8',
  eyeDark: '#232824',
};

export const BlockyTRex: React.FC<{
  t?: number;
  duration?: number;
  position?: V3;
  rotation?: V3;
  scale?: number;
  /** 0 = idle (source idle exactly), 1 = full walk. Default 0. */
  walk?: number;
}> = ({t = 0, duration = 3, position = [0, 0, 0], rotation = [0, 0, 0], scale = 1, walk = 0}) => {
  const ph = (t / duration) * Math.PI * 2;
  const breathe = Math.sin(ph) * 0.04;
  const jawOpen = 0.08 + (Math.sin(ph * 2) * 0.5 + 0.5) * 0.14;
  const tailSway = Math.sin(ph) * 0.14;
  const armBob = Math.sin(ph * 2) * 0.08;

  // Walk cycle: 1s loop, independent of the 3s idle phase.
  const wph = (t / 1) * Math.PI * 2;
  const walkSin = Math.sin(wph) * walk;
  const tailWalk = Math.sin(wph) * 0.16 * walk;
  const headYaw = Math.sin(wph) * 0.12 * walk;
  const walkBob = walk * 0.07 * Math.abs(Math.sin(wph));

  return (
    <group position={position} rotation={rotation} scale={scale}>
      {/* Big Blocky T. rex (Facing -x / camera-left) */}
      <group position={[0.2, 0, 0]} rotation={[0, -Math.PI / 2, 0]}>
        {/* Two Thick Strong Legs, pivoted at the hip (y = 2.2) for the walk */}
        {([-1, 1] as const).map((side) => (
          <group key={side} position={[side * 0.85, 2.2, 0]} rotation={[side * 0.5 * walkSin, 0, 0]}>
            {/* Upper thigh */}
            <RBox size={[0.78, 1.35, 1.05]} color={COLORS.dinoDark} position={[0, -0.65, -0.15]} radius={0.04} />
            {/* Lower shin */}
            <RBox size={[0.66, 1.05, 0.72]} color={COLORS.dinoDark} position={[0, -1.55, -0.2]} radius={0.04} />
            {/* Blocky 3-toed foot */}
            <RBox size={[0.74, 0.34, 1.02]} color={COLORS.dinoDark} position={[0, -2.03, 0.02]} radius={0.03} />
            {[-0.22, 0, 0.22].map((tx, ti) => (
              <RBox key={ti} size={[0.16, 0.2, 0.24]} color={COLORS.dinoMain} position={[tx, -2.1, 0.6]} radius={0.02} />
            ))}
          </group>
        ))}

        {/* Torso + Chest + Tiny Two-Finger Arms + Tail + Huge Head */}
        <group position={[0, breathe + walkBob, 0]}>
          {/* Angled Body */}
          <group position={[0, 2.35, 0]} rotation={[0.42, 0, 0]}>
            <RBox size={[1.55, 2.05, 1.55]} color={COLORS.dinoMain} position={[0, 0, 0]} radius={0.05} />
            <RBox size={[1.28, 1.85, 0.35]} color={COLORS.dinoLight} position={[0, -0.05, 0.72]} radius={0.04} />
          </group>

          {/* Two Tiny Two-Finger Arms */}
          {([-1, 1] as const).map((side) => (
            <group key={side} position={[side * 0.88, 2.45, 0.88]} rotation={[0.35 + armBob, 0, 0]}>
              <RBox size={[0.28, 0.28, 0.56]} color={COLORS.dinoMain} position={[0, 0, 0.22]} radius={0.03} />
              {/* Two tiny blocky fingers */}
              <RBox size={[0.09, 0.18, 0.14]} color={COLORS.dinoDark} position={[-0.06, -0.1, 0.52]} radius={0.01} />
              <RBox size={[0.09, 0.18, 0.14]} color={COLORS.dinoDark} position={[0.06, -0.1, 0.52]} radius={0.01} />
            </group>
          ))}

          {/* Long Thick Segmented Tail Stretching Behind */}
          <group position={[0, 1.9, -0.85]} rotation={[0, tailSway + tailWalk, 0]}>
            <RBox size={[1.18, 1.05, 1.15]} color={COLORS.dinoMain} position={[0, 0.05, -0.5]} radius={0.04} />
            <RBox size={[0.88, 0.82, 1.1]} color={COLORS.dinoMain} position={[0, 0.18, -1.45]} rotation={[0.12, 0, 0]} radius={0.04} />
            <RBox size={[0.62, 0.6, 1.05]} color={COLORS.dinoDark} position={[0, 0.38, -2.35]} rotation={[0.2, 0, 0]} radius={0.04} />
            <RBox size={[0.42, 0.42, 0.85]} color={COLORS.dinoDark} position={[0, 0.62, -3.1]} rotation={[0.25, 0, 0]} radius={0.03} />
          </group>

          {/* Huge Square Head with Wide Jaw & Small White Blocky Teeth */}
          <group position={[0, 3.65, 0.82]} rotation={[0, headYaw, 0]}>
            {/* Cranium */}
            <RBox size={[1.56, 1.28, 1.25]} color={COLORS.dinoMain} position={[0, 0.22, -0.12]} radius={0.05} />
            {/* Wide Upper Snout */}
            <RBox size={[1.44, 0.82, 1.22]} color={COLORS.dinoMain} position={[0, 0.1, 0.95]} radius={0.04} />
            {/* Nostrils */}
            {[-0.36, 0.36].map((nx, ni) => (
              <RBox key={ni} size={[0.16, 0.16, 0.08]} color={COLORS.eyeDark} position={[nx, 0.3, 1.56]} radius={0.02} />
            ))}
            {/* Eyes on Both Sides */}
            {[-0.79, 0.79].map((ex, ei) => (
              <group key={ei} position={[ex, 0.46, 0.15]}>
                <RBox size={[0.06, 0.28, 0.28]} color={COLORS.teeth} radius={0.01} />
                <RBox size={[0.08, 0.18, 0.18]} color={COLORS.eyeDark} position={[ei === 0 ? -0.01 : 0.01, 0, 0.02]} radius={0.01} />
              </group>
            ))}
            {/* Upper White Blocky Teeth */}
            {[-0.5, -0.25, 0, 0.25, 0.5].map((tx, ti) => (
              <RBox key={ti} size={[0.14, 0.14, 0.12]} color={COLORS.teeth} position={[tx, -0.34, 1.44]} radius={0.01} />
            ))}
            {[-0.58, 0.58].map((sx, si) =>
              [0.55, 0.88, 1.2].map((sz, zi) => (
                <RBox key={`${si}-${zi}`} size={[0.12, 0.14, 0.14]} color={COLORS.teeth} position={[sx, -0.34, sz]} radius={0.01} />
              ))
            )}

            {/* Hinged Lower Jaw */}
            <group position={[0, -0.38, 0.15]} rotation={[jawOpen, 0, 0]}>
              <RBox size={[1.38, 0.42, 1.95]} color={COLORS.dinoLight} position={[0, -0.2, 0.45]} radius={0.04} />
              {/* Lower White Blocky Teeth */}
              {[-0.42, -0.14, 0.14, 0.42].map((tx, ti) => (
                <RBox key={ti} size={[0.13, 0.12, 0.12]} color={COLORS.teeth} position={[tx, 0.05, 1.3]} radius={0.01} />
              ))}
            </group>
          </group>
        </group>
      </group>
    </group>
  );
};
