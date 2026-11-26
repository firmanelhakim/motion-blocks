import React from 'react';
import { AbsoluteFill } from 'remotion';
import { ThreeCanvas } from '@remotion/three';
import { useThree } from '@react-three/fiber';
import { R6Character } from './components/R6Character';
import { CHARACTER_PRESETS } from './characters/look';

/**
 * Bolt Boy showcase — the same two-view turntable as the maintainer's reference
 * image (front + three-quarter), on a plain light background.
 *   npx remotion still src/index.ts BoltBoyShowcase out/bolt-boy.png --frame=15
 * The character itself is the `bolt_boy` preset in src/characters/look.ts;
 * this composition is only the demo frame. Use the preset in any story via
 *   cast: { bolt_boy: 'bolt_boy' }
 * with expression 'grin' and anim 'idle' / 'walk' / 'wave'.
 */

const CAM_Z = 16.5;
const FOV = 32;

const FixedCamera: React.FC = () => {
  const { camera } = useThree();
  camera.position.set(0, 3.6, CAM_Z);
  camera.lookAt(0, 3.1, 0);
  return null;
};

export const BoltBoyShowcase: React.FC = () => {
  const look = CHARACTER_PRESETS.bolt_boy;
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
        {/* Front view, as in the reference (left figure) */}
        <R6Character look={look} position={[-3.2, 0, 0]} rotationY={0} anim="idle" expression="grin" />
        {/* Three-quarter view, as in the reference (right figure) */}
        <R6Character look={look} position={[3.2, 0, 0]} rotationY={-0.5} anim="idle" expression="grin" />
      </ThreeCanvas>
    </AbsoluteFill>
  );
};
