"""Rebuild steamcurios_animated: animated 64px strips for the new designs.

Animated (10 frames): steam states of all three amulets + the isothermal idle pulse.
The idle/dry base textures stay static in the main mod.
"""
from PIL import Image, ImageDraw
import math
import os
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "..", "addon", "src", "assets", "steamcurios", "textures", "item")
os.makedirs(OUT, exist_ok=True)

P = dict(outline=(32, 26, 16), steel=(118, 122, 130), steel_hi=(162, 167, 176), steel_lo=(70, 72, 78),
         brass=(190, 140, 46), brass_hi=(228, 180, 78), brass_lo=(116, 84, 26), copper=(196, 108, 56),
         copper_hi=(232, 150, 84), water=(52, 120, 196), water_hi=(116, 190, 242), water_lo=(30, 78, 140),
         ember=(235, 120, 45), ember_hi=(255, 216, 110), chain=(158, 160, 168),
         glass=(198, 228, 246, 55), crystal=(110, 220, 255), crystal_hi=(200, 244, 255),
         dial=(228, 233, 239))


def disc(d, cx, cy, r, fill, steps=20):
    pts = [(cx + r * math.cos(2 * math.pi * i / steps), cy + r * math.sin(2 * math.pi * i / steps))
           for i in range(steps)]
    d.polygon(pts, fill=fill)


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


def chain(d, cx, top_y, u, links=3, fine=False):
    w = max(1, int(u * (0.26 if fine else 0.36)))
    for k in range(links):
        ly = top_y - (k + 0.55) * 1.6 * u
        w1 = 0.55 * (0.7 if fine else 1.0) * u
        d.ellipse([cx - w1, ly, cx + w1, ly + 1.55 * u], outline=P["chain"], width=w)
    r = 0.8 * (0.75 if fine else 1.0) * u
    d.ellipse([cx - r, top_y - r * 0.6, cx + r, top_y + r * 1.4], outline=P["chain"], width=w)


def draw_ring(d, S, u, state, frame=0):
    cx = S / 2
    chain(d, cx, 3.1 * u, u)
    R = 5.1 * u
    wt = 1.5 * u
    d.ellipse([cx - R, S / 2 - R, cx + R, S / 2 + R], outline=P["outline"], width=max(4, int(wt + 1.2 * u)))
    d.ellipse([cx - R, S / 2 - R, cx + R, S / 2 + R], outline=P["brass"], width=max(3, int(wt)))
    r_in = R - wt
    d.ellipse([cx - r_in, S / 2 - r_in, cx + r_in, S / 2 + r_in], fill=P["glass"])
    d.pieslice([cx - r_in, S / 2 - r_in, cx + r_in, S / 2 + r_in], 0, 180, fill=P["water"])
    d.pieslice([cx - r_in, S / 2 - r_in, cx + r_in, S / 2 + r_in], 0, 22, fill=P["water_lo"])
    for seg in range(3):
        base = seg * (2 * math.pi / 3) + 0.35
        for k in range(3):
            a = base + ((frame * 0.35 + k * 0.24) % (2 * math.pi / 3 - 0.55))
            d.ellipse([cx + R * math.cos(a) - 0.32 * u, S / 2 + R * math.sin(a) - 0.32 * u,
                       cx + R * math.cos(a) + 0.32 * u, S / 2 + R * math.sin(a) + 0.32 * u],
                      fill=P["water_hi"])
    for a in (0.785, 2.36, 3.93, 5.5):
        bx, by = cx + R * math.cos(a), S / 2 + R * math.sin(a)
        r = u * 0.5
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=P["steel_hi"], outline=P["outline"])
        d.point((bx - r * 0.4, by - r * 0.4), fill=P["outline"])
    va = frame * 0.9
    gear(d, cx, S / 2, 2.0 * u, 4, P["brass_hi"], ang=va, hole=(52, 120, 196, 255))
    d.ellipse([cx - 0.38 * u, S / 2 - 0.38 * u, cx + 0.38 * u, S / 2 + 0.38 * u],
              fill=P["brass_lo"], outline=P["outline"])
    for k in range(2):
        r = u * (0.3 + 0.16 * ((frame + k) % 3))
        d.ellipse([cx + (0.5 * u if k else -0.5 * u) - r, 1.0 * u - (frame % 3) * 0.55 * u - r,
                   cx + (0.5 * u if k else -0.5 * u) + r, 1.0 * u - (frame % 3) * 0.55 * u + r],
                  fill=(240, 247, 252, 228 - k * 36))


