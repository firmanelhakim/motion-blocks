/**
 * Eevee-style look upgrade — single toggle for the whole package.
 *
 * ON (default for the test): solid PMREM environment lighting, a
 * key/fill/rim lighting rig with PCFSoft shadows, ACES filmic tone
 * mapping, and a subtle UnrealBloom post pass. OFF restores the exact
 * pre-upgrade lighting (flat ambient + hemisphere + one sun).
 *
 * The toggle is a module constant on purpose: the Remotion bundle is
 * built once and reused by `render.mjs still/range/story`, so an env
 * var would not reliably reach the bundled code. Flip this one line
 * to switch the look off.
 */
export const LOOK_EEVEE = true;

/** Tuned constants for the Eevee look (day / night pairs where they differ). */
export const EEVEE_LOOK = {
  /** PMREM RoomEnvironment strength — the "solid environment" ambient. */
  envIntensityDay: 0.7,
  envIntensityNight: 0.16,
  /** ACES filmic exposure. */
  exposureDay: 1.08,
  exposureNight: 1.0,
  /** UnrealBloomPass (half-resolution mip chain): keep it subtle — only
   * bright highlights (sky, lamps, sunlit ice) should glow. */
  bloomStrength: 0.18,
  bloomRadius: 0.5,
  bloomThreshold: 0.88,
  /** Light rig (applied in MotionBlocksComposition when the look is on). */
  ambientDay: 0.55,
  ambientNight: 0.25,
  hemisphereDay: 0.45,
  hemisphereNight: 0.35,
  /** Hemisphere ground colour (Eevee day only): lightened from #334155 so
   * downward-facing surfaces — the classroom ceiling underside — are not
   * starved when ambient drops. v3: #64748B closed about half the gap;
   * #94A3B8 closes most of the rest. Night keeps the dark ground. */
  hemisphereGroundDay: '#94A3B8',
  sunDay: 2.6,
  sunNight: 1.3,
  fillDay: 0.55,
  fillNight: 0.3,
  rimDay: 1.1,
  rimNight: 0.6,
  /** ACES caps the brightest blue channel (~234 out for a 255 input), so
   * bright day skies come out paler than the raw colour. These
   * pre-compensated sky colours restore the blue-vs-red separation ACES
   * removes; R/G land back on target, B lands at the ACES cap instead of
   * 254. Only the two bright day skies are mapped — night / interior /
   * undersea skies are untouched. */
  skyCompensation: {
    '#BFDBFE': '#A0D0FF', // pale icy blue (ice street)
    '#38BDF8': '#3C9CFC', // bright exterior blue
  } as Record<string, string>,
} as const;

/** ACES-compensated sky colour: identity unless the Eevee look is on in daytime. */
export function eeveeSkyColor(sky: string, isNight: boolean): string {
  if (!LOOK_EEVEE || isNight) return sky;
  return EEVEE_LOOK.skyCompensation[sky] ?? sky;
}
