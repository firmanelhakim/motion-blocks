import React, { useMemo } from 'react';
import { Box, Cyl, V3 } from './kit';
import { ScienceFx } from '../types/schema';
import { ScienceFxMesh } from './fx';

/**
 * Vertical shaft for "What if you dug a hole through the Earth?" (Gemini
 * tunnel reference): a square well of dark brown stacked blocks, a bright
 * disc of daylight at the top opening, orange lava glow at the bottom floor.
 * Standalone environment (not the town map): fx render inside it directly,
 * in stage space — the same arrangement as SpaceEnvironment / MarsEnvironment.
 *
 * The camera sits INSIDE the shaft: the reference shows both the sky disc
 * above and the lava below in one frame, which no single real camera angle
 * can do at a sane fov — so stories use two shots (look up: sky + boy;
 * look down: lava + boy). Actors float mid-shaft (y 4–14); the falling boy
 * is keyframed downward with the 'jump' anim (arms up).
 * Scenes should set skyColor '#1E293B' (dark rock shadow; the disc is the sky).
 */

const DARK = ['#3B2F2F', '#4A3226', '#2D2118', '#5C4033', '#43302A'];
const HOT = ['#7C2D12', '#9A3412', '#5C3319', '#7C2D12', '#8A3B12'];

interface Course {
  key: number;
  y: number;
  jx: number;
  jx2: number;
  jz: number;
  jz2: number;
  c: string;
}

export const TunnelEnvironment: React.FC<{ fx?: ScienceFx[] }> = ({ fx }) => {
  // Deterministic stacked-block courses: 23 courses of height 2, from
  // y=-12 to y=+34, each course jittered a little so the walls read as
  // irregular blockwork, not one flat wall (as in the reference).
  const courses = useMemo<Course[]>(() => {
    let seed = 20261117;
    const rnd = () => {
      seed = (seed * 16807) % 2147483647;
      return (seed - 1) / 2147483646;
    };
    const out: Course[] = [];
    for (let i = 0; i < 23; i++) {
      const y = -11 + i * 2;
      const pal = y < 0 ? HOT : DARK;
      out.push({
        key: i,
        y,
        jx: (rnd() - 0.5) * 0.7,
        jx2: (rnd() - 0.5) * 0.7,
        jz: (rnd() - 0.5) * 0.7,
        jz2: (rnd() - 0.5) * 0.7,
        c: pal[i % pal.length],
      });
    }
    return out;
  }, []);

  return (
    <group>
      {/* shaft walls: four sides of stacked courses, interior x,z in [-8, 8] */}
      {courses.map((c) => (
        <group key={c.key}>
          <Box p={[c.jx, c.y, -8.75]} s={[17.5, 2, 1.5]} c={c.c} rough={0.95} />
          <Box p={[c.jx2, c.y, 8.75]} s={[17.5, 2, 1.5]} c={c.c} rough={0.95} />
          <Box p={[-8.75, c.y, c.jz]} s={[1.5, 2, 16]} c={c.c} rough={0.95} />
          <Box p={[8.75, c.y, c.jz2]} s={[1.5, 2, 16]} c={c.c} rough={0.95} />
        </group>
      ))}

      {/* bright disc of daylight at the top opening: blue, not blown white */}
      <Cyl p={[0, 34, 0]} rt={5} rb={5} h={0.6} seg={24} c="#93C5FD" e="#60A5FA" ei={1.2} rough={0.4} />

      {/* lava floor: orange, not blown cream — deeper colours, gentler glow */}
      <Box p={[0, -12.5, 0]} s={[17.5, 1, 17.5]} c="#EA580C" e="#F97316" ei={1.2} rough={0.4} />
      <Box p={[0, -11.8, 0]} s={[12, 0.7, 12]} c="#F97316" e="#FB923C" ei={1.5} rough={0.4} />

      {fx?.map((f) => (
        <ScienceFxMesh key={f.id} fx={f} />
      ))}
    </group>
  );
};
