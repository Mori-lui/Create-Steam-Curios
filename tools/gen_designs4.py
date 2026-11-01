"""Round 4: three clean, single-shape variants for the auto_thermostat. 64px only.

  radiator - mini ribbed heating radiator: headers, valve, water window, heat shimmer
  retort   - round flask with sloshing liquid on a burner cradle, vent pipe
  spiral   - open case with a winding bimetal spiral + ember core (classic thermostat)

Output: tools/gallery7/*.png + fragment.html
"""
from PIL import Image, ImageDraw
import math
import os
import base64

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "gallery7")
os.makedirs(OUT, exist_ok=True)

P = dict(outline=(32, 26, 16), steel=(118, 122, 130), steel_hi=(162, 167, 176), steel_lo=(70, 72, 78),
         brass=(190, 140, 46), brass_hi=(228, 180, 78), brass_lo=(116, 84, 26), copper=(196, 108, 56),
         copper_hi=(232, 150, 84), water=(52, 120, 196), water_hi=(116, 190, 242), water_lo=(30, 78, 140),
         ember=(235, 120, 45), ember_hi=(255, 216, 110), chain=(158, 160, 168),
         glass=(198, 228, 246, 55))


def chain(d, cx, top_y, u, links=2):
    w = max(1, int(u * 0.36))
    for k in range(links):
        ly = top_y - (k + 0.55) * 1.6 * u
        w1 = 0.55 * u
        d.ellipse([cx - w1, ly, cx + w1, ly + 1.55 * u], outline=P["chain"], width=w)
    r = 0.8 * u
    d.ellipse([cx - r, top_y - r * 0.6, cx + r, top_y + r * 1.4], outline=P["chain"], width=w)


def rib_body(d, x, y0, y1, w, body, hi, outline):
    d.rounded_rectangle([x, y0, x + w, y1], radius=w * 0.4, fill=body, outline=outline)
    d.rectangle([x + w * 0.18, y0 + w * 0.3, x + w * 0.42, y1 - w * 0.3], fill=hi)


# ---------------- 1. radiator ----------------
def draw_radiator(d, S, u, state, frame=0):
    cx = S / 2
    chain(d, cx, 2.6 * u, u)
    # top header with valve
    d.rounded_rectangle([2.8 * u, 3.4 * u, S - 2.8 * u, 4.8 * u], radius=u * 0.3,
                        fill=P["brass"], outline=P["outline"])
    # valve wheel on the right of the header
    va = 0.0 if state != "steam" else frame * 0.8
    vx, vy = S - 3.6 * u, 2.9 * u
    d.ellipse([vx - 1.0 * u, vy - 1.0 * u, vx + 1.0 * u, vy + 1.0 * u], outline=P["brass_hi"],
              width=max(2, int(u * 0.4)))
    d.line([vx, vy, vx + 0.8 * u * math.cos(va), vy + 0.8 * u * math.sin(va)], fill=P["brass_hi"])
    d.ellipse([vx - 0.3 * u, vy - 0.3 * u, vx + 0.3 * u, vy + 0.3 * u], fill=P["brass_lo"],
              outline=P["outline"])
    # ribs (4 sections), middle one has the water window
    ry0, ry1 = 4.8 * u, 13.4 * u
    w = 1.9 * u
    xs = [3.0 * u, 5.05 * u, 7.1 * u, 9.15 * u]
    for i, x in enumerate(xs):
        if i == 1 and state != "dry":
            d.rounded_rectangle([x, ry0, x + w, ry1], radius=w * 0.4, fill=P["glass"],
                                outline=P["outline"])
            lvl = 0.3 if state == "steam" else 0.5
            top = ry0 + (ry1 - ry0) * lvl
            d.rectangle([x + 0.15 * u, top, x + w - 0.15 * u, ry1 - 0.15 * u], fill=P["water"])
            if state == "steam":
                for k in range(2):
                    by = ry1 - 1.0 * u - ((frame * 0.9 + k * 2.0) % 4) * 0.55 * u
                    d.ellipse([x + w / 2 - 0.16 * u, by - 0.16 * u, x + w / 2 + 0.16 * u, by + 0.16 * u],
                              outline=P["water_hi"], width=1)
        elif i == 1:
            d.rounded_rectangle([x, ry0, x + w, ry1], radius=w * 0.4, fill=(40, 42, 46),
                                outline=P["outline"])
        else:
            hot = state == "steam"
            body = P["ember"] if (hot and i == 2) else P["steel"]
            hi = P["ember_hi"] if (hot and i == 2) else P["steel_hi"]
            rib_body(d, x, ry0, ry1, w, body, hi, P["outline"])
    # bottom header
    d.rounded_rectangle([2.8 * u, 13.4 * u, S - 2.8 * u, 14.8 * u], radius=u * 0.3,
                        fill=P["brass"], outline=P["outline"])
    if state == "steam":
        # heat shimmer above
        for k in range(3):
            xx = 4.2 * u + k * 2.6 * u
            yy = 2.2 * u - (frame % 3) * 0.45 * u
            d.arc([xx - 0.8 * u, yy - 0.5 * u, xx + 0.8 * u, yy + 0.5 * u], 200, 340,
                  fill=(240, 247, 252, 190))


