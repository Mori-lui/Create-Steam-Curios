"""Final amulet designs: three DISTINCT silhouettes in the Create pipe/brass family,
all with prominent chains (icon + separate body-chain texture).

  steam_heater_charm  «Кольцо-трубопровод»  - brass pipe ring, water flow, small valve
  auto_thermostat     «Маностанция»         - big pressure gauge on a pipe tree, water side-branch
  isothermal_amulet   «Спиральный конденсатор» - copper coil around a glowing crystal, coolant dashes

Output: straight into src textures (only on user approval) -> tools/gallery4 for preview.
"""
from PIL import Image, ImageDraw
import math
import os
import base64

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "gallery4")
os.makedirs(OUT, exist_ok=True)

P = dict(outline=(32, 26, 16), steel=(118, 122, 130), steel_hi=(162, 167, 176), steel_lo=(70, 72, 78),
         brass=(190, 140, 46), brass_hi=(228, 180, 78), brass_lo=(116, 84, 26),
         water=(52, 120, 196), water_hi=(116, 190, 242), water_lo=(30, 78, 140),
         glass=(198, 228, 246, 55), ember=(235, 120, 45), ember_hi=(255, 216, 110),
         chain=(158, 160, 168), dial=(228, 233, 239), crystal=(110, 220, 255),
         crystal_hi=(196, 242, 255), coil=(196, 108, 56), coil_hi=(232, 150, 84))


def disc(d, cx, cy, r, fill, steps=20):
    pts = [(cx + r * math.cos(2 * math.pi * i / steps), cy + r * math.sin(2 * math.pi * i / steps))
           for i in range(steps)]
    d.polygon(pts, fill=fill)


def chain(d, cx, top_y, u, p, links=3, lw=None, fine=False):
    """Prominent chain going up from the pendant; returns nothing."""
    w = max(1, int(u * (0.28 if fine else 0.38)))
    for k in range(links):
        ly = top_y - (k + 0.55) * 1.6 * u
        w1 = 0.55 * (0.7 if fine else 1.0) * u
        d.ellipse([cx - w1, ly, cx + w1, ly + 1.55 * u], outline=p["chain"], width=w)
    # attachment ring on the pendant
    r = 0.8 * (0.75 if fine else 1.0) * u
    d.ellipse([cx - r, top_y - r * 0.6, cx + r, top_y + r * 1.4], outline=p["chain"], width=w)


# ------------- painter 1: pipe-ring brooch -------------
def draw_ring(d, S, u, state, frame=0):
    p = P
    cx = S / 2
    chain(d, cx, 3.1 * u, u, p)
    R = 5.1 * u
    wt = 1.5 * u
    d.ellipse([cx - R, S / 2 - R, cx + R, S / 2 + R], outline=p["outline"], width=max(4, int(wt + 1.2 * u)))
    d.ellipse([cx - R, S / 2 - R, cx + R, S / 2 + R], outline=p["brass"], width=max(3, int(wt)))
    r_in = R - wt
    d.ellipse([cx - r_in, S / 2 - r_in, cx + r_in, S / 2 + r_in], fill=p["glass"])
    if state != "dry":
        d.pieslice([cx - r_in, S / 2 - r_in, cx + r_in, S / 2 + r_in], 0, 180, fill=p["water"])
        d.pieslice([cx - r_in, S / 2 - r_in, cx + r_in, S / 2 + r_in], 0, 22, fill=p["water_lo"])
        for seg in range(3):
            base = seg * (2 * math.pi / 3) + 0.35
            for k in range(3):
                a = base + ((frame * 0.35 + k * 0.24) % (2 * math.pi / 3 - 0.55))
                d.ellipse([cx + R * math.cos(a) - 0.32 * u, S / 2 + R * math.sin(a) - 0.32 * u,
                           cx + R * math.cos(a) + 0.32 * u, S / 2 + R * math.sin(a) + 0.32 * u],
                          fill=p["water_hi"])
    for a in (0.785, 2.36, 3.93, 5.5):
        bx, by = cx + R * math.cos(a), S / 2 + R * math.sin(a)
        r = u * 0.5
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=p["steel_hi"], outline=p["outline"])
        d.point((bx - r * 0.4, by - r * 0.4), fill=p["outline"])
    # center valve
    va = 0.0 if state != "steam" else frame * 0.9
    gear(d, cx, S / 2, 2.0 * u, 4, p["brass_hi"], ang=va, hole=(52, 120, 196, 255))
    d.ellipse([cx - 0.38 * u, S / 2 - 0.38 * u, cx + 0.38 * u, S / 2 + 0.38 * u],
              fill=p["brass_lo"], outline=p["outline"])
    if state == "steam":
        for k in range(2):
            r = u * (0.3 + 0.16 * ((frame + k) % 3))
            d.ellipse([cx + (0.5 * u if k else -0.5 * u) - r, 1.0 * u - (frame % 3) * 0.55 * u - r,
                       cx + (0.5 * u if k else -0.5 * u) + r, 1.0 * u - (frame % 3) * 0.55 * u + r],
                      fill=(240, 247, 252, 228 - k * 36))


