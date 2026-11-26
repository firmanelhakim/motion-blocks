/**
 * render-port-verify.mjs — one process, one port (3050): verifies the
 * Claude motion port (2026-11-20) with stills of the new clips.
 *
 * KitPoseLab (23.2s, 696f): walk 2 → run 2 → wave 2 → jump 1.2 → dance 2 …
 *   wave raised:  frame 150 (wave segment 120–180, local t=1.0s, arm up)
 *   jump peak:    frame 198 (jump segment 180–216, local t=0.6s, max height)
 *   dance:        frame 231 (dance segment 216–276, local t=0.5s, 1 beat)
 * TurnCheck (4s turntable, idle + withTurn): frame 30 = 90° turn (side
 * view), frame 60 = 180° turn (back view).
 *
 * Same VM workarounds as render-kickcheck.mjs: chrome-for-testing,
 * Playwright Chromium, swangle GL, port 3050. `renderStill` takes `output`.
 *
 *   node render-port-verify.mjs
 * Output → ~/workspace/videos/noob-compare/
 */
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
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

const poselab = await selectComposition({serveUrl: bundled, id: 'KitPoseLab'});
for (const [frame, file] of [[150, 'port-wave.png'], [198, 'port-jump.png'], [231, 'port-dance.png']]) {
  await renderStill({...opts, composition: poselab, serveUrl: bundled, frame, output: path.join(OUT, file)});
  console.log('still ok →', file);
}

const turn = await selectComposition({serveUrl: bundled, id: 'TurnCheck'});
for (const [frame, file] of [[30, 'port-turn-90.png'], [60, 'port-turn-180.png']]) {
  await renderStill({...opts, composition: turn, serveUrl: bundled, frame, output: path.join(OUT, file)});
  console.log('still ok →', file);
}

console.log('all port-verify stills done');
