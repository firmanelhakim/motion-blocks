"""GRAVITY SWITCHES OFF FOR 10 SECONDS - revival Short.

Build:   python scripts/make_short.py stories/gravity_off.py --stills
Render:  python scripts/make_short.py stories/gravity_off.py --skip-tts --render

Topic: in this town, gravity switches off for ten seconds every day at noon.
Science beats (kept honest): things float; without gravity nothing falls,
things just keep moving (inertia); ten seconds is too short for the air to
escape, so you can still breathe; when gravity comes back, everything falls.

Floating is staged with real y positions (the renderer passes keyframe y
straight through to the character group). Camera helpers ignore actor y,
so every floated close-up uses a manual shot() aimed at head height + y.
Spacing is checked in 2D (x,z only), so horizontal separation stays >= 4.5
even when actors float at different heights.
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, split_shots, wide  # noqa: F401

TITLE = "GRAVITY SWITCHES OFF FOR 10 SECONDS"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this town, gravity switches off for ten seconds every day at noon.", "pause": 0.08},
    {"id": "b2", "text": "Ten seconds. That's all. But ten seconds is enough for everything to float.", "pause": 0.08},
    {"id": "b3", "text": "Desks float. Lunch trays float. Even the teacher floats, right in the middle of maths.", "pause": 0.08},
    {"id": "b4", "text": "My best friend was sprinting across the playground when it happened. She never came down.", "pause": 0.08},
    {"id": "b5", "text": "She just kept gliding, straight across the park. Without gravity, nothing falls. Things just keep moving.", "pause": 0.10},
    {"id": "b6", "text": "The bully tried to float away once. He grabbed the flagpole and held on for dear life.", "pause": 0.08},
    {"id": "b7", "text": "And the air? The air stays. Ten seconds is too short for the whole sky to float away.", "pause": 0.08},
    {"id": "b8", "text": "You can still breathe. You just can't stand still.", "pause": 0.10},
    {"id": "b9", "text": "But here is the part nobody tells you. Gravity always comes back.", "pause": 0.10},
    {"id": "b10", "text": "And when it does, everything that is floating... falls.", "pause": 0.12},
    {"id": "b11", "text": "Yesterday, my friend floated all the way up to the ceiling, and she couldn't get down.", "pause": 0.08},
    {"id": "b12", "text": "I grabbed her hand just as the clock hit ten.", "pause": 0.08},
    {"id": "w1", "text": "GRAVITY!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "IS!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "BACK!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b13", "text": "We all landed in a big pile on the floor. Well, most of us did.", "pause": 0.08},
    {"id": "b14", "text": "The bully landed on the teacher's desk. He says it was on purpose.", "pause": 0.08},
    {"id": "b15", "text": "But last night, I checked the calendar. Tomorrow is Saturday. And gravity doesn't take weekends off.", "pause": 0.10},
    {"id": "b16", "text": "So if you see me floating past your window tomorrow morning, say hi. And hold on to something.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/fallen-down.mp3",
    "under_voice": 0.022,
    "gaps": 0.05,
    "dropouts": [("b12+0.3", "w3.end")],
}

SFX = [
    ("b1", "whoosh"),
    ("b1+0.5", "sparkle"),
    ("b2+0.5", "pop", {"f": 600}),
    ("b3+1.0", "pop", {"f": 720}),
    ("b4+0.5", "whoosh"),
    ("b5+1.5", "pop", {"f": 650}),
    ("b6+1.0", "laugh"),
    ("b7+0.8", "sparkle"),
    ("b8+0.8", "pop", {"f": 700}),
    ("b9+0.8", "bell_low"),
    ("b10", "riser", {"dur": 2.0}),
    ("b11+1.0", "whoosh"),
    ("b12+0.5", "whoosh"),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b13+1.0", "thud"),
    ("b14+1.0", "laugh"),
    ("b15+2.0", "twist"),
    ("b16+1.5", "sparkle"),
]

# 3. CAST ----------------------------------------------------------------------
# Same hero/friend as late_power, so the channel has one recognisable cast.
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
    "bully": "bully",
    "mom": {"extends": "real_mom", "hair": {"style": "ponytail", "color": "brown"}},
    "teacher": {"extends": "teacher_woman", "skin": "fair", "hair": {"style": "bun", "color": "blonde"}},
}


# 4. SCENES ---------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S2 = B["b2"] - 1    # classroom: everything floats
    S3 = B["b4"] - 1    # playground: friend never comes down
    S4 = B["b6"] - 1    # school exterior: bully at the flagpole
    S5 = B["b7"] - 1    # street: the air stays
    S6 = B["b9"] - 1    # classroom: countdown, friend rises to the ceiling
    S7 = B["b12"] - 1   # classroom: grab, gravity back, landing
    S8 = B["b15"] - 1   # living room night: Saturday twist

    scenes = []

    # 1. HOOK - aerial town ------------------------------------------------------
    scenes.append({
        "id": "hook", "location": "town_overview", "startFrame": 0, "endFrame": S2,
        "cameraShots": [shot(0, S2 // 2, [-10, 62, 74], [-6, 54, 65], [8, 0, -6], [7, 1, -7], 55),
                        shot(S2 // 2, S2, [-6, 54, 65], [-2, 46, 56], [7, 1, -7], [6, 2, -8], 55)],
        "characters": {},
    })

    # 2. CLASSROOM - everything floats (teacher, hero, friend at y 2-2.5) --------
    # Manual shots: close_up/wide ignore actor y, so aim at head height + y.
    scenes.append({
        "id": "float-class", "location": "classroom",
        "boardText": ["GRAVITY OFF", "12:00 = FLOAT", "HOLD ON TIGHT"],
        "startFrame": S2, "endFrame": S3,
        "cameraShots": cover(S2, S3, [
            lambda a, b: shot(a, b, [0, 9.5, 21], [0, 9.0, 18.5], [0, 5.5, 0], [0, 5.2, 0], 58),
            lambda a, b: shot(a, b, [-0.5, 7.5, 7.5], [-0.5, 7.3, 6.3], [-0.5, 6.9, 0.5], [-0.5, 6.9, 0.5], 44),
            lambda a, b: shot(a, b, [-5.5, 7.0, 2.5], [-5.5, 6.8, 1.3], [-5.5, 6.4, -4.5], [-5.5, 6.4, -4.5], 44),
        ]),
        "characters": {
            "teacher": hold(S2, S3, [-5.5, 2.0, -4.5], 0.5, "jump", "panic"),
            "hero": hold(S2, S3, [-0.5, 2.5, 0.5], 0, "jump", "laugh"),
            "friend": hold(S2, S3, [4.5, 2.5, 0.5], 0, "jump", "laugh"),
        },
    })

    # 3. PLAYGROUND - friend sprint-glides mid-air, hero watches -------------------
    scenes.append({
        "id": "glide", "location": "playground", "startFrame": S3, "endFrame": S4,
        "cameraShots": cover(S3, S4, [lambda a, b: wide(a, b, [0, 0, 0], 24),
                                       lambda a, b: wide(a, b, [2, 0, -1], 24),
                                       lambda a, b: wide(a, b, [-2, 0, -1], 24)]),
        "characters": {
            "friend": [kf(S3, [-4.5, 2.0, -1], HALF, "sprint", "laugh"),
                       kf(S4, [4.5, 2.0, -1], HALF, "sprint", "laugh")],
            "hero": hold(S3, S4, [0, 0, 4], 0, "idle", "shocked"),
        },
    })

    # 4. SCHOOL EXTERIOR - bully clings to the flagpole ----------------------------
    scenes.append({
        "id": "flagpole", "location": "school_exterior", "schoolName": "GRAVITY SCHOOL",
        "startFrame": S4, "endFrame": S5,
        "cameraShots": cover(S4, S5, [lambda a, b: wide(a, b, [0, 0, 0], 24),
                                       lambda a, b: close_up(a, b, [4.5, 0, 0])]),
        "characters": {
            "bully": hold(S4, S5, [4.5, 0, 0], -0.6, "celebrate", "panic"),
            "hero": hold(S4, S5, [-4.5, 0, 0], 0.6, "point", "laugh"),
        },
    })

    # 5. STREET - the air stays, everyone on the ground ----------------------------
    scenes.append({
        "id": "air-stays", "location": "street", "startFrame": S5, "endFrame": S6,
        "cameraShots": cover(S5, S6, [lambda a, b: wide(a, b, [0, 0, 0.5], 24),
                                       lambda a, b: close_up(a, b, [0, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [-4.5, 0, 0.5])]),
        "characters": {
            "hero": hold(S5, S6, [-4.5, 0, 0.5], 0.2, "idle", "smile"),
            "friend": hold(S5, S6, [0, 0, 0.5], -0.2, "wave", "smile"),
        },
    })

    # 6. CLASSROOM - countdown: friend rises to the ceiling, hero reaches up ---------
    RISE = B["b11"]
    MID9 = (S6 + B["b10"]) // 2
    scenes.append({
        "id": "countdown", "location": "classroom",
        "boardText": ["GRAVITY OFF", "12:00 = FLOAT", "HOLD ON TIGHT"],
        "startFrame": S6, "endFrame": S7,
        # Manual cuts aligned to the beats: the actors change height mid-scene,
        # so cover() lands the high close-ups while they are still rising.
        "cameraShots": [
            shot(S6, MID9, [0, 7.4, 20], [0, 7.0, 17.5], [0, 4.8, -1], [0, 4.7, -1], 58),
            close_up(MID9, B["b10"], [-5.5, 0, -4.5]),
            shot(B["b10"], B["b11"], [4.5, 5.0, 8], [4.5, 4.8, 7], [4.5, 4.4, 0.5], [4.5, 4.4, 0.5], 50),
            shot(B["b11"], B["b11"] + 45, [-0.5, 5.6, 12], [-0.5, 6.6, 11], [-0.5, 4.8, 0.5], [-0.5, 6.5, 0.5], 44),
            shot(B["b11"] + 45, S7, [0, 9.5, 21], [0, 9.0, 18.5], [0, 5.5, 0], [0, 5.2, 0], 58),
        ],
        "characters": {
            "teacher": [kf(S6, [-5.5, 0, -4.5], 0.5, "point", "deadpan", "pointer"),
                        kf(RISE, [-5.5, 0, -4.5], 0.5, "point", "shocked", "pointer"),
                        kf(S7, [-5.5, 0, -4.5], 0.5, "point", "shocked", "pointer")],
            "hero": [kf(S6, [-0.5, 0, 0.5], 0, "idle", "smile"),
                     kf(RISE, [-0.5, 0, 0.5], 0, "idle", "shocked"),
                     kf(RISE + 30, [-0.5, 2.5, 0.5], 0, "jump", "shocked"),
                     kf(S7, [-0.5, 2.5, 0.5], 0, "jump", "shocked")],
            "friend": [kf(S6, [4.5, 0, 0.5], 0, "idle", "smile"),
                       kf(B["b10"], [4.5, 0, 0.5], 0, "idle", "shocked"),
                       kf(RISE, [4.5, 0, 0.5], 0, "idle", "shocked"),
                       kf(RISE + 30, [4.5, 5.0, 0.5], 0, "jump", "panic"),
                       kf(S7, [4.5, 5.0, 0.5], 0, "jump", "panic")],
        },
    })

    # 7. CLASSROOM - gravity back: everyone lands, bully on the teacher's desk -------
    LAND = B["w1"]
    scenes.append({
        "id": "gravity-back", "location": "classroom",
        "boardText": ["GRAVITY OFF", "12:00 = FLOAT", "HOLD ON TIGHT"],
        "startFrame": S7, "endFrame": S8,
        "cameraShots": cover(S7, S8, [lambda a, b: wide(a, b, [0, 0, 0.5], 24),
                                       lambda a, b: close_up(a, b, [-2.0, 0, 1.0]),
                                       lambda a, b: close_up(a, b, [4.5, 0, 0.5])]),
        "characters": {
            "hero": [kf(S7, [-0.5, 2.5, 0.5], 0, "jump", "shocked"),
                     kf(LAND, [-2.0, 0, 1.0], 0, "celebrate", "laugh"),
                     kf(S8, [-2.0, 0, 1.0], 0, "celebrate", "laugh")],
            "friend": [kf(S7, [4.5, 5.0, 0.5], 0, "jump", "panic"),
                       kf(LAND, [4.5, 0, 0.5], 0, "panting", "shocked"),
                       kf(S8, [4.5, 0, 0.5], 0, "panting", "shocked")],
            "bully": [kf(S7, OFF, 0, "idle", "deadpan"),
                      kf(LAND, OFF, 0, "idle", "deadpan"),
                      kf(LAND + 1, [-1.0, 0, -4.5], 0, "panting", "deadpan"),
                      kf(S8, [-1.0, 0, -4.5], 0, "panting", "deadpan")],
            "teacher": hold(S7, S8, [-5.5, 0, -6.8], 0.5, "point", "angry", "pointer"),
        },
    })

    # 8. LIVING ROOM (blue), NIGHT - Saturday twist ------------------------------------
    scenes.append({
        "id": "saturday", "location": "living_room", "variant": "blue", "isNight": True,
        "startFrame": S8, "endFrame": END,
        "cameraShots": cover(S8, END, [lambda a, b: wide(a, b, [0, 0, 0.4], 24),
                                        lambda a, b: close_up(a, b, [-4.0, 0, 0.4]),
                                        lambda a, b: close_up(a, b, [4.0, 0, 0.4])]),
        "characters": {
            "hero": [kf(S8, [-4.0, 0, 0.4], 0.9, "idle", "deadpan"),
                     kf(B["b16"], [-4.0, 0, 0.4], 0.9, "idle", "smile"),
                     kf(END, [-4.0, 0, 0.4], 0.9, "idle", "smile")],
            "mom": [kf(S8, [4.0, 0, 0.4], -0.9, "wave", "smile"),
                    kf(END, [4.0, 0, 0.4], -0.9, "wave", "smile")],
        },
    })

    return scenes
