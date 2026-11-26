"""Scene engine: keyframe/camera helpers, rule checks and the TypeScript story writer.

A story's `scenes(T)` function builds plain dicts with these helpers; `write_story()` checks them
(actor spacing, 2-3 s camera cuts, shot coverage) and writes src/story/currentStory.ts.
"""
from __future__ import annotations

import math

FPS = 30
HALF = math.pi / 2          # rotationY: 0 faces the camera (+Z), HALF faces +X (screen right), -HALF faces -X
OFF = [0, -80, 0]           # parking spot for an actor that is swapped out (other hair, crown, ...)
MIN_GAP = 4.5               # min distance between two actor centers (an R6 actor is ~4 studs wide with arms)
SHOT_MIN = 1.0              # seconds: shorter shots feel like glitches
SHOT_MAX = 3.5              # seconds: the references cut every ~1.2-3 s; never hold a shot longer than this


# ---------------------------------------------------------------------------
# Building blocks
# ---------------------------------------------------------------------------
def kf(frame, pos, ry, anim, expr, prop=None, rx=None, rz=None, bubble=None, bubble_anchor=None):
    """One character keyframe. Position/rotation interpolate to the next keyframe; anim/expression/prop switch.
    bubble_anchor: world [x, y, z] the chat bubble floats above, instead of the speaker's head —
    for a voice from a character who is off-screen / invisible (parked OFF)."""
    out = {"frame": int(frame), "position": [float(v) for v in pos], "rotationY": ry}
    if rx is not None:
        out["rotationX"] = rx
    if rz is not None:
        out["rotationZ"] = rz
    out["anim"] = anim
    out["expression"] = expr
    if prop:
        out["prop"] = prop
    if bubble:
        out["chatBubble"] = bubble
    if bubble_anchor:
        out["bubbleAnchor"] = [float(v) for v in bubble_anchor]
    return out


def hold(a, b, pos, ry, anim, expr, prop=None):
    """Actor stays in place from frame a to b."""
    return [kf(a, pos, ry, anim, expr, prop), kf(b, pos, ry, anim, expr, prop)]


def face(src, dst) -> float:
    """rotationY that makes an actor at `src` look at `dst` (both [x, y, z])."""
    return math.atan2(dst[0] - src[0], dst[2] - src[2])


def shot(a, b, from_pos, to_pos, from_t, to_t, fov=50, shake=None):
    """Camera move from frame a to b (position + look-at target interpolate linearly)."""
    s = {"startFrame": int(a), "endFrame": int(b), "fromPos": list(from_pos), "toPos": list(to_pos),
         "fromTarget": list(from_t), "toTarget": list(to_t), "fov": fov}
    if shake:
        s["shake"] = shake
    return s


def close_up(a, b, actor_pos, scale=1.0, dist=7.0, side=0.0, fov=44, shake=None, push=1.2):
    """Face close-up on an actor standing at actor_pos (head height ~4.4 * scale)."""
    x, _, z = actor_pos
    h = 4.4 * scale
    return shot(a, b, [x + side, h + 0.6, z + dist], [x + side * 0.8, h + 0.4, z + dist - push],
                [x, h, z], [x, h, z], fov, shake)


def medium(a, b, center, dist=12.0, height=5.6, fov=50, drift=(0.0, 0.0, -1.2), shake=None):
    """Waist-up shot of 1-2 actors around `center` with a slow push/drift."""
    x, _, z = center
    p0 = [x, height, z + dist]
    p1 = [x + drift[0], height + drift[1] - 0.3, z + dist + drift[2]]
    return shot(a, b, p0, p1, [x, 4.3, z], [x + drift[0] * 0.5, 4.3, z], fov, shake)


def wide(a, b, center=(0, 0, 0), dist=20.0, height=7.4, fov=58, push=2.5):
    """Wide establishing shot of the stage (3 actors side by side need dist >= 20, fov 58-60)."""
    x, _, z = center
    return shot(a, b, [x, height, z + dist], [x, height - 0.4, z + dist - push], [x, 4.8, z - 1], [x, 4.7, z - 1], fov)


