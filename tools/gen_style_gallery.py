"""Generate 4 texture style variants (32px + 64px, states idle/steam/dry, animated preview).

Output: tools/gallery/*.png and an HTML fragment with everything embedded.
"""
from PIL import Image, ImageDraw
import os
import base64
import io

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "gallery")
os.makedirs(OUT, exist_ok=True)

STYLES = {
    "brass": {
        "label": "1. Латунь классика",
        "rim": (43, 31, 9), "body": (183, 135, 39), "hi": (224, 180, 84), "lo": (118, 88, 26),
        "dial_bg": (168, 212, 240), "dial_hi": (228, 244, 252), "dial_lo": (112, 158, 196),
        "needle": (200, 40, 30), "fire": (221, 84, 52), "fire_hi": (255, 214, 120),
        "crystal": (94, 200, 242), "rivet": (94, 70, 16), "steam": (238, 246, 250),
    },
    "copper": {
        "label": "2. Медь с патиной",
        "rim": (36, 22, 12), "body": (184, 98, 56), "hi": (221, 137, 84), "lo": (122, 60, 30),
        "dial_bg": (150, 202, 186), "dial_hi": (212, 240, 228), "dial_lo": (96, 150, 134),
        "needle": (240, 220, 90), "fire": (210, 92, 60), "fire_hi": (250, 200, 110),
        "crystal": (110, 226, 196), "rivet": (70, 110, 96), "steam": (232, 244, 240),
    },
    "iron": {
        "label": "3. Чугун индустриальный",
        "rim": (18, 18, 20), "body": (86, 88, 94), "hi": (128, 132, 140), "lo": (52, 54, 58),
        "dial_bg": (218, 216, 208), "dial_hi": (246, 245, 240), "dial_lo": (162, 160, 152),
        "needle": (208, 60, 44), "fire": (230, 120, 50), "fire_hi": (255, 220, 130),
        "crystal": (94, 200, 242), "rivet": (30, 30, 32), "steam": (238, 246, 250),
    },
    "enamel": {
        "label": "4. Эмаль и золото",
        "rim": (94, 70, 16), "body": (240, 238, 228), "hi": (252, 251, 246), "lo": (198, 194, 182),
        "dial_bg": (28, 30, 38), "dial_hi": (58, 62, 76), "dial_lo": (14, 15, 20),
        "needle": (226, 188, 74), "fire": (226, 110, 50), "fire_hi": (255, 216, 120),
        "crystal": (110, 214, 255), "rivet": (140, 105, 28), "steam": (240, 247, 252),
    },
}


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_amulet(size, style, item, state):
    """item: charm | auto | iso ; state: idle | steam | dry"""
    p = STYLES[style]
    S = size
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = cy = S / 2.0
    R = S * 0.46            # outer radius
    u = S / 16.0            # one 16px unit

    def poly_circle(r, fill, width=None, outline=None):
        steps = max(24, int(r * 2))
        pts = [(cx + r * np_cos(i / steps * 6.28318), cy + r * np_sin(i / steps * 6.28318))
               for i in range(steps)]
        d.polygon(pts, fill=fill, outline=outline, width=width or 1)

    # body: shading via 3 arcs approximation — draw rings
    poly_circle(R, p["rim"])
    poly_circle(R - u * 0.55, p["body"])
    # top-left highlight crescent
    steps = 60
    for i in range(steps):
        ang = 3.5 + (i / steps) * 2.6
        x = cx + (R - u * 0.9) * np_cos(ang)
        y = cy + (R - u * 0.9) * np_sin(ang)
        d.point((x, y), fill=p["hi"])
        if S >= 64:
            d.point((x - 1, y), fill=lerp(p["hi"], p["body"], 0.5))
    # bottom-right shade
    for i in range(steps):
        ang = 0.4 + (i / steps) * 2.2
        x = cx + (R - u * 0.9) * np_cos(ang)
        y = cy + (R - u * 0.9) * np_sin(ang)
        d.point((x, y), fill=p["lo"])

    # rivets
    for ang in (0.8, 2.35, 3.9, 5.5):
        x = cx + (R - u * 1.15) * np_cos(ang)
        y = cy + (R - u * 1.15) * np_sin(ang)
        r = max(1, u * 0.22)
        d.ellipse([x - r, y - r, x + r, y + r], fill=p["rivet"])
        d.point((x - r / 2, y - r / 2), fill=lerp(p["rivet"], (255, 255, 255), 0.3))

    if item == "iso":
        # silver outer handled by palette; crystal core
        r0 = R - u * 1.8
        poly_circle(r0, p["dial_lo"])
        poly_circle(r0 - u * 0.3, p["crystal"])
        # crystal facets
        d.line([cx - r0 * 0.5, cy - r0 * 0.5, cx + r0 * 0.4, cy + r0 * 0.5], fill=(255, 255, 255, 120), width=1)
        d.point((cx - r0 * 0.25, cy - r0 * 0.3), fill=(255, 255, 255))
        if state == "steam":
            for (x, y, r) in [(cx - u, cy - R * 0.72, u * 0.5), (cx + u * 0.8, cy - R * 0.85, u * 0.62)]:
                d.ellipse([x - r, y - r, x + r, y + r], fill=(*p["steam"], 225))
        return img

    # dial for charm/auto
    rd = R - u * 1.9
    poly_circle(rd, p["dial_lo"])
    poly_circle(rd - u * 0.35, p["dial_bg"])
    if item == "auto" or style == "enamel":
        # white/black dial with ticks + needle
        for a in range(12):
            ang = a / 12 * 6.28318
            x1 = cx + (rd - u * 0.6) * np_cos(ang)
            y1 = cy + (rd - u * 0.6) * np_sin(ang)
            x2 = cx + (rd - u * 0.25) * np_cos(ang)
            y2 = cy + (rd - u * 0.25) * np_sin(ang)
            d.line([x1, y1, x2, y2], fill=p["rim"], width=1)
        na = 4.4 if state != "steam" else 2.0
        d.line([cx, cy, cx + (rd - u * 0.5) * np_cos(na), cy + (rd - u * 0.5) * np_sin(na)],
               fill=p["needle"], width=max(1, int(u * 0.18)))
        d.ellipse([cx - u * 0.14, cy - u * 0.14, cx + u * 0.14, cy + u * 0.14], fill=p["rim"])
    if item == "charm":
        # fire core in the middle of the dial
        rf = u * (1.7 if state == "steam" else 1.35)
        if state == "dry":
            poly_circle(rf, lerp(p["dial_lo"], (20, 20, 20), 0.55))
        else:
            poly_circle(rf, p["fire"])
            poly_circle(rf * 0.55, p["fire_hi"])
            d.point((cx - rf * 0.3, cy + rf * 0.1), fill=(255, 255, 255))

    if state == "steam":
        puffs = [(cx - u * 1.1, cy - R * 0.78, u * 0.5),
                 (cx + u * 0.4, cy - R * 0.92, u * 0.66),
                 (cx + u * 1.5, cy - R * 0.68, u * 0.42)]
        for (x, y, r) in puffs:
            d.ellipse([x - r, y - r, x + r, y + r], fill=(*p["steam"], 230))
    return img


