import React, { useLayoutEffect, useMemo } from 'react';
import * as THREE from 'three';
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { ThreeCanvas } from '@remotion/three';
import { useThree } from '@react-three/fiber';
import { CharacterId, CharacterKeyframe, MotionBlocksStory, AnimationMode } from './types/schema';
import { R6Character } from './components/R6Character';
import { BoltBoy } from './components/BoltBoy';
import { CasualMan } from './components/CasualMan';
import { WingedBoy } from './components/WingedBoy';
import { ClassicNoob } from './components/ClassicNoob';
import { BlockyTRex } from './components/BlockyTRex';
import { clipPose, ClipName, Pose } from './kit/kit';
import { EnvironmentSwitch } from './environments/Environments';
import { ShortsHUD } from './components/ShortsHUD';
import { CURRENT_STORY } from './story/currentStory';
import { CharacterLook, lookForActor, kitForActor, kitScaleForActor } from './characters/look';
import { evaluateCharacterKeyframes, animStartFrame } from './story/keyframes';
import { CameraState, cameraStateForFrame } from './story/camera';
import { LOCATION_INFO } from './environments/locations';

/**
 * Story `anim` -> kit clip. The story pipeline's AnimationMode is the R6 set;
 * the kit has a clip for most of them. The four with no kit clip (sleep,
 * knocked, panting, sit) fall back to idle - the character stays standing, which
 * is a known gap, not a crash. (R6 'sit' is procedural in R6Character; only
 * the kit characters fall back.) `t` is global frame time in seconds for
 * cyclic clips (walk/idle/dance), so they stay continuous across keyframes;
 * one-shots (wave, jump) use local time since the anim started, so a wave
 * begun mid-story raises the arm from down instead of snapping to its end
 * phase (wave saturates arm-up after 0.5s; jump starts mid-air on global t).
 */
const STORY_ANIM_TO_CLIP: Record<AnimationMode, ClipName> = {
  idle: 'idle',
  sleep: 'idle',
  walk: 'walk',
  sprint: 'sprint',
  jump: 'jump',
  sit: 'idle',
  wave: 'wave',
  point: 'point',
  dance: 'dance',
  knocked: 'idle',
  panting: 'idle',
  celebrate: 'celebrate',
  fly: 'fly',
};

/** Clips that play once from their beginning instead of looping on global time. */
const ONE_SHOT_CLIPS: ReadonlySet<ClipName> = new Set(['wave', 'jump']);

const storyAnimPose = (anim: AnimationMode, frame: number, fps: number, animStart: number): Pose => {
  const clip = STORY_ANIM_TO_CLIP[anim] ?? 'idle';
  // One-shots run on time since the anim started (see animStartFrame in
  // src/story/keyframes.ts); everything else stays on global story time.
  const t = ONE_SHOT_CLIPS.has(clip)
    ? Math.max(0, frame - animStart) / Math.max(1, fps)
    : frame / Math.max(1, fps);
  return clipPose(clip, t);
};

const CameraRig: React.FC<{ cam: CameraState }> = ({ cam }) => {
  const { camera } = useThree();
  const [camX, camY, camZ] = cam.position;
  const [targetX, targetY, targetZ] = cam.target;

  useLayoutEffect(() => {
    camera.position.set(camX, camY, camZ);
    if ('fov' in camera) {
      const persp = camera as THREE.PerspectiveCamera;
      if (persp.fov !== cam.fov) {
        persp.fov = cam.fov;
        persp.updateProjectionMatrix();
      }
    }
    camera.lookAt(targetX, targetY, targetZ);
  }, [camera, camX, camY, camZ, targetX, targetY, targetZ, cam.fov]);

  return null;
};

