# render_artwork.py - draws entry.png for news-image-20261119.
#
# A dark "night edition" front page: the world news of Thursday
# 19 November 2026 on one 1024x1024 sheet. Local tooling only
# (Python + Pillow); the harness never runs this file. The shipped
# program is main.ts, which copies the finished entry.png to the
# grader's output. Deterministic: same pixels in, same PNG out.

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

SIDE = 1024
MX = 46                      # page margin
W = SIDE - 2 * MX            # text column width

INK = (12, 20, 36)           # page background, deep ink navy
PANEL = (19, 31, 54)         # panel background
HAIR = (51, 69, 107)         # hairline rules
PAPER = (242, 234, 216)      # main text, warm paper white
MUTE = (159, 176, 201)       # secondary text
GOLD = (217, 164, 65)        # accent
RED = (224, 72, 62)          # breaking / kicker accent
DARK = (20, 15, 4)           # text on the gold ticker band

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(path, size, text, max_w, min_size=12):
    """Largest font at or below size whose text fits max_w."""
    while size > min_size:
        f = font(path, size)
        if f.getlength(text) <= max_w:
            return f
        size -= 1
    return font(path, min_size)


def wrap(draw, text, f, max_w):
    """Greedy word wrap by measured width."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_h(f, extra=0):
    a, d = f.getmetrics()
    return a + d + extra


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def burst(draw, cx, cy, r, fill):
    pts = []
    for i in range(16):
        ang = i * math.pi / 8
        rad = r if i % 2 == 0 else r * 0.38
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def gradient(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    steps = max(1, y1 - y0)
    for i in range(steps):
        t = i / steps
        c = tuple(round(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def flag_china(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(draw, x + w * 0.26, y + h * 0.32, h * 0.17, (255, 222, 0))
    for dx, dy in ((0.48, 0.16), (0.54, 0.34), (0.54, 0.54), (0.46, 0.68)):
        draw.ellipse([x + w * dx - 3, y + h * dy - 3,
                      x + w * dx + 3, y + h * dy + 3], fill=(255, 222, 0))


def flag_usa(draw, x, y, w, h):
    stripe = h / 7
    for i in range(7):
        c = (179, 34, 52) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=c)
    cw, ch = w * 0.44, stripe * 4
    draw.rectangle([x, y, x + cw, y + ch], fill=(60, 59, 110))
    for r in range(3):
        for cix in range(4):
            cx = x + cw * (cix + 0.5) / 4
            cy = y + ch * (r + 0.5) / 3
            draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 255, 255))


def flag_russia(draw, x, y, w, h):
    third = h / 3
    for i, c in enumerate(((255, 255, 255), (0, 57, 166), (213, 43, 30))):
        draw.rectangle([x, y + i * third, x + w, y + (i + 1) * third], fill=c)


def palm(draw, bx, by, s, color):
    """A simple palm silhouette: leaning trunk plus five fronds."""
    top = (bx + 0.35 * s, by - s)
    pts = []
    for i in range(9):
        t = i / 8
        pts.append((bx + 0.35 * s * t * t, by - s * t))
    draw.line(pts, fill=color, width=max(3, int(s * 0.09)))
    for ang in (-165, -125, -85, -45, -8):
        ex = top[0] + 0.62 * s * math.cos(math.radians(ang))
        ey = top[1] + 0.34 * s * math.sin(math.radians(ang)) + 0.16 * s
        mid = (top[0] + 0.34 * s * math.cos(math.radians(ang)),
               top[1] + 0.40 * s * math.sin(math.radians(ang)))
        draw.line([top, mid, (ex, ey)], fill=color, width=max(3, int(s * 0.06)))


def main():
    img = Image.new("RGB", (SIDE, SIDE), INK)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.line([(MX, 32), (SIDE - MX, 32)], fill=GOLD, width=3)
    name_f = fit(SERIF_B, 58, "THE WORLD TODAY", 596)
    d.text((MX, 50), "THE WORLD TODAY", font=name_f, fill=PAPER)
    d.text((MX, 128), "The whole day's news, on a single page",
           font=font(SANS, 19), fill=MUTE)
    d.line([(706, 48), (706, 170)], fill=GOLD, width=2)
    rx = SIDE - MX
    thu_f = font(SANS_B, 23)
    d.text((rx, 46), "THURSDAY", font=thu_f, fill=GOLD, anchor="ra")
    big_f = font(SERIF_B, 84)
    d.text((rx, 68), "19", font=big_f, fill=GOLD, anchor="ra")
    nov_f = fit(SANS_B, 23, "NOVEMBER 2026", 250)
    d.text((rx, 150), "NOVEMBER 2026", font=nov_f, fill=PAPER, anchor="ra")
    d.line([(MX, 190), (SIDE - MX, 190)], fill=GOLD, width=3)
    d.line([(MX, 197), (SIDE - MX, 197)], fill=HAIR, width=1)

    # ---------- hero: the Shenzhen trilateral ----------
    y = 210
    d.text((MX, y), "SHENZHEN - APEC SUMMIT - THE LEAD STORY",
           font=font(SANS_B, 20), fill=RED)
    y += 34
    head_f = fit(SERIF_B, 58, "XI, TRUMP AND PUTIN,", W)
    for line in ("XI, TRUMP AND PUTIN,", "FACE TO FACE"):
        d.text((MX, y), line, font=head_f, fill=PAPER)
        y += text_h(head_f, 1)
    y += 2
    deck_f = font(SANS, 23)
    deck = ("China, the United States and Russia hold their first "
            "three-way summit at Kylin Villa - nuclear arms atop the "
            "agenda, and no agreement expected.")
    for line in wrap(d, deck, deck_f, W):
        d.text((MX, y), line, font=deck_f, fill=(216, 222, 233))
        y += 31

    # hero visual strip: night skyline, three flags over a long table;
    # its position follows the deck so the two never collide
    sy0, sy1 = y + 12, y + 94
    gradient(d, (MX, sy0, SIDE - MX, sy1), (22, 38, 63), (8, 13, 24))
    d.ellipse([846, sy0 + 8, 876, sy0 + 38], fill=GOLD)
    rng = [7, 13, 5, 17, 9, 21, 11, 6, 15, 8, 19, 12, 5, 16, 10, 14]
    bx = MX + 6
    for i, bh in enumerate(rng):
        bw = 46
        d.rectangle([bx, sy1 - 20 - bh, bx + bw, sy1 - 20], fill=(4, 7, 14))
        for wy in range(sy1 - 26 - bh, sy1 - 24, 9):
            for wx in range(bx + 6, bx + bw - 6, 11):
                if (wx * 31 + wy * 17) % 13 < 4:
                    d.point((wx, wy), fill=GOLD)
        bx += bw + 8
    table_y = sy1 - 14
    d.rectangle([MX + 130, table_y, SIDE - MX - 130, table_y + 10], fill=(107, 79, 42))
    d.line([(MX + 130, table_y), (SIDE - MX - 130, table_y)], fill=GOLD, width=2)
    for cx, draw_flag in ((330, flag_china), (512, flag_usa), (694, flag_russia)):
        d.line([(cx, table_y), (cx, sy0 + 44)], fill=(140, 148, 165), width=3)
        draw_flag(d, cx - 32, sy0 + 4, 64, 40)

    # ---------- second row: two panels ----------
    py0, py1 = sy1 + 20, 802
    pw = (W - 22) // 2
    # left: GTA VI, neon dusk panel
    gx0, gx1 = MX, MX + pw
    gradient(d, (gx0, py0, gx1, py1), (150, 23, 130), (46, 13, 74))
    palm(d, gx0 + 46, py1 - 6, 76, (16, 5, 24))
    palm(d, gx1 - 84, py1 - 6, 58, (16, 5, 24))
    d.text((gx0 + 22, py0 + 16), "LAUNCH DAY - ENTERTAINMENT",
           font=font(SANS_B, 16), fill=(255, 205, 92))
    gh_f = font(SERIF_B, 31)
    gy = py0 + 44
    for line in ("VICE CITY", "OPENS AT LAST"):
        d.text((gx0 + 22, gy), line, font=gh_f, fill=(255, 255, 255))
        gy += text_h(gh_f, 1)
    gd_f = font(SANS, 19)
    gdeck = ("Grand Theft Auto VI rolls out worldwide after a 13-year "
             "wait, landing a Metacritic 99 that ties the all-time record.")
    gy += 4
    for line in wrap(d, gdeck, gd_f, pw - 44):
        d.text((gx0 + 22, gy), line, font=gd_f, fill=(245, 230, 245))
        gy += 25

    # right: Crimean Bridge panel
    cx0, cx1 = MX + pw + 22, SIDE - MX
    d.rectangle([cx0, py0, cx1, py1], fill=PANEL, outline=HAIR, width=1)
    d.text((cx0 + 22, py0 + 16), "UKRAINE - CRIMEA",
           font=font(SANS_B, 16), fill=RED)
    ch_f = fit(SERIF_B, 31, "CRIMEAN BRIDGE HIT AGAIN", pw - 44)
    cy = py0 + 46
    d.text((cx0 + 22, cy), "CRIMEAN BRIDGE HIT AGAIN", font=ch_f, fill=PAPER)
    cy += text_h(ch_f, 6)
    cdeck = ("An overnight strike - the third this week - halts traffic "
             "on the Kerch crossing, and Crimea's Moscow-installed chief "
             "confirms the closure.")
    for line in wrap(d, cdeck, gd_f, pw - 44):
        d.text((cx0 + 22, cy), line, font=gd_f, fill=(216, 222, 233))
        cy += 25
    # bridge glyph: two pylons, a broken deck, one burst
    by = cy + 26
    d.line([(cx0 + 24, by), (cx0 + 190, by)], fill=MUTE, width=4)
    d.line([(cx0 + 268, by), (cx1 - 24, by)], fill=MUTE, width=4)
    for px in (cx0 + 60, cx1 - 60):
        d.line([(px, by - 30), (px, by + 8)], fill=MUTE, width=4)
    burst(d, cx0 + 229, by - 8, 16, (240, 140, 40))

    # ---------- third row: two text columns ----------
    ty = 826
    d.line([(512, ty + 2), (512, 946)], fill=HAIR, width=1)
    colw = pw - 12
    k_f = font(SANS_B, 16)
    h3_f = font(SERIF_B, 26)
    d3_f = font(SANS, 19)
    d.text((MX, ty), "MARKETS - ARTIFICIAL INTELLIGENCE", font=k_f, fill=GOLD)
    d.text((MX, ty + 26), "ANTHROPIC'S RECORD DEBUT", font=h3_f, fill=PAPER)
    yy = ty + 66
    for line in wrap(d, "The AI lab starts trading on Nasdaq today after "
                        "an $81.3bn IPO, the largest on record.", d3_f, colw):
        d.text((MX, yy), line, font=d3_f, fill=(216, 222, 233))
        yy += 25
    x2 = MX + pw + 22
    d.text((x2, ty), "WASHINGTON", font=k_f, fill=GOLD)
    d.text((x2, ty + 26), "A FIRST AT THE CAPITOL", font=h3_f, fill=PAPER)
    yy = ty + 66
    for line in wrap(d, "House Democrats nominate Hakeem Jeffries, 251-11 - "
                        "the first Black Speaker within reach.", d3_f, colw):
        d.text((x2, yy), line, font=d3_f, fill=(216, 222, 233))
        yy += 25

    # ---------- ticker band ----------
    d.rectangle([0, 958, SIDE, SIDE], fill=GOLD)
    t_f = fit(SANS_B, 19, "HORMUZ - TANKER STRUCK NEAR KHASAB, CREW SAFE - "
                          "BRUSSELS - EU FLOATS A 45BN-EURO UKRAINE LOAN", 984)
    line1 = ("HORMUZ - TANKER STRUCK NEAR KHASAB, CREW SAFE - "
             "BRUSSELS - EU FLOATS A 45BN-EURO UKRAINE LOAN")
    line2 = ("PRAGUE MARCHES FOR PRESS FREEDOM - "
             "ISRAEL - HERZOG ASKS EISENKOT TO FORM A GOVERNMENT")
    d.text((SIDE // 2, 968), line1, font=t_f, fill=DARK, anchor="ma")
    t2_f = fit(SANS_B, 19, line2, 984)
    d.text((SIDE // 2, 994), line2, font=t2_f, fill=DARK, anchor="ma")

    img.save(OUT, format="PNG")
    print("wrote", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
