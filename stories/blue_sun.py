"""BLUE SUN — "What if the Sun was blue?"

Science explainer, lead: kid_boy hero ("Milo" look: messy brown fringe,
yellow hoodie — kept the whole video). The Sun rises blue, the sky goes a
deeper blue, and the world looks wrong. The teacher explains the one
science idea: a star's colour is its temperature. Our yellow Sun is about
5,500 C on its surface; a blue star is 10,000 C and more, and gives off
far more ultraviolet light. The plants still grow — plants love blue
light for photosynthesis. Colour is a clue to temperature.

FIX 1 (2026-11-22): opens with the title question "What if the Sun was
blue?" (the maintainer's channel rule overrides the "In this town," opening).
The Sun fx is raised +6 (disc at [0, 13.2, -13], high in the sky, clear
of the lamp line) and both look-up shots moved to the STREET location as
their own scenes (hook_q, twist_look): in town_overview the
traffic-light pole sits 1 stud from the MAIN ST sign and crosses it from
every southern camera (round-1 reframe from x = -8 still covered the
"A"); in the street the sign and lights sit 20 studs east, out of frame.
Plant moved to [12, 0, -2] (clear of the lamp at world x = -9) with a
matching close-up camera; plants and reveal 2-shots are wides, not
mediums — two actors 5 apart with arms out span ~8.4 studs, wider than
a medium frame, which sliced the hero at the left edge in both;
lesson wide re-centred so the friend is whole; space orbit dropped to
height 5 looking up at the raised Sun so the floor line stays out of
frame.

THE BLUE SUN: fx shape 'blue-sun' (BlueSun — glowing saturated-blue
sphere radius 2.1 + radial glow + blue point light, gently pulsing). The
component carries an internal offset — the sun sits at [0, 7.2, -13]
inside it — so the fx is placed at [0, 6, 0], scale 1.5, putting the disc
at [0, 13.2, -13], high in the sky above the street lamps, and the SAME
fx (same id, same keyframes spanning the story) is included in EVERY
outdoor scene: hook, both street scenes, space, and the twist. No
yellow-Sun fx anywhere — the narration carries the 5,500 C comparison,
the visuals stay blue throughout.

THE BLUE SKY: a re-skin, NOT a new location. Same town, skyColor
'#1E40AF' (deep blue) in every outdoor town scene; the classroom is
indoors (no sky, no sun fx); space uses '#000000'.

THE PLANT: fx shape 'plant' (BlueLightPlant — potted plant, pot bottom
on y = 0, ~3.5 tall, dark blue-green leaves with emissive lit tips). One
at [12, 0, -2] in the street "world looks wrong" scene and again in the
street "plants still grow" scene, which also gets a dedicated plant
close-up camera shot.

Build (coordinator runs the previews serially — do NOT run make_short.py
alongside other stories):
    python scripts/make_short.py stories/blue_sun.py --stills
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, orbit, shot, split_shots, static_shot, wide  # noqa: F401

TITLE = "THE SUN IS BLUE"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b0", "text": "What if the Sun was blue?", "pause": 0.10},
    {"id": "b1", "text": "In this town, the Sun rose blue.", "pause": 0.08},
    {"id": "b2", "text": "The sky was a deeper blue, and the light was cold and strange.", "pause": 0.08},
    {"id": "b3", "text": "The trees looked darker, almost black-green, under the blue light.", "pause": 0.08},
    {"id": "b4", "text": "The plants looked strange too, but they kept on growing.", "pause": 0.08},
    {"id": "b5", "text": "Our Sun is yellow, and about five thousand five hundred degrees.", "pause": 0.08},
    {"id": "b6", "text": "This Sun is blue — and blue means hotter.", "pause": 0.10},
    {"id": "b7", "text": "A blue star burns far hotter than our yellow Sun.", "pause": 0.08},
    {"id": "b8", "text": "It gives off far more ultraviolet light, the light you cannot see.", "pause": 0.10},
    {"id": "b9", "text": "But the plants still grow, because plants love blue light.", "pause": 0.08},
    {"id": "b10", "text": "Blue light is the light plants use to make their food.", "pause": 0.10},
    {"id": "w1", "text": "TEN!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "THOUSAND!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "DEGREES!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b11", "text": "Ten thousand degrees. That is how hot a blue star burns.", "pause": 0.08},
    {"id": "b12", "text": "The colour of a star tells you how hot it is. Blue is the hottest of all.", "pause": 0.10},
    {"id": "b13", "text": "But tonight, look up. The blue Sun is still there — and tomorrow, it might be a different colour.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05,
         "dropouts": [("b10+0.3", "w3.end")]}
SFX = [
    ("b0", "whoosh"),
    ("b0+0.5", "sparkle"),
    ("b1", "whoosh"),
    ("b2+0.5", "sparkle"),
    ("b3+0.4", "pop", {"f": 600}),
    ("b4+0.5", "sparkle"),
    ("b5+0.5", "pop", {"f": 700}),
    ("b6+0.4", "bell_low"),
    ("b7+0.5", "pop", {"f": 800}),
    ("b8+0.5", "sparkle"),
    ("b9+0.5", "pop", {"f": 650}),
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
    # Hero: one distinct look, kept the whole video (messy brown fringe,
    # yellow hoodie, freckles). He looks up at the blue Sun with 'point' +
    # 'shocked' (sky_blue.py hook pattern); the Sun sits in the sky behind
    # him from the +Z cameras, so his face stays visible.
    "hero": {"extends": "kid_boy", "hair": {"style": "messyFringe", "color": "brown"},
             "top": {"style": "hoodie", "color": "yellow", "secondary": "white"},
             "bottom": {"style": "jeans", "color": "denim"},
             "shoes": {"color": "white", "sole": "white"}, "freckles": True},
    "friend": {"extends": "kid_girl", "hair": {"style": "ponytail", "color": "blonde"},
               "top": {"style": "hoodie", "color": "pink", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"},
               "shoes": {"color": "white", "sole": "white"}},
    # Standard teacher (sky_blue.py): white blouse, bun, beside the desk.
    "teacher": {"extends": "teacher_woman", "skin": "fair",
                "hair": {"style": "bun", "color": "blonde"}},
}


# 4. SCENES --------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END
    S_STREET = B["b3"] - 1    # street: the world looks wrong
    S_CLASS = B["b5"] - 1     # classroom: the teacher explains
    S_SPACE = B["b7"] - 1     # space: the blue star among stars
    S_PLANT = B["b9"] - 1     # street: the plants still grow
    S_SHOUT = B["w1"] - 1     # street: the temperature reveal
    S_END = B["b13"] - 1      # town_overview: tonight, look up
    Q_END = S_STREET // 3     # hook look-up takes the first third (b0 + start of b1)
    T_LOOK = S_END + (END - S_END) // 2  # twist look-up takes the second half

    # THE BLUE SUN — one fx, reused verbatim in every outdoor scene.
    # Placed at [0, 6, 0]: the component's internal offset puts the glowing
    # sphere high in the sky at [0, 13.2, -13] (SUN) — above the lamp line,
    # so it reads as a sun, not a street lamp. Scale 1.5 for a big sun.
    # Static keyframes spanning the whole story (the pulse is internal).
    SUN = [0, 13.2, -13]
    sun_fx = [{"id": "bluesun", "shape": "blue-sun", "color": "#38BDF8", "scale": 1.5,
               "keyframes": [{"frame": 0, "position": [0, 6, 0]},
                             {"frame": END, "position": [0, 6, 0]}]}]

    # THE PLANT — potted, pot bottom on y = 0, at the street's right side,
    # x = 12: clear of the north-side lamp at world x = -9 (local x = 3),
    # whose pole cut the left of the v1 plant close-up. One entry per scene
    # it appears in (ids are per-scene).
    def plant_fx(a, b):
        return [{"id": "plant", "shape": "plant", "color": "#247575", "scale": 1.0,
                 "keyframes": [{"frame": a, "position": [12, 0, -2]},
                               {"frame": b, "position": [12, 0, -2]}]}]

    HERO_P, FRIEND_P = [-2.5, 0, 1.0], [2.5, 0, 1.0]
    TEACHER_P = [-3.0, 0, -4.5]
    HERO_C, FRIEND_C = [-0.5, 0, 0.5], [4.5, 0, 0.5]
    BLUE_SKY = "#1E40AF"
    return [
        {   # Hook, part 1: the question. OPENS on a street-level look-up
            # at the raised blue Sun itself while "What if the Sun was
            # blue?" is asked — the premise made visual. Shot in the
            # STREET location (not town_overview): there the MAIN ST sign
            # and the intersection traffic lights sit 20 studs east, out
            # of frame, so no pole can cross the sign — in town_overview
            # the traffic-light pole at local x = -0.4 sits 1 stud from
            # the sign and crosses it from every southern camera. Only
            # two thin lamp poles show low in the frame, clear of the Sun.
            "id": "hook_q", "location": "street", "skyColor": BLUE_SKY,
            "startFrame": 0, "endFrame": Q_END,
            "fx": sun_fx,
            "cameraShots": [
                shot(0, Q_END, [-5, 1.2, 9], [-5, 1.6, 7.5], SUN, SUN, 45),
            ],
            "characters": {},
        },
        {   # Hook, part 2: two aerials over the town under the deep-blue
            # sky while "In this town, the Sun rose blue" lands.
            "id": "hook", "location": "town_overview", "skyColor": BLUE_SKY,
            "startFrame": Q_END, "endFrame": S_STREET,
            "fx": sun_fx,
            "cameraShots": split_shots(Q_END, S_STREET, [
                lambda a, b: shot(a, b, [-10, 62, 74], [-7, 56, 67], [8, 0, -6], [7, 1, -7], 55),
                lambda a, b: shot(a, b, [-7, 56, 67], [-4, 50, 61], [7, 1, -7], [6, 2, -8], 55),
            ]),
            "characters": {},
        },
        {   # Street: the world looks wrong. Hero points up at the Sun with
            # a shocked face; the blue Sun hangs in the sky behind him and
            # the strange dark plant stands at the street's right side.
            "id": "wrong", "location": "street", "skyColor": BLUE_SKY,
            "startFrame": S_STREET, "endFrame": S_CLASS,
            "fx": sun_fx + plant_fx(S_STREET, S_CLASS),
            "cameraShots": cover(S_STREET, S_CLASS, [
                lambda a, b: shot(a, b, [0, 7.4, 24.5], [0, 7.4, 24.5], [0, 4.8, -0.5], [0, 4.8, -0.5], 58),
                lambda a, b: low_angle(a, b, HERO_P),
                lambda a, b: close_up(a, b, HERO_P),
                lambda a, b: medium(a, b, [0, 0, 1.0]),
            ]),
            "characters": {
                "hero": hold(S_STREET, S_CLASS, HERO_P, 0.2, "point", "shocked"),
                "friend": hold(S_STREET, S_CLASS, FRIEND_P, -0.2, "idle", "shocked"),
            },
        },
        {   # Classroom: the teacher explains — colour is temperature. The
            # chalkboard carries the numbers so they land visually too.
            "id": "lesson", "location": "classroom",
            "boardText": ["BLUE = HOTTER", "YELLOW SUN 5,500 C",
                          "BLUE STAR 10,000 C+", "COLOUR = TEMPERATURE"],
            "startFrame": S_CLASS, "endFrame": S_SPACE,
            "cameraShots": cover(S_CLASS, S_SPACE, [
                lambda a, b: shot(a, b, [0, 7.4, 23], [0, 7.4, 23], [0, 4.8, -1], [0, 4.8, -1], 58),
                # Wide centred on the trio's midpoint (x = 0.5): in v1 the
                # centre x = -1.5 pushed the friend (x = 4.5) off the
                # right edge. At dist 20 she sits ~4.0 off-centre, inside
                # the frame with margin; teacher and hero fit too.
                lambda a, b: wide(a, b, [0.5, 0, -1], dist=20),
                lambda a, b: close_up(a, b, HERO_C),
            ]),
            "characters": {
                "teacher": hold(S_CLASS, S_SPACE, TEACHER_P, 0.5, "point", "deadpan", "pointer"),
                "hero": [kf(S_CLASS, HERO_C, 0, "idle", "smile"),
                         kf(B["b6"], HERO_C, 0, "idle", "shocked"),
                         kf(S_SPACE, HERO_C, 0, "idle", "shocked")],
                "friend": hold(S_CLASS, S_SPACE, FRIEND_C, 0, "idle", "smile"),
            },
        },
        {   # Space: the blue Sun as a star among stars — hotter, and pouring
            # out ultraviolet light you cannot see. The camera orbits it.
            "id": "star", "location": "space", "skyColor": "#000000",
            "startFrame": S_SPACE, "endFrame": S_PLANT,
            "fx": sun_fx,
            "cameraShots": cover(S_SPACE, S_PLANT, [
                # Tighter wide (dist 16) so the actors + Sun fill the
                # frame instead of black void at the edges.
                lambda a, b: wide(a, b, [0, 0, 0.5], dist=16),
                # Orbit LOW (height 5) looking UP at the raised Sun: the
                # floor plane stays below the frame, so no horizon line
                # and no dead black half. Tighter radius (11) keeps the
                # Sun big among the stars.
                lambda a, b: orbit(a, b, SUN, 11, 5, 0.5, -0.5, SUN, 50),
                lambda a, b: close_up(a, b, HERO_P),
            ]),
            "characters": {
                "hero": hold(S_SPACE, S_PLANT, HERO_P, 0.2, "point", "shocked"),
                "friend": hold(S_SPACE, S_PLANT, FRIEND_P, -0.2, "idle", "shocked"),
            },
        },
        {   # Street: the plants still grow. The plant gets its own close-up
            # so the dark blue-green leaves read, then the hero points at
            # the blue light that feeds them.
            "id": "plants", "location": "street", "skyColor": BLUE_SKY,
            "startFrame": S_PLANT, "endFrame": S_SHOUT,
            "fx": sun_fx + plant_fx(S_PLANT, S_SHOUT),
            "cameraShots": cover(S_PLANT, S_SHOUT, [
                # Wide 2-shot, not medium: two idle actors 5 apart with
                # arms at their sides span ~8.4 studs, wider than a
                # medium frame (half-width ~3.2) — the v1 medium sliced
                # the hero at the left edge. Wide at dist 18 fits both
                # whole with margin.
                lambda a, b: wide(a, b, [0, 0, 1.0], dist=18),
                # Plant close-up from the east, tight on the moved plant:
                # no lamp pole in the sight line any more.
                lambda a, b: shot(a, b, [16, 3.2, 2], [16, 2.8, 1], [12, 1.8, -2], [12, 1.8, -2], 50),
                lambda a, b: close_up(a, b, HERO_P),
            ]),
            "characters": {
                "hero": [kf(S_PLANT, HERO_P, 0.2, "idle", "smile"),
                         kf(B["b10"], HERO_P, 0.2, "point", "smile"),
                         kf(S_SHOUT, HERO_P, 0.2, "point", "smile")],
                "friend": hold(S_PLANT, S_SHOUT, FRIEND_P, -0.2, "idle", "smile"),
            },
        },
        {   # The reveal: TEN! THOUSAND! DEGREES! Hero points up in panic,
            # then celebrates as the rule lands — colour is temperature.
            "id": "reveal", "location": "street", "skyColor": BLUE_SKY,
            "startFrame": S_SHOUT, "endFrame": S_END,
            "fx": sun_fx,
            "cameraShots": cover(S_SHOUT, S_END, [
                lambda a, b: shot(a, b, [0, 7.4, 24.5], [0, 7.4, 24.5], [0, 4.8, -0.5], [0, 4.8, -0.5], 58),
                lambda a, b: close_up(a, b, HERO_P, shake=0.08),
                # Wide 2-shot for the celebration, same reason as the
                # plants 2-shot: the v1 medium sliced the hero's raised
                # arm and head at the left edge.
                lambda a, b: wide(a, b, [0, 0, 1.0], dist=18),
            ]),
            "characters": {
                "hero": [kf(S_SHOUT, HERO_P, 0.3, "point", "panic"),
                         kf(B["b11"], HERO_P, 0.3, "celebrate", "laugh"),
                         kf(S_END, HERO_P, 0.3, "celebrate", "laugh")],
                "friend": [kf(S_SHOUT, FRIEND_P, -0.3, "idle", "shocked"),
                           kf(B["w3"], FRIEND_P, -0.3, "idle", "panic"),
                           kf(B["b11"], FRIEND_P, -0.3, "wave", "smile"),
                           kf(S_END, FRIEND_P, -0.3, "wave", "smile")],
            },
        },
        {   # Twist, part 1: bookend aerial over the blue town.
            "id": "twist", "location": "town_overview", "skyColor": BLUE_SKY,
            "startFrame": S_END, "endFrame": T_LOOK,
            "fx": sun_fx,
            "cameraShots": [
                shot(S_END, T_LOOK, [-7, 56, 67], [-4, 50, 61], [7, 1, -7], [6, 2, -8], 55),
            ],
            "characters": {},
        },
        {   # Twist, part 2: one last look up at the blue Sun — tomorrow
            # it might be a different colour. Same street look-up as the
            # hook (sign and traffic lights out of frame by location).
            "id": "twist_look", "location": "street", "skyColor": BLUE_SKY,
            "startFrame": T_LOOK, "endFrame": END,
            "fx": sun_fx,
            "cameraShots": [
                shot(T_LOOK, END, [-5, 1.2, 9], [-5, 1.6, 7.5], SUN, SUN, 45),
            ],
            "characters": {},
        },
    ]
