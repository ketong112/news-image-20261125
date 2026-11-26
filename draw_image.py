#!/usr/bin/env python3
"""Draw the front page that sums up Wednesday 25 November 2026 in one image.

Deterministic: no network, no clock, no randomness. Same input bytes in,
same PNG bytes out. Run:  python3 draw_image.py  ->  entry.png (1024x1024).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (247, 242, 232)
INK = (26, 26, 26)
MUTED = (90, 84, 74)
RED = (179, 32, 44)
NAVY = (23, 54, 93)
RULE = (26, 26, 26)
SKY = (207, 227, 238)
SEA = (46, 111, 158)
STEEL = (70, 78, 88)
ORANGE = (232, 116, 24)
GOLD = (233, 178, 44)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def fit(draw, text, fnt, max_w):
    """Truncate text with an ellipsis so it fits max_w pixels."""
    if text_w(draw, text, fnt) <= max_w:
        return text
    ell = "..."
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if text_w(draw, text[:mid] + ell, fnt) <= max_w:
            lo = mid
        else:
            hi = mid - 1
    return text[:lo] + ell


def wrap(draw, text, fnt, max_w, max_lines):
    """Greedy word wrap, at most max_lines; last line gets an ellipsis."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
        if len(lines) == max_lines:
            break
    if len(lines) < max_lines and cur:
        lines.append(cur)
    if len(lines) == max_lines and (cur and lines[-1] != cur):
        lines[-1] = fit(draw, lines[-1], fnt, max_w)
    return lines[:max_lines]


def flame(d, x, y, s):
    """A small stylised flame: outer orange, inner gold."""
    d.polygon([(x, y), (x + 0.45 * s, y - 0.9 * s), (x + 0.7 * s, y - 0.35 * s),
               (x + s, y - 1.05 * s), (x + 1.35 * s, y - 0.25 * s),
               (x + 1.7 * s, y - 0.6 * s), (x + 1.9 * s, y),
               (x + 1.55 * s, y + 0.25 * s), (x + 0.4 * s, y + 0.25 * s)],
              fill=ORANGE)
    d.polygon([(x + 0.55 * s, y), (x + 0.85 * s, y - 0.55 * s),
               (x + 1.1 * s, y - 0.1 * s), (x + 1.35 * s, y - 0.5 * s),
               (x + 1.5 * s, y), (x + 1.2 * s, y + 0.18 * s),
               (x + 0.8 * s, y + 0.18 * s)], fill=GOLD)


def smoke(d, x, y, r, color=(120, 120, 118)):
    for dx, dy, rr in ((0, 0, r), (r * 0.9, -r * 0.7, r * 0.8),
                       (-r * 0.8, -r * 0.8, r * 0.75), (r * 0.3, -r * 1.5, r * 0.7)):
        d.ellipse([x + dx - rr, y + dy - rr, x + dx + rr, y + dy + rr], fill=color)


def scene_tanker(d, x, y, w, h):
    """Strait of Hormuz: a tanker, a spiked mine, fire on the water."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA)
    for i in range(5):
        yy = y + h * (0.68 + i * 0.07)
        d.line([x + 8, yy, x + w - 8, yy], fill=(120, 170, 205), width=2)
    # hull + containers
    d.polygon([(x + 18, y + h * 0.52), (x + w - 18, y + h * 0.52),
               (x + w - 34, y + h * 0.72), (x + 34, y + h * 0.72)], fill=(38, 44, 54))
    for i, c in enumerate(((179, 32, 44), (233, 178, 44), (46, 111, 158))):
        d.rectangle([x + 34 + i * 26, y + h * 0.30, x + 56 + i * 26, y + h * 0.52], fill=c)
    d.rectangle([x + w - 78, y + h * 0.34, x + w - 52, y + h * 0.52], fill=(240, 240, 235))
    # spiked mine, upper right
    mx, my, mr = x + w - 52, y + 34, 13
    for a in range(0, 360, 45):
        import math
        rad = math.radians(a)
        d.line([mx + int(mr * 0.7 * math.cos(rad)), my + int(mr * 0.7 * math.sin(rad)),
                mx + int(mr * 1.5 * math.cos(rad)), my + int(mr * 1.5 * math.sin(rad))],
               fill=(20, 20, 20), width=3)
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(20, 20, 20))
    flame(d, x + w - 96, y + h * 0.52, 16)
    smoke(d, x + w - 78, y + 62, 9)


def scene_refinery(d, x, y, w, h):
    """Ras Tanura: refinery towers under a dusk sky, one burning."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 176))
    d.ellipse([x + w - 52, y + 10, x + w - 16, y + 46], fill=(240, 196, 90))
    base = y + h
    for tx, tw, th in ((14, 26, 58), (52, 20, 78), (84, 30, 66)):
        d.rectangle([x + tx, base - th, x + tx + tw, base], fill=STEEL)
        d.rectangle([x + tx - 3, base - th - 8, x + tx + tw + 3, base - th], fill=(52, 58, 66))
    d.rectangle([x + 128, base - 46, x + w - 14, base], fill=(96, 104, 114))
    d.rectangle([x + 138, base - 60, x + 168, base - 46], fill=(120, 128, 138))
    flame(d, x + 56, base - 78, 15)
    smoke(d, x + 66, base - 96, 10)
    d.rectangle([x, base - 4, x + w, base], fill=(52, 58, 66))


