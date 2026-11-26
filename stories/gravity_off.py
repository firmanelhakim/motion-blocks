"""GRAVITY OFF FOR 10 SECONDS - v2 science explainer.

Replaces the v1 day-in-the-life story (kept as gravity_off_v1.py).
the maintainer's verdict on v1 (2026-11-16): the render flickered and went black,
and the story was a fun narrative, not the science explainer he wanted.
This version teaches the physics: you don't fall up, you fly straight
while the Earth curves away; inertia; the air starts to leave; the Moon
would fly off; gravity coming back is the dangerous part; the 10s / 10min
/ 1-day scale.

Science kept honest: Earth spins ~465 m/s at the equator (faster than the
speed of sound, ~343 m/s); without gravity you keep that velocity in a
straight line while the ground curves away, so you drift up; air molecules
move ~500 m/s, so in 10 s the sky thins but is not gone; the Moon keeps its
~1 km/s orbital velocity and leaves in a straight line; no weight means no
friction, so you cannot walk or steer; when gravity returns, everything
falls from wherever it drifted to.

Build:   python scripts/make_short.py stories/gravity_off.py --stills
Render:  python scripts/make_short.py stories/gravity_off.py --skip-tts --render
         (re-render on the SwiftShader path only -- the pod's --gl=angle-egl
          render of v1 flickered and blackened the classroom; the VM stills
          of the same shots are bright and correct.)

Floating is staged with real y positions (the renderer passes keyframe y
straight through to the character group). Camera helpers ignore actor y,
so every floated close-up uses a manual shot() aimed at head height + y.
Spacing is checked in 2D (x,z only), so horizontal separation stays >= 4.5
even when actors float at different heights.
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, split_shots, wide  # noqa: F401

TITLE = "WHAT IF GRAVITY SWITCHED OFF FOR 10 SECONDS"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this world, what if gravity switched off for ten seconds?", "pause": 0.08},
    {"id": "b2", "text": "First, you would not fall up. Nothing pulls you up. Gravity just... lets go.", "pause": 0.08},
    {"id": "b3", "text": "You are standing on a planet spinning faster than the speed of sound. You keep flying straight, and the Earth curves away under you. That is why you float.", "pause": 0.10},
    {"id": "b4", "text": "Everything keeps its speed. My friend was sprinting when it happened, so she just kept gliding, in a straight line, until something stopped her.", "pause": 0.10},
    {"id": "b5", "text": "The air starts to leave too. Gravity is the only thing holding the sky down. Ten seconds is not enough to lose it all, so you can still breathe.", "pause": 0.10},
    {"id": "b5b", "text": "The water lifts off too. The sea, the lakes, your drink, all of it rises in blobs and drifts away.", "pause": 0.10},
    {"id": "b6", "text": "But the Moon stays in orbit because gravity pulls it. Switch gravity off, and it flies away in a straight line, and never comes back.", "pause": 0.10},
    {"id": "b7", "text": "And you cannot steer. With no weight, there is no grip. You cannot walk, you cannot push off, you just drift.", "pause": 0.08},
    {"id": "b8", "text": "Here is the part nobody tells you. Gravity always comes back.", "pause": 0.10},
    {"id": "b9", "text": "And when it does, everything that drifted up... falls.", "pause": 0.12},
    {"id": "b10", "text": "Ten seconds up there is a long way to fall.", "pause": 0.08},
    {"id": "w1", "text": "GRAVITY!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "IS!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "BACK!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b11", "text": "We all landed in a big pile. The floating was fun. The landing was not.", "pause": 0.08},
    {"id": "b12", "text": "Ten seconds, we survive. Ten minutes, the air is gone. A whole day, and the Earth itself would come apart.", "pause": 0.10},
    {"id": "b13", "text": "Gravity is not just what pulls you down. It holds the sky, the sea, and the Moon in place.", "pause": 0.10},
    {"id": "b14", "text": "So if gravity ever takes ten seconds off... hold on to something.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/fallen-down.mp3",
    "under_voice": 0.022,
    "gaps": 0.05,
    "dropouts": [("b10+0.3", "w3.end")],
}

SFX = [
    ("b1", "whoosh"),
    ("b1+0.5", "sparkle"),
    ("b2+0.5", "pop", {"f": 600}),
    ("b3+1.0", "sparkle"),
    ("b4+0.5", "whoosh"),
    ("b5+0.8", "sparkle"),
    ("b5b+0.5", "bubbles"),
    ("b6+0.8", "whoosh"),
    ("b7+0.8", "pop_down"),
    ("b8+0.8", "bell_low"),
    ("b9", "riser", {"dur": 2.0}),
    ("b10+0.5", "whoosh"),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b11+1.0", "thud"),
    ("b12+0.5", "pop", {"f": 600}),
    ("b13+0.8", "sparkle"),
    ("b14+1.5", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
# Same hero/friend as late_power and v1, so the channel has one recognisable cast.
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

    S2 = B["b2"] - 1    # classroom: let go, hero rises as Earth curves away
    S3 = B["b4"] - 1    # playground: friend glides (inertia)
    S4 = B["b5"] - 1    # street: the air starts to leave
    S5 = B["b5b"] - 1   # classroom: water lifts off the teacher's desk
    S6 = B["b6"] - 1    # school exterior: the Moon would fly away
    S7 = B["b7"] - 1    # classroom: you cannot steer
    S8 = B["b9"] - 1    # classroom: countdown, friend rises to the ceiling
    S9 = B["w1"] - 1    # classroom: gravity back, landing pile
    S10 = B["b12"] - 1  # classroom: the 10s / 10min / 1-day scale on the board
    S11 = B["b13"] - 1  # living room night: closer

    scenes = []

    # 1. HOOK - aerial town ------------------------------------------------------
    scenes.append({
        "id": "hook", "location": "town_overview", "startFrame": 0, "endFrame": S2,
        "cameraShots": [shot(0, S2 // 2, [-10, 62, 74], [-6, 54, 65], [8, 0, -6], [7, 1, -7], 55),
                        shot(S2 // 2, S2, [-6, 54, 65], [-2, 46, 56], [7, 1, -7], [6, 2, -8], 55)],
        "characters": {},
    })

    # 2. CLASSROOM - let go: hero rises while the Earth curves away --------------
    # Manual shots: close_up/wide ignore actor y, so aim at head height + y.
    scenes.append({
        "id": "let-go", "location": "classroom",
        "boardText": ["GRAVITY OFF", "EARTH SPINS 465 m/s", "YOU FLY STRAIGHT"],
        "startFrame": S2, "endFrame": S3,
        "cameraShots": cover(S2, S3, [
            lambda a, b: shot(a, b, [0, 9.5, 21], [0, 9.0, 18.5], [0, 5.5, 0], [0, 5.2, 0], 58),
            lambda a, b: shot(a, b, [-0.5, 7.5, 7.5], [-0.5, 7.3, 6.3], [-0.5, 6.9, 0.5], [-0.5, 6.9, 0.5], 44),
            lambda a, b: shot(a, b, [-5.5, 7.0, 2.5], [-5.5, 6.8, 1.3], [-5.5, 6.4, -4.5], [-5.5, 6.4, -4.5], 44),
        ]),
        "characters": {
            "teacher": hold(S2, S3, [-5.5, 2.0, -4.5], 0.5, "jump", "panic"),
            "hero": [kf(S2, [-0.5, 0, 0.5], 0, "idle", "smile"),
                     kf(B["b3"] + 15, [-0.5, 2.5, 0.5], 0, "jump", "shocked"),
                     kf(S3, [-0.5, 2.5, 0.5], 0, "jump", "shocked")],
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

    # 4. STREET - the air starts to leave, you can still breathe ------------------
    scenes.append({
        "id": "air", "location": "street", "startFrame": S4, "endFrame": S5,
        "cameraShots": cover(S4, S5, [lambda a, b: wide(a, b, [0, 0, 0.5], 24),
                                       lambda a, b: close_up(a, b, [0, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [-4.5, 0, 0.5])]),
        "characters": {
            "hero": hold(S4, S5, [-4.5, 0, 0.5], 0.2, "point", "smile"),
            "friend": hold(S4, S5, [0, 0, 0.5], -0.2, "wave", "smile"),
        },
    })

    # 5. CLASSROOM - water lifts off the teacher's desk (NEW: science fx) ---------
    # The blobs rise from the desk top (y ~3.4), clear of the teacher at x -5.5:
    # blob1 at the desk's right end (x -3.0), blob2 at the left end (x -7.5).
    scenes.append({
        "id": "water", "location": "classroom",
        "boardText": ["WATER LIFTS OFF", "SEA + LAKES", "RISES IN BLOBS"],
        "startFrame": S5, "endFrame": S6,
        "cameraShots": cover(S5, S6, [
            lambda a, b: shot(a, b, [0, 7.4, 20], [0, 7.0, 17.5], [0, 4.8, -1], [0, 4.7, -1], 58),
            lambda a, b: shot(a, b, [-4.5, 6.5, 9.0], [-4.5, 6.8, 7.5], [-4.5, 5.0, -4.4], [-4.5, 5.5, -4.4], 52),
            lambda a, b: close_up(a, b, [-0.5, 0, 0.5]),
        ]),
        "fx": [
            {"id": "waterBlob1", "shape": "sphere", "radius": 1.1, "color": "#38BDF8",
             "emissive": "#0EA5E9", "emissiveIntensity": 0.35, "roughness": 0.15, "opacity": 0.65,
             "keyframes": [{"frame": S5, "position": [-3.0, 3.6, -4.4]}, {"frame": S6, "position": [-3.0, 9.0, -4.4]}]},
            {"id": "waterBlob2", "shape": "sphere", "radius": 0.7, "color": "#7DD3FC",
             "emissive": "#0EA5E9", "emissiveIntensity": 0.35, "roughness": 0.15, "opacity": 0.65,
             "keyframes": [{"frame": S5, "position": [-7.5, 3.6, -4.4]},
                           {"frame": (S5 + S6) // 2, "position": [-7.5, 3.6, -4.4]},
                           {"frame": S6, "position": [-7.5, 7.5, -4.4]}]},
        ],
        "characters": {
            "teacher": hold(S5, S6, [-5.5, 0, -4.5], 0.5, "point", "shocked", "pointer"),
            "hero": hold(S5, S6, [-0.5, 0, 0.5], 0, "idle", "shocked"),
        },
    })

    # 6. SCHOOL EXTERIOR - the Moon flies away; bully clings to the flagpole --------
    # The Moon is a science fx: a pale sphere high in the sky that drifts
    # up-right in a straight line across the scene (and never comes back).
    scenes.append({
        "id": "moon", "location": "school_exterior", "schoolName": "GRAVITY SCHOOL",
        "startFrame": S6, "endFrame": S7,
        "cameraShots": cover(S6, S7, [lambda a, b: wide(a, b, [0, 0, 0], 24),
                                       lambda a, b: close_up(a, b, [4.5, 0, 0])]),
        "fx": [
            {"id": "moon", "shape": "sphere", "radius": 4.0, "color": "#FDE68A",
             "emissive": "#FDE68A", "emissiveIntensity": 0.9, "roughness": 0.9,
             "keyframes": [{"frame": S6, "position": [-12, 16, -22]}, {"frame": S7, "position": [-4, 18.5, -22]}]},
        ],
        "characters": {
            "bully": hold(S6, S7, [4.5, 0, 0], -0.6, "celebrate", "panic"),
            "hero": hold(S6, S7, [-4.5, 0, 0], 0.6, "point", "shocked"),
        },
    })

    # 7. CLASSROOM - you cannot steer: hero drifts toward the camera ----------------
    # Hero drifts in z (4.5 -> 0.5), staying >= 5 from the friend at x 4.5 and
    # >= 6 from the teacher; drifting in x toward the friend breaks spacing.
    D1 = S7 + (S8 - S7) // 3
    D2 = S7 + 2 * (S8 - S7) // 3
    scenes.append({
        "id": "drift", "location": "classroom",
        "boardText": ["NO WEIGHT", "NO GRIP", "NO STEERING"],
        "startFrame": S7, "endFrame": S8,
        "cameraShots": [
            shot(S7, D1, [0, 7.4, 20], [0, 7.0, 17.5], [0, 4.8, -1], [0, 4.7, -1], 58),
            shot(D1, D2, [-0.5, 7.0, 11], [-0.5, 7.0, 10], [-0.5, 6.9, 3.2], [-0.5, 6.9, 1.8], 50),
            close_up(D2, S8, [-5.5, 0, -4.5]),
        ],
        "characters": {
            "hero": [kf(S7, [-0.5, 2.5, 4.5], 0, "jump", "panic"),
                     kf(S8, [-0.5, 2.5, 0.5], 0, "jump", "panic")],
            "friend": hold(S7, S8, [4.5, 2.5, 0.5], 0, "jump", "shocked"),
            "teacher": hold(S7, S8, [-5.5, 0, -4.5], 0.5, "point", "deadpan", "pointer"),
        },
    })

    # 8. CLASSROOM - countdown: friend rises to the ceiling, hero reaches up ---------
    RISE = B["b10"]
    MID8 = (S8 + B["b10"]) // 2
    scenes.append({
        "id": "countdown", "location": "classroom",
        "boardText": ["GRAVITY OFF", "12:00 = FLOAT", "HOLD ON TIGHT"],
        "startFrame": S8, "endFrame": S9,
        # Manual cuts aligned to the beats: the actors change height mid-scene,
        # so cover() lands the high close-ups while they are still rising.
        "cameraShots": [
            shot(S8, MID8, [0, 7.4, 20], [0, 7.0, 17.5], [0, 4.8, -1], [0, 4.7, -1], 58),
            close_up(MID8, B["b10"], [-5.5, 0, -4.5]),
            shot(B["b10"], B["b10"] + 30, [-0.5, 5.6, 12], [-0.5, 6.6, 11], [-0.5, 4.8, 0.5], [-0.5, 6.5, 0.5], 44),
            shot(B["b10"] + 30, S9, [0, 9.5, 21], [0, 9.0, 18.5], [0, 5.5, 0], [0, 5.2, 0], 58),
        ],
        "characters": {
            "teacher": [kf(S8, [-5.5, 0, -4.5], 0.5, "point", "deadpan", "pointer"),
                        kf(RISE, [-5.5, 0, -4.5], 0.5, "point", "shocked", "pointer"),
                        kf(S9, [-5.5, 0, -4.5], 0.5, "point", "shocked", "pointer")],
            "hero": [kf(S8, [-0.5, 0, 0.5], 0, "idle", "smile"),
                     kf(RISE, [-0.5, 0, 0.5], 0, "idle", "shocked"),
                     kf(RISE + 30, [-0.5, 2.5, 0.5], 0, "jump", "shocked"),
                     kf(S9, [-0.5, 2.5, 0.5], 0, "jump", "shocked")],
            "friend": [kf(S8, [4.5, 0, 0.5], 0, "idle", "smile"),
                       kf(RISE, [4.5, 0, 0.5], 0, "idle", "shocked"),
                       kf(RISE + 30, [4.5, 5.0, 0.5], 0, "jump", "panic"),
                       kf(S9, [4.5, 5.0, 0.5], 0, "jump", "panic")],
        },
    })

    # 9. CLASSROOM - gravity back: everyone lands, bully on the teacher's desk -------
    LAND = B["w1"]
    scenes.append({
        "id": "gravity-back", "location": "classroom",
        "boardText": ["GRAVITY OFF", "12:00 = FLOAT", "HOLD ON TIGHT"],
        "startFrame": S9, "endFrame": S10,
        "cameraShots": cover(S9, S10, [lambda a, b: wide(a, b, [0, 0, 0.5], 24),
                                        lambda a, b: close_up(a, b, [-2.0, 0, 1.0]),
                                        lambda a, b: close_up(a, b, [4.5, 0, 0.5])]),
        "characters": {
            "hero": [kf(S9, [-0.5, 2.5, 0.5], 0, "jump", "shocked"),
                     kf(LAND, [-2.0, 0, 1.0], 0, "celebrate", "laugh"),
                     kf(S10, [-2.0, 0, 1.0], 0, "celebrate", "laugh")],
            "friend": [kf(S9, [4.5, 5.0, 0.5], 0, "jump", "panic"),
                       kf(LAND, [4.5, 0, 0.5], 0, "panting", "shocked"),
                       kf(S10, [4.5, 0, 0.5], 0, "panting", "shocked")],
            "bully": [kf(S9, OFF, 0, "idle", "deadpan"),
                      kf(LAND, OFF, 0, "idle", "deadpan"),
                      kf(LAND + 1, [-1.0, 0, -4.5], 0, "panting", "deadpan"),
                      kf(S10, [-1.0, 0, -4.5], 0, "panting", "deadpan")],
            "teacher": hold(S9, S10, [-5.5, 0, -6.8], 0.5, "point", "angry", "pointer"),
        },
    })

    # 10. CLASSROOM - the scale on the board: 10 seconds / 10 minutes / 1 day --------
    scenes.append({
        "id": "scale", "location": "classroom",
        "boardText": ["10 SECONDS: SURVIVE", "10 MINUTES: NO AIR", "1 DAY: NO EARTH"],
        "startFrame": S10, "endFrame": S11,
        "cameraShots": cover(S10, S11, [lambda a, b: wide(a, b, [0, 0, 0.5], 24),
                                         lambda a, b: close_up(a, b, [-0.5, 0, 0.5]),
                                         lambda a, b: close_up(a, b, [-5.5, 0, -4.5])]),
        "characters": {
            "teacher": hold(S10, S11, [-5.5, 0, -4.5], 0.5, "point", "deadpan", "pointer"),
            "hero": hold(S10, S11, [-0.5, 0, 0.5], 0, "idle", "deadpan"),
            "friend": hold(S10, S11, [4.5, 0, 0.5], 0, "idle", "deadpan"),
        },
    })

    # 11. LIVING ROOM (blue), NIGHT - closer ------------------------------------------
    scenes.append({
        "id": "closer", "location": "living_room", "variant": "blue", "isNight": True,
        "startFrame": S11, "endFrame": END,
        "cameraShots": cover(S11, END, [lambda a, b: wide(a, b, [0, 0, 0.4], 24),
                                         lambda a, b: close_up(a, b, [-4.0, 0, 0.4]),
                                         lambda a, b: close_up(a, b, [4.0, 0, 0.4])]),
        "characters": {
            "hero": [kf(S11, [-4.0, 0, 0.4], 0.9, "idle", "deadpan"),
                     kf(B["b14"], [-4.0, 0, 0.4], 0.9, "idle", "smile"),
                     kf(END, [-4.0, 0, 0.4], 0.9, "idle", "smile")],
            "mom": [kf(S11, [4.0, 0, 0.4], -0.9, "wave", "smile"),
                    kf(END, [4.0, 0, 0.4], -0.9, "wave", "smile")],
        },
    })

    return scenes
