"""INTERNET SEA — "How does the internet travel under the sea?"

Science explainer, lead: CasualMan (kit `{"kit": "casualman"}`) — a friendly
guide standing on the ocean floor next to the fibre-optic cable, with an R6
kid_girl friend. The undersea location (src/environments/undersea.tsx) was
already built for this topic from the Gemini reference
(~/workspace/user/files/1000374695_1_nklo.jpg): black cable snaking across
the sand, light rays, light patches, seaweed, rocks. The reference's school
of yellow blocky fish is recreated with five 'fish' fx drifting across the
water; the light pulses are one glowing 'sphere' fx racing along the
cable's S-curve (cable_pt() reproduces the curve from undersea.tsx).

THE ONE science idea: fibre-optic cables lying on the ocean floor carry
the internet as pulses of light through tiny threads of glass — most of
the world's internet crosses the sea, not the sky. Stated plainly in b1
("doesn't fly through the sky. It swims under the sea"), b5-b6 (glass
threads, light flashing through them), b9-b10 (one cable carries millions
of videos; hundreds of cables criss-cross every ocean).

Staging notes:
- Actors stand on the sand in FRONT of the cable (z=2.5); the cable's
  S-curve crosses the stage at x≈-6..-2 (z≈+1.9..-4.3), so the hero's short
  walk (scene 3) stays parallel to it and never crosses it.
- The pulse resets at SCENE cuts only (one run per scene, t 0.333→0.50),
  never mid-shot. The pulse close-up TRACKS the pulse (_pulse_cam):
  a fixed camera let the pulse drift to the frame edge, half out.
- 2-shots of the two heroes (6.5 studs apart, ~8.7 with bodies) need a
  WIDE centred on their midpoint (-2.25 once the hero is at -5.5):
  a dist-12 medium cuts both actors in half at the frame edges
  (f01118, f01313), and a dist-17 medium is still not wide enough.
  NO low_angle shots: the low camera looks up into the fish layer and
  the fish sit on the hero's head like earmuffs (f00491, f00989).
- close_up scale=1.5 on the kit hero aims at the kit head height (6.6);
  scale=1.25 on the R6 friend aims at 5.6.
"""
import math

from shorts.scene import HALF, close_up, cover, hold, kf, medium, shot, split_shots, wide  # noqa: F401

TITLE = "THE INTERNET SWIMS UNDER THE SEA"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "q1", "text": "How does the internet travel under the sea?", "pause": 0.10},
    {"id": "b1", "text": "In this world, the internet doesn't fly through the sky. It swims under the sea.", "pause": 0.08},
    {"id": "b2", "text": "When you tap a video, it dives down, into a giant cable on the ocean floor.", "pause": 0.08},
    {"id": "b3", "text": "A thick black cable, snaking across the sand, from one continent to another.", "pause": 0.08},
    {"id": "b4", "text": "It stretches for thousands of kilometres, across the whole ocean.", "pause": 0.08},
    {"id": "b5", "text": "Inside the cable, there is no water. There are tiny threads of glass.", "pause": 0.08},
    {"id": "b6", "text": "And your video travels as light, flashing through the glass.", "pause": 0.08},
    {"id": "b7", "text": "The light blinks on and off, billions of times a second.", "pause": 0.08},
    {"id": "b8", "text": "Each blink is a piece of your video, your game, your message.", "pause": 0.08},
    {"id": "b9", "text": "One thin cable carries millions of videos, all at the same time.", "pause": 0.08},
    {"id": "b10", "text": "And hundreds of cables criss-cross every ocean on Earth.", "pause": 0.08},
    {"id": "w1", "text": "LIGHT!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "GLASS!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "SEA!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b11", "text": "So the next time your video loads in a second, thank a thread of glass under the sea.", "pause": 0.08},
    {"id": "b12", "text": "But the cable has no fence, no guard. Just sand, seaweed, and a little fish, swimming right over it.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05,
         "dropouts": [("b10+0.3", "w3.end")]}
