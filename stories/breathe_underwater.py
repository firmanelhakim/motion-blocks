"""BREATHE UNDERWATER — "What If You Could Breathe Underwater?"

Science explainer, lead: R6 `kid_boy` with the `gills` accessory — a kid
dives into the sea and keeps breathing. A little blocky fish becomes his
guide and shows him the reef; the fish explains gills, and the kid learns
his lungs are built for air, not water, and swims back up for a breath.

The ONE science idea: gills pull oxygen out of water; lungs can't. Fish
breathe dissolved oxygen through thin, feathery gills with a huge surface
area. Air is about 21% oxygen; water holds only a tiny amount dissolved
in it, and our lungs are built for air — they can't get enough oxygen
from water, and they fill up.

THE SWIMMING (first time any character has swum in the undersea
location — PROVEN by stories/swim_test.py, 2026-11-22): the hero swims
horizontal with rotationZ (kf(..., rz=-pi/2); R6Character applies one
Euler [rx, ry, rz]). rz=-pi/2 lays the body along +x (head leads,
chest/face toward the camera) and the 'walk' limb swing reads as a
paddling kick. rx does NOT do it — rx=1.2 left him diagonal and
head-toward-camera (v1 stills), and rx=pi/2, ry=HALF put him upside
down (swim_test scene C). The camera must target the BODY CENTER
(root + ~3 studs toward the head), NOT the root (the feet): targeting
the root put his head 6 studs off-frame (swim_test). The gills sit at
the neck, ~5 studs from the root toward the head — a gills close-up
targets root + 5. He dives in upright (rz 0), tilts to rz=-pi/2 as he
descends, cruises at y 4, then rises back to upright (rz 0) for the
shouts. The fish is the 'fish' ScienceFx (BlockyFish, faces +z, ~2.75
long): it swims by keyframing POSITION with a FIXED rotation
[0, HALF, 0] (its forward +z turns toward +x), scale 1.2. Bubbles are
the 'bubbles' fx, keyframed to follow the hero at hero position +
[0, 1, 0.5].

FIX 1 (2026-11-22, the maintainer: every story starts with the big "What if"
question): new opening beat q1 "What if you could breathe underwater?"
over its own hook scene — the hero already swimming horizontal, wide
side view, full body in frame, bubbles streaming — then the dive scene
restarts at the surface for b1 ("In this world, ..."). The cut between
hook and dive is a deliberate hook-then-setup reset.
FIX 1 staging fixes (independent review of v1):
  1. Dive shot 2 reframed: v1's _swim_cam targeted root+3 in x, but
     mid-tilt the true body center sits ~0.8 left and ~1.3 above that,
     so the feet landed on the left frame edge (~2.8-4.0s). The new
     shot tracks the true body-center path (-2.0, 7.1) -> (1.0, 4.0)
     from a wider distance (15-16, fov 55). Dive shot 1 also pulled
     back 1 stud so the head keeps its margin at the end of the tilt.
  2. Shout shot retargeted: v1 aimed at the FINAL upright head
     position (5.5, 11) while the hero was still tilted, so his face
     was cut at the right edge during "UP!"/"AIR!". The new shot
     tracks the head itself through the rise: (9.0, 8.5) -> (5.5, 11.5).
  3. Guide fish raised through the turning point: v1 parked it at
     (7, 7.5), exactly on the hero's rising body diagonal, so the
     torso hid it ~27-31s. It now rises to (6.5, 9.5) at S_CLIMAX and
     HOLDS there through w1, clear above the torso through b10 and
     the shouts (preview round 1: the first attempt at (6, 9.0) still
     let it sink back onto the diagonal by w1, and its tail clipped
     the left edge of the realisation shots — so the two realisation
     shots were also widened to dist 14-14.5, fov 55; preview round 2:
     the hold lifted to 9.5 for arm clearance, and the limit low shot
     widened to dist 13.5, fov 54, because the higher fish's tail
     touched the left edge there).
  4. Fish exit: v1 swam it to x=9 by the twist, past the right edge
     of the surface shot (~36.7s). It now stops at x=7.5, and the
     surface shot 2 is wider (fov 55, dist 12-13) so the whole fish
     stays in frame.
  5. Surface scene: shot 2 is now a low look-up (camera y ~5,
     target y ~8.5) so the bright top of frame and light rays read
     as the surface he is kicking toward. Seaweed: the undersea
     location already has seaweed clusters, but at x ~ +/-13, off
     the portrait frame of every v1 shot; the hook wide shot is
     framed to catch the left cluster at the frame edge.
"""
import math

