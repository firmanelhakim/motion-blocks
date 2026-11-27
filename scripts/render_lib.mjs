/**
 * Shared programmatic @remotion/renderer helpers for CPU-only Linux VPS renders.
 *
 * Centralizes:
 * - Software WebGL + OOM-safe Chromium flags (`gl: 'swangle'`,
 *   `--use-angle=swiftshader`, `--enable-unsafe-swiftshader`,
 *   `--disable-dev-shm-usage`, `--force-gpu-mem-available-mb=1024`).
 * - Correct top-level `browserExecutable` and `port` options (fixes the legacy
 *   scripts that nested `browserExecutable` inside `chromiumOptions` and used
 *   non-existent `serveStatic: { port }`).
 * - CPU-safe concurrency (~50% vCPUs, RAM-capped at ~2 GiB/tab).
 * - Warm single-browser reuse (`openBrowser` + `puppeteerInstance`) across
 *   multi-still loops to avoid cold-starting Chromium per frame.
 *
 * Stills only — no video rendering in this module (selective port; the
 * upstream `renderVideo` helper was deliberately not ported).
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { fileURLToPath } from 'node:url';
import { bundle } from '@remotion/bundler';
import { openBrowser, renderStill, selectComposition } from '@remotion/renderer';

const execFileAsync = promisify(execFile);

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const ENGINE_ROOT = path.resolve(__dirname, '..');

export const SWIFTSHADER_FLAGS = {
  'use-angle': 'swiftshader',
  'enable-unsafe-swiftshader': true,
  'disable-dev-shm-usage': true,
  'force-gpu-mem-available-mb': '1024',
};

export function defaultOutDir(...segments) {
  // Repo-relative by default (out/ under the engine root, gitignored).
  // Override with REMOTION_OUT for a shared/dev-machine location.
  // Previously this hardcoded a dev-VM-only path under the home directory.
  const base = process.env.REMOTION_OUT
    ? path.resolve(process.env.REMOTION_OUT)
    : path.join(ENGINE_ROOT, 'out');
  return path.join(base, ...segments);
}

/**
 * Chromium executable for Remotion's programmatic path.
 *
 * Precedence: REMOTION_CHROME_PATH, then CHROME_BIN, then the newest
 * installed Playwright Chromium (chromium-<rev>/chrome-linux/chrome, picked
 * by highest revision number — never pin one revision here; a pinned
 * revision returns null on any machine with a different Playwright
 * install and Remotion falls back to downloading Chrome).
 * Returns null when nothing is found (Remotion then uses its default).
 */
export function detectBrowserExecutable() {
  for (const envVar of ['REMOTION_CHROME_PATH', 'CHROME_BIN']) {
    const p = process.env[envVar];
    if (p && fs.existsSync(p)) {
      return p;
    }
  }
  const cacheDir = path.join(os.homedir(), '.cache/ms-playwright');
  let newest = null;
  let newestRev = -1;
  try {
    for (const entry of fs.readdirSync(cacheDir)) {
      const m = /^chromium-(\d+)$/.exec(entry);
      if (!m) continue;
      const candidate = path.join(cacheDir, entry, 'chrome-linux', 'chrome');
      if (fs.existsSync(candidate) && Number(m[1]) > newestRev) {
        newestRev = Number(m[1]);
        newest = candidate;
      }
    }
  } catch {
    // No Playwright cache dir — fall through to null.
  }
  return newest;
}

/**
 * Canonical concurrency rule for the JS/TS side: ~50% of vCPUs, RAM-capped
 * at ~2 GiB per SwiftShader tab, at least 1. remotion.config.ts imports
 * this; scripts/make_short.py has a Python port of the same rule (it
 * cannot import JS — keep the two formulas in sync when changing this).
 */
export function safeConcurrency(explicit) {
  if (explicit !== undefined && explicit !== null && Number(explicit) >= 1) {
    return Math.floor(Number(explicit));
  }
  if (process.env.REMOTION_CONCURRENCY && Number(process.env.REMOTION_CONCURRENCY) >= 1) {
    return Math.floor(Number(process.env.REMOTION_CONCURRENCY));
  }
  const vcpus = Math.max(1, os.cpus().length);
  const ramCap = Math.max(1, Math.floor(os.totalmem() / (2 * 1024 ** 3)));
  return Math.max(1, Math.min(Math.floor(vcpus / 2) || 1, ramCap));
}

