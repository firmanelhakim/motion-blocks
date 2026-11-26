import React from 'react';
import { Composition, registerRoot } from 'remotion';
import { MotionBlocksComposition } from './MotionBlocksComposition';
import { CURRENT_STORY } from './story/currentStory';

/**
 * Slim Remotion entry point for headless production renders of `MotionBlocks`.
 * Excludes the ~20 showcase/lab compositions in `src/Root.tsx` so bundling and
 * Chromium startup on CPU-only VPSes are smaller and faster.
 */
const ShortRoot: React.FC = () => (
  <Composition
    id="MotionBlocks"
    component={MotionBlocksComposition}
    durationInFrames={CURRENT_STORY.durationInFrames}
    fps={CURRENT_STORY.fps}
    width={CURRENT_STORY.width}
    height={CURRENT_STORY.height}
  />
);

registerRoot(ShortRoot);