def static_shot(a, b, pos, target, fov=50, shake=None):
    """Fully static camera: eye position AND look-at target are identical from
    start to end, so the frame only moves with the actors (breathing, anims).
    Use for calm explainers and for shots with large flat surfaces (walls,
    floors), where the usual push drags high-contrast edges across the frame
    and reads as shimmer. Note close_up/wide still drop height even at
    push=0, so they are not fully static — this helper is."""
    return shot(a, b, list(pos), list(pos), list(target), list(target), fov, shake)


def orbit(a, b, center, radius, height, start_angle, end_angle, target, fov=58):
    """Camera arcs around `center` at constant `radius` and `height`, always
    looking at `target` (usually the subject's position). Angles in radians,
    measured in the XZ plane from +Z (the camera side); positive angles swing
    toward +X (screen right). The arc is rendered as a true circle on the TS
    side (CameraShot.arc) — the from/to positions are only the chord endpoints
    for fallback. Use for space subjects (Moon, Earth globe, black hole) and
    anything that deserves a circling reveal."""
    cx, _, cz = center
    x0 = cx + radius * math.sin(start_angle)
    z0 = cz + radius * math.cos(start_angle)
    x1 = cx + radius * math.sin(end_angle)
    z1 = cz + radius * math.cos(end_angle)
    s = shot(a, b, [x0, height, z0], [x1, height, z1], list(target), list(target), fov)
    s["arc"] = {"center": [cx, height, cz], "radius": radius, "height": height,
                "startAngle": start_angle, "endAngle": end_angle}
    return s


def low_angle(a, b, actor_pos, dist=9.0, eye_height=1.2, fov=50, push=0.8, scale=1.0):
    """Low camera looking UP at the subject: eye near the ground, target at
    the actor's real head height. Unlike close_up/wide, which ignore actor y
    and assume ~4.4, this takes a full [x, y, z] position and aims at
    y + 4.4 * scale — so it works for a floating actor, a tiny hero, or a
    giant. Use to make a subject feel huge (ant macro world, rainbow, stars)."""
    x, y, z = actor_pos
    h = y + 4.4 * scale
    return shot(a, b, [x, eye_height, z + dist], [x, eye_height + 0.2, z + dist - push],
                [x, h, z], [x, h, z], fov)


def split_shots(a, b, makers):
    """Cut the window [a, b) into len(makers) equal shots. makers: list of fn(a, b) -> shot (e.g. lambda a, b: wide(a, b))."""
    n = len(makers)
    edges = [a + round((b - a) * i / n) for i in range(n + 1)]
    return [m(edges[i], edges[i + 1]) for i, m in enumerate(makers)]


def cover(a, b, makers, target_sec=2.5):
    """Fill [a, b) with cuts of ~target_sec (2-3 s), cycling through the camera makers.
    e.g. cover(a, b, [lambda a, b: wide(a, b), lambda a, b: close_up(a, b, HERO)])"""
    n = max(1, round((b - a) / (target_sec * FPS)))
    return split_shots(a, b, [makers[i % len(makers)] for i in range(n)])


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------
def _pos_at(keys, f):
    if f <= keys[0]["frame"]:
        return keys[0]["position"]
    for a, b in zip(keys, keys[1:]):
        if a["frame"] <= f <= b["frame"]:
            if b["frame"] == a["frame"]:
                return b["position"]
            t = (f - a["frame"]) / (b["frame"] - a["frame"])
            return [a["position"][i] + (b["position"][i] - a["position"][i]) * t for i in range(3)]
    return keys[-1]["position"]


def _scale(actor, cast):
    entry = cast.get(actor)
    return entry.get("scale", 1.0) if isinstance(entry, dict) else 1.0


def check_spacing(scenes, cast) -> list[str]:
    msgs, seen = [], set()
    for sc in scenes:
        actors = list(sc["characters"].items())
        for f in range(sc["startFrame"], sc["endFrame"], 2):
            pts = [(n, _pos_at(k, f)) for n, k in actors if k]
            pts = [(n, p) for n, p in pts if p[1] > -10]
            for i in range(len(pts)):
                for j in range(i + 1, len(pts)):
                    (n1, p1), (n2, p2) = pts[i], pts[j]
                    need = MIN_GAP * (_scale(n1, cast) + _scale(n2, cast)) / 2
                    d = math.hypot(p1[0] - p2[0], p1[2] - p2[2])
                    if d < need and (sc["id"], n1, n2) not in seen:
                        seen.add((sc["id"], n1, n2))
                        msgs.append(f"SPACING {sc['id']} frame {f}: {n1} <-> {n2} only {d:.2f} apart (min {need:.2f})")
    return msgs


