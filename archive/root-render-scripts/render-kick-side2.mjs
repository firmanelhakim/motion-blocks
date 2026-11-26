import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'node:path';
const OUT = path.resolve(process.env.HOME, 'workspace/videos/noob-compare/overlap');
const bundled = await bundle({entryPoint: path.resolve('src/index.ts'), webpackOverride: (c) => c});
const opts = {
  chromiumOptions: {
    browserExecutable: `${process.env.HOME}/.cache/ms-playwright/chromium-1181/chrome-linux/chrome`,
    gl: 'swangle', enableMultiProcessOnLinux: true,
  },
  chromeMode: 'chrome-for-testing', serveStatic: {port: 3050}, timeoutInMilliseconds: 120_000,
};
const comp = await selectComposition({serveUrl: bundled, id: 'KickCheck'});
// Peaks at f7 and f34 (cycle 0.9s, peak at t=0.225s and 1.125s). Mid-swing f11 and f38.
for (const [frame, file] of [[34,'kick-side-34.png'],[11,'kick-side-11.png'],[38,'kick-side-38.png']]) {
  await renderStill({...opts, composition: comp, serveUrl: bundled, frame, output: path.join(OUT, file)});
  console.log('still ok →', file);
}
console.log('kick side2 done');
