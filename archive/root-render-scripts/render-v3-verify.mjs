/**
 * render-v3-verify.mjs — one process, one port (3050): stills only, to
 * verify the V3 Pose refactor (2026-11-20, the maintainer approved) is
 * behaviour-preserving and the new work reads:
 *
 *   KitPoseLab frame 15   walk — motion identical, waist clean
 *   KitPoseLab frame 150  wave — z-spread wobble
 *   KitPoseLab frame 240  dance — 150 bpm, arms/legs spread
 *   KitPoseLab frame 546  bow peak, FRONT — 0.75 lean reads from the front
 *   BowCheck frame 12     bow peak, SIDE — bow still connects at 0.75
 *   KickCheck frame 7     kick peak — still forward
 *   KitFly frame 8 / 23   flap wide / folded — wing-beat pivot (vertical)
 *   ClipCheck (7 stills)  climb, swim, catch, high-five, hug, dig, hammer
 *
 * Same VM workarounds as the other engine scripts: loopback-only port
 * probe, chrome-for-testing, Playwright Chromium, swangle GL.
 * `renderStill` takes `output`.
 *
 *   node render-v3-verify.mjs
 * Output → ~/workspace/videos/noob-compare/v3/
 */
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'node:path';
import fs from 'node:fs';

const OUT = path.resolve(process.env.HOME, 'workspace/videos/noob-compare/v3');
fs.mkdirSync(OUT, {recursive: true});

const bundled = await bundle({entryPoint: path.resolve('src/index.ts'), webpackOverride: (c) => c});

const opts = {
  chromiumOptions: {
    browserExecutable: `${process.env.HOME}/.cache/ms-playwright/chromium-1181/chrome-linux/chrome`,
    gl: 'swangle',
    enableMultiProcessOnLinux: true,
  },
  chromeMode: 'chrome-for-testing',
  serveStatic: {port: 3050},
  timeoutInMilliseconds: 120_000,
};

const renderStills = async (id, frames, inputProps) => {
  const comp = await selectComposition({serveUrl: bundled, id, inputProps});
  for (const [frame, file] of frames) {
    await renderStill({...opts, composition: comp, serveUrl: bundled, frame, inputProps, output: path.join(OUT, file)});
    console.log('still ok →', file);
  }
};

await renderStills('KitPoseLab', [
  [15, 'v3-walk.png'],
  [150, 'v3-wave.png'],
  [240, 'v3-dance.png'],
  [546, 'v3-bow-front.png'],
]);
await renderStills('BowCheck', [[12, 'v3-bow-side.png']]);
await renderStills('KickCheck', [[7, 'v3-kick.png']]);
await renderStills('KitFly', [[8, 'v3-fly-wide.png'], [23, 'v3-fly-folded.png']]);

const newClips = [
  ['climb', 18, 'v3-climb.png'],
  ['swim', 15, 'v3-swim.png'],
  ['catch', 15, 'v3-catch.png'],
  ['high-five', 18, 'v3-highfive.png'],
  ['hug', 24, 'v3-hug.png'],
  ['dig', 15, 'v3-dig.png'],
  ['hammer', 12, 'v3-hammer.png'],
];
for (const [clip, frame, file] of newClips) {
  await renderStills('ClipCheck', [[frame, file]], {clip});
}

console.log('all v3 verify stills done');
