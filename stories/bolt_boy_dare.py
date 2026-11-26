"""BOLT BOY'S DARE — "Bolt Boy's dare."

Short dialogue story, lead: Bolt Boy (kit `{"kit": "boltboy"}` — the only
story in this batch he leads). A friend dares him to race to school, jump
the fence, climb the tree. Three quick bubble exchanges, he says yes every
time. Then the twist: she dares him to stand perfectly still for one
whole minute — and he cannot.

Minimal narrator: the beats set up each dare, the bubbles carry the
dialogue. Every dare gets a close-up on the speaker, so no bubble hides.

Build (fake timings — Kokoro is not installed on this VM):
    python3 /tmp/build_stories.py bolt_boy_dare
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, orbit, shot, split_shots, wide  # noqa: F401

TITLE = "BOLT BOY'S DARE"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this town, there is a kid who never says no to a dare.", "pause": 0.08},
    {"id": "b2", "text": "His name is Bolt Boy, and his friend knows how to use it.", "pause": 0.08},
    {"id": "b3", "text": "One morning, she dared him to race her to school.", "pause": 0.08},
    {"id": "b4", "text": "Bolt Boy did not even think. He was already running.", "pause": 0.08},
    {"id": "b5", "text": "At the school gate, she dared him to jump the fence.", "pause": 0.08},
    {"id": "b6", "text": "He jumped it clean, and landed with a grin.", "pause": 0.08},
    {"id": "b7", "text": "In the playground, she dared him to climb the highest tree.", "pause": 0.08},
    {"id": "b8", "text": "He leapt to the very top, and waved down at the town.", "pause": 0.08},
    {"id": "b9", "text": "Three dares, three yeses, and Bolt Boy had not broken a sweat.", "pause": 0.10},
    {"id": "b10", "text": "So his friend thought hard, and came up with the hardest dare of all.", "pause": 0.10},
    {"id": "b11", "text": "Stand perfectly still, she said, for one whole minute.", "pause": 0.12},
    {"id": "w1", "text": "STILL!", "voice": "af_bella", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "ONE!", "voice": "af_bella", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "MINUTE!", "voice": "af_bella", "shout": True, "pause": 0.18},
    {"id": "b12", "text": "Bolt Boy froze. For three whole seconds. Then his foot started tapping.", "pause": 0.08},
    {"id": "b13", "text": "His arms wiggled, his head bobbed, and he burst into a dance.", "pause": 0.08},
    {"id": "b14", "text": "His friend laughed until her sides hurt. The dare had finally won.", "pause": 0.08},
    {"id": "b15", "text": "Bolt Boy never said no. Not once. Not even to standing still.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05,
         "dropouts": [("b11+0.3", "w3.end")]}
SFX = [
    ("b1", "whoosh"),
    ("b2+0.5", "sparkle"),
    ("b3+0.4", "pop", {"f": 700}),
    ("b4", "whoosh"),
    ("b5+0.4", "pop", {"f": 800}),
    ("b6+0.5", "sparkle"),
    ("b7+0.4", "pop", {"f": 750}),
    ("b8+0.6", "sparkle"),
    ("b9+0.5", "laugh"),
    ("b10+0.4", "riser", {"dur": 1.6}),
    ("b11+0.5", "ding_dong"),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b12+0.8", "pop", {"f": 900}),
    ("b13+0.5", "laugh"),
    ("b14+0.6", "laugh"),
    ("b15+1.0", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
CAST = {
    "hero": {"kit": "boltboy"},
    "friend": {"extends": "kid_girl", "hair": {"style": "ponytail", "color": "blonde"},
               "top": {"style": "hoodie", "color": "pink", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"},
               "shoes": {"color": "white", "sole": "white"}},
}


# 4. SCENES --------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END
    S_RACE = B["b3"] - 1    # street: the race dare
    S_FENCE = B["b5"] - 1   # school exterior: the fence jump
    S_TREE = B["b7"] - 1    # playground: the climb
    S_STILL = B["b10"] - 1  # playground: the stillness dare
    S_END = B["b15"] - 1    # street: the twist

    # Hero on the right, friend on the left, so the race sprint runs right
    # (toward the school) away from her — no spacing clash on the path.
    HERO_P, FRIEND_P = [2.5, 0, 1.0], [-2.5, 0, 1.0]

    # The dare tree (RoundTree at [2.5, 0, -2.5] in the Playground); its
    # canopy top is ~8.4, so feet at 8.1 plant him on it.
    TREE_TOP = [2.5, 8.1, -2.5]

    # The race: Bolt Boy sprints from the back of the street to the front.
    # The fence: a jump at the school gate. The tree: a climb in the park.
    # The stillness dare: he tries idle, breaks into dance.
    return [
        {   # Hook: aerial town, three angles.
            "id": "hook", "location": "town_overview", "startFrame": 0, "endFrame": S_RACE,
            "cameraShots": [
                shot(0, S_RACE // 3, [-10, 62, 74], [-7, 56, 67], [8, 0, -6], [7, 1, -7], 55),
                shot(S_RACE // 3, 2 * S_RACE // 3, [-7, 56, 67], [-4, 50, 61], [7, 1, -7], [6, 2, -8], 55),
                shot(2 * S_RACE // 3, S_RACE, [-4, 50, 61], [-2, 46, 56], [6, 2, -8], [6, 2, -8], 55),
            ],
            "characters": {},
        },
        {   # The race dare: friend dares, Bolt Boy says yes and sprints.
            # Crossroads (open crosswalk) so the sprint has room; he runs
            # right, away from her, so the path never comes near her.
            "id": "race", "location": "crossroads",
            "startFrame": S_RACE, "endFrame": S_FENCE,
            "cameraShots": [
                close_up(S_RACE, B["b3"] + 30, FRIEND_P),
                close_up(B["b3"] + 30, B["b4"], HERO_P),
                medium(B["b4"], S_FENCE, [0, 0, 0.5]),
            ],
            "characters": {
                "hero": [kf(S_RACE, HERO_P, -0.4, "idle", "grin"),
                         kf(B["b3"] + 30, HERO_P, -0.4, "wave", "grin", bubble="Yes! Easy!"),
                         kf(B["b4"], [2.5, 0, 0.5], HALF, "sprint", "grin"),
                         kf(B["b4"] + 45, [9.0, 0, 0.5], HALF, "sprint", "grin"),
                         kf(B["b4"] + 51, [9.0, 0, 0.5], 0, "idle", "grin"),
                         kf(S_FENCE, [9.0, 0, 0.5], 0, "idle", "grin")],
                "friend": [kf(S_RACE, FRIEND_P, 0.4, "idle", "smile"),
                           kf(B["b3"], FRIEND_P, 0.4, "point", "smile", bubble="Race me to school!"),
                           kf(B["b4"], FRIEND_P, 0.4, "idle", "shocked"),
                           kf(S_FENCE, FRIEND_P, 0.4, "idle", "shocked")],
            },
        },
        {   # The fence jump: friend dares, Bolt Boy jumps it clean.
            "id": "fence", "location": "school_exterior", "schoolName": "DARE SCHOOL",
            "startFrame": S_FENCE, "endFrame": S_TREE,
            "cameraShots": [
                close_up(S_FENCE, B["b5"] + 30, FRIEND_P),
                close_up(B["b5"] + 30, B["b6"], HERO_P),
                low_angle(B["b6"], S_TREE, HERO_P),
            ],
            "characters": {
                "hero": [kf(S_FENCE, HERO_P, -0.4, "idle", "grin"),
                         kf(B["b5"] + 30, HERO_P, -0.4, "wave", "grin", bubble="Watch this!"),
                         kf(B["b6"], HERO_P, -0.4, "jump", "laugh"),
                         kf(B["b6"] + 30, HERO_P, -0.4, "idle", "grin"),
                         kf(S_TREE, HERO_P, -0.4, "idle", "grin")],
                "friend": [kf(S_FENCE, FRIEND_P, 0.4, "idle", "smile"),
                           kf(B["b5"], FRIEND_P, 0.4, "point", "smile", bubble="Jump the fence!"),
                           kf(B["b6"], FRIEND_P, 0.4, "idle", "shocked"),
                           kf(S_TREE, FRIEND_P, 0.4, "idle", "shocked")],
            },
        },
        {   # The climb: friend dares, Bolt Boy leaps onto the tree and waves.
            # The leap is staged, not faked: he rises from the ground to the
            # canopy (TREE_TOP) during the tilt-up shot, waves from up there
            # ("I'm already up!"), then hops down before the stillness dare.
            "id": "tree", "location": "playground",
            "startFrame": S_TREE, "endFrame": S_STILL,
            "cameraShots": [
                close_up(S_TREE, B["b7"] + 30, FRIEND_P),
                close_up(B["b7"] + 30, B["b8"], HERO_P),
                # Tilt-up following the leap: ground hero -> treetop hero.
                shot(B["b8"], B["b9"], [2.5, 2.0, 8.0], [2.5, 1.2, 6.5],
                     [2.5, 4.4, 1.0], [2.5, 12.5, -2.5], 50),
                # Wide on the tree: hero on top, friend below; he hops down
                # in the last second so the stillness dare starts on the ground.
                shot(B["b9"], S_STILL, [0, 8, 16], [0, 7.5, 14.5],
                     [0.5, 7, -1], [0.5, 7, -1], 55),
            ],
            "characters": {
                "hero": [kf(S_TREE, HERO_P, -0.4, "idle", "grin"),
                         kf(B["b7"] + 30, HERO_P, -0.4, "wave", "grin"),
                         kf(B["b8"], HERO_P, -0.4, "jump", "laugh"),
                         # Leap arcs UP IN FRONT of the tree (z=1.5, clear of
                         # the canopy front edge ~0.1) and only then back onto
                         # the canopy — a straight ground->treetop lerp would
                         # clip straight through the canopy ball.
                         kf(B["b8"] + 12, [2.5, 6.5, 1.5], -0.4, "jump", "laugh"),
                         kf(B["b8"] + 25, TREE_TOP, -0.4, "idle", "laugh"),
                         kf(B["b8"] + 40, TREE_TOP, -0.4, "wave", "laugh", bubble="I'm already up!"),
                         kf(B["b9"], TREE_TOP, -0.4, "wave", "laugh"),
                         kf(S_STILL - 30, TREE_TOP, -0.4, "jump", "laugh"),
                         # Hop down arcs OUT IN FRONT of the tree (z=1.5, clear
                         # of the canopy front edge ~0.1) before dropping —
                         # a straight treetop->ground lerp descends through
                         # the canopy ball (the maintainer caught it in v2).
                         kf(S_STILL - 15, [2.5, 6.5, 1.5], -0.4, "jump", "laugh"),
                         kf(S_STILL, HERO_P, -0.4, "idle", "grin")],
                "friend": [kf(S_TREE, FRIEND_P, 0.4, "idle", "smile"),
                           kf(B["b7"], FRIEND_P, 0.4, "point", "smile", bubble="Climb the tree!"),
                           kf(B["b8"], FRIEND_P, 0.4, "idle", "shocked"),
                           kf(S_STILL, FRIEND_P, 0.4, "idle", "shocked")],
            },
        },
        {   # The stillness dare: he freezes, then his foot taps, then he dances.
            "id": "still", "location": "playground",
            "startFrame": S_STILL, "endFrame": S_END,
            "cameraShots": cover(S_STILL, S_END, [
                lambda a, b: medium(a, b, [0, 0, 1.0]),
                lambda a, b: close_up(a, b, HERO_P, shake=0.06),
                lambda a, b: close_up(a, b, FRIEND_P),
                lambda a, b: wide(a, b),
            ]),
            "characters": {
                "hero": [kf(S_STILL, HERO_P, -0.4, "idle", "grin"),
                         kf(B["b11"], HERO_P, -0.4, "idle", "panic", bubble="Still? For a MINUTE?"),
                         kf(B["w1"], HERO_P, -0.4, "idle", "panic"),
                         kf(B["b12"], HERO_P, -0.4, "idle", "panic"),
                         kf(B["b13"], HERO_P, -0.4, "dance", "laugh"),
                         kf(S_END, HERO_P, -0.4, "dance", "laugh")],
                "friend": [kf(S_STILL, FRIEND_P, 0.4, "idle", "smile"),
                           kf(B["b11"], FRIEND_P, 0.4, "point", "smile", bubble="Stand still. One minute."),
                           kf(B["b13"], FRIEND_P, 0.4, "idle", "laugh"),
                           kf(S_END, FRIEND_P, 0.4, "idle", "laugh")],
            },
        },
        {   # The twist: he never said no. Not once.
            "id": "twist", "location": "street",
            "startFrame": S_END, "endFrame": END,
            "cameraShots": split_shots(S_END, END, [
                lambda a, b: medium(a, b, [0, 0, 0.5]),
                lambda a, b: close_up(a, b, HERO_P),
            ]),
            "characters": {
                "hero": hold(S_END, END, HERO_P, -0.4, "idle", "grin"),
                "friend": hold(S_END, END, FRIEND_P, 0.4, "idle", "laugh"),
            },
        },
    ]
