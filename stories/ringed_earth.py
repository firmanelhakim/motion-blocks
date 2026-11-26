"""WHAT IF EARTH HAD RINGS LIKE SATURN? - science explainer.

Week 1 storyboard (the maintainer, 2026-11-17): video 3 of 7.
Structure: hook (orbit around the ringed globe) -> space detail (what the
rings are made of) -> street (looking up at the band across the sky) ->
classroom mechanism (shadow + meteors) -> closer. No shouts, bright
shimmering mood.

The science: Saturn's rings are chunks of ice and rock, from dust-sized to
house-sized. Earth's rings would cross the whole sky as a bright band and
light up the night. They would also cast a giant shadow, cooling the
ground beneath it. And bits would fall out of the rings, burning up as
meteors — with the biggest chunks reaching the ground. All plain-language,
standard figures, simplified for a Short.

Fresh visuals: Earth globe fx + ring fx TOGETHER (a tilted torus around the
globe, tracked to its keyframes), an orbit camera circling the globe, a
giant ring arc across the sky over the street, new music (ringed-earth.wav).
The teacher is in the standard white blouse, placed beside the desk at
x -3.0 (not on it).

Build:   python scripts/make_short.py stories/ringed_earth.py --stills
Render:  python scripts/make_short.py stories/ringed_earth.py --skip-tts --render
"""
import math  # noqa: F401

from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, orbit, shot, split_shots, static_shot, wide  # noqa: F401

TITLE = "WHAT IF EARTH HAD RINGS LIKE SATURN?"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this world, Earth has rings. Like Saturn — a giant ring of ice and rock, circling the equator.", "pause": 0.08},
    {"id": "b2", "text": "The rings are made of chunks of ice and rock. Some as small as dust, some as big as houses.", "pause": 0.10},
    {"id": "b2b", "text": "The ice chunks bump into each other all the time, slowly — like bumper cars in slow motion.", "pause": 0.08},
    {"id": "b3", "text": "From the ground, the rings would cross the whole sky. A bright band, right over your head.", "pause": 0.10},
    {"id": "b3b", "text": "At sunset, the rings would glow orange and gold, like a bridge made of light.", "pause": 0.08},
    {"id": "b4", "text": "At night, they would light up the sky. Brighter than the Moon — you could read by ringlight.", "pause": 0.10},
    {"id": "b5", "text": "But the rings would also cast a shadow. A giant dark stripe, moving across the ground.", "pause": 0.10},
    {"id": "b5b", "text": "The shadow is so big you could see it from space — a dark stripe across the whole planet.", "pause": 0.08},
    {"id": "b6", "text": "Whole towns would sit in the ring's shadow for hours. Cooler days, in the middle of summer.", "pause": 0.10},
    {"id": "b6b", "text": "Farmers would have to learn the shadow's timetable, like a second sunset every day.", "pause": 0.08},
    {"id": "b7", "text": "And the rings would not stay up there forever. Bits of ice and rock would fall out of the sky.", "pause": 0.10},
    {"id": "b8", "text": "Most of them burn up as meteors. Bright streaks, every single night.", "pause": 0.08},
    {"id": "b8b", "text": "The biggest chunks would reach the ground. Space rocks, in your backyard.", "pause": 0.10},
    {"id": "b9", "text": "So Earth with rings would be beautiful — and a little bit dangerous.", "pause": 0.10},
    {"id": "b10", "text": "Would you look up every night? Or would you get used to the band across the sky?", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/ringed-earth.wav",
    "under_voice": 0.022,
    "gaps": 0.05,
}

