/**
 * CasualMan.tsx — Deterministic 3D character component for Remotion + @remotion/three.
 * The engine's second kit cast member, next to BoltBoy (see
 * src/components/BoltBoy.tsx). Built on the engine kit (`src/kit/kit.tsx`).
 *
 * Props:
 *   t?: number        Elapsed time in seconds (default 0). Drive with `frame / fps`.
 *   walk?: number     Walk blend 0..1 (default 1; 0 = idle breathing).
 *   cycle?: number    Seconds per full left+right walk cycle (default 1).
 *   pose?: Pose       A Pose from the clip library (see kit.tsx). When given,
 *                     it drives the character and `t`/`walk`/`cycle` are ignored.
 *   position?: V3     World position [x, y, z] (default [0, 0, 0]).
 *   rotation?: V3     Euler rotation [x, y, z] in radians (default [0, 0, 0]).
 *   scale?: number    Uniform scale (default 1).
 *
 * Conventions: 1 unit ~ 1 stud (~7 units tall), feet rest on y = 0, character faces +z, up is +y.
 */
import React from 'react';
import {RBox, V3, walkPose, Pose} from '../kit/kit';
import {ExpressionName, FaceLayout, FaceState, drawFaceParts, useCharacterFaceTexture} from '../kit/expressions';

export const COLORS = {
  skin: '#fdca9f',
  skinShade: '#d6a581',
  hair: '#3e3e3e',
  hairDark: '#262524',
  beard: '#404040',
  shirt: '#1d5b90',
  shirtDark: '#15456f',
  button: '#dce4ee',
  pants: '#3e3e3e',
  pantsCuff: '#2c2c2e',
  shoeWhite: '#f5f6f8',
  shoeSole: '#dcdfe4',
  eyeDark: '#16161a',
  tongue: '#d04e4a',
};

const CASUALMAN_LAYOUT: FaceLayout = {
  eyeL: [170, 206],
  eyeR: [342, 206],
  eyeRX: 17,
  eyeRY: 26,
  browY: 126,
  browR: 32,
  mouth: [256, 380],
  mouthW: 150,
  ink: '#16161a',
};

/** Draw CasualMan's trimmed goatee / beard & moustache framing the mouth
 * (a fixed feature that frames the mouth in every expression). */
const drawBeard = (g: CanvasRenderingContext2D) => {
  g.fillStyle = COLORS.beard;
  g.strokeStyle = COLORS.hairDark;
  g.lineWidth = 5;
  g.beginPath();
  g.moveTo(154, 340);
  g.quadraticCurveTo(154, 294, 256, 294);
  g.quadraticCurveTo(358, 294, 358, 340);
  g.lineTo(354, 412);
  g.quadraticCurveTo(344, 464, 256, 468);
  g.quadraticCurveTo(168, 464, 158, 412);
  g.closePath();
  g.fill();
  g.stroke();
};

/** CasualMan's face. The default 'smile' is the original face,
 * pixel-identical to before the expression system (sclera-and-iris eyes,
 * beard, teeth band, tongue); every other expression is the beard plus the
 * shared `drawFaceParts` at CasualMan's layout. Known limit: non-default
 * expressions use the shared solid-dark oval eyes, not the original
 * sclera-and-iris eyes — the default keeps the original eyes. */
const drawCasualManFace = (g: CanvasRenderingContext2D, expression: ExpressionName, t: number) => {
  if (expression === 'smile') {
    // Curved dark eyebrows
    g.strokeStyle = COLORS.eyeDark;
    g.lineWidth = 11;
    g.beginPath();
    g.moveTo(125, 138);
    g.quadraticCurveTo(170, 114, 212, 132);
    g.stroke();
    g.beginPath();
    g.moveTo(300, 132);
    g.quadraticCurveTo(342, 114, 387, 138);
    g.stroke();

    // Large expressive eyes: white sclera, dark iris/pupil, crisp white highlight
    for (const x of [170, 342]) {
      g.fillStyle = '#ffffff';
      g.beginPath();
      g.ellipse(x, 206, 26, 36, 0, 0, Math.PI * 2);
      g.fill();
      g.lineWidth = 5;
      g.strokeStyle = COLORS.eyeDark;
      g.stroke();

      g.fillStyle = COLORS.eyeDark;
      g.beginPath();
      g.ellipse(x, 209, 17, 26, 0, 0, Math.PI * 2);
      g.fill();

      g.fillStyle = '#ffffff';
      g.beginPath();
      g.arc(x - 5, 196, 7, 0, Math.PI * 2);
      g.fill();
    }

    // Trimmed goatee / beard & moustache framing the mouth
    drawBeard(g);

    // Friendly open smile: dark mouth cavity, upper white teeth, red tongue
    g.beginPath();
    g.moveTo(182, 342);
    g.quadraticCurveTo(256, 354, 330, 342);
    g.quadraticCurveTo(318, 418, 256, 420);
    g.quadraticCurveTo(194, 418, 182, 342);
    g.closePath();
    g.fillStyle = COLORS.eyeDark;
    g.fill();
    g.lineWidth = 6;
    g.strokeStyle = COLORS.eyeDark;
    g.stroke();

    // Upper teeth band
    g.save();
    g.clip();
    g.fillStyle = '#ffffff';
    g.beginPath();
    g.moveTo(182, 340);
    g.quadraticCurveTo(256, 352, 330, 340);
    g.lineTo(330, 368);
    g.quadraticCurveTo(256, 376, 182, 368);
    g.closePath();
    g.fill();

    // Red tongue
    g.fillStyle = COLORS.tongue;
    g.beginPath();
    g.ellipse(256, 412, 42, 22, 0, Math.PI, Math.PI * 2);
    g.fill();
    g.restore();
    return;
  }
  drawBeard(g);
  drawFaceParts(g, CASUALMAN_LAYOUT, expression, t);
};

