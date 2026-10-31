"""Fundamentally new texture CONCEPTS for the amulets - different silhouettes, not palette swaps.

Concepts:
  boiler   - vertical mini-boiler pendant: dome, rivet bands, glowing firebox, whistle
  piston   - twin-piston pump: cylinders + rods + ember window (pistons animate)
  skeleton - openwork watch movement: exposed rotating gears, balance wheel, ember core
  lantern  - hanging ember lantern: ring + chain, hex mesh cage, coal heap

Output: tools/gallery2/*.png + fragment.html (everything embedded).
"""
from PIL import Image, ImageDraw
import math
import os
import base64

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "gallery2")
os.makedirs(OUT, exist_ok=True)

PALETTES = {
    "boiler": dict(outline=(38, 28, 10), body=(150, 108, 32), hi=(198, 152, 66), lo=(96, 68, 20),
                   metal2=(120, 86, 26), glow=(235, 120, 45), glow_hi=(255, 210, 110),
                   dial=(210, 226, 236), steam=(240, 247, 252), crystal=(104, 214, 255)),
    "piston": dict(outline=(30, 26, 22), body=(96, 100, 108), hi=(140, 145, 154), lo=(56, 58, 64),
                   metal2=(184, 132, 44), glow=(240, 130, 40), glow_hi=(255, 216, 120),
                   dial=(226, 232, 238), steam=(238, 246, 250), crystal=(110, 220, 255)),
    "skeleton": dict(outline=(40, 30, 12), body=(206, 168, 78), hi=(236, 202, 110), lo=(140, 106, 40),
                     metal2=(96, 72, 26), glow=(240, 140, 48), glow_hi=(255, 220, 130),
                     dial=(214, 228, 238), steam=(240, 247, 252), crystal=(120, 226, 255)),
    "lantern": dict(outline=(30, 22, 10), body=(168, 118, 42), hi=(210, 160, 74), lo=(108, 76, 24),
                    metal2=(84, 84, 92), glow=(238, 128, 42), glow_hi=(255, 214, 110),
                    dial=(214, 228, 238), steam=(240, 247, 252), crystal=(110, 220, 255)),
}


def gear(d, cx, cy, r, teeth, fill, ang=0.0, hole=None, u=1.0):
    n = teeth * 2
    pts = []
    for i in range(n):
        a = ang + i / n * 2 * math.pi
        rr = r if i % 2 == 0 else r * 0.78
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)
    if hole:
        hr = r * 0.34
        steps = 20
        pts = [(cx + hr * math.cos(2 * math.pi * i / steps), cy + hr * math.sin(2 * math.pi * i / steps))
               for i in range(steps)]
        d.polygon(pts, fill=hole)


def disc(d, cx, cy, r, fill, steps=28):
    pts = [(cx + r * math.cos(2 * math.pi * i / steps), cy + r * math.sin(2 * math.pi * i / steps))
           for i in range(steps)]
    d.polygon(pts, fill=fill)


# ---------------- concept painters. u = one 16-grid unit = size/16 ----------------

def draw_boiler(d, S, u, p, item, state, frame=0):
    cx = S / 2
    # dome
    d.ellipse([cx - 3.2 * u, 1.2 * u, cx + 3.2 * u, 7.4 * u], fill=p["body"], outline=p["outline"])
    d.ellipse([cx - 3.2 * u, 1.2 * u, cx + 3.2 * u, 7.4 * u], outline=p["outline"])
    d.arc([cx - 3.2 * u, 1.2 * u, cx + 3.2 * u, 7.4 * u], 180, 320, fill=p["hi"])
    # body cylinder
    d.rounded_rectangle([cx - 3.6 * u, 5.6 * u, cx + 3.6 * u, 14.2 * u], radius=u * 0.8,
                        fill=p["body"], outline=p["outline"])
    # shading bands
    d.rectangle([cx - 3.6 * u, 5.6 * u, cx - 2.4 * u, 14.2 * u], fill=p["hi"])
    d.rectangle([cx + 2.6 * u, 5.6 * u, cx + 3.6 * u, 14.2 * u], fill=p["lo"])
    # rivet bands
    for yy in (7.2, 12.8):
        d.line([cx - 3.4 * u, yy * u, cx + 3.4 * u, yy * u], fill=p["metal2"])
        for xx in (-2.8, -1.4, 0, 1.4, 2.8):
            r = max(0.5, u * 0.14)
            d.ellipse([cx + xx * u - r, yy * u - r, cx + xx * u + r, yy * u + r], fill=p["outline"])
    # firebox
    fy = 9.6 * u
    if state == "dry":
        d.rounded_rectangle([cx - 2.0 * u, fy, cx + 2.0 * u, fy + 2.6 * u], radius=u * 0.5,
                            fill=(30, 26, 22), outline=p["outline"])
    else:
        flick = 1.0 + 0.12 * math.sin(frame * 1.1)
        d.rounded_rectangle([cx - 2.0 * u, fy, cx + 2.0 * u, fy + 2.6 * u], radius=u * 0.5,
                            fill=p["glow"], outline=p["outline"])
        d.ellipse([cx - 1.2 * u, fy + 0.5 * u, cx + 1.2 * u, fy + 2.1 * u],
                  fill=(*p["glow_hi"], int(255 * min(1, flick))))
    # item personality: dial (auto) / crystal (iso)
    if item == "auto":
        d.ellipse([cx - 1.5 * u, 7.6 * u, cx + 1.5 * u, 10.6 * u], fill=p["dial"], outline=p["outline"])
        a = 2.2 if state != "steam" else 0.8
        d.line([cx, 9.1 * u, cx + 1.1 * u * math.cos(a), 9.1 * u + 1.1 * u * math.sin(a)],
               fill=(190, 40, 30))
    elif item == "iso":
        disc(d, cx, 9.4 * u, 1.6 * u, p["crystal"])
        d.point((cx - 0.4 * u, 9.0 * u), fill=(255, 255, 255))
    # whistle pipe
    d.rectangle([cx + 1.6 * u, 0.6 * u, cx + 2.5 * u, 2.4 * u], fill=p["metal2"], outline=p["outline"])
    if state == "steam":
        ox, oy = cx + 2.05 * u, 0.4 * u
        for k in range(3):
            r = u * (0.35 + 0.16 * ((frame + k) % 3))
            yy = oy - k * 0.9 * u
            d.ellipse([ox - r, yy - r, ox + r, yy + r], fill=(*p["steam"], 235 - k * 40))


