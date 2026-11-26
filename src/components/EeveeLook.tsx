import { useEffect, useMemo } from 'react';
import * as THREE from 'three';
import { useFrame, useThree } from '@react-three/fiber';
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/examples/jsm/postprocessing/OutputPass.js';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
import { EEVEE_LOOK } from '../look';

/**
 * Eevee-style look: solid PMREM environment, ACES filmic tone mapping,
 * and a subtle UnrealBloom post pass. Rendered through an EffectComposer
 * that takes over the R3F render loop (useFrame priority 1); the
 * stills + ffmpeg pipeline is untouched — this only changes what each
 * still looks like.
 *
 * Deterministic by construction: the RoomEnvironment is a fixed scene,
 * the bloom pass has no random kernel, and nothing here reads time or
 * Math.random. (three's SSAOPass was deliberately NOT used: its sample
 * kernel is built with Math.random, so stills would differ run to run.)
 */
export const EeveeLook: React.FC<{ enabled: boolean; isNight: boolean }> = ({
  enabled,
  isNight,
}) => {
  const gl = useThree((s) => s.gl);
  const scene = useThree((s) => s.scene);
  const camera = useThree((s) => s.camera);
  const size = useThree((s) => s.size);

  // One PMREM environment texture per WebGL context (the "solid
  // environment": real reflections + ambient response for every
  // meshStandardMaterial in the scene).
  const envTexture = useMemo(() => {
    if (!enabled) return null;
    const pmrem = new THREE.PMREMGenerator(gl);
    const tex = pmrem.fromScene(new RoomEnvironment(gl), 0.04).texture;
    pmrem.dispose();
    return tex;
  }, [enabled, gl]);

  // Environment + tone mapping. Restored on unmount so toggling the look
  // off returns the scene to its exact pre-upgrade state.
  useEffect(() => {
    if (!enabled || !envTexture) return;
    const prevEnv = scene.environment;
    const prevEnvIntensity = scene.environmentIntensity;
    const prevToneMapping = gl.toneMapping;
    const prevExposure = gl.toneMappingExposure;
    scene.environment = envTexture;
    scene.environmentIntensity = isNight
      ? EEVEE_LOOK.envIntensityNight
      : EEVEE_LOOK.envIntensityDay;
    gl.toneMapping = THREE.ACESFilmicToneMapping;
    gl.toneMappingExposure = isNight ? EEVEE_LOOK.exposureNight : EEVEE_LOOK.exposureDay;
    return () => {
      scene.environment = prevEnv;
      scene.environmentIntensity = prevEnvIntensity;
      gl.toneMapping = prevToneMapping;
      gl.toneMappingExposure = prevExposure;
    };
  }, [enabled, envTexture, scene, gl, isNight]);

  // Post chain: scene -> subtle bloom -> tone map + sRGB out. The render
  // target is multisampled (WebGL2 MSAA) so the composer does not lose
  // the antialiasing the default framebuffer had.
  const composer = useMemo(() => {
    if (!enabled) return null;
    const rt = new THREE.WebGLRenderTarget(size.width, size.height, {
      samples: 4,
      type: THREE.HalfFloatType,
    });
    const c = new EffectComposer(gl, rt);
    c.addPass(new RenderPass(scene, camera));
    c.addPass(
      new UnrealBloomPass(
        new THREE.Vector2(size.width / 2, size.height / 2),
        EEVEE_LOOK.bloomStrength,
        EEVEE_LOOK.bloomRadius,
        EEVEE_LOOK.bloomThreshold,
      ),
    );
    c.addPass(new OutputPass());
    return c;
  }, [enabled, gl, scene, camera, size.width, size.height]);

  useEffect(() => {
    if (composer) composer.setSize(size.width, size.height);
  }, [composer, size]);

  useEffect(() => {
    return () => {
      composer?.dispose();
      envTexture?.dispose();
    };
  }, [composer, envTexture]);

  // Take over the render loop when enabled: a positive-priority useFrame
  // disables R3F's automatic render, so each Remotion still goes through
  // the composer instead of straight to the canvas. Priority 0 when off,
  // so the toggle-off path keeps R3F's normal rendering (a priority-1
  // subscription alone would suppress it even with a no-op callback).
  useFrame(
    () => {
      composer?.render();
    },
    enabled ? 1 : 0,
  );

  return null;
};
