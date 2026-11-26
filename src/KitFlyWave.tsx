import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {Stage, clipPose, layerPose, orbitPath} from './kit/kit';
import {WingedBoy} from './components/WingedBoy';

/**
 * KitFlyWave — combined movements, all at once. WingedBoy flies in a
 * circle around the stage while waving with his right hand, 6s (180
 * frames). Three combination modes in one demo:
 *   - Layer: fly for the body, legs, head and wings + wave for the right
 *     arm only (`layerPose(fly, wave, ['armR'])`).
 *   - Path: the fly clip keeps playing while `orbitPath` moves him around
 *     the circle and turns him to face where he is going — pose and path
 *     are independent tracks.
 *   - Sequence (not shown here, already proven by PoseLab): the timeline
 *     plays clips one after another with a crossfade, e.g. fly → wave.
 * Camera is wide enough to hold the whole circle (radius 4).
 */
export const KitFlyWave: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const pose = layerPose(clipPose('fly', t), clipPose('wave', t), ['armR']);
  const path = orbitPath(t, {radius: 4, duration: 6});
  return (
    <Stage cameraPosition={[0, 6, 24]} lookAt={[0, 4.5, 0]} fov={30} shadows>
      <WingedBoy pose={pose} position={path.position} rotation={[0, path.yaw, 0]} />
    </Stage>
  );
};
