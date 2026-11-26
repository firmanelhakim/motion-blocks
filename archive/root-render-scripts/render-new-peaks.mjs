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
// Peak frames (not the sine zero-crossings my first pass hit)
const shots = [
  ['swim', 7], ['swim', 22],
  ['catch', 7], ['catch', 22],
  ['hug', 12], ['hug', 36],
  ['dig', 7], ['dig', 22],
];
for (const [clip, frame] of shots) {
  const comp = await selectComposition({serveUrl: bundled, id: 'ClipCheck', inputProps: {clip}});
  const file = `peak-${clip}-${frame}.png`;
  await renderStill({...opts, composition: comp, serveUrl: bundled, frame, output: path.join(OUT, file)});
  console.log('still ok →', file);
}
console.log('peaks done');
