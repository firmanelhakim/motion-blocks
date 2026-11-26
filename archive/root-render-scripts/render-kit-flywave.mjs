/**
 * render-kit-flywave.mjs — one process, one port (3050): renders the engine
 * fly + wave circle demo in a single bundle + serve session.
 *   KitFlyWave frame 0  (front, facing the camera, arm raised waving)
 *   KitFlyWave frame 90 (back, wings from behind, mid-circle)
 *   KitFlyWave video, 180 frames (6s, one full circle)
 *
 * Same VM workarounds as render-kit-stills.mjs: loopback-only port probe
 * (see patches/), chrome-for-testing, Playwright Chromium, swangle GL.
 * `renderStill` takes `output`, `renderMedia` takes `outputLocation`.
 * Clear /tmp/remotion-webpack-bundle-* first if /tmp is full (see AGENTS.md).
 *
 *   node render-kit-flywave.mjs
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

const comp = await selectComposition({serveUrl: bundled, id: 'KitFlyWave', inputProps: {}});

for (const [frame, file] of [[0, 'kit-flywave-front.png'], [90, 'kit-flywave-back.png']]) {
  await renderStill({...opts, composition: comp, serveUrl: bundled, frame, output: path.join(OUT, file)});
  console.log('still ok →', file);
}

await renderMedia({...opts, composition: comp, serveUrl: bundled, codec: 'h264', crf: 19, concurrency: 1, outputLocation: path.join(OUT, 'kit-flywave.mp4')});
console.log('video ok → kit-flywave.mp4');
