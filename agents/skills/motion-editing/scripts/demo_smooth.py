"""Reference demo: staggered spring cards + word pop + counter + motion blur (moving layer only) + supersampling.
python3 demo_smooth.py [smooth|naive]  -> demo_<mode>.mp4   (720x1280, 30 fps, 3.5 s)"""
import sys, math, os
from motion import *
W, H, FPS, DUR = 720, 1280, 30, 3.5

for _fp in ["fonts/InterDisplay-Bold.otf", "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf", os.path.expanduser("~/Library/Fonts/InterDisplay-Bold.otf")]:
    if os.path.exists(_fp): FB = _fp; break
else: FB = "fonts/InterDisplay-Bold.otf"
mode = sys.argv[1] if len(sys.argv) > 1 else "smooth"
bg = Image.new("RGB", (W, H)); d = ImageDraw.Draw(bg)
for y in range(H):
    t = y / H; d.line([(0, y), (W, y)], fill=tuple(int((8, 12, 28)[i] + ((30, 16, 70)[i] - (8, 12, 28)[i]) * t) for i in range(3)))
CARDS = [("Predict", (70, 220, 255)), ("Act", (150, 110, 255)), ("Observe", (90, 235, 150))]
def card_x(i, t):                                   # x position of card i at time t
    if mode == "naive": return int(lerp(W + 40, 60, clamp((t - 0.4 - i * 0.25) / 0.5)))                 # linear, integer px
    return lerp(W + 40, 60, spring(t - 0.4 - i * 0.12 - random.Random(i).uniform(-0.02, 0.02)))          # spring, stagger, sub-pixel
def cards_layer(t):
    S = 1 if mode == "naive" else 2; ss = SS((W, H), S); f = ss.font(FB, 54)
    for i, (n, c) in enumerate(CARDS):
        x = card_x(i, t); y = 420 + i * 190
        ss.rrect([x, y, x + 600, y + 150], radius=34, fill=(30, 26, 70, 255), outline=c, width=6); ss.text((x + 300, y + 75), n, f, fill=(255, 255, 255, 255))
    return ss.out()
def frame(k):
    t = k / FPS; ss = SS((W, H), 1 if mode == "naive" else 2); f = ss.font(FB, 64); f2 = ss.font(FB, 150)
    if mode == "naive": ss.text((W / 2, 220), "How agents work", f, fill=(255, 255, 255, 255))
    else: word_pop(ss, (W / 2, 220), "How agents work".split(), t, 0.1, f)
    ss.text((W / 2, 1120), count_up(t, 1.4, 1.4, 87) + "%" if mode != "naive" else f"{int(87 * clamp((t - 1.4) / 1.4))}%", f2, fill=(255, 205, 70, 255))
    sp = max(speed_px(lambda tt, i=i: (card_x(i, tt), 0), t, FPS) for i in range(3))       # fastest card, px/frame
    layer = blur_layer(cards_layer, t, FPS, 180, auto_samples(sp)) if (mode == "smooth" and sp > 1.5) else cards_layer(t)
    im = composite(push_in(bg, clamp(t / DUR), 0.03) if mode == "smooth" else bg, layer, ss.out())
    return finish(im, k, 2.5, 0.12) if mode == "smooth" else im
if __name__ == "__main__":
    enc = open_encoder(f"demo_{mode}.mp4", W, H, FPS)
    for k in range(int(DUR * FPS)): enc.stdin.write(frame(k).tobytes())
    enc.stdin.close(); enc.wait(); print("done", mode)
