"""NO FRICTION — "What If There Was No Friction?"

Science explainer, lead: Max, an R6 kid_boy (blue spiky hair, red
hoodie — kept the whole video). His friend Mia watches from the
sidewalk; the teacher explains the science at the end.

The one science idea: friction is what lets you walk and stop. Your
foot pushes back on the ground and the ground pushes you forward —
take away the grip and you just slide. Brakes can't grip wheels, so
nothing stops.

FIX ROUND 1 (2026-11-22): the narration now OPENS with the title
question ("What if there was no friction?") over a medium shot of Max
looking at the camera, per the channel rule — every Short starts with
a big "What if" question. Staging fixes from independent review:
(1) the shout close-ups now track Max at medium distance so he stays
in frame through "NO! GRIP! AT ALL!"; (2) the lamppost grab and hold
are shot from the north-east, with Max facing the pole, arm out, so
the hand-on-pole reads and the pole stays visible beside him (from
the south/east the pole hides directly behind his body); (3) the bus-glide shot is a slow pan along the bus's east face from
far enough east that the tree at [21, 0, 17] stays out of frame and
the bus stays visible the whole shot; (4) the hook slide lane moved
right (x -4..-1) so the foreground pine at [-6.4, 0.2, 3.6] no longer
occludes Max; (5) the classroom wides pulled back to dist 24,
centred on the class, so the teacher and Mia are whole.

The slip pose (proven in stills at
~/workspace/videos/noob-compare/new-assets/sliding-boy/front-t0.png):
the kid leans back (rz=0.4) with a 'panic' face and 'walk' anim while
his keyframe position slides across the street — the legs walk but the
body glides, which reads as sliding. rz=0 once he grabs the lamppost.

Locations: 'ice_street' (icy street with mirror reflection; use
skyColor '#BFDBFE') for the slide, the bag and the lamppost grab;
'school_exterior' for the bus shot (the yellow school bus sits on the
side at x ~26 — it is environment geometry, so it cannot move; the
"glide" is carried by a camera pan along the bus + a whoosh SFX +
the narration); 'classroom' for the teacher's explanation, with the
science on the chalkboard.

The lamppost: ice_street has real street lamps — the nearest one to
the actor area is at [-3.85, 0.18, -5.5]. The grab is staged beside
it (hero ends at [-3.0, 0, -4.6], ~1.2 studs from the post, facing
the pole so his raised 'point' arm reaches it). There is no bag prop:
the bag lives in the narration + his reaching gesture, he slides
past it.
"""
import math

from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, orbit, shot, split_shots, static_shot, wide  # noqa: F401

TITLE = "NO FRICTION"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b0", "text": "What if there was no friction?", "pause": 0.10},
    {"id": "b1", "text": "In this town, there is no friction. The streets are slippery as ice.", "pause": 0.08},
    {"id": "b2", "text": "Max walks to school, and his feet slide out from under him.", "pause": 0.08},
    {"id": "b3", "text": "He tries to stop, but his shoes cannot grip the ground at all.", "pause": 0.08},
    {"id": "b4", "text": "He slides across the street, arms waving, faster and faster.", "pause": 0.08},
    {"id": "b5", "text": "He reaches for his bag, but his fingers slide right off it.", "pause": 0.08},
    {"id": "b6", "text": "The school bus comes, and the driver hits the brakes. But nothing stops.", "pause": 0.08},
    {"id": "b7", "text": "The bus just glides past him, smooth and slow, like a boat on ice.", "pause": 0.10},
    {"id": "w1", "text": "NO!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "GRIP!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "AT ALL!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b8", "text": "Max reaches out and grabs the lamppost, and holds on tight.", "pause": 0.08},
    {"id": "b9", "text": "His friend Mia watches from the sidewalk, too scared to step out.", "pause": 0.08},
    {"id": "b10", "text": "At school, the teacher explains: friction is the grip between two surfaces.", "pause": 0.08},
    {"id": "b11", "text": "Your foot pushes back, and the ground pushes you forward.", "pause": 0.08},
    {"id": "b12", "text": "Brakes grip the wheels to stop. No grip, no stopping.", "pause": 0.08},
    {"id": "b13", "text": "But tonight, Max sleeps holding the bedpost, just in case the grip never comes back.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05,
         "dropouts": [("b7+0.3", "w3.end")]}
