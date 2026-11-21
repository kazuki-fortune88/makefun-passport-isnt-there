"""Generate the passport spread for the fictional Republic of Talmara.

Deterministic, stdlib + PIL only, no network. Draws a 1024x1024 PNG:
an open passport spread -- data page (left) + visa/stamp page (right).
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF_I = lambda s: font("DejaVuSerif-Italic.ttf", s) if os.path.exists(
    os.path.join(FONT_DIR, "DejaVuSerif-Italic.ttf")) else font("DejaVuSerif.ttf", s)
MONO = lambda s: font("DejaVuSansMono.ttf", s)

CREAM = (247, 242, 230)
CREAM2 = (240, 233, 214)
INK = (28, 32, 48)
MUTED = (110, 105, 90)
NAVY = (24, 48, 88)
GOLD = (176, 138, 52)
TEAL = (38, 110, 105)


# --- MRZ (ICAO 9303 check digits) -------------------------------------------
def _check(s):
    weights = [7, 3, 1]
    vals = {}
    for i, c in enumerate("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        vals[c] = i
    total = 0
    for i, ch in enumerate(s):
        v = vals.get(ch, 0) if ch != "<" else 0
        total += v * weights[i % 3]
    return str(total % 10)


def mrz_lines():
    line1 = "P<TALANSEL<<ELENA<MARIS<<<<<<<<<<<<<<<<"
    line1 = line1[:44].ljust(44, "<")
    doc = "TAL482913"
    doc_cd = _check(doc)
    dob = "940314"
    dob_cd = _check(dob)
    exp = "330511"
    exp_cd = _check(exp)
    personal = "<" * 14
    composite_src = doc + doc_cd + dob + dob_cd + exp + exp_cd + personal + "0"
    comp_cd = _check(composite_src)
    line2 = (doc + doc_cd + "TAL" + dob + dob_cd + "F" + exp + exp_cd
             + personal + comp_cd + "0")
    assert len(line1) == 44 and len(line2) == 44, (len(line1), len(line2))
    return line1, line2


# --- helpers -----------------------------------------------------------------
def text(d, xy, s, f, fill=INK, anchor="la"):
    d.text(xy, s, font=f, fill=fill, anchor=anchor)


def wrap_guilloche(d, box, color, step=7):
    """Fine wavy security lines inside a page box."""
    x0, y0, x1, y1 = box
    for k in range(0, (y1 - y0) // step + 1):
        y = y0 + k * step
        pts = []
        for x in range(x0, x1 + 1, 8):
            pts.append((x, y + 2.2 * math.sin((x - x0) / 26.0 + k * 0.55)))
        d.line(pts, fill=color, width=1)


def draw_emblem(d, cx, cy, r):
    """Talmara emblem: gold ring, navy disc, white wave + gold seabird."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=3)
    d.ellipse([cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5], fill=NAVY)
    for i, yy in enumerate((-6, 2, 10)):
        pts = []
        for x in range(cx - r + 10, cx + r - 9, 4):
            pts.append((x, cy + yy + 3 * math.sin((x - cx) / 9.0 + i)))
        d.line(pts, fill=(255, 255, 255), width=2)
    # seabird: two arcs
    d.arc([cx - 16, cy - 26, cx - 2, cy - 10], 200, 340, fill=GOLD, width=3)
    d.arc([cx + 2, cy - 26, cx + 16, cy - 10], 200, 340, fill=GOLD, width=3)
    d.ellipse([cx - 2, cy - 21, cx + 2, cy - 17], fill=GOLD)


