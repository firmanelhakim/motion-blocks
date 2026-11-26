/**
 * render-kit-stills.mjs — one process, one port (3050): renders the engine
 * kit verification stills in a single bundle + serve session.
 *   KitCast frame 0 (idle cast shot)
 *   KitPoseLab frame 7 (walk, mid-stride)
 *   KitPoseLab frame 90 (run, mid-stride)
 *
 * Same VM workarounds as the casualman render scripts: loopback-only port
 * probe (see patches/), chrome-for-testing, Playwright Chromium, swangle GL.
 * `renderStill` takes `output` (unlike `renderMedia`, which takes
 * `outputLocation`).
 *
 *   node render-kit-stills.mjs
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

const shots = [
  ['KitCast', 0, 'kit-cast.png'],
  ['KitPoseLab', 7, 'kit-poselab-walk.png'],
  ['KitPoseLab', 90, 'kit-poselab-run.png'],
];

for (const [id, frame, file] of shots) {
  const comp = await selectComposition({serveUrl: bundled, id, inputProps: {}});
  await renderStill({...opts, composition: comp, serveUrl: bundled, frame, output: path.join(OUT, file)});
  console.log('still ok →', file);
}
