import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { ThreeCanvas } from '@remotion/three';
import { useThree } from '@react-three/fiber';
import { R6Character } from './components/R6Character';
import { BoltBoy } from './components/BoltBoy';
import { CHARACTER_PRESETS } from './characters/look';

/**
 * Side-by-side: my Bolt Boy (R6 preset `bolt_boy`, left) vs the maintainer's
 * BoltBoy.tsx (right), both front-facing, standing idle, same camera.
 * BoltBoy is taller (~7.1 studs vs the R6's ~5.9), so the size gap is
 * real and shown honestly — scale it 0.83 to match R6 cast height.
 *   npx remotion still src/index.ts BoltBoyCompare out/compare.png --frame=15
 */

const CAM_Z = 19;
const FOV = 32;

const FixedCamera: React.FC = () => {
  const { camera } = useThree();
  camera.position.set(0, 3.9, CAM_Z);
  camera.lookAt(0, 3.4, 0);
  return null;
};

const Scene: React.FC = () => (
  <>
    <color attach="background" args={['#F2F2F2']} />
    <FixedCamera />
    <ambientLight intensity={0.85} />
    <hemisphereLight args={['#FFFFFF', '#94A3B8', 0.65]} position={[0, 25, 0]} />
    <directionalLight position={[12, 22, 14]} intensity={2.1} color="#FFFBEB" castShadow />
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
      <planeGeometry args={[200, 200]} />
      <shadowMaterial opacity={0.22} />
    </mesh>
    <R6Character look={CHARACTER_PRESETS.bolt_boy} position={[-3.4, 0, 0]} rotationY={0} anim="idle" expression="grin" />
    <BoltBoy t={0} walk={0} position={[3.4, 0, 0]} rotation={[0, 0, 0]} scale={1} />
  </>
);

const Label: React.FC<{ left: boolean; children: React.ReactNode }> = ({ left, children }) => (
  <div
    style={{
      position: 'absolute',
      bottom: 36,
      left: left ? 48 : undefined,
      right: left ? undefined : 48,
      fontFamily: 'Inter, sans-serif',
      fontSize: 26,
      fontWeight: 700,
      color: '#475569',
      letterSpacing: 1,
    }}
  >
    {children}
  </div>
);

export const BoltBoyCompare: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#F2F2F2' }}>
    <ThreeCanvas width={1920} height={1080} shadows camera={{ fov: FOV, near: 0.1, far: 200 }}>
      <Scene />
    </ThreeCanvas>
    <Label left>MINE · R6 PRESET “BOLT_BOY”</Label>
    <Label left={false}>YOURS · BOLTBOY.TSX</Label>
  </AbsoluteFill>
);

/** BoltBoy front + three-quarter, idle — the adoption showcase. */
export const BoltBoyKitShowcase: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#F2F2F2' }}>
    <ThreeCanvas width={1920} height={1080} shadows camera={{ fov: FOV, near: 0.1, far: 200 }}>
      <color attach="background" args={['#F2F2F2']} />
      <FixedCamera />
      <ambientLight intensity={0.85} />
      <hemisphereLight args={['#FFFFFF', '#94A3B8', 0.65]} position={[0, 25, 0]} />
      <directionalLight position={[12, 22, 14]} intensity={2.1} color="#FFFBEB" castShadow />
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
        <planeGeometry args={[200, 200]} />
        <shadowMaterial opacity={0.22} />
      </mesh>
      <BoltBoy t={0} walk={0} position={[-3.4, 0, 0]} rotation={[0, 0, 0]} scale={1} />
      <BoltBoy t={0} walk={0} position={[3.4, 0, 0]} rotation={[0, -0.5, 0]} scale={1} />
    </ThreeCanvas>
  </AbsoluteFill>
);

/** BoltBoy mid-walk, t driven by the frame clock, to check the walk cycle. */
export const BoltBoyWalk: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: '#F2F2F2' }}>
      <ThreeCanvas width={1920} height={1080} shadows camera={{ fov: FOV, near: 0.1, far: 200 }}>
        <color attach="background" args={['#F2F2F2']} />
        <FixedCamera />
        <ambientLight intensity={0.85} />
        <hemisphereLight args={['#FFFFFF', '#94A3B8', 0.65]} position={[0, 25, 0]} />
        <directionalLight position={[12, 22, 14]} intensity={2.1} color="#FFFBEB" castShadow />
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
          <planeGeometry args={[200, 200]} />
          <shadowMaterial opacity={0.22} />
        </mesh>
        <BoltBoy t={frame / fps} walk={1} position={[0, 0, 0]} rotation={[0, 0, 0]} scale={1} />
      </ThreeCanvas>
    </AbsoluteFill>
  );
};
