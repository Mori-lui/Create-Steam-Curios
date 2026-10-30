"""Draw the 16x16 pixel-art item textures for Create: Steam Curios with Pillow."""
from PIL import Image
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "src", "main", "resources", "assets", "steamcurios", "textures")

# palette
OUTLINE = (35, 26, 7)
BRASS = (183, 135, 39)
BRASS_L = (219, 170, 66)
BRASS_D = (125, 94, 25)
BRASS_DD = (94, 70, 16)
GLASS = (168, 212, 240)
GLASS_L = (222, 240, 250)
GLASS_D = (118, 162, 198)
IRON = (214, 214, 214)
IRON_D = (146, 146, 146)
FIRE = (221, 84, 52)
FIRE_L = (243, 158, 74)
FIRE_C = (255, 222, 130)
BLUE = (94, 200, 242)
BLUE_L = (176, 236, 255)
BLUE_D = (44, 130, 193)
FUR = (140, 111, 71)
FUR_D = (105, 83, 51)
FUR_L = (170, 139, 92)
WHITE = (245, 245, 245)
COG = (60, 52, 40)


def canvas():
    return Image.new("RGBA", (16, 16), (0, 0, 0, 0))


def disc(img, cx=7.5, cy=7.5, r_out=7.2):
    """Return per-pixel distance and paint the brass disc shell with outline."""
    for y in range(16):
        for x in range(16):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if d <= r_out:
                if d > r_out - 1.0:
                    img.putpixel((x, y), OUTLINE)
                else:
                    # light from top-left, shadow bottom-right
                    lx = (x - cx) + (y - cy)
                    if lx < -3.5:
                        c = BRASS_L
                    elif lx > 4.0:
                        c = BRASS_D
                    else:
                        c = BRASS
                    img.putpixel((x, y), c)


def center_disc(img, colors, cx=7.5, cy=7.5, r=3.4):
    """Paint a smaller inner disc: colors = (light, base, dark)."""
    for y in range(16):
        for x in range(16):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if d <= r:
                lx = (x - cx) + (y - cy)
                if lx < -1.5:
                    img.putpixel((x, y), colors[0])
                elif lx > 1.8:
                    img.putpixel((x, y), colors[2])
                else:
                    img.putpixel((x, y), colors[1])


def rivets(img, positions):
    for (x, y) in positions:
        img.putpixel((x, y), BRASS_DD)
        img.putpixel((x - 1, y), BRASS_D)


def save(img, *path):
    p = os.path.join(OUT, *path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    img.save(p)
    print("wrote", p)


# --- brass_medallion: brass disc, glass manometer centre, 4 rivets
img = canvas()
disc(img)
center_disc(img, (GLASS_L, GLASS, GLASS_D))
img.putpixel((7, 7), WHITE)
img.putpixel((6, 7), GLASS_L)
rivets(img, [(7, 2), (7, 13), (2, 7), (13, 7)])
save(img, "item", "brass_medallion.png")

# --- incomplete_heater_charm: medallion + fur patch
img = canvas()
disc(img)
center_disc(img, (BRASS_L, BRASS, BRASS_D))
for y in range(3, 8):
    for x in range(8, 13):
        d = ((x - 10.0) ** 2 + (y - 5.0) ** 2) ** 0.5
        if d <= 2.6:
            if d <= 1.2:
                img.putpixel((x, y), FUR_D)
            elif (x + y) % 3 == 0:
                img.putpixel((x, y), FUR_L)
            else:
                img.putpixel((x, y), FUR)
save(img, "item", "incomplete_heater_charm.png")

# --- steam_heater_charm: brass disc with a lit boiler core
img = canvas()
disc(img)
center_disc(img, (FIRE_L, FIRE, FIRE))
for (x, y) in [(7, 8), (8, 8), (8, 7)]:
    img.putpixel((x, y), FIRE_C)
img.putpixel((6, 9), FIRE_C)
rivets(img, [(7, 1), (7, 14)])
img.putpixel((7, 0), IRON)
img.putpixel((7, 1), IRON_D)
save(img, "item", "steam_heater_charm.png")

# --- auto_thermostat: brass disc with a white dial and red needle
img = canvas()
disc(img)
center_disc(img, (WHITE, WHITE, GLASS_D))
for (x, y) in [(7, 5), (5, 8), (10, 8), (7, 10)]:
    img.putpixel((x, y), OUTLINE)
for (x, y) in [(8, 6), (7, 7), (6, 8)]:
    img.putpixel((x, y), (200, 40, 30))
rivets(img, [(3, 4), (12, 11)])
save(img, "item", "auto_thermostat.png")

# --- isothermal_amulet: silver-blue frame, ice crystal core
img = canvas()
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
                if lx < -1.5:
                    img.putpixel((x, y), BLUE_L)
                elif lx > 2.0:
                    img.putpixel((x, y), BLUE_D)
                else:
                    img.putpixel((x, y), BLUE)
img.putpixel((7, 7), WHITE)
img.putpixel((8, 6), BLUE_L)
save(img, "item", "isothermal_amulet.png")

# --- thermostat_core: dark mechanism plate with a brass cog
img = canvas()
for y in range(2, 14):
    for x in range(2, 14):
        img.putpixel((x, y), COG if x in (2, 13) or y in (2, 13) else (76, 66, 52))
center_disc(img, (BRASS_L, BRASS, BRASS_D), r=2.9)
for (x, y) in [(7, 3), (7, 12), (3, 7), (12, 7)]:
    img.putpixel((x, y), BRASS_L)
for (x, y) in [(4, 4), (11, 4), (4, 11), (11, 11)]:
    img.putpixel((x, y), IRON)
    img.putpixel((x, y + 1), IRON_D)
save(img, "item", "thermostat_core.png")

# --- entity/amulet.png: flat brass plate texture for the body model
img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
for y in range(16):
    for x in range(16):
        lx = (x - 7.5) + (y - 7.5)
        if x in (0, 15) or y in (0, 15):
            c = OUTLINE
        elif lx < -4:
            c = BRASS_L
        elif lx > 5:
            c = BRASS_D
        else:
            c = BRASS
        img.putpixel((x, y), c)
for (x, y) in [(5, 5), (10, 5), (5, 10), (10, 10)]:
    img.putpixel((x, y), BRASS_DD)
img.putpixel((7, 7), GLASS_L)
img.putpixel((8, 7), GLASS)
img.putpixel((7, 8), GLASS_D)
save(img, "entity", "amulet.png")
