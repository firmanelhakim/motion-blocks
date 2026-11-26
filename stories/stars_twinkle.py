"""WHY DO STARS TWINKLE? - science explainer.

Week 1 storyboard (the maintainer, 2026-11-17): video 5 of 7.
Structure: hook (looking up at the night sky) -> space (the beam bends) ->
classroom demo (a star point vs a planet disc) -> street night (find Venus)
-> closer. A "why" explainer like sky_blue, not a "what if". No shouts,
gentle clear-night mood.

The science: a star is so far away that its light arrives as a single thin
beam. The air between the star and you is always moving, and moving air
bends light — so the star seems to wobble, and that wobble is the twinkle.
The star is not shaking; the air is. Planets do not twinkle as much
because they look like tiny discs, not points: many beams side by side, so
when the air bends one beam the others stay steady. All plain-language,
standard figures, simplified for a Short.

Fresh visuals: the classroom demo (a small glowing star point vs a bigger
steady planet sphere, floating beside the teacher), the twinkle in space
(automatic in the 'space' location — stars pulse on their own phases), new
music (stars-twinkle.wav). The teacher is in the standard white blouse,
placed beside the desk at x -3.0 (not on it).

Build:   python scripts/make_short.py stories/stars_twinkle.py --stills
Render:  python scripts/make_short.py stories/stars_twinkle.py --skip-tts --render
"""
import math  # noqa: F401

from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, shot, split_shots, static_shot, wide  # noqa: F401

TITLE = "WHY DO STARS TWINKLE?"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this town, the stars never sit still. They twinkle all night long — and here is why.", "pause": 0.08},
    {"id": "b2", "text": "A star is so far away that its light arrives as a single thin beam. Like a laser pointer.", "pause": 0.10},
    {"id": "b3", "text": "But between the star and you, there is air. And the air is always moving.", "pause": 0.10},
    {"id": "b3b", "text": "You cannot see the air moving. But you can see what it does to the light.", "pause": 0.08},
    {"id": "b4", "text": "The moving air bends the light, a little this way, a little that way. So the star seems to wobble.", "pause": 0.10},
    {"id": "b5", "text": "That wobble is the twinkle. The star is not shaking — the air is.", "pause": 0.10},
    {"id": "b5b", "text": "Hot air rises, cold air sinks, wind blows sideways. The sky is a river you cannot see.", "pause": 0.08},
    {"id": "b6", "text": "And here is the test. Planets do not twinkle as much as stars.", "pause": 0.10},
    {"id": "b7", "text": "Because a planet looks like a tiny disc, not a point. Many beams of light, side by side.", "pause": 0.10},
    {"id": "b8", "text": "When the air bends one beam, the others stay steady. So the planet looks calm.", "pause": 0.08},
    {"id": "b8b", "text": "Look up tonight. Find a star that twinkles, then find a planet that does not. Venus is the easiest one.", "pause": 0.10},
    {"id": "b9", "text": "Stars are points. Planets are discs. That is the whole trick.", "pause": 0.10},
    {"id": "b10", "text": "So the next time a star winks at you, you will know: it is not the star. It is the air.", "pause": 0.10},
    {"id": "b11", "text": "And if the air ever stood still, the stars would stop twinkling — and shine like diamonds.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/stars-twinkle.wav",
    "under_voice": 0.022,
    "gaps": 0.05,
}

