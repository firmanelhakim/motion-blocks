"""WHAT IF YOU FELL INTO THE SUN? - science explainer.

Week 1 storyboard (the maintainer, 2026-11-17): video 4 of 7.
Structure: hook (falling toward the giant Sun) -> space fall (the heat) ->
classroom mechanism (the numbers) -> space (the brightness) -> closer.
No shouts, hot and bright mood.

The science: the Sun's surface is about 5,500 degrees Celsius — hotter
than any oven, hotter than lava — and you would burn up long before
touching it. The Sun is so big that 1.3 million Earths could fit inside it,
and it holds almost all the mass in the solar system. It is not on fire: it
is a ball of gas squeezed so hard it glows (fusion), with a core around 15
million degrees. Its light is bright enough to blind you. All
plain-language, standard figures, simplified for a Short.

This is NOT sun_off: sun_off was about the light going out and the 8-minute
delay; this one is about falling in and the heat. The 8-minute light time
appears only as a board number, never as a beat.

Fresh visuals: a BIGGER Sun fx (radius 8, vs sun_off's 5), the hero
falling through space toward it, an orbit camera around the Sun, new music
(fall-into-sun.wav). The teacher is in the standard white blouse, placed
beside the desk at x -3.0 (not on it).

Build:   python scripts/make_short.py stories/fall_into_sun.py --stills
Render:  python scripts/make_short.py stories/fall_into_sun.py --skip-tts --render
"""
import math  # noqa: F401

from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, orbit, shot, split_shots, static_shot, wide  # noqa: F401

TITLE = "WHAT IF YOU FELL INTO THE SUN?"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this world, you are falling into the Sun. And you have a problem: it is very, very hot.", "pause": 0.08},
    {"id": "b2", "text": "The Sun's surface is about 5,500 degrees. Hotter than any oven, hotter than lava.", "pause": 0.10},
    {"id": "b3", "text": "You would not even reach it. The heat would cook you long before you touched the surface.", "pause": 0.10},
    {"id": "b4", "text": "First your spacesuit would melt. The heat stops you long before you ever touch the surface.", "pause": 0.08},
    {"id": "b5", "text": "And the Sun is huge. 1.3 million Earths could fit inside it.", "pause": 0.10},
    {"id": "b5b", "text": "It holds almost all the mass in the whole solar system. The planets are just crumbs around it.", "pause": 0.08},
    {"id": "b6", "text": "If the Sun were a beach ball, the Earth would be a grain of sand next to it.", "pause": 0.10},
    {"id": "b7", "text": "The Sun is not on fire, by the way. It is a giant ball of gas, squeezed so hard it glows.", "pause": 0.10},
    {"id": "b8", "text": "Deep inside, it is even hotter — about 15 million degrees. That heat is what makes the light.", "pause": 0.10},
    {"id": "b8b", "text": "That heat travels 150 million kilometres to reach us — and it still warms your face on a sunny day.", "pause": 0.08},
    {"id": "b9", "text": "That light is so bright it would blind you in a second. Sunglasses would not help.", "pause": 0.10},
    {"id": "b10", "text": "So falling into the Sun is the worst fall in the solar system. Hot, bright, and way too big.", "pause": 0.10},
    {"id": "b11", "text": "Lucky for us, gravity keeps us at a safe distance. About 150 million kilometres away.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/fall-into-sun.wav",
    "under_voice": 0.022,
    "gaps": 0.05,
}

