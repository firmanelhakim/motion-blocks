"""FRICTION 5 SECONDS — "What If Friction Vanished for 5 Seconds?"

Science explainer, lead: Mia, an R6 kid_girl (pigtails, teal sweater —
her no_friction look, but here she LEADS). Max watches from the sidewalk.

The one science idea: friction is what lets you walk, and it is also
what stops you. Take it away for five seconds and everything slides;
when it slams back, all that motion turns into heat.

HOW THIS DIFFERS FROM no_friction ("What if there was no friction?"):
that video is Max living a whole frictionless DAY on the ice street —
the slide, the lamppost grab, the bus, the bedpost. THIS video is five
seconds only: the snap-back is the whole point. Its beats are the ones
no_friction never had — the shoelaces untying, the screws backing out,
the feet stopping dead while the body keeps going, and the heat.

Filmable-limits notes (honest):
- The shoelaces untying cannot be shown literally (no lace geometry,
  no shoe-removal). The beat is a low close-up on Mia's sliding shoes
  + her shocked face; the narration carries the knot science.
- The bookshelf collapsing cannot be shown literally (no bookshelf
  prop, no collapsing furniture). The screws beat is a classroom
  board ("SCREWS = FRICTION") + teacher; the narration keeps the
  bookshelf line.
- The heat squiggles / steam cannot be shown literally. The heat beat
  is a classroom board ("MOTION → HEAT") + Mia panting; the narration
  carries the carpet burn.
- The bus is the only vehicle in the engine (school bus, environment
  geometry, cannot move). The "bus keeps drifting" beat is a
  wheel-level pan along the bus's east face (a different camera from
  no_friction's high pan) + whoosh + narration.

The slip pose (proven in no_friction): the kid leans back (rz=0.4)
with a 'panic' face and 'walk' anim while her keyframe position slides
across the street — the legs walk but the body glides, which reads as
sliding. rz=0 once she faceplants ('knocked').

Locations: 'street' (hook, slide, shoes, snap, outro); 'school_exterior'
(the bus — the bus sits at stage [26, 0, -18], spanning z -26..-10,
so the wheel-level pan stands east of it at x=40); 'classroom' (the
screws board and the heat board).

Build (run the previews serially — do NOT run make_short.py alongside
other stories):
    python scripts/make_short.py stories/friction_5_seconds.py --stills
"""
import math

from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, split_shots, wide  # noqa: F401

TITLE = "FRICTION VANISHED FOR 5 SECONDS"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b0", "text": "What if friction vanished for five seconds?", "pause": 0.10},
    {"id": "b1", "text": "In this town, friction just switched off. For five seconds.", "pause": 0.08},
    {"id": "b2", "text": "Mia lifts one foot to step, and her other foot shoots backwards.", "pause": 0.08},
    {"id": "b3", "text": "Walking works by pushing against the ground. No friction? Your foot just slides.", "pause": 0.08},
    {"id": "b4", "text": "Her shoelaces untie themselves. Knots only hold because of friction.", "pause": 0.08},
    {"id": "b5", "text": "Cars cannot grip the road. Brakes do nothing. The bus just keeps drifting.", "pause": 0.08},
    {"id": "b6", "text": "And screws and nails are held in by friction too. Your bookshelf is now a suggestion.", "pause": 0.08},
    {"id": "b7", "text": "Then, second six: friction slams back. Her feet stop dead. The rest of her does not.", "pause": 0.10},
    {"id": "w1", "text": "FRICTION!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "IS!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "BACK!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b8", "text": "Everything sliding grinds to a halt, turning motion into heat. Hello, carpet burn.", "pause": 0.08},
    {"id": "b9", "text": "Friction: annoying, invisible, and the only reason your house stays standing.", "pause": 0.10},
    {"id": "b10", "text": "What is the first thing you would lose without it? Tell us below.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05,
         "dropouts": [("b7+0.3", "w3.end")]}
