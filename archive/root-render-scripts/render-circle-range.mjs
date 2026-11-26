// Usage: node render-circle-range.mjs <start> <end> [port] [outDir]
// Backward-compatible shim over shared warm-browser render_lib.mjs.
import path from 'node:path';
import { buildRenderOptions, getServeUrl, renderStillBatch } from './scripts/render_lib.mjs';

const [, , startArg, endArg, portArg, outArg] = process.argv;
const START = Number(startArg ?? 0);
const END = Number(endArg ?? 0);
const PORT = Number(portArg ?? 3050);
const OUT = path.resolve(outArg ?? 'circle-stills');
const opts = buildRenderOptions({ port: PORT });
const serveUrl = await getServeUrl();

const items = [];
for (let f = START; f <= END; f++) {
  items.push({
    id: 'CircleShowcase',
    frame: f,
    output: path.join(OUT, `circle-${f}.png`),
    skipIfExists: true,
  });
}
const t0 = Date.now();
const { rendered, skipped } = await renderStillBatch({
  serveUrl,
  items,
  opts,
  onDone: (item, stats) =>
    console.log(`still ok -> ${item.frame} (${stats.rendered} done, ${((Date.now() - t0) / 1000).toFixed(1)}s)`),
});
console.log(`range ${START}-${END} done: ${rendered} rendered, ${skipped} skipped, ${((Date.now() - t0) / 1000).toFixed(1)}s total`);
