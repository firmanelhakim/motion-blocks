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
const comp = await selectComposition({serveUrl: bundled, id: 'KitPoseLab'});
// Every 3 frames across run (60-120), dance (216-276), sprint (276-336), kick (576-636)
const frames = [];
for (let f = 60; f <= 120; f += 3) frames.push(f);
for (let f = 216; f <= 276; f += 3) frames.push(f);
for (let f = 276; f <= 336; f += 3) frames.push(f);
for (let f = 576; f <= 636; f += 3) frames.push(f);
for (const f of frames) {
  await renderStill({...opts, composition: comp, serveUrl: bundled, frame: f, output: path.join(OUT, `red8-${f}.png`)});
}
console.log('red8 done,', frames.length, 'frames');
