"""TEST-ONLY story — verifies the four Week 2-5 builds: tunnel location,
rainbow arcs, undersea location, lightning bolt. NEVER for publishing. Run:
    python scripts/make_short.py stories/_test_week2_5_props.py --stills
"""
import math
import random

from shorts.scene import (  # noqa: F401
    HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, orbit,
    shot, split_shots, static_shot, wide,
)

TITLE = "TEST WEEK2-5 PROPS"

BEATS = [
    {"id": "b1", "text": "In this world, you can dig a hole straight through the Earth.", "pause": 0.08},
    {"id": "b2", "text": "Down you go, past the dark rock, toward the lava below.", "pause": 0.08},
    {"id": "b3", "text": "And after the rain, a rainbow arcs over the whole town.", "pause": 0.08},
    {"id": "b4", "text": "Six colours, in order, red to violet, painted across the sky.", "pause": 0.08},
    {"id": "b5", "text": "Deep under the sea, a black cable carries the internet.", "pause": 0.08},
    {"id": "b6", "text": "It snakes across the sand, past the fish and the seaweed.", "pause": 0.08},
    {"id": "b7", "text": "And when the storm comes, the lightning strikes the street.", "pause": 0.08},
    {"id": "b8", "text": "One bright zigzag, from the clouds to the ground.", "pause": 0.3},
]

MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05}
SFX = [
    ("b1", "whoosh"),
    ("b3+0.5", "pop"),
    ("b5+0.5", "sparkle"),
    ("b7+0.5", "riser"),
    ("b8+0.5", "twist"),
]

