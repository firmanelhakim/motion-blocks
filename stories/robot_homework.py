"""ROBOT HOMEWORK — "What if robots did all the homework?"

Science explainer, lead: Max (kid_boy — blue spiky hair, royal hoodie;
his sky_blue look, now leading). Mia (kid_girl, pigtails, teal sweater)
is the friend. The robot is Robo — a NEW engine asset for this video
(src/components/BlockyRobot.tsx, fx shape 'robot'): white/blue boxy
robot, dark screen face with two glowing cyan oval eyes, red-ball
antenna, holding a stack of three books (red, green, blue). Built in
code from the Gemini reference ~/workspace/user/files/1000374845_6_aif2.jpg
(reference only — never pasted into the video).

The one science idea: robots follow programs. They can copy and
calculate, but they do not understand. Understanding happens in a
human brain — so homework done by a robot teaches the robot's memory,
not yours.

Filmable-limits notes (honest):
- The robot cannot type or write (no typing anim, no pencil prop).
  The "essays" beat is the robot standing at the board with the essay
  already marked DONE + a swish; the narration carries the typing.
- The test cannot show a paper (no paper prop). The test-day beat is
  Max at his desk with a shocked/panic face + the "TEST DAY" board;
  the narration carries the blank page.
- The robot cannot hand books over (no handover anim). The outro beat
  is the robot standing beside sitting Max, still holding the books,
  while the narration says he fetches them and Max reads them.
- The robot's legs are static boxes (no walk cycle). It never walks on
  screen — it is placed, and cuts do the moving.

Locations: 'studio' (hook — plain light-grey set, matches the reference
background); 'classroom' (meet, homework, test day, science); 'street'
(every kid hands homework to Robo); 'bedroom' (outro — Max sits on the
floor doing his own homework, Robo beside him).

Build (run the previews serially — do NOT run make_short.py alongside
other stories):
    python scripts/make_short.py stories/robot_homework.py --stills
"""
import math  # noqa: F401

from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, split_shots, wide  # noqa: F401

TITLE = "THE ROBOT DID MY HOMEWORK"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b0", "text": "What if robots did all the homework?", "pause": 0.10},
    {"id": "b1", "text": "In this town, a robot does every kid's homework.", "pause": 0.08},
    {"id": "b2", "text": "Meet Robo. He never sleeps, never gets bored, and never makes a mistake.", "pause": 0.08},
    {"id": "b3", "text": "Maths homework? Done in three seconds flat.", "pause": 0.08},
    {"id": "b4", "text": "Essays? He types faster than you can blink.", "pause": 0.08},
    {"id": "b5", "text": "Every kid in town hands their homework to Robo. Even Max.", "pause": 0.08},
    {"id": "b6", "text": "Then Monday comes. Test day. And robots are not allowed in the exam hall.", "pause": 0.10},
    {"id": "b7", "text": "Max stares at the first question. His mind is totally blank.", "pause": 0.08},
    {"id": "b8", "text": "The answers were in Robo's memory. Not in Max's head.", "pause": 0.10},
    {"id": "b9", "text": "Robots follow programs. They can copy and calculate, but they do not understand.", "pause": 0.10},
    {"id": "b10", "text": "Understanding only happens in one place. Your brain.", "pause": 0.10},
    {"id": "w1", "text": "YOUR", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "BRAIN", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "LEARNS!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b11", "text": "So Max does his own homework now. Slowly. But it sticks.", "pause": 0.08},
    {"id": "b12", "text": "Robo still helps. He fetches the books. Max reads them.", "pause": 0.08},
    {"id": "b13", "text": "A robot can do your homework. But only you can learn from it.", "pause": 0.10},
    {"id": "b14", "text": "What would you let a robot do for you? Tell us below.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05,
         "dropouts": [("b10+0.2", "w3.end")]}