SFX = [
    ("b0", "whoosh"),
    ("b1", "whoosh"),
    ("b2+0.3", "swish"),
    ("b3+0.4", "pop", {"f": 600}),
    ("b4", "whoosh"),
    ("b5+0.5", "pop_down"),
    ("b6+0.3", "whoosh"),
    ("b7+0.4", "riser", {"dur": 1.6}),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b8+0.3", "thud"),
    ("b9+0.4", "sad"),
    ("b10+0.5", "ding_dong"),
    ("b11+0.5", "pop", {"f": 700}),
    ("b12+0.5", "pop", {"f": 600}),
    ("b13+1.0", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
CAST = {
    # Max: the hero. Blue spiky hair + red hoodie, kept the whole video.
    "hero": {"extends": "kid_boy", "hair": {"style": "spikyAnime", "color": "blue"},
             "top": {"style": "hoodie", "color": "red", "secondary": "white"},
             "bottom": {"style": "jeans", "color": "denim"},
             "shoes": {"color": "white", "sole": "white"}},
    # Mia: his friend, watching from the sidewalk.
    "friend": {"extends": "kid_girl", "hair": {"style": "pigtails", "color": "brown"},
               "top": {"style": "sweater", "color": "teal", "secondary": "white"},
               "bottom": {"style": "skirt", "color": "navy"},
               "shoes": {"color": "white", "sole": "white"}},
    "teacher": {"extends": "teacher"},
}


# 4. SCENES --------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END
    S_SLIDE = B["b2"] - 1   # ice street: the slide begins
    S_BAG = B["b5"] - 1     # ice street: the bag
    S_BUS = B["b6"] - 1     # school exterior: the bus
    S_POST = B["b8"] - 1    # ice street: the lamppost
    S_CLASS = B["b10"] - 1  # classroom: the teacher explains

    # The lamppost: ice_street has a real street lamp at [-3.85, 0.18,
    # -5.5]. GRAB_P is the spot 1.87 studs from its post where the
    # hero's right hand lands ON the pole: the point arm's skin hand
    # spans 0.72..1.50 forward of the shoulder (ArmSleeve: skin to
    # y -1.5, rotated -1.55 about X), centre 1.11, and the shoulder
    # sits 1.5 to his right, so |hand-centre - centre| =
    # sqrt(1.5^2 + 1.11^2) = 1.87, and the facing must sit 37 deg
    # off the pole direction (f = D(1.11-1.5i)/3.48) — facing the
    # pole dead-on puts the hand ~1.5 studs east of it. GRAB_RY =
    # -1.79 is that facing.
    # FIX ROUND 2: round 1 staged him facing the pole dead-on
    # (face(GRAB_P, LAMP)) at [-3.0, -4.6], so the point arm missed
    # the pole by ~1.5 studs, and the -3.97 turn faced him away
    # from the lamp for the whole grab beat — no frame showed a
    # hand on the pole. He now slides in by f845, grabs with the
    # corrected facing, and holds the grab through B["b9"] before
    # turning to the camera to smile. LAMP is the pole, for face().
    # GRAB_RY (2026-11-23, empirical): the arm math said -1.79, but the
    # render puts the hand off the pole. Bracketing: -1.79 -> hand ~25%
    # of frame RIGHT of the pole; -1.43 -> further right (~40%); -2.39
    # -> ~40% LEFT of the pole. Zero crossing interpolates to -2.02.
    # (Likely cause: the Euler XYZ order / shoulder Z-rotation shifts the
    # hand a few degrees off the analytic facing; the render is truth.)
    LAMP = [-3.85, 0.18, -5.5]
    GRAB_P = [-3.10, 0, -3.79]
    GRAB_RY = -2.02
    GRAB_F = B["b8"] + 40   # he reaches the pole 40f into b8 (f845)
    FRIEND_P = [9, 0, -2.5]

    # Hero's lateral slide on the ice street: x from -1 to 2 at z=1,
    # linear between S_SLIDE and S_BAG (used by the tracking cameras).
    # The lane starts at -1, not -3: the foreground pine at [-6.4, 0.2,
    # 3.6] occluded Max when the hook began at x=-6.
    def _hx(f):
        if f <= S_SLIDE:
            return -1.0
        if f >= S_BAG:
            return 2.0
        return -1.0 + 3.0 * (f - S_SLIDE) / (S_BAG - S_SLIDE)

    # Hero's diagonal slide to the lamppost: from [2, 0, 1] at S_POST to
    # GRAB_P at GRAB_F (f845), then he stays put, holding on.
    def _p5(f):
        if f <= S_POST:
            return [2.0, 0, 1.0]
        if f >= GRAB_F:
            return list(GRAB_P)
        t = (f - S_POST) / (GRAB_F - S_POST)
        return [2.0 + (GRAB_P[0] - 2.0) * t, 0, 1.0 + (GRAB_P[2] - 1.0) * t]

    # Hero's slide across the schoolyard: x from 6 at S_BUS to 14 at
    # B["w1"], then he stays at 14 through the shouts (used by the
    # tracking shout cameras so he never leaves the frame).
    def _bx(f):
        if f <= S_BUS:
            return 6.0
        if f >= B["w1"]:
            return 14.0
        return 6.0 + 8.0 * (f - S_BUS) / (B["w1"] - S_BUS)

    return [
        {   # Hook: the big question over Max's face, then the setup.
            # Shot 1 is a medium on Max (panic, leaning into the
            # slide) while "What if there was no friction?" plays —
            # a close-up does NOT work here: his rz=0.4 lean shifts
            # his head ~1.6 studs left, out of a close-up frame. The
            # medium is centred slightly left ([-4.6, 0, 1]) to hold
            # both his leaning head and his body. Shots 2-3 pull back
            # to wide/medium as b1 sets the scene. Max slides x -4..-1,
            # clear of the pine at [-6.4, 3.6].
            "id": "hook", "location": "ice_street", "skyColor": "#BFDBFE",
            "startFrame": 0, "endFrame": S_SLIDE,
            "cameraShots": [medium(0, B["b1"], [-4.6, 0, 1])] + split_shots(B["b1"], S_SLIDE, [
                lambda a, b: wide(a, b, [-2.5, 0, 1]),
                lambda a, b: medium(a, b, [-2.5, 0, 1]),
            ]),
            "characters": {
                "hero": [kf(0, [-4, 0, 1], 0, "walk", "panic", rz=0.4),
                         kf(S_SLIDE, [-1, 0, 1], 0, "walk", "panic", rz=0.4)],
            },
        },
        {   # The slide: he tries to stop, he can't, he goes faster.
            # Mia watches from the far sidewalk, well clear of his lane.
            "id": "slide", "location": "ice_street", "skyColor": "#BFDBFE",
            "startFrame": S_SLIDE, "endFrame": S_BAG,
            "cameraShots": cover(S_SLIDE, S_BAG, [
                lambda a, b: shot(a, b, [_hx(a), 5.6, 13], [_hx(b), 5.6, 12.2],
                                  [_hx(a), 4.3, 1], [_hx(b), 4.3, 1], 50),
                lambda a, b: wide(a, b, [0.5, 0, 1], dist=22),
                lambda a, b: medium(a, b, [_hx((a + b) // 2), 0, 1]),
            ]),
            "characters": {
                "hero": [kf(S_SLIDE, [-1, 0, 1], 0, "walk", "panic", rz=0.4),
                         kf(S_BAG, [2, 0, 1], 0, "walk", "panic", rz=0.4)],
                "friend": hold(S_SLIDE, S_BAG, FRIEND_P, 0, "idle", "shocked"),
            },
        },
        {   # The bag: he reaches for it and slides right past.
            # No bag prop exists — the reach + the narration carry it.
            "id": "bag", "location": "ice_street", "skyColor": "#BFDBFE",
            "startFrame": S_BAG, "endFrame": S_BUS,
            "cameraShots": cover(S_BAG, S_BUS, [
                lambda a, b: shot(a, b, [2, 5.6, 13], [4, 5.6, 12.2],
                                  [2, 4.3, 1], [4, 4.3, 1], 50),
                lambda a, b: close_up(a, b, [3, 0, 1]),
            ]),
            "characters": {
                "hero": [kf(S_BAG, [2, 0, 1], 0, "point", "panic", rz=0.4),
                         kf(S_BUS, [4, 0, 1], 0, "walk", "panic", rz=0.4)],
                "friend": hold(S_BAG, S_BUS, FRIEND_P, 0, "idle", "shocked"),
            },
        },
        {   # The bus: it can't brake, it glides past. The yellow school
            # bus sits on the side at x ~26 (W/2+6, z=2, 16 long in z).
            # It is environment geometry and cannot move, so the glide
            # is a camera pan along the bus's east face + whoosh +
            # narration. CAREFUL: those are SCHOOL-LOCAL coords. The
            # TownExterior shifts the town so the school anchor
            # [36, 0, -14] is the stage origin, and the School itself
            # sits at town [36, 0, -34] — so in STAGE coords the bus is
            # at [26, 0, -18], spanning z -26..-10. The pan camera
            # stands east of it at x=40, z=-18, and pans its target
            # along the bus's length, so the SCHOOL BUS label and
            # windows sweep across the frame while the bus stays
            # visible the whole shot. (First attempt aimed at z=2 and
            # showed an empty town street — the bus is 20 studs north
            # of there.) The shout close-ups are now tracking mediums
            # that follow Max's x, so he stays whole in frame through
            # "NO! GRIP! AT ALL!".
            # Max slides across Main St in front of the school (z=17
            # in stage coords; the schoolyard itself is at z -13..5,
            # the bike rack at [12, 0, -7] and benches at [+-17, 0, -7]
            # in stage coords). Mia watches from the far side of the
            # street.
            "id": "bus", "location": "school_exterior",
            "startFrame": S_BUS, "endFrame": S_POST,
            "cameraShots": split_shots(S_BUS, S_POST, [
                lambda a, b: shot(a, b, [4, 7, 25], [4, 6.8, 24],
                                  [6, 4.5, 17], [8, 4.5, 17], 58),
                # Bus glide: static camera east of the bus, target pans
                # along the bus's length — the SCHOOL BUS label and
                # windows sweep across the frame, so the bus reads as
                # gliding past while staying visible throughout.
                lambda a, b: shot(a, b, [40, 5, -18], [40, 5, -18],
                                  [26, 2.5, -12], [26, 2.5, -24], 55),
                # Shout peak, part 1: tracking medium on Max.
                lambda a, b: shot(a, b, [_bx(a), 5.6, 29], [_bx(b), 5.6, 29],
                                  [_bx(a), 4.3, 17], [_bx(b), 4.3, 17], 50),
                # Shout peak, part 2: same tracking medium, with shake.
                lambda a, b: shot(a, b, [_bx(a), 5.6, 29], [_bx(b), 5.6, 29],
                                  [_bx(a), 4.3, 17], [_bx(b), 4.3, 17], 50, shake=0.08),
            ]),
            "characters": {
                "hero": [kf(S_BUS, [6, 0, 17], 0, "walk", "panic", rz=0.4),
                         kf(B["w1"], [14, 0, 17], 0, "walk", "panic", rz=0.4),
                         kf(B["w1"] + 1, [14, 0, 17], 0, "point", "panic", rz=0.4),
                         kf(S_POST, [14, 0, 17], 0, "point", "panic", rz=0.4)],
                "friend": hold(S_BUS, S_POST, [-6, 0, 17], 0, "idle", "shocked"),
            },
        },
        {   # The lamppost: he slides the last stretch diagonally to the
            # lamp at [-3.85, 0.18, -5.5], grabs it and holds on — rz=0,
            # panic melting into a smile once he is safe. Mia watches
            # from the sidewalk, too scared to step out.
            # FIX ROUND 2: the grab is re-staged from the arm geometry
            # (see GRAB_P / GRAB_RY above) — he reaches the pole at
            # f845 with the corrected facing, so the point arm's hand
            # lands ON the pole, and he HOLDS that grab through
            # B["b9"] before turning to the camera (ry -3.97 = 2.31 -
            # 2*pi, the short turn) to smile. Shot 1 tracks the
            # diagonal slide in; shots 2-3 are from the NORTH-EAST:
            # the pole stands north-west of Max, so from the south/
            # east it hides directly behind his body — the first
            # attempt (due-east side view) showed only his back and
            # no pole. From the north-east the pole sits to the side
            # of Max, his 'point' arm reaches it, and his face is in
            # profile (shot 2) / turned to the camera (shot 3).
            "id": "lamppost", "location": "ice_street", "skyColor": "#BFDBFE",
            "startFrame": S_POST, "endFrame": S_CLASS,
            "cameraShots": [
                shot(S_POST, GRAB_F,
                     [_p5(S_POST)[0], 5.6, _p5(S_POST)[2] + 12],
                     [_p5(GRAB_F)[0], 5.6, _p5(GRAB_F)[2] + 12],
                     [_p5(S_POST)[0], 4.3, _p5(S_POST)[2]],
                     [_p5(GRAB_F)[0], 4.3, _p5(GRAB_F)[2]], 50),
                shot(GRAB_F, B["b9"] + 36,
                     [4.5, 5.0, -11.0], [4.0, 5.0, -10.5],
                     [-3.4, 3.2, -5.0], [-3.4, 3.2, -5.0], 50),
                shot(B["b9"] + 36, S_CLASS,
                     [4.5, 5.6, -11.0], [4.0, 5.6, -10.5],
                     [-3.2, 4.0, -5.0], [-3.2, 4.0, -5.0], 50),
            ],
            "characters": {
                "hero": [kf(S_POST, [2, 0, 1], 0, "walk", "panic", rz=0.4),
                         kf(GRAB_F, GRAB_P, GRAB_RY, "point", "panic", rz=0),
                         kf(B["b9"], GRAB_P, GRAB_RY, "point", "panic", rz=0),
                         kf(B["b9"] + 36, GRAB_P, -3.97, "idle", "smile", rz=0),
                         kf(S_CLASS, GRAB_P, -3.97, "idle", "smile", rz=0)],
                "friend": hold(S_POST, S_CLASS, FRIEND_P, 0, "idle", "shocked"),
            },
        },
        {   # The teacher explains: friction is the grip. The science
            # sits on the chalkboard behind her. The wides are pulled
            # back to dist 24 and centred on the class ([-0.25, 0, 0])
            # so the teacher at x=-5.5 and Mia at x=5 are whole.
            # FIX ROUND 2: this scene now ends at b13 (f1283) — the
            # closing line moves to the bedroom below.
            "id": "classroom", "location": "classroom",
            "boardText": ["FRICTION = GRIP", "No grip = no walk", "No grip = no stop"],
            "startFrame": S_CLASS, "endFrame": B["b13"] - 1,
            "cameraShots": cover(S_CLASS, B["b13"] - 1, [
                lambda a, b: wide(a, b, [-0.25, 0, 0], dist=24),
                lambda a, b: medium(a, b, [0, 0, 1]),
                lambda a, b: wide(a, b, [-0.25, 0, 0], dist=24),
                lambda a, b: close_up(a, b, [0, 0, 1.5]),
            ]),
            "characters": {
                "teacher": [kf(S_CLASS, [-5.5, 0, -2], face([-5.5, 0, -2], [0, 0, 1.5]), "idle", "smile"),
                            kf(B["b11"], [-5.5, 0, -2], face([-5.5, 0, -2], [0, 0, 1.5]), "point", "smile"),
                            kf(B["b13"] - 1, [-5.5, 0, -2], face([-5.5, 0, -2], [0, 0, 1.5]), "idle", "smile")],
                "hero": [kf(S_CLASS, [0, 0, 1.5], 0, "idle", "smile"),
                         kf(B["b13"] - 1, [0, 0, 1.5], 0, "idle", "smile")],
                "friend": [kf(S_CLASS, [5, 0, 1.5], 0, "idle", "smile"),
                           kf(B["b13"] - 1, [5, 0, 1.5], 0, "idle", "shocked")],
            },
        },
        {   # The closing line, at last in a bedroom: Max asleep in bed,
            # holding the bedpost. FIX ROUND 2: v2 played this line
            # over the classroom — no bedroom, bed, or bedpost existed
            # anywhere in the video. The bedroom location is real
            # (interiors.tsx, night variant) and the bed now has four
            # corner posts (see BedroomEnvironment).
            # Staging (from the R6 arm geometry): lying flat
            # (rx=-pi/2, the no_sleep pattern), the left arm hangs
            # south from the shoulder, 2.0 long — so with the root at
            # bed-local (0.7, 4.8) the left hand lands exactly on the
            # east foot post (bed-local (2.2, 3.3)), at y 2.4, mid-post.
            # NOTE: head-on-pillow + hand-on-foot-post is geometrically
            # impossible (the shoulder sits 3.5 north of the feet and
            # the arm reaches 2.0, while the foot post is 4.8 south of
            # the shoulder when the head is on the pillow) — so his
            # head rests on the blanket 2.2 south of the pillow and his
            # feet dangle 1.5 past the foot of the bed, sprawled in his
            # sleep with a grip on the post. No narration change, no
            # new TTS.
            # FIX ROUND 3 (2026-11-23): v3 FAILED on this grip alone —
            # the hand only touched the post's WEST face, nothing on
            # the far side. Root cause, found in the fix3 previews:
            # the hand was NEVER on the post in 3D — it sat 0.25 NORTH
            # of it. The arm is 1.5 long from the shoulder pivot, the
            # skin hand's CENTRE is 1.11 along it, so the hand centre
            # is at root + (1.665, 0, -2.402) — the old note's "arm
            # reaches 2.0" wrongly put the hand at the arm's very end,
            # and every x-shift since (incl. fix 2's west shift) chased
            # a 2D projection artefact. The real fix is a SOUTH shift:
            # root z 0.4 -> 1.30 puts the hand centre on the post's z
            # (-1.1), and root x -6.60 -> -6.47 centres it on the
            # post's x (-4.8). The skin box (0.98 wide, z-span
            # -1.49..-0.72) now CONTAINS the post's cross-section, so
            # beige shows on all sides of the brown post at y 1.9-2.9
            # — a genuine wrap, readable from any angle. Shot 2 is a
            # HIGH south-east drift so the hand is on the NEAR face of
            # the post (v3 shot it LOW from the south-east, with the
            # post hiding the hand and Max's head); a first west-side
            # attempt failed in preview — the camera path crossed his
            # dangling legs.
            "id": "bedroom", "location": "bedroom", "variant": "blue", "isNight": True,
            "startFrame": B["b13"] - 1, "endFrame": END,
            "cameraShots": [
                static_shot(B["b13"] - 1, (B["b13"] - 1 + END) // 2,
                            [-1.35, 7.4, 26], [-3, 4.5, -2], 58),
                # FIX ROUND 3: shot from the SOUTH-EAST, HIGH, drifting
                # in on the grip. First attempt (west side) was wrong:
                # the camera path crossed Max's dangling legs, which
                # filled the frame and cut the post off. From high
                # south-east the legs stay out of frame left, the hand
                # sits on the NEAR (south) face of the post with beige
                # showing on both sides of the brown post, the red
                # sleeve passes behind the post to the torso, and Max's
                # head stays visible upper-left. (v3 shot from the
                # south-east too, but LOW and from x=+2.5, so the post
                # hid both the grip and his head.)
                shot((B["b13"] - 1 + END) // 2, END, [-2.5, 7.0, 8.0], [-3.5, 6.2, 6.5],
                     [-4.8, 2.6, -1.6], [-4.8, 2.4, -1.1], 50),
            ],
            "characters": {
                # FIX ROUND 3 (2026-11-23): root at (-6.47, 2.4, 1.30)
                # — hand centre lands on the east foot post (-4.8, -1.1)
                # in x AND z (see the staging note above). The hips sit
                # at the bed's foot edge and the feet dangle further
                # past it, which fits the sprawled-asleep staging.
                "hero": [kf(B["b13"] - 1, [-6.47, 2.4, 1.30], 0, "sleep", "sleeping", rx=-math.pi / 2),
                         kf(END, [-6.47, 2.4, 1.30], 0, "sleep", "sleeping", rx=-math.pi / 2)],
            },
        },
    ]