def draw_piston(d, S, u, p, item, state, frame=0):
    cx = S / 2
    # back plate
    d.rounded_rectangle([2.4 * u, 3.6 * u, S - 2.4 * u, S - 2.0 * u], radius=u,
                        fill=p["lo"], outline=p["outline"])
    # manifold on top
    d.rounded_rectangle([cx - 4.2 * u, 2.2 * u, cx + 4.2 * u, 4.6 * u], radius=u * 0.5,
                        fill=p["metal2"], outline=p["outline"])
    # two cylinders
    for i, x0 in enumerate((cx - 3.6 * u, cx + 1.2 * u)):
        d.rounded_rectangle([x0, 5.0 * u, x0 + 2.4 * u, 12.6 * u], radius=u * 0.4,
                            fill=p["body"], outline=p["outline"])
        d.rectangle([x0 + 0.3 * u, 5.2 * u, x0 + 0.7 * u, 12.4 * u], fill=p["hi"])
        # piston rod (animates)
        ph = (frame + i * 4) % 8 / 8.0
        rod_y = 5.4 * u + ph * 2.2 * u
        d.rectangle([x0 + 0.9 * u, rod_y, x0 + 1.5 * u, rod_y + 1.6 * u], fill=p["metal2"],
                    outline=p["outline"])
        # piston crown
        d.rectangle([x0 + 0.25 * u, rod_y + 1.5 * u, x0 + 2.15 * u, rod_y + 2.0 * u],
                    fill=p["hi"], outline=p["outline"])
    # ember window between cylinders
    wy = 8.2 * u
    if state == "dry":
        d.rounded_rectangle([cx - 0.9 * u, wy, cx + 0.9 * u, wy + 2.4 * u], radius=u * 0.3,
                            fill=(28, 24, 20), outline=p["outline"])
    else:
        d.rounded_rectangle([cx - 0.9 * u, wy, cx + 0.9 * u, wy + 2.4 * u], radius=u * 0.3,
                            fill=p["glow"], outline=p["outline"])
        d.ellipse([cx - 0.45 * u, wy + 0.6 * u, cx + 0.45 * u, wy + 1.8 * u], fill=p["glow_hi"])
    if item == "auto":
        d.ellipse([cx - 1.3 * u, 13.0 * u, cx + 1.3 * u, 15.6 * u], fill=p["dial"], outline=p["outline"])
        d.line([cx, 14.3 * u, cx + 0.8 * u * math.cos(2.4), 14.3 * u + 0.8 * u * math.sin(2.4)],
               fill=(190, 40, 30))
    elif item == "iso":
        disc(d, cx - 2.4 * u, 13.6 * u, 1.1 * u, p["crystal"])
        disc(d, cx + 2.4 * u, 13.6 * u, 1.1 * u, p["crystal"])
    # pipes into the plate
    d.rectangle([cx - 3.0 * u, 4.4 * u, cx - 2.2 * u, 5.2 * u], fill=p["metal2"], outline=p["outline"])
    d.rectangle([cx + 2.2 * u, 4.4 * u, cx + 3.0 * u, 5.2 * u], fill=p["metal2"], outline=p["outline"])
    if state == "steam":
        for k, sx in enumerate((cx - 3.6 * u, cx + 3.0 * u)):
            r = u * (0.3 + 0.15 * ((frame + k * 2) % 4))
            yy = 1.6 * u + ((frame + k) % 3) * 0.5 * u
            d.ellipse([sx - r, yy - r, sx + r, yy + r], fill=(*p["steam"], 230 - k * 30))


