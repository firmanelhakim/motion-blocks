"""KIT HEROES TEST — all four kit characters lead a story scene.
Verifies CasualMan, WingedBoy and ClassicNoob render through the story
pipeline (RobloxShortComposition) the same way BoltBoy does.
Run: python scripts/make_short.py stories/kit_heroes_test.py --stills
(TEST ONLY — do not schedule or publish.)
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, wide  # noqa: F401

TITLE = "FOUR HEROES, ONE STREET"

BEATS = [
    {"id": "b1", "text": "In this town, four heroes walk the street.", "pause": 0.08},
    {"id": "b2", "text": "Bolt Boy leads the way.", "pause": 0.08},
    {"id": "b3", "text": "Casual Man follows, calm as ever.", "pause": 0.08},
    {"id": "b4", "text": "Winged Boy and Classic Noob wave hello.", "pause": 0.08},
    {"id": "b5", "text": "Four heroes, one street.", "pause": 0.3},
]

MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05, "dropouts": []}
SFX = [
    ("b1", "whoosh"),
    ("b2", "step"),
    ("b3", "step"),
    ("b4", "pop"),
    ("b5", "sparkle"),
]

CAST = {
    "hero_bolt": {"kit": "boltboy"},
    "hero_casual": {"kit": "casualman"},
    "hero_winged": {"kit": "wingedboy"},
    "hero_noob": {"kit": "classicnoob"},
}


def scenes(T):
    S2 = T.B["b2"] - 1
    END = T.END
    # Four heroes in a row, 6 studs apart, facing the camera.
    BOLT_P, CASUAL_P, WINGED_P, NOOB_P = [-9, 0, 2], [-3, 0, 2], [3, 0, 2], [9, 0, 2]
    BOLT_F, CASUAL_F, WINGED_F, NOOB_F = [-9, 0, -2], [-3, 0, -2], [3, 0, -2], [9, 0, -2]
    B2, B3, B4, B5 = T.B["b2"], T.B["b3"], T.B["b4"], T.B["b5"]
    return [
        {   # hook: aerial town
            "id": "hook", "location": "town_overview", "startFrame": 0, "endFrame": S2,
            "cameraShots": [shot(0, 75, [-10, 62, 74], [-2, 46, 56], [8, 0, -6], [6, 2, -8], 55),
                          shot(75, S2, [-2, 46, 56], [6, 30, 40], [6, 2, -8], [4, 0, -4], 55)],
            "characters": {},
        },
        {   # the four heroes: walk forward, then wave
            "id": "heroes", "location": "crossroads", "startFrame": S2, "endFrame": END,
            "cameraShots": cover(S2, END, [
                lambda a, b: wide(a, b, [0, 0, 0], dist=35.0),
                lambda a, b: medium(a, b, [0, 0, 0]),
            ]),
            "characters": {
                "hero_bolt": [
                    kf(S2, BOLT_P, 0, "idle", "grin"),
                    kf(B2, BOLT_P, 0, "walk", "grin"),
                    kf(B3, BOLT_F, 0, "walk", "grin"),
                    kf(B4, BOLT_F, 0, "wave", "grin"),
                    kf(END, BOLT_F, 0, "wave", "grin"),
                ],
                "hero_casual": [
                    kf(S2, CASUAL_P, 0, "idle", "smile"),
                    kf(B2, CASUAL_P, 0, "walk", "smile"),
                    kf(B3, CASUAL_F, 0, "walk", "smile"),
                    kf(B4, CASUAL_F, 0, "wave", "smile"),
                    kf(END, CASUAL_F, 0, "wave", "smile"),
                ],
                "hero_winged": [
                    kf(S2, WINGED_P, 0, "idle", "cool"),
                    kf(B2, WINGED_P, 0, "walk", "cool"),
                    kf(B3, WINGED_F, 0, "walk", "cool"),
                    kf(B4, WINGED_F, 0, "wave", "cool"),
                    kf(END, WINGED_F, 0, "wave", "cool"),
                ],
                "hero_noob": [
                    kf(S2, NOOB_P, 0, "idle", "smile"),
                    kf(B2, NOOB_P, 0, "walk", "smile"),
                    kf(B3, NOOB_F, 0, "walk", "smile"),
                    kf(B4, NOOB_F, 0, "wave", "smile"),
                    kf(END, NOOB_F, 0, "wave", "smile"),
                ],
            },
        },
    ]
