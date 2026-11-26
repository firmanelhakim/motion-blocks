"""MY SUPERPOWER SHOWED UP A YEAR LATE - test Short for the Roblox engine.

Build:   python scripts/make_short.py stories/late_power.py --stills
Render:  python scripts/make_short.py stories/late_power.py --skip-tts --render

Topic: every kid gets a superpower on their tenth birthday, but the hero's
shows up a year late - and it is the power to be in two places at once.
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, split_shots, wide  # noqa: F401

TITLE = "MY SUPERPOWER SHOWED UP A YEAR LATE"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this world, every kid gets a superpower on their tenth birthday.", "pause": 0.08},
    {"id": "b2", "text": "Some kids fly to school. Some kids talk to dogs. One kid turned invisible during maths.", "pause": 0.08},
    {"id": "b4", "text": "The principal can read minds, so nobody cheats anymore.", "pause": 0.08},
    {"id": "b5", "text": "On my tenth birthday, I waited all day by the window.", "pause": 0.08},
    {"id": "b6", "text": "Nothing happened. No lightning, no glow, no floating spoons.", "pause": 0.10},
    {"id": "b7", "text": "At school, the bully got super strength, and he lifted my whole desk.", "pause": 0.08},
    {"id": "b8", "text": "My best friend runs so fast, she finishes lunch before it starts.", "pause": 0.08},
    {"id": "b9", "text": "Even my mom got a power. She can hear me thinking about snacks.", "pause": 0.08},
    {"id": "b10", "text": "And me? I got nothing. Not even a sparkle.", "pause": 0.10},
    {"id": "b11", "text": "Then, one year later, on a totally normal Tuesday, it happened.", "pause": 0.08},
    {"id": "b12", "text": "I was late for school, so I wished I could be in two places at once.", "pause": 0.08},
    {"id": "b13", "text": "And suddenly, there were two of me.", "pause": 0.14},
    {"id": "w1", "text": "TWO!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "OF!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "ME!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b14", "text": "One of me went to school. The other one stayed home and played games.", "pause": 0.08},
    {"id": "b15", "text": "It was perfect, until mom grounded both of me.", "pause": 0.08},
    {"id": "b16", "text": "Mom said, one of you is grounded, and the other one is also grounded.", "pause": 0.08},
    {"id": "b17", "text": "The worst part? My clone is better at football than me.", "pause": 0.08},
    {"id": "b19", "text": "But last night, my little brother turned ten. And when the candles went out, there were three of him.", "pause": 0.12},
    {"id": "b20", "text": "So if you see two of me at the park, say hi to both. Only one of us will answer.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/fallen-down.mp3",
    "under_voice": 0.022,
    "gaps": 0.05,
    "dropouts": [("b13+0.3", "w3.end")],
}

SFX = [
    ("b1", "whoosh"),
    ("b1+0.5", "sparkle"),
    ("b2+0.15", "pop", {"f": 600}),
    ("b2+1.6", "pop", {"f": 720}),
    ("b4+0.8", "bell_low"),
    ("b5+0.8", "ding_dong"),
    ("b6+1.0", "sad"),
    ("b7+1.2", "impact"),
    ("b8+0.5", "whoosh"),
    ("b9+1.0", "sparkle"),
    ("b10+0.8", "sad"),
    ("b11", "whoosh"),
    ("b12", "riser", {"dur": 2.0}),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b14+1.0", "pop", {"f": 700}),
    ("b15+1.0", "thud"),
    ("b16+1.2", "bell_low"),
    ("b17+1.0", "pop", {"f": 650}),
    ("b19+2.0", "twist"),
    ("b20+1.5", "sparkle"),
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
BABY = {"extends": "little_brother", "hair": {"style": "curly", "color": "brown"}, "scale": 0.55}
CAST = {
    "hero": HERO,
    "hero_clone": {**HERO},
    "friend": {"extends": "kid_girl", "hair": {"style": "ponytail", "color": "blonde"},
               "top": {"style": "hoodie", "color": "pink", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"color": "white", "sole": "white"}},
    "bully": "bully",
    "mom": {"extends": "real_mom", "hair": {"style": "ponytail", "color": "brown"}},
    "teacher": {"extends": "teacher_woman", "skin": "fair", "hair": {"style": "bun", "color": "blonde"}},
    "principal": "principal",
    "baby": BABY,
    "baby2": {**BABY},
    "baby3": {**BABY},
}


# 4. SCENES ---------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S2 = B["b2"] - 1    # street: powers
    S3 = B["b4"] - 1    # school exterior: principal
    S4 = B["b5"] - 1    # house: birthday wait
    S5 = B["b7"] - 1    # classroom: bully strength
    S6 = B["b8"] - 1    # playground: friend runs fast
    S7 = B["b9"] - 1    # living room: mom power + me nothing
    S8 = B["b11"] - 1   # street: a year later, two of me
    S9 = B["b14"] - 1   # living room: clone life + grounded
    S10 = B["b17"] - 1  # playground: clone football
    S11 = B["b19"] - 1  # living room night: three babies

    HERO_P = [-4.5, 0, 0.5]
    FRIEND_P = [0, 0, 0.5]
    BULLY_P = [4.5, 0, 0.5]

    scenes = []

    # 1. HOOK - aerial town ------------------------------------------------------
    scenes.append({
        "id": "hook", "location": "town_overview", "startFrame": 0, "endFrame": S2,
        "cameraShots": [shot(0, S2, [-10, 62, 74], [-2, 46, 56], [8, 0, -6], [6, 2, -8], 55)],
        "characters": {},
    })

    # 2. STREET - kids show off their powers --------------------------------------
    scenes.append({
        "id": "powers", "location": "street", "startFrame": S2, "endFrame": S3,
        "cameraShots": cover(S2, S3, [lambda a, b: wide(a, b, [0, 0, 0.5], 24),
                                       lambda a, b: medium(a, b, [0, 0, 0.5]),
                                       lambda a, b: close_up(a, b, HERO_P)]),
        "characters": {
            "hero": hold(S2, S3, HERO_P, 0.2, "jump", "laugh"),
            "friend": hold(S2, S3, FRIEND_P, -0.2, "wave", "smile"),
            "bully": hold(S2, S3, BULLY_P, 0, "celebrate", "laugh"),
        },
    })

    # 3. SCHOOL EXTERIOR - the principal reads minds -------------------------------
    scenes.append({
        "id": "principal", "location": "school_exterior", "schoolName": "SUPERTOWN SCHOOL",
        "startFrame": S3, "endFrame": S4,
        "cameraShots": cover(S3, S4, [lambda a, b: wide(a, b, [0, 0, 0], 24),
                                       lambda a, b: medium(a, b, [0, 0, 0])]),
        "characters": {
            "friend": hold(S3, S4, [-4.5, 0, 0], 0.2, "wave", "smile"),
            "hero": hold(S3, S4, [0, 0, 0], 0, "idle", "shocked"),
            "principal": hold(S3, S4, [-2.25, 0, -4.5], 0.0, "point", "deadpan", "clipboard"),
        },
    })

    # 4. HOUSE (blue family) - birthday wait, nothing happens -----------------------
    scenes.append({
        "id": "birthday", "location": "house", "variant": "blue",
        "startFrame": S4, "endFrame": S5,
        "cameraShots": cover(S4, S5, [lambda a, b: medium(a, b, [0, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [0, 0, 0.5])]),
        "characters": {
            "hero": [kf(S4, [0, 0, 0.5], 0, "idle", "smile"), kf(B["b6"], [0, 0, 0.5], 0, "idle", "deadpan"),
                     kf(S5, [0, 0, 0.5], 0, "idle", "deadpan")],
            "mom": hold(S4, S5, [4.5, 0, 0.5], -0.4, "wave", "smile"),
        },
    })

    # 5. CLASSROOM - bully lifts the desk -------------------------------------------
    scenes.append({
        "id": "desk", "location": "classroom",
        "boardText": ["SUPER RULES", "FLYING = A+", "STRENGTH = B+", "MIND READ = ???"],
        "startFrame": S5, "endFrame": S6,
        "cameraShots": split_shots(S5, S6, [lambda a, b: close_up(a, b, [5.5, 0, 3]),
                                             lambda a, b: close_up(a, b, [1.0, 0, 2.5])]),
        "characters": {
            "hero": hold(S5, S6, [1.0, 0, 2.5], 0, "idle", "panic"),
            "bully": hold(S5, S6, [5.5, 0, 3], -0.6, "celebrate", "laugh"),
            "teacher": hold(S5, S6, [-5.5, 0, -6.8], 0.5, "point", "shocked", "pointer"),
        },
    })

    # 6. PLAYGROUND - friend runs so fast ----------------------------------------------
    scenes.append({
        "id": "fast-friend", "location": "playground", "startFrame": S6, "endFrame": S7,
        "cameraShots": split_shots(S6, S7, [lambda a, b: wide(a, b, [0, 0, 0], 24),
                                             lambda a, b: wide(a, b, [2, 0, -1], 24)]),
        "characters": {
            "friend": [kf(S6, [-4.5, 0, -1], HALF, "sprint", "laugh"), kf(S7, [4.5, 0, -1], HALF, "sprint", "laugh")],
            "hero": hold(S6, S7, [0, 0, 4], 0, "idle", "shocked"),
        },
    })

    # 7. LIVING ROOM (blue) - mom hears snack thoughts, me nothing -----------------------
    scenes.append({
        "id": "mom-power", "location": "living_room", "variant": "blue",
        "startFrame": S7, "endFrame": S8,
        "cameraShots": cover(S7, S8, [lambda a, b: wide(a, b, [0, 0, 0.4], 24),
                                       lambda a, b: close_up(a, b, [-4.0, 0, 0.4]),
                                       lambda a, b: close_up(a, b, [4.0, 0, 0.4])]),
        "characters": {
            "hero": [kf(S7, [-4.0, 0, 0.4], 0.9, "idle", "shocked"), kf(B["b10"], [-4.0, 0, 0.4], 0.9, "idle", "deadpan"),
                     kf(S8, [-4.0, 0, 0.4], 0.9, "idle", "deadpan")],
            "mom": [kf(S7, [4.0, 0, 0.4], -0.9, "point", "laugh"), kf(B["b10"], [4.0, 0, 0.4], -0.9, "wave", "smile"),
                    kf(S8, [4.0, 0, 0.4], -0.9, "wave", "smile")],
        },
    })

    # 8. STREET - a year later, two of me -------------------------------------------------
    CLONE_IN = B["b13"]
    scenes.append({
        "id": "two-of-me", "location": "street", "startFrame": S8, "endFrame": S9,
        "cameraShots": cover(S8, S9, [lambda a, b: wide(a, b, [0, 0, 0.5], 24),
                                       lambda a, b: medium(a, b, [0, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [0, 0, 0.5], shake=0.08)]),
        "characters": {
            "hero": [kf(S8, [-6.0, 0, 0.5], HALF, "walk", "smile"), kf(B["b12"], [0, 0, 0.5], HALF, "walk", "smile"),
                     kf(B["b12"] + 6, [0, 0, 0.5], 0, "point", "shocked"), kf(S9, [0, 0, 0.5], 0, "celebrate", "laugh")],
            "hero_clone": [kf(S8, OFF, 0, "idle", "smile"), kf(CLONE_IN, OFF, 0, "idle", "smile"),
                           kf(CLONE_IN + 1, [4.5, 0, 0.5], 0, "celebrate", "laugh"), kf(S9, [4.5, 0, 0.5], 0, "celebrate", "laugh")],
        },
    })

    # 9. LIVING ROOM (blue) - clone life, grounded twice ------------------------------------
    scenes.append({
        "id": "grounded", "location": "living_room", "variant": "blue",
        "startFrame": S9, "endFrame": S10,
        "cameraShots": cover(S9, S10, [lambda a, b: wide(a, b, [0, 0, 0.4], 24),
                                        lambda a, b: close_up(a, b, [-4.5, 0, 0.4]),
                                        lambda a, b: close_up(a, b, [4.5, 0, 0.4])]),
        "characters": {
            "hero": [kf(S9, [-4.5, 0, 0.4], 0.9, "dance", "laugh"), kf(B["b15"], [-4.5, 0, 0.4], 0.9, "idle", "deadpan"),
                     kf(S10, [-4.5, 0, 0.4], 0.9, "idle", "deadpan")],
            "hero_clone": [kf(S9, [0, 0, 0.4], -0.9, "idle", "smile"), kf(B["b15"], [0, 0, 0.4], -0.9, "idle", "panic"),
                           kf(S10, [0, 0, 0.4], -0.9, "idle", "panic")],
            "mom": [kf(S9, [4.5, 0, 0.4], -0.9, "idle", "smile"), kf(B["b15"], [4.5, 0, 0.4], -0.9, "point", "angry"),
                    kf(S10, [4.5, 0, 0.4], -0.9, "point", "angry")],
        },
    })

    # 10. PLAYGROUND - clone is better at football -------------------------------------------
    scenes.append({
        "id": "football", "location": "playground", "startFrame": S10, "endFrame": S11,
        "cameraShots": cover(S10, S11, [lambda a, b: wide(a, b, [0, 0, 1], 24),
                                         lambda a, b: medium(a, b, [0, 0, 1]),
                                         lambda a, b: close_up(a, b, [-4.5, 0, 1])]),
        "characters": {
            "hero": hold(S10, S11, [-4.5, 0, 1], 0.9, "idle", "deadpan"),
            "hero_clone": hold(S10, S11, [0, 0, 1], -0.9, "celebrate", "laugh"),
            "friend": hold(S10, S11, [4.5, 0, 1], -0.9, "wave", "laugh"),
        },
    })

    # 11. LIVING ROOM (blue), NIGHT - three babies ----------------------------------------------
    BLUE = B["b19"] + 58
    scenes.append({
        "id": "three-babies", "location": "living_room", "variant": "blue", "isNight": True,
        "startFrame": S11, "endFrame": END,
        "cameraShots": cover(S11, END, [
            lambda a, b: shot(a, b, [0, 7.0, 18.5], [0, 5.8, 15], [0, 3.8, 0], [0, 3.4, 0.5], 56),
            lambda a, b: close_up(a, b, [0, 0, 1.2], scale=0.55),
            lambda a, b: medium(a, b, [0, 0, 1.2]),
        ]),
        "characters": {
            "baby": [kf(S11, [0, 0, 1.2], 0, "idle", "smile"), kf(BLUE, [0, 0, 1.2], 0, "wave", "laugh"),
                     kf(END, [0, 0, 1.2], 0, "wave", "laugh")],
            "baby2": [kf(S11, OFF, 0, "idle", "smile"), kf(BLUE, OFF, 0, "idle", "smile"),
                      kf(BLUE + 1, [-4.5, 0, 1.2], 0, "wave", "laugh"), kf(END, [-4.5, 0, 1.2], 0, "wave", "laugh")],
            "baby3": [kf(S11, OFF, 0, "idle", "smile"), kf(BLUE, OFF, 0, "idle", "smile"),
                      kf(BLUE + 1, [4.5, 0, 1.2], 0, "wave", "laugh"), kf(END, [4.5, 0, 1.2], 0, "wave", "laugh")],
            "hero": [kf(S11, [-4.5, 0, -3.5], 0.9, "idle", "smile"), kf(BLUE - 4, [-4.5, 0, -3.5], 0.9, "idle", "smile"),
                     kf(BLUE, [-4.5, 0, -3.5], 0.9, "idle", "shocked"), kf(END, [-4.5, 0, -3.5], 0.9, "idle", "shocked")],
            "mom": [kf(S11, [4.5, 0, -3.5], -0.9, "idle", "smile"), kf(BLUE - 4, [4.5, 0, -3.5], -0.9, "idle", "smile"),
                    kf(BLUE, [4.5, 0, -3.5], -0.9, "idle", "panic"), kf(END, [4.5, 0, -3.5], -0.9, "idle", "panic")],
        },
    })

    return scenes
