/**
 * WingedBoy.tsx — Deterministic 3D character component for Remotion + @remotion/three.
 * The engine's third kit cast member, next to BoltBoy and CasualMan (see
 * src/components/BoltBoy.tsx). Ported from the WingedBoy zip the maintainer shared
 * 2026-11-20 (`~/workspace/videos/wingedboy-source/`), converted from the
 * old walkPose return shape to the engine kit's Pose system.
 *
 * Props:
 *   t?: number        Elapsed time in seconds (default 0). Drive with `frame / fps`.
 *   walk?: number     Walk blend 0..1 (default 1; 0 = idle breathing).
 *   cycle?: number    Seconds per full left+right walk cycle (default 1).
 *   pose?: Pose       A Pose from the clip library (see kit.tsx). When given,
 *                     it drives the character and `t`/`walk`/`cycle` are ignored.
 *                     The wings read `pose.flap` — the fly clip beats them
 *                     wide, the walk clip gives the small walk flap.
 *   expression?: ExpressionName  Face from the common expression system
 *                     (see src/kit/expressions.tsx). Default 'smirk' — his
 *                     original face, drawn pixel-identically. `expressionT`
 *                     animates the moving extras (falling tears, dizzy spin).
 *   position?: V3     World position [x, y, z] (default [0, 0, 0]).
 *   rotation?: V3     Euler rotation [x, y, z] in radians (default [0, 0, 0]).
 *   scale?: number    Uniform scale (default 1).
 *
 * Conventions: 1 unit ~ 1 stud (~7 units body height, ~10.5 with wings), feet rest on y = 0, facing +z, up is +y.
 */
import React from 'react';
import {RBox, V3, walkPose, Pose} from '../kit/kit';
import {drawFaceParts, ExpressionName, FaceLayout, FaceState, useCharacterFaceTexture} from '../kit/expressions';

export const COLORS = {
  skin: '#f2c6a0',
  hair: '#32b8f5',
  hairTip: '#5cd6ff',
  hoodie: '#1e488d',
  hoodieDark: '#133163',
  string: '#0e2a5b',
  pants: '#647181',
  pantsSeam: '#4b5563',
  shoeGrey: '#647181',
  shoeWhite: '#f3f5f8',
  wingWhite: '#f4f6f9',
  wingShade: '#e2e8f0',
  eyeDark: '#16161a',
};

const WINGEDBOY_LAYOUT: FaceLayout = {
  eyeL: [175, 224],
  eyeR: [337, 224],
  eyeRX: 15,
  eyeRY: 27,
  browY: 155,
  browR: 32,
  mouth: [256, 335],
  mouthW: 140,
  ink: '#16161a',
  browInk: '#16161a',
};

/** WingedBoy's face. The default 'smirk' is the original face, pixel-identical
 * to before the expression system; every other expression is drawn by the
 * shared `drawFaceParts` at WingedBoy's layout. */
const drawWingedBoyFace = (g: CanvasRenderingContext2D, expression: ExpressionName, t: number) => {
  if (expression === 'smirk') {
    // Thin expressive brows
    g.strokeStyle = COLORS.eyeDark;
    g.lineWidth = 8;
    g.beginPath();
    g.moveTo(140, 165);
    g.quadraticCurveTo(175, 146, 208, 160);
    g.stroke();
    g.beginPath();
    g.moveTo(304, 160);
    g.quadraticCurveTo(337, 144, 372, 162);
    g.stroke();

    // Oval dark eyes with white highlight dot
    for (const x of [175, 337]) {
      g.fillStyle = COLORS.eyeDark;
      g.beginPath();
      g.ellipse(x, 224, 15, 27, 0, 0, Math.PI * 2);
      g.fill();
      g.fillStyle = '#ffffff';
      g.beginPath();
      g.arc(x - 4, 211, 6, 0, Math.PI * 2);
      g.fill();
    }

    // Confident asymmetric smirk
    g.strokeStyle = COLORS.eyeDark;
    g.lineWidth = 10;
    g.beginPath();
    g.moveTo(192, 342);
    g.quadraticCurveTo(268, 354, 332, 314);
    g.stroke();
    return;
  }
  drawFaceParts(g, WINGEDBOY_LAYOUT, expression, t);
};

