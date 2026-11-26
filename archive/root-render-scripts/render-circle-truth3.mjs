import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'node:path';
const OUT = path.resolve(process.env.HOME, 'workspace/videos/noob-compare/circle');
const bundled = await bundle({entryPoint: path.resolve('src/index.ts'), webpackOverride: (c) => c});
const opts = {
  chromiumOptions: {
    browserExecutable: `${process.env.HOME}/.cache/ms-playwright/chromium-1181/chrome-linux/chrome`,
    gl: 'swangle', enableMultiProcessOnLinux: true,
  },
  chromeMode: 'chrome-for-testing', serveStatic: {port: 3050}, timeoutInMilliseconds: 180_000,
};
const comp = await selectComposition({serveUrl: bundled, id: 'CircleShowcase'});
for (const f of [300, 310, 320, 337, 350]) {
  await renderStill({...opts, composition: comp, serveUrl: bundled, frame: f, output: path.join(OUT, `t3-${f}.png`)});
  console.log('still ok →', f);
}
console.log('truth3 done');
