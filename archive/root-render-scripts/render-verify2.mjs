import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
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
// 1. R6 teacher kick after the shoe counter-rotation fix
let comp = await selectComposition({serveUrl: bundled, id: 'R6KitCheck', inputProps: {preset: 'teacher', clip: 'kick'}});
await renderStill({...opts, composition: comp, serveUrl: bundled, frame: 7, output: path.join(OUT, 'r6kit/r6-teacher-kick-7b.png')});
console.log('still ok → teacher kick v2');
// 2. KitPoseLab kick segment — verify the side-camera swing (kick is t 19.2-21.2)
comp = await selectComposition({serveUrl: bundled, id: 'KitPoseLab'});
for (const f of [576, 582, 600, 612, 630, 636]) {
  await renderStill({...opts, composition: comp, serveUrl: bundled, frame: f, output: path.join(OUT, 'v9frames', `v10-kick-${f}.png`)});
  console.log('still ok → poselab kick', f);
}
console.log('verify2 done');
