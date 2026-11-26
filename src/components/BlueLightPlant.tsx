import React from 'react';
import * as THREE from 'three';
import {RBox, useCanvasTexture, type V3} from '../kit/kit';

/**
 * BlueLightPlant.tsx — ported from new-assets/blue-light-plant.
 * Potted plant only: pot + soil + stem + 5 voxel leaves + blue glow.
 * DROPPED (source scene scaffolding): the light-blue pedestal, the mini
 * blocky sun, and the cool-blue light beam.
 * Re-based so the pot bottom sits on y = 0 (engine convention: feet on
 * y = 0). In the source the pot sat on the pedestal, pot group at
 * y = -0.45; here the pot group is at y = 0.55 and the stem group at
 * y = 1.35, preserving every internal offset exactly (+1.0 in Y).
 * The blue glow survives the dropped sun as emissive leaf tips plus a
 * standalone blue pointLight up-right of the plant (the sun's old spot).
 */
export const COLORS = {
  pot: '#8c583e',
  potRim: '#9e674a',
  soil: '#38323e',
  stem: '#25705c',
  stemLight: '#318a74',
  leafDark: '#174e52',
  leafMid: '#247575',
  leafLit: '#42a3ad',
  sunMid: '#72e3ff',
};

const useLeafTexture = () =>
  useCanvasTexture((g, size) => {
    const cell = size / 8;
    for (let x = 0; x < 8; x++) {
      for (let y = 0; y < 8; y++) {
        const v = (x * 5 + y * 9) % 4;
        g.fillStyle = ['#d4f0f2', '#e4f7f8', '#bfe4e8', '#edfbfc'][v];
        g.fillRect(x * cell, y * cell, cell, cell);
      }
    }
    // Central vein & diagonal ribs
    g.strokeStyle = 'rgba(20, 72, 74, 0.35)';
    g.lineWidth = 10;
    g.beginPath(); g.moveTo(size / 2, 0); g.lineTo(size / 2, size); g.stroke();
    g.lineWidth = 6;
    for (let y = 40; y < size; y += 52) {
      g.beginPath(); g.moveTo(size / 2, y); g.lineTo(24, y - 34); g.stroke();
      g.beginPath(); g.moveTo(size / 2, y); g.lineTo(size - 24, y - 34); g.stroke();
    }
  }, 256);

const useLeafBumpTexture = () =>
  useCanvasTexture((g, size) => {
    g.fillStyle = '#808080';
    g.fillRect(0, 0, size, size);
    g.strokeStyle = '#c8c8c8';
    g.lineWidth = 12;
    g.beginPath(); g.moveTo(size / 2, 0); g.lineTo(size / 2, size); g.stroke();
    g.lineWidth = 7;
    for (let y = 40; y < size; y += 52) {
      g.beginPath(); g.moveTo(size / 2, y); g.lineTo(20, y - 34); g.stroke();
      g.beginPath(); g.moveTo(size / 2, y); g.lineTo(size - 20, y - 34); g.stroke();
    }
  }, 256);

const useSoilTexture = () =>
  useCanvasTexture((g, size) => {
    const cell = size / 8;
    for (let x = 0; x < 8; x++) {
      for (let y = 0; y < 8; y++) {
        const v = (x * 7 + y * 11) % 4;
        g.fillStyle = ['#38323e', '#4a4152', '#2b2530', '#54463b'][v];
        g.fillRect(x * cell, y * cell, cell, cell);
      }
    }
  }, 256);

const VoxelLeaf: React.FC<{
  position: V3;
  rotation: V3;
  scale?: number;
  sway: number;
  leafTex: THREE.Texture;
  leafBump: THREE.Texture;
}> = ({position, rotation, scale = 1, sway, leafTex, leafBump}) => (
  <group position={position} rotation={[rotation[0] + sway, rotation[1], rotation[2]]} scale={scale}>
    {/* Angled stem petiole */}
    <RBox size={[0.2, 0.2, 0.36]} color={COLORS.stem} position={[0, -0.05, 0.18]} radius={0.03} />
    {/* Stepped voxel leaf base, wide mid-blade, and tapered tip */}
    <RBox size={[0.62, 0.16, 0.36]} color={COLORS.leafDark} map={leafTex} bumpMap={leafBump} bumpScale={0.04} position={[0, 0.02, 0.5]} radius={0.03} rough={0.55} />
    <RBox size={[1.04, 0.16, 0.54]} color={COLORS.leafMid} map={leafTex} bumpMap={leafBump} bumpScale={0.04} position={[0, 0.04, 0.88]} radius={0.03} rough={0.48} />
    <RBox size={[0.74, 0.14, 0.34]} color={COLORS.leafLit} map={leafTex} bumpMap={leafBump} bumpScale={0.04} position={[0, 0.07, 1.24]} radius={0.03} rough={0.4} emissive={COLORS.leafLit} emissiveIntensity={0.5} />
    <RBox size={[0.38, 0.12, 0.24]} color={COLORS.leafLit} map={leafTex} bumpMap={leafBump} bumpScale={0.04} position={[0, 0.1, 1.46]} radius={0.02} rough={0.35} emissive={COLORS.leafLit} emissiveIntensity={0.5} />
    {/* Raised central midrib ridge */}
    <RBox size={[0.16, 0.08, 0.92]} color={COLORS.stemLight} position={[0, 0.12, 0.88]} radius={0.02} rough={0.5} />
  </group>
);

