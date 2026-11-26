"""WHAT IF EARTH HAD TWO MOONS? - science explainer.

Week 1 storyboard (the maintainer, 2026-11-17): video 1 of 7.
Structure: hook (two moons over the town) -> beach demo (the tide swings
further) -> classroom mechanism -> schoolyard consequence (the wobble) ->
street night (two moons, bright night) -> closer. No shouts, calm tide mood.

The science: one Moon already pulls the oceans and makes the tides; a
second Moon would add a second pull, so high tide climbs higher and low
tide drops lower. Two moons also mean brighter nights. And the Moon
steadies Earth's tilt like a hand on a spinning top — two moons pulling in
two directions would wobble it more, so the seasons drift. All
plain-language, standard figures, simplified for a Short.

Fresh visuals: TWO Moon fx in the sky at once (different sizes/heights),
tide fx that RISES toward the beach (the opposite of moon_off's retreat),
an Earth globe fx with a wider wobble drift, new music (two-moons.wav).
The teacher is in the standard white blouse, placed beside the desk at
x -3.0 (not on it) - check the stills for the sun_off blending problem.

Build:   python scripts/make_short.py stories/two_moons.py --stills
Render:  python scripts/make_short.py stories/two_moons.py --skip-tts --render
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, split_shots, wide  # noqa: F401

TITLE = "WHAT IF EARTH HAD TWO MOONS?"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this world, Earth has two moons. And the sea can feel both of them pulling.", "pause": 0.08},
    {"id": "b2", "text": "One Moon already drags the oceans toward it. That pull is what makes the tides.", "pause": 0.08},
    {"id": "b3", "text": "Now add a second Moon. Two pulls at once — and the tides grow taller.", "pause": 0.10},
    {"id": "b4", "text": "High tide climbs further up the beach. Low tide drops further down. Twice the pull, twice the swing.", "pause": 0.10},
    {"id": "b4b", "text": "The water reaches places it never reached before. The beach shrinks.", "pause": 0.08},
    {"id": "b4c", "text": "And when the two moons line up in the sky, their pulls add together — the biggest tides of all.", "pause": 0.10},
    {"id": "b5", "text": "The nights change too. Two moons in the sky means the night never gets properly dark.", "pause": 0.10},
    {"id": "b5b", "text": "Moonlight on the sand, all night long. You could read a book outside at midnight.", "pause": 0.08},
    {"id": "b6", "text": "And the Moon does one more quiet job. It holds the Earth steady, like a hand on a spinning top.", "pause": 0.10},
    {"id": "b7", "text": "But two moons pull in two directions. The Earth wobbles more — and the seasons drift.", "pause": 0.10},
    {"id": "b7b", "text": "The wobble is slow. It takes thousands of years — but the seasons never sit still.", "pause": 0.10},
    {"id": "b8", "text": "Summers that come too early. Winters that stay too long. The calendar stops lining up.", "pause": 0.10},
    {"id": "b8b", "text": "Two moons, two shadows. Every step you take, the night follows you twice.", "pause": 0.08},
    {"id": "b9", "text": "So tonight, look up. One Moon pulls the sea. Two moons would pull it even harder.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/two-moons.wav",
    "under_voice": 0.022,
    "gaps": 0.05,
}

SFX = [
    ("b1", "whoosh"),
    ("b1+0.5", "sparkle"),
    ("b3+0.5", "swish"),
    ("b4+0.5", "swish"),
    ("b4c+0.5", "pop", {"f": 600}),
    ("b5+0.5", "pop", {"f": 600}),
    ("b5b+0.5", "sparkle"),
    ("b6+0.5", "pop", {"f": 600}),
    ("b7", "riser", {"dur": 1.5}),
    ("b7b+0.5", "pop", {"f": 600}),
    ("b8b+0.5", "sparkle"),
    ("b9+1.5", "twist"),
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


def _two_moons(a, b, low=False):
    """Two moons in the sky at once: the big one (r=4.0, with craters) high
    right, the smaller one (r=2.5, with craters) high left. Both track the
    same two keyframes so they drift together as the shot runs. low=True
    brings both moons lower and nearer the centre, so they read from street
    level (from the ground the high moons sit above the frame)."""
    fx = []
    if low:
        big_pos, small_pos = [4, 22, -14], [-7, 18, -16]
    else:
        big_pos, small_pos = [10, 38, -10], [-8, 30, -12]
    big_kf = [{"frame": a, "position": big_pos},
              {"frame": b, "position": [big_pos[0] + 2, big_pos[1] + 1, big_pos[2]]}]
    fx.append({"id": "moon1", "shape": "sphere", "radius": 4.0, "color": "#F1F5F9",
               "emissive": "#CBD5E1", "emissiveIntensity": 0.7, "roughness": 0.9,
               "keyframes": big_kf})
    for i, (ox, oy, oz, r) in enumerate([
            (1.5, 1.0, 2.8, 0.9), (-1.2, 2.0, 2.5, 0.7), (2.6, -0.8, 1.8, 0.8),
            (0.2, 3.2, 0.8, 0.6), (-2.6, -0.5, 2.0, 0.8), (0.8, -2.2, 2.4, 0.7)]):
        fx.append({"id": f"crater1-{i}", "shape": "sphere", "radius": r, "color": "#94A3B8",
                   "emissive": "#64748B", "emissiveIntensity": 0.25, "roughness": 0.9,
                   "keyframes": [{"frame": k["frame"],
                                 "position": [k["position"][0] + ox, k["position"][1] + oy, k["position"][2] + oz]}
                                for k in big_kf]})
    small_kf = [{"frame": a, "position": small_pos},
                {"frame": b, "position": [small_pos[0] + 2, small_pos[1] + 1, small_pos[2]]}]
    fx.append({"id": "moon2", "shape": "sphere", "radius": 2.5, "color": "#E2E8F0",
               "emissive": "#CBD5E1", "emissiveIntensity": 0.6, "roughness": 0.9,
               "keyframes": small_kf})
    for i, (ox, oy, oz, r) in enumerate([(1.0, 0.6, 1.7, 0.6), (-0.8, 1.2, 1.5, 0.5), (0.3, -1.0, 1.6, 0.55)]):
        fx.append({"id": f"crater2-{i}", "shape": "sphere", "radius": r, "color": "#94A3B8",
                   "emissive": "#64748B", "emissiveIntensity": 0.25, "roughness": 0.9,
                   "keyframes": [{"frame": k["frame"],
                                 "position": [k["position"][0] + ox, k["position"][1] + oy, k["position"][2] + oz]}
                                for k in small_kf]})
    return fx


# 4. SCENES ---------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S2 = B["b2"] - 1    # beach, night: the tide swings further
    S3 = B["b5"] - 1    # classroom: two pulls, brighter nights
    S4 = B["b6"] - 1    # schoolyard, day: the wobble
    S5 = B["b8"] - 1    # street, night: two moons, bright night
    S6 = B["b9"] - 1    # living room (green), night: closer

    scenes = []

    # 1. HOOK - aerial town, night, TWO moons in the sky ---------------------------
    scenes.append({
        "id": "hook", "location": "town_overview", "isNight": True,
        "startFrame": 0, "endFrame": S2,
        "cameraShots": [shot(0, S2 // 3, [-10, 62, 74], [-7, 56, 67], [8, 0, -6], [7, 1, -7], 55),
                        shot(S2 // 3, 2 * S2 // 3, [-7, 56, 67], [-4, 50, 61], [7, 1, -7], [6, 2, -8], 55),
                        shot(2 * S2 // 3, S2, [-4, 50, 61], [-2, 46, 56], [6, 2, -8], [6, 2, -8], 55)],
        "fx": _two_moons(0, S2),
        "characters": {},
    })

    # 2. BEACH, NIGHT - the tide rises toward the beach ----------------------------
    # Opposite of moon_off: the tide fx slides TOWARD the shore and rises as
    # the scene runs, so the water visibly climbs the sand.
    scenes.append({
        "id": "tide", "location": "beach", "isNight": True,
        "startFrame": S2, "endFrame": S3,
        "cameraShots": cover(S2, S3, [lambda a, b: wide(a, b, [0, 0, 0.5], 24),
                                       lambda a, b: close_up(a, b, [-4, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [1, 0, 0.5])]),
        "fx": [
            {"id": "tide", "shape": "box", "size": [40, 0.8, 10], "color": "#0EA5E9",
             "emissive": "#1D4ED8", "emissiveIntensity": 0.4, "roughness": 0.25, "opacity": 0.85,
             "keyframes": [{"frame": S2, "position": [0, 0.1, -15]}, {"frame": S3, "position": [0, 0.5, -8]}]},
        ],
        "characters": {
            "hero": [kf(S2, [-4, 0, 0.5], 0.2, "point", "shocked"),
                     kf(B["b4b"], [-4, 0, 0.5], 0.2, "idle", "shocked"),
                     kf(S3, [-4, 0, 0.5], 0.2, "idle", "shocked")],
            "friend": hold(S2, S3, [1, 0, 0.5], -0.2, "idle", "shocked"),
        },
    })

    # 3. CLASSROOM - two pulls, brighter nights --------------------------------------
    scenes.append({
        "id": "mechanism", "location": "classroom",
        "boardText": ["TWO MOONS = BIGGER TIDES", "NIGHTS BRIGHTER", "TILT WOBBLES MORE"],
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

    # 4. SCHOOLYARD, DAY - the Earth wobbles more ---------------------------------------
    # The globe fx drifts further side to side than moon_off's (x -8..2): the
    # wobble is bigger with two moons pulling. Green continent patches ride
    # on its front face and track its keyframes exactly.
    mid = (S4 + S5) // 2
    globe_kf = [{"frame": S4, "position": [-8, 16, -12]}, {"frame": mid, "position": [2, 16.5, -12]},
                {"frame": S5, "position": [-8, 16, -12]}]
    globe_fx = [{"id": "earth", "shape": "sphere", "radius": 3.0, "color": "#38BDF8",
                 "emissive": "#1D4ED8", "emissiveIntensity": 0.4, "roughness": 0.7,
                 "keyframes": globe_kf}]
    for i, (ox, oy, oz, r) in enumerate([
            (1.0, 0.7, 1.9, 1.2), (-1.2, 1.0, 1.7, 1.0), (0.2, -1.0, 2.1, 1.3),
            (-0.5, 1.7, 1.4, 0.9)]):
        globe_fx.append({"id": f"continent{i}", "shape": "sphere", "radius": r, "color": "#22C55E",
                         "emissive": "#16A34A", "emissiveIntensity": 0.25, "roughness": 0.8,
                         "keyframes": [{"frame": k["frame"],
                                       "position": [k["position"][0] + ox, k["position"][1] + oy, k["position"][2] + oz]}
                                      for k in globe_kf]})
    scenes.append({
        "id": "wobble", "location": "school_exterior",
        "startFrame": S4, "endFrame": S5,
        "cameraShots": cover(S4, S5, [lambda a, b: wide(a, b, [0, 0, 0], 24),
                                       lambda a, b: close_up(a, b, [-2.5, 0, 0]),
                                       lambda a, b: close_up(a, b, [2.5, 0, 0])]),
        "fx": globe_fx,
        "characters": {
            "hero": hold(S4, S5, [-2.5, 0, 0], 0.2, "point", "shocked"),
            "friend": hold(S4, S5, [2.5, 0, 0], -0.2, "idle", "shocked"),
        },
    })

    # 5. STREET, NIGHT - two moons over the street, bright night -------------------------
    scenes.append({
        "id": "brightnight", "location": "street", "isNight": True,
        "startFrame": S5, "endFrame": S6,
        "cameraShots": cover(S5, S6, [lambda a, b: wide(a, b, [0, 0, 0.5], 24),
                                       lambda a, b: close_up(a, b, [-2.5, 0, 0.5]),
                                       lambda a, b: shot(a, b, [0, 4, 21], [0, 4.5, 19], [0, 16, -10], [0, 17, -10], 62)]),
        "fx": _two_moons(S5, S6, low=True),
        "characters": {
            "hero": hold(S5, S6, [-2.5, 0, 0.5], 0.2, "point", "shocked"),
            "friend": hold(S5, S6, [2.5, 0, 0.5], -0.2, "idle", "shocked"),
        },
    })

    # 6. LIVING ROOM (green), NIGHT - closer ------------------------------------------------
    scenes.append({
        "id": "closer", "location": "living_room", "variant": "green", "isNight": True,
        "startFrame": S6, "endFrame": END,
        "cameraShots": cover(S6, END, [lambda a, b: wide(a, b, [0, 0, 0.4], 24),
                                         lambda a, b: close_up(a, b, [-4.0, 0, 0.4]),
                                         lambda a, b: close_up(a, b, [4.0, 0, 0.4])]),
        "characters": {
            "hero": [kf(S6, [-4.0, 0, 0.4], 0.9, "idle", "deadpan"),
                     kf(B["b9"], [-4.0, 0, 0.4], 0.9, "idle", "smile"),
                     kf(END, [-4.0, 0, 0.4], 0.9, "idle", "smile")],
            "mom": [kf(S6, [4.0, 0, 0.4], -0.9, "wave", "smile"),
                    kf(END, [4.0, 0, 0.4], -0.9, "wave", "smile")],
        },
    })

    return scenes
