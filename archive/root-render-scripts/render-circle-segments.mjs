import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';
import path from 'node:path';
import fs from 'node:fs';
const OUT = path.resolve(process.env.HOME, 'workspace/videos/noob-compare/circle');
const bundled = await bundle({entryPoint: path.resolve('src/index.ts'), webpackOverride: (c) => c});
const opts = {
  chromiumOptions: {
    browserExecutable: `${process.env.HOME}/.cache/ms-playwright/chromium-1181/chrome-linux/chrome`,
    gl: 'swangle', enableMultiProcessOnLinux: true,
  },
  chromeMode: 'chrome-for-testing', serveStatic: {port: 3050}, timeoutInMilliseconds: 300_000,
  concurrency: 1, codec: 'h264',
};
const comp = await selectComposition({serveUrl: bundled, id: 'CircleShowcase'});
const segs = [[0, 299], [300, 599], [600, 899]];
for (const [a, b] of segs) {
  const file = path.join(OUT, `circle-seg-${a}-${b}.mp4`);
  if (fs.existsSync(file)) { console.log('skip (exists) →', file); continue; }
  await renderMedia({...opts, composition: comp, serveUrl: bundled, frameRange: [a, b], outputLocation: file});
  console.log('segment ok →', file);
}
console.log('all segments done');
