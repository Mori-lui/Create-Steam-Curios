"""Round 2: reworked auto_thermostat (hot/cold mixer) and refined isothermal coil.

  auto_thermostat   «Смеситель»: hot pipe (ember) + cold pipe (water) merge into a
                    brass mixing chamber — the amulet literally mixes heat and water.
  isothermal_amulet «Спиральный конденсатор v2»: wrap rings instead of crossing arcs,
                    big faceted crystal with halo, rising bubbles, radiator fins.

Output: tools/gallery5/*.png + fragment.html
"""
from PIL import Image, ImageDraw
import math
import os
import base64

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "gallery5")
os.makedirs(OUT, exist_ok=True)

P = dict(outline=(32, 26, 16), steel=(118, 122, 130), steel_hi=(162, 167, 176), steel_lo=(70, 72, 78),
         brass=(190, 140, 46), brass_hi=(228, 180, 78), brass_lo=(116, 84, 26),
         copper=(196, 108, 56), copper_hi=(232, 150, 84),
         water=(52, 120, 196), water_hi=(116, 190, 242), water_lo=(30, 78, 140),
         ember=(235, 120, 45), ember_hi=(255, 216, 110),
         chain=(158, 160, 168), dial=(228, 233, 239), crystal=(110, 220, 255),
         crystal_hi=(200, 244, 255), glass=(198, 228, 246, 55))


def disc(d, cx, cy, r, fill, steps=20):
    pts = [(cx + r * math.cos(2 * math.pi * i / steps), cy + r * math.sin(2 * math.pi * i / steps))
           for i in range(steps)]
    d.polygon(pts, fill=fill)


def chain(d, cx, top_y, u, p, links=3, fine=False):
    w = max(1, int(u * (0.26 if fine else 0.36)))
    for k in range(links):
        ly = top_y - (k + 0.55) * 1.6 * u
        w1 = 0.55 * (0.7 if fine else 1.0) * u
        d.ellipse([cx - w1, ly, cx + w1, ly + 1.55 * u], outline=p["chain"], width=w)
    r = 0.8 * (0.75 if fine else 1.0) * u
    d.ellipse([cx - r, top_y - r * 0.6, cx + r, top_y + r * 1.4], outline=p["chain"], width=w)