export function buildRenderOptions({
  port = process.env.PORT ? Number(process.env.PORT) : 3050,
  timeoutMs = 180_000,
  logLevel = 'error',
  scale = 1,
  browserExecutable = detectBrowserExecutable(),
  chromeMode = 'chrome-for-testing',
} = {}) {
  // Deliberately does NOT load remotion.config.ts: this programmatic
  // path sets its own Chromium flags, Chrome mode, port and concurrency
  // here (see safeConcurrency). The config file applies to the Remotion
  // CLI path only (notably its JPEG intermediate format, which the
  // stills path does not use — it writes lossless PNG stills).
  const opts = {
    chromiumOptions: {
      gl: 'swangle',
      enableMultiProcessOnLinux: true,
      flags: SWIFTSHADER_FLAGS,
    },
    chromeMode,
    port,
    timeoutInMilliseconds: timeoutMs,
    logLevel,
  };
  if (browserExecutable) {
    opts.browserExecutable = browserExecutable;
  }
  if (scale !== 1) {
    opts.scale = scale;
  }
  return opts;
}

export async function getServeUrl({ bundleDir, entry = 'src/index.ts' } = {}) {
  if (bundleDir) {
    return path.resolve(ENGINE_ROOT, bundleDir);
  }
  // No shared bundle: bundle into a per-process dir under out/ (same
  // bundleToDir approach as the story path), NOT Remotion's temp dir —
  // a concurrent cleanup of the shared temp dir could wipe the bundle
  // mid-render. The dir name carries the entry slug and pid so parallel
  // processes never share one.
  const slug = path.basename(entry).replace(/\.[^.]+$/, '');
  return bundleToDir({ outDir: path.join('out', `bundle-${slug}-p${process.pid}`), entry });
}

/**
 * Bundle the entry point into a persistent directory under the engine
 * (instead of a throwaway /tmp dir) and return its path. The story
 * command uses this: /tmp bundle dirs are shared with every other agent
 * and render on this VM, and a concurrent `rm -rf /tmp/remotion-*`
 * cleanup can wipe a bundle mid-render (observed: selectComposition
 * failing on a half-written bundle). A bundle under out/ belongs to
 * this engine copy alone. Rebuilt on every invocation (~6 s with the
 * webpack cache), so it never goes stale.
 *
 * PARALLEL-SAFETY RULE: never point two concurrent processes at the
 * same outDir — webpack writes into it and a half-written bundle can
 * corrupt every shard. Callers that run in parallel must pass a unique
 * dir (e.g. include the frame range or process.pid); the shared-bundle
 * workflow (bundle once, pass --bundle to every shard) is the only
 * safe way to share one dir. Old per-process bundle dirs under out/
 * are safe to delete once their process has exited.
 */
export async function bundleToDir({ outDir, entry = 'src/short-entry.tsx' } = {}) {
  const abs = path.resolve(ENGINE_ROOT, outDir);
  await bundle({
    entryPoint: path.resolve(ENGINE_ROOT, entry),
    outDir: abs,
    webpackOverride: (c) => c,
  });
  return abs;
}

/**
 * Open a single headless Chrome instance and share it across multiple
 * `selectComposition` / `renderStill` calls.
 */
export async function withBrowser(opts, fn) {
  const browser = await openBrowser('chrome', {
    browserExecutable: opts.browserExecutable ?? null,
    chromiumOptions: opts.chromiumOptions,
    chromeMode: opts.chromeMode,
    logLevel: opts.logLevel,
  });
  try {
    return await fn(browser);
  } finally {
    await browser.close({ silent: true });
  }
}

