"""WHAT IF YOU LIVED ON MARS? - science explainer.

Week 1 storyboard (the maintainer, 2026-11-17): video 2 of 7.
Structure: hook (astronaut on the red desert) -> Mars demo (the air, the
cold, the dust) -> classroom mechanism (the numbers) -> Olympus Mons ->
Mars sunset closer. No shouts, dusty frontier mood.

The science: Mars air is too thin to breathe (mostly carbon dioxide, about
1% of Earth's pressure), so you wear a suit everywhere. It is freezing
cold, about minus 63 degrees on average. A day is 24 hours 37 minutes —
just a little longer than ours. The ground is red dust, and dust storms can
cover the whole planet. Olympus Mons is the tallest mountain in the solar
system, about 22 kilometres high — more than twice as tall as Mount
Everest. All plain-language, standard figures, simplified for a Short.

Fresh visuals: the Mars location (already built, refined to the Gemini
reference) + the astronaut cast (white suit, helmet) for the hero AND the
friend on Mars, new music (mars-life.wav). The classroom scene uses the
normal hero and friend looks (back on Earth, the teacher explaining) — the
suit is only worn on Mars. The teacher is in the standard white blouse,
placed beside the desk at x -3.0 (not on it).

Build:   python scripts/make_short.py stories/life_on_mars.py --stills
Render:  python scripts/make_short.py stories/life_on_mars.py --skip-tts --render
"""
import math  # noqa: F401

from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, shot, split_shots, wide  # noqa: F401

TITLE = "WHAT IF YOU LIVED ON MARS?"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this world, you live on Mars. And the first thing you learn is: never take off your helmet.", "pause": 0.08},
    {"id": "b2", "text": "The air on Mars is too thin to breathe. It is mostly carbon dioxide, and there is hardly any of it.", "pause": 0.10},
    {"id": "b3", "text": "So you wear a spacesuit everywhere. Even to go outside for five minutes.", "pause": 0.08},
    {"id": "b4", "text": "It is freezing cold, too. About minus 63 degrees — colder than the coldest winter on Earth.", "pause": 0.10},
    {"id": "b4b", "text": "Your breath would freeze in the air. The cold bites through every layer.", "pause": 0.08},
    {"id": "b5", "text": "But some things feel familiar. A day on Mars is 24 hours and 37 minutes — just a little longer than ours.", "pause": 0.10},
    {"id": "b6", "text": "And the ground under your feet is red dust. It gets everywhere. In your boots, in your gloves, in your lunch.", "pause": 0.08},
    {"id": "b7", "text": "The dust storms can cover the whole planet. For weeks, the sky turns orange.", "pause": 0.10},
    {"id": "b8", "text": "And then there is Olympus Mons. The tallest mountain in the whole solar system.", "pause": 0.10},
    {"id": "b9", "text": "It is 22 kilometres high — more than twice as tall as Mount Everest.", "pause": 0.10},
    {"id": "b9b", "text": "It is as wide as a whole country. You could walk for weeks and still be climbing.", "pause": 0.08},
    {"id": "b10", "text": "So living on Mars means suits, dust, and cold. But also a red sky, and a mountain taller than anything on Earth.", "pause": 0.10},
    {"id": "b11", "text": "Would you move to Mars? Pack warm — and bring a spare helmet.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/mars-life.wav",
    "under_voice": 0.022,
    "gaps": 0.05,
}

SFX = [
    ("b1", "whoosh"),
    ("b1+0.5", "sparkle"),
    ("b2+0.5", "pop", {"f": 600}),
    ("b4+0.5", "bell_low"),
    ("b4b+0.5", "pop", {"f": 600}),
    ("b5+0.5", "pop", {"f": 600}),
    ("b6+0.5", "swish"),
    ("b7+0.5", "whoosh"),
    ("b8+0.5", "riser", {"dur": 1.5}),
    ("b9b+0.5", "sparkle"),
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
    # White-suited astronaut (Gemini Mars reference): white pullover/pants,
    # no hair, white helmet with a dark visor (see Accessories.tsx 'helmet').
    # The hero wears the suit on Mars; the friend wears one too (pink accent
    # so the two astronauts stay easy to tell apart).
    "astronaut": {"extends": "kid_boy", "hair": {"style": "none"},
                  "top": {"style": "pullover", "color": "white", "secondary": "royal"},
                  "bottom": {"style": "pants", "color": "white"},
                  "shoes": {"color": "white", "sole": "white"},
                  "accessories": [{"type": "helmet", "color": "white", "secondary": "#0F172A"}]},
    "friend_astro": {"extends": "kid_girl", "hair": {"style": "none"},
                     "top": {"style": "pullover", "color": "white", "secondary": "pink"},
                     "bottom": {"style": "pants", "color": "white"},
                     "shoes": {"color": "white", "sole": "white"},
                     "accessories": [{"type": "helmet", "color": "white", "secondary": "#0F172A"}]},
    # White blouse on purpose (sun_off teal was a fix for that video). She stands
    # BESIDE the desk at x -3.0, not on it - verify in the stills.
    "teacher": {"extends": "teacher_woman", "skin": "fair", "hair": {"style": "bun", "color": "blonde"}},
}


