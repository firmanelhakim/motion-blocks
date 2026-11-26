import { Config } from '@remotion/cli/config';
import { safeConcurrency } from './scripts/render_lib.mjs';

/**
 * CPU-only headless Linux VPS configuration (SwiftShader software WebGL).
 *
 * - `swangle` maps to `--use-gl=angle --use-angle=swiftshader`.
 * - Explicit `chromiumFlags` ensure `--enable-unsafe-swiftshader`,
 *   `--disable-dev-shm-usage`, and a bounded GPU memory budget (`1024` MB)
 *   to prevent Chromium OOM crashes on 4-6 GB RAM VPSes.
 * - Concurrency is the canonical safeConcurrency rule from
 *   scripts/render_lib.mjs (~50% of vCPUs, RAM-capped at ~2 GB per
 *   SwiftShader tab, at least 1 — avoids Remotion's `'50%'` floor-to-0
 *   error on 1-vCPU hosts). Override via `REMOTION_CONCURRENCY` or CLI.
 * - NOTE: this config is loaded by the Remotion CLI path only. The
 *   programmatic path (scripts/render.mjs via render_lib.mjs
 *   buildRenderOptions) deliberately does not load it — it sets its own
 *   Chromium/concurrency options there.
 * - NOTE on image format: JPEG (quality 82) here is for the CLI video
 *   renderer's intermediate frames only. The story path
 *   (scripts/render.mjs story) never uses it — it renders lossless PNG
 *   stills and assembles them with ffmpeg, because JPEG intermediates
 *   would add compression artefacts to every frame of the final video.
 */
Config.setChromiumOpenGlRenderer('swangle');
Config.setChromeMode('chrome-for-testing');
Config.setChromiumFlags({
  'use-angle': 'swiftshader',
  'enable-unsafe-swiftshader': true,
  'disable-dev-shm-usage': true,
  'force-gpu-mem-available-mb': '1024',
});
Config.setConcurrency(safeConcurrency());
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(82);
Config.setOverwriteOutput(true);
