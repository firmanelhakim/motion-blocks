import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'node:path';
import fs from 'node:fs';

// Usage: node render-story-range.mjs <start> <end> [port] [outDir]
// Renders RobloxShort stills for frames start..end, skipping frames whose
// output file already exists. One bundle per process; run several ranges in
// parallel on different ports (3050, 3051, 3052).
// No hardcoded browserExecutable: Remotion uses its own Chrome for Testing
// (auto-downloaded on first run on fresh boxes). chromeMode
// 'chrome-for-testing' (--headless=new) — the default headless-shell is
// removed from this Chromium build.
const [,, startArg, endArg, portArg, outArg] = process.argv;
const START = Number(startArg ?? 0);
const END = Number(endArg ?? 0);
const PORT = Number(portArg ?? 3050);
const OUT = path.resolve(outArg ?? 'story-stills');
fs.mkdirSync(OUT, {recursive: true});
const bundled = await bundle({entryPoint: path.resolve('src/index.ts'), webpackOverride: (c) => c});
const opts = {
  chromiumOptions: {
    gl: 'swangle', enableMultiProcessOnLinux: true,
  },
  chromeMode: 'chrome-for-testing', serveStatic: {port: PORT}, timeoutInMilliseconds: 180_000,
};
const comp = await selectComposition({serveUrl: bundled, id: 'RobloxShort'});
console.log(`composition RobloxShort: ${comp.durationInFrames} frames, ${comp.fps} fps, ${comp.width}x${comp.height}`);
const t0 = Date.now();
let done = 0, skipped = 0;
for (let f = START; f <= END; f++) {
  const out = path.join(OUT, `frame-${String(f).padStart(5, '0')}.png`);
  if (fs.existsSync(out)) { skipped++; continue; }
  await renderStill({...opts, composition: comp, serveUrl: bundled, frame: f, output: out});
  done++;
  console.log(`still ok → ${f} (${done} done, ${((Date.now() - t0) / 1000).toFixed(1)}s)`);
}
console.log(`range ${START}-${END} done: ${done} rendered, ${skipped} skipped, ${((Date.now() - t0) / 1000).toFixed(1)}s total`);
