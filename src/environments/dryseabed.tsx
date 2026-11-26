import React from 'react';
import { Box, Facet, crackTex } from './kit';
import { ScienceFx } from '../types/schema';
import { ScienceFxMesh } from './fx';

/**
 * Dry seabed for "What if the oceans dried up?" (Gemini dry-seabed
 * reference): cracked pale earth, a beached wooden boat, and a white whale
 * skeleton. The cracks are a procedural texture (crackTex — a jittered
 * grid of plates plus random-walk cracks) on the floor plane; the boat is
 * stacked plank boxes with a cabin and broken bow posts; the skeleton is a
 * spine of small white boxes with ribs, a skull and a tapering tail.
 * Standalone environment (not the town map): fx render inside it directly,
 * in stage space — the same arrangement as MarsEnvironment.
 *
 * Actors stand on the cracked earth around x in [-6, 6], z in [-3, 4];
 * the boat is behind-right, the skeleton behind-left. Scenes should set
 * skyColor '#FDE68A' (pale hazy sky, like the reference).
 */
export const DrySeabedEnvironment: React.FC<{ fx?: ScienceFx[] }> = ({ fx }) => {
  const earth = crackTex('#E8DCC0', '#6B4A2A', 6, 6);
  return (
    <group>
      {/* cracked pale earth baseplate */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[260, 260]} />
        <meshStandardMaterial map={earth} roughness={0.95} />
      </mesh>

      {/* beached wooden boat, listing slightly, behind-right */}
      <group position={[6, 0, -5]} rotation={[0, -0.35, 0.1]}>
        {/* hull: stacked tiers, wider as they rise */}
        <Box p={[0, 0.6, 0]} s={[7, 1.2, 2.6]} c="#92400E" rough={0.9} />
        <Box p={[0, 1.8, 0]} s={[8, 1.2, 3.0]} c="#B45309" rough={0.9} />
        <Box p={[0, 3.0, 0]} s={[9, 1.0, 3.4]} c="#92400E" rough={0.9} />
        {/* broken bow/stern posts sticking up past the gunwale */}
        <Box p={[-4.3, 4.2, 0]} s={[0.5, 2.4, 0.5]} r={[0, 0, 0.28]} c="#78350F" rough={0.9} />
        <Box p={[4.3, 4.2, 0]} s={[0.5, 2.4, 0.5]} r={[0, 0, -0.28]} c="#78350F" rough={0.9} />
        {/* cabin with roof and dark windows */}
        <Box p={[-0.6, 4.1, 0]} s={[3.2, 2.2, 2.6]} c="#78350F" rough={0.9} />
        <Box p={[-0.6, 5.4, 0]} s={[3.8, 0.4, 3.0]} c="#92400E" rough={0.9} />
        <Box p={[-0.6, 4.3, 1.32]} s={[1.0, 1.0, 0.08]} c="#1F2937" rough={0.4} />
        <Box p={[-0.6, 4.3, -1.32]} s={[1.0, 1.0, 0.08]} c="#1F2937" rough={0.4} />
        {/* a broken plank leaning on the hull */}
        <Box p={[2.6, 1.6, 1.9]} s={[0.5, 3.2, 0.2]} r={[0.35, 0, -0.3]} c="#B45309" rough={0.9} />
      </group>

      {/* white whale skeleton, behind-left */}
      <group position={[-8, 0, -3]} rotation={[0, 0.4, 0]}>
        {/* spine: a row of small vertebra boxes */}
        {[-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5].map((x, i) => (
          <Box key={i} p={[x, 0.8, 0]} s={[0.9, 0.5, 0.5]} c="#F8FAFC" rough={0.6} />
        ))}
        {/* ribs hanging below the spine */}
        {[-2.5, -1.5, -0.5, 0.5, 1.5, 2.5].map((x, i) => (
          <Box key={i} p={[x, 0.35, 0.55]} s={[0.25, 1.4, 0.25]} r={[0.2, 0, 0]} c="#F8FAFC" rough={0.6} />
        ))}
        {/* skull + jaw */}
        <Box p={[-4.6, 0.6, 0]} s={[1.6, 1.0, 1.2]} c="#F8FAFC" rough={0.6} />
        <Box p={[-4.5, 0.15, 0]} s={[1.4, 0.3, 0.8]} c="#E2E8F0" rough={0.6} />
        {/* tapering tail bones */}
        <Box p={[4.2, 0.7, 0]} s={[0.7, 0.4, 0.4]} c="#F8FAFC" rough={0.6} />
        <Box p={[4.8, 0.6, 0]} s={[0.5, 0.3, 0.3]} c="#F8FAFC" rough={0.6} />
      </group>

      {/* a few dry rocks at the edges */}
      <Facet p={[-13, 0.4, 4]} rad={1.0} detail={0} c="#A8A29E" r={[0.3, 0.8, 0.1]} rough={0.95} />
      <Facet p={[13, 0.3, 6]} rad={0.8} detail={0} c="#78716C" r={[0.2, 0.4, 0.9]} rough={0.95} />
      <Facet p={[-2, 0.25, -11]} rad={0.6} detail={0} c="#A8A29E" r={[0.9, 0.2, 0.4]} rough={0.95} />

      {fx?.map((f) => (
        <ScienceFxMesh key={f.id} fx={f} />
      ))}
    </group>
  );
};
