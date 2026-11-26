import React from 'react';
import { RobloxShortComposition } from './RobloxShortComposition';
import { RobloxShortStory } from './types/schema';

/**
 * KitStoryCheck — verifies the kit BoltBoy renders inside the story pipeline.
 * Hero is the canonical kit BoltBoy (cast marker `{kit: 'boltboy'}`), friend
 * is an R6 preset — so one render exercises both the kit branch and the
 * R6 branch of RobloxShortComposition. Minimal street scene, 90 frames.
 * This is a test composition only; it does not touch currentStory.ts.
 */
const TEST_STORY: RobloxShortStory = {
  title: 'KIT STORY CHECK',
  fps: 30,
  durationInFrames: 90,
  width: 1080,
  height: 1920,
  cast: {
    hero: { kit: 'boltboy' },
    friend: 'kid_girl',
  },
  scenes: [
    {
      id: 'scene-street',
      location: 'street',
      startFrame: 0,
      endFrame: 90,
      cameraShots: [
        {
          startFrame: 0,
          endFrame: 90,
          fromPos: [0, 5, 18],
          toPos: [0, 5, 18],
          fromTarget: [-0.5, 3, 0.5],
          toTarget: [-0.5, 3, 0.5],
          fov: 50,
        },
      ],
      characters: {
        hero: [
          { frame: 0, position: [-4, 0, 0.5], rotationY: 0.3, anim: 'walk', expression: 'grin' },
          { frame: 45, position: [-2, 0, 0.5], rotationY: 0.3, anim: 'wave', expression: 'grin' },
          { frame: 90, position: [-2, 0, 0.5], rotationY: 0.3, anim: 'wave', expression: 'grin' },
        ],
        friend: [
          { frame: 0, position: [3, 0, 0.5], rotationY: -0.3, anim: 'wave', expression: 'smile' },
          { frame: 90, position: [3, 0, 0.5], rotationY: -0.3, anim: 'wave', expression: 'smile' },
        ],
      },
    },
  ],
  captions: [],
};

export const KitStoryCheck: React.FC = () => {
  return <RobloxShortComposition story={TEST_STORY} />;
};
