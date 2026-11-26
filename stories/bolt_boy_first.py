"""BOLT BOY'S FIRST SHORT - "NOBODY IS ALLOWED TO RUN"

Bolt Boy (kit `BoltBoy.tsx`, cast as `{"kit": "boltboy"}`) as hero in his first story Short.
Rule: running is banned in this town, so the race is won by walking -
it plays to his best feature, the steady walk, and his grin fits
every beat (no sad/angry face needed until the twist).

DO NOT RUN YET (2026-11-20): `src/story/currentStory.ts` is currently
the sky_blue story. Running `make_short.py --stills` overwrites
currentStory.ts. Only run this after sky_blue has shipped, and back
up currentStory.ts first (or re-run sky_blue's story file after).
(Sky blue has shipped; staging copy backed up 2026-11-23.)

CHANNEL RULE (2026-11-22): the script opens with the big "What if...?"
question (beat b0) and the takeaway is "slow and steady wins the race" -
walking, done right, beats running that breaks the rules.

Build:   python scripts/make_short.py stories/bolt_boy_first.py --stills
Render:  python scripts/make_short.py stories/bolt_boy_first.py --skip-tts --render

NOTE ON THE HERO (WIRED IN 2026-11-21): the hero is the canonical kit
BoltBoy (`src/components/BoltBoy.tsx`) — curved smile + tongue, extruded
3D bolt, two-tone sneakers — rendered by MotionBlocksComposition via the
cast marker `{"kit": "boltboy"}`. The story's `anim` is mapped to a kit
clip (walk/idle/wave). The R6 preset `bolt_boy` (look.ts) is no longer
used for this hero. Stills first, as always — check the kit hero at
full size before any full render.
"""
from shorts.scene import HALF, OFF, close_up, cover, hold, kf, medium, shot, wide  # noqa: F401

TITLE = "NOBODY IS ALLOWED TO RUN"

