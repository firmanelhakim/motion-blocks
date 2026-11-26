/**
 * Declarative preset catalog replacing the ~45 one-off root `render-*.mjs`
 * verification scripts. Run any preset via:
 *   node scripts/render.mjs preset <name> [--preview] [--port 3050]
 *
 * Stills only in this staging port: the upstream `circle-video` and
 * `circle-segments` presets were dropped entirely (video rendering is
 * excluded from this selective port), and video entries in the remaining
 * presets are recorded as data only — the CLI renders their stills and
 * reports the video outputs as skipped.
 */
import path from 'node:path';
import { defaultOutDir } from './render_lib.mjs';

function rotY(cam, look, deg) {
  const a = (deg * Math.PI) / 180;
  const dx = cam[0] - look[0];
  const dz = cam[2] - look[2];
  const c = Math.cos(a);
  const s = Math.sin(a);
  return [look[0] + dx * c - dz * s, cam[1], look[2] + dx * s + dz * c];
}

const BLUE_SKY = 'linear-gradient(180deg, #0b3d91 0%, #1d6fb8 55%, #7dd3fc 100%)';
const ICE_SKY = 'linear-gradient(180deg, #9ad6f5 0%, #c0e4f8 55%, #dfeffa 100%)';

function twoAssetStills(outRoot, slug, asset, cam, look, fov, extra = {}) {
  return [
    {
      id: 'AssetCheck',
      frame: 0,
      output: path.join(outRoot, slug, 'front-t0.png'),
      inputProps: { asset, camPos: cam, camLook: look, fov, walk: extra.walk ?? 0, bg: extra.bg, shadows: extra.shadows ?? true },
    },
    {
      id: 'AssetCheck',
      frame: 45,
      output: path.join(outRoot, slug, 'three-quarter-t1.5.png'),
      inputProps: { asset, camPos: rotY(cam, look, 40), camLook: look, fov, walk: extra.walk ?? 0, bg: extra.bg, shadows: extra.shadows ?? true },
    },
  ];
}

