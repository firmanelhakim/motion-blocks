import React, { useMemo } from 'react';
import * as THREE from 'three';
import { Ball, Box, studTex, V3 } from '../kit';
import { House, HouseVariant, Playground, School, Shop } from './buildings';
import { BlockTree, BusStop, Car, Hydrant, PineTree, RoundTree, StreetLamp, StreetSign, TrafficLight, TrashCan, StopSign } from './props';
import { ScienceFx } from '../../types/schema';
import { ScienceFxMesh } from '../fx';

/**
 * ONE persistent town. Every exterior location is the same map seen from a different
 * "anchor": the map is shifted/rotated so the anchor's stage spot sits at the local
 * origin (0,0,0) and the camera side of the stage is local +Z. Characters and cameras
 * are therefore always authored in the same comfortable local frame
 * (actors around x∈[-6,6], z∈[-3,4]; camera at z≈11–17 looking toward −Z).
 *
 *   World layout (top view, +X east, +Z south):
 *
 *        yellow house   blue house   |   |        SCHOOL (+yard)
 *        (-44,-21)      (-22,-21)    | M |        (36,-34)
 *   ============ MAIN STREET ========+ a +===================================
 *        shop           playground   | p |  red house   white house   green house
 *        (-50,16)       (-22,24)     | l |  (20,21)     (44,21)       (72,21)
 *                                    | e |
 */

export type ExteriorLocation =
  | 'town_overview'
  | 'street'
  | 'crossroads'
  | 'school_exterior'
  | 'house'
  | 'shop'
  | 'playground';

interface Anchor {
  p: V3; // world position of the stage center
  yaw: number; // direction (radians) of the camera side; local +Z points there
}

export const HOUSE_POSITIONS: Record<HouseVariant, { x: number; side: 'north' | 'south' }> = {
  yellow: { x: -44, side: 'north' },
  blue: { x: -22, side: 'north' },
  red: { x: 20, side: 'south' },
  white: { x: 44, side: 'south' },
  green: { x: 72, side: 'south' },
};

export function anchorFor(location: ExteriorLocation, variant: HouseVariant = 'blue'): Anchor {
  switch (location) {
    case 'town_overview':
      return { p: [8, 0, 0], yaw: 0 };
    case 'street':
      return { p: [-12, 0.2, -7], yaw: 0 };
    case 'crossroads':
      return { p: [0, 0, -6], yaw: 0 };
    case 'school_exterior':
      return { p: [36, 0, -14], yaw: 0 };
    case 'shop':
      return { p: [-50, 0.2, 7], yaw: Math.PI };
    case 'playground':
      return { p: [-22, 0, 24], yaw: Math.PI };
    case 'house': {
      const h = HOUSE_POSITIONS[variant];
      return h.side === 'north' ? { p: [h.x, 0, -13], yaw: 0 } : { p: [h.x, 0, 13], yaw: Math.PI };
    }
  }
}

// ---------------------------------------------------------------------------
// Roads & sidewalks
// ---------------------------------------------------------------------------

const ROAD_HALF = 5;
const WALK = 4; // sidewalk width
const WALK_H = 0.2;
const EXTENT = 130;

