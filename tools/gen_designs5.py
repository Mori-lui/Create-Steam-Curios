"""Supporting items in the approved visual language: brass medallion (blank on chain),
thermostat core (spiral heart in a drum), incomplete brooch (half-assembled pipe ring). 64px."""
from PIL import Image, ImageDraw
import math
import os
import base64

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "gallery8")
os.makedirs(OUT, exist_ok=True)

P = dict(outline=(32, 26, 16), steel=(118, 122, 130), steel_hi=(162, 167, 176), steel_lo=(70, 72, 78),
         brass=(190, 140, 46), brass_hi=(228, 180, 78), brass_lo=(116, 84, 26), copper=(196, 108, 56),
         copper_hi=(232, 150, 84), water=(52, 120, 196), water_hi=(116, 190, 242),
         ember=(235, 120, 45), ember_hi=(255, 216, 110), chain=(158, 160, 168),
         glass=(198, 228, 246, 55))


def disc(d, cx, cy, r, fill, steps=22):
    pts = [(cx + r * math.cos(2 * math.pi * i / steps), cy + r * math.sin(2 * math.pi * i / steps))
           for i in range(steps)]
    d.polygon(pts, fill=fill)


def ring(d, cx, cy, r, fill, width):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fill, width=width)


def chain(d, cx, top_y, u, links=3):
    w = max(1, int(u * 0.36))
    for k in range(links):
        ly = top_y - (k + 0.55) * 1.6 * u
        w1 = 0.55 * u
        d.ellipse([cx - w1, ly, cx + w1, ly + 1.55 * u], outline=P["chain"], width=w)
    r = 0.8 * u
    d.ellipse([cx - r, top_y - r * 0.6, cx + r, top_y + r * 1.4], outline=P["chain"], width=w)


# ---------------- brass medallion: the blank ----------------
def draw_medallion(d, S, u, frame=0):
    cx, cy = S / 2, 8.0 * u
    chain(d, cx, 2.6 * u, u, links=2)
    R = 7.0 * u
    disc(d, cx, cy, R, P["outline"])
    disc(d, cx, cy, R - 0.4 * u, P["brass"])
    # lathe rings
    ring(d, cx, cy, R - 1.6 * u, P["brass_lo"], max(1, int(u * 0.22)))
    ring(d, cx, cy, R - 2.6 * u, P["brass_hi"], max(1, int(u * 0.22)))
    # embossed cog emblem in the center (blank stamp)
    n = 8
    pts = []
    for i in range(n * 2):
        a = i / (n * 2) * 2 * math.pi + 0.2
        rr = (2.4 if i % 2 == 0 else 1.75) * u
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=P["brass_lo"])
    d.ellipse([cx - 0.75 * u, cy - 0.75 * u, cx + 0.75 * u, cy + 0.75 * u], fill=P["brass_hi"],
              outline=P["outline"])
    # highlight crescent + 4 rivets
    d.arc([cx - R + 0.8 * u, cy - R + 0.8 * u, cx + R - 0.8 * u, cy + R - 0.8 * u], 200, 250,
          fill=(255, 240, 200, 130), width=max(1, int(u * 0.25)))
    for a in (0.785, 2.36, 3.93, 5.5):
        bx, by = cx + (R - 1.2 * u) * math.cos(a), cy + (R - 1.2 * u) * math.sin(a)
        r = u * 0.3
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=P["brass_lo"], outline=P["outline"])


# ---------------- thermostat core: spiral heart in a drum ----------------
def draw_core(d, S, u, frame=0):
    cx, cy = S / 2, 8.0 * u
    # side terminals
    for dx in (-5.8, 5.8):
        d.rounded_rectangle([cx + dx * u - 0.7 * u, cy - 1.1 * u, cx + dx * u + 0.7 * u, cy + 1.1 * u],
                            radius=u * 0.2, fill=P["brass_lo"], outline=P["outline"])
    # drum body
    R = 6.2 * u
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=P["brass"], outline=P["outline"])
    d.ellipse([cx - R + 0.5 * u, cy - R + 0.5 * u, cx + R - 0.5 * u, cy + R - 0.5 * u],
              fill=P["brass_lo"], outline=P["outline"])
    # glass window with a mini spiral + ember
    wr = R - 1.5 * u
    d.ellipse([cx - wr, cy - wr, cx + wr, cy + wr], fill=P["glass"], outline=P["outline"])
    steps = 40
    pts = []
    for i in range(steps + 1):
        t = i / steps
        theta = 0.3 + t * 1.8 * 2 * math.pi
        rr = (0.3 + (wr - 0.7 * u) * t)
        pts.append((cx + rr * math.cos(theta), cy + rr * math.sin(theta)))
    d.line(pts, fill=P["copper"], width=max(1, int(u * 0.3)))
    fl = int(190 + 50 * math.sin(frame))
    disc(d, cx, cy, 0.65 * u, (*P["ember_hi"], fl), steps=10)
    # bolts around the drum
    for a in (0.785, 2.36, 3.93, 5.5):
        bx, by = cx + (R - 0.9 * u) * math.cos(a), cy + (R - 0.9 * u) * math.sin(a)
        r = u * 0.3
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=P["steel_hi"], outline=P["outline"])
    # glow when animated
    if frame > 0:
        d.ellipse([cx - wr - 0.3 * u, cy - wr - 0.3 * u, cx + wr + 0.3 * u, cy + wr + 0.3 * u],
                  outline=(*P["ember_hi"], 90), width=max(1, int(u * 0.2)))


