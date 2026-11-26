/**
 * render-fix-verify.mjs — one process, one port (3050): verifies the three
 * fixes the maintainer asked for on 2026-11-20 (flicker, pants/shirt overlap, slow
 * dance).
 *
 * 1. BowCheck still (frame 12) — the bow must STILL connect after the torso
 *    was shortened to end at the waist (the overlap fix).
 * 2. KitPoseLab walk still (frame 15) — the waist must be clean now (shirt
 *    ends at the waist, no overlap over the pants).
 * 3. PerformanceLab as ALL 240 stills + ffmpeg assemble — replaces the
 *    renderMedia video, whose frames came out tiled/intermittent (the
 *    flicker the maintainer saw; frame 60 was a 2x2 tile). Stills are reliable.
 * 4. KitPoseLab v4 video (696f) — new dance (150bpm), new wave, new jump,
 *    fixed torso. Fresh filename so the app can't show a cached copy.
 *
 * Same VM workarounds as render-verify-v3.mjs: chrome-for-testing,
 * Playwright Chromium, swangle GL, port 3050, concurrency 1.
 * `renderStill` takes `output`; `renderMedia` takes `outputLocation`.
 *
 *   node render-fix-verify.mjs
 * Output → ~/workspace/videos/noob-compare/
 */
import {bundle} from '@remotion/bundler';
import {renderStill, renderMedia, selectComposition} from '@remotion/renderer';
import {execSync} from 'node:child_process';
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
  concurrency: 1,
};

// 1. BowCheck still — bow must still connect after the torso fix.
const bow = await selectComposition({serveUrl: bundled, id: 'BowCheck'});
await renderStill({...opts, composition: bow, serveUrl: bundled, frame: 12, output: path.join(OUT, 'bowcheck-side-peak-v2.png')});
console.log('still ok → bowcheck-side-peak-v2.png');

// 2. KitPoseLab walk still — waist must be clean now.
const poselab = await selectComposition({serveUrl: bundled, id: 'KitPoseLab'});
await renderStill({...opts, composition: poselab, serveUrl: bundled, frame: 15, output: path.join(OUT, 'poselab-v4-walk.png')});
console.log('still ok → poselab-v4-walk.png');

// 3. PerformanceLab as stills (240f) + ffmpeg assemble — no renderMedia,
//    so no tiled frames.
const perf = await selectComposition({serveUrl: bundled, id: 'PerformanceLab'});
const perfDir = path.join(OUT, 'frames', 'perf-stills');
fs.mkdirSync(perfDir, {recursive: true});
for (let f = 0; f < 240; f++) {
  await renderStill({...opts, composition: perf, serveUrl: bundled, frame: f, output: path.join(perfDir, `f-${f}.png`)});
  if (f % 60 === 0) console.log(`perf still ${f}/240`);
}
console.log('perf stills done');
execSync(`ffmpeg -y -v error -framerate 30 -start_number 0 -i "${perfDir}/f-%d.png" -c:v libx264 -pix_fmt yuv420p -crf 19 "${path.join(OUT, 'performancelab-v2.mp4')}"`);
console.log('video ok → performancelab-v2.mp4');

// 4. KitPoseLab v4 video — new dance/wave/jump + fixed torso.
await renderMedia({...opts, composition: poselab, serveUrl: bundled, codec: 'h264', crf: 19, outputLocation: path.join(OUT, 'kit-poselab-v4.mp4')});
console.log('video ok → kit-poselab-v4.mp4');

console.log('all fix-verify renders done');
