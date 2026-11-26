import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {Stage, clipPose} from './kit/kit';
import {BoltBoy} from './components/BoltBoy';

/**
 * BowCheck — the bow clip alone, from a side profile, so the torso bend
 * reads unambiguously. The PoseLab's front 3/4 camera foreshortens a
 * forward bend (it moves mostly toward the camera), so a correct bow can
 * read as a head nod in the full video while the torso looks upright.
 * From the side, a real bow shows the torso leaning forward clearly;
 * if the torso stays upright here, the lean is genuinely not applying.
 *
 * 2s / 60 frames: one full bow (1.6s cycle) plus a little.
 */
export const BowCheck: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  return (
    <Stage shadows cameraPosition={[14, 4, 0]} lookAt={[0, 3, 0]} fov={30}>
      <BoltBoy pose={clipPose('bow', t)} />
    </Stage>
  );
};
