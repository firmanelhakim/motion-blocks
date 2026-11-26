/**
 * expressions.tsx — the common face-expression system for the engine's kit
 * characters (BoltBoy, CasualMan, and any future kit character).
 *
 * Design (mirrors the Pose contract):
 *  - An `ExpressionName` registry. The 9 engine expressions are ported from
 *    R6Character's createFaceTexture recipes (same idiom, same canvas);
 *    the rest are new, drawn in the same style.
 *  - Each expression is a `FaceParts` descriptor: a brow style, an eye
 *    style, a mouth style, and optional extras. The descriptor is shared;
 *    only the `FaceLayout` (where the eyes/brows/mouth sit) differs per
 *    character, because each character's face has its own coordinates and
 *    fixed features (CasualMan's beard is drawn around the mouth).
 *  - `drawFaceParts(g, layout, parts, t)` renders one expression. `t`
 *    animates the moving extras (falling tears, dizzy spin).
 *  - `useExpressionTexture(drawFace, expression, t)` re-creates the canvas
 *    texture when the expression (or the animation phase) changes.
 *  - `faceTransition(from, to, k)` draws two expressions with an alpha
 *    crossfade — the face equivalent of `lerpPose`.
 *
 * Divergences from the engine's R6Character recipes, noted honestly:
 *  - 'panic' shares the 'shocked' branch in R6Character (no sweat drop
 *    drawn there). Here panic gets a sweat drop, so the two differ.
 *  - 'cool' in R6Character is a worried/smirk face with a white mouth bar,
 *    not sunglasses. Here cool is sunglasses, matching the name and the
 *    catalog.
 *  - R6Character's face is wrapped on a cylinder; kit faces sit on a flat
 *    plane, so the same expression reads bigger and bolder here.
 */
import {useEffect, useMemo} from 'react';
import * as THREE from 'three';
import {useCanvasTexture} from './kit';

export type ExpressionName =
  | 'smile' | 'grin' | 'laugh' | 'shocked' | 'panic' | 'angry' | 'cool'
  | 'sleeping' | 'deadpan'
  | 'sad' | 'cry' | 'surprised' | 'worried' | 'confused' | 'determined'
  | 'scared' | 'excited' | 'proud' | 'embarrassed' | 'dizzy' | 'love'
  | 'wink' | 'silly' | 'thinking' | 'disgusted' | 'sleepy' | 'smirk';

export type BrowStyle = 'arc' | 'arcHigh' | 'angledDown' | 'angledUp' | 'flat' | 'raised' | 'none';
export type EyeStyle = 'oval' | 'wide' | 'closed' | 'flat' | 'heart' | 'x' | 'star' | 'half' | 'winkL' | 'glance' | 'up';
export type MouthStyle = 'smile' | 'grin' | 'laugh' | 'frown' | 'open' | 'o' | 'line' | 'wavy' | 'tilted' | 'silly' | 'smirk' | 'smallSmile';
export type FaceExtra = 'tears' | 'sweat' | 'blush' | 'tongue' | 'sunglasses';

export interface FaceParts {
  brow: BrowStyle;
  eye: EyeStyle;
  mouth: MouthStyle;
  extras?: FaceExtra[];
}