def draw_portrait(d, box):
    """Stylised portrait drawn with PIL shapes (no photo)."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(126, 178, 168))
    # faint backdrop arch
    d.ellipse([x0 + 18, y0 - 30, x1 - 18, y0 + 120], fill=(150, 196, 186))
    cx = (x0 + x1) // 2
    # shoulders / jacket
    d.polygon([(x0 + 8, y1), (cx - 52, y0 + 138), (cx - 30, y0 + 128),
               (cx, y0 + 148), (cx + 30, y0 + 128), (cx + 52, y0 + 138),
               (x1 - 8, y1)], fill=(36, 64, 96))
    # white collar + blouse
    d.polygon([(cx - 30, y0 + 128), (cx, y0 + 150), (cx + 30, y0 + 128),
               (cx + 22, y0 + 118), (cx, y0 + 132), (cx - 22, y0 + 118)],
              fill=(250, 248, 240))
    # neck
    d.rectangle([cx - 13, y0 + 104, cx + 13, y0 + 134], fill=(206, 158, 118))
    # head
    d.ellipse([cx - 38, y0 + 22, cx + 38, y0 + 112], fill=(222, 172, 132))
    # ears
    d.ellipse([cx - 44, y0 + 58, cx - 34, y0 + 80], fill=(222, 172, 132))
    d.ellipse([cx + 34, y0 + 58, cx + 44, y0 + 80], fill=(222, 172, 132))
    # hair: dark bob framing the face
    d.pieslice([cx - 46, y0 + 8, cx + 46, y0 + 96], 180, 360, fill=(52, 36, 28))
    d.ellipse([cx - 46, y0 + 30, cx - 30, y0 + 96], fill=(52, 36, 28))
    d.ellipse([cx + 30, y0 + 30, cx + 46, y0 + 96], fill=(52, 36, 28))
    d.arc([cx - 38, y0 + 20, cx + 38, y0 + 78], 180, 360, fill=(52, 36, 28), width=10)
    # brows, eyes, nose, mouth
    d.line([(cx - 24, y0 + 58), (cx - 8, y0 + 56)], fill=(52, 36, 28), width=3)
    d.line([(cx + 8, y0 + 56), (cx + 24, y0 + 58)], fill=(52, 36, 28), width=3)
    for ex in (cx - 16, cx + 16):
        d.ellipse([ex - 6, y0 + 62, ex + 6, y0 + 70], fill=(255, 255, 255))
        d.ellipse([ex - 3, y0 + 63, ex + 3, y0 + 69], fill=(40, 28, 24))
    d.line([(cx, y0 + 70), (cx - 2, y0 + 84), (cx + 3, y0 + 86)], fill=(190, 140, 104), width=2)
    d.arc([cx - 9, y0 + 88, cx + 9, y0 + 100], 15, 165, fill=(150, 70, 60), width=3)
    # portrait frame
    d.rectangle(box, outline=NAVY, width=3)


def stamp(d, cx, cy, w, h, color, lines, angle=-6):
    """One ink entry/exit stamp, drawn on its own layer then rotated."""
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([20, 20, 20 + w, 20 + h], radius=10,
                         outline=color + (255,), width=3)
    ld.rounded_rectangle([25, 25, 25 + w, 25 + h], radius=7,
                         outline=color + (255,), width=1)
    y = 20 + 12
    for s, f, col in lines:
        ld.text(((w + 40) // 2, y), s, font=f, fill=col + (255,), anchor="ma")
        y += f.size + 4
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
    d._image.paste(layer, (cx - (w + 40) // 2, cy - (h + 40) // 2), layer)


def field(d, x, y, label, value, vsize=21, label_size=12):
    text(d, (x, y), label, SANS_B(label_size), fill=MUTED)
    text(d, (x, y + 15), value, SANS_B(vsize), fill=INK)


def build(path):
    img = Image.new("RGB", (W, H), (43, 50, 66))
    d = ImageDraw.Draw(img)
    # desk shading
    for i in range(H):
        pass
    d.rectangle([0, 0, W, 46], fill=(36, 42, 56))
    text(d, (512, 14), "REPUBLIC OF TALMARA  •  PASSPORT SPREAD  •  SPECIMEN",
         SANS_B(15), fill=(200, 205, 220), anchor="ma")
    # shadow under spread
    d.rectangle([46, 108, 978, 922], fill=(20, 24, 34))
    # pages
    d.rectangle([52, 100, 502, 914], fill=CREAM)
    d.rectangle([522, 100, 972, 914], fill=CREAM2)
    d.rectangle([502, 100, 522, 914], fill=(214, 204, 182))
    d.line([(512, 100), (512, 914)], fill=(170, 158, 132), width=2)
    wrap_guilloche(d, (58, 108, 496, 906), (214, 204, 178))
    wrap_guilloche(d, (528, 108, 966, 906), (210, 200, 172))

    # ---- LEFT PAGE: data -----------------------------------------------
    draw_emblem(d, 128, 168, 42)
    text(d, (186, 132), "REPUBLIC OF TALMARA", SERIF_B(25), fill=NAVY)
    text(d, (186, 162), "REPUBLIKA TALMARA", SERIF(16), fill=MUTED)
    text(d, (186, 186), "PASSPORT  •  PASAPORT", SANS_B(13), fill=GOLD)
    d.line([(64, 216), (490, 216)], fill=GOLD, width=2)
    text(d, (490, 226), "No. TAL482913", SANS_B(17), fill=NAVY, anchor="ra")

    draw_portrait(d, (72, 252, 222, 442))
    text(d, (147, 448), "HOLDER  •  PEMEGANG", SANS_B(10), fill=MUTED, anchor="ma")

    fx = 244
    field(d, fx, 252, "SURNAME  •  NAMA KELUARGA", "ANSEL")
    field(d, fx, 302, "GIVEN NAMES  •  NAMA DEPAN", "ELENA MARIS")
    field(d, fx, 352, "NATIONALITY  •  KEWARGANEGARAAN", "TALMARIAN")
    field(d, fx, 402, "SEX  •  JANTINA", "F")
    field(d, 72, 486, "DATE OF BIRTH", "14 MAR 1994")
    field(d, 272, 486, "PLACE OF BIRTH", "PORT ANSELM")
    field(d, 72, 536, "DATE OF ISSUE", "12 MAY 2023")
    field(d, 272, 536, "DATE OF EXPIRY", "11 MAY 2033")
    field(d, 72, 586, "AUTHORITY", "PORT ANSELM")
    field(d, 272, 586, "HEIGHT", "168 cm")
    d.line([(64, 646), (490, 646)], fill=(200, 190, 164), width=1)
    text(d, (72, 658), "SIGNATURE  •  TANDATANGAN", SANS_B(11), fill=MUTED)
    text(d, (72, 678), "Elena Ansel", SERIF_I(30), fill=(40, 60, 110))
    text(d, (490, 658), "p. 4", SANS(12), fill=MUTED, anchor="ra")

    # MRZ strip
    d.rectangle([64, 736, 490, 806], fill=(232, 226, 208))
    l1, l2 = mrz_lines()
    text(d, (277, 748), l1, MONO(14), fill=INK, anchor="ma")
    text(d, (277, 770), l2, MONO(14), fill=INK, anchor="ma")
    text(d, (277, 812), "Machine-readable zone matches the data above.",
         SANS(11), fill=MUTED, anchor="ma")
    text(d, (277, 868), "Property of the Republic of Talmara — an island",
         SANS(12), fill=MUTED, anchor="ma")
    text(d, (277, 886), "republic of the Meridian Sea. Currency: thaler.",
         SANS(12), fill=MUTED, anchor="ma")

    # ---- RIGHT PAGE: visas / stamps ------------------------------------
    text(d, (747, 126), "VISAS", SERIF_B(26), fill=NAVY, anchor="ma")
    text(d, (747, 156), "VISA  •  HALAMAN COP", SANS_B(12), fill=MUTED, anchor="ma")
    d.line([(540, 182), (954, 182)], fill=GOLD, width=2)

    BLUE = (36, 80, 160)
    GREEN = (34, 120, 70)
    RED = (170, 40, 40)
    PURPLE = (110, 60, 140)
    f_big = SANS_B(17)
    f_mid = SANS_B(14)
    f_sm = SANS(12)

    stamp(d, 747, 268, 330, 92, GREEN, [
        ("REPUBLIC OF MERIDIA", f_big, GREEN),
        ("ENTRY  •  PORT LIORA", f_mid, GREEN),
        ("04 JUN 2023", f_mid, GREEN),
    ], angle=-4)
    stamp(d, 747, 386, 330, 92, GREEN, [
        ("REPUBLIC OF MERIDIA", f_big, GREEN),
        ("EXIT  •  PORT LIORA", f_mid, GREEN),
        ("18 JUN 2023", f_mid, GREEN),
    ], angle=3)
    stamp(d, 747, 504, 330, 92, RED, [
        ("KINGDOM OF SORVANE", f_big, RED),
        ("ENTRY  •  KESTREL GATE", f_mid, RED),
        ("11 OCT 2024", f_mid, RED),
    ], angle=-3)
    stamp(d, 747, 622, 330, 92, BLUE, [
        ("REPUBLIC OF TALMARA", f_big, BLUE),
        ("ENTRY  •  PORT ANSELM", f_mid, BLUE),
        ("25 OCT 2024", f_mid, BLUE),
    ], angle=4)

    # telling detail: visa-on-arrival fee stamp (Sorvane)
    stamp(d, 747, 756, 360, 84, PURPLE, [
        ("VISA ON ARRIVAL — 30 DAYS", f_big, PURPLE),
        ("FEE 25 THALERS  •  PAID", f_mid, PURPLE),
        ("SORVANE  •  11 OCT 2024", f_sm, PURPLE),
    ], angle=-2)

    text(d, (747, 830), "All stamps dated after issue (12 MAY 2023),",
         SANS(12), fill=MUTED, anchor="ma")
    text(d, (747, 848), "in chronological order. No stamp precedes issue.",
         SANS(12), fill=MUTED, anchor="ma")
    text(d, (954, 868), "p. 5", SANS(12), fill=MUTED, anchor="ra")

    img.save(path, format="PNG")
    return path


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png"
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    build(out)
    print("wrote", out)
