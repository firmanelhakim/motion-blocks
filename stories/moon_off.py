"""WHAT IF THE MOON DISAPPEARED? - science explainer.

Batch of 5 storyboards (the maintainer, 2026-11-17): video 1 of 5.
Structure is NOT sun_off's timeline shape: hook -> beach demo (the tide
goes out) -> classroom mechanism -> beach night (darkness + stars) ->
schoolyard consequence (the wobble) -> closer. No shouts, calm tide mood.

The science: the Moon's gravity drags the oceans, and that pull is most of
what makes the tides - without it the tides shrink to about a third of
their size (the Sun's pull alone). No Moon also means no moonlight, so
nights go properly dark and the stars look brighter. The slow change is the
biggest: the Moon steadies Earth's tilt like a hand on a spinning top, so
over thousands of years without it the tilt wobbles and the seasons go
wild. All plain-language, standard figures, simplified for a Short.

Fresh visuals: the new beach location (night shore, tide fx retreating),
star fx, an Earth globe fx wobbling over the schoolyard, new music
(moon-tide.wav). The teacher is in the standard white blouse, placed
beside the desk at x -3.0 (not on it) - check the stills for the sun_off
blending problem and switch her to teal if it appears.

Build:   python scripts/make_short.py stories/moon_off.py --stills
Render:  python scripts/make_short.py stories/moon_off.py --skip-tts --render
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, split_shots, wide  # noqa: F401

TITLE = "WHAT IF THE MOON DISAPPEARED?"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this town, the Moon disappeared last night. And nobody noticed — at first.", "pause": 0.08},
    {"id": "b2", "text": "The Moon looks small up there. But it is pulling on the sea, right now.", "pause": 0.08},
    {"id": "b3", "text": "Its gravity drags the oceans toward it. That pull is what makes the tides.", "pause": 0.10},
    {"id": "b4", "text": "So the first thing that changed was the sea. The tide went out — and it never came back in.", "pause": 0.10},
    {"id": "b4b", "text": "The beach grew wider. Rock pools that were underwater became dry land.", "pause": 0.08},
    {"id": "b5", "text": "Without the Moon, the tides shrink to a third of their size. The Sun pulls the sea too — but it is too far away to do the Moon's job.", "pause": 0.10},
    {"id": "b6", "text": "The nights changed next. No Moon means no moonlight. The night goes properly dark.", "pause": 0.10},
    {"id": "b7", "text": "And the stars come out brighter than you have ever seen them.", "pause": 0.08},
    {"id": "b7b", "text": "And here is the strangest part. The Moon is already drifting away from us — a little further every year.", "pause": 0.10},
    {"id": "b8", "text": "But the slowest change is the biggest one. The Moon holds the Earth steady, like a hand on a spinning top.", "pause": 0.10},
    {"id": "b9", "text": "Without it, over thousands of years, the Earth starts to wobble. And the seasons go wild.", "pause": 0.10},
    {"id": "b10", "text": "Winters in the summer. Summers in the winter. The calendar stops meaning anything.", "pause": 0.10},
    {"id": "b11", "text": "So tonight, look up. The Moon is still there — pulling the sea, steadying the Earth, lighting the night. For now.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/moon-tide.wav",
    "under_voice": 0.022,
    "gaps": 0.05,
}

SFX = [
    ("b1", "whoosh"),
    ("b1+0.5", "sparkle"),
    ("b3+0.5", "swish"),
    ("b4+0.5", "swish"),
    ("b5+0.5", "pop", {"f": 600}),
    ("b6", "bell_low"),
    ("b7+0.5", "sparkle"),
    ("b7b+0.5", "pop", {"f": 600}),
    ("b8+0.5", "pop", {"f": 600}),
    ("b9", "riser", {"dur": 1.5}),
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

    S2 = B["b3"] - 1    # beach, night: the tide goes out
    S3 = B["b5"] - 1    # classroom: why the tides shrink
    S4 = B["b6"] - 1    # beach, night: dark sky, bright stars
    S5 = B["b8"] - 1    # schoolyard, day: the Earth wobbles
    S6 = B["b11"] - 1   # living room (yellow), night: closer

    scenes = []

    # 1. HOOK - aerial town, night, the Moon in the sky ---------------------------
    # Moon raised to y 38 (2026-11-17 fix) so it sits against the black sky,
    # not low over the hill where it read as a white ball. Craters ride on
    # the Moon: same keyframe frames, offset from the Moon's centre, so they
    # track it exactly as it drifts.
    moon_kf = [{"frame": 0, "position": [10, 38, -10]}, {"frame": S2, "position": [12, 39, -10]}]
    moon_fx = [{"id": "moon", "shape": "sphere", "radius": 4.0, "color": "#F1F5F9",
                "emissive": "#CBD5E1", "emissiveIntensity": 0.7, "roughness": 0.9,
                "keyframes": moon_kf}]
    for i, (ox, oy, oz, r) in enumerate([
            (1.5, 1.0, 2.8, 0.9), (-1.2, 2.0, 2.5, 0.7), (2.6, -0.8, 1.8, 0.8),
            (0.2, 3.2, 0.8, 0.6), (-2.6, -0.5, 2.0, 0.8), (0.8, -2.2, 2.4, 0.7)]):
        moon_fx.append({"id": f"crater{i}", "shape": "sphere", "radius": r, "color": "#94A3B8",
                        "emissive": "#64748B", "emissiveIntensity": 0.25, "roughness": 0.9,
                        "keyframes": [{"frame": k["frame"],
                                      "position": [k["position"][0] + ox, k["position"][1] + oy, k["position"][2] + oz]}
                                     for k in moon_kf]})
    scenes.append({
        "id": "hook", "location": "town_overview", "isNight": True,
        "startFrame": 0, "endFrame": S2,
        "cameraShots": [shot(0, S2 // 3, [-10, 62, 74], [-7, 56, 67], [8, 0, -6], [7, 1, -7], 55),
                        shot(S2 // 3, 2 * S2 // 3, [-7, 56, 67], [-4, 50, 61], [7, 1, -7], [6, 2, -8], 55),
                        shot(2 * S2 // 3, S2, [-4, 50, 61], [-2, 46, 56], [6, 2, -8], [6, 2, -8], 55)],
        "fx": moon_fx,
        "characters": {},
    })

    # 2. BEACH, NIGHT - the tide goes out and never comes back ----------------------
    # The tide fx is a wide flat water sheet on the sand: it slides back toward
    # the sea and sinks as the scene runs, so the shoreline visibly retreats.
    scenes.append({
        "id": "tide", "location": "beach", "isNight": True,
        "startFrame": S2, "endFrame": S3,
        "cameraShots": cover(S2, S3, [lambda a, b: wide(a, b, [0, 0, 0.5], 24),
                                       lambda a, b: close_up(a, b, [-4, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [1, 0, 0.5])]),
        "fx": [
            {"id": "tide", "shape": "box", "size": [40, 0.8, 10], "color": "#0EA5E9",
             "emissive": "#1D4ED8", "emissiveIntensity": 0.4, "roughness": 0.25, "opacity": 0.85,
             "keyframes": [{"frame": S2, "position": [0, 0.5, -10]}, {"frame": S3, "position": [0, 0.1, -15]}]},
        ],
        "characters": {
            "hero": [kf(S2, [-4, 0, 0.5], 0.2, "point", "shocked"),
                     kf(B["b4b"], [-4, 0, 0.5], 0.2, "idle", "shocked"),
                     kf(S3, [-4, 0, 0.5], 0.2, "idle", "shocked")],
            "friend": hold(S2, S3, [1, 0, 0.5], -0.2, "idle", "shocked"),
        },
    })

    # 3. CLASSROOM - why the tides shrink --------------------------------------------
    scenes.append({
        "id": "mechanism", "location": "classroom",
        "boardText": ["TIDES: MOON 2/3", "SUN: 1/3", "NO MOON = SMALL TIDES"],
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

    # 4. BEACH, NIGHT - dark sky, bright stars -----------------------------------------
    star_fx = []
    for i, (sx, sy, sz) in enumerate([(-10, 20, -14), (-5, 23, -16), (0, 19, -15), (5, 22, -17), (10, 20, -14), (-2, 25, -18), (-8, 24, -17), (8, 24, -16)]):
        star_fx.append({"id": f"star{i}", "shape": "sphere", "radius": 0.5, "color": "#F8FAFC",
                        "emissive": "#FFFFFF", "emissiveIntensity": 1.2, "roughness": 0.4,
                        "keyframes": [{"frame": S4, "position": [sx, sy, sz]}, {"frame": S5, "position": [sx, sy, sz]}]})
    scenes.append({
        "id": "stars", "location": "beach", "isNight": True,
        "startFrame": S4, "endFrame": S5,
        "cameraShots": cover(S4, S5, [lambda a, b: wide(a, b, [0, 0, 0.5], 24),
                                       lambda a, b: close_up(a, b, [-4, 0, 0.5]),
                                       lambda a, b: shot(a, b, [0, 4, 21], [0, 4.5, 19], [0, 9, -10], [0, 10, -10], 62)]),
        "fx": star_fx,
        "characters": {
            "hero": hold(S4, S5, [-4, 0, 0.5], 0.2, "point", "shocked"),
            "friend": hold(S4, S5, [1, 0, 0.5], -0.2, "idle", "shocked"),
        },
    })

    # 5. SCHOOLYARD, DAY - the Earth wobbles ----------------------------------------------
    # The globe fx drifts side to side above the schoolyard: the wobble, shown.
    # Globe raised to y 16 and drifted left (2026-11-17 fix) so it clears the
    # school clock and sign, where it read as a blue balloon. Green continent
    # patches ride on its front face and track its keyframes exactly.
    mid = (S5 + S6) // 2
    globe_kf = [{"frame": S5, "position": [-6, 16, -12]}, {"frame": mid, "position": [0, 16.5, -12]},
                {"frame": S6, "position": [-6, 16, -12]}]
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
        "startFrame": S5, "endFrame": S6,
        "cameraShots": cover(S5, S6, [lambda a, b: wide(a, b, [0, 0, 0], 24),
                                       lambda a, b: close_up(a, b, [-2.5, 0, 0]),
                                       lambda a, b: close_up(a, b, [2.5, 0, 0])]),
        "fx": globe_fx,
        "characters": {
            "hero": hold(S5, S6, [-2.5, 0, 0], 0.2, "point", "shocked"),
            "friend": hold(S5, S6, [2.5, 0, 0], -0.2, "idle", "shocked"),
        },
    })

    # 6. LIVING ROOM (yellow), NIGHT - closer ----------------------------------------------
    scenes.append({
        "id": "closer", "location": "living_room", "variant": "yellow", "isNight": True,
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