from shorts.scene import HALF, close_up, cover, hold, kf, low_angle, medium, shot, split_shots  # noqa: F401

TITLE = "YOU CAN BREATHE UNDERWATER"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "q1", "text": "What if you could breathe underwater?", "pause": 0.10},
    {"id": "b1", "text": "In this world, you can breathe underwater, just like a fish.", "pause": 0.08},
    {"id": "b2", "text": "No tank. No mask. Just a kid, diving in.", "pause": 0.08},
    {"id": "b3", "text": "He looked down, and saw gills on his neck, fluttering.", "pause": 0.08},
    {"id": "b4", "text": "He breathed in. The water felt fine. Bubbles rose.", "pause": 0.08},
    {"id": "b5", "text": "Then a little fish swam up, orange and curious.", "pause": 0.08},
    {"id": "b6", "text": "The fish became his guide, showing him the reef and the seaweed.", "pause": 0.08},
    {"id": "b7", "text": "Fish breathe the oxygen dissolved in the water, through their gills.", "pause": 0.08},
    {"id": "b8", "text": "Their gills are thin and feathery, with a huge surface to catch it.", "pause": 0.08},
    {"id": "b9", "text": "Air is twenty-one percent oxygen. Water holds only a tiny sip of it.", "pause": 0.08},
    {"id": "b10", "text": "He tried to stay down. But his lungs are built for air, not water. They fill up.", "pause": 0.08},
    {"id": "w1", "text": "UP!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "AIR!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "NOW!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b11", "text": "He kicked for the surface, took a big breath of air, and waved goodbye.", "pause": 0.08},
    {"id": "b12", "text": "The little fish waved a fin back, and swam down to its reef.", "pause": 0.08},
    {"id": "b13", "text": "But tonight, if you look closely, the gills are still there.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05,
         "dropouts": [("b10+0.3", "w3.end")]}
