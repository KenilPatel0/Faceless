# render_higgsfield.py
# TechXKenil: Faceless Video Production Renderer for Open Higgsfield AI Tutorial
# Covers: Mac & Windows Setup, Links in Description, Real App Footage from GitHub
# Format: 1920x1080, 24 FPS, Kokoro TTS, MacBook Pro Mockup + Recordly/Screen Studio Cursors

import json
import math
import subprocess
import os
import sys
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from data_higgsfield import SCENES

W, H, FPS = 1920, 1080, 24

# Locate Inter Display Bold
for _fp in [
    os.path.join(REPO_ROOT, "fonts", "InterDisplay-Bold.otf"),
    "fonts/InterDisplay-Bold.otf",
    os.path.expanduser("~/Library/Fonts/InterDisplay-Bold.otf"),
    "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf",
]:
    if os.path.exists(_fp):
        FB = _fp
        break
else:
    FB = os.path.join(REPO_ROOT, "fonts", "InterDisplay-Bold.otf")

@lru_cache(None)
def F(s):
    return ImageFont.truetype(FB, max(int(s), 1))

# TechXKenil Color Palette
WHITE = (255, 255, 255)
DIM = (185, 192, 225)
RED = (255, 70, 90)
CY = (70, 220, 255)
YEL = (255, 205, 70)
GRN = (90, 235, 150)
PUR = (150, 110, 255)
DARK_PURPLE = (30, 26, 70)
CYAN_CARD = (15, 60, 80)
ACC = {"G": GRN, "R": RED, "Y": YEL, "C": CY, "P": PUR}

# Base background canvas: vertical gradient + 90px subtle grid
bg = Image.new("RGB", (W, H))
d = ImageDraw.Draw(bg)
for y in range(H):
    t = y / H
    c = tuple(int((8, 12, 28)[i] + ((30, 16, 70)[i] - (8, 12, 28)[i]) * t) for i in range(3))
    d.line([(0, y), (W, y)], fill=c)
for x in range(0, W, 90):
    d.line([(x, 0), (x, H)], fill=(22, 28, 58))
for y in range(0, H, 90):
    d.line([(0, y), (W, y)], fill=(22, 28, 58))

DUM = ImageDraw.Draw(Image.new("RGB", (4, 4)))

def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3

def ease_in_out(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)

def T(dr, xy, s, f, fill, a="mm", st=0):
    dr.text(xy, s, font=f, fill=fill, anchor=a, stroke_width=st, stroke_fill=(0, 0, 0))

def fit(s, size, maxw):
    while size > 20 and DUM.textlength(s, font=F(size)) > maxw:
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

# -------------------------------------------------------------
# Recordly Cursor & Click Ripple Drawer
# -------------------------------------------------------------
def draw_cursor(dr, cx, cy, click_progress=-1.0):
    if 0.0 <= click_progress <= 0.45:
        p = click_progress / 0.45
        r = int(6 + 28 * p)
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(70, 220, 255), width=3)
        if p < 0.6:
            r2 = max(int(r - 8), 1)
            dr.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=(150, 110, 255), width=2)
            
    pts = [
        (cx, cy),
        (cx, cy + 24),
        (cx + 6, cy + 18),
        (cx + 13, cy + 30),
        (cx + 17, cy + 28),
        (cx + 10, cy + 17),
        (cx + 18, cy + 17)
    ]
    shadow = [(x + 2, y + 2) for x, y in pts]
    dr.polygon(shadow, fill=(0, 0, 0))
    dr.polygon(pts, fill=(255, 255, 255), outline=(22, 24, 30))

# -------------------------------------------------------------
# Realistic MacBook Pro Mockup Shell
# -------------------------------------------------------------
MX0, MY0, MX1, MY1 = 250, 105, 1670, 855
DX0, DY0, DX1, DY1 = 276, 132, 1644, 828

