// Render specific RobloxShort frames from existing out/bundle (backward-compatible shim).
// Usage: node render-cheese-frames.mjs <outDir> <f1> <f2> ...
import path from 'node:path';
import { buildRenderOptions, getServeUrl, renderStillBatch } from './scripts/render_lib.mjs';

const [, , outArg, ...frames] = process.argv;
if (!outArg || frames.length === 0) {
  console.error('usage: node render-cheese-frames.mjs <outDir> <f1> <f2> ...');
  process.exit(1);
}
const outDir = path.resolve(outArg);
const opts = buildRenderOptions();
const serveUrl = await getServeUrl({ bundleDir: 'out/bundle' });
const items = frames.map((f) => {
  const frame = Number(f);
  return { id: 'RobloxShort', frame, output: path.join(outDir, `frame-${frame}.png`) };
});
await renderStillBatch({
  serveUrl,
  items,
  opts,
  onDone: (item) => console.log(`still ok -> ${item.frame}`),
});
console.log('done');