/** One shared descriptor per expression. Layout (coordinates) is per-character. */
export const EXPRESSION_PARTS: Record<ExpressionName, FaceParts> = {
  smile: {brow: 'arc', eye: 'oval', mouth: 'smile'},
  grin: {brow: 'arc', eye: 'oval', mouth: 'grin'},
  laugh: {brow: 'arc', eye: 'closed', mouth: 'laugh'},
  shocked: {brow: 'raised', eye: 'wide', mouth: 'open'},
  panic: {brow: 'raised', eye: 'wide', mouth: 'open', extras: ['sweat']},
  angry: {brow: 'angledDown', eye: 'oval', mouth: 'frown'},
  cool: {brow: 'arc', eye: 'oval', mouth: 'smirk', extras: ['sunglasses']},
  sleeping: {brow: 'none', eye: 'closed', mouth: 'line'},
  deadpan: {brow: 'flat', eye: 'oval', mouth: 'line'},
  sad: {brow: 'angledUp', eye: 'oval', mouth: 'frown'},
  cry: {brow: 'angledUp', eye: 'oval', mouth: 'wavy', extras: ['tears']},
  surprised: {brow: 'arcHigh', eye: 'wide', mouth: 'o'},
  worried: {brow: 'angledUp', eye: 'oval', mouth: 'wavy'},
  confused: {brow: 'raised', eye: 'glance', mouth: 'tilted'},
  determined: {brow: 'angledDown', eye: 'half', mouth: 'line'},
  scared: {brow: 'raised', eye: 'wide', mouth: 'wavy'},
  excited: {brow: 'arcHigh', eye: 'star', mouth: 'laugh'},
  proud: {brow: 'arc', eye: 'half', mouth: 'smallSmile'},
  embarrassed: {brow: 'arc', eye: 'glance', mouth: 'smallSmile', extras: ['blush']},
  dizzy: {brow: 'arc', eye: 'x', mouth: 'wavy'},
  love: {brow: 'arc', eye: 'heart', mouth: 'smile'},
  wink: {brow: 'arc', eye: 'winkL', mouth: 'smile'},
  silly: {brow: 'arcHigh', eye: 'oval', mouth: 'silly'},
  thinking: {brow: 'arc', eye: 'up', mouth: 'line'},
  disgusted: {brow: 'angledDown', eye: 'half', mouth: 'wavy'},
  sleepy: {brow: 'arc', eye: 'half', mouth: 'o'},
  smirk: {brow: 'arc', eye: 'oval', mouth: 'smirk'},
};

/** Where the face parts sit on one character's 512 canvas. */
export interface FaceLayout {
  eyeL: [number, number];
  eyeR: [number, number];
  eyeRX: number;
  eyeRY: number;
  browY: number;   // brow arc centre height
  browR: number;   // brow arc radius
  mouth: [number, number]; // mouth centre
  mouthW: number;  // mouth width
  ink: string;     // line/fill colour for brows, eyes, mouth outline
  browInk?: string;
}

type G = CanvasRenderingContext2D;

const line = (g: G, x1: number, y1: number, x2: number, y2: number) => {
  g.beginPath(); g.moveTo(x1, y1); g.lineTo(x2, y2); g.stroke();
};

const drawBrows = (g: G, l: FaceLayout, style: BrowStyle) => {
  const ink = l.browInk ?? l.ink;
  g.strokeStyle = ink;
  g.lineWidth = 12;
  const [lx, ly] = [l.eyeL[0], l.browY];
  const [rx, ry] = [l.eyeR[0], l.browY];
  switch (style) {
    case 'arc':
      g.beginPath(); g.arc(lx, ly, l.browR, 1.2 * Math.PI, 1.8 * Math.PI, false); g.stroke();
      g.beginPath(); g.arc(rx, ry, l.browR, 1.2 * Math.PI, 1.8 * Math.PI, false); g.stroke();
      break;
    case 'arcHigh':
      g.beginPath(); g.arc(lx, ly - 14, l.browR, 1.2 * Math.PI, 1.8 * Math.PI, false); g.stroke();
      g.beginPath(); g.arc(rx, ry - 14, l.browR, 1.2 * Math.PI, 1.8 * Math.PI, false); g.stroke();
      break;
    case 'angledDown': // angry / determined: inner ends low
      line(g, lx - 38, ly - 22, lx + 34, ly + 8);
      line(g, rx + 38, ry - 22, rx - 34, ry + 8);
      break;
    case 'angledUp': // sad / worried / cry: inner ends high
      line(g, lx - 38, ly + 6, lx + 34, ly - 14);
      line(g, rx + 38, ry + 6, rx - 34, ry - 14);
      break;
    case 'flat':
      line(g, lx - 34, ly, lx + 34, ly);
      line(g, rx - 34, ry, rx + 34, ry);
      break;
    case 'raised': // shocked / scared / confused: both ends up, inner higher
      line(g, lx - 38, ly + 2, lx + 32, ly - 14);
      line(g, rx + 38, ry + 2, rx - 32, ry - 14);
      break;
    case 'none':
      break;
  }
};

