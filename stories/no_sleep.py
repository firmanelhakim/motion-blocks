"""NO SLEEP — "What If You Never Needed Sleep?"

Science explainer, lead: R6 kid_boy ("Tommy") — a kid who stays up for
days, loves it at first, then goes foggy: he forgets the lesson and
cannot learn the new game. His friend shows him his own brain: during
sleep, fluid washes through it and clears away the waste, and the brain
replays the day and files the memories. He finally sleeps — and wakes
up sharp. Sleep isn't wasted time; it is brain maintenance.

The ONE science idea: sleep cleans your brain and files your memories.
During deep sleep, cerebrospinal fluid flows through the brain and
washes away metabolic waste (including beta-amyloid, the substance
linked to Alzheimer's), and the brain replays the day to store memories.
That is why you feel foggy after an all-nighter.

THE BRAIN: fx shape 'brain' (BlockyBrain — a pink blocky brain ~2.25
wide with a glowing blue wash blanket over the right hemisphere +
falling glowing blue droplets, animated on its own 3s cycle). It gets
a studio close-up while the friend points at it, and it floats in the
bedroom over the sleeping hero during the shout climax.
THE CLOCK: fx shape 'clock' (BigClock — a wall clock ~4.2 across with
bold numbers and two thick hands spinning continuously, 2 turns per 3s
loop). It hangs in the bedroom at [5, 6, -4] through the whole story
so the spinning hands sell "days passing" without sleep.
TIRED HERO: there is no tired-eyes expression, so fogginess is faked
with 'sleeping' (heavy eyelids) + 'panic' when he forgets, and 'idle' /
'panting' as the days pile up. He starts bright ('smile'/'laugh'),
goes foggy, then sleeps and wakes up sharp ('smile', 'celebrate').

Sleep staging: the 'sleep' anim on its own only breathes/snores
upright — it does NOT lie the body flat. Lying flat follows the
proven _test_week2_5_props2.py pattern: root at the FOOT of the bed
[-7, 2.4, -1.6] with rx=-pi/2, so the head lands on the pillow
(z ≈ -6.4). (The bed centre z ≈ -4.4 is NOT the root: a root there
would push the head past the headboard into the wall.)

FIX ROUND 1 (2026-11-22): the maintainer decided every Short must START with the
big "What if" question, so the narration now opens with b0 "What if you
never needed sleep?" over a hero close-up looking at camera; the old
"In this town," line follows as b1. Staging fixes: the BlockyBrain is
~4.9 studs wide at scale 1.4 (the 2.25 core is not the full width — the
hemisphere blocks reach x ±1.74), so the old 9-stud _brain_close cropped
it at both edges; cameras pulled back to 17→16 studs so the brain spans
~2/3 of the frame. The bedroom brain now floats above the sleeper
([-7, 5.5, -4]) instead of centre-frame, so it no longer hides the
BigClock in the sleep wide.

Build (fake timings — Kokoro is not installed on this VM):
    python3 /tmp/build_stories.py no_sleep
"""
import math

from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, orbit, shot, split_shots, static_shot, wide  # noqa: F401

TITLE = "SLEEP WASHES YOUR BRAIN"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b0", "text": "What if you never needed sleep?", "pause": 0.08},
    {"id": "b1", "text": "In this town, nobody needs to sleep. Not ever.", "pause": 0.08},
    {"id": "b2", "text": "Tommy stays up for days, and at first it is great. More time to play!", "pause": 0.08},
    {"id": "b3", "text": "No bedtime, no lights out. He plays all night, and all the next day too.", "pause": 0.08},
    {"id": "b4", "text": "But by day three, his brain gets foggy. He forgets what the teacher just said.", "pause": 0.08},
    {"id": "b5", "text": "He cannot learn the new game. His hands know the moves, but his brain does not.", "pause": 0.10},
    {"id": "b6", "text": "His friend shows him his own brain. Look, it is full of yesterday's mess.", "pause": 0.08},
    {"id": "b7", "text": "When you sleep, clean fluid washes through your brain and clears the waste away.", "pause": 0.08},
    {"id": "b8", "text": "It washes out the sticky stuff that builds up while you are awake.", "pause": 0.08},
    {"id": "b9", "text": "And while you sleep, your brain replays the day and files every memory away.", "pause": 0.10},
    {"id": "b10", "text": "So Tommy finally sleeps. One long, deep sleep.", "pause": 0.08},
    {"id": "w1", "text": "WASH!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "IT!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "CLEAN!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b11", "text": "He wakes up sharp. The game clicks, the lesson sticks.", "pause": 0.08},
    {"id": "b12", "text": "Sleep is not wasted time. It is brain maintenance.", "pause": 0.08},
    {"id": "b13", "text": "But tonight, Tommy is in bed by nine, and his brain is already dreaming about tomorrow's game.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05,
         "dropouts": [("b10+0.3", "w3.end")]}
