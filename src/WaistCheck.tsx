import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {Stage, clipPose, ClipName} from './kit/kit';
import {BoltBoy} from './components/BoltBoy';
import {CasualMan} from './components/CasualMan';
import {WingedBoy} from './components/WingedBoy';

/**
 * WaistCheck — any kit character, any single clip, from the KitPoseLab
 * front 3/4 camera ([7, 5, 16], lookAt [0, 4.2, 0]). Temporary verification
 * composition for the pants/shirt waist seam across characters.
 * Takes `character` ('boltboy' | 'casualman' | 'wingedboy') and `clip`
 * via inputProps. 2s / 60 frames.
 */
export const WaistCheck: React.FC<{character?: string; clip?: ClipName}> = ({
  character = 'boltboy',
  clip = 'dance',
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const pose = clipPose(clip, t);
  return (
    <Stage shadows cameraPosition={[7, 5, 16]} lookAt={[0, 4.2, 0]} fov={30}>
      {character === 'casualman' ? (
        <CasualMan pose={pose} />
      ) : character === 'wingedboy' ? (
        <WingedBoy pose={pose} />
      ) : (
        <BoltBoy pose={pose} />
      )}
    </Stage>
  );
};
