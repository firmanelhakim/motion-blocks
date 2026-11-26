"""MOON DRIFTS AWAY — "What If the Moon Drifted Away Forever?"

Science explainer, lead: Nia, an R6 nerd (glasses, curious astronomer
kid — kept the whole video). Mia watches the tides with her; the
teacher explains the tilt in the classroom.

The science, kept exactly as verified:
- The Moon really is drifting away, about 3.8 cm a year.
- Tides shrink to about a THIRD (the Sun still pulls) — they do NOT
  disappear.
- Nights get darker; moonlight animals get confused.
- The Moon keeps Earth's tilt steady. Without it, over MILLIONS of
  years (not overnight) the tilt could wobble wildly: scorching
  summers, endless winters, maybe a pole pointing at the Sun.
- The Moon has been slowly braking Earth's spin. Without it, days
  STOP getting longer — they do NOT speed up.

HOW THIS DIFFERS from the other Moon videos: "What If Earth Had Two
Moons?" is about a second Moon; "What If the Moon Was Made of Cheese?"
is about a cheese Moon and the sea. THIS video is about OUR Moon
leaving — tides, darkness, tilt, day length. Different science, no
overlap.

The Moon is the cheese_moon pattern: a big pale-grey sphere (radius
5.0) with darker-grey craters riding on it, drifting away across the
story via position keyframes — further and higher, so it reads smaller
in the outro ("a tiny Moon in the distance"). The space environment
already has Earth far behind the stage ([-22, 24, -48]); the 'clock'
fx (BigClock) is the visual for the day-length beat.

Filmable-limits notes (honest):
- The tide shrinking cannot be animated (the sea is environment
  geometry). The beach beats are Nia + Mia pointing at the sea while
  the narration carries "about a third"; the tide line is not visible.
- The owl bumping into a tree / the turtle with a map cannot be
  staged (no animal props). The dark-nights beat is the night beach,
  dark, both kids 'shocked'; the narration carries the animals.
- The tilt wobble cannot be animated (Earth is environment geometry).
  The timescale — the key correction — is carried by the shout trio
  ("MILLIONS! OF! YEARS!") and the classroom board.
- The melt-into-a-puddle / freeze-into-an-ice-cube panels cannot be
  staged. The extremes beat is a classroom board ("SCORCHING
  SUMMERS / ENDLESS WINTERS / POLE AT THE SUN") + Nia panting (hot);
  the cold lives in the narration.

Locations: 'street' at night (hook + outro, the Moon in the night
sky); 'beach' at night (tides + dark nights); 'space' (Earth, the
Moon, the clock); 'classroom' (the extremes board).

Build (run the previews serially — do NOT run make_short.py alongside
other stories):
    python scripts/make_short.py stories/moon_drifts_away.py --stills
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, orbit, shot, split_shots, wide  # noqa: F401

TITLE = "THE MOON DRIFTS AWAY"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b0", "text": "What if the Moon drifted away forever?", "pause": 0.10},
    {"id": "b1", "text": "In this world, the Moon really is drifting away, about four centimetres a year.", "pause": 0.08},
    {"id": "b2", "text": "But what if it just… left?", "pause": 0.10},
    {"id": "b3", "text": "First, the tides. The Moon drives most of them, so they would shrink to about a third.", "pause": 0.08},
    {"id": "b4", "text": "Only the Sun's weaker pull is left. The tide pools dry up.", "pause": 0.08},
    {"id": "b5", "text": "Nights get way darker. Animals that hunt by moonlight? All confused.", "pause": 0.08},
    {"id": "b6", "text": "Then the big one. The Moon keeps Earth's tilt steady.", "pause": 0.08},
    {"id": "b7", "text": "Without it, over millions of years, our tilt could wobble wildly.", "pause": 0.08},
    {"id": "w1", "text": "MILLIONS!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "OF!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "YEARS!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b8", "text": "Scorching summers, endless winters, maybe even a pole pointing at the Sun.", "pause": 0.08},
    {"id": "b9", "text": "Bonus weirdness: the Moon has been slowly braking Earth's spin.", "pause": 0.08},
    {"id": "b10", "text": "Without it, our days stop getting longer.", "pause": 0.10},
    {"id": "b11", "text": "So, thanks, Moon. Which cosmic disaster should we test next? Tell us below.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {"file": "music/moon-tide.wav", "under_voice": 0.022, "gaps": 0.05,
         "dropouts": [("b7+0.3", "w3.end")]}
SFX = [
    ("b0", "whoosh"),
    ("b1+0.5", "pop", {"f": 700}),
    ("b2+0.3", "whoosh"),
    ("b3+0.5", "pop", {"f": 600}),
    ("b4+0.5", "sad"),
    ("b5+0.5", "bell_low"),
    ("b6+0.5", "pop", {"f": 800}),
    ("b7+0.4", "riser", {"dur": 1.6}),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b8+0.5", "sparkle"),
    ("b9+0.5", "pop", {"f": 650}),
    ("b10+0.5", "ding_dong"),
    ("b11+1.0", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
CAST = {
    # Nia leads: the nerd preset (glasses, curious), kept the whole video.
    "hero": {"extends": "nerd"},
    # Mia watches the tides with her (her no_friction look).
    "friend": {"extends": "kid_girl", "hair": {"style": "pigtails", "color": "brown"},
               "top": {"style": "sweater", "color": "teal", "secondary": "white"},
               "bottom": {"style": "skirt", "color": "navy"},
               "shoes": {"color": "white", "sole": "white"}},
    "teacher": {"extends": "teacher"},
}


# 4. SCENES --------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END
    S_BEACH = B["b3"] - 1    # beach at night: the tides
    S_SPACE = B["b6"] - 1    # space: Earth, the tilt
    S_CLASS = B["b8"] - 1    # classroom: the extremes board
    S_SPACE2 = B["b9"] - 1   # space: the braking spin + the clock
    S_OUTRO = B["b11"] - 1   # street at night: waving at the tiny Moon

    # THE MOON — cheese_moon pattern, but a real Moon: pale-grey sphere
    # radius 5.0 with darker-grey craters riding on it. The craters sit
    # PROUD of the surface (offset magnitude ~4.6, so a 0.9–1.2-radius
    # crater pokes 0.5–0.8 out) and dark (#64748B) — the first attempt
    # used the cheese_moon offsets (magnitude ~4.0, craters buried to
    # the surface) and the Moon rendered as a featureless grey disc.
    # The Moon drifts away across the story (further + higher = visually
    # smaller), on a path kept near-overhead (x 4–16) so a low camera
    # can frame Nia AND the Moon together. Keyframes sit at the scene
    # boundaries; every outdoor scene includes the same fx list.
    moon_kf = [{"frame": 0, "position": [4, 19, -12]},
               {"frame": S_BEACH, "position": [6, 19, -18]},
               {"frame": S_SPACE, "position": [8, 22, -26]},
               {"frame": S_OUTRO, "position": [14, 26, -44]},
               {"frame": END, "position": [16, 27, -48]}]
    moon_fx = [{"id": "moon", "shape": "sphere", "radius": 5.0, "color": "#E2E8F0",
                "emissive": "#CBD5E1", "emissiveIntensity": 0.5, "roughness": 0.9,
                "keyframes": moon_kf}]
    for i, (ox, oy, oz, r) in enumerate([
            (2.1, 1.4, 3.9, 1.1), (-1.7, 2.8, 3.5, 0.9), (3.5, -1.2, 2.5, 1.0),
            (0.2, 4.4, 1.2, 0.8), (-3.5, -0.7, 2.8, 1.0), (1.2, -3.0, 3.2, 0.9)]):
        moon_fx.append({"id": f"crater{i}", "shape": "sphere", "radius": r, "color": "#64748B",
                        "emissive": "#475569", "emissiveIntensity": 0.25, "roughness": 0.9,
                        "keyframes": [{"frame": k["frame"],
                                      "position": [k["position"][0] + ox, k["position"][1] + oy, k["position"][2] + oz]}
                                     for k in moon_kf]})

    def _moon_at(frame):
        if frame <= moon_kf[0]["frame"]:
            return moon_kf[0]["position"]
        for a, b in zip(moon_kf, moon_kf[1:]):
            if a["frame"] <= frame <= b["frame"]:
                t = (frame - a["frame"]) / (b["frame"] - a["frame"]) if b["frame"] != a["frame"] else 0
                return [a["position"][i] + (b["position"][i] - a["position"][i]) * t for i in range(3)]
        return moon_kf[-1]["position"]

    # THE CLOCK — BigClock, for the day-length beat (b9-b10). It stands
    # on the space floor at [7, 0, -4], clear of the actors.
    # NOTE: the clock's face centre is at fx_y + 0.45 and the face is
    # ~4.4 studs across, so at fx_y = 0 the lower half sits BELOW the
    # space floor (top y 0) and the floor hides it — the first two
    # attempts showed only the top half of the dial. fx_y = 2.5 lifts
    # the whole face (0.75–5.15) clear of the floor.
    clock_fx = [{"id": "clock", "shape": "clock", "color": "#F8FAFC", "scale": 1.0,
                 "keyframes": [{"frame": S_SPACE2, "position": [7, 2.5, -4]},
                               {"frame": S_OUTRO, "position": [7, 2.5, -4]}]}]

    HERO_P, FRIEND_P = [-2.5, 0, 0.5], [2.5, 0, 0.5]
    return [
        {   # Hook: the big question over Nia's face, then she looks up at
            # the Moon through her binoculars. The Moon look-up is split
            # in two (the first attempt was one 4.0 s shot, over the
            # 3.5 s max): the Moon disc itself, then Nia AND the Moon
            # together — the Moon's path is near-overhead and low
            # enough (y ~20) that one frame holds her (lower left) and
            # the Moon (upper right).
            "id": "hook", "location": "street", "isNight": True,
            "startFrame": 0, "endFrame": S_BEACH,
            "fx": moon_fx,
            "cameraShots": [
                medium(0, B["b1"], [-2.5, 0, 0.5]),
                # The Moon look-up, reframed (fix round): the first
                # attempt shot it close and low (camera [-5, 1.2, 9]),
                # so Nia's head filled the lower centre and the captions
                # ("Moon really", "is drifting") printed across her
                # eyes/glasses (f87–122, worst f111). This uses the
                # space scene's proven combined framing — camera pulled
                # back and slightly west, target a fixed point below the
                # Moon — so her head sits in the lower third and the
                # caption lands on her torso, with the Moon still big
                # in the upper frame.
                shot(B["b1"], 120,
                     [-4, 2, 20], [-4, 2.2, 19],
                     [1, 11, -8], [1, 11, -8], 60),
                shot(120, B["b2"],
                     [-2.5, 2, 18], [-2.5, 2.2, 17],
                     [1, 11, -8], [1, 11, -8], 60),
                shot(B["b2"], S_BEACH,
                     [-2.5, 5.6, 12], [-2.5, 5.6, 11],
                     [-2.5, 4.3, 0.5], [-2.5, 4.3, 0.5], 50),
            ],
            "characters": {
                "hero": [kf(0, HERO_P, 0, "idle", "smile", "binoculars"),
                         kf(B["b1"], HERO_P, 0, "point", "shocked", "binoculars"),
                         kf(S_BEACH, HERO_P, 0, "point", "shocked", "binoculars")],
            },
        },
        {   # The tides: the beach at night, the sea behind the actors
            # (z < -14). The tide shrinking cannot be animated — the sea
            # is environment geometry — so Nia + Mia point at the sea
            # while the narration carries "about a third". The dark
            # nights beat (b5) stays on the same beach: it is already a
            # night shore, dark, both kids 'shocked'.
            "id": "beach", "location": "beach", "isNight": True,
            "startFrame": S_BEACH, "endFrame": S_SPACE,
            "fx": moon_fx,
            "cameraShots": cover(S_BEACH, S_SPACE, [
                lambda a, b: wide(a, b, [0, 0, 0.5], dist=20),
                # Wide, not medium, for the 2-shot: a medium at dist 12
                # (half-width ~3.2) sliced Nia at the left edge — two
                # actors 5 apart with arms out span ~8.4 studs.
                lambda a, b: wide(a, b, [0, 0, 0.5], dist=18),
                lambda a, b: close_up(a, b, HERO_P),
                lambda a, b: shot(a, b, [0, 7.4, 21], [0, 7.4, 20],
                                  [0, 4.8, -3], [0, 4.8, -6], 58),
            ]),
            "characters": {
                "hero": [kf(S_BEACH, HERO_P, 0, "point", "smile"),
                         kf(B["b4"], HERO_P, 0, "point", "shocked"),
                         kf(B["b5"], HERO_P, 0, "idle", "shocked"),
                         kf(S_SPACE, HERO_P, 0, "idle", "shocked")],
                "friend": [kf(S_BEACH, FRIEND_P, 0, "idle", "smile"),
                           kf(B["b4"], FRIEND_P, 0, "point", "shocked"),
                           kf(B["b5"], FRIEND_P, 0, "idle", "shocked"),
                           kf(S_SPACE, FRIEND_P, 0, "idle", "shocked")],
            },
        },
        {   # Space: Earth far behind the stage (built into the space
            # environment) and the Moon drifting away. Nia points at
            # them while the tilt beat lands, then the shout trio
            # ("MILLIONS! OF! YEARS!") — the timescale is the point, so
            # the shouts get tracking close-ups on Nia with shake on the
            # last word. The orbit is LOW (height 5) looking UP at the
            # Moon (blue_sun pattern) so the floor stays out of frame.
            "id": "space", "location": "space", "skyColor": "#000000",
            "startFrame": S_SPACE, "endFrame": S_CLASS,
            "fx": moon_fx,
            "cameraShots": cover(S_SPACE, S_CLASS, [
                lambda a, b: wide(a, b, [0, 0, 0.5], dist=16),
                # Nia AND the Moon together (the first attempt orbited
                # the Moon alone — a featureless disc filling the
                # frame, no actors, no Earth). Same combined framing
                # as the hook: Nia lower left, the Moon upper right.
                lambda a, b: shot(a, b, [-2.5, 2, 18], [-2.5, 2.2, 17],
                                  [1, 11, -8], [1, 11, -8], 60),
                lambda a, b: close_up(a, b, HERO_P, shake=0.08),
            ]),
            "characters": {
                "hero": [kf(S_SPACE, HERO_P, 0.2, "point", "shocked"),
                         kf(B["w1"], HERO_P, 0.2, "point", "panic"),
                         kf(S_CLASS, HERO_P, 0.2, "point", "panic")],
                "friend": [kf(S_SPACE, FRIEND_P, -0.2, "idle", "shocked"),
                           kf(B["w1"], FRIEND_P, -0.2, "idle", "panic"),
                           kf(S_CLASS, FRIEND_P, -0.2, "idle", "panic")],
            },
        },
        {   # The extremes: scorching summers, endless winters, a pole
            # pointing at the Sun. The melt / freeze panels cannot be
            # staged, so the board carries all three lines and Nia
            # pants (hot) while the teacher points at the board.
            "id": "extremes", "location": "classroom",
            "boardText": ["SCORCHING SUMMERS", "ENDLESS WINTERS", "POLE AT THE SUN"],
            "startFrame": S_CLASS, "endFrame": S_SPACE2,
            "cameraShots": cover(S_CLASS, S_SPACE2, [
                lambda a, b: wide(a, b, [-0.25, 0, 0], dist=24),
                lambda a, b: medium(a, b, [0, 0, 1]),
                lambda a, b: close_up(a, b, [0, 0, 1.5]),
            ]),
            "characters": {
                "teacher": [kf(S_CLASS, [-5.5, 0, -2], face([-5.5, 0, -2], [0, 0, 1.5]), "idle", "smile"),
                            kf(B["b8"] + 30, [-5.5, 0, -2], face([-5.5, 0, -2], [0, 0, 1.5]), "point", "smile"),
                            kf(S_SPACE2, [-5.5, 0, -2], face([-5.5, 0, -2], [0, 0, 1.5]), "idle", "smile")],
                "hero": hold(S_CLASS, S_SPACE2, [0, 0, 1.5], 0, "panting", "shocked"),
                "friend": hold(S_CLASS, S_SPACE2, [5, 0, 1.5], 0, "idle", "shocked"),
            },
        },
        {   # The braking spin + the clock: Earth (built-in, far behind)
            # for the braking beat, the BigClock for "days stop getting
            # longer". Nia points at the Earth, then at the clock.
            "id": "spin", "location": "space", "skyColor": "#000000",
            "startFrame": S_SPACE2, "endFrame": S_OUTRO,
            "fx": moon_fx + clock_fx,
            "cameraShots": cover(S_SPACE2, S_OUTRO, [
                lambda a, b: wide(a, b, [0, 0, 0.5], dist=16),
                # The clock, shot STRAIGHT ON (camera due south of it,
                # at the face-centre height y 2.95) — the first attempt
                # shot it obliquely from the upper right, which tilted
                # the face and foreshortened the lower numbers away.
                lambda a, b: shot(a, b, [7, 2.95, 6], [7, 2.95, 5.5],
                                  [7, 2.95, -4], [7, 2.95, -4], 50),
                lambda a, b: close_up(a, b, HERO_P),
            ]),
            "characters": {
                "hero": [kf(S_SPACE2, HERO_P, 0.2, "point", "shocked"),
                         kf(B["b10"], HERO_P, 0.2, "point", "smile"),
                         kf(S_OUTRO, HERO_P, 0.2, "point", "smile")],
                "friend": hold(S_SPACE2, S_OUTRO, FRIEND_P, -0.2, "idle", "smile"),
            },
        },
        {   # Outro: Nia waves a goodbye at the tiny Moon in the
            # distance (it has drifted to [32, 47, -54] by now). Wide
            # so both Nia and the far Moon are in frame, then a medium
            # on her wave.
            "id": "outro", "location": "street", "isNight": True,
            "startFrame": S_OUTRO, "endFrame": END,
            "fx": moon_fx,
            "cameraShots": [
                shot(S_OUTRO, B["b11"] + 60,
                     [-2.5, 5.6, 12], [-2.5, 5.6, 11],
                     [-2.5, 4.3, 0.5], [-2.5, 4.3, 0.5], 50),
                # The tiny Moon in the distance, shot from EAST of Nia
                # (camera x 8) — the first attempt shot from the west
                # and Nia's head intruded at the bottom of the frame,
                # cut off. From the east the sightline to the Moon
                # passes clear of him.
                shot(B["b11"] + 60, END,
                     [8, 1.2, 9], [8, 1.6, 7.5],
                     _moon_at(END), _moon_at(END), 45),
            ],
            "characters": {
                "hero": [kf(S_OUTRO, HERO_P, 0, "wave", "smile"),
                         kf(END, HERO_P, 0, "wave", "smile")],
                "friend": [kf(S_OUTRO, FRIEND_P, 0, "wave", "smile"),
                           kf(END, FRIEND_P, 0, "wave", "smile")],
            },
        },
    ]
