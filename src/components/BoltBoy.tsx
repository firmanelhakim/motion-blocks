/**
 * BoltBoy: a procedural 3D blocky character (blue lightning-bolt hoodie, red/black headphones
 * around the neck, spiky brown hair, dark pants, blue/white sneakers).
 *
 * Built on the engine kit (`src/kit/kit.tsx`): RBox, the canvas face texture,
 * and the Pose contract. Every transform is a function of props, so it is
 * deterministic per frame (no useFrame, no refs).
 *
 * Units: 1 unit ~ 1 stud. Feet rest on y = 0, character faces +z, height ~7 (hair tips ~ 7.1).
 *
 * Props:
 *   t        seconds on the animation clock (drive with frame / fps)
 *   walk     0..1 walk intensity (0 = idle standing pose, 1 = full walk cycle)
 *   cycle    seconds for one full walk cycle (left+right step), default 1
 *   pose     A Pose from the clip library (see kit.tsx). When given, it drives
 *            the character and `t`/`walk`/`cycle` are ignored.
 *   position / rotation / scale  placement of the whole character
 */
import React from 'react';
import * as THREE from 'three';
import {RBox, V3, walkPose, Pose} from '../kit/kit';
import {ExpressionName, FaceLayout, FaceState, drawFaceParts, useCharacterFaceTexture} from '../kit/expressions';

export const COLORS = {
  skin: '#f1c29b', hair: '#5a3b25', hoodie: '#2b86e8', hoodieDark: '#1f68c4', bolt: '#ffd21f',
  pants: '#3a3f48', shoeBlue: '#2f8be6', shoeWhite: '#f3f3f3', phBlack: '#15151a', phRed: '#e8212b', string: '#f4f4f4',
};

const BOLTBOY_LAYOUT: FaceLayout = {
  eyeL: [170, 215],
  eyeR: [342, 215],
  eyeRX: 15,
  eyeRY: 28,
  browY: 150,
  browR: 32,
  mouth: [256, 380],
  mouthW: 210,
  ink: '#16161a',
  browInk: '#4a2f1e',
};

/** BoltBoy's face. The default 'grin' is the original face, pixel-identical
 * to before the expression system; every other expression is drawn by the
 * shared `drawFaceParts` at BoltBoy's layout, plus his tongue on open
 * mouths. */
const drawBoltBoyFace = (g: CanvasRenderingContext2D, expression: ExpressionName, t: number) => {
  if (expression === 'grin') {
    // brows
    g.strokeStyle = '#4a2f1e'; g.lineWidth = 9;
    g.beginPath(); g.moveTo(130, 150); g.quadraticCurveTo(170, 128, 205, 142); g.stroke();
    g.beginPath(); g.moveTo(307, 142); g.quadraticCurveTo(342, 128, 382, 150); g.stroke();
    // eyes
    for (const x of [170, 342]) {
      g.fillStyle = '#16161a'; g.beginPath(); g.ellipse(x, 215, 15, 28, 0, 0, Math.PI * 2); g.fill();
      g.fillStyle = '#fff'; g.beginPath(); g.arc(x - 4, 202, 6, 0, Math.PI * 2); g.fill();
    }
    // big smile with teeth
    g.beginPath(); g.moveTo(150, 330); g.quadraticCurveTo(256, 345, 362, 330); g.quadraticCurveTo(340, 430, 256, 432); g.quadraticCurveTo(172, 430, 150, 330); g.closePath();
    g.fillStyle = '#fff'; g.fill(); g.lineWidth = 9; g.strokeStyle = '#16161a'; g.stroke();
    g.fillStyle = '#e8837a'; g.beginPath(); g.ellipse(256, 418, 50, 12, 0, 0, Math.PI); g.fill();
    return;
  }
  drawFaceParts(g, BOLTBOY_LAYOUT, expression, t);
  if (expression === 'laugh' || expression === 'silly') {
    g.fillStyle = '#e8837a';
    g.beginPath(); g.ellipse(256, 418, 50, 12, 0, 0, Math.PI); g.fill();
  }
};