# ---------------- 2. retort on a burner ----------------
def draw_retort(d, S, u, state, frame=0):
    cx = 7.6 * u
    chain(d, cx, 2.4 * u, u)
    # stopper + vent pipe going up-right
    d.rectangle([cx - 0.9 * u, 3.2 * u, cx + 0.9 * u, 4.6 * u], fill=p_brass(), outline=P["outline"])
    d.line([cx + 0.9 * u, 3.7 * u, cx + 3.0 * u, 2.6 * u], fill=P["brass"], width=max(2, int(u * 0.55)))
    # round flask
    fy = 9.0 * u
    R = 4.3 * u
    d.ellipse([cx - R, fy - R, cx + R, fy + R], fill=P["glass"], outline=P["outline"])
    if state != "dry":
        lvl = 0.35 if state == "steam" else 0.55
        # liquid fills the bottom of the circle
        h = 2 * R * lvl
        ly0 = fy + R - h
        d.chord([cx - R + 0.2 * u, fy - R + 0.2 * u, cx + R - 0.2 * u, fy + R - 0.2 * u],
                start=90 - 0, end=0, fill=(0, 0, 0, 0))
        # simpler: clip a rectangle by drawing the flask shape again
        d.ellipse([cx - R + 0.2 * u, ly0, cx + R - 0.2 * u, fy + R - 0.2 * u], fill=P["water"])
        d.ellipse([cx - R + 0.2 * u, ly0, cx + R - 0.2 * u, fy + R - 0.2 * u], outline=P["water_lo"])
        if state == "steam":
            for k in range(3):
                bx = cx + (k - 1) * 1.3 * u
                by = fy + R - 0.8 * u - ((frame * 0.8 + k * 1.7) % 3) * 0.7 * u
                r = u * 0.22
                d.ellipse([bx - r, by - r, bx + r, by + r], outline=P["water_hi"], width=1)
    # glass shine
    d.arc([cx - R + 0.7 * u, fy - R + 0.7 * u, cx + R - 0.7 * u, fy + R - 0.7 * u], 210, 260,
          fill=(255, 255, 255, 150), width=max(1, int(u * 0.25)))
    # cradle ring + legs
    d.ellipse([cx - R, fy + 0.9 * u, cx + R, fy + 2.4 * u], outline=P["brass"], width=max(2, int(u * 0.5)))
    d.line([cx - R * 0.85, fy + 2.1 * u, cx - R * 0.55, 14.6 * u], fill=P["brass_lo"],
           width=max(2, int(u * 0.45)))
    d.line([cx + R * 0.85, fy + 2.1 * u, cx + R * 0.55, 14.6 * u], fill=P["brass_lo"],
           width=max(2, int(u * 0.45)))
    # burner under the flask
    d.rounded_rectangle([cx - 2.0 * u, 14.4 * u, cx + 2.0 * u, 15.6 * u], radius=u * 0.3,
                        fill=P["steel"], outline=P["outline"])
    if state != "dry":
        fl = int(170 + 60 * math.sin(frame * 1.4))
        for k, dx in enumerate((-0.8, 0.0, 0.8)):
            fh = (1.6 if k == 1 else 1.0) * u
            d.ellipse([cx + dx * u - 0.35 * u, 14.3 * u - fh, cx + dx * u + 0.35 * u, 14.3 * u],
                      fill=(*P["ember"], fl))
            d.ellipse([cx + dx * u - 0.16 * u, 14.3 * u - fh * 0.55, cx + dx * u + 0.16 * u, 14.3 * u],
                      fill=(*P["ember_hi"], min(255, fl + 50)))
    if state == "steam":
        r = u * (0.3 + 0.16 * (frame % 3))
        d.ellipse([cx + 2.7 * u - r, 1.9 * u - (frame % 3) * 0.5 * u - r, cx + 2.7 * u + r,
                   1.9 * u - (frame % 3) * 0.5 * u + r], fill=(240, 247, 252, 228))


def p_brass():
    return P["brass"]


