"""Round 3: auto_thermostat as a mini steam engine with a spinning flywheel. 64px only."""
from PIL import Image, ImageDraw
import math
import os
import base64

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "gallery6")
os.makedirs(OUT, exist_ok=True)

P = dict(outline=(32, 26, 16), steel=(118, 122, 130), steel_hi=(162, 167, 176), steel_lo=(70, 72, 78),
         brass=(190, 140, 46), brass_hi=(228, 180, 78), brass_lo=(116, 84, 26),
         copper=(196, 108, 56), copper_hi=(232, 150, 84),
         water=(52, 120, 196), water_hi=(116, 190, 242), water_lo=(30, 78, 140),
         ember=(235, 120, 45), ember_hi=(255, 216, 110), chain=(158, 160, 168),
         glass=(198, 228, 246, 55))


def chain(d, cx, top_y, u, links=3):
    w = max(1, int(u * 0.36))
    for k in range(links):
        ly = top_y - (k + 0.55) * 1.6 * u
        w1 = 0.55 * u
        d.ellipse([cx - w1, ly, cx + w1, ly + 1.55 * u], outline=P["chain"], width=w)
    r = 0.8 * u
    d.ellipse([cx - r, top_y - r * 0.6, cx + r, top_y + r * 1.4], outline=P["chain"], width=w)


def draw_engine(d, S, u, state, frame=0):
    cx = S / 2
    chain(d, cx, 3.2 * u, u)
    # mounting beam
    d.rounded_rectangle([2.6 * u, 3.6 * u, S - 2.6 * u, 4.8 * u], radius=u * 0.3,
                        fill=P["brass"], outline=P["outline"])
    d.rectangle([2.6 * u, 3.6 * u, S - 2.6 * u, 4.0 * u], fill=P["brass_hi"])
    # chimney on the cylinder top
    d.rectangle([4.4 * u, 4.8 * u, 5.6 * u, 6.4 * u], fill=P["brass_lo"], outline=P["outline"])
    # horizontal cylinder
    cyl = [3.4 * u, 6.2 * u, 9.0 * u, 10.6 * u]
    d.rounded_rectangle(cyl, radius=u * 0.8, fill=P["copper"], outline=P["outline"])
    d.rectangle([cyl[0] + 0.4 * u, cyl[1] + 0.4 * u, cyl[0] + 1.1 * u, cyl[3] - 0.4 * u],
                fill=P["copper_hi"])
    # firebox window at the left end of the cylinder
    if state == "dry":
        d.rounded_rectangle([3.9 * u, 7.0 * u, 6.1 * u, 9.8 * u], radius=u * 0.4,
                            fill=(30, 24, 20), outline=P["outline"])
    else:
        fl = int(170 + 60 * math.sin(frame * 1.2))
        d.rounded_rectangle([3.9 * u, 7.0 * u, 6.1 * u, 9.8 * u], radius=u * 0.4,
                            fill=P["ember"], outline=P["outline"])
        d.ellipse([4.5 * u, 7.9 * u, 5.5 * u, 9.0 * u], fill=(*P["ember_hi"], fl))
    # piston rod to the flywheel crank (slides with the wheel angle)
    wa = 0.0 if state != "steam" else frame * 0.7
    wc_x, wc_y = 11.4 * u, 8.4 * u
    crank_x = wc_x + 1.1 * u * math.cos(wa)
    crank_y = wc_y + 1.1 * u * math.sin(wa)
    d.line([7.6 * u, 8.4 * u, crank_x, crank_y], fill=P["steel_hi"], width=max(2, int(u * 0.5)))
    d.ellipse([crank_x - 0.4 * u, crank_y - 0.4 * u, crank_x + 0.4 * u, crank_y + 0.4 * u],
              fill=P["steel_hi"], outline=P["outline"])
    # flywheel: rim + 4 spokes + hub (rotates)
    R = 3.4 * u
    d.ellipse([wc_x - R, wc_y - R, wc_x + R, wc_y + R], outline=P["steel"], width=max(3, int(u * 0.7)))
    for k in range(4):
        a = wa + k / 4 * 2 * math.pi
        d.line([wc_x, wc_y, wc_x + (R - u * 0.35) * math.cos(a), wc_y + (R - u * 0.35) * math.sin(a)],
               fill=P["steel_hi"], width=max(1, int(u * 0.45)))
    d.ellipse([wc_x - 0.8 * u, wc_y - 0.8 * u, wc_x + 0.8 * u, wc_y + 0.8 * u],
              fill=P["brass_hi"], outline=P["outline"])
    # base skid
    d.rounded_rectangle([2.8 * u, 12.2 * u, S - 2.4 * u, 13.6 * u], radius=u * 0.4,
                        fill=P["brass"], outline=P["outline"])
    for bx in (4.0, S / u - 4.0):
        d.rectangle([bx * u - 0.25 * u, 10.4 * u, bx * u + 0.25 * u, 12.4 * u],
                    fill=P["brass_lo"], outline=P["outline"])
    # water glass tank on the skid (feeds the boiler)
    d.rounded_rectangle([9.6 * u, 10.2 * u, 12.2 * u, 12.4 * u], radius=u * 0.25,
                        fill=P["glass"], outline=P["outline"])
    if state != "dry":
        lvl = 0.35 if state == "steam" else 0.55
        d.rectangle([9.75 * u, 10.2 * u + (12.4 * u - 10.2 * u) * lvl, 12.05 * u, 12.25 * u],
                    fill=P["water"])
        if state == "steam":
            for k in range(2):
                by = 11.9 * u - ((frame * 0.9 + k * 1.8) % 3) * 0.5 * u
                d.ellipse([10.85 * u - 0.15 * u, by - 0.15 * u, 10.85 * u + 0.15 * u, by + 0.15 * u],
                          outline=P["water_hi"], width=1)
    # steam puffs from the chimney
    if state == "steam":
        for k in range(2):
            r = u * (0.3 + 0.16 * ((frame + k) % 3))
            d.ellipse([5.0 * u - r, 3.4 * u - (frame % 3) * 0.7 * u - k * 0.4 * u - r,
                       5.0 * u + r, 3.4 * u - (frame % 3) * 0.7 * u - k * 0.4 * u + r],
                      fill=(240, 247, 252, 228 - k * 40))