def check_shots(scenes) -> list[str]:
    msgs = []
    for sc in scenes:
        shots = sorted(sc["cameraShots"], key=lambda s: s["startFrame"])
        if not shots:
            msgs.append(f"SHOTS {sc['id']}: no camera shots")
            continue
        if shots[0]["startFrame"] > sc["startFrame"] or shots[-1]["endFrame"] < sc["endFrame"]:
            msgs.append(f"SHOTS {sc['id']}: shots cover {shots[0]['startFrame']}..{shots[-1]['endFrame']}, scene is {sc['startFrame']}..{sc['endFrame']}")
        for s1, s2 in zip(shots, shots[1:]):
            if s2["startFrame"] > s1["endFrame"]:
                msgs.append(f"SHOTS {sc['id']}: gap between frames {s1['endFrame']} and {s2['startFrame']}")
            if s2["startFrame"] < s1["endFrame"]:
                msgs.append(f"SHOTS {sc['id']}: shot starting at {s2['startFrame']} overlaps the previous shot ending at {s1['endFrame']}")
        for s in shots:
            dur = (s["endFrame"] - s["startFrame"]) / FPS
            if dur > SHOT_MAX:
                msgs.append(f"SHOTS {sc['id']} {s['startFrame']}..{s['endFrame']}: {dur:.1f}s is too long (cut every 2-3 s, max {SHOT_MAX}s)")
            if dur < SHOT_MIN:
                msgs.append(f"SHOTS {sc['id']} {s['startFrame']}..{s['endFrame']}: {dur:.1f}s is too short (min {SHOT_MIN}s)")
    return msgs


def check_scenes(scenes, end) -> list[str]:
    msgs = []
    ordered = sorted(scenes, key=lambda s: s["startFrame"])
    if ordered[0]["startFrame"] != 0:
        msgs.append("SCENES: first scene must start at frame 0")
    for a, b in zip(ordered, ordered[1:]):
        if a["endFrame"] != b["startFrame"]:
            msgs.append(f"SCENES: {a['id']} ends at {a['endFrame']} but {b['id']} starts at {b['startFrame']}")
    if ordered[-1]["endFrame"] != end:
        msgs.append(f"SCENES: last scene ends at {ordered[-1]['endFrame']}, audio ends at {end}")
    return msgs


# ---------------------------------------------------------------------------
# TypeScript writer
# ---------------------------------------------------------------------------
def ts(v, indent=0):
    pad = "  " * indent
    if isinstance(v, str):
        return "'" + v.replace("\\", "\\\\").replace("'", "\\'") + "'"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(round(v, 4)) if isinstance(v, float) else str(v)
    if isinstance(v, dict):
        lines = [f"{pad}  {k if k.isidentifier() else ts(k)}: {ts(val, indent + 1)}," for k, val in v.items() if val is not None]
        return "{\n" + "\n".join(lines) + f"\n{pad}" + "}"
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(ts(x, indent) for x in v) + "]"
    raise TypeError(repr(v))


def check_story(title, scenes, cast, cues) -> list[str]:
    """Run all rule checks WITHOUT writing anything. Callers that gate on
    rule checks (make_short.py --stills/--render) must call this BEFORE
    write_story, so a failing story never lands on disk."""
    end = cues["durationInFrames"]
    return check_scenes(scenes, end) + check_shots(scenes) + check_spacing(scenes, cast)


def write_story(title, scenes, cast, cues, out_path="src/story/currentStory.ts") -> list[str]:
    end = cues["durationInFrames"]
    problems = check_story(title, scenes, cast, cues)
    story = {
        "title": title, "fps": FPS, "durationInFrames": end, "width": 1080, "height": 1920,
        "cast": cast or None, "scenes": scenes, "captions": cues["captions"],
    }
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("// GENERATED by scripts/make_short.py from stories/*.py. Do not edit by hand.\n")
        f.write("import { RobloxShortStory } from '../types/schema';\n\n")
        f.write("export const CURRENT_STORY: RobloxShortStory = " + ts(story) + ";\n")
    print(f"Story: {out_path} ({end} frames, {len(scenes)} scenes, "
          f"{sum(len(s['cameraShots']) for s in scenes)} camera shots)")
    return problems
