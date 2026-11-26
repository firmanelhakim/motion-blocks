"""NO ELECTRICITY FOR A DAY — "What If There Was No Electricity for a Day?"

Science explainer, lead: CasualMan
(`{"kit": "casualman"}` — "Cas", the family's dad figure, ~7 studs tall,
head 6.6: kit close-ups use close_up(..., scale=1.5) and kit mediums use
explicit static_shot targets at y ~5.5-6). Max (R6 kid_boy, blue spiky
hair, royal hoodie) and Lily (R6 kid_girl, blonde ponytail, pink hoodie)
are the kids.

The one science idea, stated plainly in the narration: electricity is
power made in big power plants and carried to every home by a web of
wires called the grid. It runs the lights, the fridge, the water pumps
and the traffic lights — so a day without it shows how much we lean on
it. No moral, just the mechanism + the payoff.

Structure: hook question (b0) -> "In this town" setup (b1) -> the
blackout hits home (switch, fridge, dead phone) -> the mechanism
(classroom board: plants + grid + what it runs) -> the town goes dark
(street, night) -> the candle (living room, night — the _candle fx from
stories/_test_week2_5_props2.py, proven geometry: white box + glowing
flame + translucent glow sphere, boy at [0,0,0] with 'point') -> shouts
POWER! IS! BACK! -> lights blink on, everyone celebrates -> takeaway
-> question.

Filmable-limits notes (honest):
- The light switch has no geometry; the switch beat is Cas pointing at
  the wall + 'shocked', narration carries the clicks.
- The dead phone has no prop; the phone beat is Max centre-frame,
  deadpan, Cas pointing at him — narration carries "dead".
- The candle is fx, not a PropId (same reason as the test file: the arm
  pose cannot hold a prop upright in front, while fx places the flame
  exactly where the Gemini candle reference has it).
- `sit` is NOT used for Cas: kit characters fall back to idle for sit
  (MotionBlocksComposition.tsx). R6 `sit` is procedural and fine for Max,
  but this story never needs it.
- Kit characters are ~7 studs tall: keep kit close-ups at scale=1.5
  (head 6.6) and kit mediums as static_shot with target y ~5.5.

Build:   python scripts/make_short.py stories/no_electricity.py --stills
Render:  node scripts/render.mjs story no_electricity --port 3051
         (stills + ffmpeg; NEVER renderMedia — proven drift)
"""
import math

from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, split_shots, static_shot, wide  # noqa: F401

TITLE = "THE DAY THE POWER WENT OUT"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b0", "text": "What if there was no electricity for a day?", "pause": 0.10},
    {"id": "b1", "text": "In this town, one morning, the power just switched off.", "pause": 0.08},
    {"id": "b2", "text": "No lights. No fridge humming. No phone charging. Nothing at all.", "pause": 0.08},
    {"id": "b3", "text": "Cas taps the light switch. Click. Click. Nothing happens.", "pause": 0.08},
    {"id": "b4", "text": "In the kitchen, the fridge has gone quiet, and the ice cream is melting.", "pause": 0.08},
    {"id": "b5", "text": "Max holds up his phone. Dead. No games, no videos, no messages.", "pause": 0.08},
    {"id": "b6", "text": "But electricity is not magic. It is power, flowing through wires from far away.", "pause": 0.10},
    {"id": "b7", "text": "Big power plants make it, and a web of wires called the grid carries it to every home.", "pause": 0.10},
    {"id": "b8", "text": "It runs the lights, the fridge, the water pumps, and even the traffic lights.", "pause": 0.08},
    {"id": "b9", "text": "Without it, the whole town slows down. Shops shut, lifts stop, and the streets go dark.", "pause": 0.10},
    {"id": "b10", "text": "That night, Max lights one small candle, and its warm glow fills the room.", "pause": 0.08},
    {"id": "b11", "text": "One tiny flame, doing the job of a hundred light bulbs. Well, almost.", "pause": 0.08},
    {"id": "w1", "text": "POWER!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "IS!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "BACK!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b12", "text": "The lights blink on, and the whole town cheers.", "pause": 0.08},
    {"id": "b13", "text": "Electricity powers almost everything we do. We only notice it when it is gone.", "pause": 0.10},
    {"id": "b14", "text": "What is the first thing you would miss? Tell us below.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/moon-tide.wav",
    "under_voice": 0.022,
    "gaps": 0.05,
    "dropouts": [("b11+0.5", "w3.end")],
}