# ------------- auto_thermostat: hot/cold mixer -------------
def draw_mixer(d, S, u, state, frame=0):
    cx = S / 2
    p = P
    chain(d, cx, 3.0 * u, u, p)
    # top mixing chamber
    d.rounded_rectangle([cx - 3.6 * u, 3.4 * u, cx + 3.6 * u, 6.6 * u], radius=u * 0.7,
                        fill=p["brass"], outline=p["outline"])
    d.rectangle([cx - 3.6 * u, 3.4 * u, cx - 2.5 * u, 6.6 * u], fill=p["brass_hi"])
    for bx in (-2.6, 2.6):
        r = u * 0.35
        d.ellipse([cx + bx * u - r, 5.0 * u - r, cx + bx * u + r, 5.0 * u + r],
                  fill=p["steel_hi"], outline=p["outline"])
    # small dial on the chamber
    d.ellipse([cx - 1.1 * u, 4.0 * u, cx + 1.1 * u, 6.2 * u], fill=p["dial"], outline=p["outline"])
    na = 2.4 if state == "idle" else (2.4 + 0.45 * math.sin(frame) if state == "steam" else 3.6)
    d.line([cx, 5.1 * u, cx + 0.75 * u * math.cos(na), 5.1 * u + 0.75 * u * math.sin(na)],
           fill=(200, 44, 30), width=max(1, int(u * 0.25)))
    # two vertical pipes: hot (left, copper) and cold (right, steel)
    pipes = ((cx - 2.9 * u, p["copper"], p["copper_hi"]), (cx + 1.0 * u, p["steel"], p["steel_hi"]))
    for (x0, body, hi) in pipes:
        d.rounded_rectangle([x0, 6.4 * u, x0 + 1.9 * u, 13.0 * u], radius=u * 0.3,
                            fill=body, outline=p["outline"])
        d.rectangle([x0 + 0.25 * u, 6.6 * u, x0 + 0.55 * u, 12.8 * u], fill=hi)
    # hot window: ember flicker
    if state == "dry":
        d.rounded_rectangle([cx - 2.6 * u, 8.0 * u, cx - 1.3 * u, 10.6 * u], radius=u * 0.25,
                            fill=(30, 24, 20), outline=p["outline"])
    else:
        fl = int(170 + 60 * math.sin(frame * 1.3))
        d.rounded_rectangle([cx - 2.6 * u, 8.0 * u, cx - 1.3 * u, 10.6 * u], radius=u * 0.25,
                            fill=p["ember"], outline=p["outline"])
        d.ellipse([cx - 2.25 * u, 8.9 * u, cx - 1.65 * u, 9.9 * u], fill=(*p["ember_hi"], fl))
    # cold window: water level + flow
    d.rounded_rectangle([cx + 1.3 * u, 8.0 * u, cx + 2.6 * u, 10.6 * u], radius=u * 0.25,
                        fill=p["glass"], outline=p["outline"])
    if state != "dry":
        lvl = 0.35 if state == "steam" else 0.55
        d.rectangle([cx + 1.45 * u, 8.0 * u + (10.6 * u - 8.0 * u) * lvl, cx + 2.45 * u, 10.45 * u],
                    fill=p["water"])
        if state == "steam":
            for k in range(2):
                by = 9.9 * u - ((frame * 0.9 + k * 1.6) % 3) * 0.55 * u
                d.ellipse([cx + 1.7 * u - 0.18 * u, by - 0.18 * u, cx + 1.7 * u + 0.18 * u, by + 0.18 * u],
                          outline=p["water_hi"], width=1)
    # bottom merge block + outlet
    d.rounded_rectangle([cx - 3.4 * u, 12.8 * u, cx + 3.4 * u, 14.8 * u], radius=u * 0.4,
                        fill=p["brass"], outline=p["outline"])
    d.rectangle([cx - 0.7 * u, 14.8 * u, cx + 0.7 * u, 15.6 * u], fill=p["brass_lo"],
                outline=p["outline"])
    if state == "steam":
        for k in range(2):
            r = u * (0.28 + 0.14 * ((frame + k) % 3))
            xx = cx + (2.2 * u if k else -2.2 * u)
            yy = 2.6 * u - (frame % 3) * 0.5 * u
            d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=(240, 247, 252, 226 - k * 36))


# ------------- isothermal: coil capacitor v2 -------------
def draw_coil2(d, S, u, state, frame=0):
    cx = S / 2
    p = P
    chain(d, cx, 1.7 * u, u, p, fine=True, links=3)
    # radiator fins behind the tube (top and bottom)
    for (fy0, fy1) in ((2.6 * u, 4.0 * u), (12.6 * u, 14.0 * u)):
        for fx in (-2.6, -1.3, 0, 1.3, 2.6):
            d.rectangle([cx + fx * u - 0.2 * u, fy0, cx + fx * u + 0.2 * u, fy1],
                        fill=p["steel_lo"], outline=p["outline"])
    # hex caps
    for cy in (4.4 * u, 12.4 * u):
        pts = [(cx + 3.3 * u * math.cos(math.pi / 6 + i / 6 * 2 * math.pi),
                cy + 1.4 * u * math.sin(math.pi / 6 + i / 6 * 2 * math.pi)) for i in range(6)]
        d.polygon(pts, fill=p["brass"], outline=p["outline"])
        d.point((cx - 1.0 * u, cy - 0.3 * u), fill=p["brass_hi"])
    # glass tube
    tx0, tx1 = cx - 1.8 * u, cx + 1.8 * u
    d.rounded_rectangle([tx0, 4.8 * u, tx1, 12.0 * u], radius=u * 0.8,
                        fill=p["glass"], outline=p["outline"])
    # crystal: big faceted diamond with halo
    ky = 8.4 * u
    if state == "dry":
        d.polygon([(cx, ky - 2.0 * u), (cx + 1.5 * u, ky), (cx, ky + 2.0 * u), (cx - 1.5 * u, ky)],
                  fill=(64, 90, 110), outline=p["outline"])
    else:
        pulse = int(120 + 60 * math.sin(frame * 1.1))
        d.ellipse([cx - 2.3 * u, ky - 2.6 * u, cx + 2.3 * u, ky + 2.6 * u],
                  fill=(*p["crystal"], pulse))
        d.polygon([(cx, ky - 2.1 * u), (cx + 1.6 * u, ky), (cx, ky + 2.1 * u), (cx - 1.6 * u, ky)],
                  fill=p["crystal"], outline=p["outline"])
        d.polygon([(cx, ky - 1.0 * u), (cx + 0.75 * u, ky), (cx, ky + 1.0 * u), (cx - 0.75 * u, ky)],
                  fill=p["crystal_hi"])
        d.point((cx - 0.35 * u, ky - 0.7 * u), fill=(255, 255, 255))
    # wrap rings around the tube (3 turns)
    for yy in (5.8 * u, 8.4 * u, 11.0 * u):
        d.rounded_rectangle([cx - 2.4 * u, yy - 0.45 * u, cx + 2.4 * u, yy + 0.45 * u],
                            radius=u * 0.2, fill=p["copper"], outline=p["outline"])
        d.rectangle([cx - 2.4 * u, yy - 0.45 * u, cx + 2.4 * u, yy - 0.1 * u], fill=p["copper_hi"])
    # bubbles rising inside the glass when steaming
    if state == "steam":
        for k in range(3):
            bx = cx + (k - 1) * 0.55 * u
            by = 11.0 * u - ((frame * 0.8 + k * 2.4) % 6) * u
            r = u * 0.16
            d.ellipse([bx - r, by - r, bx + r, by + r], outline=p["water_hi"], width=1)
    if state == "steam":
        d.point((cx + 2.9 * u, 3.4 * u - (frame % 3) * 0.7 * u), fill=(255, 255, 255))
        d.point((cx - 2.9 * u, 13.6 * u + (frame % 3) * 0.7 * u), fill=(*p["water_hi"], 220))


