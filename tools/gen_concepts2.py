"""Create-flavored amulet concepts: chains + visible water flow.

  tank   - bolted steel tank with a glass window: water level, waves, bubbles
  wheel  - mini water wheel in a brass bracket: wheel spins, water pours over it
  pipes  - circular pipe ring with transparent segments: flowing water dashes + valve
  cog    - brass cogwheel pendant: water streams through the center hole

All hang on chains (top links). Output: tools/gallery3/*.png + fragment.html
"""
from PIL import Image, ImageDraw
import math
import os
import base64

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "gallery3")
os.makedirs(OUT, exist_ok=True)

P = dict(outline=(32, 26, 16), steel=(118, 122, 130), steel_hi=(160, 165, 174), steel_lo=(70, 72, 78),
         brass=(190, 140, 46), brass_hi=(226, 178, 76), brass_lo=(118, 86, 26),
         water=(52, 120, 196), water_hi=(110, 186, 240), water_lo=(30, 78, 140),
         glass=(196, 226, 244, 70), ember=(235, 120, 45), ember_hi=(255, 214, 110),
         chain=(150, 152, 160), crystal=(110, 220, 255), dial=(226, 232, 238))



def disc(d, cx, cy, r, fill, steps=16):
    pts = [(cx + r * math.cos(2 * math.pi * i / steps), cy + r * math.sin(2 * math.pi * i / steps))
           for i in range(steps)]
    d.polygon(pts, fill=fill)

def gear(d, cx, cy, r, teeth, fill, ang=0.0, hole=None):
    n = teeth * 2
    pts = []
    for i in range(n):
        a = ang + i / n * 2 * math.pi
        rr = r if i % 2 == 0 else r * 0.76
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)
    if hole:
        hr = r * 0.36
        pts = [(cx + hr * math.cos(2 * math.pi * i / 20), cy + hr * math.sin(2 * math.pi * i / 20))
               for i in range(20)]
        d.polygon(pts, fill=hole)


def chain_up(d, cx, top_y, p, u, n=2, sw=1):
    """Chain links going up from the pendant top."""
    for k in range(n):
        ly = top_y - (k + 0.5) * 1.5 * u
        d.ellipse([cx - 0.5 * u, ly, cx + 0.5 * u, ly + 1.5 * u], outline=p["chain"], width=sw)
    d.ellipse([cx - 0.75 * u, top_y - (n + 0.6) * 1.5 * u,
               cx + 0.75 * u, top_y - (n + 0.6) * 1.5 * u + 1.5 * u],
              outline=p["chain"], width=sw)


# ---------------- painters ----------------

def draw_tank(d, S, u, state, frame=0, item="charm"):
    cx = S / 2
    chain_up(d, cx, 4.4 * u, P, u, n=1)
    # bolted steel frame
    d.rounded_rectangle([3.0 * u, 4.2 * u, S - 3.0 * u, S - 1.6 * u], radius=u,
                        fill=P["steel"], outline=P["outline"])
    d.rounded_rectangle([3.0 * u, 4.2 * u, S - 3.0 * u, S - 1.6 * u], radius=u, outline=P["outline"])
    for (bx, by) in ((4.0, 5.2), (S / u - 4.0, 5.2), (4.0, S / u - 2.6), (S / u - 4.0, S / u - 2.6)):
        r = u * 0.42
        d.ellipse([bx * u - r, by * u - r, bx * u + r, by * u + r], fill=P["steel_hi"], outline=P["outline"])
    # glass window
    wx0, wy0, wx1, wy1 = 4.6 * u, 5.6 * u, S - 4.6 * u, S - 2.6 * u
    d.rectangle([wx0, wy0, wx1, wy1], fill=(196, 226, 244, 60), outline=P["outline"])
    # water body
    level = {"steam": 0.45, "idle": 0.55, "dry": 0.92}[state]  # fraction from window bottom
    wh = (wy1 - wy0) * level
    d.rectangle([wx0 + 0.15 * u, wy1 - wh, wx1 - 0.15 * u, wy1], fill=P["water"])
    d.rectangle([wx0 + 0.15 * u, wy1 - wh, wx0 + 0.75 * u, wy1], fill=P["water_lo"])
    if state != "dry":
        # wavy surface line (animates)
        steps = 10
        pts = []
        for i in range(steps + 1):
            xx = wx0 + 0.15 * u + (wx1 - wx0 - 0.3 * u) * i / steps
            yy = wy1 - wh + math.sin(i * 1.1 + frame * 1.4) * 0.22 * u
            pts.append((xx, yy))
        d.line(pts, fill=P["water_hi"], width=max(1, int(u * 0.28)))
        if state == "steam":
            for k in range(2):
                bx = wx0 + (2.2 + 2.5 * ((frame + k * 2) % 3)) * u / 2 + 1.0 * u
                by = wy1 - wh * (0.3 + 0.25 * ((frame + k) % 2))
                r = u * 0.22
                d.ellipse([bx - r, by - r, bx + r, by + r], outline=P["water_hi"], width=1)
    if item == "auto":
        d.ellipse([cx - 1.6 * u, wy0 + 0.2 * u, cx + 1.6 * u, wy0 + 3.4 * u], fill=P["dial"],
                  outline=P["outline"])
        d.line([cx, wy0 + 1.8 * u, cx + 0.9 * u * math.cos(2.1), wy0 + 1.8 * u + 0.9 * u * math.sin(2.1)],
               fill=(190, 40, 30))
    elif item == "iso":
        disc(d, cx, wy1 - wh * 0.55, 1.0 * u, P["crystal"], steps=6)
    # vent with steam
    d.rectangle([cx - 0.8 * u, 3.4 * u, cx + 0.8 * u, 4.4 * u], fill=P["steel_hi"], outline=P["outline"])
    if state == "steam":
        for k in range(2):
            r = u * (0.32 + 0.16 * ((frame + k) % 3))
            d.ellipse([cx - 0.8 * u + k * 1.0 * u - r, 2.0 * u - ((frame + k) % 3) * 0.6 * u - r,
                       cx - 0.8 * u + k * 1.0 * u + r, 2.0 * u - ((frame + k) % 3) * 0.6 * u + r],
                      fill=(240, 247, 252, 230 - k * 40))


