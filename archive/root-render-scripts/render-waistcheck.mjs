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
const frames = [6, 12, 18, 24, 30, 36, 42, 48];
for (const character of ['casualman', 'wingedboy']) {
  for (const clip of ['dance', 'march']) {
    const comp = await selectComposition({serveUrl: bundled, id: 'WaistCheck', inputProps: {character, clip}});
    for (const frame of frames) {
      const file = `wc-${character}-${clip}-${frame}.png`;
      await renderStill({...opts, composition: comp, serveUrl: bundled, frame, output: path.join(OUT, file)});
    }
    console.log('done', character, clip);
  }
}
console.log('waistcheck done');