def gear(d, cx, cy, r, teeth, fill, ang=0.0, hole=None):
    n = teeth * 2
    pts = []
    for i in range(n):
        a = ang + i / n * 2 * math.pi
        rr = r if i % 2 == 0 else r * 0.74
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)
    if hole:
        hr = r * 0.4
        d.polygon([(cx + hr * math.cos(2 * math.pi * i / 18), cy + hr * math.sin(2 * math.pi * i / 18))
                   for i in range(18)], fill=hole)


# ------------- painter 2: gauge station -------------
def draw_gauge(d, S, u, state, frame=0):
    p = P
    cx = S / 2
    chain(d, cx, 2.2 * u, u, p)
    # big pressure gauge
    gy = 6.6 * u
    R = 4.6 * u
    d.ellipse([cx - R, gy - R, cx + R, gy + R], fill=p["steel"], outline=p["outline"])
    d.ellipse([cx - R + 0.5 * u, gy - R + 0.5 * u, cx + R - 0.5 * u, gy + R - 0.5 * u],
              fill=p["brass_lo"], outline=p["outline"])
    d.ellipse([cx - R + 1.1 * u, gy - R + 1.1 * u, cx + R - 1.1 * u, gy + R - 1.1 * u],
              fill=p["dial"], outline=p["outline"])
    for a in range(10):
        ang = math.pi * 0.15 + a / 9 * math.pi * 0.7 * 2
        x1 = cx + (R - 1.5 * u) * math.cos(ang)
        y1 = gy + (R - 1.5 * u) * math.sin(ang)
        x2 = cx + (R - 2.1 * u) * math.cos(ang)
        y2 = gy + (R - 2.1 * u) * math.sin(ang)
        d.line([x1, y1, x2, y2], fill=(70, 74, 82))
    na = (2.6 if state == "idle" else (2.6 + 0.5 * math.sin(frame) if state == "steam" else 3.9))
    d.line([cx, gy, cx + (R - 1.9 * u) * math.cos(na), gy + (R - 1.9 * u) * math.sin(na)],
           fill=(200, 44, 30), width=max(1, int(u * 0.3)))
    d.ellipse([cx - 0.35 * u, gy - 0.35 * u, cx + 0.35 * u, gy + 0.35 * u], fill=p["outline"])
    # glass shine
    d.arc([cx - R + 1.3 * u, gy - R + 1.3 * u, cx + R - 1.3 * u, gy + R - 1.3 * u], 200, 250,
          fill=(255, 255, 255, 150))
    # vertical pipe below gauge -> T junction
    d.rectangle([cx - 0.9 * u, gy + R - 0.4 * u, cx + 0.9 * u, 12.4 * u], fill=p["brass"],
                outline=p["outline"])
    d.rectangle([cx - 0.9 * u, gy + R - 0.4 * u, cx - 0.4 * u, 12.4 * u], fill=p["brass_hi"])
    d.rounded_rectangle([cx - 3.4 * u, 12.2 * u, cx + 3.4 * u, 14.2 * u], radius=u * 0.4,
                        fill=p["brass"], outline=p["outline"])
    # side branch with water window
    d.rounded_rectangle([cx + 2.2 * u, 10.2 * u, S - 1.6 * u, 12.4 * u], radius=u * 0.35,
                        fill=p["steel"], outline=p["outline"])
    wx0, wy0, wx1, wy1 = cx + 2.7 * u, 10.7 * u, S - 2.1 * u, 11.9 * u
    d.rectangle([wx0, wy0, wx1, wy1], fill=p["glass"], outline=p["outline"])
    if state != "dry":
        d.rectangle([wx0 + 0.1 * u, wy0 + (wy1 - wy0) * 0.35, wx1 - 0.1 * u, wy1], fill=p["water"])
        for k in range(3):
            ph = ((frame * 0.9 + k * 1.5) % 4.5) / 4.5
            xx = wx0 + (wx1 - wx0 - 0.5 * u) * ph
            d.line([xx, wy0 + (wy1 - wy0) * 0.55, xx + 0.5 * u, wy0 + (wy1 - wy0) * 0.55],
                   fill=p["water_hi"], width=max(1, int(u * 0.22)))
    # small valve on the branch
    d.ellipse([cx - 2.9 * u, 13.2 * u - 0.7 * u, cx - 1.5 * u, 13.2 * u + 0.7 * u],
              fill=p["brass_hi"], outline=p["outline"])
    if state == "steam":
        r = u * (0.3 + 0.15 * (frame % 3))
        d.ellipse([cx - 0.4 * u, 1.4 * u - (frame % 3) * 0.5 * u - r, cx + 0.4 * u,
                   1.4 * u - (frame % 3) * 0.5 * u + r], fill=(240, 247, 252, 226))