def np_cos(x):
    import math
    return math.cos(x)


def np_sin(x):
    import math
    return math.sin(x)


def gif_frames(size, style, item, frames=8):
    imgs = []
    for k in range(frames):
        img = draw_amulet(size, style, item, "idle" if k < 2 else "steam")
        if k >= 2:
            d = ImageDraw.Draw(img)
            # moving puffs
            ph = (k - 2) / (frames - 3)
            for j in range(3):
                x = size / 2 + (j - 1) * size * 0.09 + (ph - 0.5) * size * 0.05 * (1 if j % 2 else -1)
                y = size * 0.14 - ph * size * 0.10
                r = size * (0.035 + 0.02 * j) * (0.8 + ph * 0.9)
                d.ellipse([x - r, y - r, x + r, y + r], fill=(*STYLES[style]["steam"], int(235 - ph * 140)))
        imgs.append(img)
    return imgs


files = []
for style, meta in STYLES.items():
    for item in ("charm", "auto", "iso"):
        for state in ("idle", "steam", "dry"):
            if item == "iso" and state != "idle":
                continue
            for size in (32, 64):
                name = f"{style}_{item}_{state}_{size}.png"
                img = draw_amulet(size, style, item, state)
                img.save(os.path.join(OUT, name))
                files.append(name)
    # animated preview (32px, steam cycle)
    frames = gif_frames(32, style, "charm")
    frames[0].save(os.path.join(OUT, f"{style}_anim.gif"), save_all=True,
                   append_images=frames[1:], duration=180, loop=0)
    files.append(f"{style}_anim.gif")
print("generated", len(files), "files in", OUT)

# --- build the HTML fragment with everything embedded
def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()

cards = []
for style, meta in STYLES.items():
    cell = f'<div class="stycell"><div class="styname">{meta["label"]}</div>'
    cell += '<div class="row">'
    for item, lbl in (("charm", "Брошка"), ("auto", "Автотермостат"), ("iso", "Изоамулет")):
        states = ["idle", "steam", "dry"] if item != "iso" else ["idle"]
        cell += f'<div class="grp"><div class="grpname">{lbl}</div><div class="imgs">'
        for st in states:
            cell += (f'<figure><img src="data:image/png;base64,{b64(os.path.join(OUT, style + "_" + item + "_" + st + "_32.png"))}" '
                     f'width="64" height="64" class="pix"><figcaption class="text-small text-muted">{st}</figcaption></figure>')
        cell += '</div></div>'
    cell += '</div>'
    cell += ('<div class="row big">'
             f'<figure><img src="data:image/png;base64,{b64(os.path.join(OUT, style + "_charm_steam_64.png"))}" width="128" height="128" class="pix">'
             f'<figcaption class="text-small text-muted">64 px</figcaption></figure>'
             f'<figure><img src="data:image/gif;base64,{b64(os.path.join(OUT, style + "_anim.gif"))}" width="96" height="96" class="pix">'
             f'<figcaption class="text-small text-muted">анимация</figcaption></figure></div>')
    cell += '</div>'
    cards.append(cell)

html = ('<div id="texture-styles">' + "".join(cards) + '</div>'
        '<style>#texture-styles{display:grid;gap:14px}'
        '#texture-styles .stycell{border-top:1px solid var(--border);padding-top:10px}'
        '#texture-styles .styname{font-weight:500;margin-bottom:6px}'
        '#texture-styles .row{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}'
        '#texture-styles .grpname{font-size:12px;color:var(--muted-foreground);margin-bottom:2px}'
        '#texture-styles .imgs{display:flex;gap:10px}'
        '#texture-styles figure{margin:0;text-align:center}'
        '#texture-styles .pix{image-rendering:pixelated;background:var(--muted);border-radius:6px}'
        '#texture-styles .big{align-items:center;margin-top:6px}</style>')
open(os.path.join(OUT, "fragment.html"), "w", encoding="utf-8").write(html)
print("fragment.html written,", len(html) // 1024, "KB")
