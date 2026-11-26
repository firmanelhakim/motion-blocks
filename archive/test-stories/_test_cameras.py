"""TEST-ONLY story — verifies the three new camera helpers (static_shot,
orbit, low_angle). NEVER for publishing. Run:
    python scripts/make_short.py stories/_test_cameras.py --stills
"""
from shorts.scene import (  # noqa: F401
    HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, orbit,
    shot, split_shots, static_shot, wide,
)

TITLE = "TEST CAMERAS"

BEATS = [
    {"id": "b1", "text": "In this town, the camera learned three new tricks.", "pause": 0.08},
    {"id": "b2", "text": "First, it learned to hold perfectly still.", "pause": 0.08},
    {"id": "b3", "text": "Then it learned to circle around the Earth.", "pause": 0.08},
    {"id": "b4", "text": "And it learned to look up from the ground.", "pause": 0.08},
    {"id": "b5", "text": "Three new moves, ready for next week.", "pause": 0.3},
]

MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05}
SFX = [
    ("b1", "whoosh"),
    ("b3+0.5", "sparkle"),
    ("b5+0.5", "twist"),
]

CAST = {
    "hero": {"extends": "kid_boy", "hair": {"style": "spikyAnime", "color": "blue"},
             "top": {"style": "hoodie", "color": "royal", "secondary": "white"},
             "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"color": "white", "sole": "white"},
             "freckles": True},
    "friend": {"extends": "kid_girl", "hair": {"style": "ponytail", "color": "blonde"},
               "top": {"style": "hoodie", "color": "pink", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"color": "white", "sole": "white"}},
}


def scenes(T):
    S2, S3, S4, END = T.B["b3"] - 1, T.B["b4"] - 1, T.B["b5"] - 1, T.END
    HERO_P, FRIEND_P = [-2.5, 0, 0.5], [2.5, 0, 0.5]

    # Globe for the orbit test: blue Earth + one green continent, fixed in place.
    globe_fx = [
        {"id": "earth", "shape": "sphere", "radius": 3.0, "color": "#38BDF8",
         "emissive": "#1D4ED8", "emissiveIntensity": 0.4, "roughness": 0.7,
         "keyframes": [{"frame": S2, "position": [0, 14, -12]}, {"frame": S3, "position": [0, 14, -12]}]},
        {"id": "continent", "shape": "sphere", "radius": 1.2, "color": "#22C55E",
         "emissive": "#16A34A", "emissiveIntensity": 0.25, "roughness": 0.8,
         "keyframes": [{"frame": S2, "position": [1.0, 14.7, -10.1]}, {"frame": S3, "position": [1.0, 14.7, -10.1]}]},
    ]

    return [
        {   # static shots: the frame must not move at all
            "id": "static", "location": "street", "startFrame": 0, "endFrame": S2,
            "cameraShots": split_shots(0, S2, [
                lambda a, b: static_shot(a, b, [0, 7.4, 24], [0, 4.8, -1], 58),
                lambda a, b: static_shot(a, b, [0, 5.6, 13], [0, 4.3, 0.5], 50),
            ]),
            "characters": {
                "hero": hold(0, S2, HERO_P, 0.2, "idle", "smile"),
                "friend": hold(0, S2, FRIEND_P, -0.2, "idle", "smile"),
            },
        },
        {   # orbit: camera arcs around the globe, no actors in frame
            "id": "orbit", "location": "space", "skyColor": "#000000",
            "startFrame": S2, "endFrame": S3,
            "cameraShots": [orbit(S2, S3, [0, 14, -12], 18, 10, -0.45, 0.45, [0, 14, -12], 58)],
            "fx": globe_fx,
            "characters": {},
        },
        {   # low angle: eye near the ground, looking up at the hero
            "id": "lowangle", "location": "street", "startFrame": S3, "endFrame": S4,
            "cameraShots": [low_angle(S3, S4, [-2.5, 0, 0.5])],
            "characters": {
                "hero": hold(S3, S4, HERO_P, 0.2, "idle", "shocked"),
                "friend": hold(S3, S4, FRIEND_P, -0.2, "idle", "smile"),
            },
        },
        {   # closer: one more static wide to close
            "id": "closer", "location": "street", "startFrame": S4, "endFrame": END,
            "cameraShots": [static_shot(S4, END, [0, 7.4, 24], [0, 4.8, -1], 58)],
            "characters": {
                "hero": hold(S4, END, HERO_P, 0.2, "wave", "smile"),
                "friend": hold(S4, END, FRIEND_P, -0.2, "wave", "smile"),
            },
        },
    ]