const boltShape = (() => {
  const s = new THREE.Shape();
  [[0.17, 0.55], [-0.28, -0.05], [-0.04, -0.05], [-0.17, -0.6], [0.28, 0.08], [0.04, 0.08]].forEach(([x, y], i) => (i ? s.lineTo(x, y) : s.moveTo(x, y)));
  s.closePath(); return s;
})();

const Hair: React.FC<{bounce: number}> = ({bounce}) => {
  const spikes: [V3, number, number, number][] = [
    [[-0.5, 0.95, 0.1], 0.12, 0.55, 0.9], [[-0.2, 1.0, -0.1], -0.1, 0.3, 1.15], [[0.15, 1.0, 0.0], 0.0, -0.2, 1.25], [[0.5, 0.95, 0.1], 0.1, -0.6, 0.95],
    [[0.0, 0.95, 0.4], 0.95, 0.0, 0.8], [[-0.42, 0.9, 0.4], 0.8, 0.45, 0.7], [[0.42, 0.9, 0.4], 0.8, -0.45, 0.7],
    [[-0.2, 0.95, -0.4], -0.7, 0.3, 0.95], [[0.3, 0.95, -0.4], -0.7, -0.3, 0.95], [[0.0, 0.7, -0.75], -1.1, 0, 0.8],
  ];
  return (
    <group rotation={[bounce, 0, 0]}>
      <RBox size={[1.5, 0.5, 1.5]} color={COLORS.hair} position={[0, 0.72, 0]} radius={0.12} rough={0.9} />
      <RBox size={[1.5, 1.1, 0.4]} color={COLORS.hair} position={[0, 0.2, -0.62]} radius={0.1} rough={0.9} />
      <RBox size={[0.22, 0.7, 1.1]} color={COLORS.hair} position={[-0.65, 0.3, -0.1]} radius={0.06} rough={0.9} />
      <RBox size={[0.22, 0.7, 1.1]} color={COLORS.hair} position={[0.65, 0.3, -0.1]} radius={0.06} rough={0.9} />
      <RBox size={[1.0, 0.3, 0.25]} color={COLORS.hair} position={[0.05, 0.5, 0.74]} rotation={[0.25, 0, -0.08]} radius={0.08} rough={0.9} />
      {spikes.map(([p, rx, rz, s], i) => (
        <mesh key={i} position={p} rotation={[rx, 0, rz]}>
          <coneGeometry args={[0.26, 0.65 * s, 5]} /><meshStandardMaterial color={COLORS.hair} roughness={0.9} />
        </mesh>
      ))}
    </group>
  );
};

const Headphones: React.FC = () => (
  <group position={[0, 4.52, 0.2]}>
    {[-1, 1].map((sx) => (
      <group key={sx} position={[sx * 0.84, 0, 0.08]} rotation={[0, -sx * 0.55, 0]}>
        <group rotation={[0, 0, Math.PI / 2]}>
          {/* black ear pad (faces the head) + black outer rim, red ring on the outside, black centre cap */}
          <mesh position={[0, sx * 0.14, 0]}><cylinderGeometry args={[0.36, 0.36, 0.16, 32]} /><meshStandardMaterial color={COLORS.phBlack} roughness={0.4} /></mesh>
          <mesh position={[0, -sx * 0.1, 0]}><cylinderGeometry args={[0.38, 0.38, 0.14, 32]} /><meshStandardMaterial color={COLORS.phBlack} roughness={0.4} /></mesh>
          <mesh position={[0, -sx * 0.17, 0]}><cylinderGeometry args={[0.31, 0.31, 0.1, 32]} /><meshStandardMaterial color={COLORS.phRed} roughness={0.3} /></mesh>
          <mesh position={[0, -sx * 0.225, 0]}><cylinderGeometry args={[0.15, 0.15, 0.06, 28]} /><meshStandardMaterial color={COLORS.phBlack} roughness={0.35} /></mesh>
        </group>
      </group>
    ))}
    {/* red headband behind the neck with black ends near the cups */}
    <mesh rotation={[-Math.PI / 2, 0, 0]}><torusGeometry args={[0.84, 0.09, 12, 48, Math.PI]} /><meshStandardMaterial color={COLORS.phRed} roughness={0.3} /></mesh>
    {[-1, 1].map((sx) => (
      <mesh key={sx} position={[sx * 0.84, 0, -0.02]} rotation={[0, 0, 0]}><boxGeometry args={[0.16, 0.2, 0.22]} /><meshStandardMaterial color={COLORS.phBlack} roughness={0.4} /></mesh>
    ))}
  </group>
);

