#!/usr/bin/env python3
"""
render_vertical.py — High-retention 15-second Vertical Short for TechXKenil:
Topic: "What is a Black Hole and How It Works"
Resolution: 1080x1920 @ 30 FPS
"""

import os
import sys
import json
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import (
    SS, spring, arc_point, draw_cursor, draw_karaoke,
    open_encoder, clamp, lerp
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(BASE_DIR, "..", "..", "fonts")
META_PATH = os.path.join(BASE_DIR, "black_hole_vertical_meta.json")
AUDIO_PATH = os.path.join(BASE_DIR, "black_hole_vertical_audio.wav")
OUT_MP4 = os.path.join(BASE_DIR, "black_hole_vertical_15s.mp4")

WIDTH, HEIGHT, FPS = 1080, 1920, 30

# TechXKenil Brand Palette
BG_TOP = (8, 12, 28)
BG_BOTTOM = (30, 16, 70)
GRID_COLOR = (22, 28, 58)
WHITE = (255, 255, 255)
DIM_TEXT = (185, 192, 225)
BRAND_COLOR = (160, 170, 210)
CYAN = (70, 220, 255)
PURPLE = (150, 110, 255)
YELLOW = (255, 205, 70)
ORANGE = (255, 150, 80)
GREEN = (90, 235, 150)
RED_SUB = (255, 30, 50)
DARK_CARD = (15, 20, 42)

# Typography
FONT_BRAND = ImageFont.truetype(os.path.join(FONTS_DIR, "InterDisplay-Bold.otf"), 46)
FONT_BADGE = ImageFont.truetype(os.path.join(FONTS_DIR, "InterDisplay-Bold.otf"), 34)
FONT_TITLE = ImageFont.truetype(os.path.join(FONTS_DIR, "InterDisplay-Bold.otf"), 66)
FONT_CARD_H = ImageFont.truetype(os.path.join(FONTS_DIR, "InterDisplay-Bold.otf"), 40)
FONT_CARD_B = ImageFont.truetype(os.path.join(FONTS_DIR, "InterDisplay-Bold.otf"), 32)
FONT_SUB = ImageFont.truetype(os.path.join(FONTS_DIR, "BebasNeue-Regular.ttf"), 82)
FONT_OUTRO_LOGO = ImageFont.truetype(os.path.join(FONTS_DIR, "InterDisplay-Bold.otf"), 130)
FONT_OUTRO_TAG = ImageFont.truetype(os.path.join(FONTS_DIR, "InterDisplay-Bold.otf"), 48)
FONT_TXK = ImageFont.truetype(os.path.join(FONTS_DIR, "InterDisplay-Bold.otf"), 84)

def draw_background(draw, t):
    """Draw brand vertical gradient and subtle animated grid."""
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * ratio)
        g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * ratio)
        b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
        
    grid_spacing = 90
    grid_offset = int((t * 15) % grid_spacing)
    for x in range(0, WIDTH, grid_spacing):
        draw.line([(x, 0), (x, HEIGHT)], fill=GRID_COLOR, width=1)
    for y in range(grid_offset, HEIGHT, grid_spacing):
        draw.line([(0, y), (WIDTH, y)], fill=GRID_COLOR, width=1)

def draw_black_hole(ss, cx, cy, t, scale=1.0):
    """Draw rotating accretion disk, gravitational lensing halo, and pitch-black horizon."""
    num_rings = 22
    for i in range(num_rings, 0, -1):
        r_outer = int((185 + i * 9) * scale)
        tilt_y = 0.40
        
        color_r = 255
        color_g = int(lerp(120, 210, i / num_rings))
        color_b = int(lerp(20, 80, i / num_rings))
        outline_color = (color_r, color_g, color_b)
        
        ss.ellipse(
            (cx - r_outer, cy - int(r_outer * tilt_y), cx + r_outer, cy + int(r_outer * tilt_y)),
            outline=outline_color,
            width=max(2, int(4 * scale))
        )

    # Gravitational Lensing Halo (Photon sphere)
    halo_r = int(140 * scale)
    ss.ellipse(
        (cx - halo_r, cy - halo_r, cx + halo_r, cy + halo_r),
        outline=(255, 230, 150),
        width=int(5 * scale)
    )
               
    # The Event Horizon (Pitch-black center)
    eh_r = int(105 * scale)
    ss.ellipse(
        (cx - eh_r, cy - eh_r, cx + eh_r, cy + eh_r),
        fill=(2, 2, 6),
        outline=(20, 20, 40),
        width=2
    )
    
    # Gravitational Singularity core pinpoint
    ss.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=WHITE)

