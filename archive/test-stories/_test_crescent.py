"""TEST-ONLY diagnostic — is the Crescent shape a crescent or a disc?
NEVER for publishing. Run:
    python scripts/make_short.py stories/_test_crescent.py --stills
"""
from shorts.scene import kf, static_shot, split_shots  # noqa: F401

TITLE = "TEST CRESCENT"

BEATS = [
    {"id": "b1", "text": "In this world, the moon is a crescent.", "pause": 0.3},
]

MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05}
SFX = []

CAST = {}


def scenes(T):
    END = T.END
    return [
        {
            "id": "crescent", "location": "space", "skyColor": "#000000",
            "startFrame": 0, "endFrame": END,
            "fx": [
                {"id": "moon", "shape": "crescent", "radius": 3.0,
                 "color": "#FDE68A", "emissive": "#FBBF24", "emissiveIntensity": 1.6,
                 "roughness": 0.5,
                 "keyframes": [{"frame": 0, "position": [0, 7, -10]},
                              {"frame": END, "position": [0, 7, -10]}]},
            ],
            "cameraShots": split_shots(0, END, [
                lambda a, b: static_shot(a, b, [0, 7, 8], [0, 7, -10], 50),
            ]),
            "characters": {},
        },
    ]
