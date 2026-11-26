"""WHAT IF YOU TRAVELLED AT LIGHT SPEED? - science explainer.

Week 1 storyboard (the maintainer, 2026-11-17): video 6 of 7.
Structure: hook (the ship warps past) -> space warp (the stars stretch,
time slows) -> classroom mechanism (the energy wall) -> space (the speed
limit) -> closer. No shouts, fast driving mood.

The science: light moves at about 300,000 kilometres a second — fast
enough to circle the Earth seven times in one second. The faster you go,
the slower your clock runs: near light speed, a year for you could be ten
years back on Earth. But the faster you go, the more energy you need, and
reaching light speed itself would take infinite energy — so nothing with
mass can ever reach it. Light can, because light has no mass. All
plain-language, standard figures, simplified for a Short.

Fresh visuals: the spaceship (already built) + star streaks (already
built), framed three-quarter and from the side so the nose reads as a nose
and not a ball, warp shots looking up at the streak field, new music
(light-speed.wav). The teacher is in the standard white blouse, placed
beside the desk at x -3.0 (not on it).

Build:   python scripts/make_short.py stories/light_speed.py --stills
Render:  python scripts/make_short.py stories/light_speed.py --skip-tts --render
"""
import math  # noqa: F401

from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, shot, split_shots, static_shot, wide  # noqa: F401

TITLE = "WHAT IF YOU TRAVELLED AT LIGHT SPEED?"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this world, you are flying at light speed. And the stars are stretching past you like lines.", "pause": 0.08},
    {"id": "b2", "text": "Light moves at about 300,000 kilometres every second. Fast enough to circle the Earth seven times in one second.", "pause": 0.10},
    {"id": "b3", "text": "At that speed, the stars ahead of you squeeze together. The stars behind you stretch out.", "pause": 0.10},
    {"id": "b4", "text": "And something strange happens to time. The faster you go, the slower your clock runs.", "pause": 0.10},
    {"id": "b5", "text": "Fly near light speed for a year, come home — and ten years have passed on Earth.", "pause": 0.10},
    {"id": "b5b", "text": "Your twin back on Earth would grow old while you stay young. That is not science fiction — it is real physics.", "pause": 0.08},
    {"id": "b6", "text": "But there is a catch. The faster you go, the heavier you get — and the more energy you need.", "pause": 0.10},
    {"id": "b7", "text": "To reach light speed itself, you would need infinite energy. More energy than the whole universe has.", "pause": 0.10},
    {"id": "b8", "text": "So light speed is the speed limit of the universe. Nothing with mass can ever reach it.", "pause": 0.10},
    {"id": "b8b", "text": "Even the biggest rocket ever built could only dream of it. The fuel would weigh more than the Earth.", "pause": 0.08},
    {"id": "b9", "text": "Not a rocket. Not a spaceship. Not even the fastest thing anyone could build.", "pause": 0.10},
    {"id": "b10", "text": "Light itself can do it — because light has no mass at all.", "pause": 0.10},
    {"id": "b11", "text": "So the fastest trip in the universe is one we can never take. But we can dream about it — at 300,000 kilometres a second.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/light-speed.wav",
    "under_voice": 0.022,
    "gaps": 0.05,
}

