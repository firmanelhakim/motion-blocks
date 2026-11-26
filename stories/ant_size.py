"""WHAT IF YOU SHRANK TO THE SIZE OF AN ANT? - science explainer.

Batch of 5 storyboards (the maintainer, 2026-11-17): video 4 of 5.
Structure: hook (kitchen, macro world) -> classroom mechanism (square-cube
law) -> kitchen walk (falling is harmless) -> raindrop (the hazard) ->
puddle (surface tension) -> living-room closer. No timeline shape, no
classroom repeat, no space/beach.

The science: ants lift ~50x their own weight. Strength comes from muscle
width (area, squared) while weight comes from size (volume, cubed) - shrink
and strength wins, so a shrunken you would be relatively much stronger too.
Falling is harmless at that size: air resistance catches you, terminal
velocity is tiny, you could fall off a table and walk away. A raindrop is
the danger: one drop weighs about as much as an ant-sized you and falls at
~30 km/h, so to an ant it is a wrecking ball. A puddle is a lake, and the
water's surface is like a stretchy skin too strong to break through
(surface tension rules at small scales). All plain-language, standard
figures, simplified for a Short.

Fresh visuals: the hero is TINY (cast scale 0.15) for the whole video while
the friend and mom stay full size - the size gap IS the visual. Macro world
built from fx: giant grass blades, a crumb as big as the hero, a falling
raindrop, a puddle lake. New music (ant-size.wav). If the tiny hero reads
as a bug in the stills instead of the premise, fall back to a normal-scale
hero with giant props (second cast entry + swap).
The teacher is in the standard white blouse, placed beside the desk at
x -3.0 - check the stills for the sun_off blending problem and switch her
to teal if it appears.

Build:   python scripts/make_short.py stories/ant_size.py --stills
Render:  python scripts/make_short.py stories/ant_size.py --skip-tts --render
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, split_shots, wide  # noqa: F401

TITLE = "WHAT IF YOU SHRANK TO THE SIZE OF AN ANT?"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this town, you woke up the size of an ant. Everything you know just got huge.", "pause": 0.08},
    {"id": "b2", "text": "A blade of grass is now a tree. A crumb is a feast. And the kitchen floor is a desert.", "pause": 0.10},
    {"id": "b3", "text": "But here is the good news. Ants can lift 50 times their own weight.", "pause": 0.10},
    {"id": "b4", "text": "Muscles get their strength from how wide they are. Weight comes from how big you are. Shrink, and strength wins.", "pause": 0.10},
    {"id": "b5", "text": "At ant size, you could lift 50 times your weight too. A sugar cube would feel like a feather.", "pause": 0.10},
    {"id": "b6", "text": "And falling? Forget about it. The air catches you like a cushion. You could fall off the table and walk away.", "pause": 0.10},
    {"id": "b7", "text": "But the rain is a different story. One raindrop weighs as much as you do — and it falls at 30 kilometres an hour.", "pause": 0.10},
    {"id": "b8", "text": "To an ant, a raindrop is a wrecking ball. You would run for cover under the nearest leaf.", "pause": 0.10},
    {"id": "b9", "text": "And a puddle? That is a lake now. The surface of the water is like a stretchy skin — too strong to break through.", "pause": 0.10},
    {"id": "b9b", "text": "Getting stuck in a drop is the real danger. Ants can drown in a single drop of dew.", "pause": 0.08},
    {"id": "b10", "text": "Small is not weak. At ant size, you are stronger, lighter, and harder to hurt than you have ever been.", "pause": 0.10},
    {"id": "b11", "text": "You just have to watch the weather. And never, ever stand under a dripping tap.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/ant-size.wav",
    "under_voice": 0.022,
    "gaps": 0.05,
}

SFX = [
    ("b1", "whoosh"),
    ("b1+0.5", "pop", {"f": 600}),
    ("b3+0.5", "pop", {"f": 700}),
    ("b5+0.5", "sparkle"),
    ("b6+0.5", "whoosh"),
    ("b7", "bell_low"),
    ("b7+1.2", "thud"),
    ("b9+0.5", "bubbles"),
    ("b10+0.5", "reveal"),
    ("b11+1.5", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
# The hero is TINY (scale 0.15) for the whole video; friend and mom stay full
# size, so the size gap is visible in every scene.
HERO = {
    "skin": "light",
    "hair": {"style": "spikyAnime", "color": "blue"},
    "top": {"style": "hoodie", "color": "royal", "secondary": "white"},
    "bottom": {"style": "jeans", "color": "denim"},
    "shoes": {"color": "white", "sole": "white"},
    "freckles": True,
    "scale": 0.15,
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

# Giant grass blades: tall thin boxes, base at y 0 (centre y = height / 2).
def grass(a, b, positions):
    out = []
    for i, (gx, gz, h) in enumerate(positions):
        out.append({"id": f"blade{i}", "shape": "box", "size": [0.5, h, 0.5],
                    "color": "#22C55E", "roughness": 0.8,
                    "keyframes": [{"frame": a, "position": [gx, h / 2, gz]},
                                  {"frame": b, "position": [gx, h / 2, gz]}]})
    return out


# 4. SCENES ---------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S2 = B["b3"] - 1    # classroom: why ants are strong
    S3 = B["b6"] - 1    # kitchen: the walk (falling is harmless)
    S4 = B["b7"] - 1    # kitchen: the raindrop
    S5 = B["b9"] - 1    # kitchen: the puddle lake
    S6 = B["b10"] - 1   # living room (blue), night: closer

    scenes = []

    # 1. HOOK - kitchen, macro world. Tiny hero, towering friend, grass trees --------
    scenes.append({
        "id": "hook", "location": "kitchen", "variant": "blue",
        "startFrame": 0, "endFrame": S2,
        "cameraShots": cover(0, S2, [lambda a, b: shot(a, b, [0, 2.5, 11], [0, 2.2, 10], [0, 1.5, -1], [0, 1.5, -1], 55),
                                      lambda a, b: close_up(a, b, [-2, 0, 0], scale=0.15, dist=4),
                                      # Shot 3 was reframed 2026-11-17: the old camera at
                                      # [2,3,8] put the giant blade at (-1,2,11) exactly on
                                      # the sightline to the tiny hero, so the frame was
                                      # empty floor + blade. New low shot from the left,
                                      # target at the hero's own height (0.35).
                                      lambda a, b: shot(a, b, [-4.5, 1.3, 5.5], [-4.5, 1.1, 5.0], [-2, 0.35, 0], [-2, 0.35, 0], 50)]),
        "fx": grass(0, S2, [(-4, -2, 10), (3, -3, 12), (0, -4, 9), (-1, 2, 11)]) + [
            {"id": "crumb", "shape": "box", "size": [1.2, 0.8, 1.2], "color": "#92400E",
             "roughness": 0.8,
             "keyframes": [{"frame": 0, "position": [3, 0.4, -1]}, {"frame": S2, "position": [3, 0.4, -1]}]},
        ],
        "characters": {
            "hero": hold(0, S2, [-2, 0, 0], 0.9, "idle", "shocked"),
            "friend": hold(0, S2, [1, 0, 0], -0.9, "idle", "shocked"),
        },
    })

    # 2. CLASSROOM - why ants are strong ------------------------------------------------
    # Board shot shows teacher + board (hero tiny at the bottom edge); the hero
    # close-up is shot low, at his own height.
    scenes.append({
        "id": "strong", "location": "classroom",
        "boardText": ["ANTS LIFT 50x", "STRENGTH = WIDTH", "WEIGHT = SIZE"],
        "startFrame": S2, "endFrame": S3,
        "cameraShots": cover(S2, S3, [lambda a, b: shot(a, b, [0, 7.4, 23], [0, 7.0, 20.5], [0, 4.8, -1], [0, 4.7, -1], 58),
                                       lambda a, b: close_up(a, b, [-0.5, 0, 0.5], scale=0.15, dist=4),
                                       lambda a, b: close_up(a, b, [-3.0, 0, -4.5])]),
        "characters": {
            "teacher": hold(S2, S3, [-3.0, 0, -4.5], 0.5, "point", "deadpan", "pointer"),
            "hero": hold(S2, S3, [-0.5, 0, 0.5], 0, "idle", "smile"),
            "friend": hold(S2, S3, [4.0, 0, 0.5], 0, "idle", "smile"),
        },
    })

    # 3. KITCHEN - the walk. The tiny hero crosses the giant floor -------------------------
    scenes.append({
        "id": "walk", "location": "kitchen", "variant": "blue",
        "startFrame": S3, "endFrame": S4,
        "cameraShots": cover(S3, S4, [lambda a, b: shot(a, b, [-2, 2, 8], [-1, 2, 7], [-1, 1, 0], [0, 1, 0], 55),
                                       lambda a, b: close_up(a, b, [0, 0, 0], scale=0.15, dist=4),
                                       lambda a, b: shot(a, b, [2, 2.5, 9], [2, 2.2, 8], [0, 1.5, -1], [0, 1.5, -1], 55)]),
        "fx": grass(S3, S4, [(-4, -2, 10), (3, -3, 12), (0, -4, 9), (-1, 2, 11)]),
        "characters": {
            "hero": [kf(S3, [-4, 0, 0], HALF, "walk", "smile"),
                     kf(S4, [2, 0, 0], HALF, "walk", "smile")],
        },
    })

    # 4. KITCHEN - the raindrop. A giant drop falls where the hero stood -----------------------
    drop_at = S4 + 45
    scenes.append({
        "id": "raindrop", "location": "kitchen", "variant": "blue",
        "startFrame": S4, "endFrame": S5,
        "cameraShots": cover(S4, S5, [lambda a, b: shot(a, b, [0, 3, 10], [0, 2.6, 9], [0, 3, -1], [0, 2, -1], 55),
                                       lambda a, b: close_up(a, b, [-2, 0, 1], scale=0.15, dist=4),
                                       lambda a, b: shot(a, b, [2, 4, 9], [2, 3.5, 8], [2, 6, -1], [2, 2, -1], 55)]),
        "fx": grass(S4, S5, [(-4, -2, 10), (3, -3, 12), (0, -4, 9)]) + [
            {"id": "drop", "shape": "sphere", "radius": 1.2, "color": "#38BDF8",
             "emissive": "#0EA5E9", "emissiveIntensity": 0.4, "roughness": 0.2, "opacity": 0.85,
             "keyframes": [{"frame": S4, "position": [2, 14, -1]},
                           {"frame": drop_at, "position": [2, 1.0, -1]},
                           {"frame": S5, "position": [2, 1.0, -1]}]},
        ],
        "characters": {
            # The hero sprints away from the falling drop and shelters by a blade.
            "hero": [kf(S4, [2, 0, 0], -HALF, "idle", "shocked"),
                     kf(S4 + 30, [-1, 0, 1], -HALF, "sprint", "panic"),
                     kf(S5, [-3, 0, 1], -HALF, "idle", "panic")],
        },
    })

    # 5. KITCHEN - the puddle lake ---------------------------------------------------------------
    scenes.append({
        "id": "puddle", "location": "kitchen", "variant": "blue",
        "startFrame": S5, "endFrame": S6,
        "cameraShots": cover(S5, S6, [lambda a, b: shot(a, b, [0, 2.5, 9], [0, 2.2, 8], [0, 1, -2], [0, 1, -2], 55),
                                       lambda a, b: close_up(a, b, [-2, 0, 0], scale=0.15, dist=4),
                                       lambda a, b: shot(a, b, [3, 2, 8], [3, 1.8, 7], [0, 0.8, -3], [0, 0.8, -3], 55)]),
        "fx": [
            {"id": "lake", "shape": "box", "size": [8, 0.4, 6], "color": "#0EA5E9",
             "emissive": "#0369A1", "emissiveIntensity": 0.3, "roughness": 0.2, "opacity": 0.8,
             "keyframes": [{"frame": S5, "position": [0, 0.3, -3]}, {"frame": S6, "position": [0, 0.3, -3]}]},
        ],
        "characters": {
            "hero": hold(S5, S6, [-2, 0, 0], 0.9, "point", "shocked"),
        },
    })

    # 6. LIVING ROOM (blue), NIGHT - closer. Mom towers over the tiny hero ------------------------
    scenes.append({
        "id": "closer", "location": "living_room", "variant": "blue", "isNight": True,
        "startFrame": S6, "endFrame": END,
        "cameraShots": cover(S6, END, [lambda a, b: shot(a, b, [1, 3, 13], [1, 2.8, 11.5], [1, 1.5, 0.4], [1, 1.5, 0.4], 58),
                                         lambda a, b: close_up(a, b, [-2, 0, 0.4], scale=0.15, dist=4),
                                         lambda a, b: close_up(a, b, [3, 0, 0.4])]),
        "characters": {
            "hero": [kf(S6, [-2, 0, 0.4], 0.9, "idle", "deadpan"),
                     kf(B["b11"], [-2, 0, 0.4], 0.9, "idle", "smile"),
                     kf(END, [-2, 0, 0.4], 0.9, "idle", "smile")],
            "mom": [kf(S6, [3, 0, 0.4], -0.9, "wave", "smile"),
                    kf(END, [3, 0, 0.4], -0.9, "wave", "smile")],
        },
    })

    return scenes