const Hair: React.FC<{bounce: number}> = ({bounce}) => {
  const spikes: [V3, number, number, number][] = [
    [[-0.55, 0.92, 0.12], 0.12, 0.62, 0.95],
    [[-0.22, 1.02, -0.08], -0.1, 0.34, 1.2],
    [[0.16, 1.02, 0.02], 0.0, -0.22, 1.3],
    [[0.54, 0.94, 0.1], 0.1, -0.62, 1.0],
    [[0.0, 0.94, 0.42], 0.95, 0.0, 0.85],
    [[-0.44, 0.88, 0.42], 0.82, 0.48, 0.78],
    [[0.44, 0.88, 0.42], 0.82, -0.48, 0.78],
    [[-0.22, 0.94, -0.42], -0.72, 0.32, 0.95],
    [[0.3, 0.94, -0.42], -0.72, -0.32, 0.95],
    [[0.0, 0.72, -0.74], -1.1, 0, 0.85],
  ];
  return (
    <group rotation={[bounce, 0, 0]}>
      <RBox size={[1.48, 0.48, 1.48]} color={COLORS.hair} position={[0, 0.72, 0]} radius={0.12} rough={0.78} />
      <RBox size={[1.48, 1.05, 0.38]} color={COLORS.hair} position={[0, 0.2, -0.6]} radius={0.1} rough={0.78} />
      <RBox size={[0.2, 0.68, 1.08]} color={COLORS.hair} position={[-0.64, 0.3, -0.1]} radius={0.06} rough={0.78} />
      <RBox size={[0.2, 0.68, 1.08]} color={COLORS.hair} position={[0.64, 0.3, -0.1]} radius={0.06} rough={0.78} />
      <RBox size={[1.05, 0.28, 0.24]} color={COLORS.hair} position={[0.04, 0.5, 0.72]} rotation={[0.25, 0, -0.08]} radius={0.07} rough={0.78} />
      {spikes.map(([p, rx, rz, s], i) => (
        <mesh key={i} position={p} rotation={[rx, 0, rz]}>
          <coneGeometry args={[0.25, 0.68 * s, 5]} />
          <meshStandardMaterial color={i % 2 === 0 ? COLORS.hair : COLORS.hairTip} roughness={0.75} />
        </mesh>
      ))}
    </group>
  );
};

