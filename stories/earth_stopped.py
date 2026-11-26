"""WHAT IF THE EARTH STOPPED SPINNING? - science explainer.

Batch of 5 storyboards (the maintainer, 2026-11-17): video 3 of 5.
Structure: hook (aerial) -> classroom number (465 m/s) -> playground demo
(everything flies east) -> street day (eternal day) -> street night (eternal
night, same spot) -> living-room closer. No timeline shape, no beach, no
space, no classroom repeat.

The science: Earth spins at the equator at 465 m/s - 1,670 km/h, faster
than sound (343 m/s) - and we never feel it because everything spins with
us, including the air. If it stopped suddenly, inertia would keep everything
loose flying east at that speed: people, cars, air, oceans - winds faster
than any hurricane, waves taller than buildings. After the chaos, one side
faces the Sun forever (eternal day, never cools) and the other faces away
forever (eternal night, never warms); a day would last a whole year. NOTE:
this reuses the 465 m/s fact from gravity v2, but none of its beats or
scenes - v2 was about things floating up; this is about things flying
sideways and the day/night cycle breaking.

Fresh visuals: the inertia demo (actors sliding east + balls flying across
the playground), the same street shot twice - day then night - to show the
split, new music (earth-stopped.wav). The teacher is in the standard white
blouse, placed beside the desk at x -3.0 - check the stills for the sun_off
blending problem and switch her to teal if it appears.

Build:   python scripts/make_short.py stories/earth_stopped.py --stills
Render:  python scripts/make_short.py stories/earth_stopped.py --skip-tts --render
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, split_shots, wide  # noqa: F401

TITLE = "WHAT IF THE EARTH STOPPED SPINNING?"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this world, the Earth stopped spinning. Just stopped. Right now.", "pause": 0.08},
    {"id": "b2", "text": "You would not feel the Earth stop. You would feel everything else keep going.", "pause": 0.10},
    {"id": "b3", "text": "The Earth spins at 465 metres every second. That is 1,670 kilometres an hour.", "pause": 0.10},
    {"id": "b4", "text": "Faster than the speed of sound. And you never feel it — because everything spins with you.", "pause": 0.10},
    {"id": "b4b", "text": "The air spins with us too. That is why the wind is not blowing at 1,670 kilometres an hour right now.", "pause": 0.08},
    {"id": "b5", "text": "But if the Earth stopped, everything loose would keep flying east. People, cars, the air, the oceans.", "pause": 0.10},
    {"id": "b6", "text": "Winds faster than any hurricane. Waves taller than buildings. All moving east, all at once.", "pause": 0.10},
    {"id": "b7", "text": "And then it goes quiet. One side of the Earth faces the Sun forever. Eternal day. It never cools down.", "pause": 0.10},
    {"id": "b8", "text": "The other side faces away forever. Eternal night. It never warms up again.", "pause": 0.10},
    {"id": "b9", "text": "No more sunrises. No more sunsets. A day would last a whole year.", "pause": 0.10},
    {"id": "b10", "text": "So the spin you never feel is doing two jobs: it gives you day and night, and it keeps the air and the sea calm.", "pause": 0.10},
    {"id": "b11", "text": "You are spinning right now, at 1,670 kilometres an hour — and you never feel a thing.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/earth-stopped.wav",
    "under_voice": 0.022,
    "gaps": 0.05,
}

SFX = [
    ("b1", "whoosh"),
    ("b1+0.5", "bell_low"),
    ("b3+0.5", "pop", {"f": 600}),
    ("b5+0.5", "whoosh"),
    ("b6", "riser", {"dur": 1.5}),
    ("b7+0.5", "sparkle"),
    ("b8", "bell_low"),
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


# 4. SCENES ---------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S2 = B["b3"] - 1    # classroom: the number
    S3 = B["b5"] - 1    # playground: everything flies east
    S4 = B["b7"] - 1    # street, day: eternal day
    S5 = B["b8"] - 1    # street, night: eternal night (same spot)
    S6 = B["b9"] - 1    # living room (red), night: closer

    scenes = []

    # 1. HOOK - aerial town, day ------------------------------------------------------
    scenes.append({
        "id": "hook", "location": "town_overview",
        "startFrame": 0, "endFrame": S2,
        "cameraShots": [shot(0, S2 // 3, [-10, 62, 74], [-7, 56, 67], [8, 0, -6], [7, 1, -7], 55),
                        shot(S2 // 3, 2 * S2 // 3, [-7, 56, 67], [-4, 50, 61], [7, 1, -7], [6, 2, -8], 55),
                        shot(2 * S2 // 3, S2, [-4, 50, 61], [-2, 46, 56], [6, 2, -8], [6, 2, -8], 55)],
        "characters": {},
    })

    # 2. CLASSROOM - the number ---------------------------------------------------------
    scenes.append({
        "id": "number", "location": "classroom",
        "boardText": ["SPIN: 465 m/s", "1,670 km/h", "FASTER THAN SOUND"],
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

    # 3. PLAYGROUND - everything flies east ------------------------------------------------
    # Hero and friend slide east in parallel lanes (4.5 apart), then lie knocked
    # down; coloured balls streak across above them - the loose stuff, still moving.
    slide_end = S3 + 60
    scenes.append({
        "id": "inertia", "location": "playground",
        "startFrame": S3, "endFrame": S4,
        "cameraShots": cover(S3, S4, [lambda a, b: wide(a, b, [0, 0, 2], 24),
                                       lambda a, b: shot(a, b, [-7, 7, 16], [-6, 6.5, 14], [3.5, 1.5, 2], [3.5, 1.5, 2], 55),
                                       lambda a, b: shot(a, b, [-8, 5, 12], [-7, 4.5, 10], [3.5, 1.5, 2], [3.5, 1.5, 2], 55)]),
        "fx": [
            {"id": "fly1", "shape": "sphere", "radius": 0.9, "color": "#EF4444",
             "emissive": "#DC2626", "emissiveIntensity": 0.5, "roughness": 0.5,
             "keyframes": [{"frame": S3, "position": [-12, 4, -2]}, {"frame": S4, "position": [12, 4, -2]}]},
            {"id": "fly2", "shape": "sphere", "radius": 0.9, "color": "#3B82F6",
             "emissive": "#2563EB", "emissiveIntensity": 0.5, "roughness": 0.5,
             "keyframes": [{"frame": S3, "position": [-12, 5.5, 0]}, {"frame": S4, "position": [12, 5.5, 0]}]},
            {"id": "fly3", "shape": "sphere", "radius": 0.9, "color": "#FACC15",
             "emissive": "#EAB308", "emissiveIntensity": 0.5, "roughness": 0.5,
             "keyframes": [{"frame": S3, "position": [-12, 3.5, -4]}, {"frame": S4, "position": [12, 3.5, -4]}]},
        ],
        "characters": {
            "hero": [kf(S3, [-5, 0, 0], HALF, "sprint", "panic"),
                     kf(slide_end, [3, 0, 0], HALF, "sprint", "panic"),
                     kf(slide_end + 6, [3, 0, 0], 0, "knocked", "panic"),
                     kf(S4, [3, 0, 0], 0, "knocked", "panic")],
            "friend": [kf(S3, [-4, 0, 4.5], HALF, "sprint", "panic"),
                       kf(slide_end, [4, 0, 4.5], HALF, "sprint", "panic"),
                       kf(slide_end + 6, [4, 0, 4.5], 0, "knocked", "panic"),
                       kf(S4, [4, 0, 4.5], 0, "knocked", "panic")],
        },
    })

    # 4. STREET, DAY - eternal day ------------------------------------------------------------
    scenes.append({
        "id": "eternalday", "location": "street",
        "startFrame": S4, "endFrame": S5,
        "cameraShots": cover(S4, S5, [lambda a, b: wide(a, b, [0, 0, 0.5], 24),
                                       lambda a, b: close_up(a, b, [-4.5, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [0, 0, 0.5])]),
        "characters": {
            "hero": hold(S4, S5, [-4.5, 0, 0.5], 0.2, "panting", "shocked"),
            "friend": hold(S4, S5, [0, 0, 0.5], -0.2, "panting", "shocked"),
        },
    })

    # 5. STREET, NIGHT - eternal night, same spot ------------------------------------------------
    scenes.append({
        "id": "eternalnight", "location": "street", "isNight": True,
        "startFrame": S5, "endFrame": S6,
        "cameraShots": cover(S5, S6, [lambda a, b: wide(a, b, [0, 0, 0.5], 24),
                                       lambda a, b: close_up(a, b, [-4.5, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [0, 0, 0.5])]),
        "characters": {
            "hero": hold(S5, S6, [-4.5, 0, 0.5], 0.2, "panting", "shocked"),
            "friend": hold(S5, S6, [0, 0, 0.5], -0.2, "panting", "shocked"),
        },
    })

    # 6. LIVING ROOM (red), NIGHT - closer ---------------------------------------------------------
    scenes.append({
        "id": "closer", "location": "living_room", "variant": "red", "isNight": True,
        "startFrame": S6, "endFrame": END,
        # Close-ups pulled back to dist 10 (2026-11-17 fix): at the default
        # dist 7 the actors filled the frame and mom's face sat tight to the
        # right edge with her ponytail/arm cropped. Same makers and timing.
        "cameraShots": cover(S6, END, [lambda a, b: wide(a, b, [0, 0, 0.4], 24),
                                         lambda a, b: close_up(a, b, [-4.0, 0, 0.4], dist=10),
                                         lambda a, b: close_up(a, b, [4.0, 0, 0.4], dist=10)]),
        "characters": {
            "hero": [kf(S6, [-4.0, 0, 0.4], 0.9, "idle", "deadpan"),
                     kf(B["b11"], [-4.0, 0, 0.4], 0.9, "idle", "smile"),
                     kf(END, [-4.0, 0, 0.4], 0.9, "idle", "smile")],
            "mom": [kf(S6, [4.0, 0, 0.4], -0.9, "wave", "smile"),
                    kf(END, [4.0, 0, 0.4], -0.9, "wave", "smile")],
        },
    })

    return scenes