def draw_skeleton(d, S, u, p, item, state, frame=0):
    cx = S / 2
    # open frame: thick border only (see-through middle)
    t = 1.5 * u
    m = 1.4 * u
    d.rounded_rectangle([m, m, S - m, S - m], radius=u * 1.5, outline=p["outline"], width=max(2, int(t)))
    d.rounded_rectangle([m + t * 0.9, m + t * 0.9, S - m - t * 0.9, S - m - t * 0.9],
                        radius=u * 1.2, outline=p["metal2"], width=max(1, int(u * 0.35)))
    # corner screws
    for (sx, sy) in ((m + u, m + u), (S - m - u, m + u), (m + u, S - m - u), (S - m - u, S - m - u)):
        r = u * 0.5
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=p["body"], outline=p["outline"])
        d.point((sx - r * 0.4, sy - r * 0.4), fill=p["hi"])
    # gears (rotate with frame)
    a1 = frame * 0.5
    gear(d, cx - 1.1 * u, S / 2 + 0.6 * u, 3.1 * u, 8, p["body"], ang=a1, hole=(30, 26, 20, 255), u=u)
    gear(d, cx + 3.0 * u, S / 2 - 1.6 * u, 2.2 * u, 7, p["metal2"], ang=-a1 * 1.4 + 0.3,
         hole=(30, 26, 20, 255), u=u)
    # balance wheel
    bw = cx - 0.4 * u
    by = 4.2 * u
    d.ellipse([bw - 1.8 * u, by - 1.8 * u, bw + 1.8 * u, by + 1.8 * u], outline=p["metal2"],
              width=max(1, int(u * 0.4)))
    d.line([bw + 1.6 * u * math.cos(a1 * 2), by + 1.6 * u * math.sin(a1 * 2),
            bw - 1.6 * u * math.cos(a1 * 2), by - 1.6 * u * math.sin(a1 * 2)], fill=p["hi"])
    # center jewel: ember or crystal
    jy = S / 2 - 2.6 * u
    if item == "iso" or state == "dry":
        core = p["crystal"] if item == "iso" else (52, 46, 40)
        disc(d, cx + 0.2 * u, jy, 1.5 * u, core, steps=6)
    else:
        flick = int(200 + 55 * math.sin(frame))
        disc(d, cx + 0.2 * u, jy, 1.5 * u, (*p["glow_hi"], flick), steps=6)
        disc(d, cx + 0.2 * u, jy, 0.8 * u, (255, 246, 220, 240), steps=6)


def draw_lantern(d, S, u, p, item, state, frame=0):
    cx = S / 2
    # hanging ring + chain
    d.ellipse([cx - 1.1 * u, 0.3 * u, cx + 1.1 * u, 2.5 * u], outline=p["outline"], width=max(2, int(u * 0.5)))
    d.ellipse([cx - 0.55 * u, 2.6 * u, cx + 0.55 * u, 3.7 * u], outline=p["outline"], width=max(1, int(u * 0.35)))
    # roof
    d.polygon([(cx - 3.4 * u, 5.4 * u), (cx, 3.9 * u), (cx + 3.4 * u, 5.4 * u)],
              fill=p["body"], outline=p["outline"])
    # hexagonal cage
    top, bot = 5.4 * u, 13.8 * u
    d.polygon([(cx - 3.4 * u, top), (cx + 3.4 * u, top), (cx + 2.6 * u, bot), (cx - 2.6 * u, bot)],
              outline=p["outline"], width=max(2, int(u * 0.5)))
    d.rectangle([cx - 2.6 * u, bot, cx + 2.6 * u, bot + 0.8 * u], fill=p["metal2"], outline=p["outline"])
    # vertical bars
    for xx in (-1.7, 0, 1.7):
        d.line([cx + xx * u, top, cx + xx * 0.76 * u, bot], fill=p["outline"])
    # coals
    heap_y = bot - 1.6 * u
    if state == "dry":
        d.ellipse([cx - 2.1 * u, heap_y, cx + 2.1 * u, heap_y + 1.5 * u], fill=(40, 34, 28))
    else:
        pulse = 0.5 + 0.5 * math.sin(frame * 1.3)
        d.ellipse([cx - 2.1 * u, heap_y, cx + 2.1 * u, heap_y + 1.5 * u], fill=p["glow"])
        for k, (dx, dy) in enumerate(((-1.2, 0.2), (0, -0.2), (1.2, 0.3))):
            r = u * 0.35
            d.ellipse([cx + dx * u - r, heap_y + dy * u - r, cx + dx * u + r, heap_y + dy * u + r],
                      fill=(*p["glow_hi"], int(180 + 70 * pulse)))
    # item personality: small dial on the roof band / crystals in the mesh
    if item == "auto":
        d.ellipse([cx - 1.4 * u, 4.6 * u, cx + 1.4 * u, 6.4 * u], fill=p["dial"], outline=p["outline"])
        d.line([cx, 5.5 * u, cx + 0.7 * u * math.cos(1.8), 5.5 * u + 0.7 * u * math.sin(1.8)],
               fill=(190, 40, 30))
    elif item == "iso":
        disc(d, cx, 8.0 * u, 1.0 * u, p["crystal"], steps=6)
    if state == "steam":
        for k in range(2):
            r = u * (0.3 + 0.18 * ((frame + k) % 3))
            xx = cx + (0.8 * u if k else -0.8 * u)
            yy = 3.2 * u - ((frame + k) % 3) * 0.7 * u
            d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=(*p["steam"], 225 - k * 40))


