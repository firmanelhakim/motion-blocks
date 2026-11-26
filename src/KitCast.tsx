/**
 * KitCast — the engine's two kit cast members side by side: BoltBoy and
 * CasualMan, standing idle on the kit Stage with the engine's ground shadow.
 * The cast shot for the better engine.
 */
import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {Stage, clipPose} from './kit/kit';
import {BoltBoy} from './components/BoltBoy';
import {CasualMan} from './components/CasualMan';

const LABEL: React.CSSProperties = {
  position: 'absolute',
  bottom: 28,
  left: 40,
  fontFamily: 'Inter, sans-serif',
  fontSize: 22,
  fontWeight: 700,
  color: '#475569',
  letterSpacing: 1,
};

export const KitCast: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  return (
    <AbsoluteFill>
      <Stage shadows>
        <BoltBoy pose={clipPose('idle', t)} position={[-2.2, 0, 0]} />
        <CasualMan pose={clipPose('idle', t)} position={[2.2, 0, 0]} />
      </Stage>
      <div style={LABEL}>KIT CAST · BOLTBOY + CASUALMAN</div>
    </AbsoluteFill>
  );
};
