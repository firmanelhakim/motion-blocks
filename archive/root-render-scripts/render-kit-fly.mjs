/**
 * render-kit-fly.mjs — one process, one port (3050): renders the engine
 * WingedBoy fly demo in a single bundle + serve session.
 *   KitFly frame 8  (wings wide, t=0.25s — top of the flap)
 *   KitFly frame 23 (wings folded, t=0.75s — bottom of the flap)
 *   KitFly video, 90 frames (3s)
 *
 * Same VM workarounds as render-kit-stills.mjs (the proven pattern on this
 * project): loopback-only port probe (see patches/), chrome-for-testing,
 * Playwright Chromium, swangle GL. `renderStill` takes `output`,
 * `renderMedia` takes `outputLocation`.
 *
 *   node render-kit-fly.mjs
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

const comp = await selectComposition({serveUrl: bundled, id: 'KitFly', inputProps: {}});

for (const [frame, file] of [[8, 'kit-fly-top.png'], [23, 'kit-fly-bottom.png']]) {
  await renderStill({...opts, composition: comp, serveUrl: bundled, frame, output: path.join(OUT, file)});
  console.log('still ok →', file);
}

await renderMedia({...opts, composition: comp, serveUrl: bundled, codec: 'h264', crf: 19, concurrency: 1, outputLocation: path.join(OUT, 'kit-fly.mp4')});
console.log('video ok → kit-fly.mp4');
