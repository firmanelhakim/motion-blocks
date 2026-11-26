"""DINOSAURS — "What If Dinosaurs Were Still Alive?" (FIX ROUND 1)

Science explainer, lead: hero kid_boy. A T. rex walks down Main Street
and the town has to live with dinosaurs: the kid hides behind a tree,
then watches the great animal sniff the air and move on. The teacher
explains why they are gone — 66 million years ago a rock about 10 km
wide hit the Earth, threw up dust that blocked the Sun for months, the
plants died, and the big dinosaurs starved. But they never fully left:
small feathered dinosaurs survived and became birds.

The one science idea: an asteroid blocked the Sun and ended the
dinosaurs, but birds are their living descendants.

FIX ROUND 1 changes (vs v1):
- NEW OPENING b0: the narration now STARTS with the title question,
  "What if dinosaurs were still alive?", over a wide establishing hook
  shot (hero in the foreground looking at the camera, the rex walking
  Main Street behind him). The "In this town," setup follows as b1.
  New TTS, all timings shift — full re-render, not partial.
- Hide/peek: the kid no longer hides directly behind the Dare tree —
  from every front camera his head sat inside the canopy balls' disc
  (main ball centre [2.5, 5.8, -2.5] r 2.6; side ball [3.9, 5.0, -1.9]
  r 1.7), and his hide->peek walk passed under the canopy. He now
  hides/peeks at x 8.5, clear of the canopy from the wide, the rex
  tracking shot and the peek close-up; the walk runs straight up +z
  at x 8.5 and never goes under the canopy. The rex shot in the hide
  scene is a wide two-shot (rex left, kid right, fov 64) so the peek
  is actually visible — the tight low_angle put the kid out of frame.
- Asteroid: the head was r 2.0 against an r 3.0 Earth and read ~3x
  Earth. It is now r 0.5 — a bright speck with a thin tail.
- Impact: the flash was a pale r 2.0 white blob; it is now a small
  hot orange fireball (r 1.0 in the b9 scene, r 1.5 + shock ring in
  the BOOM! scene). The volcano (scale 2.5, centre frame, smoke
  cubes floating mid-frame) is now scale 1.2, off-centre at [7, 0,
  -13], so it reads as a distant backdrop and its smoke wisp stays
  low over its own crater.
- Shouts: v1 put BOOM! / DARK! / GONE! all inside one hero close-up
  (the 3rd split shot covered all three shouts). The impact is now
  FOUR scenes, one visual per shout: b9 impact (flash), BOOM!
  (bigger flash + shock ring), DARK! (dust blanket + black gloom
  veil over a dimmed Earth, no flash), GONE! (dim Earth, thin
  scattered dust, wide empty framing). The GONE! scene runs through
  b10 ("But the dinosaurs never fully left") over the aftermath,
  and the street payoff starts at b11.
- Classroom: the teacher was hidden behind the kid from the wide
  camera. Teacher moved right to [-2.0, 0, -5.0] (still beside the
  desk, whose right edge is x -3), hero moved right to [1.5, 0, 1.5],
  so the sight line to the teacher clears the hero.
- Ferns: moved out to [+-12.5, 0, -5] and shrunk to scale 1.2, so
  no frond reaches the kid's head at the peek spot.
- Payoff: the kid now actually looks up — he leans back (rx -0.35)
  into a point at b13 and waves leaning back at the end, and the
  final shots are low_angle (sky behind his head, not the street
  tree line that made the green canopy halo in v1). The hero stands
  at x -8 (not 0): the street tree at stage (-2, -11) sat directly
  behind his head from every front camera at x 0; at x -8 the canopy
  clears his head in the wide and the low shots put sky behind him.

Cast: hero kid_boy (one look, whole video), teacher (classroom), and
the T. rex {"kit": "trex", "scale": 1.8} — walk + idle only, no V3
pose port. NO second dinosaur (plan: do not build one until the T. rex
reads in stills). No bird model exists: the kid looks up and points,
and the narration names the bird.

T. REX FACING — read before touching the rotation values: the component
faces -x at rotationY 0 (inner yaw -90 deg, snout at local +z), so the
scene.py face() value aims it 90 deg off. rex_face() below is
face(src, dst) + HALF, which is the rotationY that actually points the
snout at dst. Verified against BlockyTRex.tsx by hand — CHECK IN
STILLS: if the rex walks sideways, this is the line to fix.

Staging notes (checked against the environment code, not just by eye):
- Street walk (scene 1): rex at z=-2, clear of the hydrant (local
  [-6, 0, 0.8]) and the blue-house front wall (local z=-9).
- Playground (scene 2): the kid hides/peeks at x 8.5 — clear of the
  Dare tree canopy from every camera in the scene (see above). The
  rex walks the front of the playground at z=7, [-8, 0, 7] -> [6, 0, 7],
  ending facing +x so its ~7-stud tail trails along -x and never pokes
  through the front fence (z=9.5) or the RoundTree at [12, 0, 5].
- The asteroid reuses the comet_hits.py pattern, recolored orange
  (rock, not ice), diving at the flash point of the impact scene —
  now a r 0.5 speck, not a rival planet.
- The volcano stands on the space floor as a distant backdrop in the
  impact scenes, per the plan — scale 1.2 at [7, 0, -13], top (y ~4.3)
  well below the Earth globe (bottom y ~11), off-centre so it never
  dominates the frame.

Build (coordinator runs the previews serially — do NOT run here):
    python scripts/make_short.py stories/dinosaurs.py --stills
"""
import math  # noqa: F401