SFX = [
    ("b1", "whoosh"),
    ("b1+0.5", "sparkle"),
    ("b2+0.5", "pop", {"f": 600}),
    ("b3+0.5", "whoosh"),
    ("b4+0.5", "bell_low"),
    ("b5+0.5", "pop", {"f": 600}),
    ("b6+0.5", "pop", {"f": 600}),
    ("b7+0.5", "riser", {"dur": 1.5}),
    ("b8+0.5", "bell_low"),
    ("b9+0.5", "whoosh"),
    ("b10+0.5", "sparkle"),
    ("b11+1.0", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
HERO = {
    "skin": "light",
    "hair": {"style": "spikyAnime", "color": "blue"},
    "top": {"style": "hoodie", "color": "royal", "secondary": "white"},
    "bottom": {"style": "jeans", "color": "denim"},
    "shoes": {"color": "white", "sole": "white"},
    "freckles": True,
}
CAST = {
    "hero": HERO,
    "friend": {"extends": "kid_girl", "hair": {"style": "ponytail", "color": "blonde"},
               "top": {"style": "hoodie", "color": "pink", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"color": "white", "sole": "white"}},
    "mom": {"extends": "real_mom", "hair": {"style": "ponytail", "color": "brown"}},
    # White blouse on purpose (sun_off teal was a fix for that video). She stands
    # BESIDE the desk at x -3.0, not on it - verify in the stills.
    "teacher": {"extends": "teacher_woman", "skin": "fair", "hair": {"style": "bun", "color": "blonde"}},
}


def _streaks(a, b):
    """Radial warp streaks (from _test_week1_props.py): 12 thin boxes around
    frame centre [0, 7, -18], each rotated to point outward and keyframed to
    fly outward over the shot, so a still reads as light-speed lines
    radiating from the centre. The centre sits high in the sky so no streak
    lies flat across the horizon behind the actors."""
    out = []
    for i in range(12):
        ang = i * (2 * math.pi / 12) + 0.13
        if abs(math.cos(ang)) < 0.35:
            continue  # skip near-horizontal streaks: they lie flat across the
            # horizon behind the actors and read as stray bars, not warp
        dx, dy = math.sin(ang), math.cos(ang)
        r0 = 3.5 + (i % 4) * 1.5
        length = 5.0 + (i % 3) * 1.5
        cx, cy = dx * r0, 7 + dy * r0
        ex, ey = dx * (r0 + 5), 7 + dy * (r0 + 5)
        out.append({"id": f"streak{i}", "shape": "box", "size": [0.35, length, 0.35],
                    "color": "#F8FAFC", "emissive": "#FFFFFF", "emissiveIntensity": 1.6,
                    "roughness": 0.4, "rotation": [0, 0, ang],
                    "keyframes": [{"frame": a, "position": [cx, cy, -18]},
                                  {"frame": b, "position": [ex, ey, -18]}]})
    return out


def _ship(a, b):
    """Blocky spaceship (from _test_week2_5_props2.py): white fuselage,
    faceted glowing nose, blue cockpit, swept wings with orange trailing
    edges, orange tail fin, two glowing blue engines. Flies toward the
    camera over the shot (z -8 -> -4). Every part tracks the same two
    keyframes so the ship moves as one piece."""
    parts = [
        {"id": "ship-body", "shape": "box", "size": [2.6, 2.0, 7.0],
         "color": "#F8FAFC", "roughness": 0.35, "off": [0, 0, 0]},
        {"id": "ship-nose", "shape": "facet", "radius": 0.9, "detail": 1,
         "color": "#E0F2FE", "emissive": "#7DD3FC", "emissiveIntensity": 0.5,
         "roughness": 0.3, "off": [0, 0, 3.7]},
        {"id": "ship-cockpit", "shape": "box", "size": [1.4, 0.6, 2.5],
         "color": "#0EA5E9", "emissive": "#38BDF8", "emissiveIntensity": 0.8,
         "roughness": 0.3, "off": [0, 1.1, 1.8]},
        {"id": "ship-wing-l", "shape": "box", "size": [4.5, 0.3, 2.2],
         "color": "#F8FAFC", "roughness": 0.35, "off": [-3.2, -0.4, -1.5],
         "rotation": [0, -0.35, -0.12]},
        {"id": "ship-wing-r", "shape": "box", "size": [4.5, 0.3, 2.2],
         "color": "#F8FAFC", "roughness": 0.35, "off": [3.2, -0.4, -1.5],
         "rotation": [0, 0.35, 0.12]},
        {"id": "ship-edge-l", "shape": "box", "size": [4.5, 0.32, 0.6],
         "color": "#F97316", "emissive": "#FB923C", "emissiveIntensity": 0.6,
         "roughness": 0.4, "off": [-3.2, -0.4, -2.4], "rotation": [0, -0.35, -0.12]},
        {"id": "ship-edge-r", "shape": "box", "size": [4.5, 0.32, 0.6],
         "color": "#F97316", "emissive": "#FB923C", "emissiveIntensity": 0.6,
         "roughness": 0.4, "off": [3.2, -0.4, -2.4], "rotation": [0, 0.35, 0.12]},
        {"id": "ship-fin", "shape": "box", "size": [0.3, 2.2, 2.0],
         "color": "#F97316", "emissive": "#FB923C", "emissiveIntensity": 0.4,
         "roughness": 0.4, "off": [0, 1.8, -2.8], "rotation": [0.2, 0, 0]},
        {"id": "ship-eng-l", "shape": "box", "size": [1.2, 1.2, 1.0],
         "color": "#1E293B", "emissive": "#38BDF8", "emissiveIntensity": 2.0,
         "roughness": 0.3, "off": [-1.1, 0, -3.6]},
        {"id": "ship-eng-r", "shape": "box", "size": [1.2, 1.2, 1.0],
         "color": "#1E293B", "emissive": "#38BDF8", "emissiveIntensity": 2.0,
         "roughness": 0.3, "off": [1.1, 0, -3.6]},
        {"id": "ship-flame-l", "shape": "sphere", "radius": 0.9,
         "color": "#7DD3FC", "emissive": "#38BDF8", "emissiveIntensity": 2.5,
         "roughness": 0.3, "opacity": 0.7, "off": [-1.1, 0, -4.4]},
        {"id": "ship-flame-r", "shape": "sphere", "radius": 0.9,
         "color": "#7DD3FC", "emissive": "#38BDF8", "emissiveIntensity": 2.5,
         "roughness": 0.3, "opacity": 0.7, "off": [1.1, 0, -4.4]},
    ]
    out = []
    for part in parts:
        off = part.pop("off")
        out.append({**part,
                    "keyframes": [{"frame": a, "position": [off[0], 7 + off[1], -8 + off[2]]},
                                  {"frame": b, "position": [off[0], 7 + off[1], -4 + off[2]]}]})
    return out


# 4. SCENES ---------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S2 = B["b2"] - 1    # space: the warp, time slows
    S3 = B["b6"] - 1    # classroom: the energy wall
    S4 = B["b9"] - 1    # space: the speed limit
    S5 = B["b11"] - 1   # living room (yellow), night: closer

    HERO_P, FRIEND_P = [-3, 0, 0.5], [2.5, 0, 0.5]

    scenes = []

    # 1. HOOK - space: the ship warps past, streaks radiating --------------------------
    # Three-quarter framing on the ship (camera off to the side) so the nose
    # reads as a nose, not a ball; the streak field sits high in the sky.
    scenes.append({
        "id": "hook", "location": "space", "skyColor": "#000000",
        "startFrame": 0, "endFrame": S2,
        "cameraShots": [static_shot(0, S2 // 2, [10, 8, 10], [0, 7, -6], 58),
                        static_shot(S2 // 2, S2, [12, 9, 6], [0, 7, -6], 58)],
        "fx": _ship(0, S2) + _streaks(0, S2),
        "characters": {
            "hero": hold(0, S2, HERO_P, 0.2, "point", "shocked"),
            "friend": hold(0, S2, FRIEND_P, -0.2, "idle", "shocked"),
        },
    })

    # 2. SPACE - the warp: looking up at the streak field, time slows ---------------------
    scenes.append({
        "id": "warp", "location": "space", "skyColor": "#000000",
        "startFrame": S2, "endFrame": S3,
        "cameraShots": cover(S2, S3, [lambda a, b: shot(a, b, [0, 2, 18], [0, 2.5, 16], [0, 14, -10], [0, 15, -10], 58),
                                       lambda a, b: low_angle(a, b, HERO_P, dist=9, eye_height=1.2),
                                       lambda a, b: close_up(a, b, FRIEND_P)]),
        "fx": _ship(S2, S3) + _streaks(S2, S3),
        "characters": {
            "hero": hold(S2, S3, HERO_P, 0.2, "point", "shocked"),
            "friend": hold(S2, S3, FRIEND_P, -0.2, "idle", "shocked"),
        },
    })

    # 3. CLASSROOM - the energy wall -----------------------------------------------------------
    scenes.append({
        "id": "mechanism", "location": "classroom",
        "boardText": ["LIGHT: 300,000 km/s", "FASTER = SLOWER TIME", "LIGHT SPEED = INFINITE ENERGY"],
        "startFrame": S3, "endFrame": S4,
        "cameraShots": cover(S3, S4, [lambda a, b: shot(a, b, [0, 7.4, 23], [0, 7.0, 20.5], [0, 4.8, -1], [0, 4.7, -1], 58),
                                       lambda a, b: close_up(a, b, [-0.5, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [-3.0, 0, -4.5])]),
        "characters": {
            "teacher": hold(S3, S4, [-3.0, 0, -4.5], 0.5, "point", "deadpan", "pointer"),
            "hero": hold(S3, S4, [-0.5, 0, 0.5], 0, "idle", "smile"),
            "friend": hold(S3, S4, [4.0, 0, 0.5], 0, "idle", "smile"),
        },
    })

    # 4. SPACE - the speed limit: the ship from the side ----------------------------------------
    scenes.append({
        "id": "limit", "location": "space", "skyColor": "#000000",
        "startFrame": S4, "endFrame": S5,
        "cameraShots": cover(S4, S5, [lambda a, b: static_shot(a, b, [14, 7, -2], [0, 7, -6], 58),
                                       lambda a, b: close_up(a, b, HERO_P),
                                       lambda a, b: shot(a, b, [0, 2, 18], [0, 2.5, 16], [0, 14, -10], [0, 15, -10], 58)]),
        "fx": _ship(S4, S5) + _streaks(S4, S5),
        "characters": {
            "hero": hold(S4, S5, HERO_P, 0.2, "point", "shocked"),
            "friend": hold(S4, S5, FRIEND_P, -0.2, "idle", "shocked"),
        },
    })

    # 5. LIVING ROOM (yellow), NIGHT - closer --------------------------------------------------------
    scenes.append({
        "id": "closer", "location": "living_room", "variant": "yellow", "isNight": True,
        "startFrame": S5, "endFrame": END,
        "cameraShots": cover(S5, END, [lambda a, b: wide(a, b, [0, 0, 0.4], 24),
                                         lambda a, b: close_up(a, b, [-4.0, 0, 0.4]),
                                         lambda a, b: close_up(a, b, [4.0, 0, 0.4])]),
        "characters": {
            "hero": [kf(S5, [-4.0, 0, 0.4], 0.9, "idle", "deadpan"),
                     kf(B["b11"], [-4.0, 0, 0.4], 0.9, "idle", "smile"),
                     kf(END, [-4.0, 0, 0.4], 0.9, "idle", "smile")],
            "mom": [kf(S5, [4.0, 0, 0.4], -0.9, "wave", "smile"),
                    kf(END, [4.0, 0, 0.4], -0.9, "wave", "smile")],
        },
    })

    return scenes
