import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {Stage, clipPose, ClipName} from './kit/kit';
import {R6Character} from './components/R6Character';
import {CHARACTER_PRESETS, PresetName} from './characters/look';

/**
 * R6KitCheck — any R6 preset doing any kit clip, alone, so the kit-pose
 * integration can be judged by eye. Takes `preset` and `clip` via
 * inputProps. The R6 rig is shorter than the kit rig (~5.9 vs ~7.1 studs),
 * so the camera sits lower than the KitPoseLab angle.
 * 2s / 60 frames. (2026-11-21)
 */
export const R6KitCheck: React.FC<{preset?: PresetName; clip?: ClipName; side?: boolean}> = ({
  preset = 'kid_boy',
  clip = 'walk',
  side = false,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  return (
    <Stage shadows cameraPosition={side ? [14, 4, 0] : [7, 4, 16]} lookAt={side ? [0, 2.5, 0] : [0, 2.8, 0]} fov={30}>
      <R6Character
        look={CHARACTER_PRESETS[preset]}
        position={[0, 0, 0]}
        rotationY={0}
        expression="smile"
        pose={clipPose(clip, t)}
      />
    </Stage>
  );
};
