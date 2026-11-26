import React from 'react';
import { Composition } from 'remotion';
import { MotionBlocksComposition } from './MotionBlocksComposition';
import { CURRENT_STORY } from './story/currentStory';
import { GALLERY_PAGES, LocationGallery } from './LocationGallery';
import { CharacterLineup, FRAMES_PER_PAGE, LINEUP_PAGES } from './CharacterLineup';
import { BoltBoyShowcase } from './BoltBoyShowcase';
import { BoltBoyCompare, BoltBoyKitShowcase, BoltBoyWalk } from './BoltBoyCompare';
import { NoobEngineShowcase } from './NoobEngineShowcase';
import { NoobEngineWalk } from './NoobEngineWalk';
import { KitPoseLab } from './KitPoseLab';
import { KitCast } from './KitCast';
import { KitFly } from './KitFly';
import { KitFlyWave } from './KitFlyWave';
import { FaceLab } from './FaceLab';
import { KickCheck } from './KickCheck';
import { BowCheck } from './BowCheck';
import { ClipCheck } from './ClipCheck';
import { R6KitCheck } from './R6KitCheck';
import { KitStoryCheck } from './KitStoryCheck';
import { CircleShowcase } from './CircleShowcase';
import { TurnCheck } from './TurnCheck';
import { WaistCheck } from './WaistCheck';
import { PerformanceLab } from './PerformanceLab';
import { AssetCheck } from './AssetCheck';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MotionBlocks"
        component={MotionBlocksComposition}
        durationInFrames={CURRENT_STORY.durationInFrames}
        fps={CURRENT_STORY.fps}
        width={CURRENT_STORY.width}
        height={CURRENT_STORY.height}
      />
      <Composition
        id="BoltBoyShowcase"
        component={BoltBoyShowcase}
        durationInFrames={30}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="BoltBoyCompare"
        component={BoltBoyCompare}
        durationInFrames={30}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="BoltBoyWalk"
        component={BoltBoyWalk}
        durationInFrames={30}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="BoltBoyKitShowcase"
        component={BoltBoyKitShowcase}
        durationInFrames={30}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="NoobEngineShowcase"
        component={NoobEngineShowcase}
        durationInFrames={30}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="NoobEngineWalk"
        component={NoobEngineWalk}
        durationInFrames={90}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="KitPoseLab"
        component={KitPoseLab}
        durationInFrames={696}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="KitCast"
        component={KitCast}
        durationInFrames={30}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="KitFly"
        component={KitFly}
        durationInFrames={90}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="KitFlyWave"
        component={KitFlyWave}
        durationInFrames={180}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="FaceLab"
        component={FaceLab}
        durationInFrames={30}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="KickCheck"
        component={KickCheck}
        durationInFrames={60}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="BowCheck"
        component={BowCheck}
        durationInFrames={60}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="ClipCheck"
        component={ClipCheck}
        durationInFrames={60}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="R6KitCheck"
        component={R6KitCheck}
        durationInFrames={60}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="KitStoryCheck"
        component={KitStoryCheck}
        durationInFrames={90}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="CircleShowcase"
        component={CircleShowcase}
        durationInFrames={900}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="WaistCheck"
        component={WaistCheck}
        durationInFrames={60}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="TurnCheck"
        component={TurnCheck}
        durationInFrames={120}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="PerformanceLab"
        component={PerformanceLab}
        durationInFrames={240}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="CharacterLineup"
        component={CharacterLineup}
        durationInFrames={FRAMES_PER_PAGE * LINEUP_PAGES}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="LocationGallery"
        component={LocationGallery}
        durationInFrames={GALLERY_PAGES.length}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="AssetCheck"
        component={AssetCheck}
        durationInFrames={90}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{asset: 'fish', camPos: [4.8, 1.6, 7.6], camLook: [0, 0.1, 0], fov: 34}}
      />
    </>
  );
};