SFX = [
    ("q1", "whoosh"),
    ("b1", "whoosh"),
    ("b2+0.5", "bubbles"),
    ("b3+0.4", "pop", {"f": 700}),
    ("b4+0.5", "bell_low"),
    ("b5+0.4", "sparkle"),
    ("b6+0.4", "sparkle"),
    ("b7+0.5", "pop", {"f": 800}),
    ("b8+0.5", "pop", {"f": 650}),
    ("b9+0.5", "sparkle"),
    ("b10+0.3", "riser", {"dur": 1.6}),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b11+0.5", "sparkle"),
    ("b12+1.5", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
CAST = {
    # Lead: CasualMan, the kit character — NOT Bolt Boy (lead variety).
    "hero": {"kit": "casualman"},
    "friend": {"extends": "kid_girl", "hair": {"style": "pigtails", "color": "brown"},
               "top": {"style": "tshirt", "color": "teal", "secondary": "white"},
               "bottom": {"style": "shorts", "color": "denim"},
               "shoes": {"color": "white", "sole": "white"}},
}


# 4. SCENES --------------------------------------------------------------------
HERO_P = [-4, 0, 2.5]       # hero start: on the sand, just in front of the cable
HERO_LEFT = [-5.5, 0, 2.5]  # hero after his short walk along the cable
FRIEND_P = [1, 0, 2.5]      # 5.0 studs from HERO_P, 6.5 from HERO_LEFT


def cable_pt(t):
    """Point on the cable's S-curve (same formula as UnderseaEnvironment),
    y=1.4 so the pulse rides on top of the cable (cable centre y=0.6)."""
    return [-24 + 48 * t, 1.4, 6 - 22 * t + 8 * math.sin(t * math.pi * 2.2)]


def pulse_fx(a, b, radius=0.9):
    """One glowing light pulse racing along the visible cable, t 0.333
    (foreground-left) to 0.50 (receding right). Keyframes sit on the curve
    so the path follows the S, not a straight chord."""
    ts = [0.333, 0.375, 0.40, 0.4375, 0.479, 0.50]
    kfs = []
    for i, t in enumerate(ts):
        f = a + round((b - a) * i / (len(ts) - 1))
        kfs.append({"frame": f, "position": cable_pt(t)})
    return [{"id": "pulse", "shape": "sphere", "radius": radius, "color": "#FEF9C3",
             "emissive": "#FDE047", "emissiveIntensity": 2.5, "roughness": 0.4,
             "keyframes": kfs}]


# The school of yellow blocky fish (the Gemini reference's school):
# five fish, staggered, drifting slowly +x so they are still over the
# cable for the twist. fish_x(f): -8 at frame 0, +6 at END.
FISH = [  # (x offset, y, z, scale, color)
    (0, 9.0, -6.0, 1.0, "#FACC15"),
    (-3.5, 10.5, -8.0, 0.8, "#FDE047"),
    (-6, 7.5, -5.0, 0.9, "#FBBF24"),
    (2.5, 11.0, -7.0, 0.7, "#FACC15"),
    (5, 8.5, -9.0, 1.1, "#FDE047"),
]


def fish_fx(a, b, end):
    out = []
    for i, (ox, y, z, sc, col) in enumerate(FISH):
        x0 = -8 + ox + 14 * (a / end)
        x1 = -8 + ox + 14 * (b / end)
        out.append({"id": f"fish{i}", "shape": "fish", "scale": sc, "color": col,
                    "rotation": [0, HALF, 0],
                    "keyframes": [{"frame": a, "position": [x0, y, z]},
                                  {"frame": b, "position": [x1, y, z]}]})
    return out


def _pulse_cam(a, b, s0, s1):
    """Camera that TRACKS the light pulse: aims at the pulse's position at
    the shot's midpoint (the pulse runs t 0.333→0.50 across [s0, s1]).
    A fixed camera let the pulse drift to the frame edge, half out of
    frame (f00667), with the cable filling the shot as a black wall."""
    mid = (a + b) / 2
    frac = (mid - s0) / max(1, (s1 - s0))
    px, py, pz = cable_pt(0.333 + frac * (0.50 - 0.333))
    return shot(a, b, [px, py + 2.6, pz + 9.5], [px, py + 2.6, pz + 9.0],
                [px, py, pz], [px, py, pz], 50)


def bubbles_fx(a, b, hero_x):
    """Small breath-bubble column just in front of the hero (scale 0.4:
    spans y 0.48-3.84, clear of the sand)."""
    return [{"id": "bubbles", "shape": "bubbles", "scale": 0.4, "color": "#c4efff",
             "keyframes": [{"frame": a, "position": [hero_x, 1.8, 3.0]},
                           {"frame": b, "position": [hero_x, 1.8, 3.0]}]}]


def scenes(T):
    B, E, END = T.B, T.E, T.END
    S_B1 = B["b1"] - 1    # hook -> setup
    S_B3 = B["b3"] - 1    # setup -> the cable
    S_B5 = B["b5"] - 1    # cable -> glass threads (pulse enters)
    S_B7 = B["b7"] - 1    # glass -> blinking light
    S_B9 = B["b9"] - 1    # blinks -> scale
    S_W1 = B["w1"] - 1    # scale -> shouts
    S_B11 = B["b11"] - 1  # shouts -> payoff
    S_B12 = B["b12"] - 1  # payoff -> twist

    return [
        {   # The hook: the big "How...?" question over a wide of the
            # seabed — both heroes on the sand, the black cable snaking
            # past them, the fish school drifting in from the left.
            "id": "hook", "location": "undersea", "skyColor": "#1D6FB8",
            "startFrame": 0, "endFrame": S_B1,
            "fx": fish_fx(0, S_B1, END) + bubbles_fx(0, S_B1, -4),
            # wide() centred on the heroes' midpoint (-1.5 while the hero
            # is at -4): the custom fov-55 push cut the friend in half at
            # the right edge (f00031).
            "cameraShots": [wide(0, S_B1, [-1.5, 0, 1])],
            "characters": {
                "hero": hold(0, S_B1, HERO_P, 0.3, "idle", "smile"),
                "friend": hold(0, S_B1, FRIEND_P, -0.3, "idle", "smile"),
            },
        },
        {   # The setup: it doesn't fly through the sky — it swims.
            # The hero points at the cable; the friend turns shocked as
            # the video "dives down" into it.
            "id": "setup", "location": "undersea", "skyColor": "#1D6FB8",
            "startFrame": S_B1, "endFrame": S_B3,
            "fx": fish_fx(S_B1, S_B3, END) + bubbles_fx(S_B1, S_B3, -4),
            "cameraShots": cover(S_B1, S_B3, [
                lambda a, b: medium(a, b, HERO_P),
                lambda a, b: close_up(a, b, HERO_P, scale=1.5),
                lambda a, b: wide(a, b, [-1.5, 0, 1]),
            ]),
            "characters": {
                "hero": [kf(S_B1, HERO_P, 0.5, "point", "smile"),
                         kf(S_B3, HERO_P, 0.5, "point", "smile")],
                "friend": [kf(S_B1, FRIEND_P, -0.3, "idle", "smile"),
                           kf(B["b2"], FRIEND_P, -0.3, "idle", "shocked"),
                           kf(S_B3, FRIEND_P, -0.3, "idle", "shocked")],
            },
        },
        {   # The cable: a thick black cable, snaking across the sand.
            # The hero strolls a few studs left along it (parallel, never
            # crossing) and stops, shocked at how far it stretches.
            "id": "cable", "location": "undersea", "skyColor": "#1D6FB8",
            "startFrame": S_B3, "endFrame": S_B5,
            "fx": fish_fx(S_B3, S_B5, END) + bubbles_fx(S_B3, S_B5, -5.5),
            "cameraShots": cover(S_B3, S_B5, [
                lambda a, b: wide(a, b, [-2.25, 0, 1]),
                lambda a, b: medium(a, b, HERO_LEFT),
                lambda a, b: close_up(a, b, HERO_LEFT, scale=1.5),
            ]),
            "characters": {
                "hero": [kf(S_B3, HERO_P, -HALF, "walk", "smile"),
                         kf(B["b4"], HERO_LEFT, -HALF, "walk", "smile"),
                         kf(B["b4"] + 6, HERO_LEFT, 0, "idle", "shocked"),
                         kf(S_B5, HERO_LEFT, 0, "idle", "shocked")],
                "friend": [kf(S_B3, FRIEND_P, -0.3, "idle", "shocked"),
                           kf(S_B5, FRIEND_P, -0.3, "idle", "shocked")],
            },
        },
        {   # Glass threads: the light pulse enters and races along the
            # cable — your video, travelling as light through glass.
            "id": "glass", "location": "undersea", "skyColor": "#1D6FB8",
            "startFrame": S_B5, "endFrame": S_B7,
            "fx": fish_fx(S_B5, S_B7, END) + bubbles_fx(S_B5, S_B7, -5.5)
                + pulse_fx(S_B5, S_B7),
            "cameraShots": cover(S_B5, S_B7, [
                lambda a, b: wide(a, b, [-2.25, 0, 1]),
                # pulse close-up TRACKS the pulse (see _pulse_cam)
                lambda a, b: _pulse_cam(a, b, S_B5, S_B7),
                lambda a, b: medium(a, b, HERO_LEFT),
            ]),
            "characters": {
                "hero": [kf(S_B5, HERO_LEFT, 0.5, "point", "smile"),
                         kf(B["b6"], HERO_LEFT, 0.5, "point", "laugh"),
                         kf(S_B7, HERO_LEFT, 0.5, "point", "laugh")],
                "friend": [kf(S_B5, FRIEND_P, -0.3, "idle", "shocked"),
                           kf(S_B7, FRIEND_P, -0.3, "idle", "shocked")],
            },
        },
        {   # Blinking light: billions of blinks a second — each blink a
            # piece of your video, game, message. Second pulse run.
            "id": "blinks", "location": "undersea", "skyColor": "#1D6FB8",
            "startFrame": S_B7, "endFrame": S_B9,
            "fx": fish_fx(S_B7, S_B9, END) + bubbles_fx(S_B7, S_B9, -5.5)
                + pulse_fx(S_B7, S_B9),
            "cameraShots": cover(S_B7, S_B9, [
                lambda a, b: medium(a, b, HERO_LEFT),
                lambda a, b: wide(a, b, [-2.25, 0, 1]),
                lambda a, b: close_up(a, b, FRIEND_P, scale=1.25),
            ]),
            "characters": {
                "hero": [kf(S_B7, HERO_LEFT, 0, "idle", "shocked"),
                         kf(B["b8"], HERO_LEFT, 0, "idle", "laugh"),
                         kf(S_B9, HERO_LEFT, 0, "idle", "laugh")],
                "friend": [kf(S_B7, FRIEND_P, -0.3, "idle", "shocked"),
                           kf(B["b8"], FRIEND_P, -0.3, "idle", "smile"),
                           kf(S_B9, FRIEND_P, -0.3, "idle", "smile")],
            },
        },
        {   # Scale: one cable carries millions of videos; hundreds of
            # cables criss-cross every ocean. Bigger pulse, both celebrate.
            "id": "scale", "location": "undersea", "skyColor": "#1D6FB8",
            "startFrame": S_B9, "endFrame": S_W1,
            "fx": fish_fx(S_B9, S_W1, END) + bubbles_fx(S_B9, S_W1, -5.5)
                + pulse_fx(S_B9, S_W1, radius=0.9),
            "cameraShots": cover(S_B9, S_W1, [
                lambda a, b: wide(a, b, [-2.25, 0, 1]),
                lambda a, b: close_up(a, b, HERO_LEFT, scale=1.5),
                lambda a, b: medium(a, b, HERO_LEFT),
            ]),
            "characters": {
                "hero": [kf(S_B9, HERO_LEFT, 0, "idle", "laugh"),
                         kf(B["b10"], HERO_LEFT, 0, "celebrate", "laugh"),
                         kf(S_W1, HERO_LEFT, 0, "celebrate", "laugh")],
                "friend": [kf(S_B9, FRIEND_P, -0.3, "idle", "smile"),
                           kf(B["b10"], FRIEND_P, -0.3, "celebrate", "laugh"),
                           kf(S_W1, FRIEND_P, -0.3, "celebrate", "laugh")],
            },
        },
        {   # The shouts: LIGHT! GLASS! SEA! — one WIDE shot with shake
            # (the three shouts total ~2s; per-shout cuts would break the
            # 1.0s shot minimum). Wide geometry centred on the heroes'
            # midpoint (-2.25): a dist-12 medium cut BOTH actors in half
            # at the frame edges (f01118). The pulse races one last time.
            "id": "climax", "location": "undersea", "skyColor": "#1D6FB8",
            "startFrame": S_W1, "endFrame": S_B11,
            "fx": fish_fx(S_W1, S_B11, END) + bubbles_fx(S_W1, S_B11, -5.5)
                + pulse_fx(S_W1, S_B11),
            "cameraShots": [
                shot(S_W1, S_B11, [-2.25, 7.4, 21], [-2.25, 7.0, 18.5],
                     [-2.25, 4.8, 0], [-2.25, 4.7, 0], 58, shake=0.08),
            ],
            "characters": {
                "hero": [kf(S_W1, HERO_LEFT, 0.5, "point", "shocked"),
                         kf(S_B11, HERO_LEFT, 0.5, "point", "shocked")],
                "friend": [kf(S_W1, FRIEND_P, -0.3, "point", "shocked"),
                           kf(S_B11, FRIEND_P, -0.3, "point", "shocked")],
            },
        },
        {   # The payoff: thank a thread of glass under the sea. Both
            # wave; the pulse glows slow near the cable's near end.
            "id": "payoff", "location": "undersea", "skyColor": "#1D6FB8",
            "startFrame": S_B11, "endFrame": S_B12,
            "fx": fish_fx(S_B11, S_B12, END) + bubbles_fx(S_B11, S_B12, -5.5)
                + [{"id": "pulse", "shape": "sphere", "radius": 0.9, "color": "#FEF9C3",
                    "emissive": "#FDE047", "emissiveIntensity": 2.5, "roughness": 0.4,
                    "keyframes": [{"frame": S_B11, "position": cable_pt(0.375)},
                                  {"frame": S_B12, "position": cable_pt(0.40)}]}],
            "cameraShots": cover(S_B11, S_B12, [
                lambda a, b: wide(a, b, [-2.25, 0, 1]),
                lambda a, b: medium(a, b, HERO_LEFT),
            ]),
            "characters": {
                "hero": [kf(S_B11, HERO_LEFT, 0, "wave", "smile"),
                         kf(S_B12, HERO_LEFT, 0, "wave", "smile")],
                "friend": [kf(S_B11, FRIEND_P, -0.3, "wave", "smile"),
                           kf(S_B12, FRIEND_P, -0.3, "wave", "smile")],
            },
        },
        {   # The twist: no fence, no guard — just sand, seaweed, and a
            # little fish swimming right over it. Elevated wide catches
            # the school above the cable, then a cool close-up on the hero.
            "id": "twist", "location": "undersea", "skyColor": "#1D6FB8",
            "startFrame": S_B12, "endFrame": END,
            "fx": fish_fx(S_B12, END, END) + bubbles_fx(S_B12, END, -5.5)
                + [{"id": "pulse", "shape": "sphere", "radius": 0.9, "color": "#FEF9C3",
                    "emissive": "#FDE047", "emissiveIntensity": 2.5, "roughness": 0.4,
                    "keyframes": [{"frame": S_B12, "position": cable_pt(0.375)},
                                  {"frame": END, "position": cable_pt(0.375)}]}],
            "cameraShots": split_shots(S_B12, END, [
                # wide() centred on the heroes' midpoint, fov 60 for
                # margin: the custom elevated shot cut BOTH actors in half
                # at the frame edges (f01313).
                lambda a, b: wide(a, b, [-2.25, 0, 1], dist=20, fov=60),
                lambda a, b: close_up(a, b, HERO_LEFT, scale=1.5),
            ]),
            "characters": {
                "hero": [kf(S_B12, HERO_LEFT, 0, "idle", "cool"),
                         kf(END, HERO_LEFT, 0, "idle", "cool")],
                "friend": [kf(S_B12, FRIEND_P, -0.3, "idle", "smile"),
                           kf(END, FRIEND_P, -0.3, "idle", "smile")],
            },
        },
    ]