// Multi-tiered blocky angel wings mounted behind the shoulders
const Wings: React.FC<{flap: number}> = ({flap}) => {
  // Primary outer feathers: [xOffsetFromPivot, yOffsetFromPivot, length, width, angleZ]
  const outerFeathers: [number, number, number, number, number][] = [
    [1.1, 0.5, 2.2, 0.52, -0.25],
    [1.6, 1.0, 2.5, 0.52, -0.34],
    [2.1, 1.55, 2.8, 0.52, -0.44],
    [2.65, 2.15, 3.1, 0.5, -0.54],
    [3.2, 2.8, 3.3, 0.48, -0.62],
    [3.75, 3.55, 3.4, 0.46, -0.68],
    [4.25, 4.35, 3.1, 0.44, -0.74],
    [3.4, 1.4, 2.4, 0.48, -0.82],
    [2.85, 0.65, 2.1, 0.46, -0.95],
    [2.2, 0.0, 1.85, 0.45, -1.1],
    [1.55, -0.48, 1.55, 0.44, -1.28],
    [0.95, -0.75, 1.3, 0.42, -1.45],
  ];

  // Secondary inner covert feathers layered in front for depth
  // (innermost one kept low and steep so it clears the shoulder when an
  // arm is raised — it used to cross the waving arm's silhouette)
  const innerFeathers: [number, number, number, number, number][] = [
    [0.9, 0.05, 1.35, 0.45, -0.55],
    [1.4, 0.7, 1.65, 0.45, -0.45],
    [1.95, 1.25, 1.85, 0.44, -0.55],
    [2.5, 1.85, 2.0, 0.42, -0.65],
    [3.0, 2.5, 2.05, 0.4, -0.72],
    [2.1, 0.35, 1.5, 0.42, -0.95],
    [1.45, -0.15, 1.25, 0.4, -1.18],
  ];

  return (
    // Wing root sits out and back from the shoulders (was [0, 3.65, -0.58]
    // with the side pivot at ±0.45) so the fan clears a raised arm.
    <group position={[0, 3.5, -0.72]}>
      {([-1, 1] as const).map((side) => (
        <group
          key={side}
          position={[side * 0.6, 0, 0]}
          // V3 wing-beat pivot (2026-11-20, the maintainer: the beat read as a
          // horizontal sweep): the flap now drives the z-rotation, so the
          // wingtips rise and fall — a vertical beat. The y-rotation is a
          // fixed rest angle (wings swept back). At flap 0.1 the wing is
          // near level; at flap 1.0 it is up ~23°.
          rotation={[0, side * -0.18, side * (-0.1 + flap * 0.5)]}
        >
          {/* Wing root shoulder mount */}
          <RBox
            size={[0.6, 0.85, 0.34]}
            color={COLORS.wingShade}
            position={[side * 0.28, 0.1, 0]}
            radius={0.08}
            rough={0.65}
          />
          {/* Outer primary feather layer */}
          {outerFeathers.map(([x, y, len, w, ang], i) => (
            <RBox
              key={`o-${i}`}
              size={[w, len, 0.2]}
              color={COLORS.wingWhite}
              position={[side * x, y, -0.04]}
              rotation={[0, 0, side * ang]}
              radius={0.05}
              rough={0.6}
            />
          ))}
          {/* Inner covert feather layer */}
          {innerFeathers.map(([x, y, len, w, ang], i) => (
            <RBox
              key={`i-${i}`}
              size={[w, len, 0.2]}
              color={COLORS.wingShade}
              position={[side * x, y, 0.12]}
              rotation={[0, 0, side * ang]}
              radius={0.05}
              rough={0.62}
            />
          ))}
        </group>
      ))}
    </group>
  );
};

const Arm: React.FC<{side: 1 | -1; p: V3}> = ({side, p}) => (
  <group position={[side * 1.48, 4.2, 0]} rotation={[p[0], p[1], side * (0.07 + p[2])]}>
    <RBox size={[0.92, 1.48, 0.92]} color={COLORS.hoodie} position={[0, -0.74, 0]} radius={0.12} rough={0.72} />
    <RBox size={[0.96, 0.22, 0.96]} color={COLORS.hoodieDark} position={[0, -1.44, 0]} radius={0.06} rough={0.72} />
    <RBox size={[0.88, 0.6, 0.88]} color={COLORS.skin} position={[0, -1.84, 0]} radius={0.08} rough={0.55} />
  </group>
);

const Leg: React.FC<{side: 1 | -1; p: V3; lift: number}> = ({side, p, lift}) => (
  <group position={[side * 0.52, 2.3 + lift, 0]} rotation={[p[0], p[1], side * p[2]]}>
    {/* Pants run 0.3 up inside the hoodie (top y 2.6): hides the tilting
        pants top face on leg swings (see BoltBoy — the maintainer 2026-11-20).
        Bottom (y 0.5) unchanged. */}
    <RBox size={[0.74, 2.1, 0.78]} color={COLORS.pants} position={[0, -0.75, 0]} radius={0.08} rough={0.78} />
    {/* Subtle dark pant seam */}
    <RBox size={[0.99, 2.02, 0.1]} color={COLORS.pantsSeam} position={[0, -0.73, 0]} radius={0.02} rough={0.8} />
    {/* Shoe pivots at the ANKLE (y -2.2), not the hip — see BoltBoy. */}
    <group position={[0, -2.2, 0]} rotation={[-p[0] * 0.45, 0, 0]}>
      <RBox size={[0.98, 0.18, 1.32]} color={COLORS.shoeWhite} position={[0, 0, 0.12]} radius={0.07} rough={0.5} />
      <RBox size={[1.0, 0.4, 0.92]} color={COLORS.shoeGrey} position={[0, 0.27, -0.1]} radius={0.1} rough={0.6} />
      <RBox size={[0.96, 0.32, 0.58]} color={COLORS.shoeWhite} position={[0, 0.22, 0.42]} radius={0.12} rough={0.5} />
      <RBox size={[0.6, 0.1, 0.5]} color={COLORS.shoeWhite} position={[0, 0.45, 0.14]} radius={0.04} rough={0.5} />
    </group>
  </group>
);

