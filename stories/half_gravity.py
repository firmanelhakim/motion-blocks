"""HALF GRAVITY — "What If Gravity Was Half as Strong?"

Science explainer, lead: a kid_boy hero ("Max", messyFringe brown hair,
green hoodie — kept for the whole video). Max jumps to catch a ball and
does not come down: he floats up over the school roof while his friend
Mia watches from the ground. Fun at first — half the weight, double the
jump — until the teacher points up: the Moon is drifting away, and the
sky is getting thinner at the edges.

The ONE science idea: gravity holds down more than just you — it holds
the air and the Moon too. At half strength a 40 kg kid weighs 20 kg and
jumps about twice as high, but the Moon's orbit depends on Earth's
gravity balancing its speed, so it drifts away, and the atmosphere
slowly leaks into space.

No new assets. Reuses town (playground, street), space, and the Moon fx
(sphere + craters, moon_off.py / cheese_moon.py pattern). Floating is
staged with real y positions (gravity_off pattern): the hero's keyframes
take him from y 0 up to y 11 and back down, 'jump'/'fly' while airborne,
'idle' once landed. The Moon drifts up and away across the story — its
fx keyframes move it +y and further back (-z) in every town scene, and
a separate closer Moon fx in the space scene drifts back and shrinks.

Build (fake timings — Kokoro is not installed on this VM):
    python3 /tmp/build_stories.py half_gravity
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, orbit, shot, split_shots, static_shot, wide  # noqa: F401

TITLE = "WHAT IF GRAVITY WAS HALF AS STRONG"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    # Cold-open hook (the maintainer: every Short starts with the big "What if"
    # question): Max already floating high over the roof, looking at the
    # camera, before the "In this town" setup rewinds to the jump.
    {"id": "b0", "text": "What if gravity was half as strong?", "pause": 0.08},
    {"id": "b1", "text": "In this town, gravity is only half as strong.", "pause": 0.08},
    {"id": "b2", "text": "Max jumps to catch the ball — and he does not come down.", "pause": 0.08},
    {"id": "b3", "text": "He floats up, slow and high, right over the school roof.", "pause": 0.08},
    {"id": "b4", "text": "His friend Mia watches from the ground, her mouth wide open.", "pause": 0.08},
    {"id": "b5", "text": "At first he laughs. Everything feels light. He can jump twice as high.", "pause": 0.08},
    {"id": "b6", "text": "A forty kilo kid weighs only twenty now. Half the weight, double the jump.", "pause": 0.10},
    {"id": "b7", "text": "Then the teacher points up. The Moon is drifting away, a little further every minute.", "pause": 0.10},
    {"id": "b8", "text": "Gravity does not just hold you down. It holds the air, and it holds the Moon.", "pause": 0.10},
    {"id": "b9", "text": "Without a strong pull, the sky leaks away, thin at the edges, and the Moon slips its orbit.", "pause": 0.10},
    {"id": "b10", "text": "The Moon drifts further every minute, getting smaller and smaller in the sky.", "pause": 0.10},
    {"id": "w1", "text": "THE", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "MOON!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "LEAVING!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b11", "text": "Max drifts down, soft and slow, and lands on his feet. But the Moon keeps going.", "pause": 0.08},
    {"id": "b12", "text": "Fun to jump, yes. But gravity is what holds our air and our Moon in place.", "pause": 0.08},
    {"id": "b13", "text": "But last night, Max looked up — and the Moon looked a little smaller than yesterday.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05,
         "dropouts": [("b10+0.3", "w3.end")]}
SFX = [
    ("b0+0.2", "sparkle"),
    ("b1", "whoosh"),
    ("b2+0.3", "whoosh"),
    ("b3+0.5", "sparkle"),
    ("b4+0.5", "pop", {"f": 700}),
    ("b5+0.5", "laugh"),
    ("b6+0.5", "pop", {"f": 600}),
    ("b7+0.3", "bell_low"),
    ("b8+0.5", "sparkle"),
    ("b9+0.5", "whoosh"),
    ("b10+0.5", "riser", {"dur": 1.6}),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b11+0.5", "thud"),
    ("b12+0.5", "sparkle"),
    ("b13+1.5", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
CAST = {
    # Max: the hero, one look for the whole video — messyFringe brown hair,
    # green hoodie, jeans, white shoes.
    "hero": {"extends": "kid_boy", "hair": {"style": "messyFringe", "color": "brown"},
             "top": {"style": "hoodie", "color": "green", "secondary": "white"},
             "bottom": {"style": "jeans", "color": "denim"},
             "shoes": {"color": "white", "sole": "white"}},
    # Mia: his friend on the ground — pigtails, black hair, pink hoodie.
    "friend": {"extends": "kid_girl", "hair": {"style": "pigtails", "color": "black"},
               "top": {"style": "hoodie", "color": "pink", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"},
               "shoes": {"color": "white", "sole": "white"}},
    "teacher": "teacher",
}


# 4. SCENES --------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END
    S_JUMP = B["b2"] - 1    # playground: the jump, the float
    S_STREET = B["b6"] - 1  # street: the teacher points up
    S_SPACE = B["b9"] - 1   # space: the Moon drifting, big in frame
    S_SHOUT = B["w1"] - 1   # street: the shouts
    S_PAYOFF = B["b11"] - 1  # street: Max lands, the payoff
    S_TWIST = B["b13"] - 1  # street at night: the last line

    HERO_P = [-5, 0, 1.0]       # hero's ground spot (x, z); y varies while floating
    HERO_HIGH = [-5, 11, 1.0]   # hero floating over the roof
    # FIX1: Mia was half-hidden behind the traffic-light pole (stage
    # x 4.4, z -0.6 — the world (-7.6,-7.6) light, re-anchored for the
    # street location — which projects right onto her at x 5) and cut by
    # the right edge in the street wides and the shout tableau. FIX2:
    # x 4 still left the pole crossing her right side (her right edge at
    # x 6 vs the pole at 4.4), so she moves further left and back:
    # x 2, z -3.5 — her right edge (x 4) clears the pole by 0.4 studs,
    # and she sits >= 4.5 from the teacher (sqrt(2^2 + 4.5^2) = 4.92).
    FRIEND_P = [2, 0, -3.5]
    TEACHER_P = [0, 0, 1.0]
    # Spacing (2D x,z): hero (-5,1) / teacher (0,1) / friend (5,1) are 5.0 apart.

    # The Moon (town scenes): a pale sphere high in the sky with darker
    # craters riding on it (cheese_moon.py pattern). It drifts slowly up
    # and away — +y and further back (-z) — across the whole story, so by
    # the last line it sits higher and further than at the hook.
    # FIX ROUND 2: the Moon sat at the hook camera's right edge as a
    # cropped sliver (f40) — it now starts further east ([16,38,-13])
    # so the hook shot is clean, and drifts back to the old track by
    # S_STREET (the drift happens while it is out of frame in the
    # jump scene, so the shift is invisible).
    MOON_KF = [{"frame": 0, "position": [16, 38, -13]},
               {"frame": S_JUMP, "position": [15.5, 38.5, -13]},
               {"frame": S_STREET, "position": [12, 40, -13]},
               {"frame": S_SPACE, "position": [13, 41, -15]},
               {"frame": S_SHOUT, "position": [14, 42, -17]},
               {"frame": S_PAYOFF, "position": [14.5, 42.5, -18]},
               {"frame": S_TWIST, "position": [15, 43, -19]},
               {"frame": END, "position": [16, 44, -21]}]
    moon_fx = [{"id": "moon", "shape": "sphere", "radius": 5.0, "color": "#E8EDF3",
                "emissive": "#CBD5E1", "emissiveIntensity": 0.5, "roughness": 0.9,
                "keyframes": MOON_KF}]
    for i, (ox, oy, oz, r) in enumerate([
            (2.05, 1.37, 3.88, 1.1), (-1.68, 2.68, 3.35, 1.0), (3.58, -1.19, 2.63, 1.1),
            (0.23, 4.45, 1.17, 0.9), (-3.55, -0.71, 2.84, 1.1), (1.16, -3.03, 3.26, 1.0)]):
        moon_fx.append({"id": f"crater{i}", "shape": "sphere", "radius": r, "color": "#64748B",
                        "emissive": "#64748B", "emissiveIntensity": 0.25, "roughness": 0.9,
                        "keyframes": [{"frame": k["frame"],
                                      "position": [k["position"][0] + ox, k["position"][1] + oy, k["position"][2] + oz]}
                                     for k in MOON_KF]})

    # The Moon (space scene only): same pale sphere, but close to the camera
    # so it fills the frame, drifting up and back (smaller) across the scene.
    # A separate fx instance — the cut from the street hides the jump.
    # FIX ROUND 2: the v2 Moon barely moved (camera-to-Moon distance
    # ~20 the whole scene) so it never shrank — it now starts close
    # ([2,13,-16], ~36 studs out) and ends far ([8,18,-38], ~59 out),
    # shrinking ~30% across b10, with keyframes on the shot boundaries.
    # TEST-STILL CORRECTION (2026-11-23): ending at [6,17,-32] left the
    # Moon still ~2x the Earth in frame — the drift did not read. The
    # end is now [8,18,-38] (~59 out, ~19% of frame height), smaller
    # than the Earth at the end, so "the Moon drifts away" reads.
    SPACE_MOON_KF = [{"frame": S_SPACE, "position": [2, 13, -16]},
                     {"frame": S_SPACE + 83, "position": [4, 15, -24]},
                     {"frame": S_SPACE + 166, "position": [6, 17, -31]},
                     {"frame": S_SHOUT, "position": [8, 18, -38]}]
    # FIX ROUND 2: the Earth globe, in the space scene at last — v2 had
    # no Earth fx here at all (only the env's built-in Earth, out of
    # frame), so "the Moon drifts away" had nothing to drift away
    # FROM. Static at [-5, 9, -22], left of the Moon in all three
    # shots; the env's built-in Earth sits just outside the left edge.
    # TEST-STILL CORRECTION (2026-11-23): was [-7.5,9,-26] — too far
    # (only ~15% of frame height) and hard on the left edge (cropped
    # at f1000). Moved closer and in, so it reads ~24% and sits clear
    # of the edge, bigger than the Moon by the end of the drift.
    space_earth_fx = [{"id": "earth", "shape": "sphere", "radius": 3.0, "color": "#38BDF8",
                       "emissive": "#1D4ED8", "emissiveIntensity": 0.4, "roughness": 0.7,
                       "keyframes": [{"frame": S_SPACE, "position": [-5, 9, -22]},
                                     {"frame": S_SHOUT, "position": [-5, 9, -22]}]}]
    for i, (ox, oy, oz, r) in enumerate([
            (1.0, 0.7, 1.9, 1.2), (-1.2, 1.0, 1.7, 1.0), (0.2, -1.0, 2.1, 1.3),
            (-0.5, 1.7, 1.4, 0.9)]):
        space_earth_fx.append({"id": f"continent{i}", "shape": "sphere", "radius": r, "color": "#22C55E",
                               "emissive": "#16A34A", "emissiveIntensity": 0.25, "roughness": 0.8,
                               "keyframes": [{"frame": S_SPACE, "position": [-5 + ox, 9 + oy, -22 + oz]},
                                            {"frame": S_SHOUT, "position": [-5 + ox, 9 + oy, -22 + oz]}]})
    space_moon_fx = [{"id": "moon", "shape": "sphere", "radius": 5.0, "color": "#E8EDF3",
                      "emissive": "#CBD5E1", "emissiveIntensity": 0.5, "roughness": 0.9,
                      "keyframes": SPACE_MOON_KF}]
    for i, (ox, oy, oz, r) in enumerate([
            (2.05, 1.37, 3.88, 1.1), (-1.68, 2.68, 3.35, 1.0),
            (3.58, -1.19, 2.63, 1.1), (0.23, 4.45, 1.17, 0.9)]):
        space_moon_fx.append({"id": f"crater{i}", "shape": "sphere", "radius": r, "color": "#64748B",
                              "emissive": "#64748B", "emissiveIntensity": 0.25, "roughness": 0.9,
                              "keyframes": [{"frame": k["frame"],
                                            "position": [k["position"][0] + ox, k["position"][1] + oy, k["position"][2] + oz]}
                                           for k in SPACE_MOON_KF]})

    return [
        {   # Cold-open hook: Max already floating high over the roof, looking
            # straight at the camera, while the narration asks the big
            # "What if" question. FIX2: v1 of this shot sat the camera at
            # y 1.2, z 10 — half a stud from the pale-yellow picket fence
            # (z 9.5), which filled the top of the frame as a flat olive
            # band and hid his head. Pulled back and up to mirror the
            # proven rising shot (f250): he hangs whole against empty sky
            # and the caption sits on sky below his feet.
            "id": "hook-q", "location": "playground",
            "startFrame": 0, "endFrame": B["b1"] - 1,
            "fx": moon_fx,
            "cameraShots": [
                shot(0, B["b1"] - 1, [-5, 2.5, 13], [-5, 3, 12],
                     [-5, 10, 1.0], [-5, 12, 1.0], 55),
            ],
            "characters": {
                "hero": hold(0, B["b1"] - 1, HERO_HIGH, 0.0, "fly", "shocked"),
            },
        },
        {   # Setup: the town from above, one slow push-in (a single shot —
            # b1 is only ~2 s, so splitting it would risk a sub-1 s shot).
            "id": "hook", "location": "town_overview",
            "startFrame": B["b1"] - 1, "endFrame": S_JUMP,
            "fx": moon_fx,
            "cameraShots": [
                shot(B["b1"] - 1, S_JUMP, [-10, 62, 74], [-2, 46, 56], [8, 0, -6], [6, 2, -8], 55),
            ],
            "characters": {},
        },
        {   # Playground: Max jumps, rises, and hangs high over the roof
            # while Mia watches from the ground. Shots are beat-aligned so
            # the camera tracks his height: wide on the jump, a rising
            # manual shot as he climbs, a low_angle once he is high, then
            # a wide that holds both of them (him high, her on the ground)
            # for scale.
            "id": "jump", "location": "playground",
            "startFrame": S_JUMP, "endFrame": S_STREET,
            "fx": moon_fx,
            "cameraShots": [
                wide(S_JUMP, B["b3"], [0, 0, 1.0], 22),
                shot(B["b3"], B["b4"], [-5, 3, 13], [-5, 4, 12],
                     [-5, 8, 1.0], [-5, 13, 1.0], 55),
                # FIX ROUND 2: v2's b4 shot was a close-up on floating
                # Max alone — Mia was never in frame while the narration
                # is about her watching. A two-shot now: Max high above,
                # Mia waist-up at the bottom, clear of the Dare tree
                # (she stands at MIA_CLEAR, not under its canopy). The
                # target rides high (y 12) so the 68% caption band falls
                # on empty sky between them, not on her face.
                shot(B["b4"], B["b5"], [-3.5, 4, 21], [-3.5, 4, 20.5],
                     [-3.5, 12, 0], [-3.5, 12, 0], 58),
                shot(B["b5"], (B["b5"] + S_STREET) // 2, [0, 9, 21], [0, 8.8, 20.5],
                     [-1, 9, 1.0], [-1, 9, 1.0], 58),
                shot((B["b5"] + S_STREET) // 2, S_STREET, [0, 8.8, 20.5], [0, 8.5, 20],
                     [-1, 9, 1.0], [-1, 9, 1.0], 58),
            ],
            "characters": {
                "hero": [kf(S_JUMP, HERO_P, 0.3, "jump", "smile"),
                         kf(B["b3"], [-5, 6, 1.0], 0.3, "jump", "laugh"),
                         kf(B["b4"], HERO_HIGH, 0.3, "fly", "laugh"),
                         kf(S_STREET, HERO_HIGH, 0.3, "fly", "laugh")],
                # FIX ROUND 2: Mia's ground spot FRIEND_P [2,0,-3.5]
                # sits directly under the Dare tree canopy (foliage ball
                # [2.5,5.8,-2.5] r 2.6) — her head was inside the leaves.
                # She walks to MIA_CLEAR [0,0,1] during b3 (a brisk
                # walk, mostly off-frame while the camera rides up with
                # Max) and watches from there through the scene; the
                # location cut to the street hides her return to
                # FRIEND_P in the next scene.
                # SPACING FIX (2026-11-23): MIA_CLEAR was [-2,0,1],
                # only 3.0 from the hero's x,z [-5,1] — the 2D spacing
                # check (min 4.50) failed at f251. [0,0,1] is 5.0 away,
                # and the whole walk path stays >= 5.0 from him.
                # FACE FIX (2026-11-23): she faced HERO_HIGH (Max, up
                # north-west) so the south camera saw only the back of
                # her head — her shocked mouth never read. She now faces
                # MIA_WATCH [-3,7,10] (up and south-west, between Max
                # and the camera): her gaze stays up-left toward Max
                # while her face turns ~25 deg to the camera, so the
                # open mouth reads in the two-shot.
                "friend": [kf(S_JUMP, FRIEND_P, face(FRIEND_P, HERO_P), "idle", "smile"),
                           kf(B["b3"], FRIEND_P, face(FRIEND_P, [-5, 6, 1.0]), "idle", "shocked"),
                           kf(B["b3"] + 60, [0, 0, 1], face([0, 0, 1], [-3, 7, 10]), "walk", "shocked"),
                           kf(B["b4"], [0, 0, 1], face([0, 0, 1], [-3, 7, 10]), "idle", "shocked"),
                           kf(S_STREET, [0, 0, 1], face([0, 0, 1], [-3, 7, 10]), "idle", "shocked")],
            },
        },
        {   # Street: the teacher explains the weight, then points up at the
            # Moon. The teacher points screen-right (rotY 1.0) toward where
            # the Moon sits, rather than facing it exactly — facing the Moon
            # dead-on would turn his back to the camera. b6 and b7 are long
            # beats (~3.3-3.6 s), so each window is split in two to keep
            # every shot under 3.5 s.
            "id": "teacher", "location": "street",
            "startFrame": S_STREET, "endFrame": S_SPACE,
            "fx": moon_fx,
            # FIX1: v1 close-up (side=-1.5) shot from her left while she
            # points screen-right, so her face fell in profile and was sliced
            # by the right edge, with the street-lamp arm (x 6.6-8.4, y 8.2,
            # z -16) sitting right over her head. Shooting from her right
            # (side=+2.0) puts her face near front-on and centred, and moves
            # the lamp ~27 deg off her head; dist 8.0 gives headroom.
            "cameraShots": [
                close_up(S_STREET, S_STREET + 45, TEACHER_P, side=2.0, dist=8.0),
                medium(S_STREET + 45, B["b7"], TEACHER_P),
                shot(B["b7"], B["b7"] + 45, [6, 20, 10], [7, 21, 9],
                     [12, 40, -14], [12.5, 40.5, -14.5], 50),
                shot(B["b7"] + 45, B["b8"], [2, 16, 14], [3, 17, 13],
                     [12, 40, -14], [13, 41, -15], 50),
                # FIX1: b8 wides pulled the target 1.5 left so Mia (now at
                # x 4) sits fully in frame instead of half off the right edge.
                # FIX2: the pole still crossed her right side, and the trio
                # now spans -5..2, so the cameras pull back (z 25/24) and pan
                # right (target -0.5) to centre the trio with margins.
                shot(B["b8"], (B["b8"] + S_SPACE) // 2, [0, 9, 25], [0, 8.8, 24],
                     [-0.5, 9, 0], [-0.5, 9, 0], 58),
                shot((B["b8"] + S_SPACE) // 2, S_SPACE, [0, 8.8, 24], [0, 8.5, 23],
                     [-0.5, 9, 0], [-0.5, 9, 0], 58),
            ],
            "characters": {
                "hero": [kf(S_STREET, HERO_HIGH, 0.3, "fly", "laugh"),
                         kf(B["b8"], HERO_HIGH, 0.3, "fly", "shocked"),
                         kf(S_SPACE, HERO_HIGH, 0.3, "fly", "shocked")],
                "friend": hold(S_STREET, S_SPACE, FRIEND_P, face(FRIEND_P, HERO_HIGH), "idle", "shocked"),
                "teacher": [kf(S_STREET, TEACHER_P, 1.0, "point", "deadpan"),
                            kf(B["b8"], TEACHER_P, 1.0, "point", "shocked"),
                            kf(S_SPACE, TEACHER_P, 1.0, "point", "shocked")],
            },
        },
        {   # Space: the Moon alone, big in frame, drifting up and back.
            # No characters — a cutaway while the narration explains the
            # sky leaking and the orbit slipping.
            # FIX ROUND 2: the Earth is in frame now (left), and the
            # Moon visibly shrinks across the three wide shots as it
            # drifts up and away; skyColor black (v2's bright-blue sky
            # read as daytime, and its contrast made the dark floor
            # read as a band — against black the floor vanishes).
            "id": "moon-drifts", "location": "space", "skyColor": "#000000",
            "startFrame": S_SPACE, "endFrame": S_SHOUT,
            "fx": space_moon_fx + space_earth_fx,
            "cameraShots": cover(S_SPACE, S_SHOUT, [
                lambda a, b: shot(a, b, [0, 12, 20], [0, 12, 19], [0, 12, -20], [0, 12.5, -21], 50),
                lambda a, b: shot(a, b, [0, 14, 22], [0, 14, 21], [0, 12, -20], [0, 12.5, -21], 50),
                lambda a, b: shot(a, b, [0, 12, 21], [0, 12, 20], [1, 13, -21], [1, 13.5, -22], 50),
            ]),
            "characters": {},
        },
        {   # The shouts + payoff, one scene: the three shout words land on
            # one wide shot of the whole tableau (teacher pointing up, Max
            # still floating, Mia on the ground, shake on) — the shouts
            # alone run under ~2 s, too short for their own scene — then
            # Max drifts down soft and slow and lands on his feet across
            # b11 (the wide shot tracks the descent), then a close-up on
            # him landed, smiling, as the science lands.
            "id": "payoff", "location": "street",
            "startFrame": S_SHOUT, "endFrame": S_TWIST,
            "fx": moon_fx,
            # FIX1: v1 tableau was a level wide (camera y 8, target y 9), which
            # put the teacher's head right at the 68% caption band, so THE /
            # MOON! / LEAVING! sat over her face. Reframed as a low camera
            # looking up: Max floats big in the upper half, the caption band
            # falls on empty sky, and the teacher + Mia sit at the bottom
            # edge with their heads clear of the text.
            # FIX2: the low camera (y 3) put a big dark foreground mass
            # across Mia's torso and the pole right by her face. Raised the
            # camera to y 6 and pulled back to z 26 so the sightline clears
            # low foreground and Mia (now at x 2) sits clear of the pole.
            # FIX2b: the tableau's first ~19 frames (1112-1130) render a
            # big vivid-green hill filling the bottom of the frame, hiding
            # the teacher and Mia — the frame only settles to the clean
            # street tableau from ~f1135. Workaround: open the shout on
            # the Moon itself for the first 30 frames ("THE" + "MOON!") —
            # a tight sky-only shot whose frustum excludes the ground and
            # hills entirely — then cut to the tableau at f1142 for the
            # rest of "MOON!" and "LEAVING!". The tableau runs to
            # S_PAYOFF+1 and the descent starts one frame later so both
            # shots stay >= 1.0 s (the 59-frame shout window cannot hold
            # two 30-frame shots otherwise); the hero is still at
            # HERO_HIGH through S_PAYOFF, so nothing else shifts.
            # FIX3 (round 3): FIX2b's "hill" attribution was WRONG.
            # Bisection (hide hills / baseplate / trees / houses / school /
            # SE+shop / playground one at a time, re-render f1145) proves
            # the green mass is the Playground's RoundTree at
            # playground-local [-12,0,6] -> stage (2,-0.2,25): its #22C55E
            # foliage balls sit ~1 stud in front of the tableau camera
            # start [0,6,26], so they fill the bottom ~55% vivid and
            # unfogged. As the camera pushes -z it passes into/behind the
            # foliage (backface-culled / behind camera) and the mass sweeps
            # up and clears at ~progress 0.5 — f1157 in the old framing,
            # same progress in the old 60-frame tableau (clean ~f1141).
            # The real horizon hill renders correctly as a pale fogged dome
            # in the clean frames. Fix: open the tableau at its
            # progress-0.6 camera ([0,5.88,25.4] / [-0.5,15.3,-2] = the
            # old f1160 framing, verified clean) so the shot starts past
            # the foliage; same end camera, same frames, same shake.
            "cameraShots": [
                shot(S_SHOUT, S_SHOUT + 30, [0, 6, 26], [0, 6, 25.8],
                     [14, 42, -17], [14.25, 42.25, -17.5], 40),
                # FIX ROUND 2: the old tableau ([0,5.88,25.4] -> [-0.5,15.3,-2],
                # fov 60) cropped the Moon ~55% at the top-right edge for the
                # whole shout. Pulled back and up ([0,11,32] -> [3,22,-6],
                # fov 66): the Moon sits whole at the top-right, the trio
                # waist-up along the bottom, the caption band on empty sky
                # between them. Sightline clears the street RoundTree
                # foliage at stage (2,5.8,25) by ~7 studs.
                shot(S_SHOUT + 30, S_PAYOFF + 1, [0, 11, 32], [0, 11, 31.5],
                     [3, 22, -6], [3, 22, -6], 66, shake=0.06),
                shot(S_PAYOFF + 1, (S_PAYOFF + 1 + B["b12"]) // 2, [0, 8, 22], [0, 7.8, 21],
                     [-3, 10, 1.0], [-3.5, 8, 1.0], 58),
                shot((S_PAYOFF + 1 + B["b12"]) // 2, B["b12"], [0, 7.8, 21], [0, 7.5, 20],
                     [-3.5, 8, 1.0], [-4, 6, 1.0], 58),
                close_up(B["b12"], (B["b12"] + S_TWIST) // 2, HERO_P),
                medium((B["b12"] + S_TWIST) // 2, S_TWIST, HERO_P),
            ],
            "characters": {
                "hero": [kf(S_SHOUT, HERO_HIGH, 0.3, "fly", "shocked"),
                         kf(S_PAYOFF, HERO_HIGH, 0.3, "fly", "shocked"),
                         kf(B["b12"], HERO_P, 0.3, "idle", "smile"),
                         kf(S_TWIST, HERO_P, 0.3, "idle", "smile")],
                "friend": [kf(S_SHOUT, FRIEND_P, face(FRIEND_P, HERO_HIGH), "idle", "shocked"),
                           kf(B["b12"], FRIEND_P, face(FRIEND_P, HERO_P), "idle", "smile"),
                           kf(S_TWIST, FRIEND_P, face(FRIEND_P, HERO_P), "idle", "smile")],
                "teacher": [kf(S_SHOUT, TEACHER_P, 1.0, "point", "panic"),
                            kf(B["b12"], TEACHER_P, 0.2, "idle", "smile"),
                            kf(S_TWIST, TEACHER_P, 0.2, "idle", "smile")],
            },
        },
        {   # Twist, at night: Max looks up at a Moon that is a little
            # smaller than yesterday. Wide of the three, then a last shot
            # of the Moon itself, higher and further than at the hook.
            "id": "twist", "location": "street", "isNight": True,
            "startFrame": S_TWIST, "endFrame": END,
            "fx": moon_fx,
            "cameraShots": split_shots(S_TWIST, END, [
                lambda a, b: wide(a, b, [0, 0, 1.0], 22),
                lambda a, b: shot(a, b, [6, 20, 10], [7, 21, 9],
                                  [15, 43, -19], [16, 44, -21], 50),
            ]),
            "characters": {
                "hero": hold(S_TWIST, END, HERO_P, 0.3, "idle", "shocked"),
                "friend": hold(S_TWIST, END, FRIEND_P, -0.3, "idle", "shocked"),
                "teacher": hold(S_TWIST, END, TEACHER_P, 0.2, "idle", "deadpan"),
            },
        },
    ]