SFX = [
    ("q1", "whoosh"),
    ("b1", "whoosh"),
    ("b2+0.5", "bubbles"),
    ("b3+0.4", "pop", {"f": 700}),
    ("b4+0.5", "bubbles"),
    ("b5+0.3", "pop", {"f": 800}),
    ("b6+0.5", "swish"),
    ("b7+0.5", "sparkle"),
    ("b8+0.5", "sparkle"),
    ("b9+0.5", "bell_low"),
    ("b10+0.3", "riser", {"dur": 1.6}),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b11+0.5", "sparkle"),
    ("b12+0.5", "pop", {"f": 600}),
    ("b13+1.5", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
CAST = {
    # The hero: R6 kid_boy with the gills accessory (6 thin pink slits on
    # the neck, src/characters/Accessories.tsx -> Gills). No other
    # characters: the fish is an fx, not a character, and the story is a
    # solo swim. One actor also means the spacing check is trivially clean.
    "hero": {"extends": "kid_boy", "accessories": ["gills"]},
}


# 4. SCENES --------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END
    S_HOOK = B["b1"] - 1     # hook: the "What if" question, hero swimming
    S_GILLS = B["b3"] - 1    # undersea: the gills, the first breath
    S_GUIDE = B["b5"] - 1    # undersea: the fish arrives and leads the tour
    S_LIMIT = B["b9"] - 1    # undersea: the science of the limit
    S_CLIMAX = B["b10"] - 1  # undersea: he realises, then the shouts, then up
    S_SURFACE = B["b11"] - 1  # undersea: back at the surface, goodbye wave
    S_TWIST = B["b13"] - 1   # beach: the gills are still there

    # The fish: a blocky orange clownfish that swims by keyframed POSITION
    # with a FIXED rotation [0, HALF, 0] (its forward +z turns toward +x),
    # scale 1.2. It swims in from the left at b5, leads the hero across
    # the reef (1.5 studs above him, 1.5 behind him in z, so it never
    # covers his face), rises clear above his torso while he realises
    # (S_CLIMAX and w1: (6.5, 9.5) — v1's (7, 7.5) sat on his rising
    # body diagonal and the torso hid it ~27-31s; the fish HOLDS at
    # 9.2 through w1 instead of sinking back onto the diagonal),
    # hovers through the shouts, then swims down to its reef — stopping
    # at x=7.5 so it is never clipped at the right edge on its way out
    # (v1 ran it to x=9, ~36.7s).
    fish_kf = [{"frame": S_GUIDE, "position": [-7, 7.5, -5]},
               {"frame": B["b6"], "position": [-1, 7.5, -5]},
               {"frame": B["b7"], "position": [3, 7.5, -5]},
               {"frame": S_LIMIT, "position": [6.5, 7.5, -5]},
               {"frame": S_CLIMAX, "position": [6.5, 9.5, -5]},
               {"frame": B["w1"], "position": [6.5, 9.5, -5]},
               {"frame": S_SURFACE, "position": [7.5, 6.5, -5]},
               {"frame": S_TWIST, "position": [7.5, 5.5, -5]}]
    fish_fx = [{"id": "fish", "shape": "fish", "scale": 1.2, "color": "#df6414",
                "rotation": [0, HALF, 0], "keyframes": fish_kf}]

    # The bubbles: a rising column (y -3.3 to +5.1 relative to its
    # position, scaled 0.7), keyframed to follow the hero at hero position
    # + [0, 1, 0.5] — the same path as his swim, so the breath bubbles
    # stream up from him in every underwater shot. During the hook they
    # follow his head (-3 -> 2 at y 5.5); the snap to the dive-start
    # position (-5, 8) lands on the hook/dive scene cut (S_HOOK -> +2),
    # so the jump is hidden by the cut itself.
    bubbles_kf = [{"frame": 0, "position": [-3, 5.5, -0.5]},
                  {"frame": S_HOOK, "position": [2, 5.5, -0.5]},
                  {"frame": S_HOOK + 2, "position": [-5, 8, -0.5]},
                  {"frame": B["b2"], "position": [-3.5, 6, -0.5]},
                  {"frame": S_GILLS, "position": [-1.5, 5, -0.5]},
                  {"frame": B["b4"], "position": [0.5, 5, -0.5]},
                  {"frame": S_GUIDE, "position": [2, 5, -0.5]},
                  {"frame": B["b6"], "position": [3, 5, -0.5]},
                  {"frame": B["b7"], "position": [4, 5, -0.5]},
                  {"frame": S_LIMIT, "position": [5, 5, -0.5]},
                  {"frame": S_CLIMAX, "position": [5.3, 5.2, -0.5]},
                  {"frame": B["w1"], "position": [5.5, 6, -0.5]},
                  {"frame": B["w2"], "position": [5.5, 6.8, -0.5]},
                  {"frame": S_SURFACE, "position": [5.5, 7.5, -0.5]},
                  {"frame": B["b12"], "position": [5.5, 8, -0.5]},
                  {"frame": S_TWIST, "position": [5.5, 8, -0.5]}]
    bubbles_fx = [{"id": "bubbles", "shape": "bubbles", "scale": 0.7, "color": "#c4efff",
                   "keyframes": bubbles_kf}]

    # Side-view swim camera: the hero swims toward +x, horizontal
    # (rz=-pi/2), so his body spans root .. root+6 in x. The camera sits
    # at his level on the +z side and targets the BODY CENTER (root + 3),
    # tracking him as he moves. hx0/hx1 = root x at the shot's ends.
    def _swim_cam(a, b, hx0, hx1, hy=4.3, dist=12.0, fov=50):
        return shot(a, b, [hx0 + 3, hy + 0.4, dist], [hx1 + 3, hy + 0.4, dist - 0.8],
                    [hx0 + 3, hy, -1], [hx1 + 3, hy, -1], fov)

    RZ = -math.pi / 2  # horizontal swim (head +x, chest/face to camera)
    return [
        {   # The hook: the big "What if" question over the hero already
            # swimming horizontal — wide side view, full body in frame,
            # bubbles streaming from his head. One shot (q1 is ~2s).
            # The dive scene then restarts at the surface for b1: a
            # deliberate hook-then-setup reset on the scene cut.
            "id": "hook", "location": "undersea", "skyColor": "#1D6FB8",
            "startFrame": 0, "endFrame": S_HOOK,
            "fx": bubbles_fx,
            "cameraShots": [
                shot(0, S_HOOK, [-5.5, 5.0, 16], [-0.5, 5.0, 15],
                     [-5.5, 4.5, -1], [-0.5, 4.5, -1], 55),
            ],
            "characters": {
                "hero": [kf(0, [-8, 4.5, -1], 0, "walk", "smile", rz=RZ),
                         kf(S_HOOK, [-3, 4.5, -1], 0, "walk", "smile", rz=RZ)],
            },
        },
        {   # The dive: upright at the top, tilting horizontal as he descends.
            "id": "dive", "location": "undersea", "skyColor": "#1D6FB8",
            "startFrame": S_HOOK, "endFrame": S_GILLS,
            "fx": bubbles_fx,
            "cameraShots": cover(S_HOOK, S_GILLS, [
                lambda a, b: shot(a, b, [-5, 7.5, 14], [-4, 6.5, 13],
                                  [-4.5, 7, -1], [-3, 6.3, -1], 55),
                # FIX 1: track the TRUE body center through the tilt
                # (-2.0, 7.1) -> (1.0, 4.0), from farther back (15-16,
                # fov 55). v1's _swim_cam aimed at root+3, which sits
                # ~0.8 right and ~1.3 below the tilted body center, so
                # the feet landed on the left frame edge.
                lambda a, b: shot(a, b, [-2.0, 7.6, 16], [1.0, 4.6, 15],
                                  [-2.0, 7.1, -1], [1.0, 4.0, -1], 55),
            ]),
            "characters": {
                "hero": [kf(S_HOOK, [-5, 7, -1], HALF, "idle", "smile"),
                         kf(B["b2"], [-3.5, 5, -1], HALF, "walk", "smile", rz=-math.pi / 4),
                         kf(S_GILLS, [-1.5, 4, -1], 0, "walk", "smile", rz=RZ)],
            },
        },
        {   # The gills: a side close-up on his neck (the slits sit ~5 studs
            # from the root toward the head), then a medium with the
            # bubbles streaming up.
            "id": "gills", "location": "undersea", "skyColor": "#1D6FB8",
            "startFrame": S_GILLS, "endFrame": S_GUIDE,
            "fx": bubbles_fx,
            "cameraShots": cover(S_GILLS, S_GUIDE, [
                lambda a, b: shot(a, b, [3.5, 4.6, 6.5], [4, 4.6, 6],
                                  [3.5, 4.4, -1], [4, 4.4, -1], 44),
                lambda a, b: _swim_cam(a, b, -0.5, 2.0),
            ]),
            "characters": {
                "hero": [kf(S_GILLS, [-1.5, 4, -1], 0, "walk", "smile", rz=RZ),
                         kf(B["b4"], [0.5, 4, -1], 0, "walk", "laugh", rz=RZ),
                         kf(S_GUIDE, [2, 4, -1], 0, "walk", "smile", rz=RZ)],
            },
        },
        {   # The tour: the fish swims in from the left and leads him
            # across the reef. Wide side view first (both in frame), then
            # a fish close-up (camera back at dist ~11 so the fish fits),
            # then a following medium and a low up-angle on the swimmer.
            "id": "guide", "location": "undersea", "skyColor": "#1D6FB8",
            "startFrame": S_GUIDE, "endFrame": S_LIMIT,
            "fx": bubbles_fx + fish_fx,
            "cameraShots": cover(S_GUIDE, S_LIMIT, [
                lambda a, b: shot(a, b, [-4, 7.5, 11], [-3, 7.5, 10.5],
                                  [-4, 7.5, -5], [-3, 7.5, -5], 44),
                lambda a, b: shot(a, b, [3, 5.5, 24], [4, 5.5, 23],
                                  [3, 5.5, -2], [4, 5.5, -2], 58),
                lambda a, b: shot(a, b, [4.5, 6, 16], [5.5, 6, 15],
                                  [4.5, 6, -3], [5.5, 6, -3], 55),
                lambda a, b: shot(a, b, [7, 2, 12], [7.5, 2.5, 11],
                                  [7.5, 4.5, -1], [8, 4.5, -1], 50),
                lambda a, b: _swim_cam(a, b, 4.0, 5.0),
            ]),
            "characters": {
                "hero": [kf(S_GUIDE, [2, 4, -1], 0, "walk", "smile", rz=RZ),
                         kf(B["b6"], [3, 4, -1], 0, "walk", "smile", rz=RZ),
                         kf(B["b7"], [4, 4, -1], 0, "walk", "smile", rz=RZ),
                         kf(S_LIMIT, [5, 4, -1], 0, "walk", "smile", rz=RZ)],
            },
        },
        {   # The limit: one science beat (b9) — he is still swimming,
            # smiling; the turn comes in the next scene.
            "id": "limit", "location": "undersea", "skyColor": "#1D6FB8",
            "startFrame": S_LIMIT, "endFrame": S_CLIMAX,
            "fx": bubbles_fx + fish_fx,
            "cameraShots": cover(S_LIMIT, S_CLIMAX, [
                lambda a, b: _swim_cam(a, b, 5.0, 5.3),
                lambda a, b: shot(a, b, [8, 2.5, 13.5], [8.3, 2.5, 12.5],
                                  [8.3, 4.5, -1], [8.3, 4.5, -1], 54),
            ]),
            "characters": {
                "hero": [kf(S_LIMIT, [5, 4, -1], 0, "walk", "smile", rz=RZ),
                         kf(S_CLIMAX, [5.3, 4.2, -1], 0, "walk", "smile", rz=RZ)],
            },
        },
        {   # The realisation + shouts: he stops, turns upright and rises
            # toward the surface as he shouts. The shout shot is a face
            # close-up with shake; its target tracks his HEAD through the
            # rise (head at (9.0, 8.5) when tilted at w1, (5.5, 11.5)
            # upright at the surface). v1 aimed at the final upright head
            # position for the whole shot, so his face was cut at the
            # right edge during "UP!"/"AIR!".
            "id": "climax", "location": "undersea", "skyColor": "#1D6FB8",
            "startFrame": S_CLIMAX, "endFrame": S_SURFACE,
            "fx": bubbles_fx + fish_fx,
            # b10 is 4.3s — one shot would break the 3.5s max, so the
            # realisation is two shots: horizontal, then starting to rise.
            # Both are widened (dist 14-14.5, fov 55) so the fish's tail
            # keeps its margin at the left edge while it hovers high.
            "cameraShots": [
                shot(S_CLIMAX, (S_CLIMAX + B["w1"]) // 2, [8, 5, 14.5], [8, 5.2, 14],
                     [8.3, 4.8, -1], [8, 5, -1], 55),
                shot((S_CLIMAX + B["w1"]) // 2, B["w1"], [7.5, 5.5, 14.5], [7.5, 6, 14],
                     [7.8, 5, -1], [7.5, 5.5, -1], 55),
                shot(B["w1"], S_SURFACE, [9.0, 9.0, 9.5], [5.5, 12.0, 9.0],
                     [9.0, 8.5, -1], [5.5, 11.5, -1], 44, shake=0.08),
            ],
            "characters": {
                "hero": [kf(S_CLIMAX, [5.3, 4.2, -1], 0, "walk", "shocked", rz=RZ),
                         kf(B["w1"], [5.5, 5, -1], 0.3, "walk", "panic", rz=-math.pi / 4),
                         kf(B["w2"], [5.5, 5.8, -1], 0, "walk", "panic", rz=-math.pi / 8),
                         kf(S_SURFACE, [5.5, 6.5, -1], 0, "idle", "panic", rz=0)],
            },
        },
        {   # The surface: he kicks the last stretch up (b11), then waves
            # goodbye as the fish waves a fin and swims down to its reef.
            # Shot 2 is a low look-up now (camera y ~5, target y ~8.5),
            # so the bright top of frame and the light rays read as the
            # surface he is kicking toward; it is also wider (fov 55,
            # dist 12-13) so the fish stays whole on its way out.
            "id": "surface", "location": "undersea", "skyColor": "#1D6FB8",
            "startFrame": S_SURFACE, "endFrame": S_TWIST,
            "fx": bubbles_fx + fish_fx,
            "cameraShots": cover(S_SURFACE, S_TWIST, [
                lambda a, b: shot(a, b, [2, 8, 17], [3, 8, 16],
                                  [5.5, 7, -1], [5.5, 7, -1], 55),
                lambda a, b: shot(a, b, [5.5, 5.0, 13], [5.5, 5.4, 12],
                                  [5.5, 8.2, -1], [5.5, 8.5, -1], 55),
            ]),
            "characters": {
                "hero": [kf(S_SURFACE, [5.5, 6.5, -1], 0, "walk", "smile"),
                         kf(B["b12"], [5.5, 7, -1], 0, "wave", "smile"),
                         kf(S_TWIST, [5.5, 7, -1], 0, "wave", "smile")],
            },
        },
        {   # The twist: back on the beach, on his feet — and the gills
            # are still there. Standard land helpers work again here.
            "id": "twist", "location": "beach",
            "startFrame": S_TWIST, "endFrame": END,
            "cameraShots": split_shots(S_TWIST, END, [
                lambda a, b: medium(a, b, [0, 0, 0]),
                lambda a, b: close_up(a, b, [0, 0, 0]),
            ]),
            "characters": {
                "hero": hold(S_TWIST, END, [0, 0, 0], 0, "idle", "cool"),
            },
        },
    ]
