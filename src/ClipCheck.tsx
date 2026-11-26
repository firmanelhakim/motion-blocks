import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {Stage, clipPose, ClipName} from './kit/kit';
import {BoltBoy} from './components/BoltBoy';

/**
 * ClipCheck — any single clip, alone, so a new clip can be judged by eye
 * before it goes into a timeline. Takes `clip` and `side` via inputProps.
 * Front 3/4 camera is the KitPoseLab angle ([7, 5, 16], lookAt [0, 4.2, 0]);
 * `side` switches to the KickCheck side profile ([14, 4, 0], lookAt [0, 3, 0]).
 * 2s / 60 frames.
 */
export const ClipCheck: React.FC<{clip?: ClipName; side?: boolean}> = ({clip = 'walk', side = false}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  return (
    <Stage shadows cameraPosition={side ? [14, 4, 0] : [7, 5, 16]} lookAt={side ? [0, 3, 0] : [0, 4.2, 0]} fov={30}>
      <BoltBoy pose={clipPose(clip, t)} />
    </Stage>
  );
};