SFX = [
    ("b0", "whoosh"),
    ("b2+0.3", "pop", {"f": 700}),
    ("b3+0.5", "pop", {"f": 900}),
    ("b4+0.3", "swish"),
    ("b5+0.3", "laugh"),
    ("b6", "ding_dong"),
    ("b7+0.4", "sad"),
    ("b8+0.4", "pop_down"),
    ("b9+0.4", "sparkle"),
    ("b10+0.5", "riser", {"dur": 1.6}),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b11+0.5", "pop", {"f": 600}),
    ("b12+0.5", "sparkle"),
    ("b13+0.5", "reveal"),
    ("b14+1.0", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
CAST = {
    # Max leads (his sky_blue look: blue spiky hair, royal hoodie).
    "hero": {"extends": "kid_boy", "hair": {"style": "spikyAnime", "color": "blue"},
             "top": {"style": "hoodie", "color": "royal", "secondary": "white"},
             "bottom": {"style": "jeans", "color": "denim"},
             "shoes": {"color": "white", "sole": "white"}, "freckles": True},
    # Mia, the friend (her friction_5_seconds look: pigtails, teal sweater).
    "friend": {"extends": "kid_girl", "hair": {"style": "pigtails", "color": "brown"},
               "top": {"style": "sweater", "color": "teal", "secondary": "white"},
               "bottom": {"style": "skirt", "color": "navy"},
               "shoes": {"color": "white", "sole": "white"}},
    "teacher": {"extends": "teacher"},
}


# 4. SCENES --------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END
    S_MEET = B["b2"] - 1     # classroom: meet Robo
    S_HW = B["b3"] - 1       # classroom: maths + essays
    S_STREET = B["b5"] - 1   # street: every kid hands homework to Robo
    S_TEST = B["b6"] - 1     # classroom: test day (no robot — not allowed)
    S_SCI = B["b9"] - 1      # classroom: the science + brain
    S_OUT = B["b11"] - 1     # bedroom: Max does his own homework now

    # THE ROBOT — fx shape 'robot' (BlockyRobot), feet at y = 0, scale 0.9
    # (~5.9 studs tall, kid height). One entry per scene it appears in
    # (ids are per-scene); static keyframes spanning the scene (the bob,
    # head sway, antenna wobble and eye blink are internal to the asset).
    def robot_fx(a, b, pos, ry=0):
        return [{"id": "robo", "shape": "robot", "color": "#2E7DE1", "scale": 0.9,
                 "rotation": [0, ry, 0],
                 "keyframes": [{"frame": a, "position": pos},
                               {"frame": b, "position": pos}]}]

    # THE BRAIN — fx shape 'brain' (BlockyBrain), floating above Max's head
    # for the science + shout beats. Scale 0.45 (~1.5 studs wide).
    # above Max's head (was [0, 7.2, 0.5] — dead-centre on the board,
    # covering "ROBOTS FOLLOW" / "PROGRAMS" in every science shot;
    # was [-5, 7.0, 1.5] — only a pink sliver at the left edge in the
    # science wides, so nudged +0.5 in to sit fully in frame).
    brain_fx = [{"id": "brain", "shape": "brain", "color": "#E07A96", "scale": 0.45,
                 "keyframes": [{"frame": S_SCI, "position": [-4.5, 7.0, 1.5]},
                               {"frame": S_OUT, "position": [-4.5, 7.0, 1.5]}]}]

    HERO_P, FRIEND_P = [-5, 0, 1.5], [5, 0, 1.5]
    # Teacher stands centre-back, in front of the board (was [-5.5, 0, -2]:
    # directly behind Max from the front camera — hidden + 3.54 spacing fail).
    TEACHER_P = [0, 0, -2.5]

    return [
        {   # Hook: the big question over Robo's glowing face, then the
            # setup over his whole body + the book stack. Studio, plain
            # light-grey set — matches the reference background.
            "id": "hook", "location": "studio",
            "startFrame": 0, "endFrame": S_MEET,
            "fx": robot_fx(0, S_MEET, [0, 0, 0]),
            "cameraShots": split_shots(0, S_MEET, [
                lambda a, b: close_up(a, b, [0, 0, 0], scale=0.9),
                lambda a, b: medium(a, b, [0, 0, 0], dist=13),
            ]),
            "characters": {},
        },
        {   # Meet Robo: the robot stands in the classroom aisle between
            # Max and Mia. Board carries his name.
            "id": "meet", "location": "classroom",
            "boardText": ["MEET ROBO"],
            "startFrame": S_MEET, "endFrame": S_HW,
            "fx": robot_fx(S_MEET, S_HW, [0, 0, 1.5]),
            "cameraShots": cover(S_MEET, S_HW, [
                lambda a, b: wide(a, b, [0, 0, 1.5], dist=20),
                lambda a, b: medium(a, b, [0, 0, 1.5]),
                lambda a, b: close_up(a, b, [-5, 0, 1.5]),
            ]),
            "characters": {
                "hero": hold(S_MEET, S_HW, HERO_P, 0, "idle", "shocked"),
                "friend": hold(S_MEET, S_HW, FRIEND_P, 0, "idle", "smile"),
            },
        },
        {   # The homework: maths done in three seconds, essays typed
            # faster than you can blink. The board shows finished work;
            # the robot never types on screen (no typing anim) — the
            # narration carries it. Max goes shocked -> laughing.
            "id": "homework", "location": "classroom",
            "boardText": ["2 + 2 = 4", "5 x 3 = 15", "ESSAY: DONE!"],
            "startFrame": S_HW, "endFrame": S_STREET,
            "fx": robot_fx(S_HW, S_STREET, [0, 0, 1.5]),
            "cameraShots": cover(S_HW, S_STREET, [
                lambda a, b: wide(a, b, [0, 0, 1.5], dist=20),
                lambda a, b: close_up(a, b, [0, 0, 1.5], scale=0.9),
                lambda a, b: medium(a, b, [0, 0, 1.5]),
            ]),
            "characters": {
                "hero": [kf(S_HW, HERO_P, 0, "idle", "shocked"),
                         kf(B["b4"], HERO_P, 0, "idle", "laugh"),
                         kf(S_STREET, HERO_P, 0, "idle", "laugh")],
                "friend": [kf(S_HW, FRIEND_P, 0, "idle", "smile"),
                           kf(B["b4"], FRIEND_P, 0, "idle", "laugh"),
                           kf(S_STREET, FRIEND_P, 0, "idle", "laugh")],
            },
        },
        {   # Every kid hands homework to Robo: street, robot centre,
            # both kids celebrating either side.
            "id": "street", "location": "street",
            "startFrame": S_STREET, "endFrame": S_TEST,
            "fx": robot_fx(S_STREET, S_TEST, [0, 0, 0.5]),
            "cameraShots": cover(S_STREET, S_TEST, [
                lambda a, b: wide(a, b, [0, 0, 0.5], dist=20),
                lambda a, b: medium(a, b, [0, 0, 0.5]),
            ]),
            "characters": {
                "hero": hold(S_STREET, S_TEST, [-5, 0, 0.5], 0, "celebrate", "laugh"),
                "friend": hold(S_STREET, S_TEST, [5, 0, 0.5], 0, "celebrate", "laugh"),
            },
        },
        {   # Test day: NO robot (not allowed in the exam hall). Teacher
            # points at the TEST DAY board; Max goes shocked -> panic ->
            # deadpan as his mind blanks. The paper cannot be shown (no
            # paper prop) — his face + the board carry it.
            "id": "test", "location": "classroom",
            "boardText": ["TEST DAY", "NO ROBOTS", "IN THE EXAM HALL"],
            "startFrame": S_TEST, "endFrame": S_SCI,
            "cameraShots": cover(S_TEST, S_SCI, [
                lambda a, b: wide(a, b, [0, 0, 1.5], dist=20),
                lambda a, b: medium(a, b, [-5, 0, 1.5]),
                lambda a, b: close_up(a, b, [-5, 0, 1.5]),
            ]),
            "characters": {
                "teacher": [kf(S_TEST, TEACHER_P, face(TEACHER_P, [0, 0, 1.5]), "point", "smile"),
                            kf(B["b7"], TEACHER_P, face(TEACHER_P, [0, 0, 1.5]), "idle", "smile"),
                            kf(S_SCI, TEACHER_P, face(TEACHER_P, [0, 0, 1.5]), "idle", "smile")],
                "hero": [kf(S_TEST, HERO_P, 0, "idle", "shocked"),
                         kf(B["b7"], HERO_P, 0, "idle", "panic"),
                         kf(B["b8"], HERO_P, 0, "idle", "deadpan"),
                         kf(S_SCI, HERO_P, 0, "idle", "deadpan")],
                "friend": [kf(S_TEST, FRIEND_P, 0, "idle", "smile"),
                           kf(B["b7"], FRIEND_P, 0, "idle", "shocked"),
                           kf(S_SCI, FRIEND_P, 0, "idle", "shocked")],
            },
        },
        {   # The science: robots follow programs — copy + calculate, no
            # understanding. The board carries the science; the BlockyBrain
            # floats above Max's head for "your brain". Shouts land on Max
            # celebrating + the teacher pointing at the board.
            "id": "science", "location": "classroom",
            "boardText": ["ROBOTS FOLLOW", "PROGRAMS", "COPY + CALCULATE", "NO UNDERSTANDING"],
            "startFrame": S_SCI, "endFrame": S_OUT,
            "fx": brain_fx,
            "cameraShots": cover(S_SCI, S_OUT, [
                lambda a, b: wide(a, b, [0, 0, 1.5], dist=20),
                lambda a, b: medium(a, b, [-5, 0, 1.5]),
                lambda a, b: close_up(a, b, [-5, 0, 1.5]),
            ]),
            "characters": {
                "teacher": [kf(S_SCI, TEACHER_P, face(TEACHER_P, [0, 0, 1.5]), "point", "smile"),
                            kf(B["w1"], TEACHER_P, face(TEACHER_P, [0, 0, 1.5]), "idle", "smile"),
                            kf(S_OUT, TEACHER_P, face(TEACHER_P, [0, 0, 1.5]), "idle", "smile")],
                "hero": [kf(S_SCI, HERO_P, 0, "idle", "smile"),
                         kf(B["w1"], HERO_P, 0, "celebrate", "laugh"),
                         kf(S_OUT, HERO_P, 0, "celebrate", "laugh")],
                "friend": [kf(S_SCI, FRIEND_P, 0, "idle", "smile"),
                           kf(B["w1"], FRIEND_P, 0, "celebrate", "laugh"),
                           kf(S_OUT, FRIEND_P, 0, "celebrate", "laugh")],
            },
        },
        {   # Outro: Max does his own homework now — sitting on the bedroom
            # floor ('sit' = seated on the ground, legs straight out),
            # Robo beside him still holding the books, Mia waving. The
            # sitting close-ups use manual low shots: medium()/wide()
            # target y 4.3-4.8, but a sitting kid's head is at ~2.6.
            "id": "outro", "location": "bedroom",
            "startFrame": S_OUT, "endFrame": END,
            "fx": robot_fx(S_OUT, END, [5, 0, 1]),
            "cameraShots": cover(S_OUT, END, [
                # Wide pulled back + widened (was z 19, fov 55): Mia at -5 and
                # Robo at +5 were both half-cut at the frame edges.
                lambda a, b: shot(a, b, [0, 6.5, 20.5], [0, 6.2, 19],
                                  [0, 3.2, 0], [0, 3.2, 0], 62),
                lambda a, b: shot(a, b, [-0.5, 3.0, 11], [-0.5, 2.9, 10],
                                  [0, 2.4, 1], [0, 2.4, 1], 50),
                lambda a, b: shot(a, b, [0, 2.8, 8], [0, 2.7, 7.2],
                                  [0, 2.4, 1], [0, 2.4, 1], 45),
            ]),
            "characters": {
                "hero": hold(S_OUT, END, [0, 0, 1], 0, "sit", "smile"),
                "friend": [kf(S_OUT, [-5, 0, 1], 0, "idle", "smile"),
                           kf(B["b14"], [-5, 0, 1], 0, "wave", "smile"),
                           kf(END, [-5, 0, 1], 0, "wave", "smile")],
            },
        },
    ]
