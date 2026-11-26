import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';
import path from 'node:path';
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
await renderMedia({...opts, composition: comp, serveUrl: bundled, outputLocation: path.join(OUT, 'circle-showcase.mp4')});
console.log('circle video done');
