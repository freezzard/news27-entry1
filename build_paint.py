#!/usr/bin/env python3
"""Paint the news-image-20261127 entry: a 1024x1024 broadsheet digest of
Friday 27 November 2026. Deterministic: fixed palette, fixed fonts, no
network, no timestamps, no randomness. Run: python3 build_paint.py
Writes entry.png next to this file."""

import os
from collections import Counter
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (26, 26, 26)
RED = (179, 32, 44)
NAVY = (22, 50, 79)
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)
GREY = (110, 108, 100)
CARD = (255, 253, 247)
LINE = (200, 192, 172)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


F_SERIF_B = lambda s: font(SERIF_B, s)
F_SANS = lambda s: font(SANS, s)
F_SANS_B = lambda s: font(SANS_B, s)

# ---------------------------------------------------------------- data
HEROES = [
    {
        "kicker": "MIDDLE EAST  •  CONFLICT",
        "title": "Houthi strike hits Jazan refinery",
        "lines": ["One worker killed as operations halt;", "Brent crude jumps past $96 a barrel"],
        "scene": "refinery",
    },
    {
        "kicker": "WORLD  •  TECH",
        "title": "FCC clears 1m SpaceX satellites",
        "lines": ["Orbital AI data centres approved;", "astronomers warn of a lost night sky"],
        "scene": "satellites",
    },
    {
        "kicker": "ASIA  •  DISASTER",
        "title": "Hong Kong marks fire anniversary",
        "lines": ["168 lives lost in the high-rise inferno;", "city remembers on the anniversary"],
        "scene": "tower",
    },
]

CARDS = [
    ("EUROPE", "CONFLICT", "Russian drones kill 3 in Ukraine", "Kharkiv university hit; energy grid targeted"),
    ("EUROPE", "CONFLICT", "Ukraine missiles hit Su-34 base", "Neptune strike deep inside Russia"),
    ("MIDDLE EAST", "CONFLICT", "10 killed in Gaza strikes", "Iranian drones kill 2 Italians in Kuwait"),
    ("MIDDLE EAST", "POLITICS", "Iran denies the Kuwait attack", "Katz warns of a Gaza operation"),
    ("ASIA", "POLITICS", "Kim inspects nuclear sites", "Calls for more tactical nuclear arms"),
    ("EUROPE", "POLITICS", "EU budget talks end with no deal", "Leaders chase a year-end agreement"),
    ("ASIA", "MARKETS", "Asian stocks rebound sharply", "Kospi +2.72%; Tokyo CPI hits 2.9%"),
    ("ASIA", "MARKETS", "Bank of Korea hikes to 3.25%", "Two-year high as growth outlook rises"),
    ("N. AMERICA", "DISASTER", "Thanksgiving storm cuts power", "900,000 homes dark across the US"),
    ("AFRICA", "DISASTER", "Cairo tanker fire kills 31", "Highway inferno after a fuel crash"),
    ("WORLD", "SCIENCE", "Hera maps DART's crater", "Stadium-size scar on the asteroid"),
    ("WORLD", "SPORT", "Gukesh draws Sindarov again", "Game 2 of the chess title match"),
]

