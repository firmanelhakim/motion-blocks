"""TEST-ONLY story — verifies the four Week 1 props: Mars location, star
streaks (light speed), comet, twinkling starfield. NEVER for publishing. Run:
    python scripts/make_short.py stories/_test_week1_props.py --stills
"""
import math

from shorts.scene import (  # noqa: F401
    HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, orbit,
    shot, split_shots, static_shot, wide,
)

TITLE = "TEST WEEK1 PROPS"

BEATS = [
    {"id": "b1", "text": "In this world, Mars is red, the stars streak past, and a comet crosses the sky.", "pause": 0.08},
    {"id": "b2", "text": "The desert is red dust, and an astronaut stands on Mars.", "pause": 0.08},
    {"id": "b3", "text": "At light speed, the stars stretch into lines.", "pause": 0.08},
    {"id": "b4", "text": "A comet flies by, with a tail of ice behind it.", "pause": 0.08},
    {"id": "b5", "text": "And the stars twinkle, each one on its own time.", "pause": 0.08},
    {"id": "b6", "text": "Four new props, ready for next week.", "pause": 0.3},
]

MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05}
SFX = [
    ("b1", "whoosh"),
    ("b3+0.5", "whoosh"),
    ("b4+0.5", "sparkle"),
    ("b6+0.5", "twist"),
]

CAST = {
    "hero": {"extends": "kid_boy", "hair": {"style": "spikyAnime", "color": "blue"},
             "top": {"style": "hoodie", "color": "royal", "secondary": "white"},
             "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"color": "white", "sole": "white"},
             "freckles": True},
    "friend": {"extends": "kid_girl", "hair": {"style": "ponytail", "color": "blonde"},
               "top": {"style": "hoodie", "color": "pink", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"color": "white", "sole": "white"}},
    # White-suited astronaut (Gemini Mars reference): white pullover/pants,
    # no hair, white helmet with a dark visor (see Accessories.tsx 'helmet').
    "astronaut": {"extends": "kid_boy", "hair": {"style": "none"},
                  "top": {"style": "pullover", "color": "white", "secondary": "white"},
                  "bottom": {"style": "pants", "color": "white"},
                  "shoes": {"color": "white", "sole": "white"},
                  "accessories": [{"type": "helmet", "color": "white", "secondary": "#0F172A"}]},
}


def _streaks(a, b):
    """Radial warp streaks: 12 thin boxes around frame centre [0, 7, -18],
    each rotated to point outward and keyframed to fly outward over the shot,
    so a still reads as light-speed lines radiating from the centre. The
    centre sits high in the sky so no streak lies flat across the horizon
    behind the actors."""
    out = []
    for i in range(12):
        ang = i * (2 * math.pi / 12) + 0.13
        if abs(math.cos(ang)) < 0.35:
            continue  # skip near-horizontal streaks: they lie flat across the
            # horizon behind the actors and read as stray bars, not warp
        dx, dy = math.sin(ang), math.cos(ang)
        r0 = 3.5 + (i % 4) * 1.5
        length = 5.0 + (i % 3) * 1.5
        cx, cy = dx * r0, 7 + dy * r0
        ex, ey = dx * (r0 + 5), 7 + dy * (r0 + 5)
        out.append({"id": f"streak{i}", "shape": "box", "size": [0.35, length, 0.35],
                    "color": "#F8FAFC", "emissive": "#FFFFFF", "emissiveIntensity": 1.6,
                    "roughness": 0.4, "rotation": [0, 0, ang],
                    "keyframes": [{"frame": a, "position": [cx, cy, -18]},
                                  {"frame": b, "position": [ex, ey, -18]}]})
    return out


