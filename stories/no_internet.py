"""NO INTERNET — "What if the internet disappeared for a day?"

Science explainer, lead: Sam, the CasualMan kit character
(cast as `{"kit": "casualman"}` — NOT Bolt Boy, varying the lead).
Max (R6 kid_boy, his established spiky-blue-hair / red-hoodie look)
is the friend; a teacher and a grandpa passerby fill the other beats.

The one science idea: the internet is a network of networks — your
message hops from your phone to a router, then through cables to a
server far away. No internet means no hopping, so the message has
nowhere to go. A day without it shows what breaks (videos, maps,
homework help) and what doesn't (the playground, your friends).

ASSETS (built for this story, 2026-11-23 — no blank screen existed
in the engine; the living-room TV glows blue and the bedroom monitor
glows green, both lit, which would contradict "every screen goes
black"):
- 'blank-phone' fx (BlankPhone — big blocky phone, dead-black screen,
  month-props doc prompt 14): the through-line visual, bedroom + street.
- 'blank-monitor' fx (BlankMonitor — desktop monitor, dead-black
  screen): on a student desk in the second classroom scene, for the
  "no search, no homework help" beat.

Filmable-limits notes (honest):
- The phone taps cannot be shown literally (no finger-tap on a screen).
  The beat is Sam 'point'ing at the giant blank phone + his shocked
  face; the narration carries the tapping.
- The message hopping cannot be shown literally (no packets, no cables
  in the classroom). The classroom board carries
  "PHONE → ROUTER / CABLES → SERVER / NO HOP = NO MESSAGE" and the
  teacher points at it; the narration carries the hopping.
- The video that will not play cannot be shown literally (no video
  player). The board carries "VIDEO WILL NOT PLAY" and the dead
  monitor on the student desk carries the visual.
- The map failing cannot be shown literally (no map UI). The beat is
  Sam asking a real person — the grandpa points the way, with a chat
  bubble ("Two blocks that way!").

Locations: 'bedroom' (hook — Sam wakes to a dead phone; framed tight
on the left side so the desk's glowing monitor at x 7.4 stays OUT of
frame), 'street' (the phone), 'classroom' (network board, then the
dead-monitor board), 'crossroads' (directions), 'playground'
(shouts + the turn), 'street' (outro).

Kit-head note: CasualMan's head is at y 6.6 (R6 is 5.6), so close-ups
on Sam use close_up(..., scale=1.5) to aim at 6.6. Kit anims used here
(idle / point / celebrate / wave) all map to real kit clips; no
sleep / knocked / panting / sit for Sam (those fall back to idle).

Build (run the previews serially — do NOT run make_short.py alongside
other stories):
    python scripts/make_short.py stories/no_internet.py --stills
"""
import math  # noqa: F401

from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, split_shots, wide  # noqa: F401

TITLE = "NO INTERNET FOR A DAY"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b0", "text": "What if the internet disappeared for a day?", "pause": 0.10},
    {"id": "b1", "text": "In this town, one morning, every screen goes black. No videos, no messages, nothing loads.", "pause": 0.08},
    {"id": "b2", "text": "Sam taps his phone again and again. The screen stays black and blank.", "pause": 0.08},
    {"id": "b3", "text": "The internet is a network of networks. Your message hops from your phone to a router, then through cables to a server far away.", "pause": 0.08},
    {"id": "b4", "text": "No internet means no hopping. The message has nowhere to go.", "pause": 0.08},
    {"id": "b5", "text": "At school, the lesson is a video that will not play.", "pause": 0.08},
    {"id": "b6", "text": "Homework help is gone too. No search, no answers in one click.", "pause": 0.08},
    {"id": "b7", "text": "Maps stop working. Sam has to ask a real person for directions.", "pause": 0.10},
    {"id": "w1", "text": "THE!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "INTERNET!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "DOWN!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b8", "text": "But look — the swings still swing, the ball still bounces, and your friends are still right here.", "pause": 0.08},
    {"id": "b9", "text": "The internet connects the world. But you are already connected to the people right next to you.", "pause": 0.10},
    {"id": "b10", "text": "Tomorrow the internet comes back. But today, the world kept spinning.", "pause": 0.10},
    {"id": "b11", "text": "What would YOU miss most for a day? Tell us below.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05,
         "dropouts": [("b7.end-0.5", "w3.end")]}
