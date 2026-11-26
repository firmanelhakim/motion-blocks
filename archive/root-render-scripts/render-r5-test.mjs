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
const comp = await selectComposition({serveUrl: bundled, id: 'KitPoseLab'});
// Dance wedge frames + march sliver frames + other extremes
for (const [frame, file] of [[222,'r5-dance222.png'],[234,'r5-dance234.png'],[246,'r5-dance246.png'],[258,'r5-dance258.png'],[355,'r5-march355.png'],[370,'r5-march370.png'],[385,'r5-march385.png'],[90,'r5-run90.png'],[305,'r5-sprint305.png'],[605,'r5-kick605.png'],[7,'r5-walk7.png'],[471,'r5-punch471.png']]) {
  await renderStill({...opts, composition: comp, serveUrl: bundled, frame, output: path.join(OUT, file)});
  console.log('still ok →', file);
}
console.log('r5 test done');