const drawEyeOval = (g: G, x: number, y: number, rx: number, ry: number, ink: string) => {
  g.fillStyle = ink;
  g.beginPath(); g.ellipse(x, y, rx, ry, 0, 0, Math.PI * 2); g.fill();
};

const drawEyeWide = (g: G, x: number, y: number, rx: number, ry: number, ink: string) => {
  g.fillStyle = '#ffffff';
  g.lineWidth = 10;
  g.strokeStyle = ink;
  g.beginPath(); g.ellipse(x, y, rx + 8, ry + 10, 0, 0, Math.PI * 2); g.fill(); g.stroke();
  g.fillStyle = '#111111';
  g.beginPath(); g.ellipse(x, y, 11, 16, 0, 0, Math.PI * 2); g.fill();
};

const drawEyeClosed = (g: G, x: number, y: number, r: number, ink: string) => {
  g.strokeStyle = ink;
  g.lineWidth = 13;
  g.beginPath(); g.arc(x, y, r, 1.1 * Math.PI, 1.9 * Math.PI, false); g.stroke();
};

const drawEyeHeart = (g: G, x: number, y: number, s: number) => {
  g.fillStyle = '#e11d48';
  g.beginPath();
  g.moveTo(x, y + s * 0.9);
  g.bezierCurveTo(x - s * 1.3, y - s * 0.2, x - s * 0.7, y - s * 1.1, x, y - s * 0.3);
  g.bezierCurveTo(x + s * 0.7, y - s * 1.1, x + s * 1.3, y - s * 0.2, x, y + s * 0.9);
  g.fill();
};

const drawEyeX = (g: G, x: number, y: number, s: number, ink: string) => {
  g.strokeStyle = ink;
  g.lineWidth = 11;
  line(g, x - s, y - s, x + s, y + s);
  line(g, x + s, y - s, x - s, y + s);
};

const drawEyeStar = (g: G, x: number, y: number, s: number, ink: string) => {
  g.fillStyle = ink;
  g.beginPath();
  for (let i = 0; i < 10; i++) {
    const r = i % 2 === 0 ? s : s * 0.45;
    const a = (i / 10) * Math.PI * 2 - Math.PI / 2;
    const px = x + Math.cos(a) * r;
    const py = y + Math.sin(a) * r;
    if (i === 0) g.moveTo(px, py); else g.lineTo(px, py);
  }
  g.closePath(); g.fill();
};

