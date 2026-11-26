import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {Stage, clipPose} from './kit/kit';
import {WingedBoy} from './components/WingedBoy';

/**
 * KitFly — WingedBoy flying in place on the fly clip, 3s (90 frames).
 * Camera pulled back and raised so the wings and the hover stay framed;
 * the ground shadow sits under him, detached, which is the point — he is
 * airborne. Flap extremes: frame 8 (wings wide, t=0.25s) and frame 23
 * (wings folded, t=0.75s) of the 1s flap cycle.
 */
export const KitFly: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  return (
    <Stage cameraPosition={[7.5, 5.8, 19]} lookAt={[0, 5.0, 0]} fov={30} shadows>
      <WingedBoy pose={clipPose('fly', t)} />
    </Stage>
  );
};
