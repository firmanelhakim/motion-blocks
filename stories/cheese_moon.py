"""CHEESE MOON — "What if the Moon was made of cheese?"

Science explainer, lead: WingedBoy `{"kit": "wingedboy"}` ("Wingo") — the
winged boy who flies up to the cheese Moon and takes a bite. A cheese
Moon, mice on the surface, and a bite that makes the sea go wrong.
(WingedBoy is wired into the story pipeline as a lead, 2026-11-21.)

The Moon is the existing science fx (sphere + craters, moon_off.py pattern):
a big yellow sphere high in the night sky, with darker-yellow craters.
The camera orbits it. The mice are small-scaled R6 kids (scale 0.6) in
grey, standing on the Moon's "surface" via a night street scene — the
narration names them; no new character model is invented.
Note: the story pipeline accepts the 'fly' AnimationMode (wired into
STORY_ANIM_TO_CLIP 2026-11-21 for this story), so the fly-up uses the
kit fly clip — wings beating while he rises. The bite is staged at the
Moon's edge with his face on the cheese, plus a bite-mark crater that
appears where his mouth was.

Build (fake timings — Kokoro is not installed on this VM):
    python3 /tmp/build_stories.py cheese_moon
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, orbit, shot, split_shots, static_shot, wide  # noqa: F401

TITLE = "THE MOON IS CHEESE"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this world, the Moon is not rock. It is cheese, big and yellow.", "pause": 0.08},
    {"id": "b2", "text": "Every night it hangs in the sky, and the mice nibble the edges.", "pause": 0.08},
    {"id": "b3", "text": "Wingo says the holes in the Moon are not craters. They are bites.", "pause": 0.08},
    {"id": "b4", "text": "The mice eat a little every night, and the Moon gets thinner.", "pause": 0.08},
    {"id": "b5", "text": "But the Moon pulls the sea. No Moon, no tides.", "pause": 0.10},
    {"id": "b6", "text": "So one night, Wingo flew up to tell the mice to stop.", "pause": 0.08},
    {"id": "b7", "text": "He took one bite himself, just to see. The cheese was so good.", "pause": 0.08},
    {"id": "b8", "text": "He took another bite, and another, and the Moon got lighter.", "pause": 0.08},
    {"id": "b9", "text": "Down below, the sea went strange. The waves forgot which way to go.", "pause": 0.10},
    {"id": "b10", "text": "The boats bobbed, the fish were confused, and the beach grew wider.", "pause": 0.08},
    {"id": "w1", "text": "STOP!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "PUT!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "BACK!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b11", "text": "The mice squeaked, and Wingo put the bite back, crumb by crumb.", "pause": 0.08},
    {"id": "b12", "text": "The Moon grew heavy again, and the sea remembered its rhythm.", "pause": 0.08},
    {"id": "b13", "text": "But tonight, look up. The Moon has one new hole, shaped like Wingo.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05,
         "dropouts": [("b10+0.3", "w3.end")]}
SFX = [
    ("b1", "whoosh"),
    ("b2+0.5", "bubbles"),
    ("b3+0.4", "pop", {"f": 700}),
    ("b4+0.6", "pop", {"f": 600}),
    ("b5+0.5", "sparkle"),
    ("b6", "whoosh"),
    ("b7+0.5", "pop", {"f": 800}),
    ("b8+0.4", "pop", {"f": 750}),
    ("b9+0.3", "bell_low"),
    ("b10+0.6", "riser", {"dur": 1.6}),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b11+0.5", "sparkle"),
    ("b12+0.6", "reveal"),
    ("b13+1.5", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
CAST = {
    # Wingo: WingedBoy, the kit character (wired as a story lead). His
    # expression is a valid story ExpressionId ("cool", not his kit
    # default "smirk", which fails tsc in stories).
    "hero": {"kit": "wingedboy"},
    "kid": {"extends": "kid_boy", "hair": {"style": "messyFringe", "color": "brown"},
            "top": {"style": "hoodie", "color": "yellow", "secondary": "white"},
            "bottom": {"style": "jeans", "color": "denim"},
            "shoes": {"color": "white", "sole": "white"}},
    # The mice: small grey R6 kids (scale 0.6). The narration names them as
    # mice; no animal model exists, so the small size + grey look + bubble
    # carry the identity.
    "mouse1": {"extends": "little_brother", "hair": {"style": "buzz", "color": "gray"},
               "top": {"style": "tshirt", "color": "gray", "secondary": "gray"},
               "bottom": {"style": "shorts", "color": "gray"},
               "shoes": {"color": "gray", "sole": "gray"}, "scale": 0.6},
    "mouse2": {"extends": "little_brother", "hair": {"style": "buzz", "color": "lightGray"},
               "top": {"style": "tshirt", "color": "lightGray", "secondary": "lightGray"},
               "bottom": {"style": "shorts", "color": "lightGray"},
               "shoes": {"color": "lightGray", "sole": "lightGray"}, "scale": 0.6},
}


# 4. SCENES --------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END
    S_KID = B["b3"] - 1     # street: Grandpa tells the kid about the bites
    S_MOON = B["b6"] - 1    # night sky: the climb, the bite, the mice
    S_SEA = B["b9"] - 1     # crossroads: the sea goes strange
    S_BACK = B["b11"] - 1   # night sky: put it back
    S_END = B["b13"] - 1    # street at night: the new hole

    # The cheese Moon: a big yellow sphere high in the night sky with
    # darker-yellow craters riding on it (moon_off.py pattern). It drifts
    # slowly across the night scenes.
    MOON_C = [10, 38, -10]
    moon_kf = [{"frame": S_MOON, "position": [10, 38, -10]},
               {"frame": S_SEA, "position": [12, 39, -10]},
               {"frame": S_BACK, "position": [12, 39, -10]},
               {"frame": END, "position": [13, 39, -10]}]
    moon_fx = [{"id": "moon", "shape": "sphere", "radius": 5.0, "color": "#FDE68A",
                "emissive": "#FACC15", "emissiveIntensity": 0.8, "roughness": 0.9,
                "keyframes": moon_kf}]
    for i, (ox, oy, oz, r) in enumerate([
            (1.8, 1.2, 3.4, 1.0), (-1.5, 2.4, 3.0, 0.8), (3.0, -1.0, 2.2, 0.9),
            (0.2, 3.8, 1.0, 0.7), (-3.0, -0.6, 2.4, 0.9), (1.0, -2.6, 2.8, 0.8)]):
        moon_fx.append({"id": f"crater{i}", "shape": "sphere", "radius": r, "color": "#D97706",
                        "emissive": "#B45309", "emissiveIntensity": 0.25, "roughness": 0.9,
                        "keyframes": [{"frame": k["frame"],
                                      "position": [k["position"][0] + ox, k["position"][1] + oy, k["position"][2] + oz]}
                                     for k in moon_kf]})

    # The bite mark: a dark crater that appears where Wingo's mouth was.
    # It hides inside the Moon (at its centre) until just before the bite,
    # then moves out to the Moon's edge nearest his mouth and stays there,
    # tracking the Moon's drift — it IS the "new hole" of the ending.
    # v3 (2026-11-22): the offset points at Wingo's mouth from the Moon
    # centre ([4.29, -1.40, -0.90], magnitude 4.6) — the Moon's lower-right
    # edge from the bite cameras — because the bite point moved out and
    # down from the Moon (see BITE_P) so his head and wings stay clear.
    def _moon_at(frame):
        if frame <= moon_kf[0]["frame"]:
            return moon_kf[0]["position"]
        for a, b in zip(moon_kf, moon_kf[1:]):
            if a["frame"] <= frame <= b["frame"]:
                t = (frame - a["frame"]) / (b["frame"] - a["frame"]) if b["frame"] != a["frame"] else 0
                return [a["position"][i] + (b["position"][i] - a["position"][i]) * t for i in range(3)]
        return moon_kf[-1]["position"]
    _bite_frames = [S_MOON, B["b7"] - 10, B["b7"] + 15, S_SEA, S_BACK, END]
    _bite_offs = [[0, 0, 0], [0, 0, 0], [4.29, -1.40, -0.90], [4.29, -1.40, -0.90], [4.29, -1.40, -0.90], [4.29, -1.40, -0.90]]
    moon_fx.append({"id": "bite", "shape": "sphere", "radius": 0.9, "color": "#D97706",
                    "emissive": "#B45309", "emissiveIntensity": 0.25, "roughness": 0.9,
                    "keyframes": [{"frame": f,
                                  "position": [_moon_at(f)[i] + _bite_offs[j][i] for i in range(3)]}
                                 for j, f in enumerate(_bite_frames)]})

    HERO_P, KID_P = [-2.5, 0, 1.0], [2.5, 0, 1.0]
    # Wingo's bite spot, v3 (2026-11-22, re-staged after the maintainer flagged
    # overlaps in the v2 Moon scene): he hovers OUT from the Moon, below
    # its centre, so his head and wings stay clear of the cheese.
    # Moon centre at b7 is ~[10.63, 38.32, -10]; at BITE_P his head is
    # 8.04 studs from the centre (3.04 clear of the r=5.0 surface), his
    # closest wingtip 6.71 (1.71 clear), and his mouth sits 2.30 studs
    # off the surface — the bite reads from his open mouth + the crater
    # at the Moon's edge nearest his mouth. He drifts +x/+y with the Moon.
    # LOW_P is the kink in his flight path: he flies EAST at low altitude
    # first (well below the Moon), then rises vertically to the bite —
    # a straight diagonal from the street clipped his wingtips into the
    # Moon's lower edge (3D distance 4.37 < 5.0 at frames ~520-530).
    BITE_P = [18.0, 28.0, -12.0]
    BITE_P2 = [18.74, 28.36, -12.0]
    LOW_P = [15, 8, -9]
    MOUSE1_P = [7, 0, 2.5]
    MOUSE2_P = [-5.5, 0, -2.5]
    return [
        {   # Hook: the cheese Moon over the town at night, three aerial angles.
            "id": "hook", "location": "town_overview", "isNight": True,
            "startFrame": 0, "endFrame": S_KID,
            "fx": moon_fx,
            "cameraShots": [
                shot(0, S_KID // 3, [-10, 62, 74], [-7, 56, 67], [8, 0, -6], [7, 1, -7], 55),
                shot(S_KID // 3, 2 * S_KID // 3, [-7, 56, 67], [-4, 50, 61], [7, 1, -7], [6, 2, -8], 55),
                shot(2 * S_KID // 3, S_KID, [-4, 50, 61], [-2, 46, 56], [6, 2, -8], [6, 2, -8], 55),
            ],
            "characters": {},
        },
        {   # Street: Grandpa tells the kid about the bites.
            "id": "tale", "location": "street",
            "startFrame": S_KID, "endFrame": S_MOON,
            "cameraShots": cover(S_KID, S_MOON, [
                lambda a, b: medium(a, b, [0, 0, 1.0]),
                lambda a, b: close_up(a, b, HERO_P),
                lambda a, b: low_angle(a, b, HERO_P),
                lambda a, b: close_up(a, b, KID_P),
            ]),
            "characters": {
                "hero": [kf(S_KID, HERO_P, 0.4, "idle", "smile"),
                         kf(B["b4"], HERO_P, 0.4, "point", "smile"),
                         kf(S_MOON, HERO_P, 0.4, "idle", "smile")],
                "kid": [kf(S_KID, KID_P, -0.4, "idle", "smile"),
                        kf(B["b4"], KID_P, -0.4, "idle", "shocked"),
                        kf(S_MOON, KID_P, -0.4, "idle", "shocked")],
            },
        },
        {   # The Moon: Wingo FLIES up, bites the cheese Moon, the mice watch.
            # Re-staged v3 (2026-11-22) after the maintainer flagged three overlaps
            # in the v2 Moon scene: (1) the Moon's edge cut across Wingo's
            # face and hid his Moon-side arm — his head was only 0.67 studs
            # off the surface; (2) his feet read as standing on a green
            # dome — that dome is a horizon HILL (a giant green ball,
            # radius 40-60, top y 18-27, ~150 studs away), whose silhouette
            # passed right under his feet from the old high, level cameras;
            # (3) his wingtips clipped into the Moon sphere in 3D (4.37 <
            # 5.0) on the diagonal flight path. Fixes: BITE_P moved out
            # and down (head 3.04 clear, wingtip 1.71 clear); the flight
            # goes east LOW first, then rises vertically (wingtip never
            # closer than 6.16 to the Moon centre); every Moon-scene camera
            # is LOW, looking UP, so Wingo is silhouetted against black
            # sky and the hills drop out of the frame bottom. The mice
            # watch from the street below, looking up at him.
            "id": "moon", "location": "street", "isNight": True,
            "startFrame": S_MOON, "endFrame": S_SEA,
            "fx": moon_fx,
            "cameraShots": [
                # Flight leg 1 — takeoff and low eastward flight: the
                # camera stays far south and low, looking up; Wingo's full
                # body reads against the sky, the Moon at the top of frame.
                shot(S_MOON, 505, [-10, 5, 30], [2, 10, 24],
                     [-0.63, 12.33, -0.65], [14.31, 19.16, -9.15], 58),
                # Flight leg 2 — vertical rise to the bite: camera
                # south-east, still below his head, looking up; the Moon
                # re-enters the top of frame as he nears it.
                shot(505, B["b7"], [10, 10, 12], [20, 16, 2],
                     [14.54, 18.04, -9.10], [17.26, 36.05, -11.80], 58),
                # Bite wide: Wingo right of centre against black sky, the
                # big yellow Moon beside him to the left, crater visible.
                # Camera DUE SOUTH (x 17, z 4): the bite cameras sit ~41 deg
                # off his facing axis (-0.77 rad), so his face reads in 3/4.
                # (The first v3 staging put them east at [27, 25.8, 1.2] /
                # [23.6, 21.8, -3.7] — ~80 deg off-axis — and the stills
                # showed the BACK of his head in the bite shots.)
                static_shot(B["b7"], B["b7"] + 45, [17, 24, 4], [16.0, 34.8, -12.0], 58),
                # Bite close-up: his face in 3/4, the Moon's edge and the
                # bite crater just left of his open mouth, clear separation.
                # Same due-south camera; target lowered to his chest so the
                # Moon's disc stays in frame on the left.
                static_shot(B["b7"] + 45, B["b8"], [17, 22, 2], [16.0, 35.0, -11.8], 50),
                # More bites: different angle, from due south and lower,
                # looking up — the Moon still beside him, wings clear.
                static_shot(B["b8"], S_SEA, [20, 18, 4], [17.7, 35.2, -12.0], 58),
            ],
            "characters": {
                "hero": [kf(S_MOON, HERO_P, 0.3, "fly", "smile"),
                         kf(505, LOW_P, -0.2, "fly", "smile"),
                         kf(B["b7"], BITE_P, -HALF + 0.8, "fly", "laugh"),
                         kf(B["b8"], BITE_P2, -HALF + 0.8, "fly", "laugh"),
                         kf(S_SEA, BITE_P2, -HALF + 0.8, "fly", "shocked")],
                "mouse1": [kf(S_MOON, MOUSE1_P, face(MOUSE1_P, [11, 38, -10]), "idle", "smile"),
                           kf(B["b7"], MOUSE1_P, face(MOUSE1_P, [11, 38, -10]), "idle", "shocked"),
                           kf(S_SEA, MOUSE1_P, face(MOUSE1_P, [11, 38, -10]), "idle", "shocked")],
                "mouse2": hold(S_MOON, S_SEA, MOUSE2_P, face(MOUSE2_P, [11, 38, -10]), "idle", "smile"),
            },
        },
        {   # The sea goes strange: boats bob, the beach grows.
            "id": "sea", "location": "crossroads",
            "startFrame": S_SEA, "endFrame": S_BACK,
            "cameraShots": cover(S_SEA, S_BACK, [
                lambda a, b: wide(a, b),
                lambda a, b: medium(a, b, [0, 0, 0.5]),
                lambda a, b: close_up(a, b, KID_P, shake=0.06),
                lambda a, b: low_angle(a, b, HERO_P),
            ]),
            "characters": {
                "hero": [kf(S_SEA, HERO_P, 0.3, "idle", "panic"),
                         kf(B["w1"], HERO_P, 0.3, "point", "panic"),
                         kf(S_BACK, HERO_P, 0.3, "point", "panic")],
                "kid": [kf(S_SEA, KID_P, -0.3, "idle", "shocked"),
                        kf(B["w3"], KID_P, -0.3, "idle", "panic"),
                        kf(S_BACK, KID_P, -0.3, "idle", "panic")],
            },
        },
        {   # Put it back: Grandpa returns the crumbs, the Moon grows heavy.
            "id": "return", "location": "street", "isNight": True,
            "startFrame": S_BACK, "endFrame": S_END,
            "fx": moon_fx,
            "cameraShots": cover(S_BACK, S_END, [
                lambda a, b: orbit(a, b, [12, 39, -10], 16, 41, 0.5, -0.5, [12, 39, -10], 58),
                lambda a, b: medium(a, b, [0, 0, 1.0]),
                lambda a, b: close_up(a, b, HERO_P),
            ]),
            "characters": {
                "hero": [kf(S_BACK, HERO_P, 0.3, "idle", "smile"),
                         kf(B["b12"], HERO_P, 0.3, "celebrate", "laugh"),
                         kf(S_END, HERO_P, 0.3, "celebrate", "laugh")],
                "mouse1": hold(S_BACK, S_END, [5.5, 0, -2.0], -0.5, "wave", "smile"),
                "kid": hold(S_BACK, S_END, KID_P, -0.3, "idle", "smile"),
            },
        },
        {   # The new hole, shaped like Grandpa.
            "id": "hole", "location": "street", "isNight": True,
            "startFrame": S_END, "endFrame": END,
            "cameraShots": cover(S_END, END, [
                lambda a, b: medium(a, b, [0, 0, 1.0]),
                lambda a, b: close_up(a, b, HERO_P),
            ]),
            "characters": {
                "hero": hold(S_END, END, HERO_P, 0.4, "idle", "cool"),
                "kid": [kf(S_END, KID_P, -0.4, "idle", "smile"),
                        kf(B["b13"] + 40, KID_P, -0.4, "point", "shocked"),
                        kf(END, KID_P, -0.4, "point", "shocked")],
            },
        },
    ]
