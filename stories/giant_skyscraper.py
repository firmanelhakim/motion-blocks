"""GIANT SKYSCRAPER — "What If You Grew to the Size of a Skyscraper?"

Science explainer, lead: Kai, an R6 cool_kid (black spiky hair, green
hoodie — kept the whole video, at scale 1 and at scale 3). Max watches
from the giant's feet; the teacher explains the Square-Cube Law.

The science, kept exactly as verified:
- Grow 100x taller (~180 m) and your weight grows a MILLION times
  (100 cubed), but bone strength only grows TEN THOUSAND times (100
  squared). Every bone takes 100x more stress. Stand up… crunch.
  (Square-Cube Law.)
- You would overheat: your body makes heat with its volume (up a
  million) but loses it through your skin (up only ten thousand).
  You are a walking oven.
- Your brain sits ~40 m above your heart — about THIRTEEN stories,
  not thirty. (For a "30 stories" line the giant would need to be
  roughly 400 m tall.) Pumping blood up there? Your heart taps out.

WHY THE LEAD IS R6, NOT BOLT BOY: the giant has to buckle and fall
flat (the rx=-pi/2 lying pattern), pant from the heat ('panting'), and
collapse flat again. Kit characters in stories fall back to 'idle' for
knocked / panting / sleep, so a kit giant could never fall down or pant
— the whole second half of the video would not read. An R6 giant can do
all of it. (R6 'knocked' itself only spins the torso and never lies the
body down — that is why both falls use the lying pattern, not 'knocked'.) The growth / shrink are the documented look-swap (a second cast
entry at scale 3, parked OFF when not in use).

Filmable-limits notes (honest):
- A literal 100x giant (~180 m) cannot be staged — the town is a
  fixed size. The giant is scale 3 (~18 studs tall, clearly taller
  than the houses); the "100 times" and "180 metres" live in the
  narration + the classroom board.
- The two bar scales (weight x1,000,000 vs bone strength x10,000)
  cannot be staged as bars. The classroom board carries both numbers.
- The X-ray legs with hairline cracks cannot be staged. The collapse
  (lying flat, rx=-pi/2) + the board carry the bones beat.
- Turning red / steam / morphing into an oven cannot be staged (no
  red skin, no steam). The heat beat is Kai 'panting' + the board
  ("HEAT MADE x1,000,000" / "SKIN x10,000").
- The heart at the bottom of an elevator shaft cannot be staged. The
  blood beat is a low-angle shot up the giant (he towers) + Max
  pointing up from his feet + the board line in the narration
  ("forty metres… thirteen stories").

Locations: 'street' (hook, normal Kai); 'crossroads' (the giant —
growth, fall, heat, blood; the open intersection has room for a
scale-3 giant + a friend 10 studs away); 'classroom' (the Square-Cube
boards + the shout trio); 'house' (the shrink + the door).

Build (run the previews serially — do NOT run make_short.py alongside
other stories):
    python scripts/make_short.py stories/giant_skyscraper.py --stills
"""
import math

from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, shot, split_shots, wide  # noqa: F401

TITLE = "GROW TO THE SIZE OF A SKYSCRAPER"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b0", "text": "What if you grew to the size of a skyscraper?", "pause": 0.10},
    {"id": "b1", "text": "In this town, Kai just grew a hundred times taller. About a hundred and eighty metres.", "pause": 0.08},
    {"id": "b2", "text": "Amazing, right? …Nope.", "pause": 0.10},
    {"id": "b3", "text": "Blame the Square-Cube Law. Grow a hundred times taller, and your weight grows a million times.", "pause": 0.08},
    {"id": "b4", "text": "But bone strength only grows ten thousand times. Every bone takes a hundred times more stress.", "pause": 0.08},
    {"id": "w1", "text": "SQUARE!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "CUBE!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "LAW!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b5", "text": "Stand up… crunch.", "pause": 0.10},
    {"id": "b6", "text": "And you would overheat. Your body makes heat with its volume but loses it through your skin.", "pause": 0.08},
    {"id": "b7", "text": "Volume is up a million. Skin only ten thousand. You are a walking oven.", "pause": 0.08},
    {"id": "b8", "text": "Plus, your brain sits forty metres above your heart. About thirteen stories up.", "pause": 0.08},
    {"id": "b9", "text": "Pumping blood up there? Your heart taps out.", "pause": 0.10},
    {"id": "b10", "text": "Being a giant? Physics says no.", "pause": 0.08},
    {"id": "b11", "text": "Which superpower should we ruin next? Tell us below.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05,
         "dropouts": [("b4+0.3", "w3.end")]}
