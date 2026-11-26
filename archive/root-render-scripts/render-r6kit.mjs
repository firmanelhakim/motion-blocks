import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'node:path';
const OUT = path.resolve(process.env.HOME, 'workspace/videos/noob-compare/r6kit');
const bundled = await bundle({entryPoint: path.resolve('src/index.ts'), webpackOverride: (c) => c});
const opts = {
  chromiumOptions: {
    browserExecutable: `${process.env.HOME}/.cache/ms-playwright/chromium-1181/chrome-linux/chrome`,
    gl: 'swangle', enableMultiProcessOnLinux: true,
  },
  chromeMode: 'chrome-for-testing', serveStatic: {port: 3050}, timeoutInMilliseconds: 120_000,
};
const shots = [
  ['teacher', 'walk', 15], ['teacher', 'wave', 15],
  ['teacher', 'kick', 7], ['teacher', 'dance', 7],
  ['bully', 'kick', 7], ['bully', 'dance', 7],
  ['kid_boy', 'wave', 15], ['kid_boy', 'walk', 15],
  ['bolt_boy', 'dance', 7], ['bolt_boy', 'kick', 7],
];
for (const [preset, clip, frame] of shots) {
  const comp = await selectComposition({serveUrl: bundled, id: 'R6KitCheck', inputProps: {preset, clip}});
  const file = `r6-${preset}-${clip}-${frame}.png`;
  await renderStill({...opts, composition: comp, serveUrl: bundled, frame, output: path.join(OUT, file)});
  console.log('still ok →', file);
}
console.log('r6kit done');
