"""WHY DOES ICE FLOAT? - science explainer.

Batch story: video 3 of 7.
Structure is a "why" explainer (question -> test -> answer), NOT another
"what if": the opening line IS the title question ("Why does ice float?"),
as the sky-blue and stars-twinkle Shorts did, then the setup follows.

The science: water expands when it freezes, so the same amount of water
takes up more room as ice - ice is less dense than liquid water, so it
floats. Only a small tip sticks out above the water. In winter a lake
freezes on top first; the floating ice forms a roof, the water underneath
stays liquid, and the fish keep swimming safely under the ice all winter.
If ice sank instead, lakes would freeze from the bottom up and the fish
would have nowhere left to swim. All plain-language, standard physics,
simplified for a Short.

Lead: ClassicNoob (kit {"kit": "classicnoob"}) - fresh lead for variety
(Bolt Boy led an earlier Short, Wingo led the cheese-moon Short). His friend is a
kid_girl; the teacher explains the mechanism in the classroom.

Assets: NO glass / ice-cube component exists in the engine (checked
2026-11-23). The glass + ice cube are built from fx boxes instead: a
large transparent box (the glass), a blue translucent box inside it (the
water), and a white box floating at the water line (the ice cube) - a
science-demo tank the heroes stand beside and point at. The fish payoff
reuses the BlockyFish fx from breathe_underwater, and the frozen-lake
scene reuses the ice_street location from no_friction.

Build:   python scripts/make_short.py stories/ice_floats.py --stills
Render:  node scripts/render.mjs story ice_floats  (stills + ffmpeg; NEVER renderMedia)
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, split_shots, wide  # noqa: F401

TITLE = "WHY DOES ICE FLOAT?"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "Why does ice float?", "pause": 0.10},
    {"id": "b2", "text": "In this kitchen, Noob drops an ice cube into a glass of water. And it does not sink. It floats.", "pause": 0.08},
    {"id": "b3", "text": "That is strange. Ice is solid water. And solid things usually sink to the bottom.", "pause": 0.10},
    {"id": "b4", "text": "Here is the secret. When water freezes, it spreads out. It takes up more room than the water it came from.", "pause": 0.10},
    {"id": "b5", "text": "So the same water gets bigger, and lighter for its size. Ice is less dense than liquid water.", "pause": 0.10},
    {"id": "b6", "text": "Less dense means it floats. Like a beach ball floats on a swimming pool.", "pause": 0.10},
    {"id": "b7", "text": "Look closely. Only a little bit of the ice sticks out. Most of it hides under the water.", "pause": 0.10},
    {"id": "b8", "text": "And that floating ice saves lives. In winter, the top of a lake freezes first.", "pause": 0.10},
    {"id": "b9", "text": "The ice floats and makes a roof over the lake. Underneath, the water stays liquid.", "pause": 0.10},
    {"id": "b9b", "text": "If ice sank instead, lakes would freeze from the bottom up, and the fish would have nowhere left to swim.", "pause": 0.10},
    {"id": "b10", "text": "But the ice floats. So the fish keep swimming, safe under the ice, all winter long.", "pause": 0.10},
    {"id": "b11", "text": "So ice floats because frozen water is lighter for its size. And that is why fish survive the winter.", "pause": 0.10},
    {"id": "b12", "text": "Next time you hear ice clink in a glass, remember: you are watching water break its own rule.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/moon-tide.wav",
    "under_voice": 0.022,
    "gaps": 0.05,
}

SFX = [
    ("b1", "pop", {"f": 600}),
    ("b1+0.5", "whoosh"),
    ("b2+0.5", "pop", {"f": 600}),
    ("b4+0.5", "sparkle"),
    ("b5+0.5", "pop", {"f": 600}),
    ("b6+0.5", "sparkle"),
    ("b7+0.5", "pop", {"f": 600}),
    ("b9+0.5", "reveal"),
    ("b10+0.5", "bubbles"),
    ("b11+0.5", "reveal"),
    ("b12+1.5", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
CAST = {
    # ClassicNoob: the kit character as story lead. His expression is a
    # valid story ExpressionId ("smile"/"shocked", not a kit-only one).
    "hero": {"kit": "classicnoob"},
    "friend": {"extends": "kid_girl", "hair": {"style": "ponytail", "color": "blonde"},
               "top": {"style": "hoodie", "color": "pink", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"color": "white", "sole": "white"}},
    "teacher": {"extends": "teacher_woman", "skin": "fair", "hair": {"style": "bun", "color": "blonde"}},
}


# 4. SCENES ---------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S2 = B["b4"] - 1    # classroom: the mechanism
    S3 = B["b8"] - 1    # ice street: the frozen lake
    S4 = B["b9"] - 1    # undersea: the ice roof and the fish
    S5 = B["b11"] - 1   # living room: closer

    HERO_P = [-4.5, 0, 0.5]
    FRIEND_P = [4.5, 0, 0.5]

    # The glass of water, built from fx boxes (no glass/ice-cube component
    # exists): a big transparent tank standing on the floor between the two
    # heroes, blue water inside, white ice cube floating at the water line.
    # FIX ROUND 1 (preview stills): the v1 cube (1.2, centre 2.9, only 0.4
    # above the water) was invisible in every hook shot, and the glass
    # (opacity 0.22) did not read as a container. v2: bigger cube (1.5)
    # riding 0.75 above the waterline, faint emissive so it pops against
    # the water, glass 0.35, water deeper blue at 0.55.
    # FIX ROUND 2 (preview stills): the v2 cube STILL did not render - a
    # transparent box nested inside two other transparent boxes gets
    # depth-rejected by the glass/water faces in front of it. v3 drops the
    # cube's opacity entirely: as an opaque box it renders in the opaque
    # pass first, and the translucent glass/water blend over it.
    glass_fx = [
        {"id": "glass", "shape": "box", "size": [3, 4, 3], "color": "#DBEAFE",
         "roughness": 0.1, "opacity": 0.35,
         "keyframes": [{"frame": 0, "position": [0, 2, -2.5]}, {"frame": S2, "position": [0, 2, -2.5]}]},
        {"id": "water", "shape": "box", "size": [2.7, 3, 2.7], "color": "#2563EB",
         "roughness": 0.2, "opacity": 0.55,
         "keyframes": [{"frame": 0, "position": [0, 1.6, -2.5]}, {"frame": S2, "position": [0, 1.6, -2.5]}]},
        {"id": "icecube", "shape": "box", "size": [1.5, 1.5, 1.5], "color": "#FFFFFF",
         "emissive": "#E0F2FE", "emissiveIntensity": 0.35,
         "roughness": 0.3,
         "keyframes": [{"frame": 0, "position": [0, 3.1, -2.5]}, {"frame": S2, "position": [0, 3.1, -2.5]}]},
    ]

    # The fish under the ice (BlockyFish, as in breathe_underwater): swims
    # left to right below the ice roof, 1.5+ studs clear of any actor.
    # FIX ROUND 1: v1 path ran x -7..6.5 and the fish was clipped at the
    # left edge in the first undersea shot and at the right edge in the
    # last one. v2 keeps it inside the frame: -5..5.5.
    # FIX ROUND 2: v2 still clipped the tail at the left (the fish is
    # ~3.5 studs long at scale 1.2 and the portrait frame is only ~10.5
    # wide at its depth). v3: path -3.5..4.5, cameras pulled back a little.
    fish_kf = [{"frame": S4, "position": [-3.5, 5.5, -4]},
               {"frame": B["b9b"], "position": [0.5, 5.5, -4]},
               {"frame": S5, "position": [4.5, 5.5, -4]}]
    fish_fx = [{"id": "fish", "shape": "fish", "scale": 1.2, "color": "#df6414",
                "rotation": [0, HALF, 0], "keyframes": fish_kf}]
    # The ice roof over the lake, seen from underneath: a wide pale slab.
    roof_fx = [{"id": "iceroof", "shape": "box", "size": [16, 1.2, 8], "color": "#E0F2FE",
                "roughness": 0.3, "opacity": 0.9,
                "keyframes": [{"frame": S4, "position": [0, 10, -4]}, {"frame": S5, "position": [0, 10, -4]}]}]
    bubbles_fx = [{"id": "bubbles", "shape": "bubbles", "scale": 0.7, "color": "#c4efff",
                   "keyframes": [{"frame": S4, "position": [3, 4, -3]}, {"frame": S5, "position": [3, 4, -3]}]}]

    scenes = []

    # 1. HOOK - kitchen. The glass tank between them; both point at the floating cube ----
    # Static wide (sky_blue fix): wide()'s push drags interior edges and reads as flicker.
    scenes.append({
        "id": "hook", "location": "kitchen", "variant": "blue",
        "startFrame": 0, "endFrame": S2,
        "cameraShots": cover(0, S2, [lambda a, b: shot(a, b, [0, 7.4, 24.5], [0, 7.4, 24.5], [0, 4.8, -0.5], [0, 4.8, -0.5], 58),
                                      lambda a, b: close_up(a, b, HERO_P),
                                      lambda a, b: medium(a, b, [0, 0, -1])]),
        "fx": glass_fx,
        "characters": {
            # ClassicNoob's face is the fixed classic smile (ClassicNoob.tsx:
            # canvas face, not the shared expression system), so "shocked"
            # would render as a smile anyway. "smile" states it truthfully.
            "hero": hold(0, S2, HERO_P, 0.2, "point", "smile"),
            "friend": hold(0, S2, FRIEND_P, -0.2, "point", "shocked"),
        },
    })

    # 2. CLASSROOM - the mechanism: water spreads out when it freezes ----------------------
    scenes.append({
        "id": "mechanism", "location": "classroom",
        "boardText": ["WATER FREEZES", "AND SPREADS OUT", "ICE IS LESS DENSE", "LESS DENSE = FLOATS"],
        "startFrame": S2, "endFrame": S3,
        "cameraShots": cover(S2, S3, [lambda a, b: shot(a, b, [0, 7.4, 23], [0, 7.4, 23], [0, 4.8, -1], [0, 4.8, -1], 58),
                                       lambda a, b: close_up(a, b, [-0.5, 0, 0.5]),
                                       lambda a, b: close_up(a, b, [-4.5, 0, -4.5])]),
        "characters": {
            # FIX ROUND 2: teacher moved -3.0 -> -4.5: with the 4-line board
            # her head covered the "LE" of "LESS DENSE = FLOATS" in the wide.
            "teacher": hold(S2, S3, [-4.5, 0, -4.5], 0.5, "point", "deadpan", "pointer"),
            "hero": hold(S2, S3, [-0.5, 0, 0.5], 0, "idle", "smile"),
            "friend": hold(S2, S3, [4.0, 0, 0.5], 0, "idle", "smile"),
        },
    })

    # 3. ICE STREET - the frozen lake. Both look down at the ice under their feet -----------
    scenes.append({
        "id": "lake", "location": "ice_street", "skyColor": "#BFDBFE",
        "startFrame": S3, "endFrame": S4,
        "cameraShots": cover(S3, S4, [lambda a, b: wide(a, b, [0, 0, 0.5], 24),
                                       lambda a, b: close_up(a, b, HERO_P),
                                       lambda a, b: close_up(a, b, FRIEND_P)]),
        "characters": {
            "hero": hold(S3, S4, HERO_P, 0.2, "point", "smile"),
            "friend": hold(S3, S4, FRIEND_P, -0.2, "idle", "smile"),
        },
    })

    # 4. UNDERSEA - under the ice roof. No actors: the fish swims beneath the slab ---------
    scenes.append({
        "id": "underice", "location": "undersea", "skyColor": "#1D6FB8",
        "startFrame": S4, "endFrame": S5,
        "cameraShots": cover(S4, S5, [lambda a, b: shot(a, b, [0, 5, 16], [0, 5.5, 15], [0, 7, -4], [0, 7, -4], 55),
                                       lambda a, b: shot(a, b, [7, 4.5, 14], [6, 5, 14], [-2, 6, -4], [-2, 6, -4], 55)]),
        "fx": fish_fx + roof_fx + bubbles_fx,
        "characters": {},
    })

    # 5. LIVING ROOM - closer ----------------------------------------------------------------
    scenes.append({
        "id": "closer", "location": "living_room", "variant": "blue",
        "startFrame": S5, "endFrame": END,
        "cameraShots": cover(S5, END, [lambda a, b: wide(a, b, [0, 0, 0.4], 24),
                                         lambda a, b: close_up(a, b, HERO_P),
                                         lambda a, b: close_up(a, b, FRIEND_P)]),
        "characters": {
            "hero": [kf(S5, HERO_P, 0.9, "idle", "deadpan"),
                     kf(B["b12"], HERO_P, 0.9, "idle", "smile"),
                     kf(END, HERO_P, 0.9, "idle", "smile")],
            "friend": [kf(S5, FRIEND_P, -0.9, "wave", "smile"),
                       kf(END, FRIEND_P, -0.9, "wave", "smile")],
        },
    })

    return scenes
