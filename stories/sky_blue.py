"""WHY IS THE SKY BLUE? - science explainer.

Batch of 5 storyboards (the maintainer, 2026-11-17): video 5 of 5.
Structure is a "why" explainer (question -> test -> answer), NOT another
"what if": hook (look up) -> classroom mechanism (scattering) -> street
day (the blue everywhere, sunbeam fx) -> street sunset (the red payoff) ->
living-room closer. No timeline shape, no beach, no space.

The science (Rayleigh scattering): sunlight looks white but is every
colour mixed together. Air molecules scatter blue light far more than red
(scattering scales as 1/wavelength^4, so blue scatters ~4-5x more than red),
so blue reaches your eyes from every direction and the whole sky looks
blue. At sunset the light travels much further through the air, the blue
is scattered away on the journey, and red and orange are what is left -
that is why sunsets are red. All plain-language, standard figures,
simplified for a Short.

Fresh visuals: a sunset palette (skyColor orange on the street - never
used), sunbeam fx (tall translucent shafts), a "why" structure instead of
"what if", new music (sky-blue.wav). The teacher is in the standard white
blouse, placed beside the desk at x -3.0 - check the stills for the sun_off
blending problem and switch her to teal if it appears.

Build:   python scripts/make_short.py stories/sky_blue.py --stills
Render:  python scripts/make_short.py stories/sky_blue.py --skip-tts --render
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, split_shots, wide  # noqa: F401

TITLE = "WHY IS THE SKY BLUE?"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this town, someone asked a question nobody could answer. Why is the sky blue?", "pause": 0.08},
    {"id": "b2", "text": "It looks blue. But the air has no colour at all. So where does the blue come from?", "pause": 0.10},
    {"id": "b2b", "text": "The Sun is white, the air is clear, and yet the sky is blue. Something must be happening in between.", "pause": 0.08},
    {"id": "b3", "text": "Sunlight looks white. But white light is really every colour mixed together.", "pause": 0.10},
    {"id": "b4", "text": "When sunlight hits the air, the tiny bits of air scatter the blue light in every direction.", "pause": 0.10},
    {"id": "b5", "text": "Blue scatters far more than red. So blue reaches your eyes from everywhere — and the whole sky looks blue.", "pause": 0.10},
    {"id": "b5b", "text": "Red light mostly passes straight through. Blue light bounces everywhere.", "pause": 0.08},
    {"id": "b6", "text": "It is not paint in the sky. It is sunlight, bounced around by the air.", "pause": 0.08},
    {"id": "b6b", "text": "Look up on a clear day. The blue is everywhere — above you, beside you, all around.", "pause": 0.08},
    {"id": "b7", "text": "And at sunset, the light has further to travel. The blue gets scattered away on the journey.", "pause": 0.10},
    {"id": "b8", "text": "What is left is red and orange. That is why sunsets are red — the blue ran out on the way.", "pause": 0.10},
    {"id": "b8b", "text": "The same air that makes the sky blue makes the sunset red. It is all the same trick.", "pause": 0.08},
    {"id": "b9", "text": "So the sky is blue because of the air, and sunsets are red because of the distance.", "pause": 0.10},
    {"id": "b10", "text": "Next time you look up, remember: you are seeing sunlight, scattered by the sky itself.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/sky-blue.wav",
    "under_voice": 0.022,
    "gaps": 0.05,
}

SFX = [
    ("b1", "pop", {"f": 600}),
    ("b1+0.5", "whoosh"),
    ("b2b+0.5", "pop", {"f": 600}),
    ("b8b+0.5", "sparkle"),
    ("b3+0.5", "sparkle"),
    ("b4+0.5", "pop", {"f": 600}),
    ("b6+0.5", "sparkle"),
    ("b7+0.5", "sparkle"),
    ("b9+0.5", "reveal"),
    ("b10+1.5", "twist"),
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

    S2 = B["b3"] - 1    # classroom: the mechanism
    S3 = B["b6"] - 1    # street, day: the blue everywhere, sunbeams
    S4 = B["b7"] - 1    # street, sunset: the red payoff
    S5 = B["b9"] - 1    # living room (blue), night: closer

    scenes = []

    # 1. HOOK - street, day. Both look up at the blue sky --------------------------------
    # Wide is a STATIC shot (2026-11-17 fix): wide()'s push drags the
    # door/window edges across the frame and reads as flicker. Same opening
    # framing as wide([0, 0, 0.5], 24), zero push.
    scenes.append({
        "id": "hook", "location": "street",
        "startFrame": 0, "endFrame": S2,
        "cameraShots": cover(0, S2, [lambda a, b: shot(a, b, [0, 7.4, 24.5], [0, 7.4, 24.5], [0, 4.8, -0.5], [0, 4.8, -0.5], 58),
                                      lambda a, b: close_up(a, b, [-4, 0, 0.5]),
                                      lambda a, b: close_up(a, b, [1, 0, 0.5])]),
        "characters": {
            "hero": hold(0, S2, [-4, 0, 0.5], 0.2, "point", "shocked"),
            "friend": hold(0, S2, [1, 0, 0.5], -0.2, "point", "shocked"),
        },
    })

    # 2. CLASSROOM - the mechanism ------------------------------------------------------------
    # Board-wide is a STATIC shot (2026-11-17 fix): the push drags the floor
    # tile grid across the frame and reads as flicker. Same framing.
    scenes.append({
        "id": "mechanism", "location": "classroom",
        "boardText": ["SUNLIGHT = ALL COLOURS", "BLUE SCATTERS MOST", "RED PASSES THROUGH"],
        "startFrame": S2, "endFrame": S3,
        "cameraShots": cover(S2, S3, [lambda a, b: shot(a, b, [0, 7.4, 23], [0, 7.4, 23], [0, 4.8, -1], [0, 4.8, -1], 58),
                                       lambda a, b: close_up(a, b, [-0.5, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [-3.0, 0, -4.5])]),
        "characters": {
            "teacher": hold(S2, S3, [-3.0, 0, -4.5], 0.5, "point", "deadpan", "pointer"),
            "hero": hold(S2, S3, [-0.5, 0, 0.5], 0, "idle", "smile"),
            "friend": hold(S2, S3, [4.0, 0, 0.5], 0, "idle", "smile"),
        },
    })

    # 3. STREET, DAY - the blue everywhere. Sunbeam shafts in the air ------------------------------
    scenes.append({
        "id": "blue", "location": "street",
        "startFrame": S3, "endFrame": S4,
        "cameraShots": cover(S3, S4, [lambda a, b: wide(a, b, [0, 0, 0.5], 24),
                                       lambda a, b: close_up(a, b, [-4, 0, 0.5]),
                                       lambda a, b: shot(a, b, [-1, 3, 15], [-1, 3.5, 13], [-1, 8, -6], [-1, 8, -6], 58)]),
        "fx": [
            {"id": "beam1", "shape": "box", "size": [1.2, 16, 1.2], "color": "#FDE68A",
             "emissive": "#F59E0B", "emissiveIntensity": 0.8, "roughness": 0.4, "opacity": 0.7,
             "keyframes": [{"frame": S3, "position": [4, 8, -6]}, {"frame": S4, "position": [4, 8, -6]}]},
            {"id": "beam2", "shape": "box", "size": [1.0, 14, 1.0], "color": "#FDE68A",
             "emissive": "#F59E0B", "emissiveIntensity": 0.7, "roughness": 0.4, "opacity": 0.65,
             "keyframes": [{"frame": S3, "position": [-3, 7, -8]}, {"frame": S4, "position": [-3, 7, -8]}]},
        ],
        "characters": {
            "hero": hold(S3, S4, [-4, 0, 0.5], 0.2, "point", "smile"),
            "friend": hold(S3, S4, [2, 0, 0.5], -0.2, "idle", "smile"),
        },
    })

    # 4. STREET, SUNSET - the red payoff. Same street, orange sky ------------------------------------
    scenes.append({
        "id": "sunset", "location": "street", "skyColor": "#F97316",
        "startFrame": S4, "endFrame": S5,
        "cameraShots": cover(S4, S5, [lambda a, b: wide(a, b, [0, 0, 0.5], 24),
                                       lambda a, b: close_up(a, b, [-4, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [1, 0, 0.5])]),
        "characters": {
            "hero": hold(S4, S5, [-4, 0, 0.5], 0.2, "point", "shocked"),
            "friend": hold(S4, S5, [1, 0, 0.5], -0.2, "idle", "smile"),
        },
    })

    # 5. LIVING ROOM (blue), NIGHT - closer ---------------------------------------------------------------
    scenes.append({
        "id": "closer", "location": "living_room", "variant": "blue", "isNight": True,
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
