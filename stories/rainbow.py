"""WHAT MAKES A RAINBOW? - science explainer.

Batch story: video 4 of 7.
Structure is a "why" explainer (question -> rain + sun -> classroom
mechanism -> aerial arc -> closer), like sky_blue / stars_twinkle. No
"What if" — the opening asks the "What...?" question itself.

The science: sunlight looks white but is every colour mixed together.
When sunlight hits a raindrop the drop bends (refracts) the light and
splits it into colours; inside the drop the light reflects once, then
bends again on the way out. Red bends least (outside), violet bends most
(inside), so the order is always the same. You see the arc when the sun
is behind you, low in the sky, and the rain is ahead of you — millions
of drops painting one arc. All plain-language, standard figures,
simplified for a Short.

Fresh visuals: the rainbow arcs (six half-torus rings, red outside to
violet inside — already built and tested in _test_week2_5_props.py, reused
here, not rebuilt), rain streaks over the street, the classroom raindrop
demo (white beam in, coloured fan out), the aerial arc over the town.
Lead: CasualMan (kit) — Bolt Boy does not lead this one. New music:
sky-blue.wav (bright day, fits the rainbow).

FIX ROUND 1 (preview stills, 2026-11-23): kit hero is ~1.5x R6 height, so
plain close_up/low_angle frame him too tight (hair/arms cut, teacher
half-face at the edge) — hero close-ups now scale=1.5, dist=10;
low_angles dist=12 (hero scale=1.5); sky/over-shoulder cameras pulled
back so nobody is cut at the frame edge; aerial shot 2 replaced (the old
[8,6,26] camera sat inside a building); raindrop demo sphere made solid
(the translucent one showed the wall clock through it); closer close-ups
use side offsets so the facing-each-other pair show their faces.

Build:   python scripts/make_short.py stories/rainbow.py --stills
Render:  node scripts/render.mjs story rainbow --port 3051 (stills+ffmpeg)
"""
import math
import random

from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, shot, split_shots, static_shot, wide  # noqa: F401

TITLE = "WHAT MAKES A RAINBOW?"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this town, after the rain, a rainbow arcs over the houses. But what makes a rainbow?", "pause": 0.08},
    {"id": "b2", "text": "You need two things at the same time: sunshine, and rain.", "pause": 0.10},
    {"id": "b3", "text": "The rain has to be in front of you, and the sun has to be behind you.", "pause": 0.10},
    {"id": "b3b", "text": "And the sun has to be low in the sky. At noon, the rainbow hides below the ground.", "pause": 0.08},
    {"id": "b4", "text": "Sunlight looks white. But white light is every colour, mixed together.", "pause": 0.10},
    {"id": "b5", "text": "When sunlight hits a raindrop, the drop bends the light — and splits it apart.", "pause": 0.10},
    {"id": "b6", "text": "Inside the drop, the light bounces once, like a mirror, then bends again on the way out.", "pause": 0.10},
    {"id": "b7", "text": "Red bends the least, so it lands on the outside. Violet bends the most, so it sits on the inside.", "pause": 0.10},
    {"id": "b8", "text": "That is why a rainbow always has the same order: red outside, violet inside.", "pause": 0.10},
    {"id": "b9", "text": "Millions of raindrops, each bending the light, paint one giant arc across the sky.", "pause": 0.10},
    {"id": "b10", "text": "The arc is a circle, really — the ground just hides the bottom half.", "pause": 0.08},
    {"id": "b11", "text": "No rain, no rainbow. No sun, no rainbow. You need both, at the same moment.", "pause": 0.10},
    {"id": "b12", "text": "So next time it rains and the sun comes out, turn your back to the sun — and look for the rainbow.", "pause": 0.10},
    {"id": "b13", "text": "It is sunlight, split apart by the rain. A whole rainbow, hiding inside every drop.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/sky-blue.wav",
    "under_voice": 0.022,
    "gaps": 0.05,
}