/**
 * Assemble rendered stills into a story video with ffmpeg, and mux the
 * soundtrack. This is the ONLY video path in this module: stills +
 * ffmpeg, never the Remotion video renderer (proven to drift
 * deterministically — frame 0 exact, ~RMSE 157 by frame 299 — and to
 * glitch with blank-white / tiled frames).
 *
 * Proven assembly settings — do not change: 30 fps, libx264, CRF 18,
 * yuv420p, faststart. Audio is AAC 160k from the soundtrack wav; the
 * audio is NEVER stripped — a delivered upscale once went out silent
 * because audio was stripped, and audio is part of the check.
 *
 * `frames` is the exact frame count (end - start + 1). The output is
 * forced to exactly `frames / fps` seconds with `-t`, so a soundtrack
 * longer than the video is cut and a shorter one never truncates the
 * video. For a frame range starting at `start > 0`, the audio is
 * seeked to `start / fps` so narration stays in sync.
 *
 * Returns `{ out, frames, duration, hasAudio }` after verifying the
 * output with ffprobe (frame count, duration, audio stream).
 */
export const STORY_VIDEO = Object.freeze({
  fps: 30,
  codec: 'libx264',
  crf: 18,
  pixFmt: 'yuv420p',
  audioCodec: 'aac',
  audioBitrate: '160k',
});

/**
 * Still image format for the story pipeline. PNG is the lossless
 * default; `jpeg` writes .jpg stills (quality set at the renderStill
 * call) — the disk-saving experiment: JPEGs run ~3–5x smaller per
 * frame than PNG at quality 90 (measured on ice_floats), at a small
 * lossy cost the final x264 encode mostly hides. Extension is `jpg`
 * (not `jpeg`) so ffmpeg's image2 demuxer and the `--assemble-only`
 * glob see a normal suffix.
 */
export const STILL_IMAGE_FORMATS = Object.freeze(['png', 'jpeg']);

export function stillsFileName(frame, imageFormat = 'jpeg') {
  const ext = imageFormat === 'jpeg' ? 'jpg' : 'png';
  return `frame-${String(frame).padStart(5, '0')}.${ext}`;
}

/** JPEG size from the first SOF0/1/2 marker (header scan, no decode). */
function readJpegSize(file) {
  const buf = fs.readFileSync(file);
  if (buf.length < 4 || buf[0] !== 0xff || buf[1] !== 0xd8) return null; // not SOI
  let i = 2;
  while (i + 1 < buf.length) {
    if (buf[i] !== 0xff) return null; // not a marker
    let marker = buf[i + 1];
    while (marker === 0xff) {
      i++;
      marker = buf[i + 1];
    }
    if (marker === 0x00) {
      i += 2; // stuffed byte, not a marker
      continue;
    }
    // Standalone markers carry no length field.
    if (marker === 0xd8 || marker === 0xd9 || (marker >= 0xd0 && marker <= 0xd7) || marker === 0x01) {
      i += 2;
      continue;
    }
    if (i + 4 > buf.length) return null;
    const len = buf.readUInt16BE(i + 2);
    if (len < 2 || i + 2 + len > buf.length) return null;
    if (marker === 0xc0 || marker === 0xc1 || marker === 0xc2) {
      // SOF segment: precision(1), height(2), width(2), components(1).
      if (len < 8) return null;
      const height = buf.readUInt16BE(i + 5);
      const width = buf.readUInt16BE(i + 7);
      if (!Number.isFinite(width) || !Number.isFinite(height) || width < 1 || height < 1) return null;
      return { width, height };
    }
    if (marker === 0xda) return null; // SOS: scan data starts, no SOF after this
    i += 2 + len;
  }
  return null;
}

/** Still size for either intermediate format: PNG header or JPEG SOF. */
function readStillSize(file) {
  return readPngSize(file) ?? readJpegSize(file);
}

/** PNG signature (first 8 bytes) + IHDR width/height. */
function readPngSize(file) {
  const buf = fs.readFileSync(file);
  const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
  if (buf.length < 24 || !buf.subarray(0, 8).equals(PNG_SIG)) return null;
  const width = buf.readUInt32BE(16);
  const height = buf.readUInt32BE(20);
  if (!Number.isFinite(width) || !Number.isFinite(height) || width < 1 || height < 1) return null;
  return { width, height };
}

async function stillMeanLuma(file) {
  // ffmpeg signalstats YAVG (0-255). A blank white/black frame from a
  // glitched render reads ~255 / ~0; real frames sit in between.
  const { stdout, stderr } = await execFileAsync('ffmpeg', [
    '-v', 'info', '-i', file, '-vf', 'signalstats', '-f', 'null', '-',
  ]);
  const m = /YAVG:\s*([0-9.]+)/.exec(stdout + stderr);
  return m ? Number(m[1]) : null;
}

