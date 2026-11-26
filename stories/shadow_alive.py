"""SHADOW ALIVE — "What if your shadow came to life?"

Visual comedy, lead: little_brother "Tim" (never a story lead before).
One morning his shadow wakes up before he does. It copies everything
he does, then starts doing its own thing, and Tim has to catch it.

The shadow is a second R6 character in all-dark colors (dark skin, black
clothes, same scale as Tim). There is no shadow model, so the double
mirrors Tim's ANIM at the same frames from a few studs away — the copy
reads in the movement, not the position (the spacing check forbids two
actors sharing a spot). When it breaks away, it uses a different anim
while Tim holds still. One bubble line each, at the end.

Build (fake timings — Kokoro is not installed on this VM):
    python3 /tmp/build_stories.py shadow_alive

FIX 2026-11-23: opens with the title question "What if
your shadow came to life?" as b0 (channel rule), then the "In this town,"
setup follows; new science beat b13 states the real takeaway — a shadow
is light blocked by your body, and light travels in straight lines, so
the shadow copies your shape exactly (old b13 renumbered b14). FRAMING
FIX: every two-actor medium (actors 5 studs apart, ~8.4 span with arms
out) is wider than a portrait medium frame — the old preview sheets
show Tim cut in half at the left edge in the bedroom mediums and the
same cut in the breakaway/hand/sunset mediums and the chase medium
during the sprint-in. All of them are wides now (dist 20, fov 58);
single-actor close-ups / low-angles are unchanged (they centre on
their target). CHASE FIX (preview 2026-11-23): the chase wides did not
read — both runners converged to x=0, so the shadow hid directly behind
Tim for the whole second wide, Tim's head sat behind the playground
tree canopy, and at the first frame both were half out of frame at
opposite edges; the low-angle parked on HERO_P while Tim stood at x=0,
cutting his head off at the top-right corner. Runners now end 4.5 apart
in x (hero -2, shadow +2.5, clear of the tree trunk), chase wides are
dist 22 centred z=-1.5, and the low-angle aims at Tim's real spot.

FIX2 2026-11-23 (independent review FAIL, 3 defects — v2):
(1) STREET: the shadow walked directly behind Tim (same x, 4 studs back),
fully occluded f451-550. The shadow's path is now +2 studs in x (hero x+2)
so it walks visibly BESIDE Tim, not behind him.
(2) BEDROOM: Mom was cropped at the right edge in the wides and her face
sliced in half in the shadow low-angle f299-375. Mom moved to [4.6, 0, -4.6]
(1.1 studs left, 0.6 back — 4.17 from the shadow, min 4.05) and the bedroom
wides re-centred to x=1.0, so she is whole in every bedroom shot.
(3) BREAKAWAY: "Tim sat down" was never staged (Tim stood through f707-924).
New 'sit' anim (R6Character procedural branch: hips low, legs straight out
front) — Tim turns to face his dancing shadow f740-748 and sits at f748,
holding the sit to the chase cut. FIX3 2026-11-23 (independent review FAIL on v2, close-up only):
the bedroom low-angle f298-375 still sliced Mom's BODY at the right edge
(face whole, but red-shirt arm/shoulder, jeans and shoe run off-frame).
The low-angle now aims +0.5 studs toward Mom and pulls back (dist 9 -> 11.5,
fov 50 -> 54) so her full body fits with margin. No narration change.
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, orbit, shot, split_shots, wide  # noqa: F401

TITLE = "MY SHADOW STOPPED COPYING ME"  # YouTube title (the maintainer, 2026-11-23); narration still opens "What if your shadow came to life?"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b0", "text": "What if your shadow came to life?", "pause": 0.10},
    {"id": "b1", "text": "In this town, one morning, a kid's shadow woke up before he did.", "pause": 0.08},
    {"id": "b2", "text": "Tim stretched, and his shadow stretched. Tim waved, and it waved.", "pause": 0.08},
    {"id": "b3", "text": "At first it was funny. His shadow was the best copycat in town.", "pause": 0.08},
    {"id": "b4", "text": "But at breakfast, his shadow ate nothing, and still asked for seconds.", "pause": 0.08},
    {"id": "b5", "text": "On the street, Tim walked, and his shadow walked right beside him.", "pause": 0.08},
    {"id": "b6", "text": "Then, in the playground, his shadow stopped copying. And started dancing.", "pause": 0.10},
    {"id": "b7", "text": "Tim walked left. His shadow danced right. Tim sat down. It jumped.", "pause": 0.08},
    {"id": "b8", "text": "Tim chased his shadow around the slide, but a shadow is very fast.", "pause": 0.08},
    {"id": "b9", "text": "He was tired, and cross, and a little bit scared of his own shadow.", "pause": 0.10},
    {"id": "b10", "text": "Then his shadow stopped, turned around, and held out its hand.", "pause": 0.12},
    {"id": "w1", "text": "PLAY!", "voice": "am_adam", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "WITH!", "voice": "am_adam", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "ME!", "voice": "am_adam", "shout": True, "pause": 0.18},
    {"id": "b11", "text": "It was not trying to escape. It was trying to play. It was lonely too.", "pause": 0.08},
    {"id": "b12", "text": "So Tim took its hand, and they danced together until the sun went down.", "pause": 0.08},
    {"id": "b13", "text": "A shadow is not alive at all. It is just the light your body blocks. Light travels in straight lines, so your shadow copies your shape exactly.", "pause": 0.08},
    {"id": "b14", "text": "And now, every morning, Tim's shadow wakes up first. And waits for him.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05,
         "dropouts": [("b10+0.3", "w3.end")]}
SFX = [
    ("b1", "whoosh"),
    ("b2+0.5", "pop", {"f": 700}),
    ("b3+0.4", "pop", {"f": 800}),
    ("b4+0.5", "pop_down"),
    ("b5", "whoosh"),
    ("b6+0.4", "sparkle"),
    ("b7+0.6", "pop", {"f": 900}),
    ("b8", "whoosh"),
    ("b9+0.4", "sad"),
    ("b10+0.5", "bell_low"),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b11+0.5", "sparkle"),
    ("b12+0.6", "laugh"),
    ("b14+1.2", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
CAST = {
    "hero": {"extends": "little_brother", "hair": {"style": "curly", "color": "brown"},
             "top": {"style": "tshirt", "color": "yellow", "secondary": "white"},
             "bottom": {"style": "shorts", "color": "blue"},
             "shoes": {"color": "white", "sole": "white"}, "scale": 0.8},
    # The shadow: the same small kid, all dark. Same scale (0.8) so the
    # copy reads as a true double. It mirrors Tim's anim, never his spot.
    "shadow": {"extends": "little_brother", "skin": "deep",
               "hair": {"style": "curly", "color": "black"},
               "top": {"style": "tshirt", "color": "black", "secondary": "black"},
               "bottom": {"style": "shorts", "color": "black"},
               "shoes": {"color": "black", "sole": "black"}, "scale": 0.8},
    "mom": {"extends": "real_mom", "hair": {"style": "bun", "color": "black"}},
}


# 4. SCENES --------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END
    S_BED = B["b2"] - 1     # bedroom: the shadow wakes first
    S_STR = B["b5"] - 1     # street: the copycat walk
    S_PLY = B["b6"] - 1     # playground: the shadow breaks away
    S_CHASE = B["b8"] - 1   # playground: the chase
    S_HAND = B["b10"] - 1   # playground: the hand, PLAY WITH ME
    S_END = B["b14"] - 1    # street at sunset: waiting for him

    # Hero and shadow stay 5+ studs apart at all times (scale-adjusted need
    # is 3.6, but 5 keeps them readable as two separate figures).
    HERO_P, SHADOW_P = [-2.5, 0, 1.0], [2.5, 0, -1.0]
    return [
        {   # Hook: aerial town, three angles.
            "id": "hook", "location": "town_overview", "startFrame": 0, "endFrame": S_BED,
            "cameraShots": [
                shot(0, S_BED // 3, [-10, 62, 74], [-7, 56, 67], [8, 0, -6], [7, 1, -7], 55),
                shot(S_BED // 3, 2 * S_BED // 3, [-7, 56, 67], [-4, 50, 61], [7, 1, -7], [6, 2, -8], 55),
                shot(2 * S_BED // 3, S_BED, [-4, 50, 61], [-2, 46, 56], [6, 2, -8], [6, 2, -8], 55),
            ],
            "characters": {},
        },
        {   # Bedroom: Tim wakes, the shadow is already up, copying him.
            "id": "bedroom", "location": "bedroom", "variant": "green",
            "startFrame": S_BED, "endFrame": S_STR,
            "cameraShots": cover(S_BED, S_STR, [
                # FIX2: wides re-centred to x=1.0 (was 0) so Mom (now at
                # [4.5, 0, -4.5]) is whole at the right edge, not cropped.
                lambda a, b: wide(a, b, [1.0, 0, -1.0]),
                lambda a, b: close_up(a, b, HERO_P, scale=0.8),
                # FIX3: v2 still sliced Mom's BODY at the right edge here
                # (face whole, arm/shoulder/jeans/shoe cut). Aim +0.5 studs
                # toward Mom and pull back (dist 9 -> 11.5, fov 50 -> 54)
                # so her full body fits with margin.
                lambda a, b: low_angle(a, b, [3.0, 0, -1.0], scale=0.8, dist=11.5, fov=54),
            ]),
            "characters": {
                # The shadow copies Tim's anim at the same frames, from its
                # own spot across the room.
                "hero": [kf(S_BED, HERO_P, 0.4, "idle", "smile"),
                         kf(B["b2"], HERO_P, 0.4, "wave", "laugh"),
                         kf(S_STR, HERO_P, 0.4, "wave", "laugh")],
                "shadow": [kf(S_BED, SHADOW_P, -0.4, "idle", "smile"),
                           kf(B["b2"], SHADOW_P, -0.4, "wave", "laugh"),
                           kf(S_STR, SHADOW_P, -0.4, "wave", "laugh")],
                # FIX2: Mom moved 1.1 studs left / 0.6 back (was [5.5, 0, -4.0]):
                # her face was sliced in half in the shadow low-angle and her
                # body cropped in the wides. 4.17 studs from the shadow (min 4.05).
                "mom": hold(S_BED, S_STR, [4.6, 0, -4.6], -0.4, "idle", "smile"),
            },
        },
        {   # Street: the copycat walk, side by side (5 apart).
            "id": "street", "location": "street",
            "startFrame": S_STR, "endFrame": S_PLY,
            "cameraShots": cover(S_STR, S_PLY, [
                lambda a, b: wide(a, b),
                lambda a, b: wide(a, b),
                lambda a, b: close_up(a, b, HERO_P, scale=0.8),
            ]),
            "characters": {
                # FIX2: the shadow walks 2 studs to Tim's side (hero x + 2),
                # not directly behind him (same x, 4 back) — in v1 it was
                # fully occluded f451-550, only afro tufts showing.
                "hero": [kf(S_STR, [-6.0, 0, 0.5], HALF, "walk", "smile"),
                         kf(B["b5"] + 30, [0, 0, 0.5], HALF, "walk", "smile"),
                         kf(S_PLY, [0, 0, 0.5], 0.4, "idle", "smile")],
                "shadow": [kf(S_STR, [-4.0, 0, -3.5], HALF, "walk", "smile"),
                           kf(B["b5"] + 30, [2.0, 0, -3.5], HALF, "walk", "smile"),
                           kf(S_PLY, [2.0, 0, -3.5], 0.4, "idle", "smile")],
            },
        },
        {   # Playground: the shadow stops copying and starts dancing.
            "id": "breakaway", "location": "playground",
            "startFrame": S_PLY, "endFrame": S_CHASE,
            "cameraShots": cover(S_PLY, S_CHASE, [
                lambda a, b: wide(a, b),
                lambda a, b: close_up(a, b, SHADOW_P, scale=0.8),
                lambda a, b: wide(a, b),
                lambda a, b: close_up(a, b, HERO_P, scale=0.8, shake=0.06),
            ]),
            "characters": {
                # FIX2: "Tim sat down" is now staged — Tim turns to face his
                # dancing shadow f740-748 (rotation lerps) and sits at f748
                # ('sit' anim: hips low, legs straight out front), holding
                # the sit to the chase cut. No narration change.
                "hero": [kf(S_PLY, HERO_P, 0.4, "idle", "smile"),
                         kf(B["b7"], HERO_P, 0.4, "idle", "shocked"),
                         kf(740, HERO_P, 0.4, "idle", "shocked"),
                         kf(748, HERO_P, HALF, "sit", "shocked"),
                         kf(S_CHASE, HERO_P, HALF, "sit", "shocked")],
                # The shadow breaks away: Tim holds still, it dances.
                "shadow": [kf(S_PLY, SHADOW_P, -0.4, "idle", "smile"),
                           kf(B["b6"], SHADOW_P, -0.4, "dance", "laugh"),
                           kf(B["b7"], SHADOW_P, -0.4, "jump", "laugh"),
                           kf(S_CHASE, SHADOW_P, -0.4, "dance", "laugh")],
            },
        },
        {   # The chase around the slide.
            "id": "chase", "location": "playground",
            "startFrame": S_CHASE, "endFrame": S_HAND,
            "cameraShots": cover(S_CHASE, S_HAND, [
                lambda a, b: wide(a, b, [0, 0, -1.5], dist=22.0),
                lambda a, b: wide(a, b, [0, 0, -1.5], dist=22.0),
                lambda a, b: low_angle(a, b, [-2.0, 0, 0.5], scale=0.8),
            ]),
            "characters": {
                # Runners end separated (hero -2, shadow +3.5): from the
                # front camera they never stack, and Tim stays left of the
                # playground tree that used to hide his head.
                # ROUND 2 (preview 2026-11-23): the shadow still hid behind
                # the tree trunk — its end (2.5, -3.5) sits on the trunk's
                # sightline, and +4.5 would put it in the swing set. So the
                # shadow ends at (3.5, -1.0): in FRONT of the trunk, left of
                # the swing, 5.7 studs from Tim. Re-check with fresh stills.
                "hero": [kf(S_CHASE, [-6.0, 0, 0.5], HALF, "sprint", "panic"),
                         kf(B["b8"] + 30, [-2.0, 0, 0.5], HALF, "sprint", "panic"),
                         kf(S_HAND, [-2.0, 0, 0.5], 0.4, "idle", "panic")],
                "shadow": [kf(S_CHASE, [6.0, 0, -3.5], -HALF, "sprint", "laugh"),
                           kf(B["b8"] + 30, [3.5, 0, -1.0], -HALF, "sprint", "laugh"),
                           kf(S_HAND, [3.5, 0, -1.0], 0.4, "idle", "laugh")],
            },
        },
        {   # The hand: PLAY WITH ME. Tim takes it, and they dance together.
            "id": "hand", "location": "playground",
            "startFrame": S_HAND, "endFrame": S_END,
            "cameraShots": cover(S_HAND, S_END, [
                lambda a, b: wide(a, b),
                lambda a, b: close_up(a, b, SHADOW_P, scale=0.8),
                lambda a, b: close_up(a, b, HERO_P, scale=0.8),
                lambda a, b: wide(a, b),
            ]),
            "characters": {
                "hero": [kf(S_HAND, HERO_P, 0.4, "idle", "panic"),
                         kf(B["b11"], HERO_P, 0.4, "idle", "smile"),
                         kf(B["b12"], HERO_P, 0.4, "dance", "laugh"),
                         kf(S_END, HERO_P, 0.4, "dance", "laugh")],
                "shadow": [kf(S_HAND, SHADOW_P, -0.4, "idle", "smile"),
                           kf(B["w1"], SHADOW_P, -0.4, "wave", "laugh",
                              bubble="Play with me!"),
                           kf(B["b12"], SHADOW_P, -0.4, "dance", "laugh"),
                           kf(S_END, SHADOW_P, -0.4, "dance", "laugh")],
            },
        },
        {   # Sunset: the shadow wakes first now, and waits for him.
            "id": "sunset", "location": "street",
            "startFrame": S_END, "endFrame": END,
            "cameraShots": cover(S_END, END, [
                lambda a, b: wide(a, b, [0, 0, 0.5]),
                lambda a, b: close_up(a, b, HERO_P, scale=0.8),
            ]),
            "characters": {
                "hero": hold(S_END, END, HERO_P, 0.4, "idle", "smile"),
                "shadow": hold(S_END, END, SHADOW_P, -0.4, "idle", "smile"),
            },
        },
    ]
