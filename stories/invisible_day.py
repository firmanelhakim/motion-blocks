"""INVISIBLE DAY — "What if you were invisible for a day?"

Science explainer, lead: cool_kid "Max" (never a story lead before).
He wakes up invisible, pranks the town, then needs help and nobody can
find him — until his friend hears his voice.

STAGING (no invisibility in the engine): the hero is parked OFF
([0, -80, 0], hidden) during the invisible beats while the other
characters react to empty air, and a small floating ball fx shows his
unseen hand at play. He is visible at the start (bedroom mirror) and
fades back in at the sunset reveal, parked ON 5+ studs from his friend.

Build (fake timings — Kokoro is not installed on this VM):
    python3 /tmp/build_stories.py invisible_day
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, orbit, shot, split_shots, wide  # noqa: F401

TITLE = "INVISIBLE FOR A DAY"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this town, one morning, Max woke up invisible.", "pause": 0.08},
    {"id": "b2", "text": "No reflection, no shadow, just an empty bed.", "pause": 0.08},
    {"id": "b3", "text": "At first, it was the best prank ever. He moved the chairs.", "pause": 0.08},
    {"id": "b4", "text": "He whispered in the teacher's ear. She jumped a mile.", "pause": 0.08},
    {"id": "b5", "text": "He stole the bully's lunch, right from his hands.", "pause": 0.08},
    {"id": "b6", "text": "But by lunch, the fun wore off. Nobody saw him smile.", "pause": 0.10},
    {"id": "b7", "text": "He waved at his best friend. She walked straight through him.", "pause": 0.08},
    {"id": "b8", "text": "He joined the game. The ball rolled past. No one passed it back.", "pause": 0.08},
    {"id": "b9", "text": "Then he tripped and fell. Nobody came to help.", "pause": 0.10},
    {"id": "b10", "text": "Alone and invisible, he felt small for the first time.", "pause": 0.14},
    {"id": "w1", "text": "HELP!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "HERE!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "b11", "text": "His friend stopped. A voice came from nowhere.", "pause": 0.08},
    {"id": "b12", "text": "She held out her hand, and felt his. She smiled.", "pause": 0.08},
    {"id": "b13", "text": "As the sun went down, Max faded back in.", "pause": 0.12},
    {"id": "b14", "text": "That night, he left his shoes by the door. Just in case.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05,
         "dropouts": [("b10+0.3", "w2.end")]}
SFX = [
    ("b1", "whoosh"),
    ("b2+0.5", "sparkle"),
    ("b3+0.4", "pop", {"f": 700}),
    ("b4+0.6", "pop", {"f": 900}),
    ("b5+0.5", "pop_down"),
    ("b6+0.4", "sad"),
    ("b7+0.8", "whoosh"),
    ("b8+0.6", "pop", {"f": 600}),
    ("b9+0.4", "thud"),
    ("b10", "bell_low"),
    ("w1", "impact"),
    ("w2", "impact"),
    ("b11+0.5", "sparkle"),
    ("b12+0.8", "reveal"),
    ("b13+1.0", "sparkle"),
    ("b14+1.5", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
CAST = {
    "hero": {"extends": "cool_kid", "hair": {"style": "spikyAnime", "color": "blue"},
             "top": {"style": "hoodie", "color": "black", "secondary": "cyan"},
             "bottom": {"style": "jeans", "color": "darkDenim"},
             "shoes": {"color": "white", "sole": "white"},
             "accessories": ["sunglasses"]},
    "friend": {"extends": "kid_girl", "hair": {"style": "ponytail", "color": "blonde"},
               "top": {"style": "hoodie", "color": "pink", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"},
               "shoes": {"color": "white", "sole": "white"}},
    "teacher": "teacher_woman",
    "bully": "bully",
    "mom": {"extends": "real_mom", "hair": {"style": "ponytail", "color": "brown"}},
}


# 4. SCENES --------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END
    # Scene boundaries (cut just before the beat about the new place).
    S_BED = B["b2"] - 1      # bedroom: mirror, empty bed
    S_SCH = B["b3"] - 1      # classroom: chairs, whisper, lunch
    S_PLY = B["b6"] - 1      # playground: wave, ball, trip
    S_STR = B["b10"] - 1     # street at sunset: alone, shouts, reveal
    S_LIV = B["b14"] - 1     # living room, night: shoes by the door

    HERO_BED = [-4.0, 0, -2.0]
    MOM_BED = [4.0, 0, -2.0]
    # The floating ball fx: a small sphere that drifts across the playground
    # while Max is invisible, showing his unseen hand at play.
    ball_kf = [{"frame": S_PLY, "position": [-6, 1.0, 0]},
               {"frame": B["b8"], "position": [0, 1.0, 0]},
               {"frame": B["b9"], "position": [5, 1.0, 0]},
               {"frame": S_STR, "position": [5, 1.0, 0]}]
    ball_fx = [{"id": "ball", "shape": "sphere", "radius": 0.6, "color": "#F97316",
                "emissive": "#EA580C", "emissiveIntensity": 0.3, "roughness": 0.5,
                "keyframes": ball_kf}]

    return [
        {   # Hook: aerial town, two angles (b1 is short; three would be <1 s each).
            "id": "hook", "location": "town_overview", "startFrame": 0, "endFrame": S_BED,
            "cameraShots": [
                shot(0, S_BED // 2, [-10, 62, 74], [-7, 56, 67], [8, 0, -6], [7, 1, -7], 55),
                shot(S_BED // 2, S_BED, [-7, 56, 67], [-4, 50, 61], [7, 1, -7], [6, 2, -8], 55),
            ],
            "characters": {},
        },
        {   # Bedroom: Max looks in the mirror, shocked — then *poof*, gone.
            # He is visible until B["b2"], then parked OFF (invisible).
            "id": "bedroom", "location": "bedroom", "variant": "blue",
            "startFrame": S_BED, "endFrame": S_SCH,
            "cameraShots": cover(S_BED, S_SCH, [
                lambda a, b: medium(a, b, [0, 0, -2.0]),
                lambda a, b: close_up(a, b, HERO_BED),
                lambda a, b: low_angle(a, b, MOM_BED),
            ]),
            "characters": {
                "hero": [kf(S_BED, HERO_BED, 0.9, "idle", "smile"),
                         kf(B["b2"], HERO_BED, 0.9, "idle", "shocked"),
                         kf(B["b2"] + 1, OFF, 0.9, "idle", "shocked"),
                         kf(S_SCH, OFF, 0.9, "idle", "shocked")],
                "mom": [kf(S_BED, MOM_BED, -0.9, "idle", "smile"),
                        kf(B["b2"], MOM_BED, -0.9, "idle", "shocked"),
                        kf(S_SCH, MOM_BED, -0.9, "idle", "shocked")],
            },
        },
        {   # Classroom: Max is OFF (invisible). Teacher jumps, bully loses lunch.
            "id": "classroom", "location": "classroom",
            "boardText": ["TODAY", "BE KIND", "SEE EVERYONE"],
            "startFrame": S_SCH, "endFrame": S_PLY,
            "cameraShots": cover(S_SCH, S_PLY, [
                lambda a, b: wide(a, b),
                lambda a, b: close_up(a, b, [-5.5, 0, 3.0]),
                lambda a, b: medium(a, b, [0, 0, 2.5]),
                lambda a, b: close_up(a, b, [5.5, 0, 3.0]),
            ]),
            "characters": {
                "hero": hold(S_SCH, S_PLY, OFF, 0, "idle", "smile"),
                "teacher": [kf(S_SCH, [-5.5, 0, 3.0], 0.4, "idle", "smile"),
                            kf(B["b4"], [-5.5, 0, 3.0], 0.4, "idle", "shocked"),
                            kf(S_PLY, [-5.5, 0, 3.0], 0.4, "idle", "shocked")],
                "bully": [kf(S_SCH, [5.5, 0, 3.0], -0.4, "idle", "cool", "bloxy_cola"),
                          kf(B["b5"], [5.5, 0, 3.0], -0.4, "idle", "panic"),
                          kf(S_PLY, [5.5, 0, 3.0], -0.4, "idle", "panic")],
                "friend": hold(S_SCH, S_PLY, [0, 0, -2.0], 0, "idle", "smile"),
            },
        },
        {   # Playground: the floating ball, the wave-through, the trip.
            "id": "playground", "location": "playground",
            "startFrame": S_PLY, "endFrame": S_STR,
            "fx": ball_fx,
            "cameraShots": cover(S_PLY, S_STR, [
                lambda a, b: wide(a, b),
                lambda a, b: medium(a, b, [0, 0, 0]),
                lambda a, b: low_angle(a, b, [0, 0, 0]),
                lambda a, b: close_up(a, b, [-4.5, 0, 1.0]),
            ]),
            "characters": {
                "hero": hold(S_PLY, S_STR, OFF, 0, "idle", "smile"),
                "friend": [kf(S_PLY, [-4.5, 0, 1.0], 0.5, "wave", "smile"),
                           kf(B["b7"], [-4.5, 0, 1.0], 0.5, "idle", "shocked"),
                           kf(B["b9"], [-4.5, 0, 1.0], 0.5, "idle", "panic"),
                           kf(S_STR, [-4.5, 0, 1.0], 0.5, "idle", "panic")],
                "bully": hold(S_PLY, S_STR, [4.5, 0, 1.0], -0.5, "idle", "laugh"),
            },
        },
        {   # Street at sunset: alone, the shouts, then Max fades back in.
            # He parks ON at the reveal, 5+ studs from his friend.
            # The HELP! bubble (w1) is anchored at his voice — the empty
            # spot where he stands invisibly ([-2.5, 0, 0.5], where he fades
            # back in at b13). The ball drifts over to the same spot, so the
            # ball (his unseen hand) and the bubble (his voice) mark one
            # place, then rolls aside as he fades in.
            "id": "sunset", "location": "street", "isNight": False,
            "startFrame": S_STR, "endFrame": S_LIV,
            "fx": [{"id": "ball", "shape": "sphere", "radius": 0.6, "color": "#F97316",
                    "emissive": "#EA580C", "emissiveIntensity": 0.3, "roughness": 0.5,
                    "keyframes": [{"frame": S_STR, "position": [5, 1.0, 0]},
                                  {"frame": B["w1"], "position": [-2.5, 1.0, 0.5]},
                                  {"frame": B["b13"], "position": [-4.5, 1.0, 2.0]},
                                  {"frame": S_LIV, "position": [-4.5, 1.0, 2.0]}]}],
            "cameraShots": cover(S_STR, S_LIV, [
                lambda a, b: wide(a, b),
                lambda a, b: medium(a, b, [0, 0, 0.5]),
                lambda a, b: close_up(a, b, [-2.5, 0, 0.5], shake=0.06),
                lambda a, b: close_up(a, b, [2.5, 0, 0.5]),
            ]),
            "characters": {
                "hero": [kf(S_STR, OFF, 0, "idle", "panic"),
                         kf(B["w1"], OFF, 0, "idle", "panic", bubble="HELP!",
                            bubble_anchor=[-2.5, 3.4, 0.5]),
                         kf(B["w2"], OFF, 0, "idle", "panic"),
                         kf(B["b12"], OFF, 0, "idle", "smile"),
                         kf(B["b13"], [-2.5, 0, 0.5], 0.3, "idle", "smile"),
                         kf(S_LIV, [-2.5, 0, 0.5], 0.3, "wave", "grin")],
                "friend": [kf(S_STR, [2.5, 0, 0.5], -0.3, "idle", "panic"),
                           kf(B["b11"], [2.5, 0, 0.5], -0.3, "idle", "shocked"),
                           kf(B["b12"], [2.5, 0, 0.5], -0.3, "idle", "smile"),
                           kf(S_LIV, [2.5, 0, 0.5], -0.3, "wave", "laugh")],
            },
        },
        {   # Living room, night: shoes by the door, just in case.
            "id": "night", "location": "living_room", "variant": "blue", "isNight": True,
            "startFrame": S_LIV, "endFrame": END,
            "cameraShots": split_shots(S_LIV, END, [
                lambda a, b: medium(a, b, [0, 0, 0]),
                lambda a, b: close_up(a, b, [-2.5, 0, 0.5]),
                lambda a, b: close_up(a, b, [2.5, 0, 0.5]),
            ]),
            "characters": {
                "hero": hold(S_LIV, END, [-2.5, 0, 0.5], 0.4, "idle", "cool"),
                "mom": hold(S_LIV, END, [2.5, 0, 0.5], -0.4, "idle", "smile"),
            },
        },
    ]
