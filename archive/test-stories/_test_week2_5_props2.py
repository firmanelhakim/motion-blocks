"""TEST-ONLY story — verifies the nine Week 2-5 builds from Gemini prompts
7-15: light-speed spaceship, robot, rainy-street umbrella, dream-world
floating props, dry seabed (boat + cracks), heartbeat
monitor, giant phone, candle. NEVER for publishing. Run:
    python scripts/make_short.py stories/_test_week2_5_props2.py --stills
"""
import math
import random

from shorts.scene import (  # noqa: F401
    HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, orbit,
    shot, split_shots, static_shot, wide,
)

TITLE = "TEST WEEK2-5 PROPS 2"

BEATS = [
    {"id": "b1", "text": "In this world, a ship can fly faster than light itself.", "pause": 0.08},
    {"id": "b2", "text": "White hull, orange wings, and engines glowing blue behind it.", "pause": 0.08},
    {"id": "b3", "text": "And one day, the robots will do all the homework.", "pause": 0.08},
    {"id": "b4", "text": "A screen for a face, two glowing eyes, and a stack of books.", "pause": 0.08},
    {"id": "b5", "text": "When it never stops raining, one yellow umbrella is enough.", "pause": 0.08},
    {"id": "b6", "text": "The rain falls, the street shines, and the boy stays dry.", "pause": 0.08},
    {"id": "b7", "text": "And at night, the boy dreams under a glowing crescent moon.", "pause": 0.08},
    {"id": "b8", "text": "Books and clocks and lamps float above his bed while he sleeps.", "pause": 0.08},
    {"id": "b9", "text": "But what if the oceans dried up, and the sea floor cracked?", "pause": 0.08},
    {"id": "b10", "text": "A wooden boat sits beached on the dry earth, beside a whale's bones.", "pause": 0.08},
    {"id": "b11", "text": "And what if humans could fly, on giant white wings?", "pause": 0.08},
    {"id": "b12", "text": "Layered feathers, fanning out from the back, wider than the shoulders.", "pause": 0.08},
    {"id": "b13", "text": "If your heart stopped for ten seconds, a monitor would watch it.", "pause": 0.08},
    {"id": "b14", "text": "A green line zigzags across the screen, while the boy lies still.", "pause": 0.08},
    {"id": "b15", "text": "And what if phones never needed charging, and grew giant?", "pause": 0.08},
    {"id": "b16", "text": "A black phone towers over the boy, taller than the whole room.", "pause": 0.08},
    {"id": "b17", "text": "And if there was no electricity for a day, one candle would do.", "pause": 0.08},
    {"id": "b18", "text": "A small white candle, and a warm glow on the boy's face.", "pause": 0.3},
]

MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05}
SFX = [
    ("b1", "whoosh"),
    ("b3+0.5", "pop"),
    ("b5+0.5", "sparkle"),
    ("b7+0.5", "bell_low"),
    ("b9+0.5", "riser"),
    ("b11+0.5", "whoosh"),
    ("b13+0.5", "pop_down"),
    ("b15+0.5", "reveal"),
    ("b17+0.5", "sad"),
    ("b18+0.5", "twist"),
]

