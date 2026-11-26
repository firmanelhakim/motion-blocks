import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';
import path from 'node:path';
const OUT = path.resolve(process.env.HOME, 'workspace/videos/noob-compare');
const bundled = await bundle({entryPoint: path.resolve('src/index.ts'), webpackOverride: (c) => c});
const opts = {
  chromiumOptions: {
    browserExecutable: `${process.env.HOME}/.cache/ms-playwright/chromium-1181/chrome-linux/chrome`,
    gl: 'swangle', enableMultiProcessOnLinux: true,
  },
  chromeMode: 'chrome-for-testing', serveStatic: {port: 3050}, timeoutInMilliseconds: 120_000,
};
const comp = await selectComposition({serveUrl: bundled, id: 'KitPoseLab', inputProps: {}});
await renderMedia({...opts, composition: comp, serveUrl: bundled, codec: 'h264', crf: 19, concurrency: 1, outputLocation: path.join(OUT, 'kit-poselab-v5.mp4')});
console.log('video ok → kit-poselab-v5.mp4');
