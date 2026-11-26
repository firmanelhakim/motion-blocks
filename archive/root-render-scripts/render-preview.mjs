// Render MotionBlocks preview stills for one story (backward-compatible shim).
// Usage: node render-preview.mjs <slug>
// Reads frame list from /tmp/preview-frames-<slug>.json
// Writes out/preview/<slug>/frame-<NNNN>.png
import fs from 'node:fs';
import path from 'node:path';
import { buildRenderOptions, getServeUrl, renderStillBatch } from './scripts/render_lib.mjs';

const slug = process.argv[2];
if (!slug) {
  console.error('usage: node render-preview.mjs <slug>');
  process.exit(1);
}
const frames = JSON.parse(fs.readFileSync(`/tmp/preview-frames-${slug}.json`, 'utf-8'));
const outDir = path.resolve(`out/preview/${slug}`);
const opts = buildRenderOptions();
const serveUrl = await getServeUrl({ entry: 'src/short-entry.tsx' });
const items = frames.map((frame) => ({
  id: 'MotionBlocks',
  frame,
  output: path.join(outDir, `frame-${String(frame).padStart(4, '0')}.png`),
  skipIfExists: true,
}));
await renderStillBatch({
  serveUrl,
  items,
  opts,
  onDone: (item) => console.log('frame', item.frame, 'ok'),
});
console.log('done', slug, frames.length, 'frames');
