#!/usr/bin/env python3
"""
generate_thumbnail.py — Automated High-CTR Thumbnail Generator for TechXKenil & Tech Channels.
Features:
- Free AI background generation (Pollinations Flux/SDXL with zero API keys)
- 100% Procedural fallback using TechXKenil brand gradient & tech grid
- Pixel-perfect typography overlay with Inter Display Bold
- Mobile-optimized readability (large text, high contrast, 3-element composition)
- YouTube Safe Zones (protects bottom-right timestamp badge area)
"""

import argparse
import os
import sys
import urllib.parse
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1280, 720  # Standard YouTube Thumbnail resolution (16:9)

# Colors matching TechXKenil design system
BG_DARK = (8, 12, 28)
BG_PURPLE = (30, 16, 70)
WHITE = (255, 255, 255)
CYAN = (70, 220, 255)
YELLOW = (255, 205, 70)
GREEN = (90, 235, 150)
RED = (255, 70, 90)
PURPLE = (150, 110, 255)

# Font resolution
FONT_PATHS = [
    "fonts/InterDisplay-Bold.otf",
    os.path.expanduser("~/Library/Fonts/InterDisplay-Bold.otf"),
    "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
]
FB = next((fp for fp in FONT_PATHS if os.path.exists(fp)), None)

def get_font(size):
    if FB and os.path.exists(FB):
        return ImageFont.truetype(FB, int(size))
    return ImageFont.load_default()

def create_procedural_background():
    """Generates the signature TechXKenil dark gradient and faint tech grid."""
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    # Vertical gradient
    for y in range(H):
        t = y / H
        col = tuple(int(BG_DARK[i] + (BG_PURPLE[i] - BG_DARK[i]) * t) for i in range(3))
        draw.line([(0, y), (W, y)], fill=col)
    
    # 90px tech grid
    for x in range(0, W, 80):
        draw.line([(x, 0), (x, H)], fill=(22, 28, 58))
    for y in range(0, H, 80):
        draw.line([(0, y), (W, y)], fill=(22, 28, 58))
        
    # Radial cyber glow in center-right
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for r in range(400, 50, -30):
        alpha = int(40 * (1 - r / 400))
        glow_draw.ellipse([850 - r, 360 - r, 850 + r, 360 + r], fill=(70, 220, 255, alpha))
    img.paste(glow, (0, 0), glow)
    return img

def fetch_ai_background(prompt):
    """Fetches a free Flux/SDXL AI background via Pollinations API (no key needed)."""
    clean_prompt = urllib.parse.quote(prompt + ", dark cyberpunk lighting, cinematic, 8k resolution, minimalist, clean background, no text")
    url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width={W}&height={H}&model=flux&nologo=true"
    print(f"Fetching AI artwork from free generator: {prompt[:50]}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=25) as response:
            ai_img = Image.open(response).convert("RGB")
            ai_img = ai_img.resize((W, H), Image.Resampling.LANCZOS)
            # Darken slightly so text pops
            darkener = Image.new("RGB", (W, H), (0, 0, 0))
            ai_img = Image.blend(ai_img, darkener, 0.35)
            return ai_img
    except Exception as e:
        print(f"Warning: AI fetch timed out or failed ({e}). Using procedural background.")
        return create_procedural_background()

def draw_pill(draw, xy, text, font, bg_color, text_color, border_color=None, padding=(24, 12)):
    """Draws a pill button with crisp centered text."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x, y = xy
    px, py = padding
    rect = [x, y, x + tw + px * 2, y + th + py * 2]
    radius = (th + py * 2) // 2
    draw.rounded_rectangle(rect, radius=radius, fill=bg_color, outline=border_color, width=4 if border_color else 0)
    draw.text((x + px, y + py - 2), text, font=font, fill=text_color)
    return rect

def generate_thumbnail(
    title_line1,
    title_line2=None,
    accent_badge="15 MILLISECONDS",
    sub_pill="140 TRILLION OPS",
    ai_prompt=None,
    output_path="thumbnail.png"
):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # 1. Background
    if ai_prompt:
        img = fetch_ai_background(ai_prompt)
    else:
        img = create_procedural_background()
        
    draw = ImageDraw.Draw(img)

    # 2. Top Kicker Badge
    if accent_badge:
        f_badge = get_font(30)
        draw_pill(draw, (70, 75), accent_badge.upper(), f_badge, (15, 60, 80), CYAN, CYAN, padding=(20, 8))

    # 3. Main Hook Headlines (Massive, high-retention text)
    f_title = get_font(96)
    
    # Shadow offset for max contrast
    def draw_stroked_text(xy, text, font, fill):
        x, y = xy
        # Dark heavy stroke
        for dx in [-4, 0, 4]:
            for dy in [-4, 0, 4]:
                draw.text((x + dx, y + dy), text, font=font, fill=(5, 8, 18))
        draw.text(xy, text, font=font, fill=fill)

    draw_stroked_text((70, 155), title_line1, f_title, WHITE)
    
    y_next = 275
    if title_line2:
        draw_stroked_text((70, y_next), title_line2, f_title, YELLOW)
        y_next += 120

    # 4. Stat Chip / Secondary Pill
    if sub_pill:
        f_pill = get_font(38)
        draw_pill(draw, (70, y_next + 20), sub_pill, f_pill, (50, 28, 100), WHITE, PURPLE, padding=(28, 14))

    # 5. Right Graphic Element (Stopwatch / Silicon Chip)
    # Draw high-tech stopwatch badge
    cx, cy = 960, 360
    r = 180
    
    # Outer glowing ring
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(14, 18, 40), outline=CYAN, width=8)
    draw.ellipse([cx - r + 16, cy - r + 16, cx + r - 16, cy + r - 16], fill=(22, 14, 55), outline=PURPLE, width=4)
    
    f_stopwatch = get_font(68)
    draw.text((cx, cy - 20), "15 ms", font=f_stopwatch, fill=WHITE, anchor="mm")
    
    f_sub = get_font(24)
    draw.text((cx, cy + 45), "RESPONSE TIME", font=f_sub, fill=CYAN, anchor="mm")

    # 6. Channel Tag (Top Right)
    f_brand = get_font(28)
    draw.text((W - 80, 80), "TechXKenil", font=f_brand, fill=(160, 170, 210), anchor="rm")

    # 7. Safe Zone check: YouTube duration badge occupies (1100, 660) to (1260, 700)
    # Ensure nothing critical is in bottom-right corner

    img.save(output_path, "PNG", quality=95)
    print(f"Thumbnail successfully generated: {output_path} ({W}x{H})")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate YouTube Thumbnail")
    parser.add_argument("--line1", default="HOW AI ANSWERS", help="Main headline line 1")
    parser.add_argument("--line2", default="IN MILLISECONDS", help="Main headline line 2")
    parser.add_argument("--badge", default="15 MILLISECONDS", help="Top kicker badge")
    parser.add_argument("--stat", default="140 TRILLION OPS", help="Stat pill callout")
    parser.add_argument("--ai", default=None, help="Prompt for free AI background")
    parser.add_argument("--out", default="thumbnail.png", help="Output path")
    args = parser.parse_args()

    generate_thumbnail(
        title_line1=args.line1,
        title_line2=args.line2,
        accent_badge=args.badge,
        sub_pill=args.stat,
        ai_prompt=args.ai,
        output_path=args.out
    )

