"""WHAT IF THE SUN SWITCHED OFF - science explainer.

the maintainer's pick: he said "surprise me" for the next topic (2026-11-17).
Chosen to force fresh visuals under the one-new-thing-per-video rule:
night exteriors (never used before), a Sun fx (new prop), a timeline
structure instead of v2's mechanism/examples/scale shape, no bully,
a new ambient music track, and a different living-room variant (green).

The science: light travels at ~300,000 km/s; the Sun is ~150 million km
away, so its light takes 8 minutes 20 seconds to reach us. We always see
the Sun as it was 8 minutes ago. If it switched off, the sky would stay
bright for 8 minutes, then go dark; the Moon goes dark too (it only
reflects sunlight); without solar heating the surface cools fast (winter
within days) and the oceans freeze over within about a year. Those two
timescales are the standard pop-science figures, simplified for a Short.
The sky darkening would take minutes as scattered light fades, not one
instant - the story says "eight minutes later, the light runs out", which
is the honest shape of it.

Build:   python scripts/make_short.py stories/sun_off.py --stills
Render:  python scripts/make_short.py stories/sun_off.py --skip-tts --render
         (SwiftShader path only -- the pod's --gl=angle-egl render of
          gravity v1 flickered and blackened the classroom.)

The Sun is a science fx (emissive sphere) in the hook scene only. Scene 2
is the same daylight street with NO Sun in the sky - the disc is gone but
the light has not caught up yet. That is the joke the narration explains.
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, split_shots, wide  # noqa: F401

TITLE = "WHAT IF THE SUN SWITCHED OFF"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this town, the Sun just switched off. And nobody noticed.", "pause": 0.08},
    {"id": "b2", "text": "That's because sunlight takes eight minutes to reach us.", "pause": 0.08},
    {"id": "b3", "text": "The Sun is 150 million kilometres away. So the light on your face right now left the Sun eight minutes ago.", "pause": 0.10},
    {"id": "b4", "text": "Light is the fastest thing there is. 300,000 kilometres every single second. And even light needs eight minutes to cross that gap.", "pause": 0.10},
    {"id": "b5", "text": "Eight minutes is longer than your whole lunch break. Light is fast. But space is big.", "pause": 0.08},
    {"id": "b5b", "text": "So you are always seeing the past. The Sun you see is the Sun as it was eight minutes ago.", "pause": 0.10},
    {"id": "b6", "text": "Eight minutes later, the light runs out. And the sky goes dark in the middle of the day.", "pause": 0.10},
    {"id": "b7", "text": "The stars come out. At noon.", "pause": 0.08},
    {"id": "b7b", "text": "The Moon goes dark too. It has no light of its own. It only borrows the Sun's.", "pause": 0.10},
    {"id": "b8", "text": "And then it gets cold. With no Sun, nothing warms the Earth. Within days, it's winter everywhere.", "pause": 0.10},
    {"id": "b8b", "text": "Plants stop making food. Animals huddle together. Everything waits for a sunrise that never comes.", "pause": 0.10},
    {"id": "b9", "text": "In one year, the oceans freeze over. And the Earth becomes a ball of ice, drifting through the dark.", "pause": 0.10},
    {"id": "b10", "text": "The Sun holds our light, our heat, and our weather in place.", "pause": 0.10},
    {"id": "b11", "text": "So next time you feel sunshine on your face, remember: it left the Sun eight minutes ago, just for you.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
# New ambient track (solar-drift.wav), not the fallen-down loop from v1/v2.
MUSIC = {
    "file": "music/solar-drift.wav",
    "under_voice": 0.022,
    "gaps": 0.05,
}

SFX = [
    ("b1", "whoosh"),
    ("b1+0.5", "sparkle"),
    ("b2+0.5", "pop", {"f": 600}),
    ("b3+1.0", "sparkle"),
    ("b4+0.5", "pop", {"f": 600}),
    ("b5b+0.5", "sparkle"),
    ("b6", "bell_low"),
    ("b6+0.8", "whoosh"),
    ("b7+0.5", "sparkle"),
    ("b7b+0.5", "pop_down"),
    ("b8+0.5", "sad"),
    ("b9", "riser", {"dur": 2.0}),
    ("b10+0.5", "sparkle"),
    ("b11+1.5", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
# Same hero/friend/teacher/mom as gravity v2, so the channel keeps one
# recognisable cast. No bully this time - the story does not need him.
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
    "teacher": {"extends": "teacher_woman", "skin": "fair", "hair": {"style": "bun", "color": "blonde"}, "top": {"style": "blouse", "color": "teal", "secondary": "cream"}},
}


# 4. SCENES ---------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S2 = B["b2"] - 1    # street, day: the Sun is gone from the sky, light not yet
    S3 = B["b4"] - 1    # classroom: the numbers (300,000 km/s, 150M km, 8 min)
    S4 = B["b6"] - 1    # street, night: the light runs out, stars at noon
    S5 = B["b8"] - 1    # playground, night: it gets cold
    S6 = B["b9"] - 1    # classroom, night: the scale on the board
    S7 = B["b10"] - 1   # living room (green), night: closer

    scenes = []

    # 1. HOOK - aerial town, day, the Sun blazing in the sky ----------------------
    scenes.append({
        "id": "hook", "location": "town_overview", "startFrame": 0, "endFrame": S2,
        "cameraShots": [shot(0, S2 // 2, [-10, 62, 74], [-6, 54, 65], [8, 0, -6], [7, 1, -7], 55),
                        shot(S2 // 2, S2, [-6, 54, 65], [-2, 46, 56], [7, 1, -7], [6, 2, -8], 55)],
        "fx": [
            {"id": "sun", "shape": "sphere", "radius": 5.0, "color": "#FCD34D",
             "emissive": "#FBBF24", "emissiveIntensity": 1.5, "roughness": 0.9,
             "keyframes": [{"frame": 0, "position": [5, 34, 5]}, {"frame": S2, "position": [8, 35, 5]}]},
        ],
        "characters": {},
    })

    # 2. STREET, DAY - the Sun is missing from the sky, but it is still bright ---
    # No fx here on purpose: the disc is gone, the light has not caught up yet.
    scenes.append({
        "id": "delay", "location": "street", "startFrame": S2, "endFrame": S3,
        "cameraShots": cover(S2, S3, [lambda a, b: wide(a, b, [0, 0, 0.5], 24),
                                       lambda a, b: close_up(a, b, [-4.5, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [0, 0, 0.5])]),
        "characters": {
            "hero": hold(S2, S3, [-4.5, 0, 0.5], 0.2, "point", "shocked"),
            "friend": hold(S2, S3, [0, 0, 0.5], -0.2, "idle", "shocked"),
        },
    })

    # 3. CLASSROOM, DAY - the numbers on the board --------------------------------
    scenes.append({
        "id": "numbers", "location": "classroom",
        "boardText": ["LIGHT: 300,000 km/s", "SUN: 150,000,000 km", "8 MINUTES"],
        "startFrame": S3, "endFrame": S4,
        "cameraShots": cover(S3, S4, [lambda a, b: shot(a, b, [0, 7.4, 20], [0, 7.0, 17.5], [0, 4.8, -1], [0, 4.7, -1], 58),
                                       lambda a, b: close_up(a, b, [-0.5, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [-3.0, 0, -4.5])]),
        "characters": {
            "teacher": hold(S3, S4, [-3.0, 0, -4.5], 0.5, "point", "deadpan", "pointer"),
            "hero": hold(S3, S4, [-0.5, 0, 0.5], 0, "idle", "smile"),
            "friend": hold(S3, S4, [4.5, 0, 0.5], 0, "idle", "smile"),
        },
    })

    # 4. STREET, NIGHT - the light runs out, stars at noon --------------------------
    scenes.append({
        "id": "darkness", "location": "street", "isNight": True,
        "startFrame": S4, "endFrame": S5,
        "cameraShots": cover(S4, S5, [lambda a, b: wide(a, b, [0, 0, 0.5], 24),
                                       lambda a, b: close_up(a, b, [-4.5, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [0, 0, 0.5])]),
        "characters": {
            "hero": hold(S4, S5, [-4.5, 0, 0.5], 0.2, "point", "shocked"),
            "friend": hold(S4, S5, [0, 0, 0.5], -0.2, "idle", "shocked"),
        },
    })

    # 5. PLAYGROUND, NIGHT - it gets cold --------------------------------------------
    scenes.append({
        "id": "cold", "location": "playground", "isNight": True,
        "startFrame": S5, "endFrame": S6,
        "cameraShots": cover(S5, S6, [lambda a, b: wide(a, b, [0, 0, 0], 24),
                                       lambda a, b: close_up(a, b, [-2.5, 0, 0]),
                                       lambda a, b: close_up(a, b, [2.5, 0, 0])]),
        "characters": {
            "hero": hold(S5, S6, [-2.5, 0, 0], 0.2, "panting", "shocked"),
            "friend": hold(S5, S6, [2.5, 0, 0], -0.2, "panting", "shocked"),
        },
    })

    # 6. CLASSROOM, NIGHT - the scale on the board --------------------------------------
    scenes.append({
        "id": "scale", "location": "classroom", "isNight": True,
        "boardText": ["1 YEAR: OCEANS FREEZE", "EARTH: BALL OF ICE"],
        "startFrame": S6, "endFrame": S7,
        "cameraShots": cover(S6, S7, [lambda a, b: shot(a, b, [0, 7.4, 20], [0, 7.0, 17.5], [0, 4.8, -1], [0, 4.7, -1], 58),
                                       lambda a, b: close_up(a, b, [-0.5, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [-3.0, 0, -4.5])]),
        "characters": {
            "teacher": hold(S6, S7, [-3.0, 0, -4.5], 0.5, "point", "deadpan", "pointer"),
            "hero": hold(S6, S7, [-0.5, 0, 0.5], 0, "idle", "deadpan"),
            "friend": hold(S6, S7, [4.5, 0, 0.5], 0, "idle", "deadpan"),
        },
    })

    # 7. LIVING ROOM (green), NIGHT - closer ----------------------------------------------
    scenes.append({
        "id": "closer", "location": "living_room", "variant": "green", "isNight": True,
        "startFrame": S7, "endFrame": END,
        "cameraShots": cover(S7, END, [lambda a, b: wide(a, b, [0, 0, 0.4], 24),
                                         lambda a, b: close_up(a, b, [-4.0, 0, 0.4]),
                                         lambda a, b: close_up(a, b, [4.0, 0, 0.4])]),
        "characters": {
            "hero": [kf(S7, [-4.0, 0, 0.4], 0.9, "idle", "deadpan"),
                     kf(B["b11"], [-4.0, 0, 0.4], 0.9, "idle", "smile"),
                     kf(END, [-4.0, 0, 0.4], 0.9, "idle", "smile")],
            "mom": [kf(S7, [4.0, 0, 0.4], -0.9, "wave", "smile"),
                    kf(END, [4.0, 0, 0.4], -0.9, "wave", "smile")],
        },
    })

    return scenes
