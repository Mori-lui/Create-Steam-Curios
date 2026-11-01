"""Resolution comparison preview: every item rendered at 64/32/16 px,
shown both as in-inventory-slot simulation (downscaled to 16 like the game does)
and at native size. Nothing is applied - for the user to pick a resolution."""
from PIL import Image
import os
import base64

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "gallery_res")
os.makedirs(OUT, exist_ok=True)

SRC = {
    "steam_heater_charm": os.path.join(ROOT, "gallery4"),
    "auto_thermostat": os.path.join(ROOT, "gallery7"),
    "isothermal_amulet": os.path.join(ROOT, "gallery5"),
    "brass_medallion": os.path.join(ROOT, "gallery8"),
    "thermostat_core": os.path.join(ROOT, "gallery8"),
    "incomplete_heater_charm": os.path.join(ROOT, "gallery8"),
}
ITEMS = {
    "steam_heater_charm": "Брошка (кольцо)",
    "auto_thermostat": "Автотермостат (спираль)",
    "isothermal_amulet": "Изоамулет (конденсатор)",
    "brass_medallion": "Латунный медальон",
    "thermostat_core": "Сердечник",
    "incomplete_heater_charm": "Незаконченная брошка",
}


def slot_b64(img):
    """Render the icon inside a simulated inventory slot (icon shown at 16px like in game)."""
    slot_px = 36
    slot = Image.new("RGBA", (slot_px, slot_px), (139, 139, 139, 255))
    from PIL import ImageDraw
    d = ImageDraw.Draw(slot)
    d.rectangle([0, 0, slot_px - 1, slot_px - 1], outline=(55, 55, 55, 255))
    d.rectangle([slot_px - 2, 1, slot_px - 1, slot_px - 2], fill=(255, 255, 255, 255))
    d.rectangle([1, slot_px - 2, slot_px - 2, slot_px - 1], fill=(255, 255, 255, 255))
    icon16 = img.resize((16, 16), Image.NEAREST)
    slot.alpha_composite(icon16, (10, 10))
    import io, base64
    buf = io.BytesIO()
    slot.save(buf, "PNG")
    return base64.b64encode(buf.getvalue()).decode()


def ImageDraw(im):
    from PIL import ImageDraw
    return ImageDraw.Draw(im)


def b64img(im):
    import io
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return base64.b64encode(buf.getvalue()).decode()


def b64file(path):
    return base64.b64encode(open(path, "rb").read()).decode()


rows = []
for key, label in ITEMS.items():
    src_dir = SRC[key]
    variants = []
    for size in (64, 32, 16):
        src = os.path.join(src_dir, f"{key}_steam_64.png") if size == 64 and key == "steam_heater_charm" else None
        # source file names per gallery
        if key == "steam_heater_charm":
            f = os.path.join(src_dir, f"{key}_idle_64.png")
        elif key == "auto_thermostat":
            f = os.path.join(src_dir, "spiral_idle_64.png")
        elif key == "isothermal_amulet":
            f = os.path.join(src_dir, f"{key}_idle_64.png")
        else:
            f = os.path.join(src_dir, f"{key}_64.png")
        img = Image.open(f).convert("RGBA")
        # native
        native = img.resize((size, size), Image.NEAREST) if size != 64 else img
        variants.append((size, img, native))

    cells = []
    for size, img, native in variants:
        in_slot = slot_b64(img)
        big = size * 2
        cells.append(
            f'<div class="res"><div class="grpname">{size} px</div>'
            f'<div class="slotwrap"><img src="data:image/png;base64,{in_slot}" width="36" height="36" class="pix"></div>'
            f'<img src="data:image/png;base64,{b64img(native)}" width="{big}" height="{big}" class="pix"></div>')
    rows.append(f'<div class="stycell"><div class="styname">{label}</div><div class="row">{"".join(cells)}</div></div>')

html = ('<div id="texture-res">' + "".join(rows) + '</div>'
        '<style>#texture-res{display:grid;gap:14px}'
        '#texture-res .stycell{border-top:1px solid var(--border);padding-top:10px}'
        '#texture-res .styname{font-weight:500;margin-bottom:6px}'
        '#texture-res .row{display:flex;gap:26px;flex-wrap:wrap;align-items:flex-start}'
        '#texture-res .res{display:flex;flex-direction:column;gap:4px;align-items:center}'
        '#texture-res .grpname{font-size:12px;color:var(--muted-foreground)}'
        '#texture-res .slotwrap{background:#000;padding:1px;border:2px solid #373737;border-right-color:#fff;'
        'border-bottom-color:#fff;width:42px;height:42px;display:flex;align-items:center;justify-content:center}'
        '#texture-res .pix{image-rendering:pixelated}</style>')
open(os.path.join(OUT, "fragment.html"), "w", encoding="utf-8").write(html)
print("fragment.html", len(html) // 1024, "KB")