const Roads: React.FC = React.memo(() => {
  // Stud contrast softened 2026-11-21: the darker stud lines shimmered
  // (texture aliasing) on the road/sidewalk during fast tracking shots.
  const road = studTex('#334155', '#2B3648', 60, 3);
  const roadV = studTex('#334155', '#2B3648', 3, 60);
  const walkMap = studTex('#CBD5E1', '#B6C2D2', 30, 2);
  const walkMapV = studTex('#CBD5E1', '#B6C2D2', 2, 30);
  const len = EXTENT - ROAD_HALF;
  const mid = ROAD_HALF + len / 2;
  return (
    <group>
      {/* asphalt */}
      <mesh position={[0, 0.02, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[EXTENT * 2, ROAD_HALF * 2]} />
        <meshStandardMaterial map={road} roughness={0.85} />
      </mesh>
      {/* Maple Ave (vertical road). y=0.04, not 0.021: the two asphalt planes
          were only 0.001 apart at the intersection and z-fought. 0.04 sits
          clear of Main St (0.02) and below the lane dashes (bottom 0.03). */}
      <mesh position={[0, 0.04, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[ROAD_HALF * 2, EXTENT * 2]} />
        <meshStandardMaterial map={roadV} roughness={0.85} />
      </mesh>
      {/* sidewalks: 4 along Main, 4 along Maple, 4 corner squares */}
      {[-1, 1].flatMap((sx) =>
        [-1, 1].map((sz) => (
          <React.Fragment key={`${sx}${sz}`}>
            <Box p={[sx * (mid + WALK / 2), WALK_H / 2, sz * (ROAD_HALF + WALK / 2)]} s={[len - WALK, WALK_H, WALK]} map={walkMap} />
            <Box p={[sx * (ROAD_HALF + WALK / 2), WALK_H / 2, sz * (mid + WALK / 2)]} s={[WALK, WALK_H, len - WALK]} map={walkMapV} />
            <Box p={[sx * (ROAD_HALF + WALK / 2), WALK_H / 2, sz * (ROAD_HALF + WALK / 2)]} s={[WALK, WALK_H, WALK]} c="#CBD5E1" />
            {/* curbs */}
            <Box p={[sx * (mid + WALK / 2), WALK_H / 2 + 0.01, sz * (ROAD_HALF + 0.12)]} s={[len - WALK, WALK_H + 0.02, 0.25]} c="#94A3B8" />
            <Box p={[sx * (ROAD_HALF + 0.12), WALK_H / 2 + 0.01, sz * (mid + WALK / 2)]} s={[0.25, WALK_H + 0.02, len - WALK]} c="#94A3B8" />
          </React.Fragment>
        ))
      )}
      {/* lane dashes */}
      {Array.from({ length: 30 }, (_, i) => -EXTENT + 6 + i * 8.5)
        .filter((v) => Math.abs(v) > 12)
        .map((v) => (
          <React.Fragment key={v}>
            <Box p={[v, 0.04, 0]} s={[3.6, 0.02, 0.35]} c="#FACC15" receive={false} />
            <Box p={[0, 0.04, v]} s={[0.35, 0.02, 3.6]} c="#FACC15" receive={false} />
          </React.Fragment>
        ))}
      {/* zebra crosswalks on all 4 sides of the intersection */}
      {[-1, 1].map((s) =>
        Array.from({ length: 6 }, (_, i) => -4.2 + i * 1.7).map((o) => (
          <React.Fragment key={`${s}:${o}`}>
            <Box p={[o, 0.04, s * 7]} s={[0.9, 0.02, 3.2]} c="#F8FAFC" receive={false} />
            <Box p={[s * 7, 0.04, o]} s={[3.2, 0.02, 0.9]} c="#F8FAFC" receive={false} />
          </React.Fragment>
        ))
      )}
    </group>
  );
});

// ---------------------------------------------------------------------------
// The full map
// ---------------------------------------------------------------------------

export const TownMap: React.FC<{ night?: boolean; blackout?: boolean; t?: number; schoolName?: string }> = React.memo(({ night = false, blackout = false, t, schoolName }) => {
  // Blackout: night sky/lighting stay, but every electric light in the
  // town goes dark (windows, lamps, headlights, traffic lights, signs).
  // `lit` is what the lit props see; the sky stays night via `night`.
  const lit = night && !blackout;
  const grass = studTex('#4ADE80', '#22C55E', 120, 120);

  // north side avoids houses at x −44/−22 and the school entrance (36); south avoids shop −50, park −22, houses 20/44/72
  const lampsNorth = [-62, -33, 15, 26, 50, 64, 80];
  const lampsSouth = [-64, -36, -9, 12, 32, 58, 86];
  const lampsZ = [-40, -24, 24, 40];
  const backTreesN = useMemo(() => Array.from({ length: 16 }, (_, i) => -80 + i * 11), []);

  return (
    <group>
      {/* grass baseplate */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[EXTENT * 2.4, EXTENT * 2.4]} />
        <meshStandardMaterial map={grass} roughness={0.85} />
      </mesh>
      <Roads />

      {/* ---- NW block: hero houses facing Main St (+Z) ---- */}
      {(['yellow', 'blue'] as HouseVariant[]).map((v) => (
        <group key={v} position={[HOUSE_POSITIONS[v].x, 0, -21]}>
          <House variant={v} night={lit} />
        </group>
      ))}
      <BusStop p={[-33, WALK_H, -8.2]} />

      {/* ---- NE block: school ---- */}
      <group position={[36, 0, -34]}>
        <School night={lit} t={t} name={schoolName} />
      </group>

      {/* ---- SE block: hero houses facing Main St (−Z) ---- */}
      {(['red', 'white', 'green'] as HouseVariant[]).map((v) => (
        <group key={v} position={[HOUSE_POSITIONS[v].x, 0, 21]} rotation={[0, Math.PI, 0]}>
          <House variant={v} night={lit} />
        </group>
      ))}

      {/* ---- SW block: shop + playground ---- */}
      <group position={[-50, 0, 16]} rotation={[0, Math.PI, 0]}>
        <Shop night={lit} />
      </group>
      <group position={[-22, 0, 24]} rotation={[0, Math.PI, 0]}>
        <Playground t={t} />
      </group>

      {/* ---- intersection furniture ---- */}
      <TrafficLight p={[7.6, WALK_H, -7.6]} r={[0, -Math.PI / 2, 0]} lit={blackout ? "off" : "green"} arm={5} />
      <TrafficLight p={[-7.6, WALK_H, 7.6]} r={[0, Math.PI / 2, 0]} lit={blackout ? "off" : "green"} arm={5} />
      <TrafficLight p={[-7.6, WALK_H, -7.6]} r={[0, 0, 0]} lit={blackout ? "off" : "red"} arm={5} />
      <TrafficLight p={[7.6, WALK_H, 7.6]} r={[0, Math.PI, 0]} lit={blackout ? "off" : "red"} arm={5} />
      <StreetSign p={[8.3, WALK_H, -8.3]} a="MAIN ST" b="MAPLE AVE" />
      <StopSign p={[-8.3, WALK_H, 30]} r={[0, -Math.PI / 2, 0]} />

      {/* ---- street lamps ---- */}
      {lampsNorth.map((x) => (
        <StreetLamp key={`ln${x}`} p={[x, WALK_H, -8.4]} night={lit} />
      ))}
      {lampsSouth.map((x) => (
        <StreetLamp key={`ls${x}`} p={[x, WALK_H, 8.4]} r={[0, Math.PI, 0]} night={lit} />
      ))}
      {lampsZ.map((z) => (
        <React.Fragment key={`lz${z}`}>
          <StreetLamp p={[-8.4, WALK_H, z]} r={[0, Math.PI / 2, 0]} night={lit} />
          <StreetLamp p={[8.4, WALK_H, z + 8]} r={[0, -Math.PI / 2, 0]} night={lit} />
        </React.Fragment>
      ))}

      {/* ---- sidewalk clutter ---- */}
      <Hydrant p={[-4 - 14, WALK_H, -6.2]} />
      <Hydrant p={[30, WALK_H, 6.2]} />
      <TrashCan p={[-7, WALK_H, -12]} />
      <TrashCan p={[12, WALK_H, 7]} c="#1D4ED8" />

      {/* ---- traffic far from the stages ---- */}
      <Car p={[-92, 0, -2.6]} r={[0, Math.PI / 2, 0]} c="#7C3AED" night={lit} />
      <Car p={[100, 0, 2.6]} r={[0, -Math.PI / 2, 0]} c="#F59E0B" night={lit} />
      <Car p={[2.6, 0, -58]} c="#0EA5E9" night={lit} />
      <Car p={[-2.6, 0, 66]} r={[0, Math.PI, 0]} c="#16A34A" night={lit} />

      {/* ---- trees filling the blocks + skyline ---- */}
      {backTreesN.map((x, i) =>
        Math.abs(x) < 10 ? null : i % 3 === 0 ? (
          <PineTree key={`n${x}`} p={[x, 0, -48 - (i % 2) * 5]} scale={1.3} />
        ) : (
          <RoundTree key={`n${x}`} p={[x, 0, -50 - (i % 2) * 4]} scale={1.2} />
        )
      )}
      {backTreesN.map((x, i) =>
        Math.abs(x) < 10 ? null : (
          <BlockTree key={`s${x}`} p={[x + 4, 0, 44 + (i % 2) * 5]} scale={1.1} leaf={i % 2 ? '#16A34A' : '#15803D'} />
        )
      )}
      {[-1, 1].map((s) => (
        <React.Fragment key={`side${s}`}>
          <RoundTree p={[s * 14, 0, -18]} />
          <RoundTree p={[-58, 0, s * -30]} scale={1.2} />
        </React.Fragment>
      ))}
      {/* rolling hills on the horizon */}
      {[
        [-110, -120, 40],
        [-30, -140, 55],
        [70, -130, 45],
        [150, -100, 50],
        [-150, 60, 50],
        [120, 120, 45],
        [0, 150, 60],
      ].map(([x, z, r], i) => (
        <Ball key={i} p={[x, -r * 0.55, z]} rad={r} c={i % 2 ? '#22C55E' : '#16A34A'} rough={0.9} />
      ))}
    </group>
  );
});

/** Renders the whole town shifted so the requested anchor is the local origin. */
export const TownExterior: React.FC<{
  location: ExteriorLocation;
  variant?: HouseVariant;
  night?: boolean;
  blackout?: boolean;
  schoolName?: string;
  fx?: ScienceFx[];
}> = React.memo(({ location, variant = 'blue', night = false, blackout = false, schoolName, fx }) => {
  const { rot, pos } = useMemo(() => {
    const a = anchorFor(location, variant);
    const q = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), -a.yaw);
    const p = new THREE.Vector3(...a.p).applyQuaternion(q).multiplyScalar(-1);
    return { rot: -a.yaw, pos: [p.x, p.y, p.z] as V3 };
  }, [location, variant]);

  // fx positions are authored in STAGE space (same as characters/cameras).
  // They must sit OUTSIDE the translated group: the group's local space is
  // world space, so children of it would land far from the stage.
  return (
    <>
      {fx?.map((f) => (
        <ScienceFxMesh key={f.id} fx={f} />
      ))}
      <group rotation={[0, rot, 0]} position={pos}>
        <TownMap night={night} blackout={blackout} schoolName={schoolName} />
      </group>
    </>
  );
});