def draw_wheel(d, S, u, state, frame=0, item="charm"):
    cx = S / 2
    chain_up(d, cx, 3.0 * u, P, u, n=1)
    # brass bracket (A frame)
    d.polygon([(cx - 4.6 * u, S - 1.8 * u), (cx - 1.0 * u, 3.6 * u), (cx - 0.2 * u, 4.2 * u),
               (cx - 3.0 * u, S - 1.8 * u)], fill=P["brass"], outline=P["outline"])
    d.polygon([(cx + 4.6 * u, S - 1.8 * u), (cx + 1.0 * u, 3.6 * u), (cx + 0.2 * u, 4.2 * u),
               (cx + 3.0 * u, S - 1.8 * u)], fill=P["brass"], outline=P["outline"])
    # axle
    d.ellipse([cx - 0.7 * u, 4.4 * u - 0.7 * u, cx + 0.7 * u, 4.4 * u + 0.7 * u],
              fill=P["steel_hi"], outline=P["outline"])
    # water wheel: rim + spokes + flat paddles on the rim
    ang = 0.0 if state != "steam" else frame * 0.55
    R = 4.4 * u
    axle_y = 4.6 * u
    d.ellipse([cx - R, axle_y - R, cx + R, axle_y + R], outline=P["brass_lo"],
              width=max(2, int(u * 0.6)))
    for k in range(6):
        a = ang + k / 6 * 2 * math.pi
        d.line([cx, axle_y, cx + (R - u * 0.3) * math.cos(a), axle_y + (R - u * 0.3) * math.sin(a)],
               fill=P["brass"], width=max(1, int(u * 0.4)))
        # flat paddle at the rim, tangent to the wheel
        px, py = cx + R * math.cos(a), axle_y + R * math.sin(a)
        pa = a + math.pi / 2
        d.line([px - 0.6 * u * math.cos(pa), py - 0.6 * u * math.sin(pa),
                px + 0.6 * u * math.cos(pa), py + 0.6 * u * math.sin(pa)],
               fill=P["brass_hi"], width=max(2, int(u * 0.55)))
    d.ellipse([cx - 0.9 * u, axle_y - 0.9 * u, cx + 0.9 * u, axle_y + 0.9 * u],
              fill=P["brass_hi"], outline=P["outline"])
    # water channel below with flow dashes
    ch_y = S - 3.0 * u
    d.rectangle([2.2 * u, ch_y, S - 2.2 * u, ch_y + 1.4 * u], fill=P["water_lo"], outline=P["outline"])
    if state != "dry":
        d.rectangle([2.2 * u, ch_y + 0.25 * u, S - 2.2 * u, ch_y + 1.15 * u], fill=P["water"])
        n = 6
        for k in range(n):
            ph = ((frame * 1.0 + k) % n) / n
            xx = 2.2 * u + (S - 4.4 * u) * ph
            d.line([xx, ch_y + 0.5 * u, xx + 0.5 * u, ch_y + 0.5 * u], fill=P["water_hi"],
                   width=max(1, int(u * 0.22)))
        if state == "steam":
            # drops from the paddles
            for k in range(2):
                dx = cx + (2.2 * u if k else -2.2 * u) * math.sin(frame + k)
                dy = 4.4 * u + R + ((frame * 2 + k) % 4) * 0.9 * u
                r = u * 0.2
                d.ellipse([dx - r, dy - r, dx + r, dy + r], fill=P["water_hi"])
    if item == "auto":
        d.ellipse([cx - 1.3 * u, 6.2 * u, cx + 1.3 * u, 8.8 * u], fill=P["dial"], outline=P["outline"])
        d.line([cx, 7.5 * u, cx + 0.7 * u * math.cos(2.3), 7.5 * u + 0.7 * u * math.sin(2.3)],
               fill=(190, 40, 30))
    elif item == "iso":
        disc(d, cx + 3.1 * u, 7.0 * u, 0.9 * u, P["crystal"], steps=6)
    if state == "steam":
        r = u * (0.3 + 0.15 * (frame % 3))
        d.ellipse([cx - 0.4 * u, 1.4 * u - (frame % 3) * 0.5 * u - r, cx + 0.4 * u,
                   1.4 * u - (frame % 3) * 0.5 * u + r], fill=(240, 247, 252, 225))