ITEMS = {
    "auto_thermostat": ("Смеситель (автотермостат)", draw_mixer),
    "isothermal_amulet": ("Спиральный конденсатор v2", draw_coil2),
}

files = []
for key, (label, painter) in ITEMS.items():
    for state in ("idle", "steam", "dry"):
        for size in (32, 64):
            img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            painter(d, size, size / 16.0, state, frame=0)
            name = f"{key}_{state}_{size}.png"
            img.save(os.path.join(OUT, name))
            files.append(name)
    frames = []
    for f in range(10):
        img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        painter(d, 32, 2.0, "steam", frame=f)
        frames.append(img)
    frames[0].save(os.path.join(OUT, f"{key}_anim.gif"), save_all=True,
                   append_images=frames[1:], duration=150, loop=0)
    files.append(f"{key}_anim.gif")
print("generated", len(files), "files")


def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()


cards = []
for key, (label, _) in ITEMS.items():
    c = f'<div class="stycell"><div class="styname">{label}</div><div class="row">'
    for st, stl in (("idle", "покой"), ("steam", "работа (пар)"), ("dry", "сухой")):
        c += (f'<div class="grp"><div class="grpname">{stl}</div><div class="imgs">'
              f'<figure><img src="data:image/png;base64,{b64(os.path.join(OUT, key + "_" + st + "_32.png"))}" width="80" height="80" class="pix"></figure>'
              f'<figure><img src="data:image/png;base64,{b64(os.path.join(OUT, key + "_" + st + "_64.png"))}" width="128" height="128" class="pix"></figure>'
              f'</div></div>')
    c += (f'<div class="grp"><div class="grpname">анимация</div>'
          f'<img src="data:image/gif;base64,{b64(os.path.join(OUT, key + "_anim.gif"))}" width="96" height="96" class="pix"></div>')
    c += '</div>'
    cards.append(c)

html = ('<div id="texture-designs2">' + "".join(cards) + '</div>'
        '<style>#texture-designs2{display:grid;gap:16px}'
        '#texture-designs2 .stycell{border-top:1px solid var(--border);padding-top:10px}'
        '#texture-designs2 .styname{font-weight:500;margin-bottom:6px}'
        '#texture-designs2 .row{display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start}'
        '#texture-designs2 .grpname{font-size:12px;color:var(--muted-foreground);margin-bottom:2px}'
        '#texture-designs2 .imgs{display:flex;gap:10px;align-items:flex-end}'
        '#texture-designs2 figure{margin:0;text-align:center}'
        '#texture-designs2 .pix{image-rendering:pixelated;background:var(--muted);border-radius:6px}</style>')
open(os.path.join(OUT, "fragment.html"), "w", encoding="utf-8").write(html)
print("fragment.html", len(html) // 1024, "KB")