# 4. SCENES ---------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S2 = B["b2"] - 1    # Mars: the air, the suit, the cold
    S3 = B["b5"] - 1    # classroom: the numbers
    S4 = B["b8"] - 1    # Mars: Olympus Mons
    S5 = B["b10"] - 1   # Mars sunset: closer

    HERO_P, FRIEND_P = [-3, 0, 0.5], [2.5, 0, 0.5]

    scenes = []

    # 1. HOOK - Mars wide: red desert, terraced mountains, pale square sun ---------
    scenes.append({
        "id": "hook", "location": "mars", "skyColor": "#FDBA74",
        "startFrame": 0, "endFrame": S2,
        "cameraShots": cover(0, S2, [lambda a, b: wide(a, b, [0, 0, 0.5], 29),
                                      lambda a, b: close_up(a, b, HERO_P),
                                      lambda a, b: low_angle(a, b, HERO_P, dist=13, eye_height=1.5)]),
        "characters": {
            "astronaut": hold(0, S2, HERO_P, 0.2, "idle", "shocked"),
            "friend_astro": hold(0, S2, FRIEND_P, -0.2, "point", "shocked"),
        },
    })

    # 2. MARS - the air is too thin, the suit stays on, it is freezing --------------
    scenes.append({
        "id": "air", "location": "mars", "skyColor": "#FDBA74",
        "startFrame": S2, "endFrame": S3,
        "cameraShots": cover(S2, S3, [lambda a, b: wide(a, b, [0, 0, 0.5], 29),
                                       lambda a, b: close_up(a, b, HERO_P),
                                       lambda a, b: medium(a, b, [0, 0, 0.5])]),
        "characters": {
            "astronaut": [kf(S2, HERO_P, 0.2, "point", "shocked"),
                          kf(B["b3"], HERO_P, 0.2, "idle", "shocked"),
                          kf(S3, HERO_P, 0.2, "idle", "shocked")],
            "friend_astro": hold(S2, S3, FRIEND_P, -0.2, "idle", "shocked"),
        },
    })

    # 3. CLASSROOM - the numbers -------------------------------------------------------
    scenes.append({
        "id": "mechanism", "location": "classroom",
        "boardText": ["DAY: 24h 37m", "COLD: -63°C", "AIR: TOO THIN", "OLYMPUS MONS: 22 km"],
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

    # 4. MARS - Olympus Mons, the tallest mountain in the solar system -------------------
    scenes.append({
        "id": "olympus", "location": "mars", "skyColor": "#FDBA74",
        "startFrame": S4, "endFrame": S5,
        "cameraShots": cover(S4, S5, [lambda a, b: wide(a, b, [0, 0, 0.5], 29),
                                       lambda a, b: low_angle(a, b, HERO_P, dist=13, eye_height=1.5),
                                       lambda a, b: close_up(a, b, FRIEND_P)]),
        "characters": {
            "astronaut": hold(S4, S5, HERO_P, 0.2, "point", "shocked"),
            "friend_astro": hold(S4, S5, FRIEND_P, -0.2, "idle", "shocked"),
        },
    })

    # 5. MARS SUNSET - closer ----------------------------------------------------------------
    scenes.append({
        "id": "closer", "location": "mars", "skyColor": "#FDBA74",
        "startFrame": S5, "endFrame": END,
        "cameraShots": cover(S5, END, [lambda a, b: wide(a, b, [0, 0, 0.5], 29),
                                        lambda a, b: close_up(a, b, HERO_P),
                                        lambda a, b: close_up(a, b, FRIEND_P)]),
        "characters": {
            "astronaut": [kf(S5, HERO_P, 0.2, "idle", "deadpan"),
                          kf(B["b11"], HERO_P, 0.2, "idle", "smile"),
                          kf(END, HERO_P, 0.2, "idle", "smile")],
            "friend_astro": [kf(S5, FRIEND_P, -0.2, "wave", "smile"),
                             kf(END, FRIEND_P, -0.2, "wave", "smile")],
        },
    })

    return scenes