const Hair: React.FC<{bounce: number}> = ({bounce}) => (
  <group rotation={[bounce, 0, 0]}>
    {/* Top crown */}
    <RBox size={[1.46, 0.36, 1.44]} color={COLORS.hair} position={[0, 0.68, -0.02]} radius={0.14} rough={0.88} />
    {/* Slight front hairline ridge */}
    <RBox size={[1.26, 0.22, 0.32]} color={COLORS.hair} position={[0, 0.66, 0.56]} rotation={[0.18, 0, 0]} radius={0.09} rough={0.88} />
    {/* Back of head */}
    <RBox size={[1.46, 1.05, 0.38]} color={COLORS.hair} position={[0, 0.18, -0.58]} radius={0.1} rough={0.88} />
    {/* Side hair + sideburns */}
    {[-1, 1].map((sx) => (
      <group key={sx}>
        <RBox size={[0.18, 0.72, 0.78]} color={COLORS.hair} position={[sx * 0.66, 0.28, -0.18]} radius={0.06} rough={0.88} />
        <RBox size={[0.14, 0.36, 0.26]} color={COLORS.hair} position={[sx * 0.67, 0.02, 0.2]} radius={0.05} rough={0.88} />
      </group>
    ))}
  </group>
);

const Arm: React.FC<{side: 1 | -1; p: V3}> = ({side, p}) => (
  <group position={[side * 1.46, 4.18, 0]} rotation={[p[0], p[1], side * (0.07 + p[2])]}>
    <RBox size={[0.88, 1.5, 0.88]} color={COLORS.shirt} position={[0, -0.75, 0]} radius={0.14} rough={0.72} />
    <RBox size={[0.92, 0.22, 0.92]} color={COLORS.shirtDark} position={[0, -1.44, 0]} radius={0.06} rough={0.72} />
    <RBox size={[0.8, 0.56, 0.8]} color={COLORS.skin} position={[0, -1.82, 0]} radius={0.12} rough={0.55} />
  </group>
);

const Leg: React.FC<{side: 1 | -1; p: V3; lift: number}> = ({side, p, lift}) => (
  <group position={[side * 0.5, 2.3 + lift, 0]} rotation={[p[0], p[1], side * p[2]]}>
    {/* Pants run 0.3 up inside the shirt (top y 2.6): hides the tilting
        pants top face on leg swings (see BoltBoy — the maintainer 2026-11-20).
        Bottom (y 0.54) and cuff unchanged. */}
    <RBox size={[0.72, 2.06, 0.76]} color={COLORS.pants} position={[0, -0.73, 0]} radius={0.08} rough={0.78} />
    <RBox size={[0.96, 0.14, 1.0]} color={COLORS.pantsCuff} position={[0, -1.72, 0]} radius={0.05} rough={0.78} />
    {/* Shoe pivots at the ANKLE (y -2.2), not the hip — see BoltBoy. */}
    <group position={[0, -2.2, 0]} rotation={[-p[0] * 0.45, 0, 0]}>
      <RBox size={[0.98, 0.16, 1.32]} color={COLORS.shoeSole} position={[0, -0.02, 0.12]} radius={0.06} rough={0.55} />
      <RBox size={[0.94, 0.38, 1.24]} color={COLORS.shoeWhite} position={[0, 0.22, 0.1]} radius={0.1} rough={0.48} />
      <RBox size={[0.9, 0.28, 0.45]} color={COLORS.shoeWhite} position={[0, 0.18, 0.56]} radius={0.12} rough={0.48} />
      <RBox size={[0.54, 0.12, 0.45]} color={COLORS.shoeSole} position={[0, 0.44, 0.18]} radius={0.04} rough={0.5} />
    </group>
  </group>
);

