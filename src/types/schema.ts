import type { CharacterLookInput, PresetName } from '../characters/look';

/**
 * Actor id used as a key in `scene.characters`. Either a preset name
 * (see CHARACTER_PRESETS in src/characters/look.ts) or any custom name declared in `story.cast`.
 */
export type CharacterId = PresetName | (string & {});

export type ExpressionId =
  | 'smile'
  | 'grin'
  | 'shocked'
  | 'sleeping'
  | 'panic'
  | 'angry'
  | 'cool'
  | 'laugh'
  | 'deadpan';

export type AnimationMode =
  | 'idle'
  | 'sleep'
  | 'walk'
  | 'sprint'
  | 'jump'
  | 'sit'
  | 'wave'
  | 'point'
  | 'dance'
  | 'knocked'
  | 'panting'
  | 'celebrate'
  | 'fly';

import type { HouseVariantId, LocationId } from '../environments/locations';
export type { HouseVariantId, LocationId };

export type PropId =
  | 'none'
  | 'backpack'
  | 'bloxy_cola'
  | 'pointer'
  | 'pointer_draw'
  | 'pan'
  | 'clipboard'
  | 'hammer'
  | 'wood_plank'
  | 'binoculars'
  | 'halo_gold'
  | 'halo_red'
  | 'creepy_shadow'
  | 'counter_high'
  | 'counter_mid'
  | 'counter_bully'
  | 'counter_3'
  | 'counter_2'
  | 'counter_1'
  | 'counter_0'
  | 'counter_100'
  | 'counter_99'
  | 'counter_98'
  | 'counter_50'
  | 'counter_12'
  | 'mouth_tape';

export interface CharacterKeyframe {
  frame: number;
  position: [number, number, number];
  rotationY: number;
  rotationX?: number;
  rotationZ?: number;
  anim: AnimationMode;
  expression: ExpressionId;
  prop?: PropId;
  chatBubble?: string;
  /** World position the chat bubble floats above, instead of the speaker's
   *  head. For a voice from a character who is off-screen / invisible
   *  (e.g. parked OFF): the bubble is anchored at this spot and shown
   *  whenever the spot itself is on screen, even though the speaker is not
   *  rendered. The tail points down at the anchor. */
  bubbleAnchor?: [number, number, number];
}

export interface CameraShot {
  startFrame: number;
  endFrame: number;
  fromPos: [number, number, number];
  toPos: [number, number, number];
  fromTarget: [number, number, number];
  toTarget: [number, number, number];
  fov?: number;
  shake?: number;
  /** True-circle orbit: when present the camera rides the circle
   *  (centre/radius/height in world space, angles in radians from +Z)
   *  instead of lerping the from/to chord. Set by orbit() in scene.py. */
  arc?: {
    center: [number, number, number];
    radius: number;
    height: number;
    startAngle: number;
    endAngle: number;
  };
}

export interface CaptionCue {
  startFrame: number;
  endFrame: number;
  speaker?: string;
  speakerColor?: string;
  text: string;
  sfxBadge?: string;
}

export interface FxKeyframe {
  frame: number;
  position: [number, number, number];
}

/** One animated "science prop": a simple mesh whose position interpolates
 *  linearly between keyframes (like a character, but no body/face). Used to
 *  SHOW a physical property: the Moon flying away, a water blob rising.
 *  New shapes (2026-11-22, new-asset ports) are full components
 *  rendered by ScienceFxMesh: 'fish' | 'bubbles' | 'brain' | 'clock' |
 *  'blue-sun' | 'plant' | 'ferns' | 'volcano'. Lightning + rain (2026-11-23):
 *  'lightning' (LightningBolt — jagged emissive bolt, flash cycle) and
 *  'rain' (Rainfall — slanted streaks, looped). Robot (2026-11-23,
 *  robot_homework): 'robot' (BlockyRobot — white/blue boxy robot holding
 *  books). Blank screens (2026-11-23, no_internet): 'blank-phone'
 *  (BlankPhone — big blocky phone, dead-black screen) and 'blank-monitor'
 *  (BlankMonitor — desktop monitor, dead-black screen). For those, `scale` sizes the
 *  whole component (default 1); `radius` is ignored. */
export interface ScienceFx {
  id: string;
  shape: 'sphere' | 'box' | 'ring' | 'facet' | 'dome' | 'crescent' | 'fish' | 'bubbles' | 'brain' | 'clock' | 'blue-sun' | 'plant' | 'ferns' | 'volcano' | 'lightning' | 'rain' | 'robot' | 'blank-phone' | 'blank-monitor'; // ring = flat torus (accretion disc); facet = low-poly icosahedron (rocks, ice)
  radius?: number; // sphere / facet
  scale?: number; // ported-asset shapes: uniform scale of the whole component (default 1)
  detail?: number; // facet: icosahedron detail (0 = 20 faces, 1 = 80 faces)
  arc?: number; // ring: torus sweep in radians (default 2PI full ring; PI = upper half-arch, rainbow)
  tube?: number; // ring: tube radius (default radius * 0.16)
  size?: [number, number, number]; // box
  color: string;
  emissive?: string;
  emissiveIntensity?: number;
  roughness?: number;
  opacity?: number;
  /** Fixed rotation [rx, ry, rz] in radians (box and ring; e.g. radial star streaks, rainbow arch upright). */
  rotation?: [number, number, number];
  keyframes: FxKeyframe[];
}

export interface SceneSegment {
  id: string;
  location: LocationId;
  /** Which hero house / family home: 'blue' | 'yellow' | 'red' | 'white' | 'green' (house, living_room, kitchen, bedroom). */
  variant?: HouseVariantId;
  /** Up to 4 chalkboard lines for the classroom. */
  boardText?: string[];
  /** Name on the school sign (school_exterior). */
  schoolName?: string;
  locationLabel?: string;
  skyColor?: string;
  isNight?: boolean;
  /** Blackout: night scene with EVERY electric light off — house windows,
   * street lamps, car headlights, traffic lights, shop/school signs all
   * dark. The sky and scene lighting stay night; only the lit props go
   * dark. Used by no_electricity ("the streets go dark"). Default off. */
  blackout?: boolean;
  /** Animated science props (Moon, water blobs) rendered by the environment. */
  fx?: ScienceFx[];
  startFrame: number;
  endFrame: number;
  cameraShots: CameraShot[];
  characters: Partial<Record<CharacterId, CharacterKeyframe[]>>;
}

export interface RobloxShortStory {
  title: string;
  fps: number;
  durationInFrames: number;
  width: number;
  height: number;
  /** Character constructor: actor id → preset name or { extends?, hair, top, bottom, ... } overrides. */
  cast?: Record<string, CharacterLookInput>;
  scenes: SceneSegment[];
  captions: CaptionCue[];
}
