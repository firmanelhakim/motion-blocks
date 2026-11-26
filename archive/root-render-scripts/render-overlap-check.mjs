import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'node:path';
import fs from 'node:fs';
const OUT = path.resolve(process.env.HOME, 'workspace/videos/noob-compare/overlap');
fs.mkdirSync(OUT, {recursive: true});
const bundled = await bundle({entryPoint: path.resolve('src/index.ts'), webpackOverride: (c) => c});
const opts = {
  chromiumOptions: {
    browserExecutable: `${process.env.HOME}/.cache/ms-playwright/chromium-1181/chrome-linux/chrome`,
    gl: 'swangle', enableMultiProcessOnLinux: true,
  },
  chromeMode: 'chrome-for-testing', serveStatic: {port: 3050}, timeoutInMilliseconds: 120_000,
};
const comp = await selectComposition({serveUrl: bundled, id: 'KitPoseLab'});
// Leg-swing extremes: walk f7 (legL fwd peak), f22 (legR fwd peak); run f67; sprint f283; punch f471; kick f583
for (const [frame, file] of [[7, 'ov-walk-fwd.png'], [22, 'ov-walk-fwd2.png'], [67, 'ov-run.png'], [283, 'ov-sprint.png'], [471, 'ov-punch.png'], [583, 'ov-kick.png']]) {
  await renderStill({...opts, composition: comp, serveUrl: bundled, frame, output: path.join(OUT, file)});
  console.log('still ok →', file);
}
console.log('overlap check done');