def draw_spiral(d, S, u, state, frame=0):
    cx = S / 2
    cy = 8.8 * u
    chain(d, cx, 2.6 * u, u)
    R = 5.8 * u
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(52, 42, 20), outline=P["outline"],
              width=max(2, int(u * 0.4)))
    d.ellipse([cx - R + 0.5 * u, cy - R + 0.5 * u, cx + R - 0.5 * u, cy + R - 0.5 * u],
              outline=P["brass_lo"], width=max(2, int(u * 0.4)))
    for i in range(12):
        a = math.pi * 0.75 + i / 11 * math.pi * 1.5
        col = (196, 60, 44) if i < 3 else P["brass_hi"]
        x1 = cx + (R - 0.9 * u) * math.cos(a)
        y1 = cy + (R - 0.9 * u) * math.sin(a)
        x2 = cx + (R - 1.6 * u) * math.cos(a)
        y2 = cy + (R - 1.6 * u) * math.sin(a)
        d.line([x1, y1, x2, y2], fill=col, width=max(1, int(u * 0.22)))
    for a in (0.785, 2.36, 3.93, 5.5):
        bx, by = cx + (R - 0.35 * u) * math.cos(a), cy + (R - 0.35 * u) * math.sin(a)
        r = u * 0.34
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=P["steel_hi"], outline=P["outline"])
    rot = frame * 0.14
    sweep = 0.55 + 0.06 * math.sin(frame * 1.5)
    steps = 64
    pts = []
    for i in range(steps + 1):
        t = i / steps
        theta = rot + t * 2.3 * 2 * math.pi
        rr = (0.5 + 3.3 * t) * u
        pts.append((cx + rr * math.cos(theta), cy + rr * math.sin(theta)))
    d.line(pts, fill=P["ember"], width=max(2, int(u * 0.45)))
    pa = math.pi * 0.75 + (0.15 + sweep) * math.pi * 1.5
    px, py = cx + (R - 2.0 * u) * math.cos(pa), cy + (R - 2.0 * u) * math.sin(pa)
    tip_x, tip_y = cx + (R - 1.0 * u) * math.cos(pa), cy + (R - 1.0 * u) * math.sin(pa)
    d.line([px, py, tip_x, tip_y], fill=(240, 236, 220), width=max(1, int(u * 0.24)))
    d.ellipse([px - 0.3 * u, py - 0.3 * u, px + 0.3 * u, py + 0.3 * u], fill=(240, 236, 220))
    fl = int(150 + 70 * math.sin(frame))
    d.ellipse([cx - 1.9 * u, cy - 1.9 * u, cx + 1.9 * u, cy + 1.9 * u], fill=(*P["ember"], fl))
    disc(d, cx, cy, 1.0 * u, (*P["ember_hi"], 235), steps=10)
    d.point((cx - 0.25 * u, cy - 0.25 * u), fill=(255, 255, 255))
    wx, wy = cx + 3.2 * u, cy + 3.2 * u
    r_w = 0.95 * u
    d.ellipse([wx - r_w, wy - r_w, wx + r_w, wy + r_w], fill=(52, 120, 196, 160), outline=P["outline"])
    d.rectangle([wx - r_w * 0.7, wy + r_w * 0.1, wx + r_w * 0.7, wy + r_w * 0.75], fill=P["water"])
    d.point((wx - 0.2 * u, wy - r_w * 0.3), fill=P["water_hi"])
    r = u * (0.28 + 0.15 * (frame % 3))
    d.ellipse([cx - 0.4 * u, 2.0 * u - (frame % 3) * 0.5 * u - r, cx + 0.4 * u,
               2.0 * u - (frame % 3) * 0.5 * u + r], fill=(240, 247, 252, 226))