export async function assembleStillsToVideo({
  stillsDir,
  start = 0,
  frames,
  fps = STORY_VIDEO.fps,
  audio = null,
  out,
  imageFormat = 'jpeg',
}) {
  if (!frames || frames < 1) {
    throw new Error('assembleStillsToVideo: frames must be >= 1');
  }
  // Fail loudly on a missing still instead of silently producing a short video.
  const missing = [];
  for (let f = start; f < start + frames; f++) {
    if (!fs.existsSync(path.join(stillsDir, stillsFileName(f, imageFormat)))) {
      missing.push(f);
    }
  }
  if (missing.length) {
    throw new Error(
      `assembleStillsToVideo: ${missing.length} still(s) missing in ${stillsDir} ` +
        `(first: ${missing.slice(0, 5).join(', ')}) — render the range first`
    );
  }
  // Sampled still checks (first, middle, last): every sampled still must
  // be a valid still (PNG or JPEG) and share one resolution, and must not
  // be a blank (near-black / near-white) frame — the known video-renderer
  // glitch mode. This is a cheap gate, not a full-frame review: only 3
  // frames are sampled, so a bad frame elsewhere still needs an eye check.
  const sampleFrames = [...new Set([start, start + Math.floor(frames / 2), start + frames - 1])];
  let refSize = null;
  for (const f of sampleFrames) {
    const file = path.join(stillsDir, stillsFileName(f, imageFormat));
    const size = readStillSize(file);
    if (!size) {
      throw new Error(`assembleStillsToVideo: sampled still ${file} is not a valid PNG or JPEG still — re-render the range`);
    }
    if (!refSize) refSize = size;
    if (size.width !== refSize.width || size.height !== refSize.height) {
      throw new Error(
        `assembleStillsToVideo: sampled still ${file} is ${size.width}x${size.height}, ` +
          `expected ${refSize.width}x${refSize.height} — re-render the range`
      );
    }
    const yavg = await stillMeanLuma(file);
    if (yavg !== null && (yavg <= 1 || yavg >= 254)) {
      throw new Error(
        `assembleStillsToVideo: sampled still ${file} looks blank (mean luma ${yavg}) — re-render the range`
      );
    }
  }
  const duration = frames / fps;
  const ext = imageFormat === 'jpeg' ? 'jpg' : 'png';
  const inputPattern = path.join(stillsDir, `frame-%05d.${ext}`);
  const args = [
    '-y', '-v', 'error',
    '-framerate', String(fps),
    '-start_number', String(start),
    '-i', inputPattern,
  ];
  if (audio) {
    // -ss before -i seeks the audio input so a range stays in sync.
    args.push('-ss', String(start / fps), '-i', audio);
  }
  args.push(
    '-frames:v', String(frames),
    '-t', String(duration),
    '-c:v', STORY_VIDEO.codec,
    '-crf', String(STORY_VIDEO.crf),
    '-pix_fmt', STORY_VIDEO.pixFmt,
    '-movflags', '+faststart',
  );
  if (audio) {
    args.push('-c:a', STORY_VIDEO.audioCodec, '-b:a', STORY_VIDEO.audioBitrate);
  }
  args.push(out);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  await execFileAsync('ffmpeg', args);

  // Verify the output: exact frame count, duration, and audio stream.
  const probe = await execFileAsync('ffprobe', [
    '-v', 'error', '-count_frames',
    '-select_streams', 'v:0',
    '-show_entries', 'stream=nb_read_frames',
    '-show_entries', 'format=duration',
    '-of', 'json', out,
  ]);
  const info = JSON.parse(probe.stdout);
  const gotFrames = Number(info.streams?.[0]?.nb_read_frames);
  const gotDuration = Number(info.format?.duration);
  if (gotFrames !== frames) {
    throw new Error(`assembleStillsToVideo: ${out} has ${gotFrames} frames, expected ${frames}`);
  }
  if (Math.abs(gotDuration - duration) > 0.15) {
    throw new Error(`assembleStillsToVideo: ${out} is ${gotDuration}s, expected ${duration}s`);
  }
  let hasAudio = false;
  if (audio) {
    const aProbe = await execFileAsync('ffprobe', [
      '-v', 'error', '-select_streams', 'a:0',
      '-show_entries', 'stream=codec_type',
      '-of', 'csv=p=0', out,
    ]);
    hasAudio = aProbe.stdout.trim() === 'audio';
    if (!hasAudio) {
      throw new Error(`assembleStillsToVideo: ${out} has no audio stream after muxing ${audio}`);
    }
    // Audio track must last about as long as the video: a truncated mux
    // would otherwise ship a Short that goes silent part-way through.
    // Tolerance is the same ±0.15 s kept for the video duration below —
    // kept, not tightened, because no full render was run to validate a
    // tighter bound (container rounding alone can eat a few ms).
    const aDurProbe = await execFileAsync('ffprobe', [
      '-v', 'error', '-select_streams', 'a:0',
      '-show_entries', 'stream=duration',
      '-of', 'default=noprint_wrappers=1:nokey=1', out,
    ]);
    const audioDuration = Number(aDurProbe.stdout.trim());
    if (Number.isFinite(audioDuration) && Math.abs(audioDuration - duration) > 0.15) {
      throw new Error(`assembleStillsToVideo: ${out} audio is ${audioDuration}s, expected ${duration}s`);
    }
  }
  return { out, frames: gotFrames, duration: gotDuration, hasAudio };
}

