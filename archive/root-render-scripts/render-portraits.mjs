import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'node:path';
const OUT = path.resolve(process.env.HOME, 'workspace/videos/noob-compare/portraits');
const bundled = await bundle({entryPoint: path.resolve('src/index.ts'), webpackOverride: (c) => c});
const opts = {
  chromiumOptions: {
    browserExecutable: `${process.env.HOME}/.cache/ms-playwright/chromium-1181/chrome-linux/chrome`,
    gl: 'swangle', enableMultiProcessOnLinux: true,
  },
  chromeMode: 'chrome-for-testing', serveStatic: {port: 3050}, timeoutInMilliseconds: 120_000,
};
for (const character of ['blockboy', 'casualman', 'wingedboy']) {
  const comp = await selectComposition({serveUrl: bundled, id: 'WaistCheck', inputProps: {character, clip: 'idle'}});
  await renderStill({...opts, composition: comp, serveUrl: bundled, frame: 15, output: path.join(OUT, `portrait-${character}.png`)});
  console.log('still ok →', character);
}
console.log('engine portraits done');
