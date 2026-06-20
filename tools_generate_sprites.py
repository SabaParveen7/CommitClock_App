"""
Generates simple placeholder chibi-style character art for all 5 moods
using Pillow. These are deliberately simple geometric placeholders so
the app is fully runnable out of the box — swap them for real
hand-drawn/animated sprite sheets before shipping (PDR 7.2).

Each mood gets a single 256x256 PNG (not an animated sheet) for
simplicity; mood_engine.py just swaps the static image per state.
If you want real frame-by-frame animation, replace these with sprite
sheets and update screens/alarm_screen.py + schedule_screen.py to
step through frames.
"""
from PIL import Image, ImageDraw

NAVY = (13, 27, 42, 255)
BODY = (245, 240, 232, 255)
GOLD = (244, 197, 66, 255)
GREEN = (46, 204, 113, 255)
DARK = (26, 26, 26, 255)
BLUE_BG = (20, 35, 54, 255)
SAD_BLUE = (90, 110, 130, 255)

SIZE = 256


def base_canvas(bg=BLUE_BG):
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def draw_body(d, cx=128, cy=150, r=70, color=BODY):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


def draw_eyes(d, cx, cy, style="normal"):
    if style == "normal":
        d.ellipse([cx - 28, cy - 10, cx - 14, cy + 6], fill=DARK)
        d.ellipse([cx + 14, cy - 10, cx + 28, cy + 6], fill=DARK)
    elif style == "happy":
        d.arc([cx - 30, cy - 14, cx - 12, cy + 6], 200, 340, fill=DARK, width=4)
        d.arc([cx + 12, cy - 14, cx + 30, cy + 6], 200, 340, fill=DARK, width=4)
    elif style == "sad":
        d.ellipse([cx - 26, cy - 4, cx - 14, cy + 8], fill=SAD_BLUE)
        d.ellipse([cx + 14, cy - 4, cx + 26, cy + 8], fill=SAD_BLUE)
        d.line([cx - 26, cy - 8, cx - 14, cy - 14], fill=DARK, width=3)
        d.line([cx + 14, cy - 14, cx + 26, cy - 8], fill=DARK, width=3)
    elif style == "star":
        for sx in (cx - 21, cx + 21):
            d.line([sx - 8, cy, sx + 8, cy], fill=GOLD, width=4)
            d.line([sx, cy - 8, sx, cy + 8], fill=GOLD, width=4)


def draw_mouth(d, cx, cy, style="smile"):
    if style == "smile":
        d.arc([cx - 18, cy - 6, cx + 18, cy + 18], 20, 160, fill=DARK, width=4)
    elif style == "open":
        d.ellipse([cx - 14, cy, cx + 14, cy + 22], fill=DARK)
    elif style == "flat":
        d.line([cx - 14, cy + 8, cx + 14, cy + 8], fill=DARK, width=4)


def draw_cheeks(d, cx, cy, color=(244, 150, 150, 160)):
    d.ellipse([cx - 55, cy + 4, cx - 35, cy + 18], fill=color)
    d.ellipse([cx + 35, cy + 4, cx + 55, cy + 18], fill=color)


def draw_bell(d, cx=128, cy=55):
    d.polygon([(cx - 26, cy + 20), (cx + 26, cy + 20), (cx + 16, cy - 18), (cx - 16, cy - 18)], fill=GOLD)
    d.ellipse([cx - 8, cy + 14, cx + 8, cy + 30], fill=GOLD)
    d.ellipse([cx - 5, cy + 19, cx + 5, cy + 29], fill=DARK)


def draw_arms_up(d, cx=128, cy=150, r=70):
    d.line([cx - r + 10, cy - 10, cx - r - 20, cy - 70], fill=BODY, width=18)
    d.line([cx + r - 10, cy - 10, cx + r + 20, cy - 70], fill=BODY, width=18)


def draw_arms_down(d, cx=128, cy=150, r=70):
    d.line([cx - r + 10, cy, cx - r - 10, cy + 50], fill=BODY, width=16)
    d.line([cx + r - 10, cy, cx + r + 10, cy + 50], fill=BODY, width=16)


def draw_confetti(d, color1=GOLD, color2=GREEN):
    import random
    random.seed(7)
    for _ in range(18):
        x, y = random.randint(10, 246), random.randint(10, 246)
        c = color1 if random.random() > 0.5 else color2
        d.rectangle([x, y, x + 6, y + 6], fill=c)


def make_idle():
    img, d = base_canvas()
    draw_arms_down(d)
    draw_body(d)
    draw_eyes(d, 128, 140, "normal")
    draw_cheeks(d, 128, 140)
    draw_mouth(d, 128, 160, "smile")
    return img


def make_ringing():
    img, d = base_canvas()
    draw_bell(d)
    draw_arms_up(d)
    draw_body(d)
    draw_eyes(d, 128, 140, "normal")
    draw_cheeks(d, 128, 140)
    draw_mouth(d, 128, 158, "open")
    return img


def make_happy():
    img, d = base_canvas()
    draw_confetti(d)
    draw_arms_up(d)
    draw_body(d)
    draw_eyes(d, 128, 140, "happy")
    draw_cheeks(d, 128, 140)
    draw_mouth(d, 128, 158, "open")
    return img


def make_sad():
    img, d = base_canvas()
    draw_arms_down(d)
    draw_body(d, color=(225, 222, 215, 255))
    draw_eyes(d, 128, 145, "sad")
    draw_mouth(d, 128, 168, "flat")
    return img


def make_excited():
    img, d = base_canvas()
    draw_confetti(d, color1=GOLD, color2=(255, 255, 255, 255))
    draw_confetti(d, color1=GREEN, color2=GOLD)
    draw_arms_up(d)
    draw_body(d)
    draw_eyes(d, 128, 138, "star")
    draw_cheeks(d, 128, 138)
    draw_mouth(d, 128, 156, "open")
    return img


if __name__ == "__main__":
    moods = {
        "character_idle.png": make_idle,
        "character_ringing.png": make_ringing,
        "character_happy.png": make_happy,
        "character_sad.png": make_sad,
        "character_excited.png": make_excited,
    }
    for filename, fn in moods.items():
        fn().save(f"assets/{filename}")
        print(f"wrote assets/{filename}")