export function getPresets() {
  const OUT = defaultOutDir();
  const ASSETS_OUT = defaultOutDir('new-assets');
  const CIRCLE_OUT = defaultOutDir('circle');
  const R6KIT_OUT = defaultOutDir('r6kit');
  const DIALOGUE_OUT = defaultOutDir('dialogue');

  return {
    kickcheck: {
      description: 'KickCheck side-profile peaks (2 stills)',
      stills: [
        { id: 'KickCheck', frame: 7, output: path.join(OUT, 'kickcheck-side-peak1.png') },
        { id: 'KickCheck', frame: 34, output: path.join(OUT, 'kickcheck-side-peak2.png') },
      ],
      videos: [],
    },
    'kit-fly': {
      description: 'WingedBoy KitFly stills',
      stills: [
        { id: 'KitFly', frame: 8, output: path.join(OUT, 'kit-fly-top.png') },
        { id: 'KitFly', frame: 23, output: path.join(OUT, 'kit-fly-bottom.png') },
      ],
      videos: [],
    },
    'kit-flywave': {
      description: 'WingedBoy KitFlyWave stills',
      stills: [
        { id: 'KitFlyWave', frame: 0, output: path.join(OUT, 'kit-flywave-front.png') },
        { id: 'KitFlyWave', frame: 90, output: path.join(OUT, 'kit-flywave-back.png') },
      ],
      videos: [],
    },
    'kit-poselab': {
      description: 'KitPoseLab showcase stills',
      // The 6 peak stills from render-kit-poselab.mjs, kept here so the
      // upstream preset's stills-less form does not drop them:
      // 300 sprint (mid-stride) · 337 march (high knee) ·
      // 396 cheer (arms up + jump) · 455 punch (thrust) ·
      // 522 bow (bent) · 577 kick (leg up).
      stills: [
        [300, 'kit-poselab-sprint.png'],
        [337, 'kit-poselab-march.png'],
        [396, 'kit-poselab-cheer.png'],
        [455, 'kit-poselab-punch.png'],
        [522, 'kit-poselab-bow.png'],
        [577, 'kit-poselab-kick.png'],
      ].map(([frame, file]) => ({
        id: 'KitPoseLab',
        frame,
        output: path.join(OUT, file),
      })),
      videos: [],
    },
    'circle-stills': {
      description: 'CircleShowcase 8 evenly spaced verification stills',
      stills: [0, 112, 225, 337, 450, 562, 675, 787].map((frame) => ({
        id: 'CircleShowcase',
        frame,
        output: path.join(CIRCLE_OUT, `circle-${frame}.png`),
      })),
      videos: [],
    },
    r6kit: {
      description: 'R6KitCheck preset/clip verification stills',
      stills: [
        ['teacher', 'walk', 15], ['teacher', 'wave', 15],
        ['teacher', 'kick', 7], ['teacher', 'dance', 7],
        ['bully', 'kick', 7], ['bully', 'dance', 7],
        ['kid_boy', 'wave', 15], ['kid_boy', 'walk', 15],
        ['bolt_boy', 'dance', 7], ['bolt_boy', 'kick', 7],
      ].map(([preset, clip, frame]) => ({
        id: 'R6KitCheck',
        frame,
        inputProps: { preset, clip },
        output: path.join(R6KIT_OUT, `r6-${preset}-${clip}-${frame}.png`),
      })),
      videos: [],
    },
    facelab: {
      description: 'FaceLab expression regression stills',
      stills: [
        [{ character: 'blockboy', expression: 'grin' }, 'facelab-blockboy-grin.png'],
        [{ character: 'blockboy', expression: 'cry', expressionT: 0.5 }, 'facelab-blockboy-cry.png'],
        [{ character: 'blockboy', expression: 'laugh' }, 'facelab-blockboy-laugh.png'],
        [{ character: 'blockboy', expression: 'shocked' }, 'facelab-blockboy-shocked.png'],
        [{ character: 'blockboy', expression: 'cool' }, 'facelab-blockboy-cool.png'],
        [{ character: 'blockboy', expression: 'love' }, 'facelab-blockboy-love.png'],
        [{ character: 'blockboy', expression: 'angry' }, 'facelab-blockboy-angry.png'],
        [{ character: 'blockboy', expression: 'dizzy' }, 'facelab-blockboy-dizzy.png'],
        [{ character: 'casualman', expression: 'smile' }, 'facelab-casualman-smile.png'],
        [{ character: 'wingedboy', expression: 'smirk' }, 'facelab-wingedboy-smirk.png'],
        [{ character: 'wingedboy', expression: 'cry', expressionT: 0.5 }, 'facelab-wingedboy-cry.png'],
        [{ character: 'wingedboy', expression: 'laugh' }, 'facelab-wingedboy-laugh.png'],
        [{ character: 'wingedboy', expression: 'shocked' }, 'facelab-wingedboy-shocked.png'],
        [{ character: 'wingedboy', expression: 'cool' }, 'facelab-wingedboy-cool.png'],
        [{ character: 'wingedboy', expression: 'love' }, 'facelab-wingedboy-love.png'],
        [{ character: 'wingedboy', expression: 'angry' }, 'facelab-wingedboy-angry.png'],
        [{ character: 'wingedboy', expression: 'dizzy' }, 'facelab-wingedboy-dizzy.png'],
      ].map(([inputProps, file]) => ({
        id: 'FaceLab',
        frame: 0,
        inputProps,
        output: path.join(OUT, file),
      })),
      videos: [],
    },
    'dialogue-test': {
      description: 'RobloxShort chat-bubble verification stills',
      stills: [195, 285, 375, 480].map((frame) => ({
        id: 'RobloxShort',
        frame,
        output: path.join(DIALOGUE_OUT, `dialogue-f${frame}.png`),
      })),
      videos: [],
    },
    'asset-stills': {
      description: '11 new-asset verification stills',
      stills: [
        ...twoAssetStills(ASSETS_OUT, 'fish', 'fish', [4.8, 1.6, 7.6], [0, 0.1, 0], 34),
        ...twoAssetStills(ASSETS_OUT, 'bubbles', 'bubbles', [0, 0.6, 11.8], [0, 0.15, 0], 40),
        ...twoAssetStills(ASSETS_OUT, 'brain', 'brain', [0.8, 0.78, 9.6], [0.15, -0.15, 0], 38),
        ...twoAssetStills(ASSETS_OUT, 'clock', 'clock', [2.4, 0.33, 9.6], [0.2, -0.15, 0], 38),
        ...twoAssetStills(ASSETS_OUT, 'blue-sun', 'blue-sun', [0, 3.05, 13.5], [0, 3.1, -6], 44, { bg: BLUE_SKY }),
        ...twoAssetStills(ASSETS_OUT, 'plant', 'plant', [4.6, 3.8, 7.6], [0.15, 1.55, 0], 38),
        ...twoAssetStills(ASSETS_OUT, 'ferns', 'ferns', [2.4, 2.6, 10.6], [0, 2.35, 0], 40),
        ...twoAssetStills(ASSETS_OUT, 'volcano', 'volcano', [4.5, 4.2, 10.8], [0, 2.2, 0], 38),
        { id: 'AssetCheck', frame: 0, output: path.join(ASSETS_OUT, 'trex', 'front-idle-t0.png'), inputProps: { asset: 'trex', camPos: [0, 3.5, 12], camLook: [0, 2.5, 0], fov: 38, walk: 0, shadows: true } },
        { id: 'AssetCheck', frame: 8, output: path.join(ASSETS_OUT, 'trex', 'three-quarter-walk-t0.27.png'), inputProps: { asset: 'trex', camPos: [-6.2, 4.4, 9.6], camLook: [0, 1.85, 0], fov: 38, walk: 1, shadows: true } },
        { id: 'AssetCheck', frame: 22, output: path.join(ASSETS_OUT, 'trex', 'front-walk-t0.73.png'), inputProps: { asset: 'trex', camPos: [0, 3.5, 12], camLook: [0, 2.5, 0], fov: 38, walk: 1, shadows: true } },
        ...twoAssetStills(ASSETS_OUT, 'ice-street', 'ice-street', [0, 4.35, 15.8], [0, 2.75, -6], 42, { bg: ICE_SKY, shadows: false }),
        ...twoAssetStills(ASSETS_OUT, 'sliding-boy', 'sliding-boy', [0, 2.5, 10], [0, 1.2, 4.6], 40, { bg: ICE_SKY }),
        ...twoAssetStills(ASSETS_OUT, 'gills', 'gills', [0, 5.2, 7], [0, 5.0, 0], 30),
      ],
      videos: [],
    },
    wide: {
      description: 'Pulled-back (2x distance) verification stills for brain/clock/ferns/volcano',
      stills: [
        { slug: 'brain', asset: 'brain', cam: [1.45, 1.71, 19.2], look: [0.15, -0.15, 0], fov: 38 },
        { slug: 'clock', asset: 'clock', cam: [4.6, 0.81, 19.2], look: [0.2, -0.15, 0], fov: 38 },
        { slug: 'ferns', asset: 'ferns', cam: [4.8, 2.85, 21.2], look: [0, 2.35, 0], fov: 40 },
        { slug: 'volcano', asset: 'volcano', cam: [9.0, 6.2, 21.6], look: [0, 2.2, 0], fov: 38 },
      ].map((s) => ({
        id: 'AssetCheck',
        frame: 0,
        output: path.join(ASSETS_OUT, s.slug, 'wide-t0.png'),
        inputProps: { asset: s.asset, camPos: s.cam, camLook: s.look, fov: s.fov, walk: 0, bg: undefined, shadows: true },
      })),
      videos: [],
    },
  };
}