export const BlueLightPlant: React.FC<{
  t?: number;
  duration?: number;
  position?: V3;
  rotation?: V3;
  scale?: number;
}> = ({t = 0, duration = 3, position = [0, 0, 0], rotation = [0, 0, 0], scale = 1}) => {
  const leafTex = useLeafTexture();
  const leafBump = useLeafBumpTexture();
  const soilTex = useSoilTexture();
  const ph = (t / duration) * Math.PI * 2;
  const sunPulse = 1 + Math.sin(ph) * 0.04;

  return (
    <group position={position} rotation={rotation} scale={scale}>
      {/* Blocky Terracotta Pot & Textured Voxel Soil (re-based: bottom on y = 0) */}
      <group position={[0, 0.55, 0]}>
        <RBox size={[1.65, 1.1, 1.65]} color={COLORS.pot} position={[0, 0, 0]} radius={0.06} rough={0.7} />
        <RBox size={[1.92, 0.34, 1.92]} color={COLORS.potRim} position={[0, 0.62, 0]} radius={0.06} rough={0.68} />
        <RBox size={[1.5, 0.18, 1.5]} color="#ffffff" map={soilTex} position={[0, 0.72, 0]} radius={0.03} rough={0.92} />
      </group>

      {/* Stepped Branching Stem, Sprout Buds & Multi-Tiered Voxel Leaves */}
      <group position={[0, 1.35, 0]}>
        <RBox size={[0.28, 0.75, 0.28]} color={COLORS.stem} position={[0, 0.35, 0]} radius={0.04} />
        <RBox size={[0.24, 0.65, 0.24]} color={COLORS.stemLight} position={[0.06, 0.95, -0.04]} radius={0.04} />
        {/* Lower sprouting buds */}
        <RBox size={[0.26, 0.16, 0.32]} color={COLORS.leafMid} position={[-0.22, 0.36, 0.18]} rotation={[0.2, -0.5, 0]} radius={0.03} />
        <RBox size={[0.26, 0.16, 0.32]} color={COLORS.leafMid} position={[0.22, 0.48, -0.16]} rotation={[-0.2, 0.6, 0]} radius={0.03} />

        {/* 5 Stepped Voxel Leaves */}
        <VoxelLeaf position={[0, 0.65, 0]} rotation={[0.12, 0.6, 0]} scale={0.95} sway={Math.sin(ph) * 0.04} leafTex={leafTex} leafBump={leafBump} />
        <VoxelLeaf position={[0, 0.78, 0]} rotation={[0.15, -1.0, 0]} scale={0.92} sway={Math.sin(ph + 1.2) * 0.04} leafTex={leafTex} leafBump={leafBump} />
        <VoxelLeaf position={[0.06, 1.05, -0.04]} rotation={[0.08, 2.2, 0]} scale={1.0} sway={Math.sin(ph + 2.4) * 0.04} leafTex={leafTex} leafBump={leafBump} />
        <VoxelLeaf position={[0.06, 1.18, -0.04]} rotation={[0.05, -2.5, 0]} scale={0.88} sway={Math.sin(ph + 3.6) * 0.04} leafTex={leafTex} leafBump={leafBump} />
        <VoxelLeaf position={[0.06, 1.28, -0.04]} rotation={[-0.08, 0.15, 0]} scale={0.82} sway={Math.sin(ph + 4.8) * 0.04} leafTex={leafTex} leafBump={leafBump} />
      </group>

      {/* Blue glow (the dropped sun's light, kept as a bare pointLight) */}
      <pointLight position={[1.2, 3.2, -0.8]} color={COLORS.sunMid} intensity={2.2 * sunPulse} distance={8} />
    </group>
  );
};