SFX = [
    ("b1", "whoosh"),
    ("b1+0.5", "sparkle"),
    ("b2+0.5", "pop", {"f": 600}),
    ("b3+0.5", "swish"),
    ("b3b+0.5", "swish"),
    ("b4+0.5", "sparkle"),
    ("b5+0.5", "pop", {"f": 600}),
    ("b6+0.5", "bell_low"),
    ("b7+0.5", "pop", {"f": 600}),
    ("b8b+0.5", "sparkle"),
    ("b9+0.5", "pop", {"f": 600}),
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


def _star_point(a, b):
    """The demo pair, floating beside the teacher: a small bright star point
    (r=0.5, white, high emissive) and a bigger steady planet sphere (r=1.2,
    pale yellow). The board carries the words; the sizes carry the idea."""
    return [
        {"id": "star-point", "shape": "sphere", "radius": 0.5, "color": "#F8FAFC",
         "emissive": "#FFFFFF", "emissiveIntensity": 1.6, "roughness": 0.3,
         "keyframes": [{"frame": a, "position": [-6.5, 8, -2]}, {"frame": b, "position": [-6.5, 8, -2]}]},
        {"id": "planet-disc", "shape": "sphere", "radius": 1.2, "color": "#FDE68A",
         "emissive": "#F59E0B", "emissiveIntensity": 0.5, "roughness": 0.5,
         "keyframes": [{"frame": a, "position": [6.5, 8, -2]}, {"frame": b, "position": [6.5, 8, -2]}]},
    ]


def _bright_star(a, b):
    """One bright star high in the sky for the space scenes — the hero points
    at it while the starfield twinkles around it (automatic in 'space')."""
    return [{"id": "bright-star", "shape": "sphere", "radius": 1.0, "color": "#F8FAFC",
             "emissive": "#FFFFFF", "emissiveIntensity": 1.8, "roughness": 0.3,
             "keyframes": [{"frame": a, "position": [0, 22, -16]}, {"frame": b, "position": [0, 22, -16]}]}]


# 4. SCENES ---------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S2 = B["b3"] - 1    # space: the beam bends
    S3 = B["b6"] - 1    # classroom: the demo
    S4 = B["b9"] - 1    # street, night: find Venus
    S5 = B["b11"] - 1   # living room (blue), night: closer

    scenes = []

    # 1. HOOK - street, night: looking up at the twinkling sky -------------------------
    scenes.append({
        "id": "hook", "location": "street", "isNight": True,
        "startFrame": 0, "endFrame": S2,
        "cameraShots": cover(0, S2, [lambda a, b: shot(a, b, [0, 4, 21], [0, 4.5, 19], [0, 9, -10], [0, 10, -10], 62),
                                      lambda a, b: low_angle(a, b, [-2.5, 0, 0.5], dist=9, eye_height=1.2),
                                      lambda a, b: close_up(a, b, [2.5, 0, 0.5])]),
        "characters": {
            "hero": hold(0, S2, [-2.5, 0, 0.5], 0.2, "point", "shocked"),
            "friend": hold(0, S2, [2.5, 0, 0.5], -0.2, "idle", "shocked"),
        },
    })

    # 2. SPACE - the beam bends in the moving air ------------------------------------------
    scenes.append({
        "id": "beam", "location": "space", "skyColor": "#000000",
        "startFrame": S2, "endFrame": S3,
        "cameraShots": cover(S2, S3, [lambda a, b: static_shot(a, b, [0, 8, 21], [0, 4.5, -3], 58),
                                       lambda a, b: close_up(a, b, [-3, 0, 0.5]),
                                       lambda a, b: shot(a, b, [0, 6, 18], [0, 7, 16], [0, 12, -8], [0, 13, -8], 58)]),
        "fx": _bright_star(S2, S3),
        "characters": {
            "hero": hold(S2, S3, [-3, 0, 0.5], 0.2, "point", "shocked"),
            "friend": hold(S2, S3, [2.5, 0, 0.5], -0.2, "idle", "shocked"),
        },
    })

    # 3. CLASSROOM - the demo: star point vs planet disc ---------------------------------------
    scenes.append({
        "id": "mechanism", "location": "classroom",
        "boardText": ["STAR = A POINT", "PLANET = A DISC", "AIR BENDS THE LIGHT"],
        "startFrame": S3, "endFrame": S4,
        "cameraShots": cover(S3, S4, [lambda a, b: shot(a, b, [0, 7.4, 23], [0, 7.0, 20.5], [0, 4.8, -1], [0, 4.7, -1], 58),
                                       lambda a, b: close_up(a, b, [-0.5, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [-3.0, 0, -4.5])]),
        "fx": _star_point(S3, S4),
        "characters": {
            "teacher": hold(S3, S4, [-3.0, 0, -4.5], 0.5, "point", "deadpan", "pointer"),
            "hero": hold(S3, S4, [-0.5, 0, 0.5], 0, "idle", "smile"),
            "friend": hold(S3, S4, [4.0, 0, 0.5], 0, "idle", "smile"),
        },
    })

    # 4. STREET, NIGHT - find Venus ----------------------------------------------------------------
    scenes.append({
        "id": "venus", "location": "street", "isNight": True,
        "startFrame": S4, "endFrame": S5,
        "cameraShots": cover(S4, S5, [lambda a, b: shot(a, b, [0, 4, 21], [0, 4.5, 19], [0, 9, -10], [0, 10, -10], 62),
                                       lambda a, b: low_angle(a, b, [-2.5, 0, 0.5], dist=9, eye_height=1.2),
                                       lambda a, b: close_up(a, b, [2.5, 0, 0.5])]),
        "characters": {
            "hero": hold(S4, S5, [-2.5, 0, 0.5], 0.2, "point", "shocked"),
            "friend": hold(S4, S5, [2.5, 0, 0.5], -0.2, "idle", "shocked"),
        },
    })

    # 5. LIVING ROOM (blue), NIGHT - closer ----------------------------------------------------------
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
