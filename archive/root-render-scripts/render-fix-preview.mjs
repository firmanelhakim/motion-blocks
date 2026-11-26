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
// Catch v2 + Dig v2: open/scoop at f22, closed/back at f7. Kick from the side at f7.
const shots = [
  ['catch', 22, false], ['catch', 7, false],
  ['dig', 22, false], ['dig', 7, false],
  ['kick', 7, true],
];
for (const [clip, frame, side] of shots) {
  const comp = await selectComposition({serveUrl: bundled, id: 'ClipCheck', inputProps: {clip, side}});
  const file = `fix-${clip}-${side ? 'side-' : ''}${frame}.png`;
  await renderStill({...opts, composition: comp, serveUrl: bundled, frame, output: path.join(OUT, file)});
  console.log('still ok →', file);
}
console.log('fix preview done');