SFX = [
    ("b0", "whoosh"),
    ("b1+0.3", "pop_down"),
    ("b2+0.5", "sad"),
    ("b3+0.4", "pop", {"f": 600}),
    ("b3+1.0", "pop", {"f": 600}),
    ("b4+0.5", "pop_down"),
    ("b5+0.5", "sad"),
    ("b6+0.5", "sparkle"),
    ("b7+0.5", "pop", {"f": 600}),
    ("b8+0.5", "pop", {"f": 700}),
    ("b9+0.4", "riser", {"dur": 1.6}),
    ("b10+0.5", "sparkle"),
    ("b11+0.5", "riser", {"dur": 1.2}),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b12+0.5", "sparkle"),
    ("b13+0.5", "pop", {"f": 600}),
    ("b14+1.0", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
CAST = {
    # Cas leads: the kit CasualMan (blue shirt, dark hair + beard, ~7 studs).
    "hero": {"kit": "casualman"},
    "kid": {"extends": "kid_boy", "hair": {"style": "spikyAnime", "color": "blue"},
            "top": {"style": "hoodie", "color": "royal", "secondary": "white"},
            "bottom": {"style": "jeans", "color": "denim"},
            "shoes": {"color": "white", "sole": "white"}, "freckles": True},
    "friend": {"extends": "kid_girl", "hair": {"style": "ponytail", "color": "blonde"},
               "top": {"style": "hoodie", "color": "pink", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"},
               "shoes": {"color": "white", "sole": "white"}},
    "teacher": {"extends": "teacher"},
}


def _candle(a, b):
    """Candle (Gemini candle reference, proven geometry from
    stories/_test_week2_5_props2.py): a white candle held in front of the
    boy's chest (he uses the 'point' anim, arm forward), a glowing flame,
    and a translucent warm glow sphere. The candle is fx, not a PropId."""
    return [
        {"id": "candle-body", "shape": "box", "size": [0.35, 1.0, 0.35],
         "color": "#F8FAFC", "roughness": 0.4,
         "keyframes": [{"frame": a, "position": [-1.5, 3.8, 1.9]},
                      {"frame": b, "position": [-1.5, 3.8, 1.9]}]},
        {"id": "candle-flame", "shape": "sphere", "radius": 0.22,
         "color": "#FDE047", "emissive": "#F59E0B", "emissiveIntensity": 2.5,
         "roughness": 0.3,
         "keyframes": [{"frame": a, "position": [-1.5, 4.45, 1.9]},
                      {"frame": b, "position": [-1.5, 4.45, 1.9]}]},
        {"id": "candle-glow", "shape": "sphere", "radius": 1.2,
         "color": "#FDE68A", "emissive": "#FBBF24", "emissiveIntensity": 0.8,
         "roughness": 0.5, "opacity": 0.08,
         "keyframes": [{"frame": a, "position": [-1.5, 4.2, 1.9]},
                      {"frame": b, "position": [-1.5, 4.2, 1.9]}]},
    ]


# 4. SCENES ---------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S_SWITCH = B["b3"] - 1    # living room, day: the switch
    S_FRIDGE = B["b4"] - 1    # kitchen: the silent fridge
    S_PHONE = B["b5"] - 1     # living room, day: the dead phone
    S_CLASS = B["b6"] - 1     # classroom: plants + grid board
    S_DARK = B["b9"] - 1      # street, night: the town goes dark
    S_CANDLE = B["b10"] - 1   # living room, night: the candle
    S_BACK = B["w1"] - 1      # living room, day: POWER! IS! BACK! + closer

    HERO_P = [-5, 0, 0.5]
    KID_P = [0, 0, 0.5]
    FRIEND_P = [5, 0, 0.5]

    scenes = []

    # 1. HOOK — street, day. The question, then the setup. ----------------------
    scenes.append({
        "id": "hook", "location": "street",
        "startFrame": 0, "endFrame": S_SWITCH,
        "cameraShots": cover(0, S_SWITCH, [
            lambda a, b: wide(a, b, [0, 0, 0.5], dist=22),
            # kit close-up: head 6.6 -> scale 1.5 (h = 4.4 * 1.5)
            lambda a, b: close_up(a, b, HERO_P, scale=1.5),
            lambda a, b: close_up(a, b, KID_P),
        ]),
        "characters": {
            "hero": hold(0, S_SWITCH, HERO_P, 0.2, "point", "shocked"),
            "kid": hold(0, S_SWITCH, KID_P, -0.2, "point", "shocked"),
            "friend": hold(0, S_SWITCH, FRIEND_P, 0, "idle", "shocked"),
        },
    })

    # 2. THE SWITCH — living room, day. Cas taps the wall; nothing happens. -----
    scenes.append({
        "id": "switch", "location": "living_room", "variant": "blue",
        "startFrame": S_SWITCH, "endFrame": S_FRIDGE,
        "cameraShots": cover(S_SWITCH, S_FRIDGE, [
            # Was static [-2,6.5,13]->[-2,5.5,0] fov 50: cropped Cas at the
            # left edge AND Max at the right edge (5 studs apart, portrait
            # frame too narrow at dist 13). Pull back to 17 + fov 55.
            lambda a, b: static_shot(a, b, [-2.5, 6.5, 17], [-2.5, 5, 0], 55),
            lambda a, b: close_up(a, b, HERO_P, scale=1.5),
            lambda a, b: close_up(a, b, KID_P),
        ]),
        "characters": {
            "hero": hold(S_SWITCH, S_FRIDGE, HERO_P, 0.2, "point", "shocked"),
            "kid": hold(S_SWITCH, S_FRIDGE, KID_P, -0.2, "idle", "shocked"),
        },
    })

    # 3. THE FRIDGE — kitchen. Fridge back-left at [-11.2, 0, -6.6]; Cas
    # stands beside it, Max watches. -------------------------------------------
    scenes.append({
        "id": "fridge", "location": "kitchen", "variant": "blue",
        "startFrame": S_FRIDGE, "endFrame": S_PHONE,
        "cameraShots": cover(S_FRIDGE, S_PHONE, [
            lambda a, b: static_shot(a, b, [-3, 6, 13], [-7, 4.5, -4], 52),
            lambda a, b: close_up(a, b, [-8.5, 0, -3.0], scale=1.5),
            lambda a, b: close_up(a, b, [-3.5, 0, -2.0]),
        ], target_sec=2.0),  # 110f scene: default 2.5s target rounds to ONE 3.7s shot (>3.5s max); 2.0s -> 2 x 1.8s cuts
        "characters": {
            "hero": hold(S_FRIDGE, S_PHONE, [-8.5, 0, -3.0], 0.4, "idle", "shocked"),
            "kid": hold(S_FRIDGE, S_PHONE, [-3.5, 0, -2.0], -0.4, "idle", "shocked"),
        },
    })

    # 4. THE DEAD PHONE — living room, day. Max centre-frame, deadpan;
    # Cas points at him. No phone prop exists; narration carries "dead". ------
    scenes.append({
        "id": "phone", "location": "living_room", "variant": "blue",
        "startFrame": S_PHONE, "endFrame": S_CLASS,
        "cameraShots": cover(S_PHONE, S_CLASS, [
            lambda a, b: medium(a, b, [0, 0, 0.5], dist=12),
            lambda a, b: close_up(a, b, KID_P),
            # Same wide static as the switch scene (same room, same pair).
            lambda a, b: static_shot(a, b, [-2.5, 6.5, 17], [-2.5, 5, 0], 55),
        ]),
        "characters": {
            "hero": hold(S_PHONE, S_CLASS, HERO_P, 0.2, "point", "deadpan"),
            "kid": hold(S_PHONE, S_CLASS, KID_P, 0, "idle", "deadpan"),
        },
    })

    # 5. CLASSROOM — the mechanism. Teacher at the board with the
    # pointer_draw prop; Cas + Max in the free aisle (x in [-3, 3] is clear
    # of the student desks at x +/-5.5, +/-9.5). -------------------------------
    scenes.append({
        "id": "mechanism", "location": "classroom",
        "boardText": ["POWER PLANTS MAKE IT", "THE GRID CARRIES IT", "LIGHTS · FRIDGE · PUMPS"],
        "startFrame": S_CLASS, "endFrame": S_DARK,
        "cameraShots": cover(S_CLASS, S_DARK, [
            lambda a, b: shot(a, b, [0, 7.4, 23], [0, 7.4, 23], [0, 4.8, -1], [0, 4.8, -1], 58),
            # Was medium([-3,0,-4.5], dist 10): the camera at z=5.5 sat
            # BEHIND Cas (z=0.5), so his back + head filled the frame.
            # Angled static from the left side: Cas is well off-axis, the
            # teacher + board stay centred.
            lambda a, b: static_shot(a, b, [-7, 5.5, 2], [-3, 4.8, -4.5], 50),
            lambda a, b: medium(a, b, [1, 0, 0.5], dist=12),
        ]),
        "characters": {
            "teacher": hold(S_CLASS, S_DARK, [-3.0, 0, -4.5], 0.5, "point", "deadpan", "pointer_draw"),
            "hero": hold(S_CLASS, S_DARK, [-1.5, 0, 0.5], 0, "idle", "smile"),
            "kid": hold(S_CLASS, S_DARK, [3.5, 0, 0.5], 0, "idle", "smile"),
        },
    })

    # 6. THE TOWN GOES DARK — street, night. All three look around. ------------
    scenes.append({
        "id": "dark", "location": "street", "isNight": True,
        "startFrame": S_DARK, "endFrame": S_CANDLE,
        "cameraShots": cover(S_DARK, S_CANDLE, [
            lambda a, b: wide(a, b, [0, 0, 0.5], dist=22),
            lambda a, b: close_up(a, b, HERO_P, scale=1.5),
            lambda a, b: close_up(a, b, KID_P),
        ]),
        "characters": {
            "hero": hold(S_DARK, S_CANDLE, HERO_P, 0.2, "idle", "panic"),
            "kid": hold(S_DARK, S_CANDLE, KID_P, -0.2, "idle", "panic"),
            "friend": hold(S_DARK, S_CANDLE, FRIEND_P, 0, "idle", "panic"),
        },
    })

    # 7. THE CANDLE — living room, night. Max holds the candle out (point
    # anim + _candle fx); Cas watches from the side, smiling. -------------------
    scenes.append({
        "id": "candle", "location": "living_room", "variant": "blue", "isNight": True,
        "startFrame": S_CANDLE, "endFrame": S_BACK,
        "fx": _candle(S_CANDLE, S_BACK),
        "cameraShots": cover(S_CANDLE, S_BACK, [
            # Medium centred between Max and the candle (-1.5, 3.8, 1.9) so
            # the flame reads as held, not floating off-frame left.
            lambda a, b: medium(a, b, [-0.8, 0, 1.0], dist=11),
            # Was close_up([0,0,0], dist 7): the candle sat outside the
            # frame entirely. Aim at the candle; Max's face stays in frame
            # right of centre at dist 8.
            lambda a, b: close_up(a, b, [-1.5, 0, 1.9], dist=8),
            # Was static [-4,5,12]->[-1,4,0]: Cas half-cropped at the left
            # edge. Reframed to exclude him; the shot is Max + candle.
            lambda a, b: static_shot(a, b, [-2.5, 5, 12], [0.5, 4, 0], 50),
        ]),
        "characters": {
            "kid": [kf(S_CANDLE, [0, 0, 0], 0, "point", "smile"),
                    kf(S_BACK, [0, 0, 0], 0, "point", "smile")],
            "hero": [kf(S_CANDLE, [-5, 0, 0.5], 0.2, "idle", "smile"),
                     kf(S_BACK, [-5, 0, 0.5], 0.2, "idle", "smile")],
        },
    })

    # 8. POWER'S BACK + CLOSER — living room, day. Celebrate on the shouts,
    # then settle to smiles for the takeaway + question. ------------------------
    scenes.append({
        "id": "powerback", "location": "living_room", "variant": "blue",
        "startFrame": S_BACK, "endFrame": END,
        "cameraShots": cover(S_BACK, END, [
            lambda a, b: wide(a, b, [0, 0, 0.5], dist=20),
            lambda a, b: close_up(a, b, HERO_P, scale=1.5),
            lambda a, b: close_up(a, b, KID_P),
            lambda a, b: medium(a, b, [0, 0, 0.5], dist=12),
        ]),
        "characters": {
            "hero": [kf(S_BACK, HERO_P, 0.2, "celebrate", "laugh"),
                     kf(B["b13"], HERO_P, 0.2, "idle", "smile"),
                     kf(END, HERO_P, 0.2, "idle", "smile")],
            "kid": [kf(S_BACK, KID_P, -0.2, "celebrate", "laugh"),
                    kf(B["b13"], KID_P, -0.2, "idle", "smile"),
                    kf(END, KID_P, -0.2, "idle", "smile")],
            "friend": [kf(S_BACK, FRIEND_P, 0, "celebrate", "laugh"),
                       kf(B["b13"], FRIEND_P, 0, "idle", "smile"),
                       kf(END, FRIEND_P, 0, "idle", "smile")],
        },
    })

    return scenes