# ---------------- incomplete brooch: half-assembled pipe ring ----------------
def draw_incomplete(d, S, u, frame=0):
    cx = S / 2
    chain(d, cx, 1.7 * u, u, links=2)
    R = 6.9 * u
    wt = 1.8 * u
    # pipe ring, but dim / unpolished
    d.ellipse([cx - R, S / 2 - R, cx + R, S / 2 + R], outline=P["outline"], width=max(4, int(wt + 1.2 * u)))
    d.ellipse([cx - R, S / 2 - R, cx + R, S / 2 + R], outline=(150, 116, 40), width=max(3, int(wt)))
    r_in = R - wt
    d.ellipse([cx - r_in, S / 2 - r_in, cx + r_in, S / 2 + r_in], fill=(28, 24, 20, 160))
    # only two bolts installed, two holes empty
    for (a, installed) in ((0.785, True), (2.36, False), (3.93, True), (5.5, False)):
        bx, by = cx + R * math.cos(a), S / 2 + R * math.sin(a)
        if installed:
            r = u * 0.5
            d.ellipse([bx - r, by - r, bx + r, by + r], fill=P["steel_hi"], outline=P["outline"])
        else:
            r = u * 0.42
            d.ellipse([bx - r, by - r, bx + r, by + r], fill=(22, 18, 14), outline=P["outline"])
    # valve socket: empty center mount with screw holes, no valve
    d.rounded_rectangle([cx - 1.9 * u, S / 2 - 1.9 * u, cx + 1.9 * u, S / 2 + 1.9 * u],
                        radius=u * 0.3, fill=(48, 40, 30), outline=P["outline"])
    for (sx, sy) in ((-1.3, -1.3), (1.3, -1.3), (-1.3, 1.3), (1.3, 1.3)):
        r = u * 0.16
        d.ellipse([cx + sx * u - r, S / 2 + sy * u - r, cx + sx * u + r, S / 2 + sy * u + r],
                  fill=(20, 16, 12))
    # a loose bolt lying on the ring edge
    d.ellipse([cx + 2.9 * u, S / 2 - 6.0 * u, cx + 4.0 * u, S / 2 - 4.9 * u],
              fill=P["steel_hi"], outline=P["outline"])


ITEMS = {
    "brass_medallion": ("Латунный медальон (заготовка)", draw_medallion),
    "thermostat_core": ("Термостатический сердечник", draw_core),
    "incomplete_heater_charm": ("Незаконченная брошка", draw_incomplete),
}

files = []
for key, (label, painter) in ITEMS.items():
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    painter(d, 64, 4.0, frame=0)
    img.save(os.path.join(OUT, f"{key}_64.png"))
    files.append(f"{key}_64.png")
print("generated", len(files), "files")


def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()


cards = ['<div id="texture-designs5"><div class="stycell">'
         '<div class="styname">Крафтовые предметы в общем стиле (64 px)</div><div class="row">']
for key, (label, _) in ITEMS.items():
    cards.append(f'<div class="grp"><div class="grpname">{label}</div>'
                 f'<figure><img src="data:image/png;base64,{b64(os.path.join(OUT, key + "_64.png"))}" width="160" height="160" class="pix"></figure></div>')
cards.append('</div></div></div>'
             '<style>#texture-designs5{display:grid;gap:16px}'
             '#texture-designs5 .stycell{border-top:1px solid var(--border);padding-top:10px}'
             '#texture-designs5 .styname{font-weight:500;margin-bottom:6px}'
             '#texture-designs5 .row{display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start}'
             '#texture-designs5 .grpname{font-size:12px;color:var(--muted-foreground);margin-bottom:2px}'
             '#texture-designs5 figure{margin:0;text-align:center}'
             '#texture-designs5 .pix{image-rendering:pixelated;background:var(--muted);border-radius:6px}</style>')
open(os.path.join(OUT, "fragment.html"), "w", encoding="utf-8").write(html := "".join(cards))
print("fragment.html", len(html) // 1024, "KB")