export const CasualMan: React.FC<{
  t?: number;
  walk?: number;
  cycle?: number;
  /** A Pose from the clip library. When given, it drives the character and
   *  `t`/`walk`/`cycle` are ignored. */
  pose?: Pose;
  /** A face expression from the common expression system. Default 'smile'
   *  (the original face). `expressionT` animates moving extras (tears). */
  expression?: ExpressionName;
  expressionT?: number;
  /** A face-transition state (from performanceFace). When given, it drives
   *  the face with a crossfade and `expression` is ignored. */
  faceState?: FaceState;
  position?: V3;
  rotation?: V3;
  scale?: number;
}> = ({t = 0, walk = 1, cycle = 1, pose, expression = 'smile', expressionT = 0, faceState, position = [0, 0, 0], rotation = [0, 0, 0], scale = 1}) => {
  const face = useCharacterFaceTexture(drawCasualManFace, expression, faceState, expressionT);
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
          {/* Blue button-up shirt torso — bottom ends exactly at the waist
              (y 2.3), NOT extended down over the pants (see BoltBoy). */}
          <RBox size={[1.96, 2, 1.0]} color={COLORS.shirt} position={[0, 3.3, 0]} radius={0.14} rough={0.72} />
          {/* Taller hem band (0.45, y 2.30-2.75): covers the pants top
              face as it tilts up during leg swings (see BoltBoy). */}
          <RBox size={[2.28, 0.6, 1.2]} color={COLORS.shirtDark} position={[0, 2.6, 0]} radius={0.07} rough={0.72} />
          {/* Central button placket + buttons */}
          <RBox size={[0.24, 1.85, 0.06]} color={COLORS.shirtDark} position={[0, 3.32, 0.51]} radius={0.02} rough={0.72} />
          {[3.95, 3.6, 3.25, 2.9].map((by, idx) => (
            <mesh key={idx} position={[0, by, 0.545]} rotation={[Math.PI / 2, 0, 0]}>
              <cylinderGeometry args={[0.045, 0.045, 0.025, 16]} />
              <meshStandardMaterial color={COLORS.button} roughness={0.35} />
            </mesh>
          ))}

          {/* Neck + shirt collar */}
          <RBox size={[0.68, 0.32, 0.68]} color={COLORS.skin} position={[0, 4.42, 0]} radius={0.08} rough={0.55} />
          <RBox size={[1.05, 0.18, 0.95]} color={COLORS.shirtDark} position={[0, 4.3, 0]} radius={0.07} rough={0.72} />
          {[-1, 1].map((sx) => (
            <RBox
              key={sx}
              size={[0.38, 0.24, 0.14]}
              color={COLORS.shirt}
              position={[sx * 0.26, 4.24, 0.48]}
              rotation={[0.15, 0, sx * -0.35]}
              radius={0.04}
              rough={0.72}
            />
          ))}

          <Arm side={-1} p={p.armL} />
          <Arm side={1} p={p.armR} />

          {/* Head + Ears + Nose + Face + Hair */}
          <group position={[0, 5.18, 0]} rotation={p.head}>
            <RBox size={[1.4, 1.48, 1.38]} color={COLORS.skin} radius={0.22} rough={0.55} />
            {/* Ears */}
            {[-1, 1].map((sx) => (
              <group key={sx} position={[sx * 0.74, -0.04, 0]}>
                <RBox size={[0.18, 0.38, 0.22]} color={COLORS.skin} radius={0.07} rough={0.55} />
                <RBox size={[0.08, 0.2, 0.12]} color={COLORS.skinShade} position={[sx * 0.06, 0, 0.02]} radius={0.03} rough={0.55} />
              </group>
            ))}
            {/* Subtle 3D nose */}
            <RBox size={[0.16, 0.18, 0.14]} color={COLORS.skinShade} position={[0, -0.06, 0.71]} radius={0.05} rough={0.55} />
            {/* Crisp 2D face plane (eyes, brows, beard, moustache, smile) */}
            <mesh position={[0, -0.04, 0.695]}>
              <planeGeometry args={[1.3, 1.32]} />
              <meshStandardMaterial map={face} transparent roughness={0.6} />
            </mesh>
            <Hair bounce={p.hair} />
          </group>
          </group>
        </group>
      </group>
      </group>
      <ambientLight intensity={0} />
    </group>
  );
};