def scene_chart(d, x, y, w, h):
    """Markets: a red line falling across the panel, bars sinking."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    for i in range(1, 4):
        yy = y + i * h / 4
        d.line([x + 10, yy, x + w - 10, yy], fill=(225, 225, 225), width=1)
    pts = [(x + 14, y + 14), (x + w * 0.28, y + 26), (x + w * 0.48, y + 22),
           (x + w * 0.66, y + 48), (x + w * 0.84, y + 62), (x + w - 14, y + h - 12)]
    d.line(pts, fill=RED, width=4, joint="curve")
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    for i, bh in enumerate((34, 26, 30, 18, 12)):
        bx = x + 22 + i * 34
        d.rectangle([bx, y + h - 10 - bh, bx + 20, y + h - 10], fill=(179, 32, 44))


def scene_power(d, x, y, w, h):
    """Zaporizhzhia: a cooling tower, a bolt, a small drone overhead."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 232))
    d.polygon([(x + 18, y + h - 8), (x + 34, y + 18), (x + 74, y + 18),
               (x + 90, y + h - 8)], fill=(150, 158, 166))
    d.polygon([(x + 34, y + 18), (x + 40, y + 10), (x + 68, y + 10),
               (x + 74, y + 18)], fill=(120, 128, 136))
    d.polygon([(x + 52, y + 26), (x + 40, y + 52), (x + 52, y + 52),
               (x + 44, y + 74), (x + 64, y + 46), (x + 52, y + 46)],
              fill=GOLD)
    # drone: body + four rotors
    dx, dy = x + w - 52, y + 26
    d.rectangle([dx - 12, dy - 5, dx + 12, dy + 5], fill=(38, 44, 54))
    for sx in (-16, 16):
        d.line([dx + sx - 8, dy - 8, dx + sx + 8, dy - 8], fill=(38, 44, 54), width=2)
    d.line([x + 8, y + h - 8, x + w - 8, y + h - 8], fill=(90, 98, 108), width=3)


