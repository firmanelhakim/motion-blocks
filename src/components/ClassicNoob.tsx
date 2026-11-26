/**
 * ClassicNoob.tsx — the engine's `classic_noob` preset redrawn with the kit
 * technique (same pattern as CasualMan / BoltBoy: RBox + canvas face +
 * walkPose, all deterministic).
 *
 * Props: `pose` is the joint Pose from the clip library (see kit.tsx) —
 * pass one and the character does that animation with no changes to this
 * file. Without `pose` it falls back to the old `t`/`walk`/`cycle` walk.
 *
 * Faithful to the preset in the engine (`src/characters/look.ts`):
 *   skin 'classic' #F5CD30, hair none, tshirt blue #2563EB with no sleeves,
 *   pants #A3C93A, shoes #A3C93A. Face is the engine's classic smile
 *   (arched brows, oval eyes, smile arc) at the same canvas coordinates
 *   as R6Character's createFaceTexture default branch.
 *
 * Two deliberate tweaks, disclosed: the shoe sole is a slightly darker
 * green (#7FA32C) so the shoe reads against the pants, and the kit rig is
 * ~7.1 studs tall vs the R6's ~5.9 — render it at scale={0.83} when it
 * stands next to an R6 character.
 */
import React from 'react';
import {RBox, V3, useCanvasTexture, walkPose, Pose} from '../kit/kit';

export const COLORS = {
  skin: '#f5cd30',
  shirt: '#2563eb',
  shirtDark: '#1d4ed8',
  pants: '#a3c93a',
  shoe: '#a3c93a',
  shoeSole: '#7fa32c',
  eyeDark: '#141414',
};

const useFaceTexture = () =>
  useCanvasTexture((g) => {
    // Classic warm Roblox smile with eyebrows — same layout as the engine.
    g.strokeStyle = COLORS.eyeDark;
    g.fillStyle = COLORS.eyeDark;
    g.lineCap = 'round';
    // Brows: arcs above the eyes
    g.lineWidth = 12;
    g.beginPath();
    g.arc(256 - 66, 266 - 58, 32, 1.2 * Math.PI, 1.8 * Math.PI, false);
    g.stroke();
    g.beginPath();
    g.arc(256 + 66, 266 - 58, 32, 1.2 * Math.PI, 1.8 * Math.PI, false);
    g.stroke();
    // Eyes: tall ovals
    g.beginPath();
    g.ellipse(256 - 66, 266 - 30, 17, 27, 0, 0, Math.PI * 2);
    g.ellipse(256 + 66, 266 - 30, 17, 27, 0, 0, Math.PI * 2);
    g.fill();
    // Smile: wide arc
    g.lineWidth = 15;
    g.beginPath();
    g.arc(256, 266 - 4, 78, 0.22 * Math.PI, 0.78 * Math.PI, false);
    g.stroke();
  });

const Arm: React.FC<{side: 1 | -1; p: V3}> = ({side, p}) => (
  // Sleeveless tee: arms are bare skin (classic yellow), no cuff.
  <group position={[side * 1.46, 4.18, 0]} rotation={[p[0], p[1], side * (0.07 + p[2])]}>
    <RBox size={[0.88, 1.5, 0.88]} color={COLORS.skin} position={[0, -0.75, 0]} radius={0.14} rough={0.55} />
    <RBox size={[0.8, 0.56, 0.8]} color={COLORS.skin} position={[0, -1.82, 0]} radius={0.12} rough={0.55} />
  </group>
);

