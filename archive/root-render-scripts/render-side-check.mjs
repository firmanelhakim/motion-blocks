import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'node:path';
import fs from 'node:fs';
const OUT = path.resolve(process.env.HOME, 'workspace/videos/noob-compare/overlap');
const bundled = await bundle({entryPoint: path.resolve('src/index.ts'), webpackOverride: (c) => c});
const opts = {
  chromiumOptions: {
    browserExecutable: `${process.env.HOME}/.cache/ms-playwright/chromium-1181/chrome-linux/chrome`,
    gl: 'swangle', enableMultiProcessOnLinux: true,
  },
  chromeMode: 'chrome-for-testing', serveStatic: {port: 3050}, timeoutInMilliseconds: 120_000,
};
const comp = await selectComposition({serveUrl: bundled, id: 'ClipCheck'});
// walk side at forward peak (f7), sprint side at peak (f~7 of its 0.6s cycle -> f7)
for (const [clip, frame, file] of [['walk', 7, 'side-walk.png'], ['sprint', 7, 'side-sprint.png'], ['run', 7, 'side-run.png']]) {
  await renderStill({...opts, composition: comp, serveUrl: bundled, frame, inputProps: {clip, side: 'side'}, output: path.join(OUT, file)});
  console.log('still ok →', file);
}
console.log('side check done');
