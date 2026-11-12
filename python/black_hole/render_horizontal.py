#!/usr/bin/env python3
"""
render_horizontal.py — High-retention 40-second Horizontal Explainer for TechXKenil:
Topic: "What is a Black Hole and How It Works"
Resolution: 1920x1080 @ 30 FPS
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
META_PATH = os.path.join(BASE_DIR, "black_hole_horizontal_meta.json")
AUDIO_PATH = os.path.join(BASE_DIR, "black_hole_horizontal_audio.wav")
OUT_MP4 = os.path.join(BASE_DIR, "black_hole_horizontal_40s.mp4")

WIDTH, HEIGHT, FPS = 1920, 1080, 30

# TechXKenil Brand Palette
BG_TOP = (8, 12, 28)
BG_BOTTOM = (24, 16, 52)
GRID_COLOR = (20, 26, 52)
WHITE = (255, 255, 255)
DIM_TEXT = (185, 192, 225)
BRAND_COLOR = (160, 170, 210)
CYAN = (70, 220, 255)
PURPLE = (150, 110, 255)
YELLOW = (255, 205, 70)
ORANGE = (255, 150, 80)
GREEN = (90, 235, 150)
RED_SUB = (255, 30, 50)
DARK_CARD = (14, 18, 38)

# Typography
FONT_BRAND = ImageFont.truetype(os.path.join(FONTS_DIR, "InterDisplay-Bold.otf"), 36)
FONT_ACT = ImageFont.truetype(os.path.join(FONTS_DIR, "InterDisplay-Bold.otf"), 26)
FONT_HEADING = ImageFont.truetype(os.path.join(FONTS_DIR, "InterDisplay-Bold.otf"), 62)
FONT_SUBTITLE = ImageFont.truetype(os.path.join(FONTS_DIR, "InterDisplay-Bold.otf"), 30)
FONT_CARD_TITLE = ImageFont.truetype(os.path.join(FONTS_DIR, "InterDisplay-Bold.otf"), 34)
FONT_CARD_BODY = ImageFont.truetype(os.path.join(FONTS_DIR, "InterDisplay-Bold.otf"), 26)
FONT_SUB = ImageFont.truetype(os.path.join(FONTS_DIR, "InterDisplay-Bold.otf"), 40)
FONT_OUTRO_LOGO = ImageFont.truetype(os.path.join(FONTS_DIR, "InterDisplay-Bold.otf"), 150)
FONT_OUTRO_TAG = ImageFont.truetype(os.path.join(FONTS_DIR, "InterDisplay-Bold.otf"), 52)
FONT_TXK = ImageFont.truetype(os.path.join(FONTS_DIR, "InterDisplay-Bold.otf"), 78)

def draw_background(draw, t):
    """Draw horizontal gradient and subtle background grid."""
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * ratio)
        g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * ratio)
        b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
        
    grid_spacing = 90
    grid_offset = int((t * 12) % grid_spacing)
    for x in range(0, WIDTH, grid_spacing):
        draw.line([(x, 0), (x, HEIGHT)], fill=GRID_COLOR, width=1)
    for y in range(grid_offset, HEIGHT, grid_spacing):
        draw.line([(0, y), (WIDTH, y)], fill=GRID_COLOR, width=1)

def draw_horizontal_black_hole(ss, cx, cy, t, scale=1.0):
    """Draw widescreen relativistic Black Hole with spinning accretion disk."""
    num_rings = 24
    for i in range(num_rings, 0, -1):
        r_outer = int((190 + i * 11) * scale)
        tilt_y = 0.38
        
        # Relativistic Doppler shift (blue-shifted left, red-shifted right)
        color_r = 255
        color_g = int(lerp(120, 220, i / num_rings))
        color_b = int(lerp(30, 90, i / num_rings))
        outline_color = (color_r, color_g, color_b)
        
        ss.ellipse(
            (cx - r_outer, cy - int(r_outer * tilt_y), cx + r_outer, cy + int(r_outer * tilt_y)),
            outline=outline_color,
            width=max(2, int(4 * scale))
        )

    # Gravitational Lensing Halo (Photon sphere)
    halo_r = int(155 * scale)
    ss.ellipse(
        (cx - halo_r, cy - halo_r, cx + halo_r, cy + halo_r),
        outline=(255, 235, 160),
        width=int(6 * scale)
    )
               
    # The Event Horizon (Pitch-black center)
    eh_r = int(120 * scale)
    ss.ellipse(
        (cx - eh_r, cy - eh_r, cx + eh_r, cy + eh_r),
        fill=(2, 2, 6),
        outline=(25, 25, 50),
        width=2
    )
    
    # Gravitational Singularity core pinpoint
    ss.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=WHITE)

def render_horizontal():
    with open(META_PATH) as f:
        meta = json.load(f)
        
    beats = meta["beats"]
    total_dur = meta["total_duration"]
    total_frames = int(total_dur * FPS)
    
    # Build 6-7 word caption chunks with word timings for calm widescreen reading
    caption_chunks = []
    for b in beats:
        words = b["words"]
        i = 0
        while i < len(words):
            chunk = words[i:i+7]
            c_start = chunk[0][1]
            c_end = chunk[-1][2]
            caption_chunks.append({
                "words": chunk,
                "start": c_start,
                "end": c_end,
            })
            i += 7

    print(f"🎬 Rendering 40s Horizontal Explainer: {OUT_MP4}")
    print(f"   Total Duration: {total_dur:.2f}s, Total Frames: {total_frames} @ {FPS} fps")
    
    proc = open_encoder(OUT_MP4, WIDTH, HEIGHT, fps=FPS, audio=AUDIO_PATH, crf=19)
    
    for f in range(total_frames):
        t = f / FPS
        
        # Determine active beat: beat i remains active until beat i+1 starts (no gap/flicker)
        current_beat = beats[0]
        for i, b in enumerate(beats):
            next_start = beats[i + 1]["start"] if i + 1 < len(beats) else total_dur + 1.0
            if b["start"] <= t < next_start:
                current_beat = b
                break
                
        local_t = t - current_beat["start"]
        frame = Image.new("RGB", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(frame)
        draw_background(draw, t)
        
        # Outro scene in last beat
        is_outro = (current_beat["id"] == "verdict" and local_t >= (current_beat["duration"] - 4.5))
        
        if not is_outro:
            # TechXKenil Brand Tag (Top Left)
            draw.text((70, 50), "TechXKenil", fill=BRAND_COLOR, font=FONT_BRAND)
            
            # Act Pill Badge
            act_text = current_beat.get("act", "ASTROPHYSICS")
            abbox = FONT_ACT.getbbox(act_text)
            abw = (abbox[2] - abbox[0]) + 32
            abh = 42
            draw.rounded_rectangle([70, 102, 70 + abw, 102 + abh], radius=21, fill=DARK_CARD, outline=ORANGE, width=2)
            draw.text((70 + abw // 2, 102 + abh // 2), act_text, fill=ORANGE, font=FONT_ACT, anchor="mm")
            
            # Main Heading & Subtitle
            pop = spring(local_t)
            head_y = int(165 + (1 - pop) * 20)
            draw.text((70, head_y), current_beat["title"], fill=WHITE, font=FONT_HEADING)
            draw.text((70, head_y + 76), current_beat["subtitle"], fill=DIM_TEXT, font=FONT_SUBTITLE)
            
            # Left Column Cards (Staggered spring reveals)
            left_cards = []
            if current_beat["id"] == "definition":
                left_cards = [
                    ("INFINITE DENSITY IN ZERO VOLUME", "All mass is compressed into a mathematical point called the Singularity.", CYAN),
                    ("EXTREME SPACETIME CURVATURE", "Gravity is so intense that space bends into a bottomless funnel.", ORANGE),
                    ("ESCAPE VELOCITY > LIGHT SPEED", "Not even photons traveling at 300,000 km/s can escape.", YELLOW),
                ]
            elif current_beat["id"] == "collapse":
                left_cards = [
                    ("1. NUCLEAR FUEL EXHAUSTION", "Massive star (>20 Solar Masses) runs out of fusion fuel.", CYAN),
                    ("2. LOSS OF OUTWARD PRESSURE", "No outward thermal radiation left to counterbalance gravity.", ORANGE),
                    ("3. CATASTROPHIC CORE IMPLOSION", "Core collapses inward at 25% light speed in milliseconds.", GREEN),
                ]
            elif current_beat["id"] == "anatomy":
                left_cards = [
                    ("THE ACCRETION DISK", "Superheated plasma swirling around the center at relativistic speeds.", ORANGE),
                    ("THE EVENT HORIZON", "The cosmic point of no return: r_s = 2GM / c².", CYAN),
                    ("THE SINGULARITY", "Zero volume, infinite density, where laws of physics break down.", PURPLE),
                ]
            elif current_beat["id"] == "verdict":
                left_cards = [
                    ("MYTH: COSMIC VACUUM CLEANERS", "They do not suck. If our Sun became a black hole, Earth would orbit normally.", CYAN),
                    ("REALITY: PURE SPACETIME CURVATURE", "They simply curve space deeper than any other object in the cosmos.", GREEN),
                    ("EINSTEIN'S GENERAL RELATIVITY", "Directly proven by gravitational wave ripples detected across billions of light years.", YELLOW),
                ]
                
            ss = SS((WIDTH, HEIGHT))
            card_x = 70
            card_w = 900
            card_h = 135
            card_start_y = 310
            
            for idx, (head, desc, acc) in enumerate(left_cards):
                card_t = max(0, local_t - idx * 0.6)
                c_pop = spring(card_t)
                cy = int(card_start_y + idx * 170 + (1 - c_pop) * 40)
                ss.rrect((card_x, cy, card_x + card_w, cy + card_h), radius=18, fill=DARK_CARD, outline=acc, width=2)
                
            # Right Column: Relativistic Black Hole Simulation (Center: 1440, 540)
            bh_zoom = 1.0 + 0.08 * math.sin(local_t * 0.6)
            draw_horizontal_black_hole(ss, 1440, 540, t, scale=bh_zoom)
            
            # Metric Pills below Black Hole
            mp_y = int(870 + (1 - spring(max(0, local_t - 1.0))) * 30)
            pills = [
                ("ESCAPE SPEED: > c", CYAN),
                ("DENSITY: ∞", ORANGE),
                ("r_s = 2GM / c²", GREEN)
            ]
            total_pw = 680
            px_start = 1440 - total_pw // 2
            for p_idx, (p_txt, p_col) in enumerate(pills):
                px = px_start + p_idx * 230
                ss.rrect((px, mp_y, px + 215, mp_y + 48), radius=24, fill=DARK_CARD, outline=p_col, width=2)
                
            layer = ss.out()
            frame.paste(layer, (0, 0), layer)
            draw = ImageDraw.Draw(frame)
            
            # Text on left cards
            for idx, (head, desc, acc) in enumerate(left_cards):
                card_t = max(0, local_t - idx * 0.6)
                if card_t > 0.05:
                    c_pop = spring(card_t)
                    cy = int(card_start_y + idx * 170 + (1 - c_pop) * 40)
                    draw.text((card_x + 28, cy + 24), head, fill=acc, font=FONT_CARD_TITLE)
                    draw.text((card_x + 28, cy + 78), desc, fill=DIM_TEXT, font=FONT_CARD_BODY)
                    
            # Text on metric pills
            for p_idx, (p_txt, p_col) in enumerate(pills):
                px = px_start + p_idx * 230
                draw.text((px + 107, mp_y + 24), p_txt, fill=WHITE, font=FONT_ACT, anchor="mm")

        # ===================================================================
        # OUTRO CARD (Official Widescreen TechXKenil Brand Lock)
        # ===================================================================
        else:
            outro_t = local_t - (current_beat["duration"] - 4.5)
            ss = SS((WIDTH, HEIGHT))
            
            ring_cx, ring_cy = WIDTH // 2, 330
            ring_r = 130
            ss.ellipse((ring_cx - ring_r, ring_cy - ring_r, ring_cx + ring_r, ring_cy + ring_r), outline=PURPLE, width=9)
            
            btn_w, btn_h = 760, 160
            btn_x = (WIDTH - btn_w) // 2
            btn_y = 740
            
            click_time = 1.4
            is_clicked = outro_t >= click_time
            btn_color = GREEN if is_clicked else RED_SUB
            btn_label = "✓ SUBSCRIBED!" if is_clicked else "SUBSCRIBE"
            
            pulse_s = 1.0 + 0.02 * math.sin(outro_t * 5.0) if not is_clicked else 1.0
            pw = int(btn_w * pulse_s)
            ph = int(btn_h * pulse_s)
            px = (WIDTH - pw) // 2
            py = btn_y - (ph - btn_h) // 2
            
            ss.rrect((px, py, px + pw, py + ph), radius=ph // 2, fill=btn_color)
            
            p_cursor = clamp(outro_t / click_time)
            cursor_pos = arc_point((1600, 980), (ring_cx + 40, btn_y + btn_h // 2), p_cursor, bend=0.2)
            
            layer = ss.out()
            frame.paste(layer, (0, 0), layer)
            draw = ImageDraw.Draw(frame)
            
            draw_cursor(draw, cursor_pos, click_p=clamp((outro_t - click_time) / 0.35))
            
            draw.text((ring_cx, ring_cy - 4), "TXK", fill=WHITE, font=FONT_TXK, anchor="mm")
            draw.text((WIDTH // 2, 530), "TechXKenil", fill=WHITE, font=FONT_OUTRO_LOGO, anchor="mm")
            draw.text((WIDTH // 2, 640), "AI  •  TECH  •  CODE", fill=CYAN, font=FONT_OUTRO_TAG, anchor="mm")
            draw.text((WIDTH // 2, btn_y + btn_h // 2), btn_label, fill=WHITE, font=FONT_HEADING, anchor="mm")

        # ===================================================================
        # SUBTITLES (Centered at y=1000, max 7 words per chunk, calm readable style)
        # ===================================================================
        if not is_outro:
            for ch in caption_chunks:
                if ch["start"] <= t <= ch["end"]:
                    draw_karaoke(
                        draw,
                        (WIDTH // 2, 1000),
                        ch["words"],
                        t,
                        FONT_SUB,
                        color=WHITE,
                        active=YELLOW,
                        stroke=3
                    )
                    break

        # Pipe frame directly to ffmpeg
        proc.stdin.write(frame.tobytes())
        
        if f % 120 == 0 or f == total_frames - 1:
            progress = (f + 1) / total_frames * 100
            print(f"  Frame {f+1}/{total_frames} ({progress:.1f}%) rendered.")

    proc.stdin.close()
    proc.wait()
    print(f"\n✨ Horizontal Explainer render complete: {OUT_MP4}")

if __name__ == "__main__":
    render_horizontal()
