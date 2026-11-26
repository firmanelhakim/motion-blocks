/**
 * AssetCheck — verification stills for the 11 new-asset ports
 * (2026-11-22). One composition, driven by inputProps:
 * {asset, camPos, camLook, fov, walk?, bg?, shadows?}.
 * Renders a single asset on the kit Stage (or the ice-street location) so
 * renderStill can capture it from the source's reference camera. Dev check
 * tool only — the story pipeline never references it.
 */
import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {Stage, type V3} from './kit/kit';
import {BlockyFish} from './components/BlockyFish';
import {BubblesUnderwater} from './components/BubblesUnderwater';
import {BlockyBrain} from './components/BlockyBrain';
import {BigClock} from './components/BigClock';
import {BlueSun} from './components/BlueSun';
import {BlueLightPlant} from './components/BlueLightPlant';
import {GiantFerns} from './components/GiantFerns';
import {BlockyVolcano} from './components/BlockyVolcano';
import {BlockyTRex} from './components/BlockyTRex';
import {BlockyRobot} from './components/BlockyRobot';
import {IceStreetEnvironment, SlidingBoy} from './environments/ice-street';
import {R6Character} from './components/R6Character';
import {lookForActor} from './characters/look';

export interface AssetCheckProps {
  asset?: string;
  camPos?: V3;
  camLook?: V3;
  fov?: number;
  walk?: number;
  bg?: string;
  shadows?: boolean;
}

export const AssetCheck: React.FC<AssetCheckProps> = ({asset = 'fish', camPos = [4.8, 1.6, 7.6], camLook = [0, 0.1, 0], fov = 34, walk = 0, bg, shadows = true}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const p: {t: number; duration: number; position: V3; rotation: V3; scale: number} = {t, duration: 3, position: [0, 0, 0], rotation: [0, 0, 0], scale: 1};
  return (
    <AbsoluteFill>
      <Stage cameraPosition={camPos} lookAt={camLook} fov={fov} background={bg} shadows={shadows}>
        {asset === 'fish' && <BlockyFish {...p} />}
        {asset === 'bubbles' && <BubblesUnderwater {...p} />}
        {asset === 'brain' && <BlockyBrain {...p} />}
        {asset === 'clock' && <BigClock {...p} />}
        {asset === 'blue-sun' && <BlueSun {...p} />}
        {asset === 'plant' && <BlueLightPlant {...p} />}
        {asset === 'ferns' && <GiantFerns {...p} />}
        {asset === 'volcano' && <BlockyVolcano {...p} />}
        {asset === 'trex' && <BlockyTRex {...p} walk={walk} />}
        {asset === 'robot' && <BlockyRobot {...p} />}
        {asset === 'ice-street' && <IceStreetEnvironment />}
        {asset === 'sliding-boy' && <SlidingBoy t={t} duration={3} />}
        {asset === 'gills' && (
          <R6Character
            look={lookForActor('kid_boy', {kid_boy: {extends: 'kid_boy', accessories: ['gills']}})}
            position={[0, 0, 0]}
            rotationY={0}
            anim="idle"
            expression="smile"
          />
        )}
      </Stage>
    </AbsoluteFill>
  );
};