const Arm: React.FC<{side: 1 | -1; p: V3}> = ({side, p}) => (
  <group position={[side * 1.5, 4.2, 0]} rotation={[p[0], p[1], side * (0.07 + p[2])]}>
    {/* sleeve */}
    <RBox size={[0.95, 1.5, 0.95]} color={COLORS.hoodie} position={[0, -0.75, 0]} radius={0.14} />
    <RBox size={[1.0, 0.2, 1.0]} color={COLORS.hoodieDark} position={[0, -1.45, 0]} radius={0.06} />
    {/* Roblox-style hand: the plain skin-coloured end of the arm block, same width, no fingers or thumb */}
    <RBox size={[0.9, 0.62, 0.9]} color={COLORS.skin} position={[0, -1.86, 0]} radius={0.07} rough={0.55} />
  </group>
);

const Leg: React.FC<{side: 1 | -1; p: V3; lift: number}> = ({side, p, lift}) => (
  <group position={[side * 0.52, 2.3 + lift, 0]} rotation={[p[0], p[1], side * p[2]]}>
    {/* Pants run 0.3 UP INSIDE the torso (top y 2.6, not 2.3): at rest the
        extra length is hidden inside the shirt, so the waist still reads
        clean. When a leg swings, the pants top face tilts — with the top
        at the waist it rose above y 2.3 and the dark top face showed over
        the shirt (the maintainer, 2026-11-20, walk/run/sprint/march/punch/kick).
        With the top inside the torso the tilted corners stay hidden.
        Slightly narrower (0.9/0.94) so the corners stay inside the
        torso's x/z silhouette. Bottom (y 0.5) and shoe unchanged. */}
    <RBox size={[0.74, 2.1, 0.78]} color={COLORS.pants} position={[0, -0.75, 0]} radius={0.08} />
    {/* Shoe pivots at the ANKLE (y -2.2), not the hip: the old hip pivot
        let the shoe separate from the leg's end on high kicks (the shoe
        sat 2.0 studs out at angle rot*0.55 while the leg ended 2.2 studs
        out at angle rot). The boxes are re-based +2.2 so nothing moves. */}
    <group position={[0, -2.2, 0]} rotation={[-p[0] * 0.45, 0, 0]}>
      <RBox size={[1.0, 0.2, 1.35]} color={COLORS.shoeWhite} position={[0, 0, 0.12]} radius={0.08} rough={0.5} />
      <RBox size={[1.02, 0.42, 0.9]} color={COLORS.shoeBlue} position={[0, 0.28, -0.12]} radius={0.1} rough={0.55} />
      <RBox size={[0.98, 0.34, 0.6]} color={COLORS.shoeWhite} position={[0, 0.23, 0.42]} radius={0.12} rough={0.5} />
      <RBox size={[0.66, 0.1, 0.55]} color={COLORS.shoeWhite} position={[0, 0.46, 0.12]} radius={0.04} rough={0.5} />
    </group>
  </group>
);