export const WingedBoy: React.FC<{
  t?: number;
  walk?: number;
  cycle?: number;
  /** A Pose from the clip library. When given, it drives the character and
   *  `t`/`walk`/`cycle` are ignored. */
  pose?: Pose;
  /** Face from the common expression system. Default 'smirk' — the original
   *  face, drawn pixel-identically. */
  expression?: ExpressionName;
  expressionT?: number;
  /** A face-transition state (from performanceFace). When given, it drives
   *  the face with a crossfade and `expression` is ignored. */
  faceState?: FaceState;
  position?: V3;
  rotation?: V3;
  scale?: number;
}> = ({t = 0, walk = 1, cycle = 1, pose, expression = 'smirk', expressionT = 0, faceState, position = [0, 0, 0], rotation = [0, 0, 0], scale = 1}) => {
  const face = useCharacterFaceTexture(drawWingedBoyFace, expression, faceState, expressionT);
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
          {/* Navy hoodie torso — bottom ends exactly at the waist (y 2.3),
              NOT extended down over the pants (see BoltBoy for why). */}
          <RBox size={[2, 2, 1]} color={COLORS.hoodie} position={[0, 3.3, 0]} radius={0.14} rough={0.72} />
          {/* Taller ribbed waistband (0.45, y 2.30-2.75): covers the pants
              top face as it tilts up during leg swings (see BoltBoy). */}
          <RBox size={[2.34, 0.6, 1.24]} color={COLORS.hoodieDark} position={[0, 2.6, 0]} radius={0.07} rough={0.72} />
          <RBox size={[1.48, 0.2, 1.12]} color={COLORS.hoodieDark} position={[0, 4.3, 0]} radius={0.08} rough={0.72} />
          <RBox size={[0.7, 0.3, 0.7]} color={COLORS.skin} position={[0, 4.42, 0]} radius={0.06} rough={0.55} />
          {/* Front kangaroo pocket */}
          <RBox size={[1.22, 0.56, 0.1]} color={COLORS.hoodieDark} position={[0, 3.03, 0.52]} radius={0.05} rough={0.74} />
          {/* Hood drawstrings */}
          {[-0.18, 0.18].map((x) => (
            <group key={x}>
              <mesh position={[x, 3.96, 0.52]}>
                <cylinderGeometry args={[0.038, 0.038, 0.54, 8]} />
                <meshStandardMaterial color={COLORS.string} roughness={0.7} />
              </mesh>
              <mesh position={[x, 3.68, 0.52]}>
                <sphereGeometry args={[0.055, 10, 10]} />
                <meshStandardMaterial color={COLORS.string} roughness={0.7} />
              </mesh>
            </group>
          ))}

          <Arm side={-1} p={p.armL} />
          <Arm side={1} p={p.armR} />
          <Wings flap={p.flap} />

          {/* Head + Face + Spiky Cyan Hair */}
          <group position={[0, 5.17, 0]} rotation={p.head}>
            <RBox size={[1.4, 1.44, 1.38]} color={COLORS.skin} radius={0.2} rough={0.55} />
            <mesh position={[0, -0.04, 0.695]}>
              <planeGeometry args={[1.3, 1.3]} />
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
