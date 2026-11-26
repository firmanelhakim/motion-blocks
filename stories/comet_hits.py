"""WHAT IF A COMET HIT EARTH? - science explainer.

Week 1 storyboard (the maintainer, 2026-11-17): video 7 of 7.
Structure: hook (the comet crosses the sky) -> space (what a comet is, the
tail) -> street (looking up, it is coming) -> classroom mechanism (the hit,
the dust, the dinosaurs) -> space (the flash and the dust-covered Earth) ->
closer. No shouts, tense then hopeful mood.

The science: a comet is a ball of ice and rock — a dirty snowball flying
through space. Near the Sun, the ice melts and gas and dust blow off
behind it: that is the tail, which can stretch for millions of kilometres.
A big impact hits with the force of millions of bombs and throws tons of
dust into the sky, blocking the Sun; no sunlight means no plants, no food,
and the food chain breaks. That is what happened to the dinosaurs, 66
million years ago. Today we track the big rocks years ahead, and we have
tested pushing one off course (a kinetic impactor). All plain-language,
standard figures, simplified for a Short.

Fresh visuals: the comet pattern (already built, faceted head + streak
tail) + an impact flash and dust cloud around the Earth globe, new music
(comet-hits.wav). The teacher is in the standard white blouse, placed
beside the desk at x -3.0 (not on it).

Build:   python scripts/make_short.py stories/comet_hits.py --stills
Render:  python scripts/make_short.py stories/comet_hits.py --skip-tts --render
"""
import math  # noqa: F401

from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, orbit, shot, split_shots, static_shot, wide  # noqa: F401

TITLE = "WHAT IF A COMET HIT EARTH?"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this world, a comet is heading for Earth. And it is not small.", "pause": 0.08},
    {"id": "b2", "text": "A comet is a ball of ice and rock. A dirty snowball, flying through space.", "pause": 0.10},
    {"id": "b3", "text": "As it gets close to the Sun, the ice starts to melt. Gas and dust blow off behind it — and that is the tail.", "pause": 0.10},
    {"id": "b4", "text": "The tail can stretch for millions of kilometres. Longer than the distance from the Earth to the Sun.", "pause": 0.10},
    {"id": "b5", "text": "Most comets miss us. They fly past, put on a show, and disappear for a hundred years.", "pause": 0.10},
    {"id": "b6", "text": "But this one is not missing. It is coming straight at us.", "pause": 0.10},
    {"id": "b7", "text": "A big comet hits with the force of millions of bombs. The ground shakes for hundreds of kilometres.", "pause": 0.10},
    {"id": "b8", "text": "And then the dust goes up. Tons of dust, thrown into the sky, blocking out the Sun.", "pause": 0.10},
    {"id": "b9", "text": "No sunlight means no plants. No plants means no food. The whole food chain breaks.", "pause": 0.10},
    {"id": "b10", "text": "That is what happened to the dinosaurs, 66 million years ago. A rock from space ended their world.", "pause": 0.10},
    {"id": "b11", "text": "The good news: we watch the sky now. We track the big rocks, years before they get here.", "pause": 0.10},
    {"id": "b12", "text": "And if one ever comes for us, we have a plan — push it, just a little, years early.", "pause": 0.10},
    {"id": "b13", "text": "So tonight, look up. Most of the sky is beautiful. But a little of it is worth watching.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/comet-hits.wav",
    "under_voice": 0.022,
    "gaps": 0.05,
}