# ---------------- 3. bimetal spiral thermostat ----------------
def draw_spiral(d, S, u, state, frame=0):
    cx = S / 2
    cy = 8.8 * u
    chain(d, cx, 2.6 * u, u)
    # open double-ring case
    R = 5.6 * u
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=P["brass_lo"], width=max(3, int(u * 0.5)))
    d.ellipse([cx - R + 0.8 * u, cy - R + 0.8 * u, cx + R - 0.8 * u, cy + R - 0.8 * u],
              outline=P["brass"], width=max(2, int(u * 0.35)))
    # bimetal spiral winding from center
    hot = state == "steam"
    rot = (frame * 0.12) if hot else 0.0
    col = p_copper_hot() if hot else (P["copper"] if state != "dry" else (96, 84, 72))
    steps = 60
    pts = []
    for i in range(steps + 1):
        t = i / steps
        theta = rot + t * 2.4 * 2 * math.pi
        rr = (0.5 + 3.9 * t) * u
        pts.append((cx + rr * math.cos(theta), cy + rr * math.sin(theta)))
    d.line(pts, fill=col, width=max(2, int(u * 0.42)))
    # center ember core
    if state != "dry":
        fl = int(180 + 60 * math.sin(frame))
        disc(d, cx, cy, 0.9 * u, (*P["ember_hi"], fl), steps=10)
        d.point((cx - 0.25 * u, cy - 0.25 * u), fill=(255, 255, 255))
    else:
        disc(d, cx, cy, 0.9 * u, (52, 46, 40), steps=10)
    # outer end connects to a small water drop valve at the bottom-right
    d.ellipse([cx + 3.3 * u, cy + 3.3 * u, cx + 4.9 * u, cy + 4.9 * u], fill=p_water_drop(state),
              outline=P["outline"])
    if state == "steam":
        r = u * (0.28 + 0.15 * (frame % 3))
        d.ellipse([cx - 0.4 * u, 2.0 * u - (frame % 3) * 0.5 * u - r, cx + 0.4 * u,
                   2.0 * u - (frame % 3) * 0.5 * u + r], fill=(240, 247, 252, 226))


def p_copper_hot():
    return P["ember"]


def p_water_drop(state):
    return P["water"] if state == "steam" else (P["glass"] if state == "idle" else (46, 40, 36))


def disc(d, cx, cy, r, fill, steps=14):
    pts = [(cx + r * math.cos(2 * math.pi * i / steps), cy + r * math.sin(2 * math.pi * i / steps))
           for i in range(steps)]
    d.polygon(pts, fill=fill)


VARIANTS = {
    "radiator": ("Радиатор", draw_radiator),
    "retort": ("Реторта на горелке", draw_retort),
    "spiral": ("Биметаллический термостат", draw_spiral),
}

files = []
for key, (label, painter) in VARIANTS.items():
    for state in ("idle", "steam", "dry"):
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        painter(d, 64, 4.0, state, frame=0)
        img.save(os.path.join(OUT, f"{key}_{state}_64.png"))
        files.append(f"{key}_{state}_64.png")
    frames = []
    for f in range(10):
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        painter(d, 64, 4.0, "steam", frame=f)
        frames.append(img)
    frames[0].save(os.path.join(OUT, f"{key}_anim.gif"), save_all=True,
                   append_images=frames[1:], duration=150, loop=0)
    files.append(f"{key}_anim.gif")
print("generated", len(files), "files")


def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()


cards = ['<div id="texture-designs4"><div class="stycell">'
         '<div class="styname">Автотермостат — три новых варианта (64 px)</div>']
for key, (label, _) in VARIANTS.items():
    c = f'<div class="grp"><div class="grpname">{label}</div><div class="imgs">'
    for st, stl in (("idle", "покой"), ("steam", "работа"), ("dry", "сухой")):
        c += f'<figure><img src="data:image/png;base64,{b64(os.path.join(OUT, key + "_" + st + "_64.png"))}" width="140" height="140" class="pix"><figcaption class="text-small text-muted">{stl}</figcaption></figure>'
    c += f'<figure><img src="data:image/gif;base64,{b64(os.path.join(OUT, key + "_anim.gif"))}" width="140" height="140" class="pix"><figcaption class="text-small text-muted">анимация</figcaption></figure></div>'
    cards.append(c)
cards.append('</div></div>'
             '<style>#texture-designs4{display:grid;gap:16px}'
             '#texture-designs4 .stycell{border-top:1px solid var(--border);padding-top:10px}'
             '#texture-designs4 .styname{font-weight:500;margin-bottom:6px}'
             '#texture-designs4 .grp{margin-bottom:10px}'
             '#texture-designs4 .grpname{font-size:12px;color:var(--muted-foreground);margin-bottom:2px}'
             '#texture-designs4 .imgs{display:flex;gap:12px;align-items:flex-end;flex-wrap:wrap}'
             '#texture-designs4 figure{margin:0;text-align:center}'
             '#texture-designs4 .pix{image-rendering:pixelated;background:var(--muted);border-radius:6px}</style>')
open(os.path.join(OUT, "fragment.html"), "w", encoding="utf-8").write(html := "".join(cards))
print("fragment.html", len(html) // 1024, "KB")