BRIEFS = [
    ("EUROPE", "POLITICS", "Trump tells Putin to cut hostilities across Europe"),
    ("N. AMERICA", "POLITICS", "Trump doubles down on tariffs despite opposition"),
    ("N. AMERICA", "POLITICS", "Trump's Thanksgiving message attacks his critics"),
    ("EUROPE", "CONFLICT", "US approves $622m deal to keep Ukraine's F-16s flying"),
    ("EUROPE", "POLITICS", "EU bans Russian imports for good, commissioner says"),
    ("EUROPE", "CONFLICT", "Zelensky: Russia readies mass attack on energy grid"),
    ("EUROPE", "POLITICS", "Zelensky sets a deadline for Trump and Putin"),
    ("EUROPE", "POLITICS", "Sweden summons Russian envoy over airspace breach"),
    ("EUROPE", "POLITICS", "London hit by a 24-hour Tube strike"),
    ("EUROPE", "LAW", "Depardieu to face trial on sex-assault charge"),
    ("ASIA", "POLITICS", "NZ count: National 40 seats, Labour 29.88%"),
    ("EUROPE", "POLITICS", "Serbia calls a presidential vote for 27 December"),
    ("AFRICA", "LAW", "Kenya court halts US-funded Ebola centre build"),
    ("AFRICA", "DISASTER", "Congo Ebola outbreak passes 12,000 cases"),
    ("AFRICA", "LAW", "Kenyan cult leader convicted on terror charges"),
    ("MIDDLE EAST", "LAW", "Iraq jails eight French IS members for life"),
    ("N. AMERICA", "POLITICS", "Mexico protests US refusal to extradite ex-TV host"),
    ("S. AMERICA", "POLITICS", "Bradesco chief to become Brazil finance minister"),
    ("ASIA", "SPORT", "India women beat Japan 4-0 in hockey"),
    ("ASIA", "SPORT", "India A reach Rising Stars semi in Doha"),
    ("WORLD", "SCIENCE", "Moon rover Idefix launches into space"),
    ("N. AMERICA", "TECH", "SpaceX seals $44bn deal for Nvidia Rubin chips"),
    ("EUROPE", "MARKETS", "Temu agrees to change practices in the EU"),
    ("MIDDLE EAST", "LAW", "Judges urge dropping key Netanyahu charges"),
]

NUMBERS = [
    ("168", "lives lost in the Hong Kong tower fire, one year on"),
    ("1,000,000", "satellites cleared in SpaceX's orbital data plan"),
    ("900,000", "US homes without power in the Thanksgiving storm"),
    ("12,000", "cases in the Congo Ebola outbreak"),
    ("31", "killed in the Cairo fuel-tanker fire"),
    ("$96", "Brent crude per barrel after the Jazan attack"),
]

PINS = [
    ("KYIV", 30.5, 50.4),
    ("GAZA", 34.5, 31.5),
    ("JAZAN", 44.5, 16.9),
    ("HONG KONG", 114.2, 22.3),
    ("CAIRO", 31.2, 30.0),
    ("SEOUL", 127.0, 37.5),
    ("LONDON", -0.1, 51.5),
    ("NEW YORK", -74.0, 40.7),
]

CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 62), (-55, 47),
     (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
     (-125, 40), (-125, 49), (-140, 60)],
    [(-80, 10), (-60, 8), (-50, 0), (-40, -5), (-35, -8), (-40, -20), (-50, -30),
     (-60, -38), (-70, -52), (-73, -40), (-70, -20), (-80, -5)],
    [(-10, 36), (0, 38), (10, 38), (20, 40), (28, 36), (30, 42), (23, 45), (18, 55),
     (8, 57), (5, 60), (-5, 58), (-10, 50)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12),
     (51, 11), (48, 0), (40, -15), (35, -25), (28, -33), (20, -35), (15, -27),
     (12, -18), (9, -2), (9, 4), (-8, 5)],
    [(30, 42), (40, 45), (50, 50), (60, 55), (70, 60), (80, 68), (100, 70), (130, 72),
     (160, 70), (180, 66), (162, 60), (158, 52), (142, 45), (135, 35), (127, 33),
     (120, 25), (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (80, 15),
     (75, 8), (70, 25), (60, 25), (50, 30), (45, 35), (35, 36)],
    [(113, -22), (122, -14), (132, -12), (142, -11), (150, -22), (153, -27),
     (150, -37), (140, -38), (130, -32), (120, -34)],
]


def wrap(text, fnt, width, draw):
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = word if cur == "" else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur != "":
                lines.append(cur)
            cur = word
    if cur != "":
        lines.append(cur)
    return lines