def draw_pipes(d, S, u, state, frame=0, item="charm"):
    cx = cy = S / 2
    chain_up(d, cx, 3.4 * u, P, u, n=1)
    R = 4.7 * u
    wt = 1.5 * u
    # pipe ring (brass torus)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=P["brass"], width=max(3, int(wt)))
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=P["outline"], width=1)
    # inner window: water surface
    r_in = R - wt
    d.ellipse([cx - r_in, cy - r_in, cx + r_in, cy + r_in], fill=(196, 226, 244, 50))
    if state != "dry":
        # lower half filled with water
        d.pieslice([cx - r_in, cy - r_in, cx + r_in, cy + r_in], 0, 180, fill=P["water"])
        # flowing dashes around the ring (three transparent segments)
        for seg in range(3):
            base = seg * (2 * math.pi / 3) + 0.35
            for k in range(3):
                a = base + ((frame * 0.35 + k * 0.22) % (2 * math.pi / 3 - 0.5))
                rr = R
                d.ellipse([cx + rr * math.cos(a) - 0.3 * u, cy + rr * math.sin(a) - 0.3 * u,
                           cx + rr * math.cos(a) + 0.3 * u, cy + rr * math.sin(a) + 0.3 * u],
                          fill=P["water_hi"])
    # flange bolts at 4 diagonals
    for a in (0.785, 2.36, 3.93, 5.5):
        bx, by = cx + R * math.cos(a), cy + R * math.sin(a)
        r = u * 0.45
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=P["steel_hi"], outline=P["outline"])
        d.point((bx - r * 0.4, by - r * 0.4), fill=P["outline"])
    # center valve handwheel (rotates)
    va = 0.0 if state != "steam" else frame * 0.8
    gear(d, cx, cy, 2.1 * u, 4, P["brass_hi"], ang=va, hole=(52, 120, 196, 255))
    d.ellipse([cx - 0.4 * u, cy - 0.4 * u, cx + 0.4 * u, cy + 0.4 * u], fill=P["brass_lo"],
              outline=P["outline"])
    if item == "auto":
        d.ellipse([cx + 2.2 * u, cy + 2.2 * u, cx + 4.2 * u, cy + 4.2 * u], fill=P["dial"],
                  outline=P["outline"])
        d.line([cx + 3.2 * u, cy + 3.2 * u, cx + 3.2 * u + 0.7 * u * math.cos(2.0),
                cy + 3.2 * u + 0.7 * u * math.sin(2.0)], fill=(190, 40, 30))
    elif item == "iso":
        for a in (0.785, 3.93):
            disc(d, cx + R * math.cos(a) * 0.5, cy + R * math.sin(a) * 0.5, 0.8 * u, P["crystal"], steps=6)
    if state == "steam":
        r = u * (0.3 + 0.16 * (frame % 3))
        d.ellipse([cx - 0.3 * u, 1.2 * u - (frame % 3) * 0.6 * u - r, cx + 0.3 * u,
                   1.2 * u - (frame % 3) * 0.6 * u + r], fill=(240, 247, 252, 228))