def draw_macbook_base(dr, title="Open Higgsfield AI — Studio"):
    dr.rounded_rectangle([MX0, MY0, MX1, MY1], radius=24, fill=(45, 48, 56), outline=(68, 72, 84), width=2)
    dr.rounded_rectangle([DX0 - 10, DY0 - 10, DX1 + 10, DY1 + 10], radius=14, fill=(12, 14, 18))
    dr.rounded_rectangle([960 - 68, DY0 - 10, 960 + 68, DY0 + 14], radius=6, fill=(12, 14, 18))
    dr.ellipse([960 - 4, DY0 - 1, 960 + 4, DY0 + 7], fill=(28, 34, 46))
    
    dr.rounded_rectangle([200, MY1, 1720, MY1 + 20], radius=8, fill=(36, 39, 46), outline=(55, 58, 68), width=1)
    dr.rounded_rectangle([960 - 65, MY1, 960 + 65, MY1 + 7], radius=4, fill=(20, 22, 26))
    
    dr.rectangle([DX0, DY0, DX1, DY1], fill=(18, 20, 28))
    dr.rectangle([DX0, DY0, DX1, DY0 + 36], fill=(26, 29, 38))
    
    dr.ellipse([DX0 + 20, DY0 + 12, DX0 + 32, DY0 + 24], fill=(255, 95, 87))
    dr.ellipse([DX0 + 40, DY0 + 12, DX0 + 52, DY0 + 24], fill=(254, 188, 46))
    dr.ellipse([DX0 + 60, DY0 + 12, DX0 + 72, DY0 + 24], fill=(40, 201, 64))
    
    T(dr, (960, DY0 + 18), title, F(18), (170, 180, 210))
    dr.line([(DX0, DY0 + 36), (DX1, DY0 + 36)], fill=(38, 42, 54), width=1)

def draw_heading(dr, sc_heading, accent_col):
    text_w = DUM.textlength(sc_heading, font=F(28))
    pw = int(text_w / 2) + 24
    dr.rounded_rectangle([960 - pw, 32, 960 + pw, 78], radius=23, fill=(18, 22, 36), outline=accent_col, width=2)
    T(dr, (960, 55), sc_heading, F(26), accent_col, "mm")

def draw_desc_pill(dr, text="Links in description below ↓", col=CY):
    text_w = DUM.textlength(text, font=F(20))
    pw = int(text_w / 2) + 18
    dr.rounded_rectangle([960 - pw, 810, 960 + pw, 846], radius=18, fill=(15, 30, 48), outline=col, width=2)
    T(dr, (960, 828), text, F(18), col, "mm")

# -------------------------------------------------------------
# SCENE 1: HOOK
# -------------------------------------------------------------
def draw_hook(img, bi, tb):
    dr = ImageDraw.Draw(img)
    draw_heading(dr, "Open Higgsfield AI", CY)
    draw_macbook_base(dr, "Safari — github.com/Anil-matcha/Open-Higgsfield-AI")
    
    top_y = DY0 + 36
    dr.rectangle([DX0, top_y, DX1, DY1], fill=(14, 16, 24))
    
    T(dr, (960, top_y + 80), "THE OPEN-SOURCE HIGGSFIELD AI", F(44), WHITE)
    T(dr, (960, top_y + 130), "Cinematic Video Generation • Mac & Windows Studio • Zero Subscriptions", F(24), DIM)
    
    dr.rounded_rectangle([500, top_y + 175, 1420, top_y + 335], radius=16, fill=(24, 28, 42), outline=CY, width=3)
    dr.rectangle([500, top_y + 175, 520, top_y + 335], fill=CY)
    T(dr, (545, top_y + 220), "github.com / Anil-matcha / Open-Higgsfield-AI", F(28), WHITE, "lm")
    T(dr, (545, top_y + 270), "★ 4.8k Stars  •  MIT License  •  Native Mac (DMG) & Windows (EXE)", F(22), GRN, "lm")
    
    # Platform Badges
    dr.rounded_rectangle([500, top_y + 365, 800, top_y + 440], radius=12, fill=(18, 55, 75), outline=CY, width=2)
    T(dr, (650, top_y + 402), "macOS Native (DMG)", F(22), WHITE)
    
    dr.rounded_rectangle([820, top_y + 365, 1120, top_y + 440], radius=12, fill=(40, 25, 70), outline=PUR, width=2)
    T(dr, (970, top_y + 402), "Windows 10/11 (EXE)", F(22), WHITE)
    
    dr.rounded_rectangle([1140, top_y + 365, 1420, top_y + 440], radius=12, fill=(20, 65, 45), outline=GRN, width=2)
    T(dr, (1280, top_y + 402), "100% Free / MIT", F(22), WHITE)
    
    btn_box = [800, top_y + 475, 1120, top_y + 535]
    dr.rounded_rectangle(btn_box, radius=12, fill=PUR, outline=WHITE, width=2)
    T(dr, (960, top_y + 505), "DOWNLOAD NOW →", F(22), WHITE)
    
    # "Links in description" callout
    draw_desc_pill(dr, "Links & commands in description below ↓", YEL)
    
    move_t = min(tb / 1.8, 1.0)
    e = ease_in_out(move_t)
    cur_x = int(1200 + (960 - 1200) * e)
    cur_y = int(top_y + 560 + (505 - 560) * e)
    click_p = tb - 1.8 if tb >= 1.8 else -1.0
    draw_cursor(dr, cur_x, cur_y, click_p)

