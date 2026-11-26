/**
 * render-verify-v3.mjs — one process, one port (3050): renders all the
 * leftover-work verification in a single run, after the shoe-pivot fix
 * and the BowCheck/PerformanceLab builds.
 *
 *   1. BowCheck — side-profile bow (still at the bow peak, frame 12, + video)
 *   2. KickCheck — side-profile kick (stills at the two kick peaks + video,
 *      re-rendered cleanly; the first video file was tiled/glitchy)
 *   3. PerformanceLab — the two-lane Performance demo (stills at one frame
 *      per segment + video)
 *   4. KitPoseLab — the full 23s PoseLab with the shoe fix, under a NEW
 *      filename (kit-poselab-v3.mp4) so the app can't serve a cached copy
 *      of the old video
 *
 * Same VM workarounds as the other engine scripts: loopback-only port
 * probe, chrome-for-testing, Playwright Chromium, swangle GL.
 * `renderStill` takes `output`; `renderMedia` takes `outputLocation`.
 *
 *   node render-verify-v3.mjs
 * Output → ~/workspace/videos/noob-compare/
 */
import {bundle} from '@remotion/bundler';
import {renderStill, renderMedia, selectComposition} from '@remotion/renderer';
import path from 'node:path';
import fs from 'node:fs';

const OUT = path.resolve(process.env.HOME, 'workspace/videos/noob-compare');
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

const renderStills = async (id, frames) => {
  const comp = await selectComposition({serveUrl: bundled, id});
  for (const [frame, file] of frames) {
    await renderStill({...opts, composition: comp, serveUrl: bundled, frame, output: path.join(OUT, file)});
    console.log('still ok →', file);
  }
  return comp;
};

const renderVideo = async (comp, file, extra = {}) => {
  await renderMedia({...opts, composition: comp, serveUrl: bundled, codec: 'h264', outputLocation: path.join(OUT, file), ...extra});
  console.log('video ok →', file);
};

// 1. BowCheck (60f): bow peak at local t=0.4s = frame 12.
const bowComp = await renderStills('BowCheck', [[12, 'bowcheck-side-peak.png']]);
await renderVideo(bowComp, 'bowcheck-side.mp4');

// 2. KickCheck (60f): kick peaks at frames 7 and 34.
const kickComp = await renderStills('KickCheck', [[7, 'kickcheck-side-v2-peak1.png'], [34, 'kickcheck-side-v2-peak2.png']]);
await renderVideo(kickComp, 'kickcheck-side-v2.mp4');

// 3. PerformanceLab (240f): wave 0–2s, bow 2–3.6s, cheer 3.6–5.2s, idle 5.2–8s.
const perfComp = await renderStills('PerformanceLab', [
  [30, 'performancelab-wave.png'],
  [72, 'performancelab-bow.png'],
  [132, 'performancelab-cheer.png'],
  [195, 'performancelab-idle.png'],
]);
await renderVideo(perfComp, 'performancelab.mp4');

// 4. KitPoseLab (690f, 23s): full PoseLab with the shoe fix, new filename.
const poselabComp = await selectComposition({serveUrl: bundled, id: 'KitPoseLab'});
await renderVideo(poselabComp, 'kit-poselab-v3.mp4', {crf: 19, concurrency: 1});

console.log('all verify-v3 renders done');
