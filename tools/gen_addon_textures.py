"""Animated 16x16 frames (vertical strips) for the steamcurios_animated addon."""
from PIL import Image
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "addon", "src", "assets", "steamcurios", "textures", "item")
os.makedirs(OUT, exist_ok=True)

BRASS = (183, 135, 39)
BRASS_L = (219, 170, 66)
BRASS_D = (125, 94, 25)
OUTLINE = (35, 26, 7)
FIRE = (221, 84, 52)
FIRE_L = (243, 158, 74)
FIRE_C = (255, 222, 130)
IRON = (214, 214, 214)
IRON_D = (146, 146, 146)
BLUE = (94, 200, 242)
BLUE_L = (176, 236, 255)
BLUE_D = (44, 130, 193)
WHITE = (245, 245, 245)
DIAL = (228, 228, 228)


def disc(img, cx=7.5, cy=7.5, r_out=7.2):
    for y in range(16):
        for x in range(16):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if d <= r_out:
                if d > r_out - 1.0:
                    img.putpixel((x, y), OUTLINE)
                else:
                    lx = (x - cx) + (y - cy)
                    img.putpixel((x, y), BRASS_L if lx < -3.5 else (BRASS_D if lx > 4.0 else BRASS))


def strip(frames, name):
    w, h = 16, 16 * len(frames)
    sheet = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        sheet.paste(f, (0, i * 16))
    p = os.path.join(OUT, name)
    sheet.save(p)
    with open(p + ".mcmeta", "w") as fh:
        fh.write('{"animation": {"frametime": 3, "interpolate": false}}\n')
    print("wrote", p, "frames:", len(frames))


# --- steam_heater_charm: fire core flickers (steam puffs alternate)
frames = []
for k in range(4):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    disc(img)
    core = {(0, 7, 7), (1, 8, 8), (2, 7, 8), (3, 6, 8)} if k % 2 == 0 else \
           {(0, 8, 7), (1, 7, 8), (2, 8, 9), (3, 7, 9)}
    for y in range(6, 11):
        for x in range(6, 10):
            d = ((x - 7.5) ** 2 + (y - 8.0) ** 2) ** 0.5
            if d <= 2.2:
                img.putpixel((x, y), FIRE_L if k % 2 == 0 else FIRE)
    for idx, x, y in core:
        img.putpixel((x, y), FIRE_C)
    # steam wisps move with the frame
    wisps = [(7, 4), (7, 2)] if k in (0, 2) else [(6, 3), (8, 4)]
    for x, y in wisps:
        img.putpixel((x, y), (222, 236, 245, 200))
    img.putpixel((7, 0), IRON)
    img.putpixel((7, 1), IRON_D)
    frames.append(img)
strip(frames, "steam_heater_charm.png")

# --- auto_thermostat: dial needle sweeps, ticks around the dial
frames = []
angles = [(8, 5), (11, 8), (7, 11), (4, 8)]
for (nx, ny) in angles:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    disc(img)
    for y in range(5, 11):
        for x in range(5, 11):
            d = ((x - 7.5) ** 2 + (y - 7.5) ** 2) ** 0.5
            if d <= 2.9:
                img.putpixel((x, y), DIAL)
    for (x, y) in [(7, 5), (10, 8), (7, 10), (4, 8)]:
        img.putpixel((x, y), OUTLINE)
    # needle from center outward
    for f in range(4):
        x = 7 + round((nx - 7) * (f + 1) / 4.0)
        y = 7 + round((ny - 7) * (f + 1) / 4.0)
        img.putpixel((x, y), (200, 40, 30))
    frames.append(img)
strip(frames, "auto_thermostat.png")

# --- isothermal_amulet: crystal pulses bright/dim
frames = []
for k in range(4):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y in range(16):
        for x in range(16):
            d = ((x - 7.5) ** 2 + (y - 7.5) ** 2) ** 0.5
            if d <= 7.2:
                if d > 6.2:
                    img.putpixel((x, y), IRON_D if x + y > 15 else IRON)
                elif d > 4.6:
                    lx = (x - 7.5) + (y - 7.5)
                    img.putpixel((x, y), BRASS_L if lx < -2.5 else (BRASS_D if lx > 3.0 else BRASS))
                else:
                    lx = (x - 7.5) + (y - 7.5)
                    glow = (k in (1, 2))
                    if lx < -1.5:
                        img.putpixel((x, y), BLUE_L if glow else BLUE)
                    elif lx > 2.0:
                        img.putpixel((x, y), BLUE_D)
                    else:
                        img.putpixel((x, y), BLUE)
    if k in (1, 2):
        img.putpixel((7, 7), WHITE)
        img.putpixel((8, 6), BLUE_L)
    frames.append(img)
strip(frames, "isothermal_amulet.png")