SFX = [
    ("b1", "whoosh"),
    ("b1+0.5", "sparkle"),
    ("b2+0.5", "pop", {"f": 600}),
    ("b3+0.5", "swish"),
    ("b4+0.5", "sparkle"),
    ("b5+0.5", "pop", {"f": 600}),
    ("b6+0.5", "bell_low"),
    ("b7+0.5", "riser", {"dur": 1.5}),
    ("b8+0.5", "whoosh"),
    ("b9+0.5", "sad"),
    ("b10+0.5", "bell_low"),
    ("b11+0.5", "pop", {"f": 600}),
    ("b13+1.0", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
HERO = {
    "skin": "light",
    "hair": {"style": "spikyAnime", "color": "blue"},
    "top": {"style": "hoodie", "color": "royal", "secondary": "white"},
    "bottom": {"style": "jeans", "color": "denim"},
    "shoes": {"color": "white", "sole": "white"},
    "freckles": True,
}
CAST = {
    "hero": HERO,
    "friend": {"extends": "kid_girl", "hair": {"style": "ponytail", "color": "blonde"},
               "top": {"style": "hoodie", "color": "pink", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"color": "white", "sole": "white"}},
    "mom": {"extends": "real_mom", "hair": {"style": "ponytail", "color": "brown"}},
    # White blouse on purpose (sun_off teal was a fix for that video). She stands
    # BESIDE the desk at x -3.0, not on it - verify in the stills.
    "teacher": {"extends": "teacher_woman", "skin": "fair", "hair": {"style": "bun", "color": "blonde"}},
}


def _comet(a, b):
    """Comet crossing the sky left to right (from _test_week1_props.py): a
    faceted icy head + a tail of thin white/blue streaks trailing behind it,
    all tracking the same keyframe timing (moon-crater pattern)."""
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


def _impact(a, b):
    """The impact seen from space: the Earth globe, a bright white flash on
    its front face, and grey dust clouds spreading around it. The flash and
    the dust are static — the narration carries the darkening."""
    fx = [{"id": "earth", "shape": "sphere", "radius": 3.0, "color": "#38BDF8",
           "emissive": "#1D4ED8", "emissiveIntensity": 0.4, "roughness": 0.7,
           "keyframes": [{"frame": a, "position": [0, 14, -12]}, {"frame": b, "position": [0, 14, -12]}]}]
    for i, (ox, oy, oz, r) in enumerate([
            (1.0, 0.7, 1.9, 1.2), (-1.2, 1.0, 1.7, 1.0), (0.2, -1.0, 2.1, 1.3),
            (-0.5, 1.7, 1.4, 0.9)]):
        fx.append({"id": f"continent{i}", "shape": "sphere", "radius": r, "color": "#22C55E",
                   "emissive": "#16A34A", "emissiveIntensity": 0.25, "roughness": 0.8,
                   "keyframes": [{"frame": a, "position": [ox, 14 + oy, -12 + oz]},
                                {"frame": b, "position": [ox, 14 + oy, -12 + oz]}]})
    fx.append({"id": "flash", "shape": "sphere", "radius": 2.0, "color": "#FFFFFF",
               "emissive": "#FFFFFF", "emissiveIntensity": 2.5, "roughness": 0.3,
               "opacity": 0.85,
               "keyframes": [{"frame": a, "position": [1.5, 13.5, -9.5]}, {"frame": b, "position": [1.5, 13.5, -9.5]}]})
    for i, (dx, dy, dz, r) in enumerate([(-4.5, 1.5, 0.5, 1.4), (4.5, 2.0, -0.5, 1.6),
                                         (-2.5, -2.5, 1.0, 1.2), (3.0, -2.0, 0.8, 1.3),
                                         (0.5, 3.5, -0.5, 1.1)]):
        fx.append({"id": f"dust{i}", "shape": "sphere", "radius": r, "color": "#78716C",
                   "emissive": "#57534E", "emissiveIntensity": 0.3, "roughness": 0.9,
                   "opacity": 0.7,
                   "keyframes": [{"frame": a, "position": [dx, 14 + dy, -12 + dz]},
                                {"frame": b, "position": [dx, 14 + dy, -12 + dz]}]})
    return fx


# 4. SCENES ---------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S2 = B["b2"] - 1    # space: what a comet is, the tail
    S3 = B["b5"] - 1    # street: looking up, it is coming
    S4 = B["b7"] - 1    # classroom: the hit, the dust, the dinosaurs
    S5 = B["b11"] - 1   # space: the flash and the dust-covered Earth
    S6 = B["b13"] - 1   # living room (green), night: closer

    scenes = []

    # 1. HOOK - space: the comet crosses the sky ---------------------------------------
    scenes.append({
        "id": "hook", "location": "space", "skyColor": "#000000",
        "startFrame": 0, "endFrame": S2,
        "cameraShots": [static_shot(0, S2, [0, 8, 21], [0, 4.5, -3], 58)],
        "fx": _comet(0, S2),
        "characters": {
            "hero": hold(0, S2, [-3, 0, 0.5], 0.2, "point", "shocked"),
            "friend": hold(0, S2, [2.5, 0, 0.5], -0.2, "idle", "shocked"),
        },
    })

    # 2. SPACE - the comet up close: ice, rock, and the tail -------------------------------
    scenes.append({
        "id": "comet", "location": "space", "skyColor": "#000000",
        "startFrame": S2, "endFrame": S3,
        "cameraShots": cover(S2, S3, [lambda a, b: static_shot(a, b, [0, 8, 21], [0, 4.5, -3], 58),
                                       lambda a, b: close_up(a, b, [-3, 0, 0.5]),
                                       lambda a, b: orbit(a, b, [0, 14, -20], 12, 12, -0.3, 0.5, [0, 14, -20], 58)]),
        "fx": _comet(S2, S3),
        "characters": {
            "hero": hold(S2, S3, [-3, 0, 0.5], 0.2, "point", "shocked"),
            "friend": hold(S2, S3, [2.5, 0, 0.5], -0.2, "idle", "shocked"),
        },
    })

    # 3. STREET - looking up: most comets miss, this one is coming ------------------------------
    scenes.append({
        "id": "lookup", "location": "street", "isNight": True,
        "startFrame": S3, "endFrame": S4,
        "cameraShots": cover(S3, S4, [lambda a, b: shot(a, b, [0, 4, 21], [0, 4.5, 19], [0, 9, -10], [0, 10, -10], 62),
                                       lambda a, b: low_angle(a, b, [-2.5, 0, 0.5], dist=9, eye_height=1.2),
                                       lambda a, b: close_up(a, b, [2.5, 0, 0.5])]),
        "fx": _comet(S3, S4),
        "characters": {
            "hero": hold(S3, S4, [-2.5, 0, 0.5], 0.2, "point", "shocked"),
            "friend": hold(S3, S4, [2.5, 0, 0.5], -0.2, "idle", "shocked"),
        },
    })

    # 4. CLASSROOM - the hit, the dust, the dinosaurs ----------------------------------------------
    scenes.append({
        "id": "mechanism", "location": "classroom",
        "boardText": ["COMET: ICE + ROCK", "TAIL: GAS + DUST", "DUST BLOCKS THE SUN"],
        "startFrame": S4, "endFrame": S5,
        "cameraShots": cover(S4, S5, [lambda a, b: shot(a, b, [0, 7.4, 23], [0, 7.0, 20.5], [0, 4.8, -1], [0, 4.7, -1], 58),
                                       lambda a, b: close_up(a, b, [-0.5, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [-3.0, 0, -4.5])]),
        "characters": {
            "teacher": hold(S4, S5, [-3.0, 0, -4.5], 0.5, "point", "deadpan", "pointer"),
            "hero": hold(S4, S5, [-0.5, 0, 0.5], 0, "idle", "smile"),
            "friend": hold(S4, S5, [4.0, 0, 0.5], 0, "idle", "smile"),
        },
    })

    # 5. SPACE - the flash and the dust-covered Earth ----------------------------------------------
    scenes.append({
        "id": "impact", "location": "space", "skyColor": "#000000",
        "startFrame": S5, "endFrame": S6,
        "cameraShots": cover(S5, S6, [lambda a, b: static_shot(a, b, [0, 12, 8], [0, 14, -12], 58),
                                       lambda a, b: orbit(a, b, [0, 14, -12], 11, 13, -0.4, 0.6, [0, 14, -12], 58),
                                       lambda a, b: close_up(a, b, [-3, 0, 0.5])]),
        "fx": _impact(S5, S6),
        "characters": {
            "hero": hold(S5, S6, [-3, 0, 0.5], 0.2, "point", "shocked"),
            "friend": hold(S5, S6, [2.5, 0, 0.5], -0.2, "idle", "shocked"),
        },
    })

    # 6. LIVING ROOM (green), NIGHT - closer ------------------------------------------------------------
    scenes.append({
        "id": "closer", "location": "living_room", "variant": "green", "isNight": True,
        "startFrame": S6, "endFrame": END,
        "cameraShots": cover(S6, END, [lambda a, b: wide(a, b, [0, 0, 0.4], 24),
                                         lambda a, b: close_up(a, b, [-4.0, 0, 0.4]),
                                         lambda a, b: close_up(a, b, [4.0, 0, 0.4])]),
        "characters": {
            "hero": [kf(S6, [-4.0, 0, 0.4], 0.9, "idle", "deadpan"),
                     kf(B["b13"], [-4.0, 0, 0.4], 0.9, "idle", "smile"),
                     kf(END, [-4.0, 0, 0.4], 0.9, "idle", "smile")],
            "mom": [kf(S6, [4.0, 0, 0.4], -0.9, "wave", "smile"),
                    kf(END, [4.0, 0, 0.4], -0.9, "wave", "smile")],
        },
    })

    return scenes
