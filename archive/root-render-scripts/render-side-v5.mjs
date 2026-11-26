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
// run + kick from the side at the phases the maintainer sees (run f90->clip f30, kick f605->clip f29)
for (const [clip, frame, file] of [['run', 30, 'v5-side-run.png'], ['kick', 29, 'v5-side-kick.png'], ['sprint', 29, 'v5-side-sprint.png']]) {
  await renderStill({...opts, composition: comp, serveUrl: bundled, frame, inputProps: {clip, side: 'side'}, output: path.join(OUT, file)});
  console.log('still ok →', file);
}
console.log('side v5 done');
