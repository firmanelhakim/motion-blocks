"""WHAT IF YOU FELL INTO A BLACK HOLE? - science explainer.

Batch of 5 storyboards (the maintainer, 2026-11-17): video 2 of 5.
Structure: hook (space, the hole) -> classroom mechanism (spaghettification)
-> space fall (the visual centrepiece) -> time freeze -> space (no way out)
-> living-room closer. No timeline shape, no beach, no classroom repeat.

The science: a black hole is what is left when a giant star collapses - all
its weight squeezed into a tiny point, gravity so strong nothing escapes,
not even light. The edge is the event horizon: past it, no return. Falling
in feet first, gravity pulls your feet much harder than your head, so you
stretch longer and thinner (spaghettification). Near the horizon time slows
down, so a far-away watcher sees you slow, freeze at the edge and fade -
you never seem to cross it. Inside, every path leads to the middle. All
plain-language, standard figures, simplified for a Short.

Fresh visuals: the new space location (starfield, Earth far behind), the
black hole fx (black sphere + glowing orange ring, new 'ring' ScienceFx
shape), the hero genuinely falling (y keyframes toward the hole), new music
(black-hole.wav). The teacher is in the standard white blouse, placed
beside the desk at x -3.0 - check the stills for the sun_off blending
problem and switch her to teal if it appears.

Build:   python scripts/make_short.py stories/black_hole.py --stills
Render:  python scripts/make_short.py stories/black_hole.py --skip-tts --render
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, split_shots, wide  # noqa: F401

TITLE = "WHAT IF YOU FELL INTO A BLACK HOLE?"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this world, there is a place where gravity is so strong, not even light can escape it.", "pause": 0.08},
    {"id": "b2", "text": "It is called a black hole. And today, you are going to fall into one.", "pause": 0.10},
    {"id": "b3", "text": "A black hole is what is left when a giant star collapses. All of its weight, squeezed into a tiny point.", "pause": 0.10},
    {"id": "b3b", "text": "Some are as heavy as ten Suns. The biggest ones weigh millions.", "pause": 0.08},
    {"id": "b4", "text": "Around it is the event horizon. Cross that line, and there is no coming back.", "pause": 0.10},
    {"id": "b5", "text": "You fall feet first. And here is the horrible part. Gravity pulls your feet much harder than your head.", "pause": 0.10},
    {"id": "b6", "text": "So your feet speed up while your head lags behind. You get stretched — longer, and thinner. Like spaghetti.", "pause": 0.10},
    {"id": "b7", "text": "But to someone watching from far away, you never fall in at all. Near the black hole, time itself slows down.", "pause": 0.10},
    {"id": "b8", "text": "They would see you slow down, freeze at the edge — and fade away. Frozen in time, forever.", "pause": 0.10},
    {"id": "b9", "text": "Inside, everything falls toward the middle. There is no way out, no way back, no way around.", "pause": 0.10},
    {"id": "b10", "text": "So a black hole is not a hole you fall through. It is a place where gravity wins — against everything, even light.", "pause": 0.10},
    {"id": "b11", "text": "The nearest black hole is thousands of light-years away. So you are safe. For now.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/black-hole.wav",
    "under_voice": 0.022,
    "gaps": 0.05,
}

SFX = [
    ("b1", "whoosh"),
    ("b1+0.5", "bell_low"),
    ("b2", "riser", {"dur": 1.5}),
    ("b4+0.5", "bell_low"),
    ("b5+0.5", "whoosh"),
    ("b6+0.5", "pop_down"),
    ("b7", "bell_low"),
    ("b8+0.5", "sad"),
    ("b10+0.5", "reveal"),
    ("b11+1.5", "twist"),
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

# The black hole: black sphere + glowing orange ring, same centre, static.
HOLE_FX = [
    {"id": "hole", "shape": "sphere", "radius": 3.0, "color": "#0F172A",
     "emissive": "#7C2D12", "emissiveIntensity": 0.3, "roughness": 0.9,
     "keyframes": []},  # keyframes filled per scene (same position, scene frames)
    {"id": "disc", "shape": "ring", "radius": 4.5, "color": "#FB923C",
     "emissive": "#F97316", "emissiveIntensity": 1.5, "roughness": 0.5,
     "keyframes": []},
]


def hole_fx(a, b):
    """Black hole fx with keyframes clamped to scene [a, b]."""
    out = []
    for f in HOLE_FX:
        g = dict(f)
        g["keyframes"] = [{"frame": a, "position": [0, 9, -14]}, {"frame": b, "position": [0.5, 9, -14]}]
        out.append(g)
    return out


# 4. SCENES ---------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S2 = B["b3"] - 1    # classroom: what a black hole is
    S3 = B["b5"] - 1    # space: the fall
    S4 = B["b7"] - 1    # space: time freezes
    S5 = B["b9"] - 1    # space: no way out
    S6 = B["b10"] - 1   # living room (white), night: closer

    scenes = []

    # 1. HOOK - space, the black hole blazing in the dark ---------------------------
    scenes.append({
        "id": "hook", "location": "space", "skyColor": "#000000",
        "startFrame": 0, "endFrame": S2,
        "cameraShots": cover(0, S2, [lambda a, b: wide(a, b, [0, 0, 0], 24),
                                      lambda a, b: shot(a, b, [0, 8, 14], [0, 7, 12], [0, 8, -10], [0, 8, -12], 55),
                                      lambda a, b: close_up(a, b, [0, 0, 0])]),
        "fx": hole_fx(0, S2),
        "characters": {
            "hero": hold(0, S2, [0, 0, 0], 0, "point", "shocked"),
            "friend": hold(0, S2, [-4.5, 0, 0], 0.2, "idle", "shocked"),
        },
    })

    # 2. CLASSROOM - what a black hole is ----------------------------------------------
    scenes.append({
        "id": "what", "location": "classroom",
        "boardText": ["STAR COLLAPSES", "EVENT HORIZON", "NO WAY BACK"],
        "startFrame": S2, "endFrame": S3,
        "cameraShots": cover(S2, S3, [lambda a, b: shot(a, b, [0, 7.4, 23], [0, 7.0, 20.5], [0, 4.8, -1], [0, 4.7, -1], 58),
                                       lambda a, b: close_up(a, b, [-0.5, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [-3.0, 0, -4.5])]),
        "characters": {
            "teacher": hold(S2, S3, [-3.0, 0, -4.5], 0.5, "point", "deadpan", "pointer"),
            "hero": hold(S2, S3, [-0.5, 0, 0.5], 0, "idle", "smile"),
            "friend": hold(S2, S3, [4.5, 0, 0.5], 0, "idle", "smile"),
        },
    })

    # 3. SPACE - the fall. The hero genuinely floats down toward the hole --------------
    scenes.append({
        "id": "fall", "location": "space", "skyColor": "#000000",
        "startFrame": S3, "endFrame": S4,
        "cameraShots": cover(S3, S4, [lambda a, b: shot(a, b, [0, 7, 12], [0, 6, 10], [0, 6, -2], [0, 5, -5], 50),
                                       lambda a, b: shot(a, b, [4, 8, 11], [3, 7, 9], [0, 6.5, -4], [0, 5.5, -6], 50),
                                       lambda a, b: wide(a, b, [0, 0, 0], 24)]),
        "fx": hole_fx(S3, S4),
        "characters": {
            "hero": [kf(S3, [0, 8, 0], 0, "idle", "shocked"),
                     kf(S4, [0, 3, -8], 0, "idle", "panic")],
        },
    })

    # 4. SPACE - frozen in time. The hero hangs mid-fall; the friend watches ------------
    scenes.append({
        "id": "frozen", "location": "space", "skyColor": "#000000",
        "startFrame": S4, "endFrame": S5,
        "cameraShots": cover(S4, S5, [lambda a, b: wide(a, b, [0, 0, 0], 24),
                                       lambda a, b: shot(a, b, [0, 6, 8], [0, 5.5, 7], [0, 4, -6], [0, 4, -6], 50),
                                       lambda a, b: close_up(a, b, [-4.5, 0, 2])]),
        "fx": hole_fx(S4, S5),
        "characters": {
            "hero": hold(S4, S5, [0, 4, -6], 0, "idle", "shocked"),
            "friend": hold(S4, S5, [-4.5, 0, 2], 0.4, "point", "shocked"),
        },
    })

    # 5. SPACE - no way out. The hero drifts the last stretch toward the hole -----------
    scenes.append({
        "id": "noescape", "location": "space", "skyColor": "#000000",
        "startFrame": S5, "endFrame": S6,
        "cameraShots": cover(S5, S6, [lambda a, b: wide(a, b, [0, 0, 0], 24),
                                       lambda a, b: shot(a, b, [0, 7, 12], [0, 6, 10], [0, 6, -4], [0, 5, -7], 50)]),
        "fx": hole_fx(S5, S6),
        "characters": {
            "hero": [kf(S5, [0, 4, -6], 0, "idle", "panic"),
                     kf(S6, [0, 2, -10], 0, "idle", "panic")],
        },
    })

    # 6. LIVING ROOM (white), NIGHT - closer ------------------------------------------------
    scenes.append({
        "id": "closer", "location": "living_room", "variant": "white", "isNight": True,
        "startFrame": S6, "endFrame": END,
        "cameraShots": cover(S6, END, [lambda a, b: wide(a, b, [0, 0, 0.4], 24),
                                         lambda a, b: close_up(a, b, [-4.0, 0, 0.4]),
                                         lambda a, b: close_up(a, b, [4.0, 0, 0.4])]),
        "characters": {
            "hero": [kf(S6, [-4.0, 0, 0.4], 0.9, "idle", "deadpan"),
                     kf(B["b11"], [-4.0, 0, 0.4], 0.9, "idle", "smile"),
                     kf(END, [-4.0, 0, 0.4], 0.9, "idle", "smile")],
            "mom": [kf(S6, [4.0, 0, 0.4], -0.9, "wave", "smile"),
                    kf(END, [4.0, 0, 0.4], -0.9, "wave", "smile")],
        },
    })

    return scenes