export const BoltBoy: React.FC<{
  t?: number;
  walk?: number;
  cycle?: number;
  /** A Pose from the clip library. When given, it drives the character and
   *  `t`/`walk`/`cycle` are ignored. */
  pose?: Pose;
  /** A face expression from the common expression system. Default 'grin'
   *  (the original face). `expressionT` animates moving extras (tears). */
  expression?: ExpressionName;
  expressionT?: number;
  /** A face-transition state (from performanceFace). When given, it drives
   *  the face with a crossfade and `expression` is ignored. */
  faceState?: FaceState;
  position?: V3;
  rotation?: V3;
  scale?: number;
}> = ({t = 0, walk = 1, cycle = 1, pose, expression = 'grin', expressionT = 0, faceState, position = [0, 0, 0], rotation = [0, 0, 0], scale = 1}) => {
  const face = useCharacterFaceTexture(drawBoltBoyFace, expression, faceState, expressionT);
  // The old inline walk math equals walkPose exactly (legAmp 0.46, arm
  // swing s*0.75*0.62 = s*0.465, bodyY with the idle-bob term), so this
  // refactor is behaviour-preserving: same walk, plus every clip.
  const p = pose ?? walkPose(t, {cycle, walk, legLength: 2.3});
  return (
    <group position={position} rotation={rotation} scale={scale}>
      {/* V3 root: rootPos + root (y = turn) wrap the whole body. */}
      <group position={p.rootPos} rotation={p.root}>
      <group position={[0, p.y, 0]}>
        {/* legs: forward = negative x-rotation; left leg forward when s>0.
            Our legL drives the -x limb, legR the +x limb (see kit.tsx). */}
        <Leg side={-1} p={p.legL} lift={p.liftL} />
        <Leg side={1} p={p.legR} lift={p.liftR} />
        {/* Lean/twist pivot at the WAIST (y 2.3), not the floor: the torso
            bends at the waist so it stays connected to the legs. Pivoting
            at the floor threw the torso forward off the legs on deep leans
            (the bow read as disconnected). The inner wrapper re-bases the
            children so no coordinates change. */}
        <group rotation={p.torso} position={[0, 2.3, 0]}>
          <group position={[0, -2.3, 0]}>
          {/* torso — bottom ends exactly at the waist (y 2.3), NOT extended
              down over the pants. The 0.3 extension (from the bow fix) made
              the shirt visibly overlap the pants at rest — the maintainer caught it
              against Claude's render, where the shirt ends cleanly at the
              waist. The waist pivot (not the extension) is what keeps the
              bow connected; the hem band below covers the seam. */}
          <RBox size={[2, 2, 1]} color={COLORS.hoodie} position={[0, 3.3, 0]} radius={0.14} />
          {/* Taller ribbed waistband (0.45, spans y 2.30-2.75): covers the pants
        top face as it tilts up during leg swings (rises to 2.68 in sprint,
        2.79 in kick). Part of the torso, so it twists/leans with the shirt
        and stays over the seam. Pocket moved up to clear it. */}
    <RBox size={[2.34, 0.6, 1.24]} color={COLORS.hoodieDark} position={[0, 2.6, 0]} radius={0.07} />
          <RBox size={[1.5, 0.2, 1.15]} color={COLORS.hoodieDark} position={[0, 4.3, 0]} radius={0.08} />
          <RBox size={[0.7, 0.3, 0.7]} color={COLORS.skin} position={[0, 4.42, 0]} radius={0.06} rough={0.55} />
          {/* pocket */}
          <RBox size={[1.2, 0.58, 0.1]} color={COLORS.hoodieDark} position={[0, 3.05, 0.52]} radius={0.05} />
          {/* drawstrings */}
          {[-0.2, 0.2].map((x) => (
            <group key={x}>
              <mesh position={[x, 3.95, 0.52]}><cylinderGeometry args={[0.04, 0.04, 0.55, 8]} /><meshStandardMaterial color={COLORS.string} /></mesh>
              <mesh position={[x, 3.66, 0.52]}><sphereGeometry args={[0.06, 10, 10]} /><meshStandardMaterial color={COLORS.string} /></mesh>
            </group>
          ))}
          {/* lightning bolt */}
          <mesh position={[0, 3.5, 0.5]} scale={[0.95, 0.95, 1]}>
            <extrudeGeometry args={[boltShape, {depth: 0.05, bevelEnabled: false}]} />
            <meshStandardMaterial color={COLORS.bolt} roughness={0.4} />
          </mesh>
          <Arm side={-1} p={p.armL} />
          <Arm side={1} p={p.armR} />
          <Headphones />
          {/* head */}
          <group position={[0, 5.17, 0]} rotation={p.head}>
            <RBox size={[1.4, 1.45, 1.4]} color={COLORS.skin} radius={0.2} rough={0.55} />
            <mesh position={[0, -0.05, 0.705]}><planeGeometry args={[1.3, 1.3]} /><meshStandardMaterial map={face} transparent roughness={0.6} /></mesh>
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
