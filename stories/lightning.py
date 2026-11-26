"""WHY DO WE SEE LIGHTNING BEFORE WE HEAR THUNDER? - science explainer.

Batch story: video 1 of 7.
Structure is a "why" explainer (question -> storm -> answer), like the
sky-blue and stars-twinkle Shorts: the "Why...?" question itself opens
the narration, then the setup follows.

The science: light travels ~300,000 km/s, sound only ~343 m/s — about
3 seconds per kilometre — so the flash reaches your eyes almost instantly
while the thunder has to travel all the way to your ears. Count the gap
between flash and thunder and you can judge how far away the lightning
is: 3 seconds is about 1 km, 6 seconds about 2 km. All plain-language,
standard figures, simplified for a Short.

Fresh visuals: a storm street (dark slate sky, night lighting, rain
streaks, a jagged emissive lightning bolt striking behind the actors,
dark blocky storm-cloud slabs overhead) — built in code from the Gemini
reference ~/workspace/user/files/1000374699_5_a8gc.jpg (never pasted in).
New assets: LightningBolt + Rainfall components, new music
(lightning.wav). The hero wears a yellow jacket, matching the boy in
the doorway in the reference.

Build:   python scripts/make_short.py stories/lightning.py --stills
Render:  node scripts/render.mjs story lightning --port 3051 (stills + ffmpeg; never renderMedia)
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, split_shots, wide  # noqa: F401

TITLE = "WHY LIGHTNING BEATS THUNDER"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b0", "text": "Why do we see lightning before we hear thunder?", "pause": 0.08},
    {"id": "b1", "text": "In this town, every storm plays the same trick. The sky flashes — and the thunder arrives seconds later.", "pause": 0.08},
    {"id": "b2", "text": "One evening, the sky lit up over Main Street. Bright as day. Totally silent.", "pause": 0.10},
    {"id": "b3", "text": "Then — one, two, three — the thunder rolled in. The flash and the bang left at the same moment, from the same bolt.", "pause": 0.10},
    {"id": "b4", "text": "Light is just much faster. Three hundred thousand kilometres every second.", "pause": 0.10},
    {"id": "b5", "text": "Sound is slow. Three hundred and forty-three metres a second. About three seconds per kilometre.", "pause": 0.10},
    {"id": "b6", "text": "So the flash reaches your eyes almost instantly. The thunder has to walk all the way to your ears.", "pause": 0.10},
    {"id": "b7", "text": "That gap is a measuring tape. Count the seconds between the flash and the thunder.", "pause": 0.08},
    {"id": "b8", "text": "Thunder right on top of the flash? The storm is right above you. Get inside.", "pause": 0.08},
    {"id": "b9", "text": "Three seconds? About one kilometre away. Six seconds? Two kilometres. Nine seconds? Three.", "pause": 0.10},
    {"id": "b10", "text": "Next time a storm rolls in, count the gap. The sky is telling you how far away it is.", "pause": 0.10},
    {"id": "b11", "text": "Lightning is fast. Thunder is slow. And the silence between them tells you the distance.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/lightning.wav",
    "under_voice": 0.022,
    "gaps": 0.05,
    "dropouts": [("b9", "b9.end")],
}

SFX = [
    ("b0", "sparkle"),
    ("b1+0.5", "whoosh"),
    ("b2", "impact"),
    ("b3+0.3", "thud"),
    ("b4+0.5", "sparkle"),
    ("b5+0.5", "pop", {"f": 600}),
    ("b7+0.5", "pop", {"f": 600}),
    ("b9+0.5", "reveal"),
    ("b10+0.5", "sparkle"),
]

# 3. CAST ----------------------------------------------------------------------
# Hero in a yellow jacket, matching the boy in the doorway in the Gemini
# reference (1000374699_5_a8gc.jpg). Distinct from sky_blue's blue-haired hero.
HERO = {
    "skin": "light",
    "hair": {"style": "messyFringe", "color": "black"},
    "top": {"style": "jacket", "color": "yellow", "secondary": "white"},
    "bottom": {"style": "jeans", "color": "darkDenim"},
    "shoes": {"color": "white", "sole": "white"},
    "freckles": True,
}
CAST = {
    "hero": HERO,
    "friend": {"extends": "kid_girl", "hair": {"style": "ponytail", "color": "brown"},
               "top": {"style": "hoodie", "color": "pink", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"color": "white", "sole": "white"}},
    "teacher": {"extends": "teacher_woman", "skin": "fair", "hair": {"style": "bun", "color": "blonde"}},
    "mom": {"extends": "real_mom", "hair": {"style": "ponytail", "color": "brown"}},
}


# 4. SCENES ---------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S2 = B["b3"] - 1    # street storm: the count
    S3 = B["b4"] - 1    # classroom: the speeds
    S4 = B["b7"] - 1    # street storm: the measuring trick
    S5 = B["b10"] - 1   # living room, night: closer

    # Storm dressing, shared by both street scenes: one jagged bolt striking
    # behind the actors, a sheet of slanted rain, dark cloud slabs overhead.
    # Bolt top (y ~19) disappears into the cloud slabs.
    STORM_FX = [
        {"id": "bolt", "shape": "lightning", "color": "#FEF08A",
         "keyframes": [{"frame": 0, "position": [3, 0, -6]}]},
        {"id": "rain", "shape": "rain", "color": "#DBEAFE",
         "keyframes": [{"frame": 0, "position": [0, 0, 0]}]},
        {"id": "cloud1", "shape": "box", "size": [26, 3, 10], "color": "#0F172A",
         "roughness": 0.9, "keyframes": [{"frame": 0, "position": [0, 18, -8]}]},
        {"id": "cloud2", "shape": "box", "size": [18, 3, 8], "color": "#1E293B",
         "roughness": 0.9, "keyframes": [{"frame": 0, "position": [-9, 20, -4]}]},
        {"id": "cloud3", "shape": "box", "size": [16, 3, 8], "color": "#1E293B",
         "roughness": 0.9, "keyframes": [{"frame": 0, "position": [10, 19, -10]}]},
    ]

    scenes = []

    # 1. HOOK - street, storm. Both look up at the flashing sky ---------------------------
    # Wide is a STATIC shot (2026-11-17 fix): wide()'s push drags the
    # door/window edges across the frame and reads as flicker. Same opening
    # framing as wide([0, 0, 0.5], 24), zero push. Storm dusk: dark slate
    # sky + night lighting (glowing windows).
    scenes.append({
        "id": "hook", "location": "street", "skyColor": "#1E293B", "isNight": True,
        "startFrame": 0, "endFrame": S2,
        "cameraShots": cover(0, S2, [lambda a, b: shot(a, b, [0, 7.4, 24.5], [0, 7.4, 24.5], [0, 4.8, -0.5], [0, 4.8, -0.5], 58),
                                      lambda a, b: close_up(a, b, [-4, 0, 0.5]),
                                      lambda a, b: close_up(a, b, [1, 0, 0.5])]),
        "fx": STORM_FX,
        "characters": {
            "hero": hold(0, S2, [-4, 0, 0.5], 0.2, "point", "shocked"),
            "friend": hold(0, S2, [1, 0, 0.5], -0.2, "point", "shocked"),
        },
    })

    # 2. STREET STORM - the count. The bolt flashes again; hero counts --------------------
    scenes.append({
        "id": "count", "location": "street", "skyColor": "#1E293B", "isNight": True,
        "startFrame": S2, "endFrame": S3,
        "cameraShots": cover(S2, S3, [lambda a, b: shot(a, b, [0, 7.4, 24.5], [0, 7.4, 24.5], [0, 4.8, -0.5], [0, 4.8, -0.5], 58),
                                       lambda a, b: close_up(a, b, [-4, 0, 0.5]),
                                       lambda a, b: shot(a, b, [-1, 3, 15], [-1, 3.5, 13], [3, 8, -6], [3, 8, -6], 58)]),
        "fx": STORM_FX,
        "characters": {
            "hero": hold(S2, S3, [-4, 0, 0.5], 0.2, "point", "shocked"),
            "friend": hold(S2, S3, [1, 0, 0.5], -0.2, "idle", "smile"),
        },
    })

    # 3. CLASSROOM - the speeds on the board ------------------------------------------------
    scenes.append({
        "id": "mechanism", "location": "classroom",
        "boardText": ["LIGHT = 300,000 KM/S", "SOUND = 343 M/S", "3 SECONDS = 1 KM"],
        "startFrame": S3, "endFrame": S4,
        "cameraShots": cover(S3, S4, [lambda a, b: shot(a, b, [0, 7.4, 23], [0, 7.4, 23], [0, 4.8, -1], [0, 4.8, -1], 58),
                                       lambda a, b: close_up(a, b, [-0.5, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [-3.0, 0, -4.5])]),
        "characters": {
            "teacher": hold(S3, S4, [-3.0, 0, -4.5], 0.5, "point", "deadpan", "pointer"),
            "hero": hold(S3, S4, [-0.5, 0, 0.5], 0, "idle", "smile"),
            "friend": hold(S3, S4, [4.0, 0, 0.5], 0, "idle", "smile"),
        },
    })

    # 4. STREET STORM - the measuring trick. Hero counts on the gap --------------------------
    scenes.append({
        "id": "measure", "location": "street", "skyColor": "#1E293B", "isNight": True,
        "startFrame": S4, "endFrame": S5,
        "cameraShots": cover(S4, S5, [lambda a, b: shot(a, b, [0, 7.4, 24.5], [0, 7.4, 24.5], [0, 4.8, -0.5], [0, 4.8, -0.5], 58),
                                       lambda a, b: close_up(a, b, [-4, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [1, 0, 0.5])]),
        "fx": STORM_FX,
        "characters": {
            "hero": hold(S4, S5, [-4, 0, 0.5], 0.2, "point", "smile"),
            "friend": hold(S4, S5, [1, 0, 0.5], -0.2, "idle", "smile"),
        },
    })

    # 5. LIVING ROOM (blue), NIGHT - closer ----------------------------------------------------
    scenes.append({
        "id": "closer", "location": "living_room", "variant": "blue", "isNight": True,
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