export function formatFrameName(pattern, frame) {
  return pattern.replace(/\{frame(?::(\d+))?\}/g, (_, pad) =>
    pad ? String(frame).padStart(Number(pad), '0') : String(frame)
  );
}

/**
 * Render multiple stills using a single warm Chromium browser instance.
 * Each item: `{ id, frame, output, inputProps?, skipIfExists? }`.
 *
 * `imageFormat` (`'jpeg'` default, or `'png'`) is passed through to
 * renderStill; `jpegQuality` (1–100) only applies to JPEG. The resume
 * fingerprint accepts either format (PNG header or JPEG SOF).
 *
 * Resume fingerprint: a still is only skipped when it exists, is
 * non-empty, and passes a still header/size sanity check. A zero-byte or
 * corrupt still is re-rendered instead of trusted. NOTE: this is NOT a
 * pixel-blank check — decoding every still to test for blank frames
 * would cost a full image decode per frame on every resume; the
 * blank-frame gate lives in assembleStillsToVideo (sampled) instead.
 */
export async function renderStillBatch({
  serveUrl,
  items,
  opts,
  onDone,
  imageFormat = 'jpeg',
  jpegQuality,
}) {
  const compCache = new Map();
  return withBrowser(opts, async (browser) => {
    let rendered = 0;
    let skipped = 0;
    for (const item of items) {
      fs.mkdirSync(path.dirname(item.output), { recursive: true });
      if (item.skipIfExists && fs.existsSync(item.output)) {
        let valid = false;
        try {
          valid = fs.statSync(item.output).size > 0 && readStillSize(item.output) !== null;
        } catch {
          valid = false;
        }
        if (valid) {
          skipped++;
          continue;
        }
        // Missing/zero-byte/corrupt still: fall through and re-render it.
      }
      const inputProps = item.inputProps ?? {};
      const key = `${item.id}:${JSON.stringify(inputProps)}`;
      let comp = compCache.get(key);
      if (!comp) {
        comp = await selectComposition({
          serveUrl,
          id: item.id,
          inputProps,
          puppeteerInstance: browser,
          port: opts.port,
          logLevel: opts.logLevel,
        });
        compCache.set(key, comp);
      }
      await renderStill({
        ...opts,
        composition: comp,
        serveUrl,
        inputProps,
        frame: item.frame,
        output: item.output,
        puppeteerInstance: browser,
        imageFormat,
        // jpegQuality is only meaningful for JPEG; omit it for PNG so
        // Remotion never sees a quality value on a lossless render.
        ...(imageFormat === 'jpeg' ? { jpegQuality } : {}),
      });
      rendered++;
      if (onDone) onDone(item, { rendered, skipped });
    }
    return { rendered, skipped };
  });
}
