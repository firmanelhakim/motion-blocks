import React from 'react';
import { Composition, registerRoot } from 'remotion';
import { RobloxShortComposition } from './RobloxShortComposition';
import { CURRENT_STORY } from './story/currentStory';

/**
 * Slim Remotion entry point for headless production renders of `RobloxShort`.
 * Excludes the ~20 showcase/lab compositions in `src/Root.tsx` so bundling and
 * Chromium startup on CPU-only VPSes are smaller and faster.
 */
const ShortRoot: React.FC = () => (
  <Composition
    id="RobloxShort"
    component={RobloxShortComposition}
    durationInFrames={CURRENT_STORY.durationInFrames}
    fps={CURRENT_STORY.fps}
    width={CURRENT_STORY.width}
    height={CURRENT_STORY.height}
  />
);

registerRoot(ShortRoot);