def _comet(a, b):
    """Comet crossing the sky left to right (Gemini reference): a faceted icy
    head + a tail of thin white/blue streaks trailing behind it, all tracking
    the same keyframe timing (moon-crater pattern). The streaks are thin
    rotated boxes (same technique as the star streaks), in three lanes sloping
    gently down behind the head, fading with distance. A small blue cube
    planet sits low at the right, as in the reference."""
    head_kf = [{"frame": a, "position": [-25, 14, -20]}, {"frame": b, "position": [25, 16, -20]}]
    fx = [{"id": "comet-head", "shape": "facet", "radius": 1.6, "detail": 1, "color": "#BAE6FD",
           "emissive": "#38BDF8", "emissiveIntensity": 1.5, "roughness": 0.3,
           "keyframes": head_kf}]
    axis = math.pi / 2 + 0.12  # streak long axis ~horizontal, sloping down-left
    for i in range(14):
        d = 2.4 + i * 1.3                 # distance behind the head
        lat = -0.15 - i * 0.14            # tail slopes down as it trails back
        lane = ((i % 3) - 1) * 0.55       # three parallel lanes across the tail
        length = 6.0 + (i % 3) * 1.5
        op = max(0.25, 0.95 - i * 0.06)
        col = "#F8FAFC" if i < 5 else "#BFDBFE"
        em = "#FFFFFF" if i < 5 else "#7DD3FC"
        fx.append({"id": f"comet-streak{i}", "shape": "box", "size": [0.3, length, 0.3],
                   "color": col, "emissive": em, "emissiveIntensity": 1.4,
                   "roughness": 0.4, "rotation": [0, 0, axis + ((i % 3) - 1) * 0.04],
                   "opacity": op,
                   "keyframes": [{"frame": k["frame"],
                                 "position": [k["position"][0] - d, k["position"][1] + lat + lane, k["position"][2]]}
                                for k in head_kf]})
    return fx


def scenes(T):
    S2, S3, S4, S5, END = T.B["b3"] - 1, T.B["b4"] - 1, T.B["b5"] - 1, T.B["b6"] - 1, T.END
    HERO_P, FRIEND_P = [-3, 0, 0.5], [2.5, 0, 0.5]

    return [
        {   # Mars: red desert must read as Mars, not the town. The astronaut
            # stands on the right ledge at [6.8, 3, -1]; the wide is pulled
            # back (dist 29) so he stays fully in frame.
            "id": "mars", "location": "mars", "skyColor": "#FDBA74",
            "startFrame": 0, "endFrame": S2,
            "cameraShots": cover(0, S2, [lambda a, b: wide(a, b, [0, 0, 0.5], 29),
                                          lambda a, b: close_up(a, b, HERO_P),
                                          lambda a, b: low_angle(a, b, [6.8, 3, -1], dist=13, eye_height=1.5)]),
            "characters": {
                "hero": hold(0, S2, HERO_P, 0.2, "idle", "shocked"),
                "friend": hold(0, S2, FRIEND_P, -0.2, "point", "shocked"),
                "astronaut": hold(0, S2, [6.8, 3, -1], -0.3, "idle", "shocked"),
            },
        },
        {   # light speed: radial streaks in space
            "id": "streaks", "location": "space", "skyColor": "#000000",
            "startFrame": S2, "endFrame": S3,
            "cameraShots": [static_shot(S2, S3, [0, 8, 21], [0, 4.5, -3], 58)],
            "fx": _streaks(S2, S3),
            "characters": {
                "hero": hold(S2, S3, HERO_P, 0.2, "idle", "shocked"),
                "friend": hold(S2, S3, FRIEND_P, -0.2, "idle", "shocked"),
            },
        },
        {   # comet crossing the sky
            "id": "comet", "location": "space", "skyColor": "#000000",
            "startFrame": S3, "endFrame": S4,
            "cameraShots": [static_shot(S3, S4, [0, 8, 21], [0, 4.5, -3], 58)],
            "fx": _comet(S3, S4),
            "characters": {
                "hero": hold(S3, S4, HERO_P, 0.2, "point", "shocked"),
                "friend": hold(S3, S4, FRIEND_P, -0.2, "idle", "shocked"),
            },
        },
        {   # twinkle: two identical static shots at different times — the only
            # difference between the stills must be the stars' brightness
            "id": "twinkle", "location": "space", "skyColor": "#000000",
            "startFrame": S4, "endFrame": END,
            "cameraShots": split_shots(S4, END, [
                lambda a, b: static_shot(a, b, [0, 8, 21], [0, 4.5, -3], 58),
                lambda a, b: static_shot(a, b, [0, 8, 21], [0, 4.5, -3], 58),
            ]),
            "characters": {
                "hero": hold(S4, END, HERO_P, 0.2, "idle", "smile"),
                "friend": hold(S4, END, FRIEND_P, -0.2, "idle", "smile"),
            },
        },
    ]