CONCEPTS = {
    "boiler": ("Мини-котёл на подвесе", draw_boiler),
    "piston": ("Поршневое сердце", draw_piston),
    "skeleton": ("Скелетон-механизм", draw_skeleton),
    "lantern": ("Жаровня-фонарь", draw_lantern),
}

files = []
for key, (label, painter) in CONCEPTS.items():
    for item in ("charm", "auto", "iso"):
        states = ("idle", "steam", "dry") if item == "charm" else ("idle", "steam")
        if item == "iso":
            states = ("idle", "steam")
        for state in states:
            for size in (32, 64):
                img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
                d = ImageDraw.Draw(img)
                painter(d, size, size / 16.0, PALETTES[key], item, state, frame=0)
                name = f"{key}_{item}_{state}_{size}.png"
                img.save(os.path.join(OUT, name))
                files.append(name)
    # animated preview: steaming cycle
    frames = []
    for f in range(8):
        img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        painter(d, 32, 2.0, PALETTES[key], "charm", "steam", frame=f)
        frames.append(img)
    frames[0].save(os.path.join(OUT, f"{key}_anim.gif"), save_all=True,
                   append_images=frames[1:], duration=160, loop=0)
    files.append(f"{key}_anim.gif")
print("generated", len(files), "files")

# ---------------- fragment ----------------
def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()

cards = []
for key, (label, _) in CONCEPTS.items():
    c = f'<div class="stycell"><div class="styname">{label}</div><div class="row">'
    for item, lbl, sts in (("charm", "Брошка (3 состояния)", ("idle", "steam", "dry")),
                           ("auto", "Автотермостат", ("idle", "steam")),
                           ("iso", "Изоамулет", ("idle", "steam"))):
        c += f'<div class="grp"><div class="grpname">{lbl}</div><div class="imgs">'
        for st in sts:
            c += (f'<figure><img src="data:image/png;base64,{b64(os.path.join(OUT, key + "_" + item + "_" + st + "_32.png"))}" '
                  f'width="72" height="72" class="pix"><figcaption class="text-small text-muted">{st}</figcaption></figure>')
        c += '</div></div>'
    c += '</div><div class="row big">'
    c += (f'<figure><img src="data:image/png;base64,{b64(os.path.join(OUT, key + "_charm_steam_64.png"))}" width="144" height="144" class="pix">'
          f'<figcaption class="text-small text-muted">64 px, пар</figcaption></figure>'
          f'<figure><img src="data:image/gif;base64,{b64(os.path.join(OUT, key + "_anim.gif"))}" width="108" height="108" class="pix">'
          f'<figcaption class="text-small text-muted">анимация</figcaption></figure></div></div>')
    cards.append(c)

html = ('<div id="texture-concepts">' + "".join(cards) + '</div>'
        '<style>#texture-concepts{display:grid;gap:16px}'
        '#texture-concepts .stycell{border-top:1px solid var(--border);padding-top:10px}'
        '#texture-concepts .styname{font-weight:500;margin-bottom:6px}'
        '#texture-concepts .row{display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start}'
        '#texture-concepts .grpname{font-size:12px;color:var(--muted-foreground);margin-bottom:2px}'
        '#texture-concepts .imgs{display:flex;gap:10px}'
        '#texture-concepts figure{margin:0;text-align:center}'
        '#texture-concepts .pix{image-rendering:pixelated;background:var(--muted);border-radius:6px}'
        '#texture-concepts .big{align-items:center;margin-top:8px}</style>')
open(os.path.join(OUT, "fragment.html"), "w", encoding="utf-8").write(html)
print("fragment.html", len(html) // 1024, "KB")