from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, orbit, shot, split_shots, static_shot, wide  # noqa: F401

TITLE = "DINOSAURS ARE STILL ALIVE"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b0", "text": "What if dinosaurs were still alive?", "pause": 0.10},
    {"id": "b1", "text": "In this town, dinosaurs are still alive.", "pause": 0.08},
    {"id": "b2", "text": "A T. rex walks down Main Street, right past the shops.", "pause": 0.08},
    {"id": "b3", "text": "The kid hides behind a tree, holding his breath.", "pause": 0.08},
    {"id": "b4", "text": "Then he peeks out. Huge head, tiny arms, and a tail that sways as it walks.", "pause": 0.08},
    {"id": "b5", "text": "The great animal sniffs the air... and moves on.", "pause": 0.10},
    {"id": "b6", "text": "The teacher says they were here first, a very, very long time ago.", "pause": 0.08},
    {"id": "b7", "text": "About 66 million years ago, a rock about 10 kilometres wide fell from space.", "pause": 0.10},
    {"id": "b8", "text": "It hit the Earth, and threw up dust that blocked the Sun for months.", "pause": 0.10},
    {"id": "b9", "text": "No sunlight, no plants. No plants, no food. And the big dinosaurs starved.", "pause": 0.10},
    {"id": "w1", "text": "BOOM!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "DARK!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "GONE!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b10", "text": "But the dinosaurs never fully left.", "pause": 0.08},
    {"id": "b11", "text": "Small feathered dinosaurs survived.", "pause": 0.08},
    {"id": "b12", "text": "And over millions of years, they changed into birds.", "pause": 0.10},
    {"id": "b13", "text": "So the next time a bird flies past your window, look up. You are looking at a living dinosaur.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05,
         "dropouts": [("b9+0.3", "w3.end")]}