const drawEyes = (g: G, l: FaceLayout, style: EyeStyle, t: number) => {
  const [lx, ly] = l.eyeL;
  const [rx, ry] = l.eyeR;
  switch (style) {
    case 'oval':
      drawEyeOval(g, lx, ly, l.eyeRX, l.eyeRY, l.ink);
      drawEyeOval(g, rx, ry, l.eyeRX, l.eyeRY, l.ink);
      break;
    case 'wide':
      drawEyeWide(g, lx, ly, l.eyeRX, l.eyeRY, l.ink);
      drawEyeWide(g, rx, ry, l.eyeRX, l.eyeRY, l.ink);
      break;
    case 'closed':
      drawEyeClosed(g, lx, ly, 26, l.ink);
      drawEyeClosed(g, rx, ry, 26, l.ink);
      break;
    case 'flat':
      g.strokeStyle = l.ink; g.lineWidth = 12;
      line(g, lx - 26, ly, lx + 26, ly);
      line(g, rx - 26, ry, rx + 26, ry);
      break;
    case 'heart':
      drawEyeHeart(g, lx, ly, 24);
      drawEyeHeart(g, rx, ry, 24);
      break;
    case 'x':
      drawEyeX(g, lx, ly, 18, l.ink);
      drawEyeX(g, rx, ry, 18, l.ink);
      break;
    case 'star':
      drawEyeStar(g, lx, ly, 24, l.ink);
      drawEyeStar(g, rx, ry, 24, l.ink);
      break;
    case 'half': // half-lidded: oval with a lid line across the top
      drawEyeOval(g, lx, ly, l.eyeRX, l.eyeRY * 0.7, l.ink);
      drawEyeOval(g, rx, ry, l.eyeRX, l.eyeRY * 0.7, l.ink);
      g.strokeStyle = l.ink; g.lineWidth = 10;
      line(g, lx - l.eyeRX - 4, ly - l.eyeRY * 0.4, lx + l.eyeRX + 4, ly - l.eyeRY * 0.4);
      line(g, rx - l.eyeRX - 4, ry - l.eyeRY * 0.4, rx + l.eyeRX + 4, ry - l.eyeRY * 0.4);
      break;
    case 'winkL': // left eye closed, right open
      drawEyeClosed(g, lx, ly, 26, l.ink);
      drawEyeOval(g, rx, ry, l.eyeRX, l.eyeRY, l.ink);
      break;
    case 'glance': // pupils offset to one side
      drawEyeOval(g, lx, ly, l.eyeRX, l.eyeRY, l.ink);
      drawEyeOval(g, rx, ry, l.eyeRX, l.eyeRY, l.ink);
      g.fillStyle = '#ffffff';
      g.beginPath(); g.arc(lx + 6, ly - 8, 5, 0, Math.PI * 2); g.fill();
      g.beginPath(); g.arc(rx + 6, ry - 8, 5, 0, Math.PI * 2); g.fill();
      break;
    case 'up': // looking up: eyes as small arcs high in the socket
      drawEyeClosed(g, lx, ly - 8, 20, l.ink);
      drawEyeClosed(g, rx, ry - 8, 20, l.ink);
      break;
  }
  void t;
};

const drawMouthSmile = (g: G, mx: number, my: number, w: number, ink: string) => {
  g.strokeStyle = ink; g.lineWidth = 14;
  g.beginPath(); g.arc(mx, my - w * 0.28, w * 0.36, 0.22 * Math.PI, 0.78 * Math.PI, false); g.stroke();
};

const drawMouthGrin = (g: G, mx: number, my: number, w: number, ink: string) => {
  const h = w * 0.45;
  g.fillStyle = '#ffffff'; g.lineWidth = 12; g.strokeStyle = ink;
  g.beginPath(); g.roundRect(mx - w / 2, my - h / 2, w, h, 22); g.fill(); g.stroke();
  g.lineWidth = 7;
  line(g, mx - w * 0.44, my, mx + w * 0.44, my);
};

const drawMouthLaugh = (g: G, mx: number, my: number, w: number, ink: string) => {
  const r = w * 0.38;
  g.fillStyle = '#991b1b';
  g.beginPath(); g.arc(mx, my - r * 0.4, r, 0, Math.PI, false); g.closePath(); g.fill();
  g.lineWidth = 11; g.strokeStyle = ink; g.stroke();
  g.fillStyle = '#ffffff';
  g.fillRect(mx - r * 0.85, my - r * 0.4, r * 1.7, r * 0.28);
};

