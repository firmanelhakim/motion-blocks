import React from 'react';
import { AbsoluteFill } from 'remotion';
import { ThreeCanvas } from '@remotion/three';
import { useThree } from '@react-three/fiber';
import { R6Character } from './components/R6Character';
import { CHARACTER_PRESETS } from './characters/look';

/**
 * Classic Noob as the engine renders him — R6Character, cylinder head with a
 * wrapped face decal, texture-mapped tee. Front view, idle, classic smile.
 * The other half of the side-by-side with the kit redraw
 * (casualman-source/src/ClassicNoob.tsx).
 *   npx remotion still src/index.ts NoobEngineShowcase out/noob-engine.png --frame=15
 */

const CAM_Z = 16.5;
const FOV = 32;

const FixedCamera: React.FC = () => {
  const { camera } = useThree();
  camera.position.set(0, 3.6, CAM_Z);
  camera.lookAt(0, 3.1, 0);
  return null;
};

export const NoobEngineShowcase: React.FC = () => {
  const look = CHARACTER_PRESETS.classic_noob;
  return (
    <AbsoluteFill style={{ backgroundColor: '#F2F2F2' }}>
      <ThreeCanvas width={1280} height={720} shadows camera={{ fov: FOV, near: 0.1, far: 200 }}>
        <color attach="background" args={['#F2F2F2']} />
        <FixedCamera />
        <ambientLight intensity={0.85} />
        <hemisphereLight args={['#FFFFFF', '#94A3B8', 0.65]} position={[0, 25, 0]} />
        <directionalLight position={[12, 22, 14]} intensity={2.1} color="#FFFBEB" castShadow />
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
          <planeGeometry args={[200, 200]} />
          <shadowMaterial opacity={0.22} />
        </mesh>
        <R6Character look={look} position={[0, 0, 0]} rotationY={0} anim="idle" expression="smile" />
      </ThreeCanvas>
      <div
        style={{
          position: 'absolute',
          bottom: 28,
          left: 40,
          fontFamily: 'Inter, sans-serif',
          fontSize: 22,
          fontWeight: 700,
          color: '#475569',
          letterSpacing: 1,
        }}
      >
        ENGINE · R6CHARACTER — CLASSIC_NOOB
      </div>
    </AbsoluteFill>
  );
};