const Leg: React.FC<{side: 1 | -1; p: V3; lift: number}> = ({side, p, lift}) => (
  <group position={[side * 0.5, 2.3 + lift, 0]} rotation={[p[0], p[1], side * p[2]]}>
    {/* Pants run 0.3 up inside the shirt (top y 2.6): hides the tilting
        pants top face on leg swings (see BoltBoy — the maintainer 2026-11-20).
        Bottom (y 0.54) unchanged. */}
    <RBox size={[0.72, 2.06, 0.76]} color={COLORS.pants} position={[0, -0.73, 0]} radius={0.08} rough={0.78} />
    {/* Shoe pivots at the ANKLE (y -2.2), not the hip — see the engine BoltBoy. */}
    <group position={[0, -2.2, 0]} rotation={[-p[0] * 0.45, 0, 0]}>
      <RBox size={[0.98, 0.16, 1.32]} color={COLORS.shoeSole} position={[0, -0.02, 0.12]} radius={0.06} rough={0.55} />
      <RBox size={[0.94, 0.38, 1.24]} color={COLORS.shoe} position={[0, 0.22, 0.1]} radius={0.1} rough={0.48} />
      <RBox size={[0.9, 0.28, 0.45]} color={COLORS.shoe} position={[0, 0.18, 0.56]} radius={0.12} rough={0.48} />
      <RBox size={[0.54, 0.12, 0.45]} color={COLORS.shoeSole} position={[0, 0.44, 0.18]} radius={0.04} rough={0.5} />
    </group>
  </group>
);

export const ClassicNoob: React.FC<{
  t?: number;
  walk?: number;
  cycle?: number;
  /** A Pose from the clip library. When given, it drives the character and
   *  `t`/`walk`/`cycle` are ignored. */
  pose?: Pose;
  position?: V3;
  rotation?: V3;
  scale?: number;
}> = ({t = 0, walk = 1, cycle = 1, pose, position = [0, 0, 0], rotation = [0, 0, 0], scale = 1}) => {
  const face = useFaceTexture();
  const p = pose ?? walkPose(t, {cycle, walk, legLength: 2.3});

  return (
    <group position={position} rotation={rotation} scale={scale}>
      {/* V3 root: rootPos + root (y = turn) wrap the whole body. */}
      <group position={p.rootPos} rotation={p.root}>
      <group position={[0, p.y, 0]}>
        <Leg side={-1} p={p.legL} lift={p.liftL} />
        <Leg side={1} p={p.legR} lift={p.liftR} />

        {/* Lean/twist pivot at the WAIST (y 2.3), not the floor: the torso
            bends at the waist so it stays connected to the legs. Pivoting
            at the floor threw the torso forward off the legs on deep leans
            (the bow read as disconnected). The inner wrapper re-bases the
            children so no coordinates change. */}
        <group rotation={p.torso} position={[0, 2.3, 0]}>
          <group position={[0, -2.3, 0]}>
          {/* Blue tee — bottom ends exactly at the waist (y 2.3), NOT
              extended down over the pants (see BoltBoy). */}
          <RBox size={[1.96, 2, 1.0]} color={COLORS.shirt} position={[0, 3.3, 0]} radius={0.14} rough={0.72} />
          {/* Taller hem band (0.45, y 2.30-2.75): covers the pants top
              face as it tilts up during leg swings (see BoltBoy). */}
          <RBox size={[2.28, 0.6, 1.2]} color={COLORS.shirtDark} position={[0, 2.6, 0]} radius={0.07} rough={0.72} />
          {/* Neck + crew collar */}
          <RBox size={[0.68, 0.32, 0.68]} color={COLORS.skin} position={[0, 4.42, 0]} radius={0.08} rough={0.55} />
          <RBox size={[1.05, 0.18, 0.95]} color={COLORS.shirtDark} position={[0, 4.3, 0]} radius={0.07} rough={0.72} />

          <Arm side={-1} p={p.armL} />
          <Arm side={1} p={p.armR} />

          {/* Head — no hair. Crisp 2D face plane (brows, eyes, smile). */}
          <group position={[0, 5.18, 0]} rotation={p.head}>
            <RBox size={[1.4, 1.48, 1.38]} color={COLORS.skin} radius={0.22} rough={0.55} />
            <mesh position={[0, -0.04, 0.695]}>
              <planeGeometry args={[1.3, 1.32]} />
              <meshStandardMaterial map={face} transparent roughness={0.6} />
            </mesh>
          </group>
          </group>
        </group>
      </group>
      </group>
      <ambientLight intensity={0} />
    </group>
  );
};
