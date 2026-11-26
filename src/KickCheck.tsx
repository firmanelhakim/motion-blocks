import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {Stage, clipPose} from './kit/kit';
import {BoltBoy} from './components/BoltBoy';

/**
 * KickCheck — the kick clip alone, from a side profile, so the direction
 * reads unambiguously: the character faces screen-right, so a forward kick
 * moves the leg to the RIGHT and a backward kick moves it to the LEFT.
 * The PoseLab's front 3/4 camera foreshortens the forward swing (it moves
 * mostly toward the camera), which is why the same kick can read as
 * backward in the full video while the peak still looks right.
 *
 * 2s / 60 frames: two kicks, same timing as the PoseLab segment.
 */
export const KickCheck: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  return (
    <Stage shadows cameraPosition={[14, 4, 0]} lookAt={[0, 3, 0]} fov={30}>
      <BoltBoy pose={clipPose('kick', t)} />
    </Stage>
  );
};
