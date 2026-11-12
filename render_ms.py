import json, math, subprocess, os
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont
from longdata_ms import SCENES

W, H, FPS = 1920, 1080, 24

for _fp in [
    "fonts/InterDisplay-Bold.otf",
    os.path.expanduser("~/Library/Fonts/InterDisplay-Bold.otf"),
    "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
]:
    if os.path.exists(_fp):
        FB = _fp
        break
else:
    FB = "fonts/InterDisplay-Bold.otf"

@lru_cache(None)
def F(s):
    return ImageFont.truetype(FB, max(int(s), 1))

WHITE = (255, 255, 255)
DIM = (185, 192, 225)
RED = (255, 70, 90)
CY = (70, 220, 255)
YEL = (255, 205, 70)
GRN = (90, 235, 150)
PUR = (150, 110, 255)
ACC = {"G": GRN, "R": RED, "Y": YEL, "C": CY, "P": PUR}

bg = Image.new("RGB", (W, H))
d = ImageDraw.Draw(bg)
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=tuple(int((8, 12, 28)[i] + ((30, 16, 70)[i] - (8, 12, 28)[i]) * t) for i in range(3)))
for x in range(0, W, 90):
    d.line([(x, 0), (x, H)], fill=(22, 28, 58))
for y in range(0, H, 90):
    d.line([(0, y), (W, y)], fill=(22, 28, 58))

DUM = ImageDraw.Draw(Image.new("RGB", (4, 4)))

def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3

def T(dr, xy, s, f, fill, a="mm", st=0):
    dr.text(xy, s, font=f, fill=fill, anchor=a, stroke_width=st, stroke_fill=(0, 0, 0))

def fit(s, size, maxw):
    while size > 34 and DUM.textlength(s, font=F(size)) > maxw:
        size -= 2
    return F(size)

def wrap(s, font, maxw):
    out = []
    cur = ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if DUM.textlength(t, font=font) <= maxw:
            cur = t
        else:
            out.append(cur)
            cur = w
    return out + [cur]

def draw_list(img, sc, bi, tb):
    dr = ImageDraw.Draw(img)
    acc = ACC[sc["accent"]]
    bs = sc["beats"]
    T(dr, (120, 180), sc["heading"], F(78), acc, "lm")
    dr.rectangle([120, 240, 560, 246], fill=acc)
    items = []
    for k, b in enumerate(bs[:bi + 1]):
        if b[1]:
            for l in (b[1] if isinstance(b[1], list) else [b[1]]):
                items.append((l, k))
    for i, (l, k) in enumerate(items):
        y = 350 + i * 115
        cur = (k == bi)
        off = int((1 - ease(tb / 0.3)) * 70) if cur else 0
        dr.ellipse([120 + off, y - 13, 146 + off, y + 13], fill=acc)
        T(dr, (180 + off, y), l, fit(l, 62, 1100), WHITE if cur else DIM, "lm")
    
    cx, cy = 1480, 450
    r = int(170 * (0.9 + 0.1 * ease(tb / 0.3)))
    p = sc["panel"]
    if p == "good":
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(20, 70, 55), outline=GRN, width=10)
        dr.line([(cx - 80, cy + 5), (cx - 20, cy + 65), (cx + 85, cy - 60)], fill=GRN, width=28, joint="curve")
    elif p == "bad":
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(80, 20, 35), outline=RED, width=10)
        dr.line([(cx - 70, cy - 70), (cx + 70, cy + 70)], fill=RED, width=28)
        dr.line([(cx - 70, cy + 70), (cx + 70, cy - 70)], fill=RED, width=28)
    elif p == "change":
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(80, 60, 10), outline=YEL, width=10)
        T(dr, (cx, cy - 5), "!", F(240), YEL)
    else:
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 22, 70), outline=acc, width=10)
        T(dr, (cx, cy - 5), str(bi + 1), F(230), acc)
        if sc.get("prefix"):
            T(dr, (cx, cy + r + 70), f"{sc['prefix']} {bi + 1}", F(64), WHITE)
    
    side = None
    for b in bs[:bi + 1]:
        if b[2]:
            side = b[2]
    if side:
        for j, ln in enumerate(wrap(side, F(58), 760)):
            T(dr, (cx, cy + r + 70 + j * 72), ln, F(58), WHITE)

def draw_hook(img, bi, tb):
    dr = ImageDraw.Draw(img)
    T(dr, (W / 2, 130), "How AI Answers in Milliseconds", F(78), WHITE)
    T(dr, (W / 2, 218), "(No Math, No Hype)", F(68), CY)
    def sl(k):
        return int((1 - ease(tb / 0.35)) * 120) if bi == k else 0
    if bi >= 0:
        o = sl(0)
        dr.rounded_rectangle([220 - o, 320, 960 - o, 470], radius=40, fill=(90, 25, 45), outline=RED, width=6)
        T(dr, (590 - o, 395), "Human Blink: ~300ms", F(58), WHITE)
    if bi >= 1:
        o = sl(1)
        dr.rounded_rectangle([960 + o, 510, 1700 + o, 660], radius=40, fill=(15, 60, 80), outline=CY, width=6)
        T(dr, (1330 + o, 585), "AI Response: ~40ms", F(58), WHITE)
    if bi >= 2:
        dr.rounded_rectangle([420, 710, 1500, 830], radius=55, fill=(45, 34, 100), outline=PUR, width=6)
        T(dr, (960, 770), "140 TRILLION MATH CALCULATIONS PER WORD", fit("140 TRILLION MATH CALCULATIONS PER WORD", 48, 1000), WHITE)
    if bi >= 3:
        T(dr, (W / 2, 900), "The honest engineering behind real-time AI", F(48), YEL)

