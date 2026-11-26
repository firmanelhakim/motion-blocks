#!/usr/bin/env node
/**
 * Unified Remotion render CLI for stills, frame ranges, presets, and
 * story videos (stills + ffmpeg).
 *
 * Uses a single warm Chromium browser (openBrowser + puppeteerInstance) across
 * still batches and enforces CPU-only SwiftShader + OOM-safe Chromium flags.
 *
 * Story videos NEVER use the Remotion video renderer: it is proven to drift deterministically
 * (frame 0 exact, ~RMSE 157 by frame 299) and to glitch with blank-white /
 * tiled frames. The story subcommand renders every frame as a still via
 * renderStillBatch and assembles with ffmpeg (30fps, libx264, CRF 18,
 * yuv420p, faststart) + the soundtrack muxed in. See render_lib.mjs
 * assembleStillsToVideo.
 *
 * Examples:
 *   node scripts/render.mjs still --comp MotionBlocks --frames 0,60,120 --out-dir out/stills --scale 0.5
 *   node scripts/render.mjs range --comp CircleShowcase --start 0 --end 100 --out-dir circle-stills --port 3050
 *   node scripts/render.mjs story sky_blue --port 3051
 *   node scripts/render.mjs story sky_blue --start 0 --end 299 --out out/sky_blue-f0-299.mp4 --port 3051
 *   node scripts/render.mjs story sky_blue --assemble-only
 *   node scripts/render.mjs preset kickcheck
 *   node scripts/render.mjs list
 *
 * The story must already be loaded into src/story/currentStory.ts with its
 * matching public/soundtrack.wav — that is make_short.py's job
 * (`venv/bin/python scripts/make_short.py stories/<slug>.py`). This command
 * only renders the loaded story; it never regenerates the story or audio.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { openBrowser, selectComposition } from '@remotion/renderer';
import {
  STORY_VIDEO,
  assembleStillsToVideo,
  buildRenderOptions,
  bundleToDir,
  formatFrameName,
  getServeUrl,
  renderStillBatch,
  stillsFileName,
} from './render_lib.mjs';
import { getPresets } from './render_presets.mjs';

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

/**
 * Verify the story loaded in src/story/currentStory.ts is the one the
 * slug names. The slug alone does NOT select a story — the render
 * always uses the loaded currentStory.ts — so without this check,
 * `story no_friction` while ice_floats is loaded would silently
 * produce ice_floats content named no_friction.mp4. Compares the
 * loaded title against stories/<slug>.py's TITLE; on mismatch, fails
 * loudly. When no stories/<slug>.py exists the slug cannot be
 * verified (e.g. an ad-hoc output name) — warns and continues.
 */
function verifyLoadedStory(slug) {
  if (!slug || slug === 'story') return;
  const storyFile = path.join(REPO_ROOT, 'stories', `${slug}.py`);
  if (!fs.existsSync(storyFile)) {
    console.log(`WARNING: cannot verify loaded story against slug "${slug}" (no stories/${slug}.py) — rendering the loaded story under that name.`);
    return;
  }
  const current = fs.readFileSync(path.join(REPO_ROOT, 'src', 'story', 'currentStory.ts'), 'utf8');
  const loadedTitle = /title:\s*['"]([^'"]+)['"]/.exec(current)?.[1];
  const wantTitle = /^TITLE\s*=\s*['"]([^'"]+)['"]/m.exec(fs.readFileSync(storyFile, 'utf8'))?.[1];
  if (loadedTitle && wantTitle && loadedTitle !== wantTitle) {
    console.error(
      `Story mismatch: loaded currentStory.ts is "${loadedTitle}" but stories/${slug}.py is "${wantTitle}". ` +
        `Load the story first (venv/bin/python scripts/make_short.py stories/${slug}.py) — refusing to render "${loadedTitle}" as "${slug}".`
    );
    process.exit(1);
  }
}

/** Resolve the soundtrack, or fail: a missing soundtrack is an error, not a warning. */
function resolveAudio(flags) {
  if (flags['no-audio']) return null;
  if (typeof flags.audio === 'string') {
    const audio = path.resolve(flags.audio);
    if (!fs.existsSync(audio)) {
      console.error(`Audio file not found: ${audio}`);
      process.exit(1);
    }
    return audio;
  }
  const defaultAudio = path.resolve('public/soundtrack.wav');
  if (fs.existsSync(defaultAudio)) return defaultAudio;
  console.error('No soundtrack found (public/soundtrack.wav missing and no --audio given) — refusing to produce a silent video. Pass --no-audio to render video-only deliberately.');
  process.exit(1);
}