SFX = [
    ("b1", "whoosh"),
    ("b2+0.5", "pop", {"f": 700}),
    ("b3+0.5", "pop", {"f": 600}),
    ("b4+0.5", "pop_down"),
    ("b5+0.4", "sad"),
    ("b6+0.4", "pop", {"f": 800}),
    ("b7+0.5", "sparkle"),
    ("b8+0.5", "bubbles"),
    ("b9+0.5", "sparkle"),
    ("b10+0.6", "riser", {"dur": 1.6}),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b11+0.5", "sparkle"),
    ("b12+0.6", "reveal"),
    ("b13+1.5", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
CAST = {
    # Tommy: blue spiky hair + red hoodie, kept the whole video so he is
    # recognisable in every scene, bright or foggy.
    "hero": {"extends": "kid_boy", "hair": {"style": "spikyAnime", "color": "blue"},
             "top": {"style": "hoodie", "color": "red", "secondary": "white"},
             "bottom": {"style": "jeans", "color": "denim"},
             "shoes": {"color": "white", "sole": "white"}},
    # The friend who shows Tommy his brain (nerd preset, glasses).
    "friend": {"extends": "nerd"},
    # Classroom teacher (ant_size.py convention).
    "teacher": {"extends": "teacher_woman", "skin": "fair", "hair": {"style": "bun", "color": "blonde"}},
}


# 4. SCENES --------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END
    S_PLAY = B["b2"] - 1    # bedroom night: plays all night, days pass
    S_CLASS = B["b4"] - 1   # classroom: foggy, forgets, cannot learn
    S_BRAIN = B["b6"] - 1   # studio: the friend shows him the brain
    S_SLEEP = B["b10"] - 1  # bedroom night: he finally sleeps (shouts)
    S_WAKE = B["b11"] - 1   # bedroom day: wakes up sharp

    # The BigClock on the bedroom wall: hands spin on their own 2-turns-
    # per-3s loop, so it sells "days passing" in every bedroom scene
    # without any keyframed movement — two keyframes, same position.
    def _clock(a, b):
        return [{"id": "clock", "shape": "clock", "scale": 1.2, "color": "#FFFFFF",
                 "keyframes": [{"frame": a, "position": [4, 6, -4]},
                               {"frame": b, "position": [4, 6, -4]}]}]

    # The BlockyBrain. In the studio it sits centre-frame at y 5 between
    # the two boys; in the bedroom it floats above the sleeper at
    # [0, 5, -2]. Its blue wash + droplets animate on their own 3s cycle.
    def _brain(a, b, pos):
        return [{"id": "brain", "shape": "brain", "scale": 1.4, "color": "#F4A7C3",
                 "keyframes": [{"frame": a, "position": pos},
                               {"frame": b, "position": pos}]}]

    HERO_P = [0, 0, 1.0]
    # Lying flat on the bed: root at the foot, rx=-pi/2 puts the head
    # toward the headboard (pillow at z -6.4). See module docstring.
    BED_P = [-7, 2.4, -1.6]
    BRAIN_P = [0, 5, 0]
    # Bedroom brain: floats above the SLEEPER (bed centre x -7, body
    # along z -1.6..-6.4), NOT centre-frame — the old [0, 5, -2] sat
    # between the wide camera and the BigClock and hid its left edge.
    # At x -7 the brain is left of frame and the clock (x 4) is fully
    # visible on the right in the sleep wide.
    BRAIN_BED_P = [-7, 5.5, -4]
    # Brain close-up maker: the brain is ~4.9 wide at scale 1.4 (the
    # 2.25 core is only the middle — hemisphere blocks reach x ±1.74,
    # and the front face sits ~1.5 studs closer than the centre), so
    # the old 9→7.5-stud camera cropped it at both edges (it read as a
    # pink dotted waffle). Portrait 1080x1920 at fov 50 has a ~29.4°
    # horizontal fov; 17→16 studs frames the front face at ~61-65% of
    # the frame width — about two-thirds, reading as a brain.
    def _brain_close(a, b, pos):
        return shot(a, b, [pos[0], pos[1] + 0.2, pos[2] + 17], [pos[0], pos[1], pos[2] + 16],
                    [pos[0], pos[1], pos[2]], [pos[0], pos[1], pos[2]], 50)

    return [
        {   # Hook: the big "What if" question first — Tommy looks at
            # the camera, wide-eyed, while the question plays; then he
            # celebrates as the "nobody needs to sleep" setup follows.
            # Shots are cut on the beat boundary so the question owns
            # the close-up and the setup owns the medium.
            "id": "hook", "location": "bedroom", "variant": "blue",
            "startFrame": 0, "endFrame": S_PLAY,
            "fx": _clock(0, S_PLAY),
            "cameraShots": [
                close_up(0, B["b1"], HERO_P),
                medium(B["b1"], S_PLAY, [0, 0, 1.0]),
            ],
            "characters": {
                "hero": [kf(0, HERO_P, 0, "idle", "shocked"),
                         kf(B["b1"], HERO_P, 0, "celebrate", "laugh"),
                         kf(S_PLAY, HERO_P, 0, "celebrate", "laugh")],
            },
        },
        {   # Days pass: night bedroom, Tommy plays on — dancing, bright
            # at first, then the fog creeps in (sleeping eyes, panting).
            "id": "play", "location": "bedroom", "variant": "blue", "isNight": True,
            "startFrame": S_PLAY, "endFrame": S_CLASS,
            "fx": _clock(S_PLAY, S_CLASS),
            "cameraShots": cover(S_PLAY, S_CLASS, [
                lambda a, b: wide(a, b, [0, 0, 0]),
                lambda a, b: medium(a, b, [0, 0, 1.0]),
                lambda a, b: close_up(a, b, HERO_P),
            ]),
            "characters": {
                "hero": [kf(S_PLAY, HERO_P, 0, "dance", "laugh"),
                         kf(B["b3"], HERO_P, 0, "dance", "laugh"),
                         kf(B["b3"] + 45, HERO_P, 0, "panting", "sleeping"),
                         kf(S_CLASS, HERO_P, 0, "panting", "sleeping")],
            },
        },
        {   # Classroom: the foggy brain in action. Tommy forgets the
            # lesson and cannot learn the new game; the teacher points
            # at the board. Hero stands in the free aisle (x in [-3, 3]),
            # clear of the student desks (x ±5.5, ±9.5).
            "id": "class", "location": "classroom",
            "boardText": ["WHY DO WE SLEEP?", "TO WASH THE BRAIN", "TO FILE MEMORIES"],
            "startFrame": S_CLASS, "endFrame": S_BRAIN,
            "cameraShots": cover(S_CLASS, S_BRAIN, [
                lambda a, b: wide(a, b, [0, 0, 0]),
                lambda a, b: close_up(a, b, [1.5, 0, 1.5]),
            ]),
            "characters": {
                "hero": [kf(S_CLASS, [1.5, 0, 1.5], 0, "idle", "sleeping"),
                         kf(B["b5"], [1.5, 0, 1.5], 0, "idle", "panic"),
                         kf(S_BRAIN, [1.5, 0, 1.5], 0, "idle", "panic")],
                "teacher": hold(S_CLASS, S_BRAIN, [-3.0, 0, -4.5], 0.5, "point", "deadpan", "pointer"),
            },
        },
        {   # The brain, close up: the friend points at it while it
            # washes itself clean. Studio plain set, blue variant wall.
            # Hero left, friend right, brain floating centre at y 5.
            "id": "brain", "location": "studio", "variant": "blue",
            "startFrame": S_BRAIN, "endFrame": S_SLEEP,
            "fx": _brain(S_BRAIN, S_SLEEP, BRAIN_P),
            "cameraShots": cover(S_BRAIN, S_SLEEP, [
                lambda a, b: _brain_close(a, b, BRAIN_P),
                # Wide medium: at the default dist 12 the 4.9-wide brain
                # filled ~85% of the frame and hid both boys entirely.
                # dist 23 frames hero + friend + brain together.
                lambda a, b: medium(a, b, [0, 0, 1.0], dist=23),
                lambda a, b: close_up(a, b, [4.5, 0, 1.5]),
                lambda a, b: close_up(a, b, [-4.5, 0, 1.5]),
            ]),
            "characters": {
                "hero": [kf(S_BRAIN, [-4.5, 0, 1.5], 0.5, "idle", "shocked"),
                         kf(B["b7"], [-4.5, 0, 1.5], 0.5, "idle", "smile"),
                         kf(B["b9"], [-4.5, 0, 1.5], 0.5, "idle", "laugh"),
                         kf(S_SLEEP, [-4.5, 0, 1.5], 0.5, "idle", "laugh")],
                "friend": [kf(S_BRAIN, [4.5, 0, 1.5], -0.5, "point", "smile"),
                           kf(B["b8"], [4.5, 0, 1.5], -0.5, "point", "smile"),
                           kf(B["b8"] + 20, [4.5, 0, 1.5], 0, "idle", "smile"),
                           kf(S_SLEEP, [4.5, 0, 1.5], 0, "idle", "smile")],
            },
        },
        {   # He finally sleeps: Tommy lies flat on the bed, the brain
            # floats above him washing itself clean through the shouts.
            # Wide first so the bed + the brain read together, then the
            # brain close-up for the WASH / IT / CLEAN climax.
            "id": "sleep", "location": "bedroom", "variant": "blue", "isNight": True,
            "startFrame": S_SLEEP, "endFrame": S_WAKE,
            "fx": _clock(S_SLEEP, S_WAKE) + _brain(S_SLEEP, S_WAKE, BRAIN_BED_P),
            "cameraShots": cover(S_SLEEP, S_WAKE, [
                # Static pulled-back wide, re-centred on x -1.35: the
                # shot must span the bed's left edge (x -9.2) AND the
                # BigClock's right edge (x 6.5) — a 15.7-stud span. The
                # old wide(a, b, [-3, 0, -1]) centred on x -3 cut the
                # clock's right ~40% off at the frame edge (the brain
                # move alone did not fix that). Camera z 26, no push:
                # a push would narrow the frame at the end and crop
                # the bed corner / clock again. No front wall in
                # RoomShell, so z 26 is safe; the spinning clock hands,
                # bobbing brain and breathing sleeper keep it alive.
                lambda a, b: static_shot(a, b, [-1.35, 7.4, 26], [-1.35, 4.8, -2], fov=58),
                lambda a, b: _brain_close(a, b, BRAIN_BED_P),
                # Frames the bed + the brain above the sleeper (brain
                # now at x -7); the old centre [-3.5, 0, -1.5] would
                # have cut the brain off at the left edge.
                lambda a, b: medium(a, b, [-5.5, 0, -2.5], dist=16),
            ]),
            "characters": {
                "hero": [kf(S_SLEEP, BED_P, 0, "sleep", "sleeping", rx=-math.pi / 2),
                         kf(S_WAKE, BED_P, 0, "sleep", "sleeping", rx=-math.pi / 2)],
            },
        },
        {   # Wake up sharp: daylight bedroom, Tommy celebrates — then
            # points at the clock for the twist: in bed by nine tonight.
            "id": "wake", "location": "bedroom", "variant": "blue",
            "startFrame": S_WAKE, "endFrame": END,
            "fx": _clock(S_WAKE, END),
            "cameraShots": cover(S_WAKE, END, [
                lambda a, b: medium(a, b, [-2, 0, 1.0]),
                lambda a, b: close_up(a, b, [-2, 0, 1.0]),
                lambda a, b: wide(a, b, [0, 0, 0]),
            ]),
            "characters": {
                "hero": [kf(S_WAKE, [-2, 0, 1.0], 0, "celebrate", "laugh"),
                         kf(B["b12"], [-2, 0, 1.0], 0, "idle", "smile"),
                         kf(B["b13"], [-2, 0, 1.0], 0.6, "point", "smile"),
                         kf(END, [-2, 0, 1.0], 0.6, "point", "smile")],
            },
        },
    ]