SFX = [
    ("b1", "whoosh"),
    ("b1+0.5", "sparkle"),
    ("b2+0.5", "bell_low"),
    ("b3+0.5", "pop", {"f": 600}),
    ("b5+0.5", "pop", {"f": 600}),
    ("b6+0.5", "sparkle"),
    ("b7+0.5", "pop", {"f": 600}),
    ("b8+0.5", "riser", {"dur": 1.5}),
    ("b9+0.5", "whoosh"),
    ("b10+0.5", "sad"),
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


def _big_sun(a, b):
    """A BIG Sun: radius 8 (sun_off's was 5), pale yellow with a hot orange
    emissive core, hanging in space at [0, 12, -25] so it fills the sky
    behind the falling hero."""
    return [{"id": "sun", "shape": "sphere", "radius": 8.0, "color": "#FCD34D",
             "emissive": "#F59E0B", "emissiveIntensity": 1.5, "roughness": 0.6,
             "keyframes": [{"frame": a, "position": [0, 12, -25]}, {"frame": b, "position": [0, 12, -25]}]}]


# 4. SCENES ---------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S2 = B["b2"] - 1    # space: the fall, the heat
    S3 = B["b5"] - 1    # classroom: the numbers
    S4 = B["b9"] - 1    # space: the brightness
    S5 = B["b11"] - 1   # living room (red), night: closer

    scenes = []

    # 1. HOOK - space: the hero falls toward the giant Sun --------------------------------
    scenes.append({
        "id": "hook", "location": "space", "skyColor": "#000000",
        "startFrame": 0, "endFrame": S2,
        "cameraShots": [static_shot(0, S2 // 2, [0, 8, 8], [0, 6, -10], 58),
                        orbit(S2 // 2, S2, [0, 12, -25], 36, 12, -0.4, 0.1, [0, 12, -25], 58)],
        "fx": _big_sun(0, S2),
        "characters": {
            "hero": [kf(0, [0, 8, -5], 0, "idle", "panic"),
                     kf(S2, [0, 6, -8], 0, "idle", "panic")],
        },
    })

    # 2. SPACE - falling closer, the heat ----------------------------------------------------
    scenes.append({
        "id": "fall", "location": "space", "skyColor": "#000000",
        "startFrame": S2, "endFrame": S3,
        "cameraShots": cover(S2, S3, [lambda a, b: static_shot(a, b, [0, 7, 6], [0, 5, -12], 58),
                                       lambda a, b: low_angle(a, b, [0, 5, -9], dist=9, eye_height=1.2),
                                       lambda a, b: orbit(a, b, [0, 12, -25], 36, 11, 0.2, 1.0, [0, 12, -25], 58)]),
        "fx": _big_sun(S2, S3),
        "characters": {
            "hero": [kf(S2, [0, 6, -8], 0, "idle", "panic"),
                     kf(B["b4"], [0, 4, -10], 0, "idle", "panic"),
                     kf(S3, [0, 4, -10], 0, "idle", "panic")],
        },
    })

    # 3. CLASSROOM - the numbers ---------------------------------------------------------------
    scenes.append({
        "id": "mechanism", "location": "classroom",
        "boardText": ["SURFACE: 5,500°C", "CORE: 15,000,000°C", "1.3 MILLION EARTHS FIT"],
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

    # 4. SPACE - the brightness ------------------------------------------------------------------
    scenes.append({
        "id": "bright", "location": "space", "skyColor": "#000000",
        "startFrame": S4, "endFrame": S5,
        "cameraShots": cover(S4, S5, [lambda a, b: static_shot(a, b, [0, 7, 6], [0, 5, -12], 58),
                                       lambda a, b: low_angle(a, b, [0, 4, -10], dist=9, eye_height=1.2),
                                       lambda a, b: orbit(a, b, [0, 12, -25], 36, 11, -0.3, 0.5, [0, 12, -25], 58)]),
        "fx": _big_sun(S4, S5),
        "characters": {
            "hero": [kf(S4, [0, 4, -10], 0, "idle", "shocked"),
                     kf(B["b10"], [0, 4, -10], 0, "idle", "shocked"),
                     kf(S5, [0, 4, -10], 0, "idle", "shocked")],
        },
    })

    # 5. LIVING ROOM (red), NIGHT - closer -----------------------------------------------------------
    scenes.append({
        "id": "closer", "location": "living_room", "variant": "red", "isNight": True,
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