export const MotionBlocksComposition: React.FC<{
  story?: MotionBlocksStory;
  muted?: boolean;
}> = ({ story = CURRENT_STORY, muted = false }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  if (!story.scenes || story.scenes.length === 0) {
    throw new Error(
      'MotionBlocksComposition: story has no scenes (story.scenes is missing or empty) — a story needs at least one scene with cameraShots and characters.'
    );
  }

  const currentScene =
    story.scenes.find((s) => frame >= s.startFrame && frame < s.endFrame) ||
    story.scenes[story.scenes.length - 1];

  // Shared camera math (src/story/camera.ts) — the 2D HUD uses the same
  // function to project chat bubbles, so the two can never drift apart.
  // Evaluated once per frame here and shared with the HUD.
  const cam = cameraStateForFrame(currentScene.cameraShots, frame);

  // Memoize resolved R6 looks per actor for this story so `look` object
  // identity stays stable across frames (prevents R6Character look re-resolve).
  // lookForActor is pure (id + cast only), so this returns the same values
  // the per-frame calls did, computed once.
  const lookByActor = useMemo(() => {
    const map: Record<string, CharacterLook> = {};
    const ids = new Set<string>(Object.keys(story.cast ?? {}));
    for (const sc of story.scenes) {
      for (const id of Object.keys(sc.characters)) ids.add(id);
    }
    for (const id of ids) {
      if (!kitForActor(id, story.cast)) {
        map[id] = lookForActor(id, story.cast);
      }
    }
    return map;
  }, [story]);

  // Evaluate character keyframes once per frame; shared by 3D actors & 2D HUD.
  const actorEntries = Object.entries(currentScene.characters) as [CharacterId, CharacterKeyframe[]][];
  const actorStates: Partial<Record<CharacterId, CharacterKeyframe>> = {};
  for (const [charId, keyframes] of actorEntries) {
    if (keyframes && keyframes.length > 0) {
      actorStates[charId] = evaluateCharacterKeyframes(keyframes, frame);
    }
  }

  const exterior = LOCATION_INFO[currentScene.location]?.exterior ?? false;
  const overview = currentScene.location === 'town_overview';
  const skyColor = currentScene.skyColor || (currentScene.isNight ? '#090D16' : exterior ? '#38BDF8' : '#1E293B');
  const fogRange: [number, number] = overview ? [140, 360] : exterior ? [55, 190] : [26, 68];

  return (
    <AbsoluteFill style={{ backgroundColor: skyColor }}>
      <ThreeCanvas
        width={width}
        height={height}
        shadows
        camera={{ fov: 46, near: 0.1, far: 500, position: [0, 5, 10] }}
      >
        <color attach="background" args={[skyColor]} />
        <fog attach="fog" args={[skyColor, fogRange[0], fogRange[1]]} />

        {/* Dynamic Camera Rig */}
        <CameraRig cam={cam} />

        {/* Studio-style lighting */}
        <ambientLight
          intensity={currentScene.isNight ? 0.55 : 0.85}
          color={currentScene.isNight ? '#94A3B8' : '#F8FAFC'}
        />
        <hemisphereLight args={['#FFFFFF', '#334155', 0.65]} position={[0, 25, 0]} />
        <directionalLight
          key={overview ? 'sun-overview' : exterior ? 'sun-exterior' : 'sun-interior'}
          position={overview ? [60, 110, 70] : exterior ? [24, 44, 28] : [12, 22, 14]}
          intensity={currentScene.isNight ? 1.1 : 2.1}
          color={currentScene.isNight ? '#CBD5E1' : '#FFFBEB'}
          castShadow
          shadow-mapSize-width={overview ? 2048 : 1024}
          shadow-mapSize-height={overview ? 2048 : 1024}
          shadow-camera-left={overview ? -110 : exterior ? -30 : -18}
          shadow-camera-right={overview ? 110 : exterior ? 30 : 18}
          shadow-camera-top={overview ? 110 : exterior ? 30 : 18}
          shadow-camera-bottom={overview ? -110 : exterior ? -30 : -18}
          shadow-camera-far={overview ? 260 : 120}
          shadow-bias={-0.0004}
        />

        {/* Active 3D location (town anchor or interior set) */}
        <EnvironmentSwitch
          location={currentScene.location}
          isNight={currentScene.isNight}
          blackout={currentScene.blackout}
          variant={currentScene.variant}
          boardText={currentScene.boardText}
          schoolName={currentScene.schoolName}
          fx={currentScene.fx}
        />

        {/* Active R6 & Kit Characters in Scene */}
        {actorEntries.map(([charId, keyframes]) => {
          const state = actorStates[charId];
          if (!state) return null;          // Actors parked off-screen (OFF = [0, -80, 0]) skip 3D rendering
          // and shadow-map passes; their anchored bubbles still render in
          // ShortsHUD, which reads actorStates independently. No story shows
          // an actor at y <= -50 (only the OFF park at -80), and a character
          // lerping up from OFF is below the opaque ground plane until it
          // nears y 0, so nothing visible is ever culled.
          if (state.position[1] <= -50) return null;
            // Kit character (BoltBoy, CasualMan, WingedBoy, ClassicNoob) -
            // rendered by its own component with the canonical look and the
            // V3 clip system, not the R6 rig. The story's `anim` is mapped
            // to a kit clip; `prop` is not supported on kit characters yet
            // (the hero in bolt_boy_first holds none).
            const kitId = kitForActor(charId, story.cast);
            if (kitId) {
              if (kitId === 'trex') {
                return (
                  <BlockyTRex
                    key={charId}
                    t={frame / story.fps}
                    duration={3}
                    position={state.position}
                    rotation={[state.rotationX ?? 0, state.rotationY, state.rotationZ ?? 0]}
                    scale={kitScaleForActor(charId, story.cast)}
                    walk={state.anim === 'walk' || state.anim === 'sprint' ? 1 : 0}
                  />
                );
              }
              const KitComponent =
                kitId === 'boltboy' ? BoltBoy
                : kitId === 'casualman' ? CasualMan
                : kitId === 'wingedboy' ? WingedBoy
                : ClassicNoob;
              return (
                <KitComponent
                  key={charId}
                  position={state.position}
                  rotation={[state.rotationX ?? 0, state.rotationY, state.rotationZ ?? 0]}
                  pose={storyAnimPose(state.anim, frame, story.fps, animStartFrame(keyframes, frame))}
                  expression={state.expression}
                  scale={kitScaleForActor(charId, story.cast)}
                />
              );
            }
            return (
              <R6Character
                key={charId}
                look={lookByActor[charId]}
                position={state.position}
                rotationY={state.rotationY}
                rotationX={state.rotationX}
                rotationZ={state.rotationZ}
                anim={state.anim}
                expression={state.expression}
                prop={state.prop}
              />
            );
        })}
      </ThreeCanvas>

      {/* 2D Shorts Captions, Leaderboard & Chat Bubbles */}
      <ShortsHUD story={story} currentScene={currentScene} cam={cam} actorStates={actorStates} />

      {/* Voice + music + SFX, mixed by scripts/shorts/audio.py via make_short.py */}
      {!muted && <Audio src={staticFile('soundtrack.wav')} />}
    </AbsoluteFill>
  );
};