def draw_coil2(d, S, u, state, frame=0):
    cx = S / 2
    chain(d, cx, 1.7 * u, u, fine=True, links=3)
    for (fy0, fy1) in ((2.6 * u, 4.0 * u), (12.6 * u, 14.0 * u)):
        for fx in (-2.6, -1.3, 0, 1.3, 2.6):
            d.rectangle([cx + fx * u - 0.2 * u, fy0, cx + fx * u + 0.2 * u, fy1],
                        fill=P["steel_lo"], outline=P["outline"])
    for cy in (4.4 * u, 12.4 * u):
        pts = [(cx + 3.3 * u * math.cos(math.pi / 6 + i / 6 * 2 * math.pi),
                cy + 1.4 * u * math.sin(math.pi / 6 + i / 6 * 2 * math.pi)) for i in range(6)]
        d.polygon(pts, fill=P["brass"], outline=P["outline"])
        d.point((cx - 1.0 * u, cy - 0.3 * u), fill=P["brass_hi"])
    tx0, tx1 = cx - 1.8 * u, cx + 1.8 * u
    d.rounded_rectangle([tx0, 4.8 * u, tx1, 12.0 * u], radius=u * 0.8,
                        fill=P["glass"], outline=P["outline"])
    ky = 8.4 * u
    pulse = int(120 + 60 * math.sin(frame * 1.1))
    d.ellipse([cx - 2.3 * u, ky - 2.6 * u, cx + 2.3 * u, ky + 2.6 * u], fill=(*P["crystal"], pulse))
    d.polygon([(cx, ky - 2.1 * u), (cx + 1.6 * u, ky), (cx, ky + 2.1 * u), (cx - 1.6 * u, ky)],
              fill=P["crystal"], outline=P["outline"])
    d.polygon([(cx, ky - 1.0 * u), (cx + 0.75 * u, ky), (cx, ky + 1.0 * u), (cx - 0.75 * u, ky)],
              fill=P["crystal_hi"])
    d.point((cx - 0.35 * u, ky - 0.7 * u), fill=(255, 255, 255))
    for yy in (5.8 * u, 8.4 * u, 11.0 * u):
        d.rounded_rectangle([cx - 2.4 * u, yy - 0.45 * u, cx + 2.4 * u, yy + 0.45 * u],
                            radius=u * 0.2, fill=P["copper"], outline=P["outline"])
        d.rectangle([cx - 2.4 * u, yy - 0.45 * u, cx + 2.4 * u, yy - 0.1 * u], fill=P["copper_hi"])
    for k in range(3):
        bx = cx + (k - 1) * 0.55 * u
        by = 11.0 * u - ((frame * 0.8 + k * 2.4) % 6) * u
        r = u * 0.16
        d.ellipse([bx - r, by - r, bx + r, by + r], outline=P["water_hi"], width=1)
    d.point((cx + 2.9 * u, 3.4 * u - (frame % 3) * 0.7 * u), fill=(255, 255, 255))
    d.point((cx - 2.9 * u, 13.6 * u + (frame % 3) * 0.7 * u), fill=(*P["water_hi"], 220))


FRAMES = 10
S = 64


def strip(painter, state):
    frames = []
    for f in range(FRAMES):
        img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        painter(d, S, S / 16.0, state, frame=f)
        frames.append(img)
    sheet = Image.new("RGBA", (S, S * FRAMES), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        sheet.paste(f, (0, i * S))
    return sheet


JOBS = {
    "steam_heater_charm_steam": (draw_ring, "steam"),
    "auto_thermostat_steam": (draw_spiral, "steam"),
    "isothermal_amulet_steam": (draw_coil2, "steam"),
    "isothermal_amulet": (draw_coil2, "idle"),
}
for name, (painter, state) in JOBS.items():
    strip(painter, state).save(os.path.join(OUT, name + ".png"))
    with open(os.path.join(OUT, name + ".png.mcmeta"), "w") as fh:
        fh.write('{"animation": {"frametime": 2, "interpolate": false}}\n')
    print("strip", name)

src = os.path.join(ROOT, "..", "addon", "src")
out = os.path.join(ROOT, "..", "build", "libs", "steamcurios_animated-0.1.0.jar")
os.makedirs(os.path.dirname(out), exist_ok=True)
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, fls in os.walk(src):
        for f in fls:
            p = os.path.join(root, f)
            z.write(p, os.path.relpath(p, src))
    print("addon jar entries:")
    for n in z.namelist():
        print(" ", n)
print("addon jar written")
