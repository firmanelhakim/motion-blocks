"""DIALOGUE TEST — chat bubbles between Bolt Boy and a friend.
Tests the ShortsHUD bubble rendering (2D bubble above the speaker's head).
Run: python scripts/make_short.py stories/dialogue_test.py --stills
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, wide  # noqa: F401

TITLE = "EVERYONE TALKS IN BUBBLES"

BEATS = [
    {"id": "b1", "text": "In this town, nobody talks out loud. Everyone speaks in bubbles.", "pause": 0.08},
    {"id": "b2", "text": "Bolt Boy says hi.", "pause": 0.08},
    {"id": "b3", "text": "His friend says hi back.", "pause": 0.08},
    {"id": "b4", "text": "Then she asks him a question.", "pause": 0.08},
    {"id": "b5", "text": "And he answers with a grin.", "pause": 0.3},
]

MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05, "dropouts": []}
SFX = [
    ("b1", "whoosh"),
    ("b2", "pop"),
    ("b3", "pop"),
    ("b4", "pop"),
    ("b5", "sparkle"),
]

CAST = {
    "hero": {"kit": "boltboy"},
    "friend": "kid_girl",
}


def scenes(T):
    S2 = T.B["b2"] - 1
    END = T.END
    HERO_P, FRIEND_P = [-2.5, 0, 1.5], [2.5, 0, 1.5]
    # Dialogue: hero speaks on b2, friend replies on b3, friend asks on b4,
    # hero answers on b5. Each bubble shows from its keyframe to the next.
    B2, B3, B4, B5 = T.B["b2"], T.B["b3"], T.B["b4"], T.B["b5"]
    return [
        {   # hook: aerial town
            "id": "hook", "location": "town_overview", "startFrame": 0, "endFrame": S2,
            "cameraShots": [shot(0, S2, [-10, 62, 74], [-2, 46, 56], [8, 0, -6], [6, 2, -8], 55)],
            "characters": {},
        },
        {   # dialogue on the street
            "id": "dialogue", "location": "street", "startFrame": S2, "endFrame": END,
            "cameraShots": cover(S2, END, [
                lambda a, b: medium(a, b, [0, 0, 1.5]),
                lambda a, b: close_up(a, b, HERO_P),
                lambda a, b: close_up(a, b, FRIEND_P),
            ]),
            "characters": {
                "hero": [
                    kf(S2, HERO_P, 0.5, "idle", "smile"),
                    kf(B2, HERO_P, 0.5, "wave", "grin", bubble="Hi! I'm Bolt Boy!"),
                    kf(B3, HERO_P, 0.5, "idle", "smile"),
                    kf(B5, HERO_P, 0.5, "wave", "grin", bubble="Of course! Let's go!"),
                    kf(END, HERO_P, 0.5, "idle", "grin"),
                ],
                "friend": [
                    kf(S2, FRIEND_P, -0.5, "idle", "smile"),
                    kf(B3, FRIEND_P, -0.5, "wave", "smile", bubble="Hi Bolt Boy!"),
                    kf(B4, FRIEND_P, -0.5, "point", "smile", bubble="Want to race to school?"),
                    kf(B5, FRIEND_P, -0.5, "idle", "laugh"),
                    kf(END, FRIEND_P, -0.5, "idle", "smile"),
                ],
            },
        },
    ]