SFX = [
    ("b1", "whoosh"),
    ("b2+0.5", "pop", {"f": 600}),
    ("b3+0.5", "swish"),
    ("b3b+0.5", "pop", {"f": 600}),
    ("b4+0.5", "sparkle"),
    ("b5+0.5", "pop", {"f": 600}),
    ("b6+0.5", "sparkle"),
    ("b7+0.5", "pop", {"f": 600}),
    ("b8+0.5", "reveal"),
    ("b9+0.5", "whoosh"),
    ("b10+0.5", "pop", {"f": 600}),
    ("b11+0.5", "pop", {"f": 600}),
    ("b12+0.5", "sparkle"),
    ("b13+1.0", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
# Lead: CasualMan (kit) — variety, Bolt Boy does not lead this one.
CAST = {
    "hero": {"kit": "casualman"},
    "friend": {"extends": "kid_girl", "hair": {"style": "ponytail", "color": "blonde"},
               "top": {"style": "hoodie", "color": "pink", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"color": "white", "sole": "white"}},
    "mom": {"extends": "real_mom", "hair": {"style": "ponytail", "color": "brown"}},
    # White blouse on purpose (sky_blue / stars_twinkle pattern). She stands
    # BESIDE the desk at x -3.0, not on it - verify in the stills.
    "teacher": {"extends": "teacher_woman", "skin": "fair", "hair": {"style": "bun", "color": "blonde"}},
}


def _rainbow(a, b):
    """Rainbow over the town (Gemini reference, tested in
    _test_week2_5_props.py): six half-torus arcs, red outside to violet
    inside, plus blocky clouds, a glowing square sun through the arch, and
    stepped green hills in the foreground."""
    colors = ["#EF4444", "#F97316", "#FACC15", "#22C55E", "#2563EB", "#7C3AED"]
    fx = []
    for i, col in enumerate(colors):
        r = 22 - i * 1.6
        fx.append({"id": f"bow{i}", "shape": "ring", "radius": r, "tube": 0.85,
                   "color": col, "emissive": col, "emissiveIntensity": 0.55,
                   "roughness": 0.5, "arc": math.pi, "rotation": [0, 0, 0],
                   "keyframes": [{"frame": a, "position": [0, 1, -28]},
                                 {"frame": b, "position": [0, 1, -28]}]})
    for i, (x, y, z, w) in enumerate([(-18, 26, -30, 7), (16, 30, -32, 9), (26, 24, -26, 6)]):
        fx.append({"id": f"cloud{i}", "shape": "box", "size": [w, 2.5, 2], "color": "#F8FAFC",
                   "roughness": 0.9,
                   "keyframes": [{"frame": a, "position": [x, y, z]},
                                 {"frame": b, "position": [x, y, z]}]})
        fx.append({"id": f"cloud{i}b", "shape": "box", "size": [w * 0.6, 2, 1.6], "color": "#F8FAFC",
                   "roughness": 0.9,
                   "keyframes": [{"frame": a, "position": [x + 1, y + 1.6, z]},
                                 {"frame": b, "position": [x + 1, y + 1.6, z]}]})
    fx.append({"id": "sun", "shape": "box", "size": [5, 5, 0.5], "color": "#FEF3C7",
               "emissive": "#FDE68A", "emissiveIntensity": 2.5, "roughness": 0.4,
               "keyframes": [{"frame": a, "position": [0, 13, -30]},
                            {"frame": b, "position": [0, 13, -30]}]})
    for i, (x, y, z, w, h, d) in enumerate([
            (-12, 2, 33, 26, 4, 12), (14, 1.5, 31, 22, 3, 10), (0, 1, 37, 18, 2, 8)]):
        fx.append({"id": f"hill{i}", "shape": "box", "size": [w, h, d], "color": "#22C55E",
                   "roughness": 0.9,
                   "keyframes": [{"frame": a, "position": [x, y, z]},
                                 {"frame": b, "position": [x, y, z]}]})
    # second tiers so the hills read as stepped terraces, not flat slabs
    for i, (x, y, z, w, h, d) in enumerate([
            (-12, 5.5, 33, 16, 3, 8), (14, 4.25, 31, 13, 2.5, 7)]):
        fx.append({"id": f"hilltop{i}", "shape": "box", "size": [w, h, d], "color": "#16A34A",
                   "roughness": 0.9,
                   "keyframes": [{"frame": a, "position": [x, y, z]},
                                 {"frame": b, "position": [x, y, z]}]})
    return fx


def _rain(a, b):
    """Rain streaks (tested in _test_week2_5_props.py): thin translucent
    slanted boxes falling over the scene."""
    rnd = random.Random(20261117)
    fx = []
    for i in range(40):
        x = -16 + rnd.uniform(0, 34)
        y = 4 + rnd.uniform(0, 22)
        z = -12 + rnd.uniform(0, 20)
        fx.append({"id": f"rain{i}", "shape": "box", "size": [0.12, 3.2, 0.12],
                   "color": "#BFDBFE", "emissive": "#DBEAFE", "emissiveIntensity": 0.5,
                   "roughness": 0.4, "opacity": 0.3, "rotation": [0, 0, 0.18],
                   "keyframes": [{"frame": a, "position": [x, y, z]},
                                 {"frame": b, "position": [x, y - 14, z]}]})
    return fx


def _raindrop_demo(a, b):
    """Classroom demo, floating high above the board: one big raindrop
    (pale-blue translucent sphere), a white beam entering from the left,
    and three coloured beams fanning out to the right — white light in,
    colours out. Same idea as stars_twinkle's star-point / planet-disc demo."""
    fx = [
        {"id": "drop", "shape": "sphere", "radius": 1.4, "color": "#BFDBFE",
         "emissive": "#60A5FA", "emissiveIntensity": 0.35, "roughness": 0.15,
         "keyframes": [{"frame": a, "position": [0, 9.5, -2]},
                      {"frame": b, "position": [0, 9.5, -2]}]},
        {"id": "beam-in", "shape": "box", "size": [5.0, 0.35, 0.35], "color": "#FFFFFF",
         "emissive": "#FFFFFF", "emissiveIntensity": 1.4, "roughness": 0.3,
         "keyframes": [{"frame": a, "position": [-4.5, 9.5, -2]},
                      {"frame": b, "position": [-4.5, 9.5, -2]}]},
    ]
    # red bends least (shallowest fan), violet bends most (steepest fan)
    for i, (col, dy, rz) in enumerate([
            ("#EF4444", 0.9, -0.28), ("#FACC15", 0.0, 0.0), ("#7C3AED", -0.9, 0.28)]):
        fx.append({"id": f"beam-out{i}", "shape": "box", "size": [4.5, 0.3, 0.3],
                   "color": col, "emissive": col, "emissiveIntensity": 1.2,
                   "roughness": 0.3, "rotation": [0, 0, rz],
                   "keyframes": [{"frame": a, "position": [3.6, 9.5 + dy, -2]},
                                 {"frame": b, "position": [3.6, 9.5 + dy, -2]}]})
    return fx


# 4. SCENES ---------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S_RAIN = B["b3"] - 1    # street, rain: sun behind / rain ahead + sun low
    S_CLASS = B["b4"] - 1   # classroom: the mechanism
    S_AERIAL = B["b9"] - 1  # town_overview: millions of drops paint the arc
    S_STREET2 = B["b11"] - 1  # street, rainbow: no rain / no sun, no rainbow
    S_CLOSE = B["b12"] - 1  # living room (blue), night: closer

    scenes = []

    # 1. HOOK - street, rainbow over the town. Both look up at the arc --------------
    scenes.append({
        "id": "hook", "location": "street", "skyColor": "#38BDF8",
        "startFrame": 0, "endFrame": S_RAIN,
        "cameraShots": split_shots(0, S_RAIN, [
            lambda a, b: shot(a, b, [0, 4, 22], [0, 5, 20], [0, 13, -28], [0, 13, -28], 58),
            lambda a, b: low_angle(a, b, [-4, 0, 0.5], dist=12, eye_height=1.2, scale=1.5),
            lambda a, b: close_up(a, b, [1, 0, 0.5]),
            lambda a, b: shot(a, b, [-1, 6, 17], [-1, 6, 16], [0, 12, -28], [0, 12, -28], 58),
        ]),
        "fx": _rainbow(0, S_RAIN),
        "characters": {
            "hero": hold(0, S_RAIN, [-4, 0, 0.5], 0.2, "point", "shocked"),
            "friend": hold(0, S_RAIN, [1, 0, 0.5], -0.2, "idle", "shocked"),
        },
    })

    # 2. RAIN - same street, grey sky, rain falling. The other half of the recipe --
    scenes.append({
        "id": "rain", "location": "street", "skyColor": "#94A3B8",
        "startFrame": S_RAIN, "endFrame": S_CLASS,
        "cameraShots": cover(S_RAIN, S_CLASS, [lambda a, b: wide(a, b, [0, 0, 0.5], 24),
                                                lambda a, b: close_up(a, b, [-4, 0, 0.5], scale=1.5, dist=10),
                                                lambda a, b: low_angle(a, b, [1, 0, 0.5], dist=12, eye_height=1.2)]),
        "fx": _rain(S_RAIN, S_CLASS),
        "characters": {
            "hero": hold(S_RAIN, S_CLASS, [-4, 0, 0.5], 0.2, "idle", "shocked"),
            "friend": hold(S_RAIN, S_CLASS, [1, 0, 0.5], -0.2, "idle", "shocked"),
        },
    })

    # 3. CLASSROOM - the mechanism: white beam in, colours out -----------------------
    scenes.append({
        "id": "mechanism", "location": "classroom",
        "boardText": ["SUNLIGHT = ALL COLOURS", "RAINDROP BENDS LIGHT", "RED OUTSIDE, VIOLET INSIDE"],
        "startFrame": S_CLASS, "endFrame": S_AERIAL,
        "cameraShots": cover(S_CLASS, S_AERIAL, [lambda a, b: shot(a, b, [0, 7.4, 23], [0, 7.4, 23], [0, 4.8, -1], [0, 4.8, -1], 58),
                                                  lambda a, b: close_up(a, b, [-0.5, 0, 0.5], scale=1.5, dist=10),
                                                  lambda a, b: close_up(a, b, [-3.0, 0, -4.5])]),
        "fx": _raindrop_demo(S_CLASS, S_AERIAL),
        "characters": {
            "teacher": hold(S_CLASS, S_AERIAL, [-3.0, 0, -4.5], 0.5, "point", "deadpan", "pointer"),
            "hero": hold(S_CLASS, S_AERIAL, [-0.5, 0, 0.5], 0, "idle", "smile"),
            "friend": hold(S_CLASS, S_AERIAL, [4.0, 0, 0.5], 0, "idle", "smile"),
        },
    })

    # 4. AERIAL - town_overview: the whole arc, millions of drops --------------------
    scenes.append({
        "id": "aerial", "location": "town_overview", "skyColor": "#38BDF8",
        "startFrame": S_AERIAL, "endFrame": S_STREET2,
        "cameraShots": split_shots(S_AERIAL, S_STREET2, [
            lambda a, b: static_shot(a, b, [0, 16, 42], [0, 12, -28], 58),
            lambda a, b: static_shot(a, b, [16, 18, 36], [0, 12, -28], 58),
            lambda a, b: static_shot(a, b, [-14, 10, 30], [2, 14, -28], 58),
        ]),
        "fx": _rainbow(S_AERIAL, S_STREET2),
        "characters": {},
    })

    # 5. STREET, RAINBOW - back on the ground: no rain, no sun, no rainbow ----------
    scenes.append({
        "id": "both", "location": "street", "skyColor": "#38BDF8",
        "startFrame": S_STREET2, "endFrame": S_CLOSE,
        "cameraShots": cover(S_STREET2, S_CLOSE, [lambda a, b: shot(a, b, [0, 4, 22], [0, 5, 20], [0, 13, -28], [0, 13, -28], 58),
                                                   lambda a, b: close_up(a, b, [-4, 0, 0.5], scale=1.5, dist=10),
                                                   lambda a, b: close_up(a, b, [1, 0, 0.5])]),
        "fx": _rainbow(S_STREET2, S_CLOSE),
        "characters": {
            "hero": hold(S_STREET2, S_CLOSE, [-4, 0, 0.5], 0.2, "point", "smile"),
            "friend": hold(S_STREET2, S_CLOSE, [1, 0, 0.5], -0.2, "idle", "smile"),
        },
    })

    # 6. LIVING ROOM (blue), NIGHT - closer ------------------------------------------
    scenes.append({
        "id": "closer", "location": "living_room", "variant": "blue", "isNight": True,
        "startFrame": S_CLOSE, "endFrame": END,
        "cameraShots": cover(S_CLOSE, END, [lambda a, b: wide(a, b, [0, 0, 0.4], 24),
                                             lambda a, b: close_up(a, b, [-4.0, 0, 0.4], scale=1.5, dist=10, side=2.5),
                                             lambda a, b: close_up(a, b, [4.0, 0, 0.4], side=-2.5)]),
        "characters": {
            "hero": [kf(S_CLOSE, [-4.0, 0, 0.4], 0.9, "idle", "deadpan"),
                     kf(B["b13"], [-4.0, 0, 0.4], 0.9, "idle", "smile"),
                     kf(END, [-4.0, 0, 0.4], 0.9, "idle", "smile")],
            "mom": [kf(S_CLOSE, [4.0, 0, 0.4], -0.9, "wave", "smile"),
                    kf(END, [4.0, 0, 0.4], -0.9, "wave", "smile")],
        },
    })

    return scenes