function parseArgs(argv) {
  const pos = [];
  const flags = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const eq = a.indexOf('=');
      if (eq !== -1) {
        flags[a.slice(2, eq)] = a.slice(eq + 1);
      } else if (i + 1 < argv.length && !argv[i + 1].startsWith('--')) {
        flags[a.slice(2)] = argv[++i];
      } else {
        flags[a.slice(2)] = true;
      }
    } else {
      pos.push(a);
    }
  }
  return { pos, flags };
}

async function main() {
  const { pos, flags } = parseArgs(process.argv.slice(2));
  const cmd = pos[0] || 'help';

  if (cmd === 'list') {
    const presets = getPresets();
    for (const [name, p] of Object.entries(presets)) {
      console.log(`${name.padEnd(18)} ${p.description}`);
    }
    return;
  }

  if (cmd === 'help' || flags.help) {
    console.log([
      'Usage:',
      '  node scripts/render.mjs still  --comp <id> --frames 0,30 --out-dir <dir> [--pattern frame-{frame:4}.png] [--scale 0.5] [--bundle out/bundle]',
      '  node scripts/render.mjs range  --comp <id> --start 0 --end 100 --out-dir <dir> [--pattern frame-{frame}.png] [--port 3050]',
      '  node scripts/render.mjs story [slug|stories/<slug>.py] [--start 0] [--end <last>] [--out out/<slug>.mp4] [--stills-dir out/stills/<slug>] [--audio public/soundtrack.wav|--no-audio] [--port 3051] [--overwrite] [--stills-only] [--assemble-only]',
      '  node scripts/render.mjs preset <name> [--preview] [--port 3050] [--log error]',
      '  node scripts/render.mjs list',
      '',
      'Story videos are stills + ffmpeg (30fps, libx264, CRF 18, yuv420p, faststart),',
      'never the Remotion video renderer. The story must already be loaded into',
      'src/story/currentStory.ts with its public/soundtrack.wav (see make_short.py).',
      'The slug only names outputs — the render uses the loaded story, and this',
      'command verifies the loaded title matches stories/<slug>.py before rendering.',
      'A missing soundtrack is an error unless --no-audio is passed.',
      'Stills are skipped when they already exist (resume); pass --overwrite to re-render.',
      'Without --bundle, each run bundles into its own out/bundle-story-p<pid> dir;',
      'parallel runs must never share one bundle dir (pass --bundle out/bundle-shared',
      'to share a bundle built once instead).',
    ].join('\n'));
    return;
  }

  const preview = Boolean(flags.preview);
  const scale = flags.scale !== undefined ? Number(flags.scale) : (preview ? 0.5 : 1);
  if (!Number.isFinite(scale) || scale <= 0) {
    console.error(`Invalid --scale: ${flags.scale} (must be a number > 0)`);
    process.exit(1);
  }
  // Story renders default to port 3051 (the story coordinator uses 3050 on
  // the master; another staging copy uses 3052). All other commands keep
  // render_lib's default (3050).
  const port = flags.port !== undefined ? Number(flags.port) : (cmd === 'story' ? 3051 : undefined);
  if (port !== undefined && (!Number.isInteger(port) || port < 1 || port > 65535)) {
    console.error(`Invalid --port: ${flags.port} (must be an integer 1-65535)`);
    process.exit(1);
  }
  const logLevel = typeof flags.log === 'string' ? flags.log : 'error';
  const timeoutMs = flags.timeout !== undefined ? Number(flags.timeout) : 180_000;
  if (!Number.isFinite(timeoutMs) || timeoutMs <= 0) {
    console.error(`Invalid --timeout: ${flags.timeout} (must be a number > 0)`);
    process.exit(1);
  }
  const opts = buildRenderOptions({ port, logLevel, scale, timeoutMs });
  let inputProps = {};
  if (typeof flags.props === 'string') {
    try {
      inputProps = JSON.parse(flags.props);
    } catch (err) {
      console.error(`Invalid --props JSON: ${flags.props}`);
      process.exit(1);
    }
  }

  if (cmd === 'still') {
    const comp = flags.comp || 'MotionBlocks';
    const frames = String(flags.frames ?? '0').split(',').filter(Boolean).map(Number);
    const outDir = path.resolve(String(flags['out-dir'] || 'out/stills'));
    const pattern = String(flags.pattern || 'frame-{frame:4}.png');
    const skipExisting = Boolean(flags['skip-existing']);
    const entry = comp === 'MotionBlocks' ? 'src/short-entry.tsx' : 'src/index.ts';
    const serveUrl = await getServeUrl({ bundleDir: flags.bundle, entry });
    const items = frames.map((frame) => ({
      id: comp,
      frame,
      inputProps,
      output: path.join(outDir, formatFrameName(pattern, frame)),
      skipIfExists: skipExisting,
    }));
    const { rendered, skipped } = await renderStillBatch({
      serveUrl,
      items,
      opts,
      onDone: (item) => console.log('still ok ->', path.basename(item.output)),
    });
    console.log(`done: ${rendered} rendered, ${skipped} skipped`);
    return;
  }

  if (cmd === 'range') {
    const comp = flags.comp || 'CircleShowcase';
    const start = Number(flags.start ?? 0);
    const end = Number(flags.end ?? start);
    const outDir = path.resolve(String(flags['out-dir'] || 'out/stills'));
    const pattern = String(flags.pattern || 'frame-{frame}.png');
    const serveUrl = await getServeUrl({ bundleDir: flags.bundle });
    const items = [];
    for (let f = start; f <= end; f++) {
      items.push({
        id: comp,
        frame: f,
        inputProps,
        output: path.join(outDir, formatFrameName(pattern, f)),
        skipIfExists: !flags.overwrite,
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
    console.log(`range ${start}-${end} done: ${rendered} rendered, ${skipped} skipped, ${((Date.now() - t0) / 1000).toFixed(1)}s total`);
    return;
  }

  if (cmd === 'story') {
    // Story video: ALL frames as stills via renderStillBatch, then ffmpeg
    // assembly + soundtrack mux. No video-renderer call anywhere on this path.
    const arg = pos[1];
    const slug = arg
      ? path.basename(arg).replace(/\.py$/, '')
      : 'story';
    // Validate the range up front, before any bundle/browser work, so a
    // bad --start/--end fails fast (notably for --assemble-only, which
    // does no bundling or browser work at all). The upper bound against
    // the story length is checked below, once the composition is loaded.
    const start = Number(flags.start ?? 0);
    const end = Number(flags.end ?? -1); // -1 = to the end of the story
    if (!Number.isInteger(start) || start < 0) {
      console.error(`Invalid --start: ${flags.start ?? 0} (must be an integer >= 0)`);
      process.exit(1);
    }
    if (flags.end !== undefined && (!Number.isInteger(end) || end < start)) {
      console.error(`Invalid --end: ${flags.end} (must be an integer >= --start ${start})`);
      process.exit(1);
    }
    const assembleOnly = Boolean(flags['assemble-only']);
    const stillsOnly = Boolean(flags['stills-only']);
    if (assembleOnly) {
      // Re-assembly only: no bundle, no browser. fps is the fixed story
      // fps (30); the range was validated above and missing stills fail
      // loudly inside assembleStillsToVideo.
      const stillsDirA = path.resolve(String(flags['stills-dir'] || path.join('out', 'stills', slug)));
      // No --end given: assemble every still on disk (max frame-*.png).
      let endA = end;
      if (endA === -1) {
        const present = fs.existsSync(stillsDirA)
          ? fs.readdirSync(stillsDirA).map((n) => /^frame-(\d+)\.png$/.exec(n)?.[1]).filter(Boolean).map(Number)
          : [];
        if (!present.length) {
          console.error(`--assemble-only: no --end given and no stills in ${stillsDirA} to derive one from.`);
          process.exit(1);
        }
        endA = Math.max(...present);
      }
      const framesA = endA - start + 1;
      const outA = path.resolve(String(flags.out || path.join('out', `${slug}-f${start}-${endA}.mp4`)));
      verifyLoadedStory(slug);
      const audioA = resolveAudio(flags);
      const result = await assembleStillsToVideo({ stillsDir: stillsDirA, start, frames: framesA, fps: STORY_VIDEO.fps, audio: audioA, out: outA });
      console.log(`story video done: ${result.out}`);
      console.log(`  frames: ${result.frames} (expected ${framesA}), duration: ${result.duration.toFixed(2)}s (expected ${(framesA / STORY_VIDEO.fps).toFixed(2)}s), audio: ${result.hasAudio ? 'present' : 'NONE — video-only'}`);
      return;
    }
    // PARALLEL-SAFETY: without --bundle, bundle into a per-process dir
    // (pid in the name) — parallel `story` runs must never rebuild the
    // one shared out/bundle-story dir concurrently, or a half-written
    // bundle corrupts every shard. The shared-bundle workflow (bundle
    // once, pass --bundle to every shard) keeps working unchanged.
    const serveUrl = flags.bundle
      ? await getServeUrl({ bundleDir: flags.bundle, entry: 'src/short-entry.tsx' })
      : await bundleToDir({ outDir: `out/bundle-story-p${process.pid}`, entry: 'src/short-entry.tsx' });
    // Read the loaded story's length/fps from the composition itself.
    const browser = await openBrowser('chrome', {
      browserExecutable: opts.browserExecutable ?? null,
      chromiumOptions: opts.chromiumOptions,
      chromeMode: opts.chromeMode,
      logLevel: opts.logLevel,
    });
    let comp;
    try {
      comp = await selectComposition({
        serveUrl, id: 'MotionBlocks', inputProps,
        puppeteerInstance: browser, port: opts.port, logLevel: opts.logLevel,
      });
    } finally {
      await browser.close({ silent: true });
    }
    const totalFrames = comp.durationInFrames;
    const fps = comp.fps;
    const endF = end === -1 ? totalFrames - 1 : end;
    if (endF < start || endF >= totalFrames) {
      console.error(`Invalid range ${start}-${endF}: story "${slug}" has ${totalFrames} frames (0-${totalFrames - 1}), ${fps} fps.`);
      process.exit(1);
    }
    verifyLoadedStory(slug);
    const frames = endF - start + 1;
    const fullRange = start === 0 && endF === totalFrames - 1;
    const stillsDir = path.resolve(String(flags['stills-dir'] || path.join('out', 'stills', slug)));
    const out = path.resolve(String(
      flags.out || (fullRange ? path.join('out', `${slug}.mp4`) : path.join('out', `${slug}-f${start}-${endF}.mp4`))
    ));
    const audio = resolveAudio(flags);

    const items = [];
    for (let f = start; f <= endF; f++) {
      items.push({
        id: 'MotionBlocks',
        frame: f,
        inputProps,
        output: path.join(stillsDir, stillsFileName(f)),
        skipIfExists: !flags.overwrite,
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
    console.log(`stills ${start}-${endF} done: ${rendered} rendered, ${skipped} skipped (resume), ${((Date.now() - t0) / 1000).toFixed(1)}s total`);
    if (stillsOnly) {
      console.log(`stills-only: stills in ${stillsDir}; assemble later with: node scripts/render.mjs story ${slug} --start ${start} --end ${endF} --assemble-only --out ${out}`);
      return;
    }
    const result = await assembleStillsToVideo({ stillsDir, start, frames, fps, audio, out });
    console.log(`story video done: ${result.out}`);
    console.log(`  frames: ${result.frames} (expected ${frames}), duration: ${result.duration.toFixed(2)}s (expected ${(frames / fps).toFixed(2)}s), audio: ${result.hasAudio ? 'present' : 'NONE — video-only'}`);
    return;
  }

  if (cmd === 'preset') {
    const name = pos[1];
    const presets = getPresets();
    const preset = presets[name];
    if (!preset) {
      console.error(`Unknown preset "${name}". Available: ${Object.keys(presets).join(', ')}`);
      process.exit(1);
    }
    const serveUrl = await getServeUrl({ bundleDir: flags.bundle });
    if (preset.stills?.length) {
      await renderStillBatch({
        serveUrl,
        items: preset.stills,
        opts,
        onDone: (item) => console.log('still ok ->', path.basename(item.output)),
      });
    }
    // Preset `videos` entries are data only (every preset has videos: [])
    // — video rendering is deliberately excluded from this CLI, so there
    // is no video loop here.
    return;
  }

  console.error(`Unknown subcommand "${cmd}". Run "node scripts/render.mjs help".`);
  process.exit(1);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
