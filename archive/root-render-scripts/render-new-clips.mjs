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
const clips = ['climb', 'swim', 'catch', 'high-five', 'hug', 'dig', 'hammer'];
const frames = [0, 15, 30, 45];
for (const clip of clips) {
  const comp = await selectComposition({serveUrl: bundled, id: 'ClipCheck', inputProps: {clip}});
  for (const frame of frames) {
    const file = `new-${clip}-${frame}.png`;
    await renderStill({...opts, composition: comp, serveUrl: bundled, frame, output: path.join(OUT, file)});
  }
  console.log('done', clip);
}
console.log('new clips done');
