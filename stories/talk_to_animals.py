"""TALK TO ANIMALS — "What if you could talk to animals?"

Dialogue story, lead: teen_girl "Maya" (never a story lead before).
She wakes up understanding animals, and each one has a different
personality — the cat is dismissive, the dog is hyper, the bird is a
gossip. The twist: the animals have been listening to her all along.

The animals are small-scaled R6 presets (no animal models exist):
a grey cat (0.6), a brown dog (0.65), a blue bird (0.55). Their bubbles
carry their identity, and the narration names each one. The bubble anchor
scales with the cast scale (ShortsHUD fix, 2026-11-21), so a small
animal's bubble sits on its real head. Each dialogue line gets its own
close-up on the speaker, so the bubble never hides.

CHANNEL RULE (the maintainer 2026-11-21): opens with the big "What if you could
talk to animals?" question (b0), then the "In this town," setup follows —
and it answers the question with real science: dogs really do learn
words, cats really do meow mostly at us, prairie dogs really do have a
different alarm call for each predator (b14-b16).

FRAMING FIXES (2026-11-23, from the original fake-timing preview):
- Triple bubble: the bird's "pigeon" bubble persisted from b10 through
  the shouts, and the cat's "LOUD!" persisted into the dog's "SLOW!"
  shot — three bubbles at once. Fixed with bubble-clearing keyframes:
  bird goes bubble-less at w1, cat goes bubble-less at w2, so each shout
  shot shows exactly one bubble.
- Bird close-up was blocked: in the talk scene the cat stands at [0,0,2]
  directly between the bird camera and the bird at [0,0,-3], so the
  bird's close-up framed the cat's giant face instead. Fixed with
  side=3.0 on the bird close-up (three-quarter view, cat out of frame).
- Edge cuts: every wide/medium that showed two characters 5+ studs
  apart sliced one of them in half at the portrait frame edge (Maya in
  the cat medium, dog wide, bird medium and deal wide; the dog in the
  deal medium; Maya AND mom in the morning medium). Fixed per the
  blue_sun lesson — two-character shots are now wides with enough
  distance (dist 22-26), and the deal medium became animal close-ups.

"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, low_angle, medium, orbit, shot, split_shots, wide  # noqa: F401

TITLE = "SHE TALKS TO ANIMALS"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b0", "text": "What if you could talk to animals?", "pause": 0.10},
    {"id": "b1", "text": "In this town, one morning, Maya woke up understanding animals.", "pause": 0.08},
    {"id": "b2", "text": "The cat on the fence was not meowing. He was complaining.", "pause": 0.08},
    {"id": "b3", "text": "The dog in the park was not barking. He was begging for a game.", "pause": 0.08},
    {"id": "b4", "text": "And the bird on the wire knew everyone's secrets.", "pause": 0.08},
    {"id": "b5", "text": "Maya asked the cat why he was grumpy.", "pause": 0.08},
    {"id": "b6", "text": "The cat said the food bowl was empty, and it was her fault.", "pause": 0.08},
    {"id": "b7", "text": "She asked the dog what he wanted most in the world.", "pause": 0.08},
    {"id": "b8", "text": "The dog said the ball, the ball, always the ball.", "pause": 0.08},
    {"id": "b9", "text": "She asked the bird what he had heard today.", "pause": 0.08},
    {"id": "b10", "text": "The bird said the pigeon knows everything, and the pigeon tells him.", "pause": 0.08},
    {"id": "b11", "text": "Maya laughed, and asked the animals what they thought of her.", "pause": 0.10},
    {"id": "w1", "text": "LOUD!", "voice": "af_bella", "shout": True, "pause": 0.55},
    {"id": "w2", "text": "SLOW!", "voice": "af_bella", "shout": True, "pause": 0.55},
    {"id": "b12", "text": "The animals had been listening to her all along. Every secret, every song.", "pause": 0.08},
    {"id": "b13", "text": "So Maya made a deal: she would keep their secrets, if they kept hers.", "pause": 0.08},
    {"id": "b14", "text": "And here is the real science. Animals really do talk, just not in words.", "pause": 0.08},
    {"id": "b15", "text": "Dogs can learn over a hundred words, and cats meow mostly at us, not at each other.", "pause": 0.08},
    {"id": "b16", "text": "Prairie dogs even have a different alarm call for a hawk, a coyote, and a human.", "pause": 0.08},
    {"id": "b17", "text": "And now, every morning, the whole town talks. Most of it sounds like meowing.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05,
         "dropouts": [("b11+0.3", "w2.end")]}
SFX = [
    ("b0", "whoosh"),
    ("b1", "whoosh"),
    ("b2+0.5", "pop", {"f": 700}),
    ("b3+0.5", "pop", {"f": 800}),
    ("b4+0.5", "sparkle"),
    ("b5+0.3", "bubbles"),
    ("b6+0.5", "pop_down"),
    ("b7+0.3", "bubbles"),
    ("b8+0.5", "pop", {"f": 900}),
    ("b9+0.3", "bubbles"),
    ("b10+0.6", "sparkle"),
    ("b11+0.4", "laugh"),
    ("w1", "impact"),
    ("w2", "impact"),
    ("b12+0.5", "reveal"),
    ("b13+0.6", "sparkle"),
    ("b14+0.5", "sparkle"),
    ("b15+0.5", "pop", {"f": 700}),
    ("b16+0.5", "sparkle"),
    ("b17+1.5", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
CAST = {
    "hero": {"extends": "teen_girl", "hair": {"style": "wavyLong", "color": "auburn"},
             "top": {"style": "hoodie", "color": "teal", "secondary": "white"},
             "bottom": {"style": "jeans", "color": "denim"},
             "shoes": {"color": "white", "sole": "white"},
             "accessories": ["bow"]},
    # The cat: small, grey, dismissive. The dog: small, brown, hyper.
    # The bird: smallest, blue, a gossip. All R6 kids at animal scale.
    "cat": {"extends": "little_brother", "hair": {"style": "buzz", "color": "gray"},
            "top": {"style": "tshirt", "color": "gray", "secondary": "charcoal"},
            "bottom": {"style": "shorts", "color": "charcoal"},
            "shoes": {"color": "gray", "sole": "gray"}, "scale": 0.6},
    "dog": {"extends": "little_brother", "hair": {"style": "curly", "color": "brown"},
            "top": {"style": "tshirt", "color": "brown", "secondary": "mustard"},
            "bottom": {"style": "shorts", "color": "brown"},
            "shoes": {"color": "brown", "sole": "brown"}, "scale": 0.65},
    "bird": {"extends": "little_brother", "hair": {"style": "spikyAnime", "color": "blue"},
             "top": {"style": "tshirt", "color": "sky", "secondary": "white"},
             "bottom": {"style": "shorts", "color": "sky"},
             "shoes": {"color": "blue", "sole": "blue"}, "scale": 0.55},
    "mom": {"extends": "real_mom", "hair": {"style": "bun", "color": "black"}},
}


# 4. SCENES --------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END
    S_CAT = B["b2"] - 1     # house: the cat on the fence
    S_PARK = B["b3"] - 1    # playground: the dog
    S_WIRE = B["b4"] - 1    # street: the bird on the wire
    S_TALK = B["b5"] - 1    # playground: the three conversations
    S_DEAL = B["b12"] - 1   # playground: the deal + the real science
    S_END = B["b17"] - 1    # street at night: the whole town talks

    # Four speakers in one scene: a 5-stud grid so every pair is >= 5 apart
    # (the spacing check measures all of them, even in close-ups).
    HERO_P = [-5, 0, 2]
    CAT_P = [0, 0, 2]
    DOG_P = [5, 0, -3]
    BIRD_P = [0, 0, -3]

    # The talk scene cuts to the speaker for every line, so each bubble is
    # on screen with its owner. Shots are built from the beat frames. b6 is
    # 3.7 s, so its shot is split in two: cat close-up, then a reaction
    # close-up on Maya.
    # Bird close-up uses side=3.0: head-on, the cat at [0,0,2] stands
    # directly between the bird camera and the bird at [0,0,-3] and fills
    # the frame with his own face (old preview f00740). From the side the
    # cat is ~50 degrees off-axis, out of frame.
    _b6mid = (B["b6"] + B["b7"]) // 2
    talk_shots = [
        close_up(S_TALK, B["b6"], HERO_P),
        close_up(B["b6"], _b6mid, CAT_P, scale=0.6),
        close_up(_b6mid, B["b7"], HERO_P),
        close_up(B["b7"], B["b8"], HERO_P),
        close_up(B["b8"], B["b9"], DOG_P, scale=0.65),
        close_up(B["b9"], B["b10"], HERO_P),
        close_up(B["b10"], B["b11"], BIRD_P, scale=0.55, side=3.0),
        close_up(B["b11"], B["w1"], HERO_P),
        close_up(B["w1"], B["w2"], CAT_P, scale=0.6, shake=0.06),
        close_up(B["w2"], S_DEAL, DOG_P, scale=0.65, shake=0.06),
    ]

    return [
        {   # Hook: aerial town, two angles (b0 + b1 span it; three shots would be <1 s each).
            "id": "hook", "location": "town_overview", "startFrame": 0, "endFrame": S_CAT,
            "cameraShots": [
                shot(0, S_CAT // 2, [-10, 62, 74], [-7, 56, 67], [8, 0, -6], [7, 1, -7], 55),
                shot(S_CAT // 2, S_CAT, [-7, 56, 67], [-4, 50, 61], [7, 1, -7], [6, 2, -8], 55),
            ],
            "characters": {},
        },
        {   # The cat on the fence. The opening 2-shot is a WIDE, not a
            # medium: two actors 5 apart span ~8 studs with arms out,
            # wider than a medium frame, which sliced Maya in half at the
            # left edge in the old preview.
            "id": "cat", "location": "house", "variant": "yellow",
            "startFrame": S_CAT, "endFrame": S_PARK,
            "cameraShots": cover(S_CAT, S_PARK, [
                lambda a, b: wide(a, b, [-2.5, 0, 2], dist=22),
                lambda a, b: close_up(a, b, CAT_P, scale=0.6),
                lambda a, b: low_angle(a, b, CAT_P, scale=0.6),
            ]),
            "characters": {
                "hero": hold(S_CAT, S_PARK, HERO_P, 0.4, "idle", "shocked"),
                "cat": hold(S_CAT, S_PARK, CAT_P, -0.4, "idle", "deadpan"),
            },
        },
        {   # The dog in the park. Wide pulled back to dist 26 and centred
            # on the pair midpoint: the old dist-20 wide sliced Maya in
            # half at the left edge. The old medium framed the empty
            # playground between them — replaced with a Maya reaction
            # close-up.
            "id": "dog", "location": "playground",
            "startFrame": S_PARK, "endFrame": S_WIRE,
            "cameraShots": cover(S_PARK, S_WIRE, [
                lambda a, b: wide(a, b, [0, 0, -0.5], dist=26),
                lambda a, b: close_up(a, b, DOG_P, scale=0.65),
                lambda a, b: close_up(a, b, HERO_P),
            ]),
            "characters": {
                "hero": hold(S_PARK, S_WIRE, HERO_P, 0.4, "idle", "smile"),
                "dog": [kf(S_PARK, DOG_P, -0.4, "idle", "smile"),
                        kf(B["b3"] + 20, DOG_P, -0.4, "jump", "laugh"),
                        kf(S_WIRE, DOG_P, -0.4, "idle", "laugh")],
            },
        },
        {   # The bird on the wire. Opening 2-shot is a WIDE centred on
            # the pair midpoint: the old medium sliced Maya in half at
            # the left edge.
            "id": "bird", "location": "street",
            "startFrame": S_WIRE, "endFrame": S_TALK,
            "cameraShots": cover(S_WIRE, S_TALK, [
                lambda a, b: wide(a, b, [-2.5, 0, -0.5], dist=22),
                lambda a, b: low_angle(a, b, BIRD_P, scale=0.55),
                lambda a, b: close_up(a, b, BIRD_P, scale=0.55),
            ]),
            "characters": {
                "hero": hold(S_WIRE, S_TALK, HERO_P, 0.4, "idle", "smile"),
                "bird": hold(S_WIRE, S_TALK, BIRD_P, -0.4, "idle", "cool"),
            },
        },
        {   # The three conversations — one close-up per line, on the speaker.
            # Bubble discipline: a bubble lives only until its owner's next
            # keyframe, so the bird's "pigeon" bubble is cleared at w1 and
            # the cat's "LOUD!" is cleared at w2 — each shout shot shows
            # exactly one bubble (old preview showed all three at once).
            "id": "talk", "location": "playground",
            "startFrame": S_TALK, "endFrame": S_DEAL,
            "cameraShots": talk_shots,
            "characters": {
                "hero": [
                    kf(S_TALK, HERO_P, 0.4, "idle", "smile"),
                    # FIX 2026-11-23 (review FAIL: bubble on the wrong keyframe):
                    # "Why so grumpy?" belongs to b5 (Maya asks the cat, f397-449).
                    # It was on the b7 keyframe, so it played over the dog beat
                    # (f533-604) instead. Bubble lives until the next keyframe,
                    # so this one clears at B["b6"].
                    kf(B["b5"], HERO_P, 0.4, "idle", "smile", bubble="Why so grumpy?"),
                    kf(B["b6"], HERO_P, 0.4, "idle", "shocked"),
                    kf(B["b7"], HERO_P, 0.4, "idle", "smile"),
                    kf(B["b8"], HERO_P, 0.4, "idle", "laugh"),
                    kf(B["b9"], HERO_P, 0.4, "idle", "smile", bubble="What did you hear?"),
                    kf(B["b10"], HERO_P, 0.4, "idle", "shocked"),
                    kf(B["b11"], HERO_P, 0.4, "idle", "laugh", bubble="What do you think of me?"),
                    kf(B["w1"], HERO_P, 0.4, "idle", "shocked"),
                    kf(S_DEAL, HERO_P, 0.4, "idle", "shocked"),
                ],
                "cat": [
                    kf(S_TALK, CAT_P, -0.4, "idle", "deadpan"),
                    kf(B["b6"], CAT_P, -0.4, "idle", "deadpan",
                       bubble="The bowl is empty. Your fault."),
                    kf(B["b7"], CAT_P, -0.4, "idle", "deadpan"),
                    kf(B["w1"], CAT_P, -0.4, "idle", "angry", bubble="LOUD!"),
                    kf(B["w2"], CAT_P, -0.4, "idle", "deadpan"),
                    kf(S_DEAL, CAT_P, -0.4, "idle", "deadpan"),
                ],
                "dog": [
                    kf(S_TALK, DOG_P, -0.4, "idle", "smile"),
                    kf(B["b8"], DOG_P, -0.4, "jump", "laugh",
                       bubble="THE BALL! THE BALL!"),
                    kf(B["b9"], DOG_P, -0.4, "idle", "laugh"),
                    kf(B["w2"], DOG_P, -0.4, "jump", "laugh", bubble="SLOW!"),
                    kf(S_DEAL, DOG_P, -0.4, "idle", "laugh"),
                ],
                "bird": [
                    kf(S_TALK, BIRD_P, -0.4, "idle", "cool"),
                    kf(B["b10"], BIRD_P, -0.4, "idle", "cool",
                       bubble="The pigeon knows everything."),
                    kf(B["w1"], BIRD_P, -0.4, "idle", "cool"),
                    kf(S_DEAL, BIRD_P, -0.4, "idle", "cool"),
                ],
            },
        },
        {   # The deal + the real science: she keeps their secrets, they
            # keep hers — then the takeaway (dogs learn words, cats meow
            # at us, prairie dogs have a call for each predator). Wide
            # pulled back to dist 26: the old dist-20 wide sliced Maya in
            # half at the left edge, and the old medium sliced the dog at
            # the right edge. Now the montage cycles the group wide and a
            # close-up per animal, so each takeaway line lands on its animal.
            "id": "deal", "location": "playground",
            "startFrame": S_DEAL, "endFrame": S_END,
            # Montage aligned to the takeaway BEATS, not a blind cycle: the
            # old cover() cycle put the bird's close-up on the dogs line and
            # the CAT on the prairie-dogs line. Now each takeaway line leads
            # on its own animal — dog CU for the dogs half of b15, cat CU
            # for the cats half of b15 (split at f1383), bird CU for b16
            # (prairie-dog alarm calls; the bird is the cast's alarm-caller
            # stand-in). b14 ("here is the real science") stays neutral:
            # wide, then Maya.
            "cameraShots": (
                cover(S_DEAL, B["b13"] - 1, [
                    lambda a, b: wide(a, b, [0, 0, 0], dist=26),
                    lambda a, b: close_up(a, b, CAT_P, scale=0.6),
                ])
                + cover(B["b13"] - 1, B["b14"] - 1, [
                    lambda a, b: close_up(a, b, HERO_P),
                ])
                + cover(B["b14"] - 1, B["b15"] - 1, [
                    lambda a, b: wide(a, b, [0, 0, 0], dist=26),
                    lambda a, b: close_up(a, b, HERO_P),
                ])
                # b15 carries TWO takeaway animals in one beat: the dogs half
                # ("Dogs can learn over a hundred words") runs to f1382 and
                # the cats half ("cats meow mostly at us") starts f1383
                # (word timings in public/kokoro-cues.json, stable across
                # runs — same text, same voice). Split the beat there so the
                # dog CU leads the dogs half and the cat CU leads the cats
                # half; a single cover over b15 put the cat on the dogs line.
                + cover(B["b15"] - 1, 1383, [
                    lambda a, b: close_up(a, b, DOG_P, scale=0.65),
                ])
                + cover(1383, B["b16"] - 1, [
                    lambda a, b: close_up(a, b, CAT_P, scale=0.6),
                ])
                + cover(B["b16"] - 1, S_END, [
                    lambda a, b: close_up(a, b, BIRD_P, scale=0.55, side=3.0),
                    lambda a, b: wide(a, b, [0, 0, 0], dist=26),
                ])
            ),
            "characters": {
                "hero": [kf(S_DEAL, HERO_P, 0.4, "idle", "smile"),
                         kf(B["b13"], HERO_P, 0.4, "celebrate", "laugh"),
                         kf(S_END, HERO_P, 0.4, "idle", "laugh")],
                "cat": hold(S_DEAL, S_END, CAT_P, -0.4, "idle", "cool"),
                "dog": hold(S_DEAL, S_END, DOG_P, -0.4, "idle", "smile"),
                "bird": hold(S_DEAL, S_END, BIRD_P, 0.4, "idle", "cool"),
            },
        },
        {   # Every morning, the whole town talks. Opening 2-shot is a
            # WIDE centred on the Maya-mom midpoint: the old medium
            # sliced BOTH of them in half at the edges and framed the
            # empty street between them.
            "id": "morning", "location": "street", "isNight": True,
            "startFrame": S_END, "endFrame": END,
            "cameraShots": cover(S_END, END, [
                lambda a, b: wide(a, b, [-1.25, 0, 1.25], dist=22),
                lambda a, b: close_up(a, b, HERO_P),
            ]),
            "characters": {
                "hero": hold(S_END, END, HERO_P, 0.4, "idle", "smile"),
                "mom": hold(S_END, END, [2.5, 0, 0.5], -0.4, "idle", "smile"),
            },
        },
    ]