SFX = [
    ("b1", "whoosh"),
    ("b1+0.5", "sparkle"),
    ("b2+0.5", "pop", {"f": 600}),
    ("b2b+0.5", "sparkle"),
    ("b3+0.5", "sparkle"),
    ("b4+0.5", "pop", {"f": 600}),
    ("b5+0.5", "bell_low"),
    ("b5b+0.5", "pop", {"f": 600}),
    ("b6+0.5", "pop", {"f": 600}),
    ("b7+0.5", "riser", {"dur": 1.5}),
    ("b8+0.5", "whoosh"),
    ("b9+0.5", "pop", {"f": 600}),
    ("b10+1.0", "twist"),
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


def _ringed_globe(a, b):
    """Earth globe + tilted ring around it (the black-hole ring pattern, but
    pale ice instead of glowing orange). The ring tracks the globe's
    keyframes exactly, so it stays centred on the globe as it drifts."""
    globe_kf = [{"frame": a, "position": [0, 14, -12]}, {"frame": b, "position": [2, 14.5, -12]}]
    fx = [{"id": "earth", "shape": "sphere", "radius": 3.0, "color": "#38BDF8",
           "emissive": "#1D4ED8", "emissiveIntensity": 0.4, "roughness": 0.7,
           "keyframes": globe_kf}]
    for i, (ox, oy, oz, r) in enumerate([
            (1.0, 0.7, 1.9, 1.2), (-1.2, 1.0, 1.7, 1.0), (0.2, -1.0, 2.1, 1.3),
            (-0.5, 1.7, 1.4, 0.9)]):
        fx.append({"id": f"continent{i}", "shape": "sphere", "radius": r, "color": "#22C55E",
                   "emissive": "#16A34A", "emissiveIntensity": 0.25, "roughness": 0.8,
                   "keyframes": [{"frame": k["frame"],
                                 "position": [k["position"][0] + ox, k["position"][1] + oy, k["position"][2] + oz]}
                                for k in globe_kf]})
    fx.append({"id": "ring", "shape": "ring", "radius": 4.6, "tube": 0.35,
               "color": "#E0F2FE", "emissive": "#BAE6FD", "emissiveIntensity": 0.9,
               "roughness": 0.4, "rotation": [0.45, 0, 0],
               "keyframes": globe_kf})
    return fx


def _sky_band(a, b):
    """The rings seen from the ground: a pale arc across the sky, high above
    the street. Same half-torus arc as the rainbow bands, but smaller and
    lower — the street camera is only ~35 studs away and the portrait
    horizontal half-FOV is ~17°, so a big arc sits outside the frame (round 0
    had radius 26 and was invisible). The look-up shot aims up at it."""
    return [{"id": "skyband", "shape": "ring", "radius": 12, "tube": 1.0, "arc": math.pi,
             "color": "#E0F2FE", "emissive": "#BAE6FD", "emissiveIntensity": 0.8,
             "roughness": 0.4, "rotation": [0.15, 0, 0],
             "keyframes": [{"frame": a, "position": [0, 11, -14]}, {"frame": b, "position": [0, 11, -14]}]}]


# 4. SCENES ---------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S2 = B["b2"] - 1    # space: what the rings are made of
    S3 = B["b4"] - 1    # street: looking up at the band
    S4 = B["b7"] - 1    # classroom: shadow + meteors
    S5 = B["b9"] - 1    # living room (white), night: closer

    scenes = []

    # 1. HOOK - space: orbit around the ringed globe --------------------------------
    scenes.append({
        "id": "hook", "location": "space", "skyColor": "#000000",
        "startFrame": 0, "endFrame": S2,
        "cameraShots": [orbit(0, S2 // 2, [0, 14, -12], 12, 14, -0.5, 0.2, [0, 14, -12], 58),
                        orbit(S2 // 2, S2, [0, 14, -12], 12, 14, 0.2, 0.9, [0, 14, -12], 58)],
        "fx": _ringed_globe(0, S2),
        "characters": {},
    })

    # 2. SPACE - the rings up close: ice chunks -----------------------------------------
    # A few faceted ice chunks float beside the globe, like the ring's
    # building blocks. Hero + friend float in space, looking at them.
    chunk_fx = _ringed_globe(S2, S3)
    for i, (cx, cy, cz, r) in enumerate([(-6, 18, -8, 0.9), (6, 11, -9, 1.1), (-3, 10, -7, 0.7), (8, 17, -10, 0.8)]):
        chunk_fx.append({"id": f"chunk{i}", "shape": "facet", "radius": r, "detail": 1,
                         "color": "#BAE6FD", "emissive": "#38BDF8", "emissiveIntensity": 0.8,
                         "roughness": 0.3,
                         "keyframes": [{"frame": S2, "position": [cx, cy, cz]}, {"frame": S3, "position": [cx, cy + 0.5, cz]}]})
    scenes.append({
        "id": "rings", "location": "space", "skyColor": "#000000",
        "startFrame": S2, "endFrame": S3,
        "cameraShots": cover(S2, S3, [lambda a, b: static_shot(a, b, [0, 12, 8], [0, 14, -12], 58),
                                       lambda a, b: orbit(a, b, [0, 14, -12], 10, 13, 0.3, 1.2, [0, 14, -12], 58),
                                       lambda a, b: close_up(a, b, [-3, 0, 0.5])]),
        "fx": chunk_fx,
        "characters": {
            "hero": hold(S2, S3, [-3, 0, 0.5], 0.2, "point", "shocked"),
            "friend": hold(S2, S3, [2.5, 0, 0.5], -0.2, "idle", "shocked"),
        },
    })

    # 3. STREET - looking up at the band across the sky -----------------------------------
    scenes.append({
        "id": "lookup", "location": "street", "isNight": True,
        "startFrame": S3, "endFrame": S4,
        "cameraShots": cover(S3, S4, [lambda a, b: shot(a, b, [0, 4, 21], [0, 4.5, 19], [0, 9, -10], [0, 10, -10], 62),
                                       lambda a, b: low_angle(a, b, [-2.5, 0, 0.5], dist=9, eye_height=1.2),
                                       lambda a, b: shot(a, b, [0, 5, 24], [0, 5, 22], [0, 14, -12], [0, 15, -12], 62)]),
        "fx": _sky_band(S3, S4),
        "characters": {
            "hero": hold(S3, S4, [-2.5, 0, 0.5], 0.2, "point", "shocked"),
            "friend": hold(S3, S4, [2.5, 0, 0.5], -0.2, "idle", "shocked"),
        },
    })

    # 4. CLASSROOM - the shadow and the falling bits -----------------------------------------
    scenes.append({
        "id": "mechanism", "location": "classroom",
        "boardText": ["RINGS: ICE + ROCK", "SHADOW: COOLER DAYS", "FALLING BITS = METEORS"],
        "startFrame": S4, "endFrame": S5,
        "cameraShots": cover(S4, S5, [lambda a, b: shot(a, b, [0, 7.4, 23], [0, 7.0, 20.5], [0, 4.8, -1], [0, 4.7, -1], 58),
                                       lambda a, b: close_up(a, b, [-0.5, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [-3.0, 0, -4.5])]),
        "characters": {
            "teacher": hold(S4, S5, [-3.0, 0, -4.5], 0.5, "point", "deadpan", "pointer"),
            "hero": hold(S4, S5, [-0.5, 0, 0.5], 0, "idle", "smile"),
            "friend": hold(S4, S5, [4.0, 0, 0.5], 0, "idle", "smile"),
        },
    })

    # 5. LIVING ROOM (white), NIGHT - closer ----------------------------------------------------
    scenes.append({
        "id": "closer", "location": "living_room", "variant": "white", "isNight": True,
        "startFrame": S5, "endFrame": END,
        "cameraShots": cover(S5, END, [lambda a, b: wide(a, b, [0, 0, 0.4], 24),
                                         lambda a, b: close_up(a, b, [-4.0, 0, 0.4]),
                                         lambda a, b: close_up(a, b, [4.0, 0, 0.4])]),
        "characters": {
            "hero": [kf(S5, [-4.0, 0, 0.4], 0.9, "idle", "deadpan"),
                     kf(B["b10"], [-4.0, 0, 0.4], 0.9, "idle", "smile"),
                     kf(END, [-4.0, 0, 0.4], 0.9, "idle", "smile")],
            "mom": [kf(S5, [4.0, 0, 0.4], -0.9, "wave", "smile"),
                    kf(END, [4.0, 0, 0.4], -0.9, "wave", "smile")],
        },
    })

    return scenes
