import React from 'react';
import { AbsoluteFill } from 'remotion';
import { ThreeCanvas } from '@remotion/three';
import { useThree } from '@react-three/fiber';
import { R6Character } from './components/R6Character';
import { CHARACTER_PRESETS } from './characters/look';

/**
 * The engine's classic_noob walking — R6Character, anim="walk", classic
 * smile. 3/4 camera matching the kit redraw's walk video (NoobWalk), so the
 * two videos sit side by side.
 *   npx remotion render src/index.ts NoobEngineWalk out/noob-engine-walk.mp4 --gl=angle
 *
 * Note: the engine's walk runs at speed 7.5 (cycle ~0.84s), so a 3s clip
 * holds ~3.58 cycles and does not loop seamlessly, unlike the kit's 1s
 * walk cycle. It is a straight 3s walk clip, not a seamless loop.
 */

const FixedCamera: React.FC = () => {
  const { camera } = useThree();
  camera.position.set(6.5, 4.0, 13.5);
  camera.lookAt(0, 3.45, 0);
  return null;
};

export const NoobEngineWalk: React.FC = () => {
  const look = CHARACTER_PRESETS.classic_noob;
  return (
    <AbsoluteFill style={{ backgroundColor: '#F2F2F2' }}>
      <ThreeCanvas width={1280} height={720} shadows camera={{ fov: 30, near: 0.1, far: 200 }}>
        <color attach="background" args={['#F2F2F2']} />
        <FixedCamera />
        <ambientLight intensity={0.85} />
        <hemisphereLight args={['#FFFFFF', '#94A3B8', 0.65]} position={[0, 25, 0]} />
        <directionalLight position={[12, 22, 14]} intensity={2.1} color="#FFFBEB" castShadow />
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
          <planeGeometry args={[200, 200]} />
          <shadowMaterial opacity={0.22} />
        </mesh>
        <R6Character look={look} position={[0, 0, 0]} rotationY={0} anim="walk" expression="smile" />
      </ThreeCanvas>
    </AbsoluteFill>
  );
};