# ------------- painter 3: coil capacitor -------------
def draw_coil(d, S, u, state, frame=0):
    p = P
    cx = S / 2
    chain(d, cx, 1.9 * u, u, p, fine=True, links=3)
    # hex end caps
    for (cy, col) in ((3.6 * u, p["brass"]), (S - 3.2 * u, p["brass"])):
        pts = [(cx + 3.4 * u * math.cos(math.pi / 6 + i / 6 * 2 * math.pi),
                cy + 1.5 * u * math.sin(math.pi / 6 + i / 6 * 2 * math.pi)) for i in range(6)]
        d.polygon(pts, fill=col, outline=p["outline"])
    # central glass tube
    tx0, tx1 = cx - 1.7 * u, cx + 1.7 * u
    d.rounded_rectangle([tx0, 4.2 * u, tx1, S - 3.8 * u], radius=u * 0.8,
                        fill=p["glass"], outline=p["outline"])
    # crystal core (glows, dim when dry)
    ky = S / 2 - 0.4 * u
    core = p["crystal"] if state != "dry" else (64, 90, 110)
    pts = [(cx + 1.2 * u * math.cos(math.pi / 6 + i / 6 * 2 * math.pi),
            ky + 1.9 * u * math.sin(math.pi / 6 + i / 6 * 2 * math.pi)) for i in range(6)]
    d.polygon(pts, fill=core, outline=p["outline"])
    if state != "dry":
        pulse = int(160 + 70 * math.sin(frame * 1.2))
        disc(d, cx, ky, 0.75 * u, (255, 255, 255, min(255, pulse + 60)))
        d.point((cx - 0.3 * u, ky - 0.5 * u), fill=(255, 255, 255))
    # copper coil turns across the tube
    for k in range(4):
        yy = 5.4 * u + k * 2.1 * u
        d.arc([cx - 2.6 * u, yy - 1.0 * u, cx + 2.6 * u, yy + 1.0 * u], 15, 165,
              fill=p["coil"], width=max(1, int(u * 0.42)))
        d.arc([cx - 2.6 * u, yy - 1.0 * u, cx + 2.6 * u, yy + 1.0 * u], 20, 80,
              fill=p["coil_hi"], width=max(1, int(u * 0.2)))
    # coolant dashes rising in the coil gaps
    if state == "steam":
        for k in range(3):
            yy = 6.0 * u + ((frame * 0.8 + k * 2.2) % 7) * u
            xx = cx - 2.3 * u if k % 2 == 0 else cx + 2.3 * u
            d.ellipse([xx - 0.22 * u, yy - 0.32 * u, xx + 0.22 * u, yy + 0.32 * u],
                      fill=(*p["water_hi"], 220))
    if state != "dry" and state == "steam":
        d.point((cx + 2.4 * u, 5.0 * u - (frame % 3) * 0.8 * u), fill=(255, 255, 255))
        d.point((cx + 2.4 * u, 5.6 * u - (frame % 3) * 0.8 * u), fill=(255, 255, 255))


DESIGNS = {
    "steam_heater_charm": ("Кольцо-трубопровод", draw_ring),
    "auto_thermostat": ("Маностанция", draw_gauge),
    "isothermal_amulet": ("Спиральный конденсатор", draw_coil),
}

files = []
for key, (label, painter) in DESIGNS.items():
    states = ("idle", "steam", "dry")
    for state in states:
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

# body chain texture: V-shaped links on 32x32
ch = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
dc = ImageDraw.Draw(ch)
for side in (-1, 1):
    for k in range(7):
        t = k / 6.0
        x = 16 + side * (13.5 * t)
        y = 2 + 20 * t
        r = 2.2 - 0.5 * t
        a = math.atan2(20, 13.5 * side) + math.pi / 2
        pts = [(x + r * math.cos(a + 2 * math.pi * i / 12), y + r * math.sin(a + 2 * math.pi * i / 12))
               for i in range(12)]
        dc.polygon(pts, outline=(150, 152, 160, 255))
        dc.line([(x - r * math.cos(a), y - r * math.sin(a)), (x + r * math.cos(a), y + r * math.sin(a))],
                fill=(190, 140, 46, 255), width=1)
ch.save(os.path.join(OUT, "chain_body_32.png"))
files.append("chain_body_32.png")
print("generated", len(files), "files")


def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()


cards = []
for key, (label, _) in DESIGNS.items():
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
cards.append('<div class="stycell"><div class="styname">Цепь на теле (текстура 32×32)</div>'
             f'<img src="data:image/png;base64,{b64(os.path.join(OUT, "chain_body_32.png"))}" width="128" height="128" class="pix"></div>')

html = ('<div id="texture-designs">' + "".join(cards) + '</div>'
        '<style>#texture-designs{display:grid;gap:16px}'
        '#texture-designs .stycell{border-top:1px solid var(--border);padding-top:10px}'
        '#texture-designs .styname{font-weight:500;margin-bottom:6px}'
        '#texture-designs .row{display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start}'
        '#texture-designs .grpname{font-size:12px;color:var(--muted-foreground);margin-bottom:2px}'
        '#texture-designs .imgs{display:flex;gap:10px;align-items:flex-end}'
        '#texture-designs figure{margin:0;text-align:center}'
        '#texture-designs .pix{image-rendering:pixelated;background:var(--muted);border-radius:6px}</style>')
open(os.path.join(OUT, "fragment.html"), "w", encoding="utf-8").write(html)
print("fragment.html", len(html) // 1024, "KB")