CAST = {
    "hero": {"extends": "kid_boy", "hair": {"style": "spikyAnime", "color": "blue"},
             "top": {"style": "hoodie", "color": "royal", "secondary": "white"},
             "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"color": "white", "sole": "white"},
             "freckles": True},
    "friend": {"extends": "kid_girl", "hair": {"style": "ponytail", "color": "blonde"},
               "top": {"style": "hoodie", "color": "pink", "secondary": "white"},
               "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"color": "white", "sole": "white"}},
    # Boy in the rain (Gemini rainy-street reference): yellow raincoat.
    "stormboy": {"extends": "kid_boy", "hair": {"style": "messyFringe", "color": "brown"},
                 "top": {"style": "hoodie", "color": "yellow", "secondary": "white"},
                 "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"color": "white", "sole": "white"}},
    # Sleeping boy (Gemini dream-world + monitor references): brown hair,
    # blue pyjamas.
    "sleeper": {"extends": "kid_boy", "hair": {"style": "messyFringe", "color": "brown"},
                "top": {"style": "pullover", "color": "blue", "secondary": "blue"},
                "bottom": {"style": "pants", "color": "blue"}, "shoes": {"color": "white", "sole": "white"}},
    # Boy with the candle (Gemini candle reference): blue shirt, jeans.
    "candleboy": {"extends": "kid_boy", "hair": {"style": "messyFringe", "color": "brown"},
                  "top": {"style": "tshirt", "color": "blue", "secondary": "white"},
                  "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"color": "white", "sole": "white"}},
    # Boy facing the giant phone (Gemini phone reference): red shirt, no hair.
    "phoneboy": {"extends": "kid_boy", "hair": {"style": "none"},
                 "top": {"style": "tshirt", "color": "red", "secondary": "white"},
                 "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"color": "white", "sole": "white"}},
}


def _streaks(a, b):
    """Radial warp streaks (copied from _test_week1_props.py): 12 thin boxes
    around frame centre [0, 7, -18], each rotated to point outward and
    keyframed to fly outward over the shot, so a still reads as light-speed
    lines radiating from the centre. The centre sits high in the sky so no
    streak lies flat across the horizon behind the actors."""
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


def _ship(a, b):
    """Blocky spaceship (Gemini light-speed reference): white fuselage,
    faceted glowing nose, blue cockpit, swept wings with orange trailing
    edges, orange tail fin, two glowing blue engines. Flies toward the
    camera over the shot (z -8 -> -4). Every part tracks the same two
    keyframes so the ship moves as one piece."""
    parts = [
        # fuselage
        {"id": "ship-body", "shape": "box", "size": [2.6, 2.0, 7.0],
         "color": "#F8FAFC", "roughness": 0.35, "off": [0, 0, 0]},
        # faceted nose cone (front, toward camera) — kept small so it reads
        # as a nose, not a ball swallowing the fuselage
        {"id": "ship-nose", "shape": "facet", "radius": 0.9, "detail": 1,
         "color": "#E0F2FE", "emissive": "#7DD3FC", "emissiveIntensity": 0.5,
         "roughness": 0.3, "off": [0, 0, 3.7]},
        # cockpit window on top-front
        {"id": "ship-cockpit", "shape": "box", "size": [1.4, 0.6, 2.5],
         "color": "#0EA5E9", "emissive": "#38BDF8", "emissiveIntensity": 0.8,
         "roughness": 0.3, "off": [0, 1.1, 1.8]},
        # swept wings (left/right) + orange trailing-edge strips
        {"id": "ship-wing-l", "shape": "box", "size": [4.5, 0.3, 2.2],
         "color": "#F8FAFC", "roughness": 0.35, "off": [-3.2, -0.4, -1.5],
         "rotation": [0, -0.35, -0.12]},
        {"id": "ship-wing-r", "shape": "box", "size": [4.5, 0.3, 2.2],
         "color": "#F8FAFC", "roughness": 0.35, "off": [3.2, -0.4, -1.5],
         "rotation": [0, 0.35, 0.12]},
        {"id": "ship-edge-l", "shape": "box", "size": [4.5, 0.32, 0.6],
         "color": "#F97316", "emissive": "#FB923C", "emissiveIntensity": 0.6,
         "roughness": 0.4, "off": [-3.2, -0.4, -2.4], "rotation": [0, -0.35, -0.12]},
        {"id": "ship-edge-r", "shape": "box", "size": [4.5, 0.32, 0.6],
         "color": "#F97316", "emissive": "#FB923C", "emissiveIntensity": 0.6,
         "roughness": 0.4, "off": [3.2, -0.4, -2.4], "rotation": [0, 0.35, 0.12]},
        # orange tail fin on top-rear
        {"id": "ship-fin", "shape": "box", "size": [0.3, 2.2, 2.0],
         "color": "#F97316", "emissive": "#FB923C", "emissiveIntensity": 0.4,
         "roughness": 0.4, "off": [0, 1.8, -2.8], "rotation": [0.2, 0, 0]},
        # glowing engines at the back
        {"id": "ship-eng-l", "shape": "box", "size": [1.2, 1.2, 1.0],
         "color": "#1E293B", "emissive": "#38BDF8", "emissiveIntensity": 2.0,
         "roughness": 0.3, "off": [-1.1, 0, -3.6]},
        {"id": "ship-eng-r", "shape": "box", "size": [1.2, 1.2, 1.0],
         "color": "#1E293B", "emissive": "#38BDF8", "emissiveIntensity": 2.0,
         "roughness": 0.3, "off": [1.1, 0, -3.6]},
        {"id": "ship-flame-l", "shape": "sphere", "radius": 0.9,
         "color": "#7DD3FC", "emissive": "#38BDF8", "emissiveIntensity": 2.5,
         "roughness": 0.3, "opacity": 0.7, "off": [-1.1, 0, -4.4]},
        {"id": "ship-flame-r", "shape": "sphere", "radius": 0.9,
         "color": "#7DD3FC", "emissive": "#38BDF8", "emissiveIntensity": 2.5,
         "roughness": 0.3, "opacity": 0.7, "off": [1.1, 0, -4.4]},
    ]
    out = []
    for part in parts:
        off = part.pop("off")
        out.append({**part,
                    "keyframes": [{"frame": a, "position": [off[0], 7 + off[1], -8 + off[2]]},
                                  {"frame": b, "position": [off[0], 7 + off[1], -4 + off[2]]}]})
    return out


def _robot(a, b):
    """Robot character (Gemini robot reference), built as fx because the
    character constructor's head is a fixed lathe — it cannot take a screen
    face. White/blue boxy body, dark screen face with two glowing cyan
    eyes, red-ball antenna, holding a stack of three books (red, green,
    blue) against its chest. Static over the shot."""
    base = [
        # head + screen face + glowing eyes + antenna
        {"id": "robot-head", "shape": "box", "size": [1.9, 1.9, 1.9],
         "color": "#F8FAFC", "roughness": 0.35, "p": [0, 4.9, 0]},
        {"id": "robot-screen", "shape": "box", "size": [1.5, 1.1, 0.1],
         "color": "#0F172A", "emissive": "#0F172A", "emissiveIntensity": 0.3,
         "roughness": 0.3, "p": [0, 5.0, 0.98]},
        {"id": "robot-eye-l", "shape": "sphere", "radius": 0.3,
         "color": "#22D3EE", "emissive": "#22D3EE", "emissiveIntensity": 2.5,
         "roughness": 0.3, "p": [-0.4, 5.05, 1.06]},
        {"id": "robot-eye-r", "shape": "sphere", "radius": 0.3,
         "color": "#22D3EE", "emissive": "#22D3EE", "emissiveIntensity": 2.5,
         "roughness": 0.3, "p": [0.4, 5.05, 1.06]},
        {"id": "robot-antenna", "shape": "box", "size": [0.12, 0.9, 0.12],
         "color": "#94A3B8", "roughness": 0.4, "p": [0, 6.3, 0]},
        {"id": "robot-antenna-ball", "shape": "sphere", "radius": 0.35,
         "color": "#EF4444", "emissive": "#DC2626", "emissiveIntensity": 1.5,
         "roughness": 0.3, "p": [0, 6.9, 0]},
        # torso + blue chest panel, arms, blue legs, feet
        {"id": "robot-torso", "shape": "box", "size": [2.3, 1.9, 1.3],
         "color": "#F8FAFC", "roughness": 0.35, "p": [0, 3.1, 0]},
        {"id": "robot-chest", "shape": "box", "size": [1.4, 0.9, 0.1],
         "color": "#2563EB", "roughness": 0.4, "p": [0, 3.3, 0.68]},
        {"id": "robot-arm-l", "shape": "box", "size": [0.6, 1.9, 0.6],
         "color": "#F8FAFC", "roughness": 0.35, "p": [-1.5, 3.1, 0]},
        {"id": "robot-arm-r", "shape": "box", "size": [0.6, 1.9, 0.6],
         "color": "#F8FAFC", "roughness": 0.35, "p": [1.5, 3.1, 0]},
        {"id": "robot-leg-l", "shape": "box", "size": [0.8, 1.7, 0.8],
         "color": "#2563EB", "roughness": 0.4, "p": [-0.6, 0.85, 0]},
        {"id": "robot-leg-r", "shape": "box", "size": [0.8, 1.7, 0.8],
         "color": "#2563EB", "roughness": 0.4, "p": [0.6, 0.85, 0]},
        {"id": "robot-foot-l", "shape": "box", "size": [0.9, 0.4, 1.2],
         "color": "#1E40AF", "roughness": 0.4, "p": [-0.6, 0.2, 0.1]},
        {"id": "robot-foot-r", "shape": "box", "size": [0.9, 0.4, 1.2],
         "color": "#1E40AF", "roughness": 0.4, "p": [0.6, 0.2, 0.1]},
        # stack of three books held against the chest — red on top so it
        # contrasts with the blue chest panel behind it
        {"id": "robot-book-blue", "shape": "box", "size": [1.2, 0.25, 0.9],
         "color": "#2563EB", "roughness": 0.5, "p": [0, 2.35, 0.95]},
        {"id": "robot-book-green", "shape": "box", "size": [1.2, 0.25, 0.9],
         "color": "#16A34A", "roughness": 0.5, "p": [0, 2.62, 0.95]},
        {"id": "robot-book-red", "shape": "box", "size": [1.2, 0.25, 0.9],
         "color": "#EF4444", "roughness": 0.5, "p": [0, 2.89, 0.95]},
    ]
    out = []
    for e in base:
        p = e.pop("p")
        out.append({**e, "keyframes": [{"frame": a, "position": p},
                                       {"frame": b, "position": p}]})
    return out


def _umbrella(a, b):
    """Big yellow umbrella (Gemini rainy-street reference): a dome canopy
    over the boy's head, a shaft down to his right hand, a finial on top.
    Static over the shot."""
    return [
        {"id": "umbrella-canopy", "shape": "dome", "radius": 2.8,
         "color": "#FACC15", "emissive": "#FDE047", "emissiveIntensity": 0.4,
         "roughness": 0.5,
         "keyframes": [{"frame": a, "position": [-0.3, 7.0, 0.5]},
                      {"frame": b, "position": [-0.3, 7.0, 0.5]}]},
        {"id": "umbrella-shaft", "shape": "box", "size": [0.14, 5.0, 0.14],
         "color": "#78350F", "roughness": 0.6,
         "keyframes": [{"frame": a, "position": [-1.2, 4.75, 0.5]},
                      {"frame": b, "position": [-1.2, 4.75, 0.5]}]},
        {"id": "umbrella-tip", "shape": "sphere", "radius": 0.18,
         "color": "#78350F", "roughness": 0.6,
         "keyframes": [{"frame": a, "position": [-0.3, 9.9, 0.5]},
                      {"frame": b, "position": [-0.3, 9.9, 0.5]}]},
        {"id": "umbrella-hook", "shape": "box", "size": [0.5, 0.14, 0.14],
         "color": "#78350F", "roughness": 0.6,
         "keyframes": [{"frame": a, "position": [-1.0, 1.9, 0.5]},
                      {"frame": b, "position": [-1.0, 1.9, 0.5]}]},
    ]


def _rain(a, b):
    """Rain streaks (copied from _test_week2_5_props.py): thin translucent
    slanted boxes falling over the scene."""
    rnd = random.Random(20261117)
    fx = []
    for i in range(40):
        x = -16 + rnd.uniform(0, 34)
        y = 4 + rnd.uniform(0, 22)
        z = -12 + rnd.uniform(0, 20)
        fx.append({"id": f"rain{i}", "shape": "box", "size": [0.18, 3.2, 0.18],
                   "color": "#BFDBFE", "emissive": "#DBEAFE", "emissiveIntensity": 0.5,
                   "roughness": 0.4, "opacity": 0.45, "rotation": [0, 0, 0.18],
                   "keyframes": [{"frame": a, "position": [x, y, z]},
                                 {"frame": b, "position": [x, y - 14, z]}]})
    return fx


def _wet_street(a, b):
    """Wet street (simplified _wet from _test_week2_5_props.py): a dark
    glossy slab over the road. No true mirror reflection — this is the
    honest limit, as with the lightning wide."""
    return [
        {"id": "wet", "shape": "box", "size": [34, 0.06, 22], "color": "#1E293B",
         "roughness": 0.08,
         "keyframes": [{"frame": a, "position": [1, 0.03, 2]},
                      {"frame": b, "position": [1, 0.03, 2]}]},
    ]


def _dream(a, b):
    """Dream-world floating props (Gemini dream-world reference): a giant
    glowing crescent moon, floating open books, a floating alarm clock, a
    floating lamp, and small clouds. Everything bobs slowly (two keyframes,
    +/-0.5 in y) so the stills read as floating, not fixed."""
    fx = [
        # crescent moon, upper-left, in front of the back wall
        {"id": "dream-moon", "shape": "crescent", "radius": 2.4,
         "color": "#FDE68A", "emissive": "#FBBF24", "emissiveIntensity": 1.6,
         "roughness": 0.5, "rotation": [0, 0, 0.15],
         "keyframes": [{"frame": a, "position": [-7, 10.5, -5]},
                      {"frame": b, "position": [-7, 11.5, -5]}]},
        # small clouds (white ball clusters)
        {"id": "dream-cloud1a", "shape": "sphere", "radius": 1.2,
         "color": "#F8FAFC", "roughness": 0.6, "opacity": 0.9,
         "keyframes": [{"frame": a, "position": [-10, 10, -6]},
                      {"frame": b, "position": [-10, 10.6, -6]}]},
        {"id": "dream-cloud1b", "shape": "sphere", "radius": 0.9,
         "color": "#F8FAFC", "roughness": 0.6, "opacity": 0.9,
         "keyframes": [{"frame": a, "position": [-8.8, 10.4, -6]},
                      {"frame": b, "position": [-8.8, 11.0, -6]}]},
        {"id": "dream-cloud2a", "shape": "sphere", "radius": 1.0,
         "color": "#F8FAFC", "roughness": 0.6, "opacity": 0.9,
         "keyframes": [{"frame": a, "position": [-3, 12.5, -6]},
                      {"frame": b, "position": [-3, 13.0, -6]}]},
        {"id": "dream-cloud2b", "shape": "sphere", "radius": 0.8,
         "color": "#F8FAFC", "roughness": 0.6, "opacity": 0.9,
         "keyframes": [{"frame": a, "position": [-1.9, 12.8, -6]},
                      {"frame": b, "position": [-1.9, 13.3, -6]}]},
        {"id": "dream-cloud3a", "shape": "sphere", "radius": 0.9,
         "color": "#F8FAFC", "roughness": 0.6, "opacity": 0.9,
         "keyframes": [{"frame": a, "position": [-4, 9, -2]},
                      {"frame": b, "position": [-4, 9.5, -2]}]},
        # open book 1 (red): two thin angled pages
        {"id": "dream-book1-l", "shape": "box", "size": [1.1, 0.12, 0.8],
         "color": "#EF4444", "roughness": 0.5, "rotation": [0, 0, 0.4],
         "keyframes": [{"frame": a, "position": [-5.5, 8, -3]},
                      {"frame": b, "position": [-5.5, 8.5, -3]}]},
        {"id": "dream-book1-r", "shape": "box", "size": [1.1, 0.12, 0.8],
         "color": "#EF4444", "roughness": 0.5, "rotation": [0, 0, -0.4],
         "keyframes": [{"frame": a, "position": [-4.5, 8, -3]},
                      {"frame": b, "position": [-4.5, 8.5, -3]}]},
        # open book 2 (blue)
        {"id": "dream-book2-l", "shape": "box", "size": [1.1, 0.12, 0.8],
         "color": "#2563EB", "roughness": 0.5, "rotation": [0, 0, 0.4],
         "keyframes": [{"frame": a, "position": [-7.5, 7, 1]},
                      {"frame": b, "position": [-7.5, 7.5, 1]}]},
        {"id": "dream-book2-r", "shape": "box", "size": [1.1, 0.12, 0.8],
         "color": "#2563EB", "roughness": 0.5, "rotation": [0, 0, -0.4],
         "keyframes": [{"frame": a, "position": [-6.5, 7, 1]},
                      {"frame": b, "position": [-6.5, 7.5, 1]}]},
        # alarm clock: white face + two gold bells
        {"id": "dream-clock", "shape": "box", "size": [1.2, 1.2, 0.3],
         "color": "#F8FAFC", "roughness": 0.4,
         "keyframes": [{"frame": a, "position": [-9, 9, -5]},
                      {"frame": b, "position": [-9, 9.5, -5]}]},
        {"id": "dream-clock-bell-l", "shape": "sphere", "radius": 0.3,
         "color": "#FACC15", "emissive": "#FDE047", "emissiveIntensity": 0.6,
         "roughness": 0.4,
         "keyframes": [{"frame": a, "position": [-9.5, 9.8, -5]},
                      {"frame": b, "position": [-9.5, 10.3, -5]}]},
        {"id": "dream-clock-bell-r", "shape": "sphere", "radius": 0.3,
         "color": "#FACC15", "emissive": "#FDE047", "emissiveIntensity": 0.6,
         "roughness": 0.4,
         "keyframes": [{"frame": a, "position": [-8.5, 9.8, -5]},
                      {"frame": b, "position": [-8.5, 10.3, -5]}]},
        # lamp: glowing shade + stem + base
        {"id": "dream-lamp-shade", "shape": "box", "size": [1.2, 1.0, 1.2],
         "color": "#FDE68A", "emissive": "#FBBF24", "emissiveIntensity": 1.2,
         "roughness": 0.5,
         "keyframes": [{"frame": a, "position": [-2, 7, -4]},
                      {"frame": b, "position": [-2, 7.5, -4]}]},
        {"id": "dream-lamp-stem", "shape": "box", "size": [0.2, 1.0, 0.2],
         "color": "#78350F", "roughness": 0.6,
         "keyframes": [{"frame": a, "position": [-2, 6, -4]},
                      {"frame": b, "position": [-2, 6.5, -4]}]},
        {"id": "dream-lamp-base", "shape": "box", "size": [0.8, 0.2, 0.8],
         "color": "#78350F", "roughness": 0.6,
         "keyframes": [{"frame": a, "position": [-2, 5.4, -4]},
                      {"frame": b, "position": [-2, 5.9, -4]}]},
    ]
    return fx


def _monitor(a, b):
    """Heartbeat monitor (Gemini monitor reference): white cabinet with a
    dark screen, a green zigzag waveform of thin emissive boxes on the
    screen, a base, and a green cable (a chain of boxes, undersea-cable
    technique) curving from the monitor to the bed. Static over the shot."""
    fx = [
        {"id": "monitor-cabinet", "shape": "box", "size": [2.8, 5.5, 1.6],
         "color": "#F1F5F9", "roughness": 0.4, "p": [-11.5, 2.75, -3.5]},
        {"id": "monitor-base", "shape": "box", "size": [2.0, 0.4, 1.4],
         "color": "#CBD5E1", "roughness": 0.5, "p": [-11.5, 0.2, -3.5]},
        {"id": "monitor-screen", "shape": "box", "size": [2.3, 3.6, 0.1],
         "color": "#0F172A", "emissive": "#0F172A", "emissiveIntensity": 0.3,
         "roughness": 0.3, "p": [-11.5, 3.6, -2.65]},
    ]
    # green heartbeat waveform across the screen (z just in front of it)
    pts = [(-12.4, 3.6), (-12.0, 3.6), (-11.9, 4.5), (-11.8, 3.1),
           (-11.7, 4.2), (-11.6, 3.6), (-11.2, 3.6), (-11.1, 4.5),
           (-11.0, 3.1), (-10.9, 4.2), (-10.8, 3.6), (-10.6, 3.6)]
    for i in range(len(pts) - 1):
        (x1, y1), (x2, y2) = pts[i], pts[i + 1]
        length = math.hypot(x2 - x1, y2 - y1)
        fx.append({"id": f"monitor-wave{i}", "shape": "box",
                   "size": [length, 0.12, 0.05],
                   "color": "#22C55E", "emissive": "#22C55E", "emissiveIntensity": 1.8,
                   "roughness": 0.3, "rotation": [0, 0, math.atan2(y2 - y1, x2 - x1)],
                   "p": [(x1 + x2) / 2, (y1 + y2) / 2, -2.58]})
    # green cable from the monitor to the bed (sagging curve)
    cable_pts = []
    for i in range(7):
        t = i / 6
        x = -10.5 + 2.0 * t
        z = -3.2 - 1.3 * t
        y = 1.5 + 0.9 * t - 0.4 * math.sin(math.pi * t)
        cable_pts.append((x, y, z))
    for i in range(len(cable_pts) - 1):
        (x1, y1, z1), (x2, y2, z2) = cable_pts[i], cable_pts[i + 1]
        length = math.hypot(x2 - x1, y2 - y1, z2 - z1)
        fx.append({"id": f"monitor-cable{i}", "shape": "box",
                   "size": [0.3, 0.3, length],
                   "color": "#16A34A", "emissive": "#22C55E", "emissiveIntensity": 0.5,
                   "roughness": 0.5,
                   "rotation": [math.atan2(y2 - y1, math.hypot(x2 - x1, z2 - z1)),
                                math.atan2(x2 - x1, z2 - z1), 0],
                   "p": [(x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2]})
    out = []
    for e in fx:
        p = e.pop("p")
        out.append({**e, "keyframes": [{"frame": a, "position": p},
                                       {"frame": b, "position": p}]})
    return out


def _phone(a, b):
    """Giant phone (Gemini phone reference): a huge black smartphone towering
    over the boy — black frame, two-tone blue wallpaper, app-icon grid, dock,
    status bar with camera dot + time + battery, side buttons. No reflection
    (the maintainer: not needed; a real reflection is impossible anyway). Static."""
    fx = [
        {"id": "phone-frame", "shape": "box", "size": [8.5, 16.5, 1.0],
         "color": "#0F172A", "roughness": 0.3,
         "keyframes": [{"frame": a, "position": [2, 8.25, -3]},
                      {"frame": b, "position": [2, 8.25, -3]}]},
        {"id": "phone-screen", "shape": "box", "size": [7.6, 15.2, 0.12],
         "color": "#1E293B", "roughness": 0.1,
         "keyframes": [{"frame": a, "position": [2, 8.25, -2.45]},
                      {"frame": b, "position": [2, 8.25, -2.45]}]},
        {"id": "phone-btn1", "shape": "box", "size": [0.15, 1.0, 0.3],
         "color": "#334155", "roughness": 0.4,
         "keyframes": [{"frame": a, "position": [6.3, 10, -3]},
                      {"frame": b, "position": [6.3, 10, -3]}]},
        {"id": "phone-btn2", "shape": "box", "size": [0.15, 1.0, 0.3],
         "color": "#334155", "roughness": 0.4,
         "keyframes": [{"frame": a, "position": [6.3, 8, -3]},
                      {"frame": b, "position": [6.3, 8, -3]}]},
        # two-tone blue wallpaper
        {"id": "phone-wall-top", "shape": "box", "size": [7.6, 7.6, 0.05],
         "color": "#3B82F6", "roughness": 0.4,
         "keyframes": [{"frame": a, "position": [2, 12.05, -2.375]},
                      {"frame": b, "position": [2, 12.05, -2.375]}]},
        {"id": "phone-wall-bot", "shape": "box", "size": [7.6, 7.6, 0.05],
         "color": "#1E40AF", "roughness": 0.4,
         "keyframes": [{"frame": a, "position": [2, 4.45, -2.375]},
                      {"frame": b, "position": [2, 4.45, -2.375]}]},
        # status bar: camera dot, time pill, battery
        {"id": "phone-cam", "shape": "sphere", "radius": 0.22,
         "color": "#0F172A", "roughness": 0.2,
         "keyframes": [{"frame": a, "position": [2, 15.0, -2.36]},
                      {"frame": b, "position": [2, 15.0, -2.36]}]},
        {"id": "phone-time", "shape": "box", "size": [1.3, 0.4, 0.05],
         "color": "#F8FAFC", "roughness": 0.4,
         "keyframes": [{"frame": a, "position": [0.0, 15.0, -2.36]},
                      {"frame": b, "position": [0.0, 15.0, -2.36]}]},
        {"id": "phone-batt", "shape": "box", "size": [0.8, 0.4, 0.05],
         "color": "#F8FAFC", "roughness": 0.4,
         "keyframes": [{"frame": a, "position": [4.9, 15.0, -2.36]},
                      {"frame": b, "position": [4.9, 15.0, -2.36]}]},
        {"id": "phone-batt-fill", "shape": "box", "size": [0.5, 0.25, 0.05],
         "color": "#22C55E", "roughness": 0.4,
         "keyframes": [{"frame": a, "position": [4.85, 15.0, -2.34]},
                      {"frame": b, "position": [4.85, 15.0, -2.34]}]},
        # dock bar + home indicator
        {"id": "phone-dock", "shape": "box", "size": [6.8, 1.7, 0.05],
         "color": "#F8FAFC", "roughness": 0.4, "opacity": 0.25,
         "keyframes": [{"frame": a, "position": [2, 2.7, -2.36]},
                      {"frame": b, "position": [2, 2.7, -2.36]}]},
        {"id": "phone-home", "shape": "box", "size": [1.8, 0.2, 0.05],
         "color": "#F8FAFC", "roughness": 0.4,
         "keyframes": [{"frame": a, "position": [2, 1.15, -2.36]},
                      {"frame": b, "position": [2, 1.15, -2.36]}]},
    ]
    # app-icon grid: 5 rows x 4 cols, then 4 dock icons
    colors = ["#EF4444", "#22C55E", "#3B82F6", "#FACC15",
              "#8B5CF6", "#F97316", "#EC4899", "#06B6D4",
              "#FACC15", "#22C55E", "#EF4444", "#3B82F6",
              "#06B6D4", "#EC4899", "#F97316", "#8B5CF6",
              "#22C55E", "#3B82F6", "#FACC15", "#EF4444"]
    cols = [-0.9, 0.7, 2.3, 3.9]
    rows = [12.6, 10.8, 9.0, 7.2, 5.4]
    for r, y in enumerate(rows):
        for c, x in enumerate(cols):
            fx.append({"id": f"phone-icon{r}{c}", "shape": "box",
                       "size": [1.05, 1.05, 0.05],
                       "color": colors[r * 4 + c], "roughness": 0.4,
                       "keyframes": [{"frame": a, "position": [x, y, -2.36]},
                                    {"frame": b, "position": [x, y, -2.36]}]})
    for c, x in enumerate(cols):
        fx.append({"id": f"phone-dockicon{c}", "shape": "box",
                   "size": [1.0, 1.0, 0.05],
                   "color": ["#22C55E", "#3B82F6", "#EF4444", "#FACC15"][c],
                   "roughness": 0.4,
                   "keyframes": [{"frame": a, "position": [x, 2.7, -2.34]},
                                {"frame": b, "position": [x, 2.7, -2.34]}]})
    return fx


def _candle(a, b):
    """Candle (Gemini candle reference): a white candle held in front of the
    boy's chest (he uses the 'point' anim, arm forward), a glowing flame,
    and a translucent warm glow sphere. The candle is fx, not a PropId:
    the arm pose cannot hold a prop upright in front, while fx places the
    flame exactly where the reference has it. Static over the shot."""
    return [
        # slimmer and shorter: the first version read as a white pillar,
        # not a candle in a hand
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


def scenes(T):
    A1, A2, A3, A4, A5, A6, A7, A8, END = (
        T.B["b3"] - 1, T.B["b5"] - 1, T.B["b7"] - 1, T.B["b9"] - 1,
        T.B["b11"] - 1, T.B["b13"] - 1, T.B["b15"] - 1, T.B["b17"] - 1, T.END)

    return [
        {   # SPACESHIP: light-speed warp in the space void.
            "id": "spaceship", "location": "space", "skyColor": "#000000",
            "startFrame": 0, "endFrame": A1,
            "fx": _streaks(0, A1) + _ship(0, A1),
            "cameraShots": split_shots(0, A1, [
                # three-quarter views: head-on foreshortens the 7-stud
                # fuselage to nothing and hides the engines
                lambda a, b: static_shot(a, b, [9, 9, 14], [0, 7, -8], 58),
                # front-half detail shot: nose + cockpit + near wing, from
                # far enough that the fuselage does not become a white wall
                lambda a, b: static_shot(a, b, [7, 8, 6], [0, 7, -5], 58),
            ]),
            "characters": {},
        },
        {   # ROBOT: the screen-faced robot in the white studio.
            "id": "robot", "location": "studio", "variant": "white",
            "startFrame": A1, "endFrame": A2,
            "fx": _robot(A1, A2),
            "cameraShots": split_shots(A1, A2, [
                lambda a, b: static_shot(a, b, [0, 5.5, 13], [0, 3.5, 0], 58),
                lambda a, b: static_shot(a, b, [0, 5.2, 7], [0, 5.0, 0], 50),
            ]),
            "characters": {},
        },
        {   # RAINY STREET: stormboy under the yellow umbrella, night rain.
            "id": "rain", "location": "street", "isNight": True, "skyColor": "#334155",
            "startFrame": A2, "endFrame": A3,
            "fx": _rain(A2, A3) + _wet_street(A2, A3) + _umbrella(A2, A3),
            "cameraShots": split_shots(A2, A3, [
                lambda a, b: wide(a, b, [0, 3, 0.5], dist=18),
                lambda a, b: medium(a, b, [0, 3.5, 0.5], dist=13),
            ]),
            "characters": {
                "stormboy": [kf(A2, [0, 0, 0.5], 0, "idle", "smile"),
                             kf(A3, [0, 0, 0.5], 0, "idle", "smile")],
            },
        },
        {   # DREAM WORLD: the sleeper lies in bed under the floating props.
            "id": "dream", "location": "bedroom", "variant": "blue", "isNight": True,
            "startFrame": A3, "endFrame": A4,
            "fx": _dream(A3, A4),
            "cameraShots": split_shots(A3, A4, [
                lambda a, b: wide(a, b, [-4, 4, -3], dist=20),
                lambda a, b: static_shot(a, b, [-2, 6, 12], [-7, 4, -4], 58),
            ]),
            "characters": {
                # lying flat on the bed: root at the foot, rotationX -90deg
                # puts the head toward the headboard (pillow at z -6.4).
                "sleeper": [kf(A3, [-7, 2.4, -1.6], 0, "sleep", "sleeping", rx=-math.pi / 2),
                            kf(A4, [-7, 2.4, -1.6], 0, "sleep", "sleeping", rx=-math.pi / 2)],
            },
        },
        {   # DRY SEABED: hero + friend on the cracked earth, boat + skeleton.
            "id": "dryseabed", "location": "dryseabed", "skyColor": "#FDE68A",
            "startFrame": A4, "endFrame": A5,
            "cameraShots": split_shots(A4, A5, [
                lambda a, b: wide(a, b, [-1, 3, 0], dist=22),
                # from the front-right: the boat fills the frame, the
                # skeleton at the left edge (low_angle put the friend
                # between the camera and the boat)
                lambda a, b: static_shot(a, b, [13, 4, 6], [4, 3, -5], 58),
            ]),
            "characters": {
                "hero": [kf(A4, [-2, 0, 2], 0, "idle", "shocked"),
                         kf(A5, [-2, 0, 2], 0, "idle", "shocked")],
                "friend": [kf(A4, [3, 0, 2], 0, "idle", "shocked"),
                           kf(A5, [3, 0, 2], 0, "idle", "shocked")],
            },
        },
        {   # TURNTABLE: the hero turns slowly. (Was the wings-prop test;
            # the wings prop is retired — WingedBoy is the engine's winged
            # character now.)
            "id": "wings", "location": "studio", "variant": "blue",
            "startFrame": A5, "endFrame": A6,
            "cameraShots": split_shots(A5, A6, [
                lambda a, b: wide(a, b, [0, 3.5, 0], dist=18),
                lambda a, b: medium(a, b, [0, 4, 0], dist=11),
            ]),
            "characters": {
                "hero": [kf(A5, [0, 0, 0], 0, "idle", "smile"),
                         kf(A6, [0, 0, 0], math.pi, "idle", "smile")],
            },
        },
        {   # HEARTBEAT MONITOR: the sleeper lies in the white bedroom.
            "id": "monitor", "location": "bedroom", "variant": "white",
            "startFrame": A6, "endFrame": A7,
            "fx": _monitor(A6, A7),
            "cameraShots": split_shots(A6, A7, [
                lambda a, b: static_shot(a, b, [-2, 6, 14], [-9, 3, -4], 58),
                lambda a, b: static_shot(a, b, [-3, 5, 9], [-9.5, 3, -3.8], 55),
            ]),
            "characters": {
                "sleeper": [kf(A6, [-7, 2.4, -1.6], 0, "sleep", "sleeping", rx=-math.pi / 2),
                            kf(A7, [-7, 2.4, -1.6], 0, "sleep", "sleeping", rx=-math.pi / 2)],
            },
        },
        {   # GIANT PHONE: the phoneboy stands before the towering phone.
            "id": "phone", "location": "studio", "variant": "white",
            "startFrame": A7, "endFrame": A8,
            "fx": _phone(A7, A8),
            "cameraShots": split_shots(A7, A8, [
                lambda a, b: static_shot(a, b, [0, 8, 26], [0, 7, -3], 58),
                lambda a, b: medium(a, b, [0, 4, 1], dist=12),
            ]),
            "characters": {
                # back to the camera, facing the phone (ry ~2.68)
                "phoneboy": [kf(A7, [0, 0, 1], 2.68, "idle", "shocked"),
                             kf(A8, [0, 0, 1], 2.68, "idle", "shocked")],
            },
        },
        {   # CANDLE: the candleboy holds the candle out in the dark room.
            "id": "candle", "location": "living_room", "variant": "blue", "isNight": True,
            "startFrame": A8, "endFrame": END,
            "fx": _candle(A8, END),
            "cameraShots": split_shots(A8, END, [
                lambda a, b: medium(a, b, [0, 3.5, 0], dist=11),
                lambda a, b: close_up(a, b, [-1, 4, 1], dist=7),
            ]),
            "characters": {
                "candleboy": [kf(A8, [0, 0, 0], 0, "point", "smile"),
                              kf(END, [0, 0, 0], 0, "point", "smile")],
            },
        },
    ]