CAST = {
    "hero": {"extends": "kid_boy", "hair": {"style": "spikyAnime", "color": "blue"},
             "top": {"style": "hoodie", "color": "royal", "secondary": "white"},
             "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"color": "white", "sole": "white"},
             "freckles": True},
    "friend": {"extends": "kid_girl", "hair": {"style": "ponytail", "color": "blonde"},
               "top": {"style": "hoodie", "color": "pink", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"color": "white", "sole": "white"}},
    # Falling boy (Gemini tunnel reference): red shirt, blue jeans, brown hair.
    "digger": {"extends": "kid_boy", "hair": {"style": "messyFringe", "color": "brown"},
               "top": {"style": "tshirt", "color": "red", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"color": "white", "sole": "white"}},
    # Boy in the doorway (Gemini lightning reference): yellow jacket.
    "stormboy": {"extends": "kid_boy", "hair": {"style": "messyFringe", "color": "brown"},
                 "top": {"style": "hoodie", "color": "yellow", "secondary": "white"},
                 "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"color": "white", "sole": "white"}},
}


def _rainbow(a, b):
    """Rainbow over the town (Gemini reference): six half-torus arcs, red
    outside to violet inside, plus blocky clouds, a glowing square sun
    through the arch, and stepped green hills in the foreground."""
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


def _fish(a, b):
    """School of yellow blocky fish (Gemini undersea reference): body box +
    tail box per fish, drifting slowly left with a small bob."""
    rnd = random.Random(20261117)
    fx = []
    for i in range(8):
        x = 0 + rnd.uniform(-4, 8)
        y = 5 + rnd.uniform(0, 4)
        z = -6 + rnd.uniform(-3, 3)
        drift = -2 - rnd.uniform(0, 1.5)
        bob = rnd.uniform(-0.5, 0.5)
        fx.append({"id": f"fish{i}", "shape": "box", "size": [1.4, 0.9, 0.6],
                   "color": "#FACC15", "emissive": "#FDE047", "emissiveIntensity": 0.6,
                   "roughness": 0.5,
                   "keyframes": [{"frame": a, "position": [x, y, z]},
                                 {"frame": b, "position": [x + drift, y + bob, z]}]})
        fx.append({"id": f"fish{i}-tail", "shape": "box", "size": [0.5, 1.1, 0.3],
                   "color": "#FACC15", "emissive": "#FDE047", "emissiveIntensity": 0.6,
                   "roughness": 0.5,
                   "keyframes": [{"frame": a, "position": [x + 0.95, y, z]},
                                 {"frame": b, "position": [x + drift + 0.95, y + bob, z]}]})
    return fx


def _bolt(a, b):
    """Lightning bolt (Gemini reference): a thick jagged staircase of glowing
    yellow boxes from the cloud base to the ground, plus two side branches."""
    fx = []
    x0, y0, z0 = 9.0, 30.0, -4.0
    x1, y1, z1 = 8.0, 0.0, -1.0
    n = 8
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        cx = x0 + (x1 - x0) * (t0 + t1) / 2 + (0.9 if i % 2 == 0 else -0.9)
        cy = y0 + (y1 - y0) * (t0 + t1) / 2
        cz = z0 + (z1 - z0) * (t0 + t1) / 2
        rz = 0.35 if i % 2 == 0 else -0.35
        fx.append({"id": f"bolt{i}", "shape": "box", "size": [1.2, 4.4, 1.2],
                   "color": "#FACC15", "emissive": "#EAB308", "emissiveIntensity": 1.6,
                   "roughness": 0.4, "rotation": [0, 0, rz],
                   "keyframes": [{"frame": a, "position": [cx, cy, cz]},
                                 {"frame": b, "position": [cx, cy, cz]}]})
    for j, (bx, by, bz, s) in enumerate([(10.2, 22, -3.5, 1), (6.8, 14, -2.5, -1)]):
        for k in range(3):
            fx.append({"id": f"branch{j}-{k}", "shape": "box", "size": [0.7, 2.0, 0.7],
                       "color": "#FACC15", "emissive": "#EAB308", "emissiveIntensity": 1.6,
                       "roughness": 0.4, "rotation": [0, 0, s * 0.7],
                       "keyframes": [{"frame": a, "position": [bx + s * k * 1.1, by - k * 1.6, bz]},
                                     {"frame": b, "position": [bx + s * k * 1.1, by - k * 1.6, bz]}]})
    return fx


def _clouds(a, b):
    """Dark storm clouds: big stacked slabs overhead."""
    out = []
    for i, (x, y, z, w, h, d, c) in enumerate([
            (-6, 24, -6, 22, 4, 10, "#0F172A"),
            (8, 26, -8, 18, 3.5, 9, "#1E293B"),
            (16, 23, -4, 16, 3, 8, "#0F172A"),
            (-16, 25, -8, 20, 3.5, 9, "#334155"),
            (0, 27, -10, 14, 3, 8, "#1E293B")]):
        out.append({"id": f"storm{i}", "shape": "box", "size": [w, h, d], "color": c,
                    "roughness": 0.95,
                    "keyframes": [{"frame": a, "position": [x, y, z]},
                                 {"frame": b, "position": [x, y, z]}]})
    return out


def _rain(a, b):
    """Rain streaks: thin translucent slanted boxes falling over the scene."""
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


def _wet(a, b):
    """Wet street: a dark glossy slab over the yard/road (the engine has no
    true mirror reflections — this plus the glow streak under the strike
    point is the honest limit), and a yellow glow streak for the bolt's
    reflection."""
    return [
        {"id": "wet", "shape": "box", "size": [34, 0.06, 22], "color": "#1E293B",
         "roughness": 0.08,
         "keyframes": [{"frame": a, "position": [1, 0.03, 2]},
                      {"frame": b, "position": [1, 0.03, 2]}]},
        {"id": "glow", "shape": "box", "size": [2.5, 0.1, 12], "color": "#FDE047",
         "emissive": "#FDE047", "emissiveIntensity": 1.2, "roughness": 0.4, "opacity": 0.45,
         "keyframes": [{"frame": a, "position": [8, 0.14, 2]},
                      {"frame": b, "position": [8, 0.14, 2]}]},
    ]


def scenes(T):
    S2, S3, S4, END = T.B["b3"] - 1, T.B["b5"] - 1, T.B["b7"] - 1, T.END

    return [
        {   # TUNNEL: the boy falls down the shaft (y 14 -> 4, 'jump' arms up).
            # The camera sits inside the shaft: look up for sky + boy, look
            # down for lava + boy, low-angle for the boy himself.
            "id": "tunnel", "location": "tunnel", "skyColor": "#1E293B",
            "startFrame": 0, "endFrame": S2,
            "cameraShots": split_shots(0, S2, [
                lambda a, b: static_shot(a, b, [0, 1, 5], [0, 16, -3], 58),
                lambda a, b: static_shot(a, b, [0, 20, 7], [0, 6, -2], 58),
                lambda a, b: low_angle(a, b, [0, 9, -1], dist=7, eye_height=1.0),
            ]),
            "characters": {
                "digger": [kf(0, [0, 14, -1], 0, "jump", "shocked"),
                           kf(S2, [0, 4, -1], 0, "jump", "shocked")],
            },
        },
        {   # RAINBOW over the town: arcs + clouds + square sun + green hills.
            "id": "rainbow", "location": "town_overview", "skyColor": "#38BDF8",
            "startFrame": S2, "endFrame": S3,
            "cameraShots": split_shots(S2, S3, [
                lambda a, b: static_shot(a, b, [0, 16, 42], [0, 12, -28], 58),
                lambda a, b: static_shot(a, b, [8, 6, 26], [-2, 15, -28], 58),
                lambda a, b: close_up(a, b, [-3, 0, 8]),
            ]),
            "fx": _rainbow(S2, S3),
            "characters": {
                "hero": hold(S2, S3, [-3, 0, 8], 0.2, "point", "shocked"),
                "friend": hold(S2, S3, [2.5, 0, 8], -0.2, "idle", "smile"),
            },
        },
        {   # UNDERSEA: sand, cable, rays, fish school.
            "id": "undersea", "location": "undersea", "skyColor": "#1D6FB8",
            "startFrame": S3, "endFrame": S4,
            "cameraShots": split_shots(S3, S4, [lambda a, b: wide(a, b, [0, 0, 3.5], 24),
                                                lambda a, b: close_up(a, b, [-3, 0, 3.5]),
                                                lambda a, b: static_shot(a, b, [6, 14, 16], [0, 0, -2], 58)]),
            "fx": _fish(S3, S4),
            "characters": {
                "hero": hold(S3, S4, [-3, 0, 3.5], 0.2, "point", "shocked"),
                "friend": hold(S3, S4, [2.5, 0, 3.5], -0.2, "idle", "smile"),
            },
        },
        {   # LIGHTNING: yellow house at night, boy in the doorway, bolt
            # striking the yard, storm clouds, rain, wet street.
            "id": "lightning", "location": "house", "variant": "yellow", "isNight": True,
            "skyColor": "#1E3A8A",
            "startFrame": S4, "endFrame": END,
            "cameraShots": split_shots(S4, END, [
                lambda a, b: wide(a, b, [4, 0, 0], 24),
                lambda a, b: close_up(a, b, [0, 0, -2]),
                lambda a, b: static_shot(a, b, [6, 3, 14], [8, 10, -3], 58),
                lambda a, b: static_shot(a, b, [0, 3, 12], [4, 18, -4], 58),
            ]),
            "fx": _bolt(S4, END) + _clouds(S4, END) + _rain(S4, END) + _wet(S4, END),
            "characters": {
                "stormboy": hold(S4, END, [0, 0, -2], 0, "idle", "shocked"),
            },
        },
    ]