SFX = [
    ("b0", "whoosh"),
    ("b1+1.0", "pop_down"),
    ("b2+0.4", "pop", {"f": 600}),
    ("b2+1.2", "pop", {"f": 700}),
    ("b3+0.5", "pop", {"f": 600}),
    ("b3+1.8", "pop", {"f": 720}),
    ("b3+3.2", "pop", {"f": 860}),
    ("b4+0.5", "pop_down"),
    ("b5+0.4", "pop_down"),
    ("b6+0.5", "pop", {"f": 600}),
    ("b7+0.8", "sparkle"),
    ("b7.end-0.6", "riser", {"dur": 1.6}),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b8+0.5", "sparkle"),
    ("b9+0.5", "sparkle"),
    ("b11+1.0", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
CAST = {
    # Sam leads this one — the CasualMan kit character (NOT Bolt Boy).
    "hero": {"kit": "casualman"},
    # Max, the friend (his established no_friction look).
    "friend": {"extends": "kid_boy", "hair": {"style": "spikyAnime", "color": "blue"},
               "top": {"style": "hoodie", "color": "red", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"},
               "shoes": {"color": "white", "sole": "white"}},
    "teacher": {"extends": "teacher"},
    "walker": "grandpa",
}


# 4. SCENES --------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END
    S_PHONE = B["b2"] - 1    # street: the dead phone
    S_NET = B["b3"] - 1      # classroom: the network board
    S_CLASS2 = B["b5"] - 1   # classroom: video won't play / no search
    S_MAPS = B["b7"] - 1     # crossroads: asking directions
    S_PLAY = B["w1"] - 1     # playground: shouts + the turn
    S_OUT = B["b9"] - 1      # street: outro

    # The giant blank phone. Bedroom: centre [3.2, 3.2, -1.5] — clear of
    # the bed (back-left, x -7) and of the desk (back-right, x 7.4, whose
    # monitor glows green and must stay out of frame). Street: [2.5, 3.2, 0].
    def _phone(a, b, pos):
        return [{"id": "phone", "shape": "blank-phone", "scale": 1.0, "color": "#1F2937",
                 "keyframes": [{"frame": a, "position": pos},
                               {"frame": b, "position": pos}]}]

    # The dead monitor on a student desk (classroom scene 2). Desk top is
    # y ~2.3; at scale 0.6 the unit is 2.5 tall with its base 1.62 below
    # centre, so centre y 3.9 rests the base on the desk.
    def _monitor(a, b):
        return [{"id": "monitor", "shape": "blank-monitor", "scale": 0.6, "color": "#0F172A",
                 "keyframes": [{"frame": a, "position": [5.5, 3.9, 0.5]},
                               {"frame": b, "position": [5.5, 3.9, 0.5]}]}]

    HERO_P = [-2.5, 0, 1.0]
    PHONE_BED = [3.2, 3.2, -1.5]
    PHONE_STREET = [2.5, 3.2, 0]

    return [
        {   # Hook: the big question, then the setup — Sam wakes to a dead
            # phone. NO wide here: a bedroom wide would show the desk's
            # glowing green monitor at x 7.4, contradicting "every screen
            # goes black". Medium + phone close-up only, framed so the desk
            # (x >= 4.8) stays out of frame (medium dist 16 spans about
            # x -3.7..4.7 at target depth). The middle shot is a straight-on
            # close-up of the dead phone screen — NOT a close-up on Sam:
            # Sam faces the phone (away from the +z camera), so close_up
            # on him shows the back of his head.
            "id": "hook", "location": "bedroom",
            "startFrame": 0, "endFrame": S_PHONE,
            "cameraShots": cover(0, S_PHONE, [
                lambda a, b: medium(a, b, [0.5, 0, -0.2], dist=16),
                lambda a, b: shot(a, b, [3.2, 3.6, 6.2], [3.2, 3.4, 5.5],
                                  [3.2, 3.2, -1.5], [3.2, 3.2, -1.5], 44),
            ]),
            "fx": _phone(0, S_PHONE, PHONE_BED),
            "characters": {
                "hero": [kf(0, HERO_P, face(HERO_P, PHONE_BED), "idle", "shocked"),
                         kf(B["b1"], HERO_P, face(HERO_P, PHONE_BED), "point", "shocked"),
                         kf(S_PHONE, HERO_P, face(HERO_P, PHONE_BED), "point", "shocked")],
            },
        },
        {   # The phone: Sam taps it again and again on Main St. The giant
            # blank phone stands beside him; he points at its dead screen.
            "id": "phone", "location": "street",
            "startFrame": S_PHONE, "endFrame": S_NET,
            # Medium pulled back to dist 16: at dist 12 the half-width
            # (~2.8) put Sam (-2.5) half out of the left edge and cropped
            # half the phone. At dist 16 both fit whole. NO close_up here:
            # Sam faces the phone (away from the +z camera), so a close-up
            # on him would show the back of his head.
            "cameraShots": cover(S_PHONE, S_NET, [
                lambda a, b: wide(a, b, [0, 0, 0.5]),
                lambda a, b: medium(a, b, [0.2, 0, 0.5], dist=16),
            ]),
            "fx": _phone(S_PHONE, S_NET, PHONE_STREET),
            "characters": {
                "hero": hold(S_PHONE, S_NET, HERO_P, face(HERO_P, PHONE_STREET), "point", "shocked"),
            },
        },
        {   # The network: the teacher explains at the board — the hops.
            "id": "network", "location": "classroom",
            "boardText": ["PHONE → ROUTER", "CABLES → SERVER", "NO HOP = NO MESSAGE"],
            "startFrame": S_NET, "endFrame": S_CLASS2,
            "cameraShots": cover(S_NET, S_CLASS2, [
                lambda a, b: wide(a, b, [-0.25, 0, 0], dist=24),
                lambda a, b: medium(a, b, [0, 0, 1.5]),
                lambda a, b: close_up(a, b, [-2.5, 0, 1.5], scale=1.5),
            ]),
            "characters": {
                "teacher": [kf(S_NET, [-5.5, 0, -2], face([-5.5, 0, -2], [0, 0, 1.5]), "idle", "smile"),
                            kf(B["b3"] + 30, [-5.5, 0, -2], face([-5.5, 0, -2], [0, 0, 1.5]), "point", "smile"),
                            kf(S_CLASS2, [-5.5, 0, -2], face([-5.5, 0, -2], [0, 0, 1.5]), "idle", "smile")],
                "hero": hold(S_NET, S_CLASS2, [-2.5, 0, 1.5], 0, "idle", "smile"),
                "friend": hold(S_NET, S_CLASS2, [2.5, 0, 1.5], 0, "idle", "smile"),
            },
        },
        {   # The dead lesson: the video will not play, and there is no
            # search. The blank monitor sits on the right-hand student
            # desk; the third shot is a close-up on its dead screen,
            # landing on b6 ("No search...").
            "id": "lesson", "location": "classroom",
            "boardText": ["VIDEO WILL NOT PLAY", "NO SEARCH TODAY"],
            "startFrame": S_CLASS2, "endFrame": S_MAPS,
            # The monitor close-up is shot from an angle (+x): straight-on,
            # Max at [2.5, 0, 1.5] stands between the camera and the monitor
            # and blocks its left edge. From [7.0, 4.6, 9.0] he falls out
            # of frame.
            "cameraShots": split_shots(S_CLASS2, S_MAPS, [
                lambda a, b: wide(a, b, [-0.25, 0, 0], dist=24),
                lambda a, b: medium(a, b, [0, 0, 1.5]),
                lambda a, b: shot(a, b, [7.0, 4.6, 9.0], [6.9, 4.4, 8.6],
                                  [5.5, 3.9, 0.5], [5.5, 3.9, 0.5], 50),
            ]),
            "fx": _monitor(S_CLASS2, S_MAPS),
            "characters": {
                "teacher": hold(S_CLASS2, S_MAPS, [-5.5, 0, -2], face([-5.5, 0, -2], [0, 0, 1.5]), "idle", "deadpan"),
                "hero": hold(S_CLASS2, S_MAPS, [-2.5, 0, 1.5], 0, "idle", "shocked"),
                "friend": hold(S_CLASS2, S_MAPS, [2.5, 0, 1.5], 0, "idle", "shocked"),
            },
        },
        {   # The directions: maps are dead, so Sam asks a real person.
            # The grandpa points the way, with a chat bubble.
            "id": "maps", "location": "crossroads",
            "startFrame": S_MAPS, "endFrame": S_PLAY,
            # Third shot is a close-up on the GRANDPA, shot from the
            # NORTHWEST with an explicit shot(): the grandpa faces west
            # (toward Sam), so close_up — whose camera always sits due
            # south (+z) of its target — shows the BACK of his head (his
            # white horseshoe hair; verified in the f902 still). From the
            # northwest his face is visible in 3/4. Sam sits behind the
            # grandpa from this angle, not between camera and subject.
            "cameraShots": split_shots(S_MAPS, S_PLAY, [
                lambda a, b: wide(a, b, [1, 0, 0]),
                lambda a, b: medium(a, b, [1, 0, 0], dist=15),
                lambda a, b: shot(a, b, [-1.0, 6.2, -5.5], [-0.8, 6.0, -5.0],
                                  [3.5, 5.4, -1.5], [3.5, 5.4, -1.5], 44),
            ]),
            "characters": {
                "hero": [kf(S_MAPS, [-1.5, 0, 0.5], face([-1.5, 0, 0.5], [3.5, 0, -1.5]), "idle", "shocked"),
                         kf(B["b7"] + 30, [-1.5, 0, 0.5], face([-1.5, 0, 0.5], [3.5, 0, -1.5]), "point", "shocked"),
                         kf(S_PLAY, [-1.5, 0, 0.5], face([-1.5, 0, 0.5], [3.5, 0, -1.5]), "point", "smile")],
                "walker": [kf(S_MAPS, [3.5, 0, -1.5], face([3.5, 0, -1.5], [-1.5, 0, 0.5]), "idle", "smile"),
                           kf(B["b7"] + 20, [3.5, 0, -1.5], face([3.5, 0, -1.5], [-1.5, 0, 0.5]), "point", "smile",
                              bubble="Two blocks that way!"),
                           kf(S_PLAY, [3.5, 0, -1.5], face([3.5, 0, -1.5], [-1.5, 0, 0.5]), "point", "smile",
                              bubble="Two blocks that way!")],
            },
        },
        {   # The turn: the shouts, then the playground still works. The
            # first shot is a close-up with shake over all three shout
            # words; then Sam celebrates and Max dances.
            "id": "playground", "location": "playground",
            "startFrame": S_PLAY, "endFrame": S_OUT,
            "cameraShots": split_shots(S_PLAY, S_OUT, [
                lambda a, b: close_up(a, b, [-2.5, 0, 1.0], scale=1.5, shake=0.08),
                lambda a, b: medium(a, b, [0, 0, 1.0]),
                lambda a, b: wide(a, b, [0, 0, 1.0]),
            ]),
            "characters": {
                "hero": [kf(S_PLAY, [-2.5, 0, 1.0], 0, "point", "shocked"),
                         kf(B["b8"], [-2.5, 0, 1.0], 0, "celebrate", "laugh"),
                         kf(S_OUT, [-2.5, 0, 1.0], 0, "celebrate", "laugh")],
                "friend": [kf(S_PLAY, [2.5, 0, 1.0], 0, "idle", "shocked"),
                           kf(B["b8"], [2.5, 0, 1.0], 0, "dance", "laugh"),
                           kf(S_OUT, [2.5, 0, 1.0], 0, "dance", "laugh")],
            },
        },
        {   # Outro: the takeaway, the closing line, and the question.
            # The outro medium was pulled back to dist 17 (friction
            # lesson): at dist 12 the half-width shrinks to ~2.8 while
            # Sam and Max stand at ±2.5, so BOTH faces were cropped at
            # the frame edges. At dist 17 the half-width is ~4.4 and
            # both faces stay whole.
            "id": "outro", "location": "street",
            "startFrame": S_OUT, "endFrame": END,
            "cameraShots": cover(S_OUT, END, [
                lambda a, b: wide(a, b, [0, 0, 0.5], dist=18),
                lambda a, b: medium(a, b, [0, 0, 0.5], dist=17),
                lambda a, b: close_up(a, b, [-2.5, 0, 0.5], scale=1.5),
            ]),
            "characters": {
                "hero": [kf(S_OUT, [-2.5, 0, 0.5], 0, "idle", "smile"),
                         kf(B["b11"], [-2.5, 0, 0.5], 0, "wave", "laugh"),
                         kf(END, [-2.5, 0, 0.5], 0, "wave", "laugh")],
                "friend": [kf(S_OUT, [2.5, 0, 0.5], 0, "idle", "smile"),
                           kf(B["b11"], [2.5, 0, 0.5], 0, "wave", "laugh"),
                           kf(END, [2.5, 0, 0.5], 0, "wave", "laugh")],
            },
        },
    ]
