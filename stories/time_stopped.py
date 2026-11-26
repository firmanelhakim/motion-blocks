"""TIME STOPPED — "What if time stopped for everyone except you?"

Science explainer, lead: nerd "Nia" (never a story lead before) — the
science kid who works out that time has stopped and walks through a
frozen town. A frozen mid-air ball, stopped people, a clock that reads
the same minute all day.

Staging: the frozen people are characters holding a single idle pose for
the whole scene (no walk cycle, no expression change), which reads as
frozen time. Nia is the only one who moves. The mid-air ball is a small
sphere fx, frozen at chest height.

The ONE science idea: time never truly stops — it can only run slower.
If time really stopped, light would stop too, and you would see nothing
at all. And near a black hole, or on a fast spaceship, time runs slower
than on Earth: scientists call it time dilation.

FIX (2026-11-23, channel rule): opens with the title question "What if
time stopped for everyone except you?" as b0, then the "In this town,"
setup follows. Science takeaway added as s1/s2 before the moustache
punchline, so the video ends on the joke.

Build (fake timings — Kokoro is not installed on this VM):
    python3 /tmp/build_stories.py time_stopped
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, orbit, shot, split_shots, wide  # noqa: F401

TITLE = "WHAT IF TIME STOPPED FOR EVERYONE EXCEPT YOU"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b0", "text": "What if time stopped for everyone except you?", "pause": 0.10},
    {"id": "b1", "text": "In this town, one Tuesday, time stopped for everyone except Nia.", "pause": 0.08},
    {"id": "b2", "text": "The school bell froze mid-ring. The clock read ten oh nine, all day.", "pause": 0.08},
    {"id": "b3", "text": "Her teacher stopped mid-word, one hand in the air, and never finished.", "pause": 0.08},
    {"id": "b4", "text": "In the playground, a ball hung in the air, halfway to the goal.", "pause": 0.08},
    {"id": "b5", "text": "Nia walked through the frozen town, the only moving thing in it.", "pause": 0.08},
    {"id": "b6", "text": "She poked the bully. He did not blink. She drew a moustache on him.", "pause": 0.10},
    {"id": "b7", "text": "She finished everyone's homework, and ate two ice creams from the shop.", "pause": 0.08},
    {"id": "b8", "text": "But by dinner, the quiet was too quiet. Nobody laughed at her jokes.", "pause": 0.10},
    {"id": "b9", "text": "She missed the noise, the mess, the way her friend talked too much.", "pause": 0.08},
    {"id": "b10", "text": "So she climbed the clock tower and pushed the big hand, one minute.", "pause": 0.12},
    {"id": "w1", "text": "TICK!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "TOCK!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "GO!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b11", "text": "The bell rang, the ball flew, and the whole town woke up at once.", "pause": 0.08},
    {"id": "b12", "text": "Her friend asked where she had been. Nia just smiled and said nothing.", "pause": 0.08},
    {"id": "s1", "text": "Here is the real science. If time really stopped, light would stop too, and you would see nothing at all.", "pause": 0.10},
    {"id": "s2", "text": "Time never truly stops. Near a black hole, or on a fast spaceship, time runs slower. Scientists call it time dilation.", "pause": 0.10},
    {"id": "b13", "text": "But the bully still has that moustache. Nobody knows how it got there.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05,
         "dropouts": [("b10+0.3", "w3.end")]}
SFX = [
    ("b0+0.2", "sparkle"),
    ("b1", "whoosh"),
    ("b2+0.5", "ding_dong"),
    ("b3+0.4", "pop", {"f": 600}),
    ("b4+0.5", "sparkle"),
    ("b5", "whoosh"),
    ("b6+0.6", "pop", {"f": 800}),
    ("b7+0.8", "pop", {"f": 700}),
    ("b8+0.4", "sad"),
    ("b9+0.5", "bell_low"),
    ("b10+0.4", "riser", {"dur": 1.8}),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b11+0.5", "laugh"),
    ("b12+0.6", "sparkle"),
    ("s1+0.3", "sparkle"),
    ("s2+0.4", "pop", {"f": 700}),
    ("b13+1.2", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
CAST = {
    "hero": {"extends": "nerd", "hair": {"style": "sidePart", "color": "black"},
             "top": {"style": "hoodie", "color": "green", "secondary": "white"},
             "bottom": {"style": "jeans", "color": "denim"},
             "shoes": {"color": "white", "sole": "white"},
             "accessories": ["glasses"]},
    "teacher": "teacher_man",
    "bully": "bully",
    # The bully AFTER Nia draws on him (b6): same preset, plus a moustache.
    # Swapped in with the parking trick at B["b6"]; used from then on.
    "bully_moustache": {"extends": "bully", "facialHair": "mustache",
                        "facialHairColor": "black"},
    "friend": {"extends": "kid_girl", "hair": {"style": "pigtails", "color": "brown"},
               "top": {"style": "hoodie", "color": "purple", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"},
               "shoes": {"color": "white", "sole": "white"}},
    "mom": {"extends": "real_mom", "hair": {"style": "bun", "color": "black"}},
}


# 4. SCENES --------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END
    S_CLS = B["b3"] - 1     # classroom: teacher frozen mid-word
    S_PLY = B["b5"] - 1     # playground: the frozen ball, Nia walks through
    S_SHOP = B["b7"] - 1    # shop + street: homework, ice cream, quiet
    S_TWR = B["b10"] - 1    # school exterior: the clock tower push
    S_WAKE = B["b11"] - 1   # playground: everything wakes up
    S_END = B["b13"] - 1    # street: the moustache mystery

    # The frozen ball: a small sphere hanging mid-air at chest height over
    # the playground. One keyframe pair, same position — it never moves.
    ball_fx = [{"id": "ball", "shape": "sphere", "radius": 0.7, "color": "#F8FAFC",
                "emissive": "#E2E8F0", "emissiveIntensity": 0.2, "roughness": 0.4,
                "keyframes": [{"frame": S_PLY, "position": [0, 3.5, 0]},
                              {"frame": S_WAKE, "position": [0, 3.5, 0]}]}]

    HERO_P = [-2.5, 0, 1.0]
    return [
        {   # Hook: aerial town, three angles.
            "id": "hook", "location": "town_overview", "startFrame": 0, "endFrame": S_CLS,
            "cameraShots": [
                shot(0, S_CLS // 3, [-10, 62, 74], [-7, 56, 67], [8, 0, -6], [7, 1, -7], 55),
                shot(S_CLS // 3, 2 * S_CLS // 3, [-7, 56, 67], [-4, 50, 61], [7, 1, -7], [6, 2, -8], 55),
                shot(2 * S_CLS // 3, S_CLS, [-4, 50, 61], [-2, 46, 56], [6, 2, -8], [6, 2, -8], 55),
            ],
            "characters": {},
        },
        {   # Classroom: teacher frozen mid-word, Nia the only one moving.
            "id": "classroom", "location": "classroom",
            "boardText": ["10:09", "DO NOT", "MOVE"],
            "startFrame": S_CLS, "endFrame": S_PLY,
            "cameraShots": cover(S_CLS, S_PLY, [
                lambda a, b: wide(a, b),
                lambda a, b: close_up(a, b, [-5.5, 0, 3.0]),
                lambda a, b: medium(a, b, [0, 0, 2.5]),
                lambda a, b: close_up(a, b, HERO_P),
            ]),
            "characters": {
                # The teacher holds ONE idle pose the whole scene: frozen.
                "teacher": hold(S_CLS, S_PLY, [-5.5, 0, 3.0], 0.4, "idle", "deadpan", "pointer"),
                "hero": [kf(S_CLS, [4.5, 0, 3.0], -0.4, "idle", "shocked"),
                         kf(B["b3"], [0, 0, 2.5], -0.4, "walk", "shocked"),
                         kf(B["b3"] + 24, [0, 0, 2.5], 0.4, "idle", "shocked"),
                         kf(S_PLY, [0, 0, 2.5], 0.4, "idle", "shocked")],
                "friend": hold(S_CLS, S_PLY, [6.5, 0, -2.0], -0.6, "idle", "smile"),
            },
        },
        {   # Playground: the frozen ball, Nia walks through the frozen town.
            "id": "playground", "location": "playground",
            "startFrame": S_PLY, "endFrame": S_SHOP,
            "fx": ball_fx,
            # FIX 2026-11-23 (fix1): the b6 gag ("She poked the bully... She drew
            # a moustache on him.") was told but never shown — the orbit + medium
            # framed Nia alone, the bully 5 studs off at the frame edge, and the
            # moustache swap fired at B["b6"], before she "drew" it. Re-staged as
            # an explicit 4-shot split so the beat lands in two-shots:
            # wide (ball, unchanged) -> short ball orbit -> poke two-shot
            # (565-619, Nia points at the bully) -> draw two-shot (619-662,
            # pointer prop in hand, moustache swaps in on "on him" at 649).
            # Only frames 533-662 change; 468-532 (wide) is byte-identical to v1.
            "cameraShots": [
                wide(S_PLY, 533),
                orbit(533, B["b6"], [0, 0, 0], 12, 6, -0.5, 0.5, [0, 3.0, 0], 58),
                medium(B["b6"], B["b6"] + 54, [2.5, 0, 0.5], dist=20),
                medium(B["b6"] + 54, S_SHOP, [2.5, 0, 0.5], dist=17, height=5.2,
                       drift=(0.6, 0.0, -1.0)),
            ],
            "characters": {
                # Nia walks up to the bully, plants at B["b6"] facing him (+X)
                # and POINTS — right arm out toward his face: the poke. At
                # B["b6"]+54 ("She drew") she KEEPS the arm raised ("point")
                # with the new "pointer_draw" prop: rotation 2.8 about X in
                # arm space, so the stick sits ~18 deg above horizontal and
                # aims up-right at his face (FIX2 2026-11-23 — v2's
                # idle+pointer dangled down-left at shin level; plain
                # pointer+point tips up-backward instead).
                "hero": [kf(S_PLY, [-6.0, 0, 0.5], HALF, "walk", "smile"),
                         kf(B["b6"], [0, 0, 0.5], HALF, "point", "laugh"),
                         kf(B["b6"] + 54, [0, 0, 0.5], HALF, "point", "laugh", "pointer_draw"),
                         kf(S_SHOP, [0, 0, 0.5], HALF, "idle", "laugh")],
                # The bully, frozen mid-stride, never moves or changes face.
                # He stays moustache-less through the poke and the draw, and is
                # swapped for the moustache look ONLY on "on him" (B["b6"]+84
                # = 649, the caption start of "on him."): the moustache appears
                # exactly as she draws it on him.
                "bully": [kf(S_PLY, [5.0, 0, 0.5], -0.5, "idle", "cool"),
                          kf(B["b6"] + 83, [5.0, 0, 0.5], -0.5, "idle", "cool"),
                          kf(B["b6"] + 84, OFF, -0.5, "idle", "cool"),
                          kf(S_SHOP, OFF, -0.5, "idle", "cool")],
                "bully_moustache": [kf(S_PLY, OFF, -0.5, "idle", "cool"),
                                    kf(B["b6"] + 83, OFF, -0.5, "idle", "cool"),
                                    kf(B["b6"] + 84, [5.0, 0, 0.5], -0.5, "idle", "cool"),
                                    kf(S_SHOP, [5.0, 0, 0.5], -0.5, "idle", "cool")],
                "friend": hold(S_PLY, S_SHOP, [-4.5, 0, -4.5], 0.5, "idle", "smile"),
            },
        },
        {   # Shop and street: homework done, ice cream eaten, the quiet.
            "id": "shop", "location": "shop",
            "startFrame": S_SHOP, "endFrame": S_TWR,
            # FIX 2026-11-23: medium at dist 12 is too tight for a 2-shot in
            # portrait — Nia and mom both landed half out of frame. dist 20,
            # centred on the midpoint of the two actors, keeps both whole.
            "cameraShots": cover(S_SHOP, S_TWR, [
                lambda a, b: medium(a, b, [1.0, 0, 0], dist=20),
                lambda a, b: close_up(a, b, HERO_P),
                lambda a, b: wide(a, b),
                lambda a, b: low_angle(a, b, HERO_P),
            ]),
            "characters": {
                "hero": [kf(S_SHOP, HERO_P, 0.3, "idle", "smile", "backpack"),
                         kf(B["b8"], HERO_P, 0.3, "idle", "deadpan"),
                         kf(S_TWR, HERO_P, 0.3, "idle", "deadpan")],
                "mom": hold(S_SHOP, S_TWR, [4.5, 0, -1.0], -0.4, "idle", "smile"),
            },
        },
        {   # School exterior: Nia climbs and pushes the big hand.
            "id": "tower", "location": "school_exterior", "schoolName": "TIME SCHOOL",
            "startFrame": S_TWR, "endFrame": S_WAKE,
            "cameraShots": cover(S_TWR, S_WAKE, [
                lambda a, b: wide(a, b),
                lambda a, b: low_angle(a, b, HERO_P),
                lambda a, b: close_up(a, b, HERO_P, shake=0.06),
            ]),
            "characters": {
                "hero": [kf(S_TWR, HERO_P, 0.2, "walk", "smile"),
                         kf(B["w1"], HERO_P, 0.2, "point", "shocked"),
                         kf(B["w3"], HERO_P, 0.2, "celebrate", "laugh"),
                         kf(S_WAKE, HERO_P, 0.2, "celebrate", "laugh")],
            },
        },
        {   # Everything wakes up at once.
            "id": "wake", "location": "playground",
            "startFrame": S_WAKE, "endFrame": S_END,
            # FIX 2026-11-23: medium at dist 12 cropped Nia and her friend
            # half out of frame at opposite edges (all three wake mediums).
            # dist 20 keeps both whole.
            "cameraShots": cover(S_WAKE, S_END, [
                lambda a, b: wide(a, b),
                lambda a, b: medium(a, b, [0, 0, 1.0], dist=20),
                lambda a, b: close_up(a, b, [2.5, 0, 1.0]),
            ]),
            "characters": {
                "hero": hold(S_WAKE, S_END, [-2.5, 0, 1.0], 0.4, "idle", "smile"),
                "friend": [kf(S_WAKE, [2.5, 0, 1.0], -0.4, "idle", "shocked"),
                           kf(B["b12"], [2.5, 0, 1.0], -0.4, "idle", "smile"),
                           kf(S_END, [2.5, 0, 1.0], -0.4, "idle", "smile")],
                "bully_moustache": hold(S_WAKE, S_END, [6.5, 0, -2.0], -0.5, "idle", "panic"),
            },
        },
        {   # The moustache mystery.
            "id": "mystery", "location": "street",
            "startFrame": S_END, "endFrame": END,
            # FIX 2026-11-23: medium at dist 12 cropped Nia and the bully
            # half out of frame at opposite edges. dist 20 keeps both whole.
            "cameraShots": cover(S_END, END, [
                lambda a, b: medium(a, b, [0, 0, 0.5], dist=20),
                lambda a, b: close_up(a, b, [2.5, 0, 0.5]),
            ]),
            "characters": {
                "hero": hold(S_END, END, [-2.5, 0, 0.5], 0.4, "idle", "cool"),
                "bully_moustache": hold(S_END, END, [2.5, 0, 0.5], -0.4, "idle", "panic"),
            },
        },
    ]