const drawMouths = (g: G, l: FaceLayout, style: MouthStyle) => {
  const [mx, my] = l.mouth;
  const w = l.mouthW;
  switch (style) {
    case 'smile':
      drawMouthSmile(g, mx, my, w, l.ink);
      break;
    case 'grin':
      drawMouthGrin(g, mx, my, w, l.ink);
      break;
    case 'laugh':
      drawMouthLaugh(g, mx, my, w, l.ink);
      break;
    case 'frown':
      g.strokeStyle = l.ink; g.lineWidth = 14;
      g.beginPath(); g.arc(mx, my + w * 0.3, w * 0.3, 1.2 * Math.PI, 1.8 * Math.PI, false); g.stroke();
      break;
    case 'open': // tall gasping mouth, white with dark outline
      g.fillStyle = '#ffffff'; g.lineWidth = 12; g.strokeStyle = l.ink;
      g.beginPath(); g.roundRect(mx - w * 0.26, my - w * 0.28, w * 0.52, w * 0.5, 20); g.fill(); g.stroke();
      break;
    case 'o':
      g.strokeStyle = l.ink; g.lineWidth = 12;
      g.beginPath(); g.ellipse(mx, my, w * 0.1, w * 0.14, 0, 0, Math.PI * 2); g.stroke();
      break;
    case 'line':
      g.strokeStyle = l.ink; g.lineWidth = 12;
      line(g, mx - w * 0.28, my, mx + w * 0.28, my);
      break;
    case 'wavy': {
      g.strokeStyle = l.ink; g.lineWidth = 11;
      g.beginPath();
      const n = 24;
      for (let i = 0; i <= n; i++) {
        const x = mx - w * 0.28 + (i / n) * w * 0.56;
        const y = my + Math.sin((i / n) * Math.PI * 2) * 7;
        if (i === 0) g.moveTo(x, y); else g.lineTo(x, y);
      }
      g.stroke();
      break;
    }
    case 'tilted':
      g.strokeStyle = l.ink; g.lineWidth = 12;
      line(g, mx - w * 0.26, my + 8, mx + w * 0.26, my - 8);
      break;
    case 'silly':
      drawMouthSmile(g, mx, my, w, l.ink);
      g.fillStyle = '#d04e4a';
      g.beginPath(); g.ellipse(mx, my + w * 0.16, w * 0.16, w * 0.08, 0, 0, Math.PI * 2); g.fill();
      break;
    case 'smirk': // asymmetric: one side higher
      g.strokeStyle = l.ink; g.lineWidth = 13;
      g.beginPath();
      g.moveTo(mx - w * 0.3, my + 6);
      g.quadraticCurveTo(mx, my + w * 0.12, mx + w * 0.3, my - 10);
      g.stroke();
      break;
    case 'smallSmile':
      g.strokeStyle = l.ink; g.lineWidth = 12;
      g.beginPath(); g.arc(mx, my - w * 0.14, w * 0.2, 0.25 * Math.PI, 0.75 * Math.PI, false); g.stroke();
      break;
  }
};

const drawExtras = (g: G, l: FaceLayout, extras: FaceExtra[], t: number) => {
  const [lx, ly] = l.eyeL;
  const [rx, ry] = l.eyeR;
  const [mx, my] = l.mouth;
  for (const e of extras) {
    switch (e) {
      case 'tears': { // falling drops under each eye; t animates the fall
        g.fillStyle = '#38bdf8';
        for (const [x, y0] of [[lx, ly + 30], [rx, ry + 30]] as const) {
          const fall = ((t * 60) % 26);
          const y = y0 + fall;
          g.beginPath();
          g.moveTo(x, y - 12);
          g.quadraticCurveTo(x + 9, y + 2, x, y + 12);
          g.quadraticCurveTo(x - 9, y + 2, x, y - 12);
          g.fill();
        }
        break;
      }
      case 'sweat': {
        g.fillStyle = '#38bdf8';
        const x = rx + 52;
        const y = ry - 34;
        g.beginPath();
        g.moveTo(x, y - 14);
        g.quadraticCurveTo(x + 11, y + 2, x, y + 14);
        g.quadraticCurveTo(x - 11, y + 2, x, y - 14);
        g.fill();
        break;
      }
      case 'blush': {
        g.fillStyle = '#f472b6';
        g.globalAlpha = 0.32;
        g.beginPath(); g.ellipse(lx - 46, ly + 44, 26, 13, 0, 0, Math.PI * 2); g.fill();
        g.beginPath(); g.ellipse(rx + 46, ry + 44, 26, 13, 0, 0, Math.PI * 2); g.fill();
        g.globalAlpha = 1;
        break;
      }
      case 'tongue':
        g.fillStyle = '#d04e4a';
        g.beginPath(); g.ellipse(mx, my + 26, 26, 13, 0, 0, Math.PI * 2); g.fill();
        break;
      case 'sunglasses': {
        g.fillStyle = '#111111';
        for (const [x, y] of [[lx, ly], [rx, ry]] as const) {
          g.beginPath(); g.roundRect(x - 34, y - 22, 68, 44, 12); g.fill();
        }
        g.strokeStyle = '#111111'; g.lineWidth = 8;
        line(g, lx + 34, ly - 4, rx - 34, ry - 4);
        break;
      }
    }
  }
};