files = []
for state in ("idle", "steam", "dry"):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    draw_engine(d, 64, 4.0, state, frame=0)
    img.save(os.path.join(OUT, f"engine_{state}_64.png"))
    files.append(f"engine_{state}_64.png")
frames = []
for f in range(10):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    draw_engine(d, 64, 4.0, "steam", frame=f)
    frames.append(img)
frames[0].save(os.path.join(OUT, "engine_anim.gif"), save_all=True,
               append_images=frames[1:], duration=150, loop=0)
files.append("engine_anim.gif")
print("generated", len(files), "files")


def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()


cards = ['<div id="texture-designs3"><div class="stycell"><div class="styname">Паровой двигатель (автотермостат, 64 px)</div><div class="row">']
for st, stl in (("idle", "покой"), ("steam", "работа"), ("dry", "сухой")):
    cards.append(f'<div class="grp"><div class="grpname">{stl}</div>'
                 f'<figure><img src="data:image/png;base64,{b64(os.path.join(OUT, "engine_" + st + "_64.png"))}" width="160" height="160" class="pix"></figure></div>')
cards.append(f'<div class="grp"><div class="grpname">анимация</div>'
             f'<img src="data:image/gif;base64,{b64(os.path.join(OUT, "engine_anim.gif"))}" width="160" height="160" class="pix"></div>')
cards.append('</div></div></div>'
             '<style>#texture-designs3{display:grid;gap:16px}'
             '#texture-designs3 .stycell{border-top:1px solid var(--border);padding-top:10px}'
             '#texture-designs3 .styname{font-weight:500;margin-bottom:6px}'
             '#texture-designs3 .row{display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start}'
             '#texture-designs3 .grpname{font-size:12px;color:var(--muted-foreground);margin-bottom:2px}'
             '#texture-designs3 figure{margin:0;text-align:center}'
             '#texture-designs3 .pix{image-rendering:pixelated;background:var(--muted);border-radius:6px}</style>')
open(os.path.join(OUT, "fragment.html"), "w", encoding="utf-8").write(html := "".join(cards))
print("fragment.html", len(html) // 1024, "KB")
