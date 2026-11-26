/**
 * render-facelab-stills.mjs — one process, one port (3050): renders the
 * FaceLab expression verification stills in a single bundle + serve session.
 * One still per expression (frame 0), each with its own inputProps.
 *
 * The set covers the regression checks (each character's default face must
 * match the original exactly) plus one still per distinct drawing path:
 * tears (cry), open mouth + closed eyes (laugh), wide eyes (shocked),
 * sunglasses (cool), heart eyes (love), angled brows (angry), spiral eyes
 * (dizzy). 'cry' is rendered at expressionT=0.5 so a tear is mid-drop.
 *
 * Same VM workarounds as render-kit-stills.mjs: loopback-only port probe
 * (see patches/), chrome-for-testing, Playwright Chromium, swangle GL.
 * `renderStill` takes `output`.
 *
 *   node render-facelab-stills.mjs
 * Output → ~/workspace/videos/noob-compare/
 */
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'node:path';
import fs from 'node:fs';

const OUT = path.resolve(process.env.HOME, 'workspace/videos/noob-compare');
fs.mkdirSync(OUT, {recursive: true});

const bundled = await bundle({entryPoint: path.resolve('src/index.ts'), webpackOverride: (c) => c});

const opts = {
  chromiumOptions: {
    browserExecutable: `${process.env.HOME}/.cache/ms-playwright/chromium-1181/chrome-linux/chrome`,
    gl: 'swangle',
    enableMultiProcessOnLinux: true,
  },
  chromeMode: 'chrome-for-testing',
  serveStatic: {port: 3050},
  timeoutInMilliseconds: 120_000,
};

const shots = [
  [{character: 'blockboy', expression: 'grin'}, 'facelab-blockboy-grin.png'],
  [{character: 'blockboy', expression: 'cry', expressionT: 0.5}, 'facelab-blockboy-cry.png'],
  [{character: 'blockboy', expression: 'laugh'}, 'facelab-blockboy-laugh.png'],
  [{character: 'blockboy', expression: 'shocked'}, 'facelab-blockboy-shocked.png'],
  [{character: 'blockboy', expression: 'cool'}, 'facelab-blockboy-cool.png'],
  [{character: 'blockboy', expression: 'love'}, 'facelab-blockboy-love.png'],
  [{character: 'blockboy', expression: 'angry'}, 'facelab-blockboy-angry.png'],
  [{character: 'blockboy', expression: 'dizzy'}, 'facelab-blockboy-dizzy.png'],
  [{character: 'casualman', expression: 'smile'}, 'facelab-casualman-smile.png'],
  [{character: 'wingedboy', expression: 'smirk'}, 'facelab-wingedboy-smirk.png'],
  [{character: 'wingedboy', expression: 'cry', expressionT: 0.5}, 'facelab-wingedboy-cry.png'],
  [{character: 'wingedboy', expression: 'laugh'}, 'facelab-wingedboy-laugh.png'],
  [{character: 'wingedboy', expression: 'shocked'}, 'facelab-wingedboy-shocked.png'],
  [{character: 'wingedboy', expression: 'cool'}, 'facelab-wingedboy-cool.png'],
  [{character: 'wingedboy', expression: 'love'}, 'facelab-wingedboy-love.png'],
  [{character: 'wingedboy', expression: 'angry'}, 'facelab-wingedboy-angry.png'],
  [{character: 'wingedboy', expression: 'dizzy'}, 'facelab-wingedboy-dizzy.png'],
];

for (const [inputProps, file] of shots) {
  const comp = await selectComposition({serveUrl: bundled, id: 'FaceLab', inputProps});
  await renderStill({...opts, composition: comp, serveUrl: bundled, frame: 0, output: path.join(OUT, file)});
  console.log('still ok →', file);
}