def draw_scene(draw, kind, x, y, w, h):
    if kind == "refinery":
        draw.rectangle([x, y, x + w, y + h], fill=(32, 36, 44))
        draw.rectangle([x, y + h - 18, x + w, y + h], fill=(20, 22, 28))
        for i, tx in enumerate([x + 18, x + 78, x + 138, x + 198, x + 258]):
            th = 52 + (i % 3) * 10
            draw.rectangle([tx, y + h - 18 - th, tx + 26, y + h - 18], fill=(70, 76, 88))
            draw.rectangle([tx + 4, y + h - 18 - th - 8, tx + 22, y + h - 18 - th], fill=(96, 102, 116))
        draw.polygon([(x + 250, y + h - 18), (x + 268, y + h - 62), (x + 286, y + h - 18)],
                     fill=(240, 120, 30))
        draw.polygon([(x + 258, y + h - 18), (x + 268, y + h - 44), (x + 278, y + h - 18)],
                     fill=(250, 200, 60))
        for cx, cy, r in [(x + 60, y + 22, 9), (x + 110, y + 14, 12), (x + 170, y + 24, 8)]:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 118, 112))
    elif kind == "satellites":
        draw.rectangle([x, y, x + w, y + h], fill=(14, 34, 66))
        for sx, sy in [(x + 20, y + 14), (x + 70, y + 30), (x + 130, y + 10), (x + 200, y + 26),
                       (x + 250, y + 12), (x + 300, y + 34), (x + 160, y + 40), (x + 40, y + 48)]:
            draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=WHITE)
        draw.ellipse([x + 40, y + 34, x + 290, y + 84], outline=(90, 140, 190), width=2)
        for sx, sy in [(x + 90, y + 58), (x + 190, y + 50), (x + 260, y + 66)]:
            draw.rectangle([sx - 4, sy - 4, sx + 4, sy + 4], fill=(220, 220, 220))
            draw.rectangle([sx - 20, sy - 2, sx - 5, sy + 2], fill=(90, 140, 200))
            draw.rectangle([sx + 5, sy - 2, sx + 20, sy + 2], fill=(90, 140, 200))
    elif kind == "tower":
        draw.rectangle([x, y, x + w, y + h], fill=(58, 42, 58))
        draw.rectangle([x + 120, y + 18, x + 200, y + h - 10], fill=(40, 30, 44))
        for wy in range(y + 26, y + h - 16, 14):
            for wx in range(x + 128, x + 196, 16):
                lit = (wx + wy) % 32 == 0
                draw.rectangle([wx, wy, wx + 8, wy + 8],
                               fill=(250, 190, 80) if lit else (90, 80, 96))
        for cx, cy, r in [(x + 150, y + 12, 10), (x + 180, y + 6, 13), (x + 210, y + 14, 9)]:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 146, 140))
        draw.polygon([(x + 60, y + h - 10), (x + 72, y + h - 52), (x + 84, y + h - 10)],
                     fill=(240, 200, 90))
        draw.rectangle([x + 10, y + h - 8, x + 110, y + h - 4], fill=(30, 24, 32))
    else:
        draw.rectangle([x, y, x + w, y + h], fill=NAVY)


FIELD_COLORS = {
    "CONFLICT": (179, 32, 44),
    "POLITICS": (22, 50, 79),
    "MARKETS": (28, 110, 70),
    "DISASTER": (150, 80, 10),
    "SCIENCE": (90, 60, 140),
    "SPORT": (160, 110, 10),
    "LAW": (100, 90, 80),
    "TECH": (20, 110, 130),
}