SFX = [
    ("b0", "whoosh"),
    ("b0+0.3", "thud"),
    ("b1", "whoosh"),
    ("b2+0.5", "thud"),
    ("b3+0.3", "pop", {"f": 500}),
    ("b4+0.5", "sparkle"),
    ("b5+0.3", "swish"),
    ("b6", "ding_dong"),
    ("b7", "whoosh"),
    ("b8+0.5", "bell_low"),
    ("b9+0.3", "riser", {"dur": 1.6}),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b10+0.3", "sparkle"),
    ("b11+0.5", "reveal"),
    ("b12+0.5", "pop", {"f": 800}),
    ("b13+1.5", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
CAST = {
    # Hero: one look for the whole video — black spiky hair, green hoodie.
    "hero": {"extends": "kid_boy", "hair": {"style": "spikyAnime", "color": "black"},
             "top": {"style": "hoodie", "color": "green", "secondary": "white"},
             "bottom": {"style": "jeans", "color": "denim"},
             "shoes": {"color": "white", "sole": "white"}, "freckles": True},
    # Teacher in the standard white blouse (comet_hits pattern), standing
    # BESIDE the desk at x -2.0 (desk right edge is x -3), not on it.
    "teacher": {"extends": "teacher_woman", "skin": "fair", "hair": {"style": "bun", "color": "blonde"}},
    # The T. rex: kit character, walk + idle only. Scale 1.8 so it reads
    # HUGE against the ~5.9-stud kid (about 9 studs tall, head ~7.9 up).
    # Spacing need vs the kid: 4.5 x (1.8 + 1) / 2 = 6.3 studs — the kid
    # is never closer than ~7 studs from it in any scene.
    "rex": {"kit": "trex", "scale": 1.8},
}


def _asteroid(a, b):
    """The 10 km rock, diving at the Earth: the comet_hits.py pattern
    (faceted head + tail of thin streaks), recolored orange for rock
    instead of ice. It streaks from high left to the impact flash
    point [2, 13.5, -10], which the impact scene reuses. FIX ROUND 1:
    the head is a r 0.5 speck with a short thin tail — a 10 km rock
    against the r 3.0 Earth, not a rival planet (v1's r 2.0 head read
    ~3x Earth)."""
    head_kf = [{"frame": a, "position": [-25, 20, -20]}, {"frame": b, "position": [2, 13.5, -10]}]
    fx = [{"id": "asteroid-head", "shape": "facet", "radius": 0.5, "detail": 1, "color": "#FDBA74",
           "emissive": "#EA580C", "emissiveIntensity": 2.0, "roughness": 0.3,
           "keyframes": head_kf}]
    axis = math.pi / 2 + 0.12  # streak long axis ~horizontal, sloping down-left
    for i in range(14):
        d = 0.9 + i * 0.5                 # distance behind the head
        lat = -0.06 - i * 0.06            # tail slopes down as it trails back
        lane = ((i % 3) - 1) * 0.22       # three parallel lanes across the tail
        length = 2.6 + (i % 3) * 0.7
        op = max(0.25, 0.95 - i * 0.06)
        col = "#FED7AA" if i < 5 else "#FDBA74"
        em = "#FB923C" if i < 5 else "#F97316"
        fx.append({"id": f"asteroid-streak{i}", "shape": "box", "size": [0.12, length, 0.12],
                   "color": col, "emissive": em, "emissiveIntensity": 1.4,
                   "roughness": 0.4, "rotation": [0, 0, axis + ((i % 3) - 1) * 0.04],
                   "opacity": op,
                   "keyframes": [{"frame": k["frame"],
                                 "position": [k["position"][0] - d, k["position"][1] + lat + lane, k["position"][2]]}
                                for k in head_kf]})
    return fx


def _earth(a, b, color="#38BDF8", emissive="#1D4ED8", ei=0.4,
           cont_color="#22C55E", cont_emissive="#16A34A", cont_ei=0.25):
    """The Earth globe + green continents, static. Colours dim per scene
    (bright for the impact, dark for DARK! / GONE!)."""
    fx = [{"id": "earth", "shape": "sphere", "radius": 3.0, "color": color,
           "emissive": emissive, "emissiveIntensity": ei, "roughness": 0.7,
           "keyframes": [{"frame": a, "position": [0, 14, -12]}, {"frame": b, "position": [0, 14, -12]}]}]
    for i, (ox, oy, oz, r) in enumerate([
            (1.0, 0.7, 1.9, 1.2), (-1.2, 1.0, 1.7, 1.0), (0.2, -1.0, 2.1, 1.3),
            (-0.5, 1.7, 1.4, 0.9)]):
        fx.append({"id": f"continent{i}", "shape": "sphere", "radius": r, "color": cont_color,
                   "emissive": cont_emissive, "emissiveIntensity": cont_ei, "roughness": 0.8,
                   "keyframes": [{"frame": a, "position": [ox, 14 + oy, -12 + oz]},
                                {"frame": b, "position": [ox, 14 + oy, -12 + oz]}]})
    return fx


def _volcano(a, b, scale=1.2, pos=None):
    """Volcano as a distant backdrop on the dark space floor. FIX ROUND 1:
    scale 1.2 (was 2.5) and off-centre, so it never dominates the frame
    and its grey smoke wisp stays low over its own crater instead of
    floating mid-frame as stray grey cubes."""
    pos = pos if pos is not None else [7, 0, -13]
    return [{"id": "volcano", "shape": "volcano", "scale": scale, "color": "#6B4226",
             "keyframes": [{"frame": a, "position": pos},
                           {"frame": b, "position": pos}]}]


def _flash(a, b, radius, pos=None):
    """The impact fireball: small and HOT (orange core, not a big pale
    white blob — v1's r 2.0 white sphere covered a third of the Earth).
    FIX ROUND 2: the base colour itself is now deep orange (#EA580C,
    not pale #FDBA74) with a hotter emissive — round 1's pale base
    washed out to cream #F7DAA5 under the strong lighting.
    TEST-STILL CORRECTION 2 (2026-11-23): ei 2.0 with the LIGHT
    emissive #FB923C still rendered pale yellow — the emissive colour
    itself is the problem, not the intensity (the shock ring, colour
    #FB923C + emissive #EA580C at ei 2.0, renders a true orange).
    Swapped to match the ring: light base + DEEP orange emissive."""
    pos = pos if pos is not None else [1.5, 13.5, -9.4]
    return [{"id": "flash", "shape": "sphere", "radius": radius, "color": "#FB923C",
             "emissive": "#EA580C", "emissiveIntensity": 2.0, "roughness": 0.3,
             "opacity": 0.95,
             "keyframes": [{"frame": a, "position": pos}, {"frame": b, "position": pos}]}]


def _dust(a, b, specs):
    """Grey dust clouds: (dx, dy, dz, r, opacity) relative to the Earth
    centre [0, 14, -12]."""
    fx = []
    for i, (dx, dy, dz, r, op) in enumerate(specs):
        fx.append({"id": f"dust{i}", "shape": "sphere", "radius": r, "color": "#78716C",
                   "emissive": "#57534E", "emissiveIntensity": 0.3, "roughness": 0.9,
                   "opacity": op,
                   "keyframes": [{"frame": a, "position": [dx, 14 + dy, -12 + dz]},
                                {"frame": b, "position": [dx, 14 + dy, -12 + dz]}]})
    return fx


def _impact(a, b):
    """The extinction seen from space (comet_hits.py pattern): the Earth
    globe, a small hot impact flash on its front face, and grey dust
    clouds starting to spread. FIX ROUND 2: the volcano backdrop is
    REMOVED from all four space scenes — its grey smoke cubes were the
    floating-cube defect (f1015) and its body kept entering the frame
    corner; the raised/tilted cameras below keep the floor out on
    their own. This is the b9 beat; the BOOM! peak lives in _boom."""
    fx = _earth(a, b)
    fx += _flash(a, b, 1.0)
    fx += _dust(a, b, [(-4.5, 1.5, 0.5, 1.2, 0.6), (4.5, 2.0, -0.5, 1.3, 0.6),
                       (-2.5, -2.5, 1.0, 1.0, 0.6), (3.0, -2.0, 0.8, 1.1, 0.6)])
    return fx


def _boom(a, b):
    """BOOM! — the flash at its peak: bigger, hotter fireball + a bright
    shock ring around the impact point, dust still at the edges."""
    fx = _earth(a, b)
    fx += _flash(a, b, 1.5)
    fx.append({"id": "shock", "shape": "ring", "radius": 2.2, "tube": 0.3,
               "color": "#FB923C", "emissive": "#EA580C", "emissiveIntensity": 2.0,
               "roughness": 0.5,
               "keyframes": [{"frame": a, "position": [1.5, 13.5, -9.3]},
                             {"frame": b, "position": [1.5, 13.5, -9.3]}]})
    fx += _dust(a, b, [(-4.5, 1.5, 0.5, 1.2, 0.6), (4.5, 2.0, -0.5, 1.3, 0.6),
                       (0.5, 3.5, -0.5, 1.0, 0.6)])
    return fx


def _dark(a, b):
    """DARK! — no flash. A blanket of dark dust covers the Earth's face
    and a big translucent black gloom veil hangs between the camera and
    the globe, so the frame actually darkens."""
    fx = _earth(a, b, color="#1E40AF", emissive="#1E3A8A", ei=0.15,
                cont_color="#166534", cont_emissive="#14532D", cont_ei=0.1)
    for i, (dx, dy, dz, r) in enumerate([
            (0.0, 0.0, 2.8, 1.6), (-1.8, 1.0, 2.8, 1.4), (1.8, 1.0, 2.8, 1.4),
            (-1.2, -1.2, 2.7, 1.5), (1.5, -1.2, 2.7, 1.5), (0.0, 2.0, 2.5, 1.3)]):
        fx.append({"id": f"blanket{i}", "shape": "sphere", "radius": r, "color": "#292524",
                   "emissive": "#1C1917", "emissiveIntensity": 0.2, "roughness": 0.9,
                   "opacity": 0.9,
                   "keyframes": [{"frame": a, "position": [dx, 14 + dy, -12 + dz]},
                                {"frame": b, "position": [dx, 14 + dy, -12 + dz]}]})
    fx.append({"id": "gloom", "shape": "sphere", "radius": 6.5, "color": "#000000",
               "emissive": "#000000", "emissiveIntensity": 0.0, "roughness": 1.0,
               "opacity": 0.3,
               "keyframes": [{"frame": a, "position": [0, 14, -5]},
                             {"frame": b, "position": [0, 14, -5]}]})
    return fx


def _gone(a, b):
    """GONE! — the aftermath, still playing under b10: a dim Earth, thin
    scattered dust drifting away, wide empty framing. No flash, no ring,
    no gloom — just a dark, quiet planet."""
    fx = _earth(a, b, color="#1E3A8A", emissive="#172554", ei=0.1,
                cont_color="#14532D", cont_emissive="#14532D", cont_ei=0.1)
    fx += _dust(a, b, [(-6.0, 2.0, 2.0, 0.9, 0.35), (6.0, -2.0, 1.0, 1.0, 0.35),
                       (-3.0, -3.5, 2.5, 0.8, 0.35), (4.0, 3.0, 2.0, 0.8, 0.35)])
    return fx


def _ast(f, S4=None, S5=None):
    """The asteroid head's position at frame f (linear dive from
    [-25, 20, -20] to [2, 13.5, -10]). Bounds are set by scenes()."""
    t = max(0.0, min(1.0, (f - _ast.S4) / (_ast.S5 - _ast.S4))) if _ast.S5 > _ast.S4 else 0.0
    return [-25 + 27 * t, 20 - 6.5 * t, -20 + 10 * t]


# 4. SCENES --------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END
    S2 = B["b3"] - 1    # playground: the kid hides, the rex walks past
    S3 = B["b6"] - 1    # classroom: the teacher explains
    S4 = B["b7"] - 1    # space: the asteroid streaks in
    S5 = B["b9"] - 1    # space: the impact, the dust, the shouts
    S6 = B["b11"] - 1   # street: the payoff — birds are living dinosaurs
    _ast.S4, _ast.S5 = S4, S5

    def rex_face(src, dst):
        # The T. rex faces -x at rotationY 0 (see file docstring), so
        # face() alone aims it 90 deg off — add HALF to point its snout
        # at dst. If the rex walks sideways in stills, fix it here.
        return face(src, dst) + HALF

    # The rex's x along its street walk (0 -> S2) and its playground
    # walk (S2 -> B["b5"]). Both are straight, slow, constant-speed.
    def _rx1(f):
        t = max(0.0, min(1.0, f / S2)) if S2 > 0 else 0.0
        return -8 + 9 * t
    def _rx2(f):
        span = B["b5"] - S2
        t = max(0.0, min(1.0, (f - S2) / span)) if span > 0 else 0.0
        return -8 + 14 * t

    # FIX ROUND 1: hide/peek at x 8.5, clear of the Dare tree canopy
    # from every camera (the old spots put the kid's head inside the
    # canopy balls' disc). The walk runs straight up +z at x 8.5 and
    # never goes under the canopy.
    HIDE_P = [8.5, 0, -4.0]  # beside the tree's right side, by the swings
    PEEK_P = [8.5, 0, -0.5]  # stepped out to watch, clear of canopy / swings / sandbox
    REX_STREET = ([-8, 0, -2], [1, 0, -2])
    REX_PARK = ([-8, 0, 7], [6, 0, 7])
    HOOK_HERO = [-6, 0, 4.5]  # foreground, looking at the camera, the rex looming behind him

    return [
        {   # Hook (NEW): "What if dinosaurs were still alive?" — the hero
            # in the foreground looking at the camera, the T. rex looming
            # right behind him as it walks Main Street. One shot: b0 is
            # 1.5 s, too short to cut. The hero stands at x -6, z 4.5 so
            # he stays 6.5+ studs from the rex's path, clear of the
            # traffic-light pole at (4.4, -0.6) and of the street tree
            # at (-2, -11) — both of which sat behind his head in the
            # first preview (v1 framing had him at [5, 0, 3]).
            # The rex's walk continues seamlessly into street_walk.
            "id": "hook", "location": "street",
            "startFrame": 0, "endFrame": B["b1"],
            "cameraShots": [
                shot(0, B["b1"], [-5, 8, 18], [-5, 7.5, 16.5],
                     [-5, 4.5, -1], [-5, 4.5, -1], 58),
            ],
            "characters": {
                "hero": hold(0, B["b1"], HOOK_HERO, 0, "idle", "shocked"),
                "rex": [kf(0, REX_STREET[0], rex_face(REX_STREET[0], REX_STREET[1]), "walk", "smile"),
                        kf(B["b1"], [_rx1(B["b1"]), 0, -2], rex_face(REX_STREET[0], REX_STREET[1]), "walk", "smile")],
            },
        },
        {   # "In this town, dinosaurs are still alive." The T. rex walks
            # down Main Street, right past the shops. Rex only — the kid
            # is not in this scene, so no spacing risk.
            "id": "street_walk", "location": "street",
            "startFrame": B["b1"], "endFrame": S2,
            "cameraShots": split_shots(B["b1"], S2, [
                lambda a, b: shot(a, b, [_rx1(a), 6, 16], [_rx1(b), 6, 16],
                                  [_rx1(a), 5, -2], [_rx1(b), 5, -2], 58),
                lambda a, b: low_angle(a, b, [_rx1((a + b) // 2), 0, -2], dist=18, scale=1.8),
                lambda a, b: shot(a, b, [_rx1(a), 5, 15], [_rx1(b), 5, 15],
                                  [_rx1(a), 5.5, -2], [_rx1(b), 5.5, -2], 58),
            ]),
            "characters": {
                "rex": [kf(B["b1"], [_rx1(B["b1"]), 0, -2], rex_face(REX_STREET[0], REX_STREET[1]), "walk", "smile"),
                        kf(S2, REX_STREET[1], rex_face(REX_STREET[0], REX_STREET[1]), "walk", "smile")],
            },
        },
        {   # The kid hides by the Dare tree, peeks out, and watches
            # the great animal sniff the air and move on. Fern clusters
            # frame the back of the playground for the prehistoric feel
            # — pushed out to x +-12.5 and shrunk, so no frond reaches
            # the kid's head at the peek spot.
            "id": "hide", "location": "playground",
            "startFrame": S2, "endFrame": S3,
            "fx": [
                {"id": "ferns-left", "shape": "ferns", "scale": 1.2, "color": "#2E8B57",
                 "keyframes": [{"frame": S2, "position": [-12.5, 0, -5]},
                               {"frame": S3, "position": [-12.5, 0, -5]}]},
                {"id": "ferns-right", "shape": "ferns", "scale": 1.2, "color": "#2E8B57",
                 "keyframes": [{"frame": S2, "position": [12.5, 0, -5]},
                               {"frame": S3, "position": [12.5, 0, -5]}]},
            ],
            "cameraShots": split_shots(S2, S3, [
                lambda a, b: wide(a, b, [4, 0, -2]),
                # Wide two-shot: the rex on the left, the kid peeking on
                # the right, both in frame (v1's tight low_angle put the
                # kid out of frame / half cut at the edge). Camera sits
                # on the midpoint between rex and kid, fov 64, so the
                # rex stays inside the frame edge as it walks.
                lambda a, b: shot(a, b, [(_rx2(a) + 8.5) / 2, 5, 22], [(_rx2(b) + 8.5) / 2, 5, 21],
                                  [(_rx2(a) + 8.5) / 2, 5, 3], [(_rx2(b) + 8.5) / 2, 5, 3], 64),
                # FIX ROUND 2: the old close_up(side=2.5) put the camera
                # at [11, 5, 6.5] — INSIDE the Dare-tree foliage ball at
                # [12, 5.8, 5], giving the solid-green flash f396-406.
                # TEST-STILL CORRECTION 2 (2026-11-23): the dark bands
                # are NOT foliage — they are the T. REX. It walks the
                # playground at z=7 ([-8,0,7]->[6,0,7], scale 1.8) and
                # idles at [6,0,7] through the close-up; any camera at
                # z 7-8 sits inside its body corridor. The fix is to put
                # the camera NORTH of the rex's path (z 4.5-4.8, so the
                # rex is behind the camera) — 5 studs from the kid, so
                # fov 55 to keep his head+torso framed as in f480.
                lambda a, b: shot(a, b, [8.0, 5, 4.8], [8.0, 4.9, 4.5],
                                  [8.5, 4.4, -0.5], [8.5, 4.4, -0.5], 55),
            ]),
            "characters": {
                "hero": [kf(S2, HIDE_P, face(HIDE_P, [-8, 0, 7]), "idle", "panic"),
                         kf(B["b4"] - 20, HIDE_P, face(HIDE_P, [_rx2(B["b4"] - 20), 0, 7]), "walk", "panic"),
                         kf(B["b4"] + 40, PEEK_P, face(PEEK_P, [_rx2(B["b4"] + 40), 0, 7]), "walk", "shocked"),
                         kf(B["b4"] + 55, PEEK_P, face(PEEK_P, [_rx2(B["b4"] + 55), 0, 7]), "idle", "shocked"),
                         kf(S3, PEEK_P, face(PEEK_P, [6, 0, 7]), "idle", "shocked")],
                "rex": [kf(S2, REX_PARK[0], rex_face(REX_PARK[0], REX_PARK[1]), "walk", "smile"),
                        kf(B["b5"], REX_PARK[1], rex_face(REX_PARK[0], REX_PARK[1]), "walk", "smile"),
                        kf(B["b5"] + 15, REX_PARK[1], rex_face(REX_PARK[0], REX_PARK[1]), "idle", "smile"),
                        kf(S3, REX_PARK[1], rex_face(REX_PARK[0], REX_PARK[1]), "idle", "smile")],
            },
        },
        {   # The teacher explains: they were here first, a very long time ago.
            # FIX ROUND 1: teacher at x -2.0 (beside the desk) and hero at
            # x 1.5, so the wide camera's sight line to the teacher clears
            # the hero — v1 had the teacher hidden behind the kid.
            "id": "classroom", "location": "classroom",
            "boardText": ["66 MILLION YEARS AGO", "A ROCK 10 KM WIDE", "DUST BLOCKED THE SUN"],
            "startFrame": S3, "endFrame": S4,
            "cameraShots": cover(S3, S4, [
                lambda a, b: wide(a, b, [-0.5, 0, -2]),
                lambda a, b: close_up(a, b, [-2.0, 0, -5.0]),
            ]),
            "characters": {
                "teacher": hold(S3, S4, [-2.0, 0, -5.0], 0.5, "point", "deadpan", "pointer"),
                "hero": hold(S3, S4, [1.5, 0, 1.5], 0, "idle", "smile"),
            },
        },
        {   # The asteroid streaks across the sky, diving at the Earth.
            # FIX ROUND 2: the Earth globe is IN this scene now (it was
            # missing, so the rock dived at an empty point and the hit
            # never read) — it enters frame late in the approach as the
            # asteroid nears it. Tracking cameras ride 10 studs below
            # the asteroid (was 6 / 4), tilting up so the navy floor
            # band never enters frame.
            "id": "asteroid", "location": "space", "skyColor": "#000000",
            "startFrame": S4, "endFrame": S5,
            "fx": _asteroid(S4, S5) + _earth(S4, S5),
            "cameraShots": cover(S4, S5, [
                # TEST-STILL CORRECTION (2026-11-23): offset -10 put
                # the tracking camera at y 4.7 right over the hero's
                # head ([-3,0,0.5]) — f780 was all hair. Offset -7
                # keeps the camera above his head (y 6.5+) while the
                # steep upward axis (21-27 deg) keeps the floor out
                # (bottom ray -2 to -8 deg) and the hero out of frame.
                lambda a, b: shot(a, b, [_ast(a)[0], _ast(a)[1] - 7, _ast(a)[2] + 18],
                                  [_ast(b)[0], _ast(b)[1] - 7, _ast(b)[2] + 18],
                                  _ast(a), _ast(b), 58),
                lambda a, b: close_up(a, b, [-3, 0, 0.5]),
                lambda a, b: shot(a, b, [_ast(a)[0], _ast(a)[1] - 7, _ast(a)[2] + 14],
                                  [_ast(b)[0], _ast(b)[1] - 7, _ast(b)[2] + 14],
                                  _ast(a), _ast(b), 58),
            ]),
            "characters": {
                "hero": hold(S4, S5, [-3, 0, 0.5], 0.2, "point", "shocked"),
            },
        },
        {   # The impact (b9): flash, dust starting to spread. The hero
            # stands off-camera (the Earth shots never frame him).
            # FIX ROUND 2: the orbit shot is GONE — its 11-stud radius
            # swung the Earth out of frame by f900. Both shots are now
            # static/slow-push from low (y 6) looking up at the globe
            # (target y 17, fov 52): the Earth stays centred at a
            # constant distance through the whole impact, and the bottom
            # ray sits above horizontal so the navy floor never enters.
            "id": "impact", "location": "space", "skyColor": "#000000",
            "startFrame": S5, "endFrame": B["w1"] - 12,
            "fx": _impact(S5, B["w1"] - 12),
            "cameraShots": split_shots(S5, B["w1"] - 12, [
                lambda a, b: shot(a, b, [0, 6, 9], [0, 6, 8],
                                  [0, 17, -12], [0, 17, -12], 52),
                lambda a, b: shot(a, b, [0, 6, 8], [0, 6, 7],
                                  [0, 17, -12], [0, 17, -12], 52),
            ]),
            "characters": {
                "hero": hold(S5, B["w1"] - 12, [-3, 0, 0.5], 0.2, "point", "panic"),
            },
        },
        {   # BOOM! — the flash at its peak, with the shock ring.
            # Boundaries are set so the BOOM! caption (w1) plays fully
            # inside this scene: it starts 12f before w1 and ends 3f
            # before w2 starts.
            "id": "boom", "location": "space", "skyColor": "#000000",
            "startFrame": B["w1"] - 12, "endFrame": B["w2"] - 3,
            "fx": _boom(B["w1"] - 12, B["w2"] - 3),
            # FIX ROUND 2: low camera (y 6) looking up at the globe
            # (target y 17) — bottom ray above horizontal, floor out.
            "cameraShots": [
                static_shot(B["w1"] - 12, B["w2"] - 3, [0, 6, 7], [0, 17, -12], 52),
            ],
            "characters": {
                "hero": hold(B["w1"] - 12, B["w2"] - 3, [-3, 0, 0.5], 0.2, "point", "panic"),
            },
        },
        {   # DARK! — the dust blanket + gloom veil: the frame actually darkens.
            # Exactly 30f (1.0s, the shot minimum): it starts 3f before
            # w2 and ends 4f into w3, so the DARK! caption plays fully
            # inside it and GONE! starts inside the gone scene.
            "id": "dark", "location": "space", "skyColor": "#000000",
            "startFrame": B["w2"] - 3, "endFrame": B["w3"] + 4,
            "fx": _dark(B["w2"] - 3, B["w3"] + 4),
            # FIX ROUND 2: low camera (y 6) looking up at the globe
            # (target y 17) — bottom ray above horizontal, floor out.
            "cameraShots": [
                static_shot(B["w2"] - 3, B["w3"] + 4, [0, 6, 6], [0, 17, -12], 50),
            ],
            "characters": {
                "hero": hold(B["w2"] - 3, B["w3"] + 4, [-3, 0, 0.5], 0.2, "point", "panic"),
            },
        },
        {   # GONE! — the aftermath under b10: a dim Earth, thin dust
            # drifting away, wide empty framing. The street payoff
            # starts at b11.
            "id": "gone", "location": "space", "skyColor": "#000000",
            "startFrame": B["w3"] + 4, "endFrame": S6,
            "fx": _gone(B["w3"] + 4, S6),
            # FIX ROUND 2: low camera (y 7) looking up at the globe
            # (target y 18, fov 52) — bottom ray above horizontal,
            # floor out; wide empty framing for the aftermath.
            "cameraShots": [
                static_shot(B["w3"] + 4, S6, [0, 7, 10], [0, 18, -12], 52),
            ],
            "characters": {
                "hero": hold(B["w3"] + 4, S6, [-3, 0, 0.5], 0.2, "point", "shocked"),
            },
        },
        {   # Payoff: the dinosaurs never fully left — the kid looks up,
            # points at the sky, and waves at a living dinosaur.
            # FIX ROUND 1: at b13 he leans back (rx) into a point and
            # waves leaning back, so he actually looks up; the last
            # shots are low_angle, putting sky (not the street tree
            # line) behind his head.
            "id": "payoff", "location": "street",
            "startFrame": S6, "endFrame": END,
            "cameraShots": split_shots(S6, END, [
                lambda a, b: wide(a, b, [-8, 0, 0.5]),
                lambda a, b: shot(a, b, [-1, 3.5, 11], [-1, 3.2, 10],
                                  [-8, 4.5, 0.5], [-8, 4.5, 0.5], 54),
                lambda a, b: low_angle(a, b, [-8, 0, 0.5], dist=9, scale=1.0),
                lambda a, b: low_angle(a, b, [-8, 0, 0.5], dist=7, scale=1.0),
            ]),
            "characters": {
                "hero": [kf(S6, [-8, 0, 0.5], 0, "idle", "smile"),
                         kf(B["b11"], [-8, 0, 0.5], 0, "point", "smile"),
                         kf(B["b13"], [-8, 0, 0.5], 0, "point", "laugh", rx=-0.35),
                         kf(END, [-8, 0, 0.5], 0, "wave", "laugh", rx=-0.30)],
            },
        },
    ]