SFX = [
    ("b0", "whoosh"),
    ("b1", "whoosh"),
    ("b2+0.3", "swish"),
    ("b3+0.4", "pop", {"f": 600}),
    ("b4+0.5", "pop_down"),
    ("b5+0.3", "whoosh"),
    ("b6+0.5", "pop", {"f": 700}),
    ("b7+0.4", "riser", {"dur": 1.6}),
    ("b7+1.3", "thud"),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b8+0.5", "pop", {"f": 600}),
    ("b9+0.5", "sparkle"),
    ("b10+1.0", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
CAST = {
    # Mia leads this one (her no_friction look: pigtails, teal sweater).
    "hero": {"extends": "kid_girl", "hair": {"style": "pigtails", "color": "brown"},
             "top": {"style": "sweater", "color": "teal", "secondary": "white"},
             "bottom": {"style": "skirt", "color": "navy"},
             "shoes": {"color": "white", "sole": "white"}},
    # Max watches from the sidewalk (his no_friction look).
    "friend": {"extends": "kid_boy", "hair": {"style": "spikyAnime", "color": "blue"},
               "top": {"style": "hoodie", "color": "red", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"},
               "shoes": {"color": "white", "sole": "white"}},
    "teacher": {"extends": "teacher"},
}


# 4. SCENES --------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END
    S_SLIDE = B["b2"] - 1    # street: the slide begins
    S_SHOES = B["b4"] - 1    # street: the shoelaces (low close-up)
    S_BUS = B["b5"] - 1      # school exterior: the bus
    S_CLASS = B["b6"] - 1    # classroom: the screws board
    S_SNAP = B["b7"] - 1     # street: the snap-back + faceplant
    S_HEAT = B["b8"] - 1     # classroom: the heat board
    S_OUT = B["b9"] - 1      # street: the outro

    # The snap: her feet stop dead 1.3 s into b7 (FALL_F), and the body
    # keeps going — she faceplants ('knocked') and stays down through
    # the "FRICTION! IS! BACK!" shouts.
    FALL_F = B["b7"] + 39    # ~1.3 s into b7
    FRIEND_P = [-9, 0, 0.5]

    # Mia's slide lane on the street: x from -2 to 2 at z=0.5. The lane
    # stays clear of the hydrant at x ~ -5.5 and the traffic light at
    # x > 4; Max watches from x=-9, 7 studs from her start.
    def _hx(f):
        if f <= S_SLIDE:
            return -2.0
        if f >= S_SHOES:
            return 2.0
        return -2.0 + 4.0 * (f - S_SLIDE) / (S_SHOES - S_SLIDE)

    # Her slide across the schoolyard in front of the school (z=17 in
    # stage coords; the schoolyard is z -13..5, the bus is at z -26..-10).
    def _bx(f):
        if f <= S_BUS:
            return 6.0
        if f >= B["w1"]:
            return 12.0
        return 6.0 + 6.0 * (f - S_BUS) / (B["w1"] - S_BUS)

    return [
        {   # Hook: the big question over Mia's face, then the setup.
            "id": "hook", "location": "street",
            "startFrame": 0, "endFrame": S_SLIDE,
            "cameraShots": [medium(0, B["b1"], [-2, 0, 0.5])] + split_shots(B["b1"], S_SLIDE, [
                lambda a, b: wide(a, b, [-2, 0, 0.5], dist=18),
                lambda a, b: medium(a, b, [-2, 0, 0.5]),
            ]),
            "characters": {
                "hero": hold(0, S_SLIDE, [-2, 0, 0.5], 0, "idle", "shocked"),
                "friend": hold(0, S_SLIDE, FRIEND_P, 0, "idle", "smile"),
            },
        },
        {   # The slide: she tries to step, her foot shoots back, she
            # glides. The tracking camera follows her x so she never
            # leaves the frame; the wide shows the whole slide.
            "id": "slide", "location": "street",
            "startFrame": S_SLIDE, "endFrame": S_SHOES,
            "cameraShots": cover(S_SLIDE, S_SHOES, [
                lambda a, b: shot(a, b, [_hx(a), 5.6, 12.5], [_hx(b), 5.6, 12],
                                  [_hx(a), 4.3, 0.5], [_hx(b), 4.3, 0.5], 50),
                lambda a, b: wide(a, b, [0, 0, 0.5], dist=20),
                lambda a, b: medium(a, b, [_hx((a + b) // 2), 0, 0.5]),
            ]),
            "characters": {
                "hero": [kf(S_SLIDE, [-2, 0, 0.5], 0, "walk", "panic", rz=0.4),
                         kf(S_SHOES, [2, 0, 0.5], 0, "walk", "panic", rz=0.4)],
                "friend": hold(S_SLIDE, S_SHOES, FRIEND_P, 0, "idle", "shocked"),
            },
        },
        {   # The shoelaces: one low close-up on her sliding shoes while
            # "Her shoelaces untie themselves" plays. The laces cannot
            # be shown untying (no lace geometry) — the low angle on the
            # sliding shoes + her shocked face + the narration carry it.
            "id": "shoes", "location": "street",
            "startFrame": S_SHOES, "endFrame": S_BUS,
            "cameraShots": [
                # Two shots: the scene is 3.7 s, over the 3.5 s max for
                # one shot. Low close-up on the sliding shoes first,
                # then a medium tracking her slide. The low shot is
                # pulled back (dist ~10.5) and aimed at y 0.6 — the
                # first attempt (camera 7.5 away, target y 0.8) cropped
                # her torso huge and cut her feet off.
                shot(S_SHOES, 436, [2, 2.0, 11], [2, 1.8, 10.2],
                     [2, 0.6, 0.5], [2, 0.6, 0.5], 50),
                medium(436, S_BUS, [3, 0, 0.5]),
            ],
            "characters": {
                "hero": [kf(S_SHOES, [2, 0, 0.5], 0, "walk", "panic", rz=0.4),
                         kf(S_BUS, [4, 0, 0.5], 0, "walk", "panic", rz=0.4)],
                "friend": hold(S_SHOES, S_BUS, FRIEND_P, 0, "idle", "shocked"),
            },
        },
        {   # The bus: it cannot grip, it keeps drifting. The yellow
            # school bus is environment geometry at stage [26, 0, -18],
            # spanning z -26..-10, and cannot move — so the drift is a
            # WHEEL-LEVEL pan along the bus's east face (a different
            # camera from no_friction's high pan): the SCHOOL BUS label
            # and windows sweep past at wheel height while the bus stays
            # visible the whole shot. Mia slides across Main St in front
            # of the school (z=17) in the other shot; Max watches from
            # the far side of the street.
            "id": "bus", "location": "school_exterior",
            "startFrame": S_BUS, "endFrame": S_CLASS,
            "cameraShots": split_shots(S_BUS, S_CLASS, [
                lambda a, b: shot(a, b, [_bx(a), 5.6, 29], [_bx(b), 5.6, 29],
                                  [_bx(a), 4.3, 17], [_bx(b), 4.3, 17], 50),
                # Bus drift: low camera east of the bus, target pans
                # along the bus at wheel height. Pulled back to dist 22
                # (was 14) and aimed at y 1.2 — the first attempt filled
                # the frame with the bus side, cut the "SCHOOL BUS"
                # text, and showed only one tyre at the edge.
                # Bus drift: pulled back to dist 30 (was 22) — the first
                # attempt never had both wheels in frame together
                # (half-width ~6.4 at dist 22 vs the 16-stud bus). At
                # dist 30 the half-width is ~8.8, so mid-pan both
                # wheels are in frame.
                lambda a, b: shot(a, b, [56, 2.5, -12], [56, 2.5, -20],
                                  [26, 1.2, -12], [26, 1.2, -20], 55),
            ]),
            "characters": {
                "hero": [kf(S_BUS, [6, 0, 17], 0, "walk", "panic", rz=0.4),
                         kf(S_CLASS, [12, 0, 17], 0, "walk", "panic", rz=0.4)],
                "friend": hold(S_BUS, S_CLASS, [-6, 0, 17], 0, "idle", "shocked"),
            },
        },
        {   # The screws: the teacher explains at the board. The
            # bookshelf collapse cannot be staged (no bookshelf prop),
            # so the board carries the science and the narration keeps
            # the bookshelf line.
            "id": "screws", "location": "classroom",
            "boardText": ["SCREWS = FRICTION", "NO FRICTION", "= NO HOLD"],
            "startFrame": S_CLASS, "endFrame": S_SNAP,
            "cameraShots": cover(S_CLASS, S_SNAP, [
                lambda a, b: wide(a, b, [-0.25, 0, 0], dist=24),
                lambda a, b: medium(a, b, [0, 0, 1]),
                lambda a, b: close_up(a, b, [0, 0, 1.5]),
            ]),
            "characters": {
                "teacher": [kf(S_CLASS, [-5.5, 0, -2], face([-5.5, 0, -2], [0, 0, 1.5]), "idle", "smile"),
                            kf(B["b6"] + 30, [-5.5, 0, -2], face([-5.5, 0, -2], [0, 0, 1.5]), "point", "smile"),
                            kf(S_SNAP, [-5.5, 0, -2], face([-5.5, 0, -2], [0, 0, 1.5]), "idle", "smile")],
                "hero": hold(S_CLASS, S_SNAP, [0, 0, 1.5], 0, "idle", "shocked"),
                "friend": hold(S_CLASS, S_SNAP, [5, 0, 1.5], 0, "idle", "shocked"),
            },
        },
        {   # The snap-back: she slides the last stretch, her feet stop
            # dead at FALL_F and the rest of her does not — she
            # faceplants and stays down through the "FRICTION! IS!
            # BACK!" shouts. The faceplant is the no_friction bedroom
            # pattern (rx=-pi/2 lays her flat on her back, face up) —
            # the R6 'knocked' anim does NOT lie a character down, it
            # spins the torso (torsoRotY = t*10), which read as a
            # dizzy top with her back to the camera, so it is NOT used
            # here. The tip-over is sudden: a keyframe at FALL_F-1
            # holds her upright at the stop point, then FALL_F tips her
            # flat in one frame. Lying flat, her feet stay at [1, 0,
            # 0.5] and her head lands ~5.9 studs north (z ~ -5.4), so
            # the cameras target the body's midpoint [1, 0.8, -2.5].
            "id": "snap", "location": "street",
            "startFrame": S_SNAP, "endFrame": S_HEAT,
            "cameraShots": [
                shot(S_SNAP, FALL_F,
                     [-2, 5.6, 12.5], [1, 5.6, 12],
                     [-2, 4.3, 0.5], [1, 4.3, 0.5], 50),
                # Lying flat, from the fall to the first shout word
                # (3.4 s — just under the 3.5 s max). From the EAST
                # SIDE (fix round): the first attempt shot her from
                # the south, end-on to the body — foreshortened into
                # a flat pile, face hidden, caption across the body.
                # From the east the whole body lies across the frame
                # (feet left, head right), her face reads in profile,
                # and the caption falls below the body.
                shot(FALL_F, B["w1"],
                     [14, 3, -2.5], [13.5, 2.9, -2.5],
                     [1, 0.8, -2.5], [1, 0.8, -2.5], 55),
                # All three shout words in one 2.1 s shot, with shake —
                # the old split left a 0.7 s tail after w3, under the
                # 1.0 s minimum. Pushed in a little closer than the
                # lying shot so the cut reads.
                shot(B["w1"], S_HEAT,
                     [12, 2.8, -2.5], [11.5, 2.7, -2.5],
                     [1, 0.8, -2.5], [1, 0.8, -2.5], 55, shake=0.08),
            ],
            "characters": {
                "hero": [kf(S_SNAP, [-2, 0, 0.5], 0, "walk", "panic", rz=0.4),
                         # Tip-over in-betweens (fix round): the first
                         # attempt tipped her flat in ONE frame, so the
                         # fall itself was invisible. She slides upright
                         # to the stop point (FALL_F-11), tips to 45° at
                         # FALL_F-5, flat at FALL_F.
                         kf(FALL_F - 11, [1, 0, 0.5], 0, "walk", "panic", rz=0.4),
                         kf(FALL_F - 5, [1, 0, 0.5], 0, "walk", "panic", rx=-math.pi / 4, rz=0.2),
                         kf(FALL_F, [1, 0, 0.5], 0, "idle", "shocked", rx=-math.pi / 2),
                         kf(S_HEAT, [1, 0, 0.5], 0, "idle", "shocked", rx=-math.pi / 2)],
                "friend": hold(S_SNAP, S_HEAT, FRIEND_P, 0, "idle", "shocked"),
            },
        },
        {   # The heat: everything sliding grinds to a halt, turning
            # motion into heat. The heat squiggles / steam cannot be
            # staged, so the board carries "MOTION → HEAT" and Mia
            # pants (she is hot from the friction burn) while the
            # teacher points at the board.
            "id": "heat", "location": "classroom",
            "boardText": ["MOTION → HEAT", "SLIDING STOPS", "HEAT APPEARS"],
            "startFrame": S_HEAT, "endFrame": S_OUT,
            "cameraShots": cover(S_HEAT, S_OUT, [
                lambda a, b: wide(a, b, [-0.25, 0, 0], dist=24),
                lambda a, b: medium(a, b, [0, 0, 1]),
                lambda a, b: close_up(a, b, [0, 0, 1.5]),
            ]),
            "characters": {
                "teacher": [kf(S_HEAT, [-5.5, 0, -2], face([-5.5, 0, -2], [0, 0, 1.5]), "idle", "smile"),
                            kf(B["b8"] + 30, [-5.5, 0, -2], face([-5.5, 0, -2], [0, 0, 1.5]), "point", "smile"),
                            kf(S_OUT, [-5.5, 0, -2], face([-5.5, 0, -2], [0, 0, 1.5]), "idle", "smile")],
                "hero": hold(S_HEAT, S_OUT, [0, 0, 1.5], 0, "panting", "shocked"),
                "friend": hold(S_HEAT, S_OUT, [5, 0, 1.5], 0, "idle", "shocked"),
            },
        },
        {   # Outro: Mia, dazed, holds the lone shelf plank ('wood_plank'
            # prop) and gives a thumbs-up to the ground — the closest
            # anim is 'wave' + 'laugh'. Max waves beside her.
            "id": "outro", "location": "street",
            "startFrame": S_OUT, "endFrame": END,
            # The outro medium was pulled back to dist 17 (fix round):
            # at dist 12 the half-width shrinks to ~2.8 while Mia and
            # Max stand at ±2.5, so BOTH faces were cropped at the
            # frame edges (f1190, f1215). At dist 17 the half-width is
            # ~4.4 and both faces stay whole.
            "cameraShots": cover(S_OUT, END, [
                lambda a, b: wide(a, b, [0, 0, 0.5], dist=18),
                lambda a, b: medium(a, b, [0, 0, 0.5], dist=17),
                lambda a, b: close_up(a, b, [-2.5, 0, 0.5]),
            ]),
            "characters": {
                "hero": [kf(S_OUT, [-2.5, 0, 0.5], 0, "idle", "laugh", "wood_plank"),
                         kf(B["b10"], [-2.5, 0, 0.5], 0, "wave", "laugh", "wood_plank"),
                         kf(END, [-2.5, 0, 0.5], 0, "wave", "laugh", "wood_plank")],
                "friend": [kf(S_OUT, [2.5, 0, 0.5], 0, "idle", "smile"),
                           kf(B["b10"], [2.5, 0, 0.5], 0, "wave", "smile"),
                           kf(END, [2.5, 0, 0.5], 0, "wave", "smile")],
            },
        },
    ]