def draw_mini(draw, idx, x, y, w, h, field):
    base = FIELD_COLORS[field]
    draw.rectangle([x, y, x + w, y + h], fill=base)
    light = tuple(min(255, c + 60) for c in base)
    dark = tuple(max(0, c - 40) for c in base)
    motif = idx % 6
    if motif == 0:
        for k in range(5):
            bx = x + 12 + k * 14
            bh = 8 + ((k * 7) % 16)
            draw.rectangle([bx, y + h - 6 - bh, bx + 8, y + h - 6], fill=light)
    elif motif == 1:
        draw.polygon([(x + 10, y + h - 8), (x + w // 2, y + 6), (x + w - 10, y + h - 8)],
                     outline=(255, 220, 120), width=3)
        draw.ellipse([x + w // 2 - 4, y + 4, x + w // 2 + 4, y + 12], fill=(255, 220, 120))
    elif motif == 2:
        draw.rectangle([x + 14, y + 8, x + w - 14, y + h - 8], outline=WHITE, width=2)
        draw.line([x + 14, y + h // 2, x + w - 14, y + h // 2], fill=WHITE, width=2)
        draw.line([x + w // 2, y + 8, x + w // 2, y + h - 8], fill=WHITE, width=2)
    elif motif == 3:
        draw.ellipse([x + w // 2 - 12, y + 4, x + w // 2 + 12, y + h - 4],
                     outline=(255, 220, 120), width=3)
        draw.ellipse([x + w // 2 - 3, y + h // 2 - 3, x + w // 2 + 3, y + h // 2 + 3],
                     fill=(255, 220, 120))
    elif motif == 4:
        for k in range(4):
            wy = y + 6 + k * 6
            draw.line([x + 10, wy, x + w - 10 - k * 8, wy], fill=light, width=3)
    else:
        draw.polygon([(x + w // 2, y + 5), (x + w - 12, y + h - 6), (x + 12, y + h - 6)],
                     outline=WHITE, width=2)
        draw.rectangle([x + w // 2 - 8, y + h - 12, x + w // 2 + 8, y + h - 6], fill=dark)


def paint():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- masthead
    draw.rectangle([0, 0, W, 86], fill=(24, 24, 24))
    draw.text((14, 8), "THE WORLD TODAY", font=F_SERIF_B(46), fill=(246, 241, 229))
    draw.text((14, 60), "39 STORIES  •  EVERY REGION  •  ONE DAY IN ONE IMAGE",
              font=F_SANS_B(13), fill=GOLD)
    right = "FRIDAY  •  27 NOVEMBER 2026"
    rw = draw.textlength(right, font=F_SANS_B(20))
    draw.text((W - 14 - rw, 14), right, font=F_SANS_B(20), fill=WHITE)
    draw.text((W - 14 - draw.textlength("ALL EVENTS OF 27 NOV 2026", font=F_SANS(12)), 62),
              "ALL EVENTS OF 27 NOV 2026", font=F_SANS(12), fill=(200, 196, 186))
    draw.line([0, 86, W, 86], fill=RED, width=3)

    # ---- heroes (one-line titles, two short sub-lines, all inside the card)
    hy, hh, hw, gap = 94, 172, 328, 8
    for i, hero in enumerate(HEROES):
        hx = 8 + i * (hw + gap)
        draw.rectangle([hx, hy, hx + hw, hy + hh], fill=CARD, outline=LINE, width=1)
        draw_scene(draw, hero["scene"], hx + 1, hy + 1, hw - 2, 92)
        draw.text((hx + 10, hy + 98), hero["kicker"], font=F_SANS_B(10), fill=RED)
        draw.text((hx + 10, hy + 112), hero["title"], font=F_SERIF_B(16), fill=INK)
        ly = hy + 134
        for line in hero["lines"]:
            draw.text((hx + 10, ly), line, font=F_SANS(11), fill=(70, 68, 62))
            ly += 14

    # ---- map + tallies
    my, mh = 274, 132
    draw.rectangle([8, my, 1016, my + mh], fill=CARD, outline=LINE, width=1)
    draw.text((20, my + 6), "WHERE THE DAY HAPPENED", font=F_SANS_B(11), fill=NAVY)
    mx0, my0, mx1, my1 = 20, my + 22, 590, my + mh - 16
    draw.rectangle([mx0, my0, mx1, my1], fill=(228, 236, 242))
    for poly in CONTINENTS:
        pts = []
        for lon, lat in poly:
            px = mx0 + (lon + 180.0) / 360.0 * (mx1 - mx0)
            py = my1 - (lat + 60.0) / 150.0 * (my1 - my0)
            pts.append((px, py))
        draw.polygon(pts, fill=(150, 170, 150), outline=(110, 135, 110))
    for n, (name, lon, lat) in enumerate(PINS, start=1):
        px = mx0 + (lon + 180.0) / 360.0 * (mx1 - mx0)
        py = my1 - (lat + 60.0) / 150.0 * (my1 - my0)
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
        draw.text((px - 3, py - 6), str(n), font=F_SANS_B(9), fill=WHITE)
    legend = "  ".join("%d %s" % (n + 1, name) for n, (name, _, _) in enumerate(PINS))
    draw.text((mx0, my + mh - 13), legend, font=F_SANS(8), fill=GREY)

    all_stories = []
    for hero in HEROES:
        region, field = hero["kicker"].split("  •  ")
        all_stories.append((region, field))
    for region, field, _, _ in CARDS:
        all_stories.append((region, field))
    for region, field, _ in BRIEFS:
        all_stories.append((region, field))
    region_counts = Counter(r for r, _ in all_stories)
    field_counts = Counter(f for _, f in all_stories)

    def tally_block(x, title, counts, order, maxw):
        draw.text((x, my + 6), title, font=F_SANS_B(11), fill=NAVY)
        yy = my + 24
        for key in order:
            val = counts.get(key, 0)
            draw.text((x, yy), key, font=F_SANS(9), fill=INK)
            bw = int(val / 14.0 * maxw)
            draw.rectangle([x + 78, yy + 1, x + 78 + bw, yy + 9], fill=RED)
            draw.text((x + 82 + bw, yy), str(val), font=F_SANS_B(9), fill=INK)
            yy += 13
        return yy

    tally_block(612, "BY REGION", region_counts,
                ["EUROPE", "ASIA", "MIDDLE EAST", "N. AMERICA", "AFRICA", "WORLD", "S. AMERICA"], 70)
    tally_block(820, "BY FIELD", field_counts,
                ["POLITICS", "CONFLICT", "LAW", "DISASTER", "MARKETS", "SPORT", "SCIENCE", "TECH"], 62)

    # ---- numbers strip (two label lines)
    ny, nh = 414, 46
    draw.rectangle([8, ny, 1016, ny + nh], fill=(24, 24, 24))
    cw = 1008 / 6.0
    for i, (num, label) in enumerate(NUMBERS):
        cx = 8 + i * cw
        draw.text((cx + 8, ny + 3), num, font=F_SANS_B(19), fill=GOLD)
        lab_lines = wrap(label, F_SANS(9), cw - 16, draw)
        ly = ny + 25
        for line in lab_lines[:2]:
            draw.text((cx + 8, ly), line, font=F_SANS(9), fill=(220, 216, 206))
            ly += 10
        if i < 5:
            draw.line([cx + cw - 1, ny + 6, cx + cw - 1, ny + nh - 6], fill=(70, 68, 62), width=1)

    # ---- 12 cards
    cy0, ch, cwid = 468, 96, 244
    draw.text((8, cy0 - 2), "THE DAY IN PICTURES", font=F_SANS_B(11), fill=NAVY)
    for i, (region, field, title, sub) in enumerate(CARDS):
        row, col = divmod(i, 4)
        cx = 8 + col * 252
        cy = cy0 + 16 + row * 100
        draw.rectangle([cx, cy, cx + cwid, cy + ch], fill=CARD, outline=LINE, width=1)
        draw_mini(draw, i, cx + 1, cy + 1, cwid - 2, 30, field)
        draw.text((cx + 8, cy + 36), region + "  •  " + field, font=F_SANS_B(9), fill=RED)
        tlines = wrap(title, F_SANS_B(12), cwid - 16, draw)
        ty = cy + 50
        for line in tlines[:2]:
            draw.text((cx + 8, ty), line, font=F_SANS_B(12), fill=INK)
            ty += 14
        draw.text((cx + 8, cy + 80), sub, font=F_SANS(9), fill=(90, 88, 82))

    # ---- briefs (tighter pitch so the last row clears the footer)
    by0 = 786
    draw.text((8, by0 - 2), "THE DAY IN BRIEF  —  24 MORE STORIES", font=F_SANS_B(11), fill=NAVY)
    draw.line([8, by0 + 14, 1016, by0 + 14], fill=RED, width=2)
    for i, (region, field, text) in enumerate(BRIEFS):
        col, row = divmod(i, 8)
        bx = 8 + col * 336
        by = by0 + 18 + row * 25
        draw.text((bx, by), "%02d" % (i + 1), font=F_SANS_B(11), fill=RED)
        lines = wrap(text, F_SANS(10), 300, draw)
        ty = by
        for line in lines[:2]:
            draw.text((bx + 26, ty), line, font=F_SANS(10), fill=INK)
            ty += 12

    # ---- footer
    draw.line([8, 1006, 1016, 1006], fill=LINE, width=1)
    draw.text((8, 1010),
              "Sources: Reuters  •  BBC  •  AP  •  Science Magazine  •  FCC  •  KCNA  •  Bank of Korea  •  The Edge",
              font=F_SANS(9), fill=GREY)
    draw.text((W - 8 - draw.textlength("THE WORLD TODAY — 27 NOVEMBER 2026", font=F_SANS_B(9)), 1010),
              "THE WORLD TODAY — 27 NOVEMBER 2026", font=F_SANS_B(9), fill=GREY)

    img.save(OUT, format="PNG", optimize=False)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    paint()
