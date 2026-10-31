"""Generate placeholder 16x16 state textures (steam / dry) from the base ones.

The real art will be replaced after the style is picked; these just prove the
custom_model_data state switching works in game.
"""
from PIL import Image, ImageDraw
import os

BASE = os.path.join(os.path.dirname(__file__), "..", "src", "main", "resources", "assets", "steamcurios", "textures", "item")
WHITE = (238, 246, 250, 235)
DARK = (60, 52, 40, 255)


def make_states(name):
    img = Image.open(os.path.join(BASE, name + ".png")).convert("RGBA")
    # steaming: puffs on top
    steam = img.copy()
    d = ImageDraw.Draw(steam)
    for (x, y, r) in [(6, 3, 1.5), (9, 2, 1.8), (11, 4, 1.2)]:
        d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)
    steam.save(os.path.join(BASE, name + "_steam.png"))
    # dry: dark core, no fire
    dry = img.copy()
    d2 = ImageDraw.Draw(dry)
    for y in range(5, 12):
        for x in range(5, 11):
            p = dry.getpixel((x, y))
            if p[3] > 0 and (p[0] > 150 and p[1] < 160):
                d2.point((x, y), fill=DARK)
    dry.save(os.path.join(BASE, name + "_dry.png"))
    print("states for", name)


for n in ["steam_heater_charm", "auto_thermostat"]:
    make_states(n)