def render_vertical():
    with open(META_PATH) as f:
        meta = json.load(f)
        
    beats = meta["beats"]
    total_dur = meta["total_duration"]
    total_frames = int(total_dur * FPS)
    
    # Build 4-word caption chunks with word timings
    caption_chunks = []
    for b in beats:
        words = b["words"]
        i = 0
        while i < len(words):
            chunk = words[i:i+4]
            c_start = chunk[0][1]
            c_end = chunk[-1][2]
            caption_chunks.append({
                "words": chunk,
                "start": c_start,
                "end": c_end,
                "is_outro": b["id"] == "outro"
            })
            i += 4

    print(f"🎬 Rendering 15s Vertical Short: {OUT_MP4}")
    print(f"   Total Duration: {total_dur:.2f}s, Total Frames: {total_frames} @ {FPS} fps")
    
    proc = open_encoder(OUT_MP4, WIDTH, HEIGHT, fps=FPS, audio=AUDIO_PATH, crf=19)
    
    for f in range(total_frames):
        t = f / FPS
        
        # Determine active beat
        current_beat = beats[-1]
        for b in beats:
            if b["start"] <= t < b["end"]:
                current_beat = b
                break
                
        local_t = t - current_beat["start"]
        is_outro = (current_beat["id"] == "outro")
        frame = Image.new("RGB", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(frame)
        draw_background(draw, t)
        
        # ===================================================================
        # SCENE 1: HOOK (What is a black hole? Accretion disk & gravity warp)
        # ===================================================================
        if current_beat["id"] == "hook":
            # Brand tag
            draw.text((WIDTH // 2, 140), "TechXKenil", fill=BRAND_COLOR, font=FONT_BRAND, anchor="mm")
            
            # Category Badge
            badge_y = 220
            badge_text = "COSMIC ASTROPHYSICS // THE UNIVERSE"
            bbox = FONT_BADGE.getbbox(badge_text)
            bw = (bbox[2] - bbox[0]) + 48
            bh = 52
            bx = (WIDTH - bw) // 2
            draw.rounded_rectangle([bx, badge_y, bx + bw, badge_y + bh], radius=26, fill=DARK_CARD, outline=CYAN, width=2)
            draw.text((WIDTH // 2, badge_y + bh // 2), badge_text, fill=CYAN, font=FONT_BADGE, anchor="mm")
            
            # Big Title with spring pop
            pop = spring(local_t)
            title_y = int(340 + (1 - pop) * 30)
            draw.text((WIDTH // 2, title_y), "WHAT IS A BLACK HOLE?", fill=WHITE, font=FONT_TITLE, anchor="mm")
            draw.text((WIDTH // 2, title_y + 55), "WHERE GRAVITY DEFEATS LIGHT", fill=YELLOW, font=FONT_CARD_B, anchor="mm")
            
            # Animated Black Hole in Center
            bh_center_y = 920
            camera_zoom = 1.0 + 0.10 * (local_t / current_beat["duration"])
            
            ss = SS((WIDTH, HEIGHT))
            draw_black_hole(ss, WIDTH // 2, bh_center_y, t, scale=camera_zoom)
            
            # Data Pill below Black Hole
            pill_y = int(1240 + (1 - spring(max(0, local_t - 0.8))) * 40)
            pill_text = "ESCAPE VELOCITY > SPEED OF LIGHT (300,000 KM/S)"
            pbbox = FONT_CARD_B.getbbox(pill_text)
            pbw = (pbbox[2] - pbbox[0]) + 50
            pbh = 58
            pbx = (WIDTH - pbw) // 2
            ss.rrect((pbx, pill_y, pbx + pbw, pill_y + pbh), radius=28, fill=DARK_CARD, outline=ORANGE, width=3)
            layer = ss.out()
            frame.paste(layer, (0, 0), layer)
            
            # Text on pill
            draw = ImageDraw.Draw(frame)
            draw.text((WIDTH // 2, pill_y + pbh // 2), pill_text, fill=WHITE, font=FONT_CARD_B, anchor="mm")

        # ===================================================================
        # SCENE 2: PHYSICS & STELLAR COLLAPSE (How it forms)
        # ===================================================================
        elif current_beat["id"] == "physics":
            draw.text((WIDTH // 2, 140), "TechXKenil", fill=BRAND_COLOR, font=FONT_BRAND, anchor="mm")
            
            # Badge
            badge_y = 220
            badge_text = "HOW IT FORMS // STELLAR COLLAPSE"
            bbox = FONT_BADGE.getbbox(badge_text)
            bw = (bbox[2] - bbox[0]) + 48
            bh = 52
            bx = (WIDTH - bw) // 2
            draw.rounded_rectangle([bx, badge_y, bx + bw, badge_y + bh], radius=26, fill=DARK_CARD, outline=PURPLE, width=2)
            draw.text((WIDTH // 2, badge_y + bh // 2), badge_text, fill=PURPLE, font=FONT_BADGE, anchor="mm")
            
            draw.text((WIDTH // 2, 330), "DEATH OF A MASSIVE STAR", fill=WHITE, font=FONT_TITLE, anchor="mm")
            draw.text((WIDTH // 2, 385), "GRAVITY WINS AGAINST ALL FORCES", fill=CYAN, font=FONT_CARD_B, anchor="mm")
            
            # 3 Step Cards with progressive spring animation
            card_items = [
                ("1. MASSIVE STAR DIES", "Nuclear fusion halts; radiation pressure drops to zero.", CYAN),
                ("2. GRAVITATIONAL IMPLOSION", "Core collapses at 25% light speed into infinite density.", ORANGE),
                ("3. EVENT HORIZON TRAP", "Point of no return forms: space curves into zero volume.", GREEN)
            ]
            
            ss = SS((WIDTH, HEIGHT))
            card_start_y = 520
            card_w = 920
            card_h = 175
            card_x = (WIDTH - card_w) // 2
            
            for idx, (head, desc, acc) in enumerate(card_items):
                card_t = max(0, local_t - idx * 0.7)
                card_pop = spring(card_t)
                cy = int(card_start_y + idx * 220 + (1 - card_pop) * 60)
                
                # Card Background & Accent Border
                ss.rrect((card_x, cy, card_x + card_w, cy + card_h), radius=24, fill=DARK_CARD, outline=acc, width=3)
                
            layer = ss.out()
            frame.paste(layer, (0, 0), layer)
            draw = ImageDraw.Draw(frame)
            
            for idx, (head, desc, acc) in enumerate(card_items):
                card_t = max(0, local_t - idx * 0.7)
                if card_t > 0.05:
                    card_pop = spring(card_t)
                    cy = int(card_start_y + idx * 220 + (1 - card_pop) * 60)
                    draw.text((card_x + 36, cy + 34), head, fill=acc, font=FONT_CARD_H)
                    draw.text((card_x + 36, cy + 96), desc, fill=DIM_TEXT, font=FONT_CARD_B)
                    
            # Pulsing miniature black hole visualization at bottom
            ss_bottom = SS((WIDTH, HEIGHT))
            draw_black_hole(ss_bottom, WIDTH // 2, 1310, t, scale=0.72)
            layer_b = ss_bottom.out()
            frame.paste(layer_b, (0, 0), layer_b)

        # ===================================================================
        # SCENE 3: TECHXKENIL OUTRO (Official Brand Lock Card with Click)
        # ===================================================================
        elif current_beat["id"] == "outro":
            ss = SS((WIDTH, HEIGHT))
            
            # TXK Ring
            ring_cx, ring_cy = WIDTH // 2, 700
            ring_r = 150
            ss.ellipse((ring_cx - ring_r, ring_cy - ring_r, ring_cx + ring_r, ring_cy + ring_r), outline=PURPLE, width=10)
            
            # Subscribe Pill Button
            btn_w, btn_h = 640, 170
            btn_x = (WIDTH - btn_w) // 2
            btn_y = 1200
            
            # Cursor click dynamics
            click_time = 1.3
            is_clicked = local_t >= click_time
            btn_color = GREEN if is_clicked else RED_SUB
            btn_label = "✓ SUBSCRIBED!" if is_clicked else "SUBSCRIBE"
            
            # Gentle button pulse
            pulse_s = 1.0 + 0.03 * math.sin(local_t * 6.0) if not is_clicked else 1.0
            pw = int(btn_w * pulse_s)
            ph = int(btn_h * pulse_s)
            px = (WIDTH - pw) // 2
            py = btn_y - (ph - btn_h) // 2
            
            ss.rrect((px, py, px + pw, py + ph), radius=ph // 2, fill=btn_color)
            
            # Cursor glide from bottom right to button
            p_cursor = clamp(local_t / click_time)
            cursor_pos = arc_point((920, 1750), (ring_cx + 20, btn_y + btn_h // 2), p_cursor, bend=0.2)
            
            layer = ss.out()
            frame.paste(layer, (0, 0), layer)
            draw = ImageDraw.Draw(frame)
            
            draw_cursor(draw, cursor_pos, click_p=clamp((local_t - click_time) / 0.35))
            
            # Text inside TXK ring
            draw.text((ring_cx, ring_cy - 4), "TXK", fill=WHITE, font=FONT_TXK, anchor="mm")
            # Brand Name & Tagline
            draw.text((WIDTH // 2, 940), "TechXKenil", fill=WHITE, font=FONT_OUTRO_LOGO, anchor="mm")
            draw.text((WIDTH // 2, 1045), "AI  •  TECH  •  CODE", fill=CYAN, font=FONT_OUTRO_TAG, anchor="mm")
            # Subscribe Button Text
            draw.text((WIDTH // 2, btn_y + btn_h // 2), btn_label, fill=WHITE, font=FONT_TITLE, anchor="mm")

        # ===================================================================
        # SUBTITLES (Bebas Neue Karaoke, centered at y=1560, 4 words per chunk)
        # ===================================================================
        if not is_outro:
            for ch in caption_chunks:
                if ch["start"] <= t <= ch["end"]:
                    draw_karaoke(
                        draw,
                        (WIDTH // 2, 1560),
                        ch["words"],
                        t,
                        FONT_SUB,
                        color=WHITE,
                        active=YELLOW,
                        stroke=4
                    )
                    break

        # Pipe frame directly to ffmpeg
        proc.stdin.write(frame.tobytes())
        
        if f % 90 == 0 or f == total_frames - 1:
            progress = (f + 1) / total_frames * 100
            print(f"  Frame {f+1}/{total_frames} ({progress:.1f}%) rendered.")

    proc.stdin.close()
    proc.wait()
    print(f"\n✨ Vertical Short render complete: {OUT_MP4}")

if __name__ == "__main__":
    render_vertical()