SFX = [
    ("b0", "whoosh"),
    ("b1+0.5", "riser", {"dur": 1.6}),
    ("b2+0.3", "pop_down"),
    ("b3+0.5", "pop", {"f": 700}),
    ("b4+0.5", "pop", {"f": 800}),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b5+0.5", "thud"),
    ("b6+0.5", "sad"),
    ("b7+0.5", "pop", {"f": 600}),
    ("b8+0.5", "pop", {"f": 650}),
    ("b9+1.3", "thud"),
    ("b10+0.5", "sparkle"),
    ("b11+1.0", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
KAI = {"extends": "cool_kid", "hair": {"style": "spikyAnime", "color": "black"},
       "top": {"style": "hoodie", "color": "green", "secondary": "white"},
       "bottom": {"style": "jeans", "color": "denim"},
       "shoes": {"color": "white", "sole": "white"}}
CAST = {
    # Kai, normal size (hook, classroom cutaway, shrink).
    "hero": KAI,
    # Kai the giant: the SAME look at scale 3 (~18 studs — clearly
    # taller than the houses). Swapped in/out with the OFF parking
    # trick at the scene boundaries.
    "hero_giant": {**KAI, "scale": 3},
    # Max, tiny at the giant's feet (his no_friction look).
    "friend": {"extends": "kid_boy", "hair": {"style": "spikyAnime", "color": "blue"},
               "top": {"style": "hoodie", "color": "red", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"},
               "shoes": {"color": "white", "sole": "white"}},
    "teacher": {"extends": "teacher"},
}


# 4. SCENES --------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END
    S_GROW = B["b1"] - 1     # crossroads: the growth
    S_CLASS = B["b3"] - 1    # classroom: the Square-Cube boards
    S_FALL = B["b5"] - 1     # crossroads: stand up… crunch
    S_HEAT = B["b6"] - 1     # crossroads: the walking oven
    S_BLOOD = B["b8"] - 1    # crossroads: heart → brain, 40 m up
    S_SHRINK = B["b10"] - 1  # house: he shrinks back

    # The crunch: 0.5 s into b5 he buckles and falls FLAT (the
    # rx=-pi/2 lying pattern — R6 'knocked' only spins the torso and
    # never lies the body down; proven on stills f640/f645, where he
    # stayed upright, arms up). b5 is a very short beat (0.93 s), so
    # the crunch CANNOT sit 1.3 s in (the first attempt put CRUNCH_F
    # past the scene end, making a negative shot) — and the fall scene
    # is only ~1.0 s long, so it holds ONE shot, not two.
    CRUNCH_F = B["b5"] + 15
    # The heart taps out: 1.3 s into b9 he collapses again.
    TAPOUT_F = B["b9"] + 39

    GIANT_P = [0, 0, 0.5]
    FRIEND_P = [10, 0, 0.5]  # 10 from the giant: spacing needs 9
    # (4.5 x (3 + 1) / 2) for a scale-3 giant + a scale-1 friend.

    # Giant cameras (the giant is ~18 studs tall, head at ~13.2):
    # a wide 2-shot centred between the giant and Max, a low-angle
    # towering shot (low_angle's scale param aims at 4.4 x scale, which
    # is the R6 head height — scale 3 aims at 13.2, the giant's head),
    # a face close-up (close_up takes scale the same way), and a
    # mid-body medium.
    def _giant_wide(a, b):
        return shot(a, b, [5, 12, 38], [5, 11.5, 36],
                    [5, 9, 0], [5, 9, 0], 58)

    def _giant_low(a, b):
        return low_angle(a, b, [0, 0, 0.5], dist=30, eye_height=1.2, fov=50, scale=3)

    def _giant_face(a, b, shake=None):
        return close_up(a, b, GIANT_P, scale=3, shake=shake)

    def _giant_med(a, b):
        return shot(a, b, [0, 10, 16], [0, 9.8, 15],
                    [0, 9, 0.5], [0, 9, 0.5], 50)

    # The fall / tapout shot: the giant is standing at the start of the
    # shot and lying flat at the end, so the frame must hold BOTH — the
    # standing head (y 13) and the lying body (y ~1, z 0.5 to -17.5).
    # Two tighter attempts FAILED and were reverted: a far south shot
    # ([2, 7, 38] targeting the midpoint) foreshortened the lying body
    # into a small unreadable box, and an east side-on shot ([25, 4, -8])
    # is blocked by the big crossroads tree and a lamppost. _giant_wide
    # (target y 9) is the shot that works: the fall reads clearly, the
    # giant is large and recognisable lying flat, Max visible beside
    # him. Its only cost is empty sky in the top half of the frame.
    def _giant_fall(a, b):
        return _giant_wide(a, b)

    return [
        {   # Hook: the big question over normal Kai's face, on the street.
            # One medium shot — the scene is only b0 (2.2 s), so there
            # is no room for a second shot (the first attempt split a
            # shot across B["b1"]..S_GROW, a negative range, because
            # S_GROW is B["b1"]-1).
            "id": "hook", "location": "street",
            "startFrame": 0, "endFrame": S_GROW,
            "cameraShots": [medium(0, S_GROW, [0, 0, 0.5])],
            "characters": {
                "hero": hold(0, S_GROW, [0, 0, 0.5], 0, "idle", "shocked"),
            },
        },
        {   # The growth: at S_GROW Kai swaps out (OFF) and the giant
            # swaps in at the same spot, while the camera pulls back
            # wide — the swap + the pull-back + the riser read as
            # growth. Max appears at his feet, 10 studs away, staring
            # up. "Amazing, right? …Nope." plays over the giant's
            # 'shocked' face and Max's 'shocked' face.
            "id": "grow", "location": "crossroads",
            "startFrame": S_GROW, "endFrame": S_CLASS,
            "cameraShots": cover(S_GROW, S_CLASS, [
                _giant_wide,
                _giant_low,
                _giant_med,
            ]),
            "characters": {
                "hero": [kf(S_GROW, [0, 0, 0.5], 0, "idle", "shocked"),
                         kf(S_GROW + 1, OFF, 0, "idle", "shocked"),
                         kf(S_CLASS, OFF, 0, "idle", "shocked")],
                "hero_giant": [kf(S_GROW, OFF, 0, "idle", "shocked"),
                               kf(S_GROW + 1, GIANT_P, 0, "idle", "shocked"),
                               kf(S_CLASS, GIANT_P, 0, "idle", "shocked")],
                "friend": [kf(S_GROW, OFF, 0, "idle", "shocked"),
                           kf(S_GROW + 1, FRIEND_P, 0, "idle", "shocked"),
                           kf(S_CLASS, FRIEND_P, 0, "idle", "shocked")],
            },
        },
        {   # The Square-Cube Law: the teacher explains at the board
            # while Kai (normal size — a classroom cutaway; a 18-stud
            # giant cannot fit in the classroom) and Max listen. The
            # board carries both numbers, and the shout trio
            # ("SQUARE! CUBE! LAW!") lands on Kai pointing.
            "id": "lesson", "location": "classroom",
            "boardText": ["WEIGHT x1,000,000", "BONES x10,000", "SQUARE-CUBE LAW"],
            "startFrame": S_CLASS, "endFrame": S_FALL,
            "cameraShots": cover(S_CLASS, S_FALL, [
                lambda a, b: wide(a, b, [-0.25, 0, 0], dist=24),
                lambda a, b: medium(a, b, [0, 0, 1]),
                lambda a, b: close_up(a, b, [0, 0, 1.5], shake=0.08),
            ]),
            "characters": {
                "teacher": [kf(S_CLASS, [-5.5, 0, -2], face([-5.5, 0, -2], [0, 0, 1.5]), "idle", "smile"),
                            kf(B["b4"], [-5.5, 0, -2], face([-5.5, 0, -2], [0, 0, 1.5]), "point", "smile"),
                            kf(S_FALL, [-5.5, 0, -2], face([-5.5, 0, -2], [0, 0, 1.5]), "idle", "smile")],
                "hero": [kf(S_CLASS, [0, 0, 1.5], 0, "idle", "smile"),
                         kf(B["w1"], [0, 0, 1.5], 0, "point", "panic"),
                         kf(S_FALL, [0, 0, 1.5], 0, "point", "panic")],
                "friend": hold(S_CLASS, S_FALL, [5, 0, 1.5], 0, "idle", "shocked"),
            },
        },
        {   # The fall: back at the crossroads, the giant tries to stand
            # — he was standing, now he buckles. At CRUNCH_F he goes
            # 'knocked' and stays down. Max watches, 'shocked'.
            "id": "fall", "location": "crossroads",
            "startFrame": S_FALL, "endFrame": S_HEAT,
            "cameraShots": [
                _giant_fall(S_FALL, S_HEAT),
            ],
            "characters": {
                "hero_giant": [
                    # The crunch: he buckles and falls FLAT. This does NOT
                    # use R6 'knocked' — 'knocked' spins the torso (a dizzy
                    # top) and never lies the body down: the first attempt
                    # showed him still upright at f640/f645, arms up, no
                    # fall at all. The lying pattern is the friction_5_seconds
                    # one: an upright keyframe at CRUNCH_F-1, then rx=-pi/2
                    # at CRUNCH_F — a 1-frame tip, so he is flat on his
                    # back (face up, body toward -Z) for the rest of the
                    # scene. He gets up again at the fall->heat cut (the
                    # heat keyframe has no rx, so he snaps upright in 1
                    # frame at the cut — the cut hides the get-up).
                    kf(S_FALL, GIANT_P, 0, "walk", "panic"),
                    kf(CRUNCH_F - 1, GIANT_P, 0, "walk", "panic"),
                    kf(CRUNCH_F, GIANT_P, 0, "idle", "shocked", rx=-math.pi / 2),
                    kf(S_HEAT, GIANT_P, 0, "idle", "shocked", rx=-math.pi / 2),
                ],
                "friend": hold(S_FALL, S_HEAT, FRIEND_P, 0, "idle", "shocked"),
            },
        },
        {   # The heat: he sits up, panting — a walking oven. The red /
            # steam / oven morph cannot be staged, so the panting +
            # the board numbers (carried in the narration here) do the
            # work. Wide + low-angle so the panting giant fills the
            # frame.
            "id": "heat", "location": "crossroads",
            "startFrame": S_HEAT, "endFrame": S_BLOOD,
            "cameraShots": cover(S_HEAT, S_BLOOD, [
                _giant_wide,
                _giant_low,
                _giant_med,
            ]),
            "characters": {
                "hero_giant": hold(S_HEAT, S_BLOOD, GIANT_P, 0, "panting", "panic"),
                "friend": hold(S_HEAT, S_BLOOD, FRIEND_P, 0, "idle", "shocked"),
            },
        },
        {   # The blood: his brain sits forty metres above his heart.
            # The low-angle towering shot is the visual — the giant's
            # whole height, Max tiny at his feet pointing up. At
            # TAPOUT_F his heart taps out and he collapses ('knocked').
            "id": "blood", "location": "crossroads",
            "startFrame": S_BLOOD, "endFrame": S_SHRINK,
            "cameraShots": [
                # Three ~2 s shots. The first attempt gave the low shot
                # all of b8 (4.0 s, too long) and left a 0.9 s tail
                # after the tapout (too short). The third shot is a
                # WIDE, not a medium: after the tapout he is lying flat
                # (y ~1), and a medium aimed at the standing head (y 9)
                # would cut the lying body out of frame.
                _giant_low(S_BLOOD, (S_BLOOD + B["b9"]) // 2),
                _giant_wide((S_BLOOD + B["b9"]) // 2, B["b9"]),
                _giant_fall(B["b9"], S_SHRINK),
            ],
            "characters": {
                "hero_giant": [
                    kf(S_BLOOD, GIANT_P, 0, "idle", "panic"),
                    kf(B["b9"], GIANT_P, 0, "panting", "panic"),
                    # The tapout: he collapses FLAT, same lying pattern
                    # as the fall (R6 'knocked' only spins — it never
                    # lies him down). Upright at TAPOUT_F-1, flat at
                    # TAPOUT_F, flat through the scene end.
                    kf(TAPOUT_F - 1, GIANT_P, 0, "panting", "panic"),
                    kf(TAPOUT_F, GIANT_P, 0, "idle", "shocked", rx=-math.pi / 2),
                    kf(S_SHRINK, GIANT_P, 0, "idle", "shocked", rx=-math.pi / 2),
                ],
                "friend": [kf(S_BLOOD, FRIEND_P, 0, "point", "shocked"),
                           kf(S_SHRINK, FRIEND_P, 0, "point", "shocked")],
            },
        },
        {   # The shrink: at S_SHRINK the giant swaps out (OFF) and
            # normal Kai swaps back in at the house, in front of the
            # door — "Being a giant? Physics says no." He celebrates,
            # hugs the door (facing the camera, 'celebrate' + 'laugh';
            # there is no hug anim), and waves for the closing line.
            "id": "shrink", "location": "house", "variant": "blue",
            "startFrame": S_SHRINK, "endFrame": END,
            # The outro two-shot: the first attempt's medium (dist 12)
            # cropped BOTH faces at the frame edges (f1181, f1230 — the
            # push-in shrinks the half-width to ~2.8 while the faces sit
            # at ±2.5). cover() over 151 frames gives only 2 shots
            # (wide + medium, no close-up), so the last shot is made
            # explicit: a medium pulled back to dist 17 (half-width
            # ~4.4) so both faces stay whole through the final frame.
            "cameraShots": split_shots(S_SHRINK, END, [
                lambda a, b: wide(a, b, [2.5, 0, -2], dist=20),
                lambda a, b: medium(a, b, [2.5, 0, -2], dist=17),
            ]),
            "characters": {
                # The giant is OFF from the very first frame of this
                # scene (not parked at his crossroads spot for one
                # frame): the first attempt left him at GIANT_P at
                # S_SHRINK while the friend was already at the house
                # [5, 0, -2] — only 5.59 apart, but a scale-3 giant +
                # a scale-1 friend need 9. The swap happens at the
                # scene cut anyway.
                "hero_giant": [kf(S_SHRINK, OFF, 0, "knocked", "shocked"),
                               kf(END, OFF, 0, "knocked", "shocked")],
                "hero": [kf(S_SHRINK, OFF, 0, "idle", "laugh"),
                         kf(S_SHRINK + 1, [0, 0, -2], 0, "celebrate", "laugh"),
                         kf(B["b11"], [0, 0, -2], 0, "wave", "laugh"),
                         kf(END, [0, 0, -2], 0, "wave", "laugh")],
                "friend": [kf(S_SHRINK, [5, 0, -2], 0, "idle", "smile"),
                           kf(B["b11"], [5, 0, -2], 0, "wave", "smile"),
                           kf(END, [5, 0, -2], 0, "wave", "smile")],
            },
        },
    ]