def draw_cog(d, S, u, state, frame=0, item="charm"):
    cx = S / 2
    chain_up(d, cx, 3.2 * u, P, u, n=1)
    # big brass cog
    ang = 0.0 if state != "steam" else frame * 0.4
    gear(d, cx, 9.0 * u, 5.4 * u, 8, P["brass"], ang=ang, hole=(30, 26, 18, 255))
    # hub
    d.ellipse([cx - 1.2 * u, 9.0 * u - 1.2 * u, cx + 1.2 * u, 9.0 * u + 1.2 * u],
              fill=P["brass_hi"], outline=P["outline"])
    # water stream through the center hole
    if state != "dry":
        d.rectangle([cx - 0.55 * u, 3.2 * u, cx + 0.55 * u, 14.6 * u], fill=(*P["water"], 210))
        for k in range(4):
            yy = 3.6 * u + ((frame * 1.6 + k * 2.6) % 11) * u
            d.line([cx - 0.25 * u, yy, cx - 0.25 * u, yy + 1.0 * u], fill=P["water_hi"],
                   width=max(1, int(u * 0.2)))
        # splash basin at the bottom
        d.rounded_rectangle([cx - 3.2 * u, 13.8 * u, cx + 3.2 * u, 15.6 * u], radius=u * 0.4,
                            fill=P["water"], outline=P["outline"])
        if state == "steam":
            for k in range(2):
                r = u * (0.24 + 0.12 * ((frame + k * 2) % 3))
                dx = cx + (1.6 * u if k else -1.6 * u)
                dy = 13.4 * u - ((frame + k) % 3) * 0.5 * u
                d.ellipse([dx - r, dy - r, dx + r, dy + r], fill=P["water_hi"])
    else:
        d.ellipse([cx, 14.0 * u, cx + 0.1 * u, 14.1 * u], fill=(0, 0, 0, 0))
    if item == "auto":
        d.ellipse([cx - 2.8 * u, 8.2 * u, cx - 0.8 * u, 10.2 * u], fill=P["dial"], outline=P["outline"])
        d.line([cx - 1.8 * u, 9.2 * u, cx - 1.8 * u + 0.6 * u * math.cos(2.2),
                9.2 * u + 0.6 * u * math.sin(2.2)], fill=(190, 40, 30))
    elif item == "iso":
        disc(d, cx + 1.8 * u, 9.0 * u, 1.0 * u, P["crystal"], steps=6)
    if state == "steam":
        for k in range(2):
            r = u * (0.28 + 0.14 * ((frame + k) % 3))
            d.ellipse([cx + (0.9 * u if k else -0.9 * u) - r, 2.4 * u - (frame % 3) * 0.5 * u - r,
                       cx + (0.9 * u if k else -0.9 * u) + r, 2.4 * u - (frame % 3) * 0.5 * u + r],
                      fill=(240, 247, 252, 225))


CONCEPTS = {
    "tank": ("Цистерна Create", draw_tank),
    "wheel": ("Водяное колесо", draw_wheel),
    "pipes": ("Трубное кольцо", draw_pipes),
    "cog": ("Шестерня с потопом", draw_cog),
}

files = []
for key, (label, painter) in CONCEPTS.items():
    for item in ("charm", "auto", "iso"):
        states = ("idle", "steam", "dry") if item == "charm" else ("idle", "steam")
        for state in states:
            for size in (32, 64):
                img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
                d = ImageDraw.Draw(img)
                painter(d, size, size / 16.0, state, frame=0, item=item)
                name = f"{key}_{item}_{state}_{size}.png"
                img.save(os.path.join(OUT, name))
                files.append(name)
    frames = []
    for f in range(8):
        img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        painter(d, 32, 2.0, "steam", frame=f, item="charm")
        frames.append(img)
    frames[0].save(os.path.join(OUT, f"{key}_anim.gif"), save_all=True,
                   append_images=frames[1:], duration=160, loop=0)
    files.append(f"{key}_anim.gif")
print("generated", len(files), "files")


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

html = ('<div id="texture-concepts2">' + "".join(cards) + '</div>'
        '<style>#texture-concepts2{display:grid;gap:16px}'
        '#texture-concepts2 .stycell{border-top:1px solid var(--border);padding-top:10px}'
        '#texture-concepts2 .styname{font-weight:500;margin-bottom:6px}'
        '#texture-concepts2 .row{display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start}'
        '#texture-concepts2 .grpname{font-size:12px;color:var(--muted-foreground);margin-bottom:2px}'
        '#texture-concepts2 .imgs{display:flex;gap:10px}'
        '#texture-concepts2 figure{margin:0;text-align:center}'
        '#texture-concepts2 .pix{image-rendering:pixelated;background:var(--muted);border-radius:6px}'
        '#texture-concepts2 .big{align-items:center;margin-top:8px}</style>')
open(os.path.join(OUT, "fragment.html"), "w", encoding="utf-8").write(html)
print("fragment.html", len(html) // 1024, "KB")