def draw_verdict(img, bi, tb):
    dr = ImageDraw.Draw(img)
    T(dr, (W / 2, 150), "THE VERDICT", F(64), CY)
    T(dr, (W / 2, 380), "NOT STORED. CALCULATED.", F(int(84 * (0.85 + 0.15 * ease(tb / 0.4)))), GRN)
    
    cx, cy = W / 2, 590
    r = 110
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(20, 70, 55), outline=GRN, width=8)
    dr.line([(cx - 50, cy + 5), (cx - 15, cy + 45), (cx + 55, cy - 40)], fill=GRN, width=20, joint="curve")
    
    if bi >= 1:
        T(dr, (W / 2, 790), "Every word is synthesized live across thousands of tensor cores.", F(56), WHITE)
        T(dr, (W / 2, 870), "Understanding the hardware makes you a better builder.", F(56), YEL)

def draw_intro(img, tb):
    dr = ImageDraw.Draw(img)
    s = ease(tb / 0.5)
    r = int(130 * s)
    dr.ellipse([W / 2 - r, 330 - r, W / 2 + r, 330 + r], fill=PUR)
    r2 = max(r - 16, 1)
    dr.ellipse([W / 2 - r2, 330 - r2, W / 2 + r2, 330 + r2], fill=(20, 14, 50))
    T(dr, (W / 2, 330), "TXK", F(int(74 * s)), WHITE)
    T(dr, (W / 2, 600), "TechXKenil", F(150), WHITE)
    if tb > 1.0:
        T(dr, (W / 2, 720), "AI  •  TECH  •  CODE", F(52), CY)

def draw_outro(img, tb):
    dr = ImageDraw.Draw(img)
    T(dr, (W / 2, 330), "TechXKenil", F(150), WHITE)
    T(dr, (W / 2, 440), "AI  •  TECH  •  CODE", F(52), CY)
    if tb > 0.7:
        s = ease((tb - 0.7) / 0.4) * (1 + 0.04 * math.sin(tb * 7))
        w, h = int(760 * s), int(180 * s)
        dr.rounded_rectangle([W / 2 - w / 2, 680 - h / 2, W / 2 + w / 2, 680 + h / 2], radius=h // 2, fill=(255, 30, 50))
        if s > 0.8:
            T(dr, (W / 2, 680), "SUBSCRIBE", F(96), WHITE)

CF = F(40)

def captions(text, dur):
    words = text.split()
    chunks = []
    cur = []
    for w in words:
        t = " ".join(cur + [w])
        if cur and (DUM.textlength(t.upper(), font=CF) > 1400 or len(cur) >= 9):
            chunks.append(cur)
            cur = [w]
        else:
            cur.append(w)
    chunks.append(cur)
    tot = sum(len(w) for w in words)
    tw = dur - 0.2
    res = []
    t = 0
    for ch in chunks:
        L = sum(len(w) for w in ch) / tot * tw
        res.append((t, t + L, " ".join(ch)))
        t += L
    return res

os.makedirs("youtube/videos", exist_ok=True)
out_file = "youtube/videos/how_ai_answers_in_milliseconds.mp4"
tl = json.load(open("tl_ms.json"))

print(f"Starting render of {out_file} at {W}x{H} @ {FPS}fps...")

ff = subprocess.Popen([
    "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
    "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", "audio_ms.wav",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out_file
], stdin=subprocess.PIPE)

start = 0.0
total_frames = sum(round(sum(bd) * FPS) for bd in tl)
rendered_frames = 0

for sc_idx, (sc, bd) in enumerate(zip(SCENES, tl)):
    end = start + sum(bd)
    f0, f1 = round(start * FPS), round(end * FPS)
    cum = [0]
    for x in bd:
        cum.append(cum[-1] + x)
    caps = [captions(b[0], bd[i]) for i, b in enumerate(sc["beats"])]
    
    for f in range(f0, f1):
        t = min(max(f / FPS - start, 0), cum[-1] - 1e-6)
        bi = max(i for i in range(len(bd)) if cum[i] <= t)
        tb = t - cum[bi]
        img = bg.copy()
        k = sc["kind"]
        if k not in ("intro", "outro"):
            T(ImageDraw.Draw(img), (70, 55), "TechXKenil", F(36), (160, 170, 210), "lm")
        
        if k == "list":
            draw_list(img, sc, bi, tb)
        elif k == "hook":
            draw_hook(img, bi, tb)
        elif k == "verdict":
            draw_verdict(img, bi, tb)
        elif k == "intro":
            draw_intro(img, tb)
        else:
            draw_outro(img, tb)
        
        for a, b, s in caps[bi]:
            if a <= tb < b + 0.05:
                T(ImageDraw.Draw(img), (W / 2, 1010), s.upper(), CF, WHITE, "mm", 5)
                break
        
        ff.stdin.write(img.tobytes())
        rendered_frames += 1
    
    pct = round((rendered_frames / total_frames) * 100, 1)
    print(f"  Rendered scene {sc_idx + 1}/{len(SCENES)}: {sc['name']} ({pct}%)")
    start = end

ff.stdin.close()
ff.wait()
print(f"Rendering complete! Output saved to: {out_file}")