/** Render one expression onto a character's face canvas. `t` animates the
 * moving extras (tears fall, dizzy spins are drawn by the caller). */
export const drawFaceParts = (g: G, layout: FaceLayout, expression: ExpressionName, t = 0) => {
  const parts = EXPRESSION_PARTS[expression];
  g.lineCap = 'round';
  drawBrows(g, layout, parts.brow);
  drawEyes(g, layout, parts.eye, t);
  drawMouths(g, layout, parts.mouth);
  if (parts.extras) drawExtras(g, layout, parts.extras, t);
};

type DrawFaceFn = (g: G, expression: ExpressionName, t: number) => void;

// Texture cache ported from Gemini Neon (2026-11-22): one cached 512×512
// CanvasTexture per (drawFace, expression, 8fps phase bucket), so repeated
// expressions across shots/scenes never redraw or leak VRAM. Only the
// time-dependent expressions re-bucket: `cry` (falling tears) and `dizzy`
// (eye 'x'). Neon's anisotropy 8→2 cut reverted — stays 8, as before.
const expressionTexCache = new WeakMap<DrawFaceFn, Map<string, THREE.CanvasTexture>>();

function hasAnimatedExtra(expression: ExpressionName): boolean {
  const parts = EXPRESSION_PARTS[expression];
  if (!parts) return false;
  return Boolean(parts.extras?.includes('tears')) || parts.eye === 'x';
}

function getCachedExpressionTexture(
  drawFace: DrawFaceFn,
  expression: ExpressionName,
  t: number,
): THREE.CanvasTexture {
  let byKey = expressionTexCache.get(drawFace);
  if (!byKey) {
    byKey = new Map();
    expressionTexCache.set(drawFace, byKey);
  }
  const bucket = hasAnimatedExtra(expression) ? Math.floor(t * 8) : 0;
  const key = `${expression}:${bucket}`;
  let tex = byKey.get(key);
  if (!tex) {
    const c = document.createElement('canvas');
    c.width = c.height = 512;
    const g = c.getContext('2d')!;
    g.clearRect(0, 0, 512, 512);
    drawFace(g, expression, bucket / 8);
    tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.anisotropy = 8;
    tex.needsUpdate = true;
    byKey.set(key, tex);
  }
  return tex;
}

/**
 * Canvas texture for one expression. Cached per (drawFace, expression, phase)
 * so repeated expressions across shots/scenes never redraw or leak VRAM.
 * `drawFace` is the character's own face function — it draws its fixed
 * features, then calls `drawFaceParts`.
 */
export const useExpressionTexture = (
  drawFace: DrawFaceFn,
  expression: ExpressionName,
  t = 0,
) => {
  const bucket = hasAnimatedExtra(expression) ? Math.floor(t * 8) : 0;
  return useMemo(
    () => getCachedExpressionTexture(drawFace, expression, bucket / 8),
    [drawFace, expression, bucket],
  );
};

// ---------------------------------------------------------------------------
// Face timeline — the face track of a Performance (runs in parallel with the
// body track from kit.tsx's timelinePose). Face and body are independent:
// any expression can play over any pose.
// ---------------------------------------------------------------------------
export interface FaceSegment { expression: ExpressionName; duration: number; }
/** `from` → `to` with `k` 0..1 (smoothstep). k = 1 means fully `to`. */
export interface FaceState { from: ExpressionName; to: ExpressionName; k: number; }