# -------------------------------------------------------------
# SCENE 2: INTRO (Official TechXKenil Brand Intro)
# -------------------------------------------------------------
def draw_intro(img, tb):
    dr = ImageDraw.Draw(img)
    s = ease(tb / 0.5)
    r = int(130 * s)
    dr.ellipse([W/2 - r, 330 - r, W/2 + r, 330 + r], fill=PUR)
    r2 = max(r - 16, 1)
    dr.ellipse([W/2 - r2, 330 - r2, W/2 + r2, 330 + r2], fill=(20, 14, 50))
    T(dr, (W/2, 330), "TXK", F(int(74 * s)), WHITE)
    T(dr, (W/2, 600), "TechXKenil", F(150), WHITE)
    if tb > 1.0:
        T(dr, (W/2, 720), "AI  •  TECH  •  CODE", F(52), CY)

# -------------------------------------------------------------
# SCENE 3: MULTIPLATFORM INSTALLATION (Mac & Windows)
# -------------------------------------------------------------
def draw_install(img, bi, tb):
    dr = ImageDraw.Draw(img)
    draw_heading(dr, "1. Download & Installation (Mac & Windows)", CY)
    
    top_y = DY0 + 36
    
    if bi <= 1:
        # Multiplatform Download Cards: Apple Silicon, Intel Mac, and Windows PC
        draw_macbook_base(dr, "GitHub Releases — Open Higgsfield AI v1.0.0")
        dr.rectangle([DX0, top_y, DX1, DY1], fill=(16, 18, 26))
        
        # Header banner
        dr.rounded_rectangle([320, top_y + 25, 1600, top_y + 105], radius=12, fill=(24, 28, 40), outline=(50, 56, 80), width=2)
        T(dr, (360, top_y + 50), "Open Higgsfield AI v1.0.0", F(26), WHITE, "lm")
        dr.rounded_rectangle([760, top_y + 38, 860, top_y + 64], radius=6, fill=GRN)
        T(dr, (810, top_y + 51), "Latest", F(16), (10, 20, 10))
        T(dr, (360, top_y + 82), "Standalone packages for macOS (Apple Silicon & Intel) and Windows PC", F(18), DIM, "lm")
        
        # 3 Side-by-Side Platform Cards
        card_w = 380
        # Card 1: Apple Silicon Mac (M1-M4)
        c1_x = 340
        dr.rounded_rectangle([c1_x, top_y + 130, c1_x + card_w, top_y + 490], radius=16, fill=(20, 48, 68), outline=CY, width=3)
        dr.rounded_rectangle([c1_x + card_w//2 - 45, top_y + 185 - 28, c1_x + card_w//2 + 45, top_y + 185 + 28], radius=10, fill=CY)
        T(dr, (c1_x + card_w//2, top_y + 185), "M1-M4", F(24), (10, 25, 35))
        T(dr, (c1_x + card_w//2, top_y + 250), "Apple Silicon Mac", F(24), WHITE)
        T(dr, (c1_x + card_w//2, top_y + 285), "M1, M2, M3, M4 Chips", F(18), DIM)
        T(dr, (c1_x + card_w//2, top_y + 340), "Open-Higgsfield-AI-arm64.dmg", F(17), CY)
        dr.rounded_rectangle([c1_x + 60, top_y + 400, c1_x + card_w - 60, top_y + 455], radius=10, fill=CY)
        T(dr, (c1_x + card_w//2, top_y + 428), "Download DMG", F(19), (10, 25, 35))
        
        # Card 2: Intel Mac
        c2_x = 760
        dr.rounded_rectangle([c2_x, top_y + 130, c2_x + card_w, top_y + 490], radius=16, fill=(24, 28, 42), outline=(60, 68, 95), width=1)
        dr.rounded_rectangle([c2_x + card_w//2 - 45, top_y + 185 - 28, c2_x + card_w//2 + 45, top_y + 185 + 28], radius=10, fill=(70, 80, 110))
        T(dr, (c2_x + card_w//2, top_y + 185), "INTEL", F(22), WHITE)
        T(dr, (c2_x + card_w//2, top_y + 250), "Intel x64 Mac", F(24), WHITE)
        T(dr, (c2_x + card_w//2, top_y + 285), "Older Intel Hardware", F(18), DIM)
        T(dr, (c2_x + card_w//2, top_y + 340), "Open-Higgsfield-AI.dmg", F(17), DIM)
        dr.rounded_rectangle([c2_x + 60, top_y + 400, c2_x + card_w - 60, top_y + 455], radius=10, fill=(45, 50, 70))
        T(dr, (c2_x + card_w//2, top_y + 428), "Download DMG", F(19), DIM)
        
        # Card 3: Windows PC
        c3_x = 1180
        dr.rounded_rectangle([c3_x, top_y + 130, c3_x + card_w, top_y + 490], radius=16, fill=(35, 25, 60), outline=PUR, width=3)
        dr.rounded_rectangle([c3_x + card_w//2 - 45, top_y + 185 - 28, c3_x + card_w//2 + 45, top_y + 185 + 28], radius=10, fill=PUR)
        T(dr, (c3_x + card_w//2, top_y + 185), "WIN", F(22), WHITE)
        T(dr, (c3_x + card_w//2, top_y + 250), "Windows 10 / 11", F(24), WHITE)
        T(dr, (c3_x + card_w//2, top_y + 285), "64-bit Installer", F(18), DIM)
        T(dr, (c3_x + card_w//2, top_y + 340), "Open-Higgsfield-AI-Setup.exe", F(17), PUR)
        dr.rounded_rectangle([c3_x + 60, top_y + 400, c3_x + card_w - 60, top_y + 455], radius=10, fill=PUR)
        T(dr, (c3_x + card_w//2, top_y + 428), "Download EXE", F(19), WHITE)
        
        draw_desc_pill(dr, "Direct download links are in the description below ↓", CY)
        
        move_t = min(tb / 2.0, 1.0)
        e = ease_in_out(move_t)
        cur_x = int(530 + (1370 - 530) * e)
        cur_y = int(top_y + 428)
        click_p = tb - 2.0 if tb >= 2.0 else -1.0
        draw_cursor(dr, cur_x, cur_y, click_p)
        
    elif bi == 2:
        # macOS Gatekeeper Terminal Fix
        draw_macbook_base(dr, "macOS Terminal — Gatekeeper Unquarantine Fix")
        dr.rectangle([DX0, top_y, DX1, DY1], fill=(12, 14, 20))
        
        dr.rounded_rectangle([340, top_y + 50, 1580, top_y + 460], radius=14, fill=(18, 20, 30), outline=CY, width=2)
        T(dr, (380, top_y + 90), "macOS Gatekeeper Fix (Run once in Terminal):", F(22), DIM, "lm")
        
        cmd = 'xattr -cr "/Applications/Open Higgsfield AI.app"'
        char_count = int(min(len(cmd), max(0, (tb - 0.4) * 16)))
        typed_cmd = cmd[:char_count]
        
        T(dr, (380, top_y + 155), "kenil@MacBook-Pro ~ %", F(26), GRN, "lm")
        T(dr, (700, top_y + 155), typed_cmd, F(26), WHITE, "lm")
        
        if (int(tb * 3) % 2) == 0:
            cx_pos = 700 + int(DUM.textlength(typed_cmd, font=F(26))) + 4
            dr.rectangle([cx_pos, top_y + 140, cx_pos + 12, top_y + 170], fill=CY)
            
        if tb >= 2.8:
            dr.rounded_rectangle([380, top_y + 225, 1540, top_y + 345], radius=10, fill=(20, 50, 40), outline=GRN, width=2)
            T(dr, (410, top_y + 265), "✓ macOS Gatekeeper quarantine cleared!", F(26), GRN, "lm")
            T(dr, (410, top_y + 305), "App is verified. Click Open to launch without security prompts.", F(22), WHITE, "lm")
            
        draw_desc_pill(dr, "Terminal command is in the description below ↓", CY)
        draw_cursor(dr, 960, top_y + 400, tb - 2.8 if tb >= 2.8 else -1.0)
        
    else:
        # Windows Defender SmartScreen Bypass
        draw_macbook_base(dr, "Windows 11 — Defender SmartScreen Setup")
        dr.rectangle([DX0, top_y, DX1, DY1], fill=(20, 24, 38))
        
        # Windows SmartScreen Dialog Box
        dr.rounded_rectangle([500, top_y + 60, 1420, top_y + 470], radius=16, fill=(24, 32, 54), outline=PUR, width=3)
        
        # Windows Blue Accent Top Bar
        dr.rounded_rectangle([520, top_y + 80, 1400, top_y + 150], radius=10, fill=(0, 120, 215))
        T(dr, (550, top_y + 115), "Windows protected your PC", F(28), WHITE, "lm")
        
        T(dr, (550, top_y + 190), "Microsoft Defender SmartScreen prevented an unrecognized app from starting.", F(22), WHITE, "lm")
        T(dr, (550, top_y + 230), "Because this is community open-source, Windows displays this one-time alert.", F(20), DIM, "lm")
        
        # Steps inside dialog
        dr.rounded_rectangle([550, top_y + 270, 1370, top_y + 350], radius=10, fill=(18, 22, 38), outline=(60, 70, 100))
        T(dr, (580, top_y + 310), "Step 1: Click 'More info'   →   Step 2: Click 'Run anyway'", F(22), YEL, "lm")
        
        # Run Anyway Button
        dr.rounded_rectangle([1060, top_y + 380, 1370, top_y + 440], radius=8, fill=PUR)
        T(dr, (1215, top_y + 410), "Run anyway", F(22), WHITE)
        
        # Don't Run Button
        dr.rounded_rectangle([720, top_y + 380, 1020, top_y + 440], radius=8, fill=(45, 52, 75))
        T(dr, (870, top_y + 410), "Don't run", F(22), DIM)
        
        draw_desc_pill(dr, "Windows setup guide is in the description below ↓", PUR)
        
        move_t = min(tb / 1.8, 1.0)
        e = ease_in_out(move_t)
        cur_x = int(870 + (1215 - 870) * e)
        cur_y = int(top_y + 410)
        click_p = tb - 1.8 if tb >= 1.8 else -1.0
        draw_cursor(dr, cur_x, cur_y, click_p)

# -------------------------------------------------------------
# SCENE 4: SETUP & LOCAL ARCHITECTURE
# -------------------------------------------------------------
def draw_setup(img, bi, tb):
    dr = ImageDraw.Draw(img)
    draw_heading(dr, "2. Setup & Configuration", GRN)
    draw_macbook_base(dr, "Open Higgsfield AI — Local Dashboard")
    
    top_y = DY0 + 36
    dr.rectangle([DX0, top_y, DX1, DY1], fill=(16, 18, 26))
    
    # Left Sidebar
    dr.rectangle([DX0, top_y, DX0 + 260, DY1], fill=(22, 25, 36))
    dr.line([(DX0 + 260, top_y), (DX0 + 260, DY1)], fill=(36, 40, 54), width=1)
    
    T(dr, (DX0 + 40, top_y + 40), "OH", F(28), PUR, "lm")
    T(dr, (DX0 + 90, top_y + 40), "Higgsfield AI", F(22), WHITE, "lm")
    
    navs = [
        ("[ VIDEO STUDIO ]", True),
        ("[ IMAGE STUDIO ]", False),
        ("[ CINEMA MODE ]", False),
        ("[ LIP SYNC ]", False),
    ]
    for i, (name, act) in enumerate(navs):
        ny = top_y + 100 + i * 55
        if act:
            dr.rounded_rectangle([DX0 + 15, ny - 20, DX0 + 245, ny + 20], radius=8, fill=(35, 45, 75), outline=CY, width=1)
        T(dr, (DX0 + 35, ny), name, F(20), CY if act else DIM, "lm")
        
    dr.rounded_rectangle([DX0 + 15, DY1 - 65, DX0 + 245, DY1 - 25], radius=8, fill=(30, 34, 48), outline=GRN if bi >= 2 else (50, 55, 75))
    T(dr, (DX0 + 35, DY1 - 45), "[ SETTINGS ]", F(20), GRN if bi >= 2 else WHITE, "lm")
    
    content_x = DX0 + 280
    if bi <= 1:
        T(dr, (content_x + 30, top_y + 60), "Local-First Architecture (BYOK)", F(32), WHITE, "lm")
        T(dr, (content_x + 30, top_y + 105), "Run models directly via your own API or local ComfyUI instance.", F(22), DIM, "lm")
        
        dr.rounded_rectangle([content_x + 30, top_y + 160, content_x + 480, top_y + 480], radius=16, fill=(28, 22, 35), outline=RED, width=2)
        T(dr, (content_x + 255, top_y + 220), "Commercial Middlemen", F(26), RED)
        T(dr, (content_x + 255, top_y + 280), "• $30-$50 monthly fee", F(22), DIM)
        T(dr, (content_x + 255, top_y + 325), "• Strict queue limits", F(22), DIM)
        T(dr, (content_x + 255, top_y + 370), "• Closed platform lock", F(22), DIM)
        
        dr.rounded_rectangle([content_x + 520, top_y + 160, content_x + 980, top_y + 480], radius=16, fill=(20, 45, 38), outline=GRN, width=3)
        T(dr, (content_x + 750, top_y + 220), "Open Higgsfield (Local-First)", F(26), GRN)
        T(dr, (content_x + 750, top_y + 280), "• 100% Free Software", F(22), WHITE)
        T(dr, (content_x + 750, top_y + 325), "• Bring Your Own Key (BYOK)", F(22), WHITE)
        T(dr, (content_x + 750, top_y + 370), "• Or run local ComfyUI free", F(22), WHITE)
        
    else:
        T(dr, (content_x + 30, top_y + 50), "Configure API & Engine", F(32), WHITE, "lm")
        dr.rounded_rectangle([content_x + 30, top_y + 90, content_x + 980, top_y + 530], radius=16, fill=(24, 28, 40), outline=GRN, width=2)
        
        T(dr, (content_x + 60, top_y + 140), "Select Generation Provider:", F(22), DIM, "lm")
        dr.rounded_rectangle([content_x + 60, top_y + 165, content_x + 950, top_y + 225], radius=10, fill=(18, 20, 30), outline=(50, 56, 75))
        T(dr, (content_x + 85, top_y + 195), "Muapi.ai  /  Google Vertex  /  Local ComfyUI", F(22), CY, "lm")
        
        T(dr, (content_x + 60, top_y + 265), "Provider API Key:", F(22), DIM, "lm")
        dr.rounded_rectangle([content_x + 60, top_y + 290, content_x + 950, top_y + 350], radius=10, fill=(18, 20, 30), outline=(50, 56, 75))
        key_chars = "••••••••••••••••••••••••••••••••••••"
        T(dr, (content_x + 85, top_y + 320), key_chars, F(22), WHITE, "lm")
        
        dr.rounded_rectangle([content_x + 60, top_y + 390, content_x + 500, top_y + 450], radius=10, fill=(20, 60, 45), outline=GRN, width=2)
        T(dr, (content_x + 280, top_y + 420), "● ENGINE CONNECTED", F(22), GRN)
            
        dr.rounded_rectangle([content_x + 720, top_y + 460, content_x + 950, top_y + 510], radius=10, fill=GRN)
        T(dr, (content_x + 835, top_y + 485), "Save & Connect", F(20), (10, 25, 15))
        
        cur_x = content_x + 835
        cur_y = top_y + 485
        draw_cursor(dr, cur_x, cur_y, tb - 2.0 if tb >= 2.0 else -1.0)

# -------------------------------------------------------------
# SCENE 5: REAL APP DEMO (Compositing Real Open-Higgsfield Video)
# -------------------------------------------------------------
TOTAL_DEMO_FRAMES = 448

frames_dir = os.path.join(SCRIPT_DIR, "real_demo_frames")
media_path = os.path.join(REPO_ROOT, "media", "higgsfield_demo.mp4")
if not os.path.exists(media_path) and os.path.exists("media/higgsfield_demo.mp4"):
    media_path = "media/higgsfield_demo.mp4"

if not os.path.exists(frames_dir) and os.path.exists(media_path):
    os.makedirs(frames_dir, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-y", "-i", media_path,
        "-r", "24", "-s", "1360x656",
        os.path.join(frames_dir, "frame_%04d.png")
    ], capture_output=True)

@lru_cache(maxsize=128)
def get_real_demo_frame(frame_num):
    fn = os.path.join(frames_dir, f"frame_{frame_num:04d}.png")
    if os.path.exists(fn):
        return Image.open(fn)
    return None

def draw_example(img, bi, tb, dur):
    dr = ImageDraw.Draw(img)
    draw_heading(dr, "3. Hands-On Real App Demo", PUR)
    draw_macbook_base(dr, "Open-Higgsfield AI — Live App on localhost:5173")
    
    top_y = DY0 + 36
    
    # Calculate exact synchronized real demo frame based on the active beat
    dur = max(dur, 0.1)
    progress = min(max(tb / dur, 0.0), 1.0)
    
    if bi == 0:
        # Beat 0: Model selector (Frames 1..106)
        frame_no = int(1 + 105 * progress)
    elif bi == 1:
        # Beat 1: Prompt description (Frames 107..211)
        frame_no = int(107 + 104 * progress)
    elif bi == 2:
        # Beat 2: Aspect ratio (Frames 212..317)
        frame_no = int(212 + 105 * progress)
    else:
        # Beat 3: Generating & Real High-Res Output (Frames 318..446)
        frame_no = int(318 + 128 * progress)
        
    frame_no = max(1, min(frame_no, TOTAL_DEMO_FRAMES))
    demo_img = get_real_demo_frame(frame_no)
    
    if demo_img:
        img.paste(demo_img, (DX0 + 4, top_y + 2))
    else:
        dr.rectangle([DX0, top_y, DX1, DY1], fill=(14, 16, 24))
        
    dr = ImageDraw.Draw(img)
    if bi == 0:
        dr.rounded_rectangle([DX0 + 30, top_y + 20, DX0 + 480, top_y + 70], radius=8, fill=(15, 20, 35), outline=CY, width=2)
        T(dr, (DX0 + 255, top_y + 45), "Model: Flux Dev / Nano Banana Pro", F(20), CY)
        draw_cursor(dr, DX0 + 260, top_y + 200, tb - 1.5 if tb >= 1.5 else -1.0)
        
    elif bi == 1:
        dr.rounded_rectangle([DX0 + 30, top_y + 20, DX0 + 520, top_y + 70], radius=8, fill=(15, 20, 35), outline=YEL, width=2)
        T(dr, (DX0 + 275, top_y + 45), "Prompt: Atmospheric Cinematic Scene", F(20), YEL)
        draw_cursor(dr, DX0 + 600, top_y + 420, tb - 1.8 if tb >= 1.8 else -1.0)
        
    elif bi == 2:
        dr.rounded_rectangle([DX0 + 30, top_y + 20, DX0 + 420, top_y + 70], radius=8, fill=(15, 20, 35), outline=PUR, width=2)
        T(dr, (DX0 + 225, top_y + 45), "Aspect Ratio: 1:1 / 16:9 / 9:16", F(20), PUR)
        draw_cursor(dr, DX0 + 460, top_y + 580, tb - 1.5 if tb >= 1.5 else -1.0)
        
    else:
        dr.rounded_rectangle([DX0 + 30, top_y + 20, DX0 + 480, top_y + 70], radius=8, fill=(15, 30, 25), outline=GRN, width=2)
        T(dr, (DX0 + 255, top_y + 45), "✓ Real Generated Cinematic Output", F(20), GRN)
        draw_cursor(dr, DX0 + 680, top_y + 580, tb - 2.0 if tb >= 2.0 else -1.0)

# -------------------------------------------------------------
# SCENE 6: THE HONEST VERDICT
# -------------------------------------------------------------
def draw_verdict(img, bi, tb):
    dr = ImageDraw.Draw(img)
    draw_heading(dr, "4. The Honest Verdict", YEL)
    draw_macbook_base(dr, "Open Higgsfield AI — Verdict & Reality Check")
    
    top_y = DY0 + 36
    dr.rectangle([DX0, top_y, DX1, DY1], fill=(16, 18, 26))
    
    card_w = 600
    # Commercial Card
    dr.rounded_rectangle([330, top_y + 40, 330 + card_w, top_y + 440], radius=16, fill=(28, 20, 30), outline=RED, width=3)
    dr.ellipse([630 - 30, top_y + 90 - 30, 630 + 30, top_y + 90 + 30], fill=RED)
    dr.line([(630 - 16, top_y + 90 - 16), (630 + 16, top_y + 90 + 16)], fill=WHITE, width=5)
    dr.line([(630 - 16, top_y + 90 + 16), (630 + 16, top_y + 90 - 16)], fill=WHITE, width=5)
    T(dr, (630, top_y + 150), "Commercial Higgsfield", F(28), RED)
    
    T(dr, (380, top_y + 220), "• $30 to $50/month subscription", F(24), DIM, "lm")
    T(dr, (380, top_y + 275), "• Strict queue limits and wait times", F(24), DIM, "lm")
    T(dr, (380, top_y + 330), "• Closed ecosystem lock-in", F(24), DIM, "lm")
    T(dr, (380, top_y + 385), "• Expensive long-term cost", F(24), DIM, "lm")
    
    # Open Higgsfield Card
    dr.rounded_rectangle([990, top_y + 40, 990 + card_w, top_y + 440], radius=16, fill=(18, 40, 32), outline=GRN, width=3)
    dr.ellipse([1290 - 30, top_y + 90 - 30, 1290 + 30, top_y + 90 + 30], fill=GRN)
    dr.line([(1290 - 18, top_y + 90), (1290 - 5, top_y + 90 + 14), (1290 + 18, top_y + 90 - 14)], fill=(10, 30, 15), width=6)
    T(dr, (1290, top_y + 150), "Open Higgsfield AI", F(28), GRN)
    
    T(dr, (1040, top_y + 220), "• 100% Free & Open Source (MIT)", F(24), WHITE, "lm")
    T(dr, (1040, top_y + 275), "• Works on Mac (DMG) & Windows (EXE)", F(24), WHITE, "lm")
    T(dr, (1040, top_y + 330), "• Pay pennies for compute or run local", F(24), WHITE, "lm")
    T(dr, (1040, top_y + 385), "• Exact same multi-model creative suite", F(24), WHITE, "lm")
    
    dr.rounded_rectangle([450, top_y + 480, 1470, top_y + 545], radius=12, fill=(25, 30, 48), outline=CY, width=2)
    T(dr, (960, top_y + 512), "Zero Subscription Locks  •  Full Creative Ownership", F(26), CY)

# -------------------------------------------------------------
# SCENE 7: OUTRO (Official TechXKenil Brand Outro)
# -------------------------------------------------------------
def draw_outro(img, tb):
    dr = ImageDraw.Draw(img)
    T(dr, (W/2, 310), "TechXKenil", F(150), WHITE)
    T(dr, (W/2, 420), "AI  •  TECH  •  CODE", F(52), CY)
    
    draw_desc_pill(dr, "All links and commands are in the description below ↓", YEL)
    
    if tb > 0.7:
        s = ease((tb - 0.7) / 0.4) * (1 + 0.04 * math.sin(tb * 7))
        w, h = int(760 * s), int(180 * s)
        dr.rounded_rectangle([W/2 - w/2, 660 - h/2, W/2 + w/2, 660 + h/2], radius=h//2, fill=(255, 30, 50))
        if s > 0.8:
            T(dr, (W/2, 660), "SUBSCRIBE", F(96), WHITE)

# -------------------------------------------------------------
# CAPTIONS ENGINE (Long format: size 40, stroke 5, at y=1010)
# -------------------------------------------------------------
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
    tw = max(dur - 0.2, 0.1)
    res = []
    t = 0
    for ch in chunks:
        L = (sum(len(w) for w in ch) / tot) * tw
        res.append((t, t + L, " ".join(ch)))
        t += L
    return res

# -------------------------------------------------------------
# MAIN RENDER LOOP & FFMPEG PIPE
# -------------------------------------------------------------
print("Loading timeline and starting render...")
tl_path = os.path.join(SCRIPT_DIR, "tl_higgsfield.json")
audio_path = os.path.join(SCRIPT_DIR, "audio_higgsfield.wav")
out_mp4 = os.path.join(SCRIPT_DIR, "techxkenil_higgsfield_ai.mp4")

tl = json.load(open(tl_path))

ff = subprocess.Popen([
    "ffmpeg", "-y", "-loglevel", "error",
    "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
    "-i", "-",
    "-i", audio_path,
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k",
    "-shortest", "-movflags", "+faststart",
    out_mp4
], stdin=subprocess.PIPE)

start = 0.0
total_scenes = len(SCENES)
frame_idx = 0
total_frames = int(sum(map(sum, tl)) * FPS)

for sc_idx, (sc, bd) in enumerate(zip(SCENES, tl)):
    end = start + sum(bd)
    f0, f1 = round(start * FPS), round(end * FPS)
    cum = [0]
    for x in bd:
        cum.append(cum[-1] + x)
    caps = [captions(b[0], bd[i]) for i, b in enumerate(sc["beats"])]
    
    print(f"Rendering scene {sc_idx + 1}/{total_scenes}: {sc['name']} (frames {f0}..{f1})")
    scene_frame_count = 0
    
    for f in range(f0, f1):
        frame_idx += 1
        scene_frame_count += 1
        t = min(max(f / FPS - start, 0), cum[-1] - 1e-6)
        bi = max(i for i in range(len(bd)) if cum[i] <= t)
        tb = t - cum[bi]
        
        img = bg.copy()
        k = sc["kind"]
        
        # Watermark on all scenes except intro/outro
        if k not in ("intro", "outro"):
            T(ImageDraw.Draw(img), (70, 55), "TechXKenil", F(36), (160, 170, 210), "lm")
            
        if k == "hook":
            draw_hook(img, bi, tb)
        elif k == "intro":
            draw_intro(img, tb)
        elif k == "install_multiplatform":
            draw_install(img, bi, tb)
        elif k == "setup_local":
            draw_setup(img, bi, tb)
        elif k == "real_app_demo":
            draw_example(img, bi, tb, bd[bi])
        elif k == "verdict_summary":
            draw_verdict(img, bi, tb)
        elif k == "outro":
            draw_outro(img, tb)
            
        # Draw burned-in subtitles at bottom center
        for a, b, s in caps[bi]:
            if a <= tb < b + 0.05:
                T(ImageDraw.Draw(img), (W/2, 1010), s.upper(), CF, WHITE, "mm", 5)
                break
                
        ff.stdin.write(img.tobytes())
    start = end

ff.stdin.close()
ff.wait()

vf_dir = os.path.join(REPO_ROOT, "VideoFiles")
if os.path.exists(vf_dir):
    vf_target = os.path.join(vf_dir, "techxkenil_higgsfield_ai.mp4")
    if os.path.islink(vf_target) or os.path.exists(vf_target):
        try:
            os.remove(vf_target)
        except OSError:
            pass
    try:
        rel_target = os.path.relpath(out_mp4, vf_dir)
        os.symlink(rel_target, vf_target)
    except OSError:
        pass

print(f"\nRender complete! Successfully created: {out_mp4}")
