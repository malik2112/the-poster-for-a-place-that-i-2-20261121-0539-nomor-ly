#!/usr/bin/env python3
"""The Poster for a Place That Isn't There — ORINTH.

Deterministic PIL travel poster (1024x1024 PNG) for an invented desert
city: a glass-domed oasis town under a low amber sun, with an hourglass
clock tower as its landmark, mesas and dunes behind, palms and a teal
pool in front. The only text in the picture is the place name, set in
the umber band at the foot.
No network; fixed-seed detail only.
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
DEST = "/output/entry.png"
dice = random.Random(20261121)

FONT_HINTS = ["/usr/share/fonts/truetype/liberation", "/usr/share/fonts/truetype/dejavu"]

def serif(size):
    for folder in FONT_HINTS:
        for fname in ("LiberationSerif-Bold.ttf", "DejaVuSerif-Bold.ttf"):
            cand = os.path.join(folder, fname)
            if os.path.isfile(cand):
                return ImageFont.truetype(cand, size)
    return ImageFont.load_default()

IVORY = (250, 243, 226)
COAL = (44, 32, 28)
UMBER = (74, 44, 32)
UMBER_D = (52, 30, 24)
SAND = (232, 184, 120)
SAND_L = (246, 212, 152)
CLAY = (178, 98, 62)
CLAY_D = (140, 72, 46)
TEAL = (46, 140, 138)
TEAL_L = (110, 196, 188)
PALM = (52, 120, 74)
PALM_D = (34, 88, 54)
AMBER = (252, 196, 96)
GLASS = (196, 230, 238)

canvas = Image.new("RGB", (SIDE, SIDE), IVORY)
pen = ImageDraw.Draw(canvas)

LEFT, TOP, RIGHT, BOTTOM = 36, 36, SIDE - 36, SIDE - 36
NAME_TOP = 872

def blend(col_a, col_b, frac):
    return tuple(int(round(col_a[k] + (col_b[k] - col_a[k]) * frac)) for k in range(3))

# ---------- dusk sky ----------
sky_high = (52, 48, 92)
sky_mid = (196, 102, 74)
sky_low = (250, 196, 120)
for yy in range(TOP, 640):
    pos = (yy - TOP) / (640 - TOP)
    tone = blend(sky_high, sky_mid, pos / 0.55) if pos < 0.55 else blend(sky_mid, sky_low, (pos - 0.55) / 0.45)
    pen.line([(LEFT, yy), (RIGHT, yy)], fill=tone)

# early stars in the indigo band + thin dusk clouds + distant birds
for _ in range(90):
    star_x = dice.randint(LEFT + 8, RIGHT - 8)
    star_y = dice.randint(TOP + 8, 210)
    star_r = dice.choice([1, 1, 2])
    pen.ellipse([star_x - star_r, star_y - star_r, star_x + star_r, star_y + star_r], fill=(240, 236, 220))
for cloud_x, cloud_y, cloud_w in [(190, 150, 150), (770, 120, 120), (860, 240, 96)]:
    pen.line([(cloud_x - cloud_w // 2, cloud_y), (cloud_x + cloud_w // 2, cloud_y)], fill=(150, 96, 106), width=5)
    pen.line([(cloud_x - cloud_w // 3, cloud_y + 8), (cloud_x + cloud_w // 3, cloud_y + 8)], fill=(122, 78, 94), width=3)
for bird_x, bird_y, bird_s in [(250, 230, 12), (300, 252, 9), (700, 200, 10)]:
    pen.arc([bird_x - bird_s, bird_y - bird_s // 2, bird_x, bird_y + bird_s // 2], start=200, end=330, fill=COAL, width=2)
    pen.arc([bird_x, bird_y - bird_s // 2, bird_x + bird_s, bird_y + bird_s // 2], start=210, end=340, fill=COAL, width=2)

# ---------- low sun with halo ----------
sun_x, sun_y, sun_r = 512, 430, 118
glow = Image.new("RGBA", (SIDE, SIDE), (0, 0, 0, 0))
glow_pen = ImageDraw.Draw(glow)
glow_pen.ellipse([sun_x - sun_r - 44, sun_y - sun_r - 44, sun_x + sun_r + 44, sun_y + sun_r + 44], fill=(254, 214, 140, 30))
canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), glow).convert("RGB"), (0, 0))
pen = ImageDraw.Draw(canvas)
pen.ellipse([sun_x - sun_r, sun_y - sun_r, sun_x + sun_r, sun_y + sun_r], fill=AMBER)
pen.ellipse([sun_x - sun_r + 16, sun_y - sun_r + 16, sun_x + sun_r - 16, sun_y + sun_r - 16], fill=(254, 214, 130))

# ---------- distant mesas ----------
pen.polygon([(LEFT, 560), (LEFT, 470), (210, 452), (330, 478), (430, 560)], fill=(122, 76, 72))
pen.polygon([(560, 560), (660, 460), (820, 446), (RIGHT, 500), (RIGHT, 560)], fill=(110, 66, 66))
pen.polygon([(LEFT, 600), (LEFT, 520), (260, 500), (520, 530), (RIGHT, 512), (RIGHT, 600)], fill=CLAY_D)

# ---------- dune field ----------
pen.polygon([(LEFT, NAME_TOP), (LEFT, 640), (300, 600), (620, 626), (RIGHT, 606), (RIGHT, NAME_TOP)], fill=CLAY)
pen.polygon([(LEFT, NAME_TOP), (LEFT, 700), (360, 660), (700, 692), (RIGHT, 672), (RIGHT, NAME_TOP)], fill=SAND)

# ---------- glass dome town (centre-left) ----------
dome_cx, dome_base, dome_r = 330, 690, 150
pen.pieslice([dome_cx - dome_r, dome_base - dome_r, dome_cx + dome_r, dome_base + dome_r], start=180, end=360, fill=GLASS)
pen.arc([dome_cx - dome_r, dome_base - dome_r, dome_cx + dome_r, dome_base + dome_r], start=180, end=360, fill=IVORY, width=4)
pen.line([(dome_cx - dome_r, dome_base), (dome_cx + dome_r, dome_base)], fill=IVORY, width=4)
# glass panel seams + a bright reflection sweep
for seam_dx in (-90, -45, 45, 90):
    pen.line([(dome_cx + seam_dx, dome_base), (dome_cx + seam_dx // 3, dome_base - dome_r + 18)], fill=(236, 248, 250), width=2)
pen.arc([dome_cx - 96, dome_base - 128, dome_cx + 10, dome_base - 30], start=190, end=300, fill=(255, 255, 252), width=7)
for tower_x, tower_h, tower_w in [(250, 66, 34), (300, 88, 40), (356, 58, 30), (396, 74, 36)]:
    pen.rectangle([tower_x, dome_base - tower_h, tower_x + tower_w, dome_base], fill=UMBER)
    pen.polygon([(tower_x - 4, dome_base - tower_h), (tower_x + tower_w + 4, dome_base - tower_h), (tower_x + tower_w // 2, dome_base - tower_h - 18)], fill=CLAY_D)
    pen.rectangle([tower_x + 8, dome_base - tower_h + 12, tower_x + 14, dome_base - tower_h + 22], fill=AMBER)
    pen.rectangle([tower_x + tower_w - 14, dome_base - tower_h + 12, tower_x + tower_w - 8, dome_base - tower_h + 22], fill=AMBER)
pen.ellipse([dome_cx - 18, dome_base - dome_r - 12, dome_cx + 18, dome_base - dome_r + 12], fill=AMBER)

# ---------- hourglass clock tower (landmark, centre-right) ----------
tx, tbase = 700, 700
pen.rectangle([tx - 34, tbase - 240, tx + 34, tbase], fill=UMBER_D)
pen.polygon([(tx - 44, tbase - 240), (tx + 44, tbase - 240), (tx, tbase - 286)], fill=CLAY_D)
pen.polygon([(tx - 22, tbase - 226), (tx + 22, tbase - 226), (tx, tbase - 168)], fill=SAND_L)
pen.polygon([(tx - 22, tbase - 110), (tx + 22, tbase - 110), (tx, tbase - 168)], fill=SAND_L)
pen.line([(tx - 22, tbase - 226), (tx + 22, tbase - 226)], fill=IVORY, width=3)
pen.line([(tx - 22, tbase - 110), (tx + 22, tbase - 110)], fill=IVORY, width=3)
# falling sand stream + warm glow at the waist of the glass
pen.line([(tx, tbase - 196), (tx, tbase - 138)], fill=AMBER, width=3)
pen.ellipse([tx - 10, tbase - 178, tx + 10, tbase - 158], fill=AMBER)
pen.line([(tx - 30, tbase - 240), (tx + 30, tbase - 240)], fill=IVORY, width=2)
pen.rectangle([tx - 10, tbase - 60, tx + 10, tbase], fill=COAL)
pen.ellipse([tx - 7, tbase - 300, tx + 7, tbase - 286], fill=AMBER)

# small domes flanking the tower
for scx, sbase, sr in [(590, 692, 52), (812, 692, 60)]:
    pen.pieslice([scx - sr, sbase - sr, scx + sr, sbase + sr], start=180, end=360, fill=GLASS)
    pen.arc([scx - sr, sbase - sr, scx + sr, sbase + sr], start=180, end=360, fill=IVORY, width=3)
    pen.rectangle([scx - 12, sbase - 30, scx + 12, sbase], fill=UMBER)

# ---------- oasis foreground ----------
pen.polygon([(LEFT, NAME_TOP), (LEFT, 782), (340, 750), (700, 782), (RIGHT, 762), (RIGHT, NAME_TOP)], fill=SAND_L)
pen.ellipse([300, 788, 724, 862], fill=TEAL)
pen.ellipse([330, 798, 694, 852], fill=TEAL_L)
pen.arc([380, 812, 560, 846], start=10, end=170, fill=IVORY, width=3)
pen.arc([470, 820, 640, 850], start=10, end=170, fill=IVORY, width=3)

def palm(px, py, tall, lean):
    pen.line([(px, py), (px + lean // 2, py - tall // 2), (px + lean, py - tall)], fill=UMBER, width=7)
    tip_x, tip_y = px + lean, py - tall
    for spread, lift, droop in [(-62, 20, 30), (-38, 28, 22), (-14, 32, 14), (14, 32, 14), (38, 28, 22), (62, 20, 30)]:
        end_x = tip_x + spread
        end_y = tip_y + droop
        mid_x = tip_x + spread // 2
        mid_y = tip_y - lift
        pen.line([(tip_x, tip_y), (mid_x, mid_y), (end_x, end_y)], fill=PALM_D, width=5)
        pen.line([(mid_x, mid_y), (end_x, end_y)], fill=PALM, width=2)
    pen.ellipse([tip_x - 6, tip_y - 4, tip_x + 6, tip_y + 8], fill=UMBER)

palm(210, 830, 96, 14)
palm(806, 836, 104, -16)
palm(262, 852, 64, 10)
palm(756, 858, 60, -10)

# wind ripples on the sand + scattered stones and dry tufts
for _ in range(36):
    rip_x = dice.randint(LEFT + 16, RIGHT - 70)
    rip_y = dice.randint(724, NAME_TOP - 16)
    pen.arc([rip_x, rip_y, rip_x + 54, rip_y + 14], start=190, end=340, fill=(214, 158, 96), width=2)
for stone_x, stone_y, stone_w in [(150, 842, 26), (876, 822, 30), (120, 800, 18), (920, 856, 22)]:
    pen.polygon([(stone_x - stone_w // 2, stone_y), (stone_x - stone_w // 4, stone_y - 12), (stone_x + stone_w // 4, stone_y - 12), (stone_x + stone_w // 2, stone_y)], fill=(150, 104, 78))
for tuft_x, tuft_y in [(176, 858), (842, 862), (96, 840)]:
    for blade_dx in (-8, -3, 3, 8):
        pen.line([(tuft_x, tuft_y), (tuft_x + blade_dx, tuft_y - 18)], fill=PALM_D, width=2)

# ---------- name band: the only text ----------
pen.rectangle([LEFT, NAME_TOP, RIGHT, BOTTOM], fill=UMBER_D)
pen.line([(LEFT + 48, NAME_TOP + 22), (RIGHT - 48, NAME_TOP + 22)], fill=AMBER, width=2)
word = "ORINTH"
pt = 78
gap = 16
while pt > 30:
    face = serif(pt)
    widths = [pen.textlength(ch, font=face) for ch in word]
    span = sum(widths) + gap * (len(word) - 1)
    if span <= (RIGHT - LEFT - 100):
        break
    pt -= 4
cursor = (SIDE - span) / 2
for ch, wch in zip(word, widths):
    pen.text((cursor, NAME_TOP + 34), ch, font=face, fill=IVORY)
    cursor += wch + gap

# ---------- print grain (deterministic) ----------
speck = Image.new("RGBA", (SIDE, SIDE), (0, 0, 0, 0))
speck_pen = ImageDraw.Draw(speck)
for _ in range(2000):
    dot_x = dice.randint(0, SIDE - 1)
    dot_y = dice.randint(0, SIDE - 1)
    dot_a = dice.randint(4, 11)
    speck_pen.point((dot_x, dot_y), fill=(40, 28, 20, dot_a) if dice.random() < 0.5 else (255, 248, 230, dot_a))
canvas = Image.alpha_composite(canvas.convert("RGBA"), speck).convert("RGB")
pen = ImageDraw.Draw(canvas)

# ---------- border ----------
pen.rectangle([LEFT, TOP, RIGHT, BOTTOM], outline=COAL, width=3)
pen.rectangle([18, 18, SIDE - 18, SIDE - 18], outline=COAL, width=1)

os.makedirs("/output", exist_ok=True)
canvas.save(DEST, "PNG", optimize=True)
print(f"wrote {DEST}: {os.path.getsize(DEST)} bytes, {canvas.size}")