/** Evaluate a looping face timeline at time t. Crossfades (smoothstep,
 * 0.25s) at every segment boundary, including the wrap, mirroring
 * timelinePose so the two tracks stay in step. */
export const performanceFace = (segments: FaceSegment[], t: number, crossfade = 0.25): FaceState => {
  const total = segments.reduce((a, s) => a + s.duration, 0);
  const tt = ((t % total) + total) % total;
  let start = 0;
  let idx = 0;
  for (let i = 0; i < segments.length; i++) {
    if (tt < start + segments[i].duration) { idx = i; break; }
    start += segments[i].duration;
  }
  const seg = segments[idx];
  const lt = tt - start;
  if (lt < crossfade) {
    const prev = idx > 0 ? segments[idx - 1] : segments[segments.length - 1];
    const k = lt / crossfade;
    const smooth = k * k * (3 - 2 * k);
    return {from: prev.expression, to: seg.expression, k: smooth};
  }
  return {from: seg.expression, to: seg.expression, k: 1};
};

export const faceTimelineDuration = (segments: FaceSegment[]): number => segments.reduce((a, s) => a + s.duration, 0);

/**
 * Canvas texture for a face transition. Reuses the cached single-expression
 * texture whenever no crossfade is active, and disposes transient blended
 * textures when they are replaced or unmounted. Each character's `drawFace`
 * draws its whole face per expression (default inline, the rest via
 * drawFaceParts), with no separate fixed-feature pass, so drawing `from`
 * fully opaque and then `to` on top with alpha `k` is a true crossfade.
 * Steady state reuses the cache (no redraw); a running transition redraws
 * at 30 k-buckets/sec, and animated extras at 8 buckets/sec.
 * (Neon's anisotropy 8→2 cut reverted in the blended path — stays 8.)
 */
export const useFaceTransitionTexture = (
  drawFace: DrawFaceFn,
  face: FaceState,
  t = 0,
) => {
  const isSteady = face.k >= 1 || face.from === face.to;
  const kBucket = isSteady ? 1 : Math.round(face.k * 30);
  const tBucket =
    hasAnimatedExtra(face.to) || (!isSteady && hasAnimatedExtra(face.from))
      ? Math.floor(t * 8)
      : 0;
  const result = useMemo(() => {
    if (isSteady) {
      return {tex: getCachedExpressionTexture(drawFace, face.to, tBucket / 8), owned: false};
    }
    const c = document.createElement('canvas');
    c.width = c.height = 512;
    const g = c.getContext('2d')!;
    g.clearRect(0, 0, 512, 512);
    drawFace(g, face.from, tBucket / 8);
    g.save();
    g.globalAlpha = Math.max(0, Math.min(1, face.k));
    drawFace(g, face.to, tBucket / 8);
    g.restore();
    const tex = new THREE.CanvasTexture(c);
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.anisotropy = 8;
    tex.needsUpdate = true;
    return {tex, owned: true};
  }, [drawFace, face.from, face.to, isSteady, kBucket, tBucket]);

  useEffect(() => {
    if (!result.owned) return;
    return () => {
      result.tex.dispose();
    };
  }, [result]);

  return result.tex;
};

/**
 * Unified face-texture hook for kit characters: avoids baking two separate
 * 512×512 CanvasTextures when a component accepts both `expression` and
 * optional `faceState`.
 */
export const useCharacterFaceTexture = (
  drawFace: DrawFaceFn,
  expression: ExpressionName,
  faceState: FaceState | undefined,
  t = 0,
): THREE.CanvasTexture =>
  useFaceTransitionTexture(
    drawFace,
    faceState ?? {from: expression, to: expression, k: 1},
    t,
  );

/** Backwards-compatible alias: the kit's old `useCanvasTexture` for faces. */
export {useCanvasTexture};