# 1. SCRIPT ------------------------------------------------------------------
# Narrator = af_heart (reference-matched). `shout: True` lines are single words, boosted, own caption.
BEATS = [
    {"id": "b0", "text": "What if you were never allowed to run?", "pause": 0.08},
    {"id": "b1", "text": "In this town, running is banned. Everyone has to walk everywhere.", "pause": 0.08},
    {"id": "b2", "text": "Buses crawl, bikes gather dust, and the school bell means a slow walk, not a sprint.", "pause": 0.08},
    {"id": "b3", "text": "Bolt Boy never minded. Walking is his superpower, steady feet and a steady grin.", "pause": 0.08},
    {"id": "b4", "text": "But the bully runs everywhere, and nobody ever stops him.", "pause": 0.10},
    {"id": "b5", "text": "One morning, the principal announced the Great Town Race.", "pause": 0.07},
    {"id": "b6", "text": "First prize: a golden sneaker, and a whole day with no homework.", "pause": 0.08},
    {"id": "b7", "text": "Everyone lined up, lacing shoes and stretching legs, ready to run.", "pause": 0.07},
    {"id": "b8", "text": "But the rule book said it plain: run, and you are out.", "pause": 0.09},
    {"id": "b9", "text": "The whistle blew, and the bully shot off like a rocket.", "pause": 0.07},
    {"id": "b10", "text": "Then the principal opened the oldest rule book in town, and read the last page.", "pause": 0.14},
    {"id": "w1", "text": "WALK!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "WINS!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "FIRST!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b11", "text": "Bolt Boy walked every step, steady as a clock, and crossed the line first.", "pause": 0.07},
    {"id": "b12", "text": "The bully had to walk all the way back, in his squeaky shoes.", "pause": 0.12},
    {"id": "b13", "text": "But last night, Bolt Boy laced up his shoes... and started to run.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/fallen-down.mp3",
    "under_voice": 0.022,          # music loudness while the narrator talks
    "gaps": 0.05,                  # loudness in pauses
    "dropouts": [("b10+0.3", "w3.end")],   # silence before the reveal, music returns after FIRST!
}

SFX = [
    ("b1", "whoosh"),
    ("b1+0.5", "sparkle"),
    ("b2+0.15", "pop", {"f": 600}),
    ("b2+1.25", "pop", {"f": 720}),
    ("b3+0.4", "sparkle"),
    ("b4+0.3", "bell_low"),
    ("b5", "ding_dong"),
    ("b6+0.5", "sparkle"),
    ("b7+0.8", "pop", {"f": 860}),
    ("b8+0.6", "thud"),
    ("b9", "whoosh"),
    ("b9+0.8", "riser", {"dur": 1.6}),
    ("b10", "riser", {"dur": 2.1}),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b11+0.6", "pop", {"f": 700}),
    ("b12+0.8", "sad"),
    ("b13+2.0", "twist"),
]

# 3. CAST (character constructor, src/characters/look.ts) ----------------------
# hero is the canonical kit BoltBoy (see header note) — cast as {"kit": "boltboy"}.
CAST = {
    "hero": {"kit": "boltboy"},
    "friend": {"extends": "kid_girl", "hair": {"style": "ponytail", "color": "blonde"},
               "top": {"style": "hoodie", "color": "pink", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"},
               "shoes": {"color": "white", "sole": "white"}},
    "bully": "bully",
    "principal": "principal",
    "mom": {"extends": "real_mom", "hair": {"style": "ponytail", "color": "brown"}},
}


# 4. SCENES (frames come from the narration timings: T.B[id] = start, T.E[id] = end, T.END) --
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S_B = B["b2"] - 1     # street: slow town + Bolt Boy walks
    S_C = B["b4"] - 1     # school exterior: bully sprints past, race announced
    S_D = B["b6"] - 1     # crossroads: lineup, rule, whistle, bully sprints off
    S_E = B["b10"] - 1    # classroom: rule book, WALK WINS FIRST
    S_F = B["b11"] - 1    # yellow house: Bolt Boy wins, bully walks back
    S_G = B["b13"] - 1    # living room, night: the twist

    HERO_P = [-4.5, 0, 0.5]
    FRIEND_P = [0.5, 0, 0.5]

    scenes = []

    # A. TOWN OVERVIEW - hook (split in two so neither shot exceeds 3.5 s:
    # b0 asks the question, b1 sets up the town) -----------------------------
    scenes.append({
        "id": "scene-hook",
        "location": "town_overview",
        "startFrame": 0,
        "endFrame": S_B,
        "cameraShots": [shot(0, B["b1"], [-10, 62, 74], [-2, 46, 56], [8, 0, -6], [6, 2, -8], 55),
                        shot(B["b1"], S_B, [-2, 46, 56], [2, 40, 50], [6, 2, -8], [4, 3, -6], 55)],
        "characters": {},
    })

    # B. STREET - the slow town, Bolt Boy walks --------------------------------
    # FIX1 (2026-11-23): the street medium (f220-286) caught Bolt Boy mid-walk
    # at x≈-6, exactly over the street hydrant (local [-6,0,0.8]) — the red
    # hydrant read as a red leg between his black legs f225-246, white shoe
    # shapes on its base. He now finishes the walk BEFORE the medium starts
    # (arrives -4.5 at MED_START=220, the first medium frame) and idles
    # through it, so the hydrant sits ~1.5 studs to his left as a separate
    # prop. The hydrant pass now happens only in the wide (f154-220), at
    # small scale. (Moving the hydrant in TownMap was rejected: it is shared
    # by every story that uses the street.)
    MED_START = S_B + (S_C - S_B) // 4   # first frame of the street medium (220)
    scenes.append({
        "id": "scene-street",
        "location": "street",
        "startFrame": S_B,
        "endFrame": S_C,
        "cameraShots": cover(S_B, S_C, [
            lambda a, b: wide(a, b),
            lambda a, b: medium(a, b, HERO_P),
            lambda a, b: close_up(a, b, HERO_P),
        ]),
        "characters": {
            "hero": [kf(S_B, [-8.0, 0, 0.5], 0.3, "walk", "grin"),
                     kf(MED_START, [-4.5, 0, 0.5], 0.3, "walk", "grin"),
                     kf(MED_START + 6, [-4.5, 0, 0.5], 0, "idle", "grin"),
                     kf(S_C, [-4.5, 0, 0.5], 0, "wave", "grin")],
            "friend": hold(S_B, S_C, FRIEND_P, -0.3, "wave", "smile"),
        },
    })

    # C. SCHOOL EXTERIOR - bully sprints past, principal announces the race ----
    scenes.append({
        "id": "scene-school",
        "location": "school_exterior",
        "schoolName": "WALKERS SCHOOL",
        "startFrame": S_C,
        "endFrame": S_D,
        "cameraShots": cover(S_C, S_D, [
            lambda a, b: wide(a, b),
            # CLOSE-UP on the PRINCIPAL (he announces the race at b5) — a
            # medium on him left the friend as a giant pink foreground block
            # (f545); the close-up puts the friend behind the camera.
            # side=-3.0 (camera to his right): side=+3 swung the camera
            # TOWARD the friend at [0,0,0] and her head filled the frame.
            # A straight-on close-up put a white canopy column directly
            # behind his head (pillar-from-head); the side angle moves the
            # column off to his left. dist=11: pulls back enough to show his
            # pointing arm; dist=7 cropped his hair and his arm, dist=9
            # still cropped the arm at the frame edge.
            # FIX1 (2026-11-23): side=-3.0 did NOT move the column far
            # enough — f545 still had it dead behind his head. side=-5.0
            # cleared the column but swung the bully into a big left-
            # foreground block (~25% of the frame). v2b: principal +1.0 in
            # x ([-1.25,0,-4.5], 4.67 studs from the friend, rule OK) plus
            # side=-4.0 — together they shift the head ~200px off the
            # column while keeping the v1 framing (bully back to an edge
            # sliver). Verify on the f545 preview still before the box render.
            lambda a, b: close_up(a, b, [-1.25, 0, -4.5], dist=11, side=-4.0),
            lambda a, b: close_up(a, b, [4.5, 0, 4.8]),
        ]),
        "characters": {
            "bully": [kf(S_C, [-11, 0, -1], HALF, "sprint", "laugh"),
                      kf(B["b5"], [-6, 0, -1], HALF, "sprint", "laugh"),
                      kf(B["b5"] + 6, [-6, 0, -1], 0.9, "idle", "cool"),
                      kf(S_D, [-6, 0, -1], 0.9, "idle", "cool")],
            "friend": hold(S_C, S_D, [0, 0, 0], 0, "idle", "smile"),
            # FIX1 (2026-11-23): principal +1.0 in x (was -2.25) — shifts
            # his head off the canopy column in the close-up; see the CU
            # comment above. (Race scene keeps -2.25; the cut hides it.)
            # He stays at -2.25 through the wide (fully visible left of the
            # friend) and steps to -1.25 on the cut frame 503, when the CU
            # takes over — a 1-frame move hidden by the camera cut.
            "principal": [kf(S_C, [-2.25, 0, -4.5], 0, "idle", "deadpan", "clipboard"),
                          kf(502, [-2.25, 0, -4.5], 0, "idle", "deadpan", "clipboard"),
                          kf(503, [-1.25, 0, -4.5], 0, "idle", "deadpan", "clipboard"),
                          kf(B["b5"], [-1.25, 0, -4.5], 0, "point", "deadpan", "clipboard"),
                          kf(S_D, [-1.25, 0, -4.5], 0, "point", "deadpan", "clipboard")],
            # hero pulled in from x=4.5: at 4.5 he was half-cut at the right
            # edge of the wide (f460).
            # FIX1 (2026-11-23): at 3.5 his right headphone / hair spikes /
            # arm still cropped out f458-488 (face whole). x=2.0 keeps him
            # whole in the wide; 5.2 studs from the friend, rule OK.
            "hero": [kf(S_C, [2.0, 0, 4.8], 0, "idle", "grin"),
                     kf(B["b5"], [2.0, 0, 4.8], 0, "wave", "grin"),
                     kf(S_D, [2.0, 0, 4.8], 0, "wave", "grin")],
        },
    })

    # D. CROSSROADS - lineup, the rule, the whistle, the bully sprints off -----
    scenes.append({
        "id": "scene-race",
        "location": "crossroads",
        "startFrame": S_D,
        "endFrame": S_E,
        "cameraShots": cover(S_D, S_E, [
            lambda a, b: wide(a, b),
            lambda a, b: medium(a, b, [0, 0, 0.5]),
            lambda a, b: close_up(a, b, HERO_P),
        ]),
        "characters": {
            "hero": [kf(S_D, HERO_P, 0.2, "idle", "grin"),
                     kf(B["b9"], HERO_P, 0.2, "walk", "grin"),
                     kf(B["b9"] + 48, [-1.0, 0, 0.5], 0.2, "walk", "grin"),
                     kf(B["b9"] + 54, [-1.0, 0, 0.5], 0, "idle", "grin"),
                     kf(S_E, [-1.0, 0, 0.5], 0, "idle", "grin")],
            "bully": [kf(S_D, [4.5, 0, 0.5], -0.2, "idle", "cool"),
                      kf(B["b9"], [4.5, 0, 0.5], -0.2, "sprint", "laugh"),
                      kf(B["b9"] + 40, [11, 0, 0.5], -0.2, "sprint", "laugh"),
                      kf(S_E, [11, 0, 0.5], -0.2, "idle", "laugh")],
            "principal": [kf(S_D, [-2.25, 0, -4.5], 0, "point", "deadpan", "clipboard"),
                          kf(B["b8"], [-2.25, 0, -4.5], 0, "idle", "deadpan", "clipboard"),
                          kf(S_E, [-2.25, 0, -4.5], 0, "idle", "deadpan", "clipboard")],
        },
    })

    # E. CLASSROOM - the rule book, WALK WINS FIRST -----------------------------
    board = ["TOWN RULES", "NO RUNNING", "WALK, DON'T RUN"]
    scenes.append({
        "id": "scene-rulebook",
        "location": "classroom",
        "boardText": board,
        "startFrame": S_E,
        "endFrame": S_F,
        "cameraShots": cover(S_E, S_F, [
            lambda a, b: medium(a, b, [0, 0, 2.5]),
            lambda a, b: close_up(a, b, [1.0, 0, 2.5]),
            lambda a, b: wide(a, b),
        ]),
        "characters": {
            "hero": [kf(S_E, [1.0, 0, 2.5], 0, "idle", "grin"),
                     kf(B["w1"], [1.0, 0, 2.5], -0.4, "point", "shocked"),
                     kf(B["w3"], [1.0, 0, 2.5], 0, "celebrate", "laugh"),
                     kf(S_F, [1.0, 0, 2.5], 0, "celebrate", "laugh")],
            "friend": [kf(S_E, [-5.5, 0, 3], 0.6, "idle", "smile"),
                       kf(B["w1"], [-5.5, 0, 3], 0.6, "idle", "shocked"),
                       kf(S_F, [-5.5, 0, 3], 0.6, "idle", "shocked")],
            "bully": [kf(S_E, [5.5, 0, 3], -0.6, "idle", "cool"),
                      kf(B["w1"], [5.5, 0, 3], -0.6, "idle", "panic"),
                      kf(S_F, [5.5, 0, 3], -0.6, "idle", "panic")],
            "principal": [kf(S_E, [-2.0, 0, -1.5], 0, "idle", "deadpan", "clipboard"),
                          kf(B["b10"], [-2.0, 0, -1.5], 0, "point", "deadpan", "clipboard"),
                          kf(S_F, [-2.0, 0, -1.5], 0, "point", "deadpan", "clipboard")],
        },
    })

    # F. YELLOW HOUSE - Bolt Boy wins, the bully walks back ----------------------
    # HERO STANDS ON THE WALKWAY (z=1.0), NOT on the porch: at z=-2.6 the
    # white door-header trim (y 5.35, front face z=-1.7, in front of his face
    # plane) crossed his eyes in both the wide (f1194) and medium (f1263).
    # In front of the porch the header sits behind his head, clear of his face.
    scenes.append({
        "id": "scene-win",
        "location": "house",
        "variant": "yellow",
        "startFrame": S_F,
        "endFrame": S_G,
        "cameraShots": cover(S_F, S_G, [
            lambda a, b: wide(a, b),
            lambda a, b: medium(a, b, [0, 0, 1.0]),
        ]),
        "characters": {
            "hero": hold(S_F, S_G, [0, 0, 1.0], 0, "celebrate", "grin"),
            "bully": [kf(S_F, [-6.5, 0, 2.6], HALF, "walk", "deadpan"),
                      # turnaround at -4.5 (was -3.0): keeps 4.5+ studs from
                      # the hero now standing at [0,0,1.0].
                      kf(B["b12"], [-4.5, 0, 2.6], HALF, "walk", "deadpan"),
                      kf(B["b12"] + 22, [-4.5, 0, 2.6], -HALF, "walk", "deadpan"),
                      kf(B["b12"] + 48, [-6.5, 0, 2.6], -HALF, "walk", "deadpan"),
                      kf(S_G, [-6.5, 0, 2.6], 0.4, "idle", "deadpan")],
            "mom": [kf(S_F, [4.5, 0, -3.6], -0.4, "idle", "smile"),
                    kf(B["b12"], [4.5, 0, -3.6], -0.4, "wave", "smile"),
                    kf(S_G, [4.5, 0, -3.6], -0.4, "celebrate", "laugh")],
        },
    })

    # G. LIVING ROOM, NIGHT - the twist ------------------------------------------
    scenes.append({
        "id": "scene-twist",
        "location": "living_room",
        "variant": "yellow",
        "isNight": True,
        "startFrame": S_G,
        "endFrame": END,
        "cameraShots": cover(S_G, END, [
            lambda a, b: wide(a, b),
            lambda a, b: close_up(a, b, [-4.0, 0, 0.4]),
        ]),
        "characters": {
            "hero": [kf(S_G, [-4.0, 0, 0.4], 0.9, "idle", "grin"),
                     kf(B["b13"] + 58, [-4.0, 0, 0.4], 0.9, "idle", "shocked"),
                     kf(END, [-4.0, 0, 0.4], 0.9, "idle", "shocked")],
            "mom": [kf(S_G, [4.0, 0, 0.4], -0.9, "idle", "smile"),
                    kf(B["b13"] + 58, [4.0, 0, 0.4], -0.9, "idle", "panic"),
                    kf(END, [4.0, 0, 0.4], -0.9, "idle", "panic")],
        },
    })

    return scenes
