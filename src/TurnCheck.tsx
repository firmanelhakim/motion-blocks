/**
 * TurnCheck — verifies withTurn (the ported turntable helper): BoltBoy
 * idling while slowly turning, one full turn in 4s. At t=1s he has turned
 * 90°, at t=2s 180° (back to camera). Registered as `TurnCheck`, 120f.
 */
import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Stage, clipPose, withTurn} from './kit/kit';
import {BoltBoy} from './components/BoltBoy';

export const TurnCheck: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / 30;
  const pose = withTurn(clipPose('idle', t), t, 4);
  return (
    <Stage shadows>
      <BoltBoy pose={pose} />
    </Stage>
  );
};
