import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'node:path';
import fs from 'node:fs';
const OUT = '/home/hatch/workspace/videos/noob-compare/kitstory';
fs.mkdirSync(OUT, {recursive: true});
const bundled = await bundle({entryPoint: path.resolve('src/index.ts'), webpackOverride: (c) => c});
const opts = {
  chromiumOptions: {
    browserExecutable: `${process.env.HOME}/.cache/ms-playwright/chromium-1181/chrome-linux/chrome`,
    gl: 'swangle', enableMultiProcessOnLinux: true,
  },
  chromeMode: 'chrome-for-testing', serveStatic: {port: 3050}, timeoutInMilliseconds: 180_000,
};
const comp = await selectComposition({serveUrl: bundled, id: 'KitStoryCheck'});
for (const f of [0, 45, 89]) {
  await renderStill({...opts, composition: comp, serveUrl: bundled, frame: f, output: path.join(OUT, `kitstory-${f}.png`)});
  console.log('frame', f, 'ok');
}
console.log('done');