def scene_skyline(d, x, y, w, h):
    """Gaza: a city skyline at dusk with a smoke plume."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 210, 186))
    d.ellipse([x + 12, y + 12, x + 44, y + 44], fill=(240, 196, 90))
    base = y + h
    for bx, bw, bh in ((8, 30, 52), (44, 24, 70), (74, 34, 58), (114, 26, 78)):
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(96, 88, 82))
        for wy in range(base - bh + 8, base - 8, 12):
            for wx in range(x + bx + 5, x + bx + bw - 4, 10):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(233, 210, 186))
    smoke(d, x + 88, base - 88, 11)
    flame(d, x + 78, base - 62, 12)

# (number, region, headline, one-line summary) — every story happened, or was
# first reported, on Wednesday 25 November 2026.
HERO = [
    ("MIDDLE EAST",
     "Tankers strike mines in the Strait of Hormuz",
     "Two oil tankers hit naval mines and catch fire; Iran's Guards blame an unauthorised route."),
    ("MIDDLE EAST",
     "Houthis hit Saudi refinery and Riyadh tower",
     "Houthis claim a strike on Ras Tanura refinery; a Riyadh tower is hit, 11 people hurt."),
    ("MARKETS & TECH",
     "Tech sell-off deepens; US unveils new tariffs",
     "Kospi -6.2%, Nasdaq -2.4% as AI shares slide; US tariffs up to 35% on 14 economies."),
]

WIDE = [
    ("UKRAINE WAR",
     "Zaporizhzhia plant loses power; refineries burn",
     "Plant switches to diesel generators; Ukrainian drones set two Russian refineries ablaze."),
    ("MIDDLE EAST",
     "Hamas security chief killed in Gaza strike",
     "Israeli strike kills the group's security chief, his wife and two children, officials say."),
]

MORE = [
    (6, "MARKETS & TECH", "Huawei convicted in US trial",
     "Guilty of trade-secret theft."),
    (7, "ASIA-PACIFIC", "China flies first foreign astronaut",
     "Pakistani flies on Shenzhou-24."),
    (8, "MARKETS & TECH", "Microsoft declares 'Code Red'",
     "Outlook outage, 24 hours."),
    (9, "AFRICA", "RSF drone strikes kill 19 in Sudan",
     "Civilians die in two cities."),
    (10, "ASIA-PACIFIC", "Australia seals Solomons pact",
     "Treaty bars any foreign base."),
    (11, "CLIMATE", "Pope laments COP31 failure",
     "Pope warns extreme weather grows."),
    (12, "ASIA-PACIFIC", "Bangladesh raises garment wage 36%",
     "Minimum pay rises to $139."),
    (13, "MARKETS & TECH", "CIA and ODNI hit by cyber breach",
     "CIA, ODNI data breached."),
    (14, "AFRICA", "Militants kill at least 30 in Nigeria",
     "Attackers strike Niger region."),
    (15, "ASIA-PACIFIC", "26 miners feared trapped in Indonesia",
     "Missing at an illegal gold mine."),
    (16, "EUROPE", "BBC strike and Eurostar disruption",
     "Journalists strike; trains halt."),
    (17, "MARKETS & TECH", "Japan aims to be world No. 3 in AI",
     "Tokyo targets No. 3 in AI."),
    (18, "EUROPE", "Turkish helicopter crash kills 5",
     "Aircraft down in Turkiye; 5 die."),
    (19, "AFRICA", "Ten die in bus-truck crash in Egypt",
     "Collision in the country's south."),
    (20, "ASIA-PACIFIC", "China sentences official to death",
     "Leaked 100+ state secrets."),
    (21, "AMERICAS", "US drones help catch 'El Chapo Isidro'",
     "Mexico captures suspect, US help."),
    (22, "ASIA-PACIFIC", "Hasina sets 16 December return date",
     "Dhaka insists on extradition."),
    (23, "AMERICAS", "Venezuela reveals $237.5bn debt pile",
     "Debt pile revealed in restructuring."),
    (24, "AMERICAS", "Ecuador, US weigh joint operations",
     "Joint operations assessed."),
    (25, "EUROPE", "Poland plans eastern no-fly zone",
     "NATO asked to weigh downing."),
    (26, "EUROPE", "Serbia eyes TV curbs, 4-day week",
     "Reality-TV curbs, 4-day week floated."),
    (27, "EUROPE", "Ex-Srebrenica commander arrested",
     "Oric held over fugitive links."),
    (28, "MARKETS & TECH", "Decathlon breach exposes 130,000",
     "Customer data leaked."),
    (29, "AFRICA", "Congo rebels halt advance on Bunia",
     "Group pulls back; violence rises."),
    (30, "UKRAINE WAR", "Hungary PM meets Zelensky",
     "First visit since 2015; gas deal."),
    (31, "UKRAINE WAR", "Ukraine defends Benghazi ship strike",
     "Kyiv: lawful self-defence."),
    (32, "UKRAINE WAR", "Leaked data: ~490,000 Russian dead",
     "Toll near 500,000, BBC says."),
    (33, "MIDDLE EAST", "Israeli rivals agree coalition pact",
     "Eisenkot, Lieberman join forces."),
    (34, "SPORT", "Lakers beat Jazz; Sinner sidelined",
     "Doncic scores 28; Sinner out long."),
    (35, "EUROPE", "Puigdemont declares 12 Dec return",
     "Catalan leader to return to Spain."),
]

REGION_COLORS = {
    "MIDDLE EAST": (179, 32, 44),
    "UKRAINE WAR": (23, 54, 93),
    "EUROPE": (46, 90, 140),
    "ASIA-PACIFIC": (0, 122, 94),
    "AFRICA": (150, 90, 20),
    "AMERICAS": (104, 62, 140),
    "MARKETS & TECH": (120, 40, 90),
    "CLIMATE": (60, 120, 40),
    "SPORT": (170, 110, 0),
}


def hero_panel(d, x, y, w, h, region, headline, summary, scene):
    d.rectangle([x, y, x + w, y + h], outline=(200, 192, 176), width=1)
    scene(d, x + 1, y + 1, w - 2, 92)
    d.rectangle([x, y + 93, x + w, y + 96], fill=RED)
    tx = x + 12
    d.text((tx, y + 104), region, font=font(SANS_B, 11), fill=RED)
    for i, line in enumerate(wrap(d, headline, font(SANS_B, 16), w - 24, 2)):
        d.text((tx, y + 122 + i * 20), line, font=font(SANS_B, 16), fill=INK)
    for i, line in enumerate(wrap(d, summary, font(SANS, 12), w - 24, 2)):
        d.text((tx, y + 164 + i * 15), line, font=font(SANS, 12), fill=MUTED)


def wide_panel(d, x, y, w, h, region, headline, summary, scene):
    d.rectangle([x, y, x + w, y + h], outline=(200, 192, 176), width=1)
    scene(d, x + 1, y + 1, 150, h - 2)
    d.rectangle([x + 151, y, x + 154, y + h], fill=RED)
    tx = x + 168
    d.text((tx, y + 12), region, font=font(SANS_B, 11), fill=RED)
    for i, line in enumerate(wrap(d, headline, font(SANS_B, 17), w - 182, 2)):
        d.text((tx, y + 30 + i * 21), line, font=font(SANS_B, 17), fill=INK)
    for i, line in enumerate(wrap(d, summary, font(SANS, 12), w - 182, 2)):
        d.text((tx, y + 76 + i * 15), line, font=font(SANS, 12), fill=MUTED)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 28  # margin
    # ---- masthead ----
    d.text((W // 2, 26), "THE WORLD IN ONE DAY",
           font=font(SERIF_B, 52), fill=INK, anchor="ma")
    d.rectangle([m, 92, W - m, 95], fill=RULE)
    d.rectangle([m, 98, W - m, 99], fill=RULE)
    d.text((W // 2, 106), "WEDNESDAY  ·  25 NOVEMBER 2026",
           font=font(SANS_B, 19), fill=NAVY, anchor="ma")
    d.text((W // 2, 130), "35 STORIES  ·  9 REGIONS  ·  ONE PAGE",
           font=font(SANS, 12), fill=MUTED, anchor="ma")
    # ---- hero row: three biggest stories ----
    hy, hh = 158, 208
    col_w = (W - 2 * m - 2 * 16) // 3
    scenes = (scene_tanker, scene_refinery, scene_chart)
    for i, (region, headline, summary) in enumerate(HERO):
        hero_panel(d, m + i * (col_w + 16), hy, col_w, hh,
                   region, headline, summary, scenes[i])
    # ---- second row: two wide stories ----
    wy, wh = 378, 122
    wide_w = (W - 2 * m - 16) // 2
    wide_panel(d, m, wy, wide_w, wh, *WIDE[0], scene_power)
    wide_panel(d, m + wide_w + 16, wy, wide_w, wh, *WIDE[1], scene_skyline)
    # ---- markets strip ----
    sy = 512
    d.rectangle([m, sy, W - m, sy + 34], fill=NAVY)
    strip = ("MARKETS   KOSPI -6.2%   ·   TAIEX -4.8%   ·   NASDAQ -2.4%   ·   "
             "S&P 500 -1.9%   ·   SOFTBANK -14%   ·   GOLD -3%")
    d.text((W // 2, sy + 17), strip, font=font(SANS_B, 13),
           fill=(255, 255, 255), anchor="mm")
    # ---- the day in 30 more stories ----
    ly = 560
    d.text((m, ly), "THE DAY IN 30 MORE STORIES",
           font=font(SANS_B, 14), fill=INK)
    d.text((W - m, ly), "25 NOV 2026", font=font(SANS_B, 14),
           fill=RED, anchor="ra")
    d.rectangle([m, ly + 22, W - m, ly + 23], fill=RULE)
    rows = 10
    row_h = 38
    top = ly + 34
    cw = (W - 2 * m - 2 * 16) // 3
    for idx, (num, region, headline, summary) in enumerate(MORE):
        col, row = idx // rows, idx % rows
        x = m + col * (cw + 16)
        y = top + row * row_h
        d.text((x, y), "%02d" % num, font=font(SANS_B, 13), fill=RED)
        hx = x + 30
        d.text((hx, y), fit(d, headline, font(SANS_B, 13), cw - 30),
               font=font(SANS_B, 13), fill=INK)
        d.text((hx, y + 17), fit(d, region + "  —  " + summary, font(SANS, 11), cw - 30),
               font=font(SANS, 11), fill=MUTED)
        if row < rows - 1:
            d.line([x, y + 36, x + cw, y + 36], fill=(222, 214, 198), width=1)
    # ---- footer ----
    fy = 982
    d.rectangle([m, fy, W - m, fy + 1], fill=RULE)
    d.text((W // 2, fy + 10),
           "All 35 stories happened, or were first reported, on Wednesday 25 November 2026.",
           font=font(SANS, 12), fill=INK, anchor="ma")
    d.text((W // 2, fy + 28),
           "Sources: AP · Reuters · BBC · IAEA · make.fun news-image-20261125",
           font=font(SANS, 11), fill=MUTED, anchor="ma")
    img.save(OUT, format="PNG", optimize=True)
    return OUT


if __name__ == "__main__":
    path = build()
    import hashlib
    data = open(path, "rb").read()
    print(path, len(data), "bytes", hashlib.sha256(data).hexdigest())
