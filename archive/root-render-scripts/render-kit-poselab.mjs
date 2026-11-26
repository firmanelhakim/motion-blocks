/**
 * render-kit-poselab.mjs — one process, one port (3050): renders the engine
 * KitPoseLab demo (23s, 690 frames) in a single bundle + serve session.
 * Stills are taken at each new clip's peak, not at segment starts:
 *   frame 300 sprint (mid-stride) · 337 march (high knee) ·
 *   396 cheer (arms up + jump) · 455 punch (thrust) ·
 *   522 bow (bent) · 577 kick (leg up).
 *
 * Same VM workarounds as render-kit-stills.mjs: loopback-only port probe
 * (see patches/), chrome-for-testing, Playwright Chromium, swangle GL.
 * `renderStill` takes `output`, `renderMedia` takes `outputLocation`.
 * Clear /tmp/remotion-webpack-bundle-* first if /tmp is full (see AGENTS.md).
 *
 *   node render-kit-poselab.mjs
 * Output → ~/workspace/videos/noob-compare/
 */
import {bundle} from '@remotion/bundler';
import {renderMedia, renderStill, selectComposition} from '@remotion/renderer';
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

const comp = await selectComposition({serveUrl: bundled, id: 'KitPoseLab', inputProps: {}});

for (const [frame, file] of [
  [300, 'kit-poselab-sprint.png'],
  [337, 'kit-poselab-march.png'],
  [396, 'kit-poselab-cheer.png'],
  [455, 'kit-poselab-punch.png'],
  [522, 'kit-poselab-bow.png'],
  [577, 'kit-poselab-kick.png'],
]) {
  await renderStill({...opts, composition: comp, serveUrl: bundled, frame, output: path.join(OUT, file)});
  console.log('still ok →', file);
}

await renderMedia({...opts, composition: comp, serveUrl: bundled, codec: 'h264', crf: 19, concurrency: 1, outputLocation: path.join(OUT, 'kit-poselab.mp4')});
console.log('video ok → kit-poselab.mp4');
