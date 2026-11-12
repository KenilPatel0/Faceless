#!/usr/bin/env python3
"""
render_press_enter.py — Autonomous Video Production for:
Short 6: "What Happens When You Press Enter on a Website"
Resolution: 1080x1920 (Vertical 9:16) @ 30 FPS
Duration: ~29.6s (Brand target: 28-32s)
"""

import os
import sys
import json
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TOOLS_DIR = os.path.join(REPO_ROOT, "python", "tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from motion import (
    SS, spring, arc_point, draw_cursor, draw_karaoke,
    open_encoder, clamp, lerp
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(REPO_ROOT, "fonts")
META_PATH = os.path.join(BASE_DIR, "meta_press_enter.json")
AUDIO_PATH = os.path.join(BASE_DIR, "audio_press_enter.wav")
OUT_MP4 = os.path.join(BASE_DIR, "press_enter_website_short.mp4")

WIDTH, HEIGHT, FPS = 1080, 1920, 30

# TechXKenil Brand Palette
BG_TOP = (8, 12, 28)
BG_BOTTOM = (30, 16, 70)
GRID_COLOR = (22, 28, 58)

WHITE = (255, 255, 255)
DIM_TEXT = (185, 192, 225)
BRAND_COLOR = (160, 170, 210)
CYAN = (70, 220, 255)
YELLOW = (255, 205, 70)
GREEN = (90, 235, 150)
RED = (255, 70, 90)
PURPLE = (150, 110, 255)
ORANGE = (255, 150, 80)
BLUE = (60, 120, 255)
RED_SUB = (255, 30, 50)
DARK_CARD = (16, 22, 48)

# Load Fonts
FONT_INTER = os.path.join(FONTS_DIR, "InterDisplay-Bold.otf")
FONT_BEBAS = os.path.join(FONTS_DIR, "BebasNeue-Regular.ttf")

FONT_BRAND = ImageFont.truetype(FONT_INTER, 52)
FONT_BADGE = ImageFont.truetype(FONT_INTER, 30)
FONT_TITLE = ImageFont.truetype(FONT_INTER, 60)
FONT_SUBTITLE = ImageFont.truetype(FONT_INTER, 36)
FONT_CARD_H = ImageFont.truetype(FONT_INTER, 42)
FONT_CARD_B = ImageFont.truetype(FONT_INTER, 32)
FONT_CODE = ImageFont.truetype(FONT_INTER, 34)
FONT_SUB = ImageFont.truetype(FONT_BEBAS, 78)

# Brand Lock Outro Fonts
FONT_TXK = ImageFont.truetype(FONT_INTER, 84)
FONT_OUTRO_LOGO = ImageFont.truetype(FONT_INTER, 130)
FONT_OUTRO_TAG = ImageFont.truetype(FONT_INTER, 48)

def draw_background(dr, t):
    """Draws vertical gradient background with animated 90px grid lines."""
    for y in range(0, HEIGHT, 8):
        factor = y / HEIGHT
        r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * factor)
        g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * factor)
        b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * factor)
        dr.line([(0, y), (WIDTH, y + 8)], fill=(r, g, b), width=8)

    # Subtle shifting grid
    grid_offset = int((t * 18) % 90)
    for x in range(0, WIDTH + 90, 90):
        dr.line([(x, 0), (x, HEIGHT)], fill=GRID_COLOR, width=1)
    for y in range(grid_offset, HEIGHT + 90, 90):
        dr.line([(0, y), (WIDTH, y)], fill=GRID_COLOR, width=1)

def draw_step_badge(dr, ss, text, accent_color, y=230):
    """Draws category / step header pill at top."""
    bbox = FONT_BADGE.getbbox(text)
    bw = (bbox[2] - bbox[0]) + 48
    bh = 54
    bx = (WIDTH - bw) // 2
    ss.rrect((bx, y, bx + bw, y + bh), radius=27, fill=(20, 26, 56), outline=accent_color, width=2)
    dr.text((WIDTH // 2, y + bh // 2 - 1), text, fill=accent_color, font=FONT_BADGE, anchor="mm")

def render_short():
    with open(META_PATH) as f:
        meta = json.load(f)

    scenes = meta["scenes"]
    total_dur = meta["total_duration"]
    total_frames = int(total_dur * FPS)

    # Pre-build 4-word caption chunks with word boundaries
    caption_chunks = []
    for sc in scenes:
        words = sc["words"]
        i = 0
        while i < len(words):
            chunk = words[i:i+4]
            c_start = chunk[0][1]
            c_end = chunk[-1][2]
            caption_chunks.append({
                "words": chunk,
                "start": c_start,
                "end": c_end,
                "is_special": sc["id"] in ("intro", "outro")
            })
            i += 4

    print(f"🎬 Rendering Short 6 (Press Enter on Website): {OUT_MP4}")
    print(f"   Total Duration: {total_dur:.2f}s, Total Frames: {total_frames} @ {FPS} fps")

    proc = open_encoder(OUT_MP4, WIDTH, HEIGHT, fps=FPS, audio=AUDIO_PATH, crf=19)

    for f in range(total_frames):
        t = f / FPS

        # Determine active scene: scene i remains active until scene i+1 starts (no gap/flicker)
        current_scene = scenes[0]
        for i, sc in enumerate(scenes):
            next_start = scenes[i + 1]["start"] if i + 1 < len(scenes) else total_dur + 1.0
            if sc["start"] <= t < next_start:
                current_scene = sc
                break

        local_t = t - current_scene["start"]
        is_intro = current_scene["id"] == "intro"
        is_outro = current_scene["id"] == "outro"

        frame = Image.new("RGB", (WIDTH, HEIGHT))
        draw = ImageDraw.Draw(frame)
        draw_background(draw, t)

        # Brand tag on all scenes except intro/outro
        if not is_intro and not is_outro:
            draw.text((WIDTH // 2, 140), "TechXKenil", fill=BRAND_COLOR, font=FONT_BRAND, anchor="mm")

        # ===================================================================
        # SCENE 1: HOOK (URL Omnibox & Enter Key Press)
        # ===================================================================
        if current_scene["id"] == "hook":
            ss = SS((WIDTH, HEIGHT))
            draw_step_badge(draw, ss, "NETWORKING // HOW THE WEB WORKS", CYAN, y=220)

            # Main Headline
            p_head = spring(clamp(local_t / 0.5))
            head_y = int(340 + (1 - p_head) * 40)
            draw.text((WIDTH // 2, head_y), "WHAT HAPPENS WHEN", fill=WHITE, font=FONT_TITLE, anchor="mm")
            draw.text((WIDTH // 2, head_y + 70), "YOU PRESS ENTER?", fill=YELLOW, font=FONT_TITLE, anchor="mm")

            # 1. Genuine URL Browser Omnibox
            p_bar = spring(clamp((local_t - 0.3) / 0.5))
            bar_w, bar_h = 920, 110
            bar_x = (WIDTH - bar_w) // 2
            bar_y = int(540 + (1 - p_bar) * 50)
            ss.rrect((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h), radius=30, fill=DARK_CARD, outline=CYAN, width=3)

            # Padlock icon inside URL bar
            ss.rrect((bar_x + 36, bar_y + 44, bar_x + 64, bar_y + 74), radius=6, fill=CYAN)
            ss.ellipse((bar_x + 40, bar_y + 28, bar_x + 60, bar_y + 50), outline=CYAN, width=4)

            # Typing domain animation
            domain_full = "https://techxkenil.dev"
            type_chars = min(len(domain_full), int((local_t - 0.4) * 16))
            typed_domain = domain_full[:max(0, type_chars)]
            cursor_blink = " |" if (int(t * 3) % 2 == 0) else ""
            draw.text((bar_x + 85, bar_y + bar_h // 2), typed_domain + cursor_blink, fill=WHITE, font=FONT_CODE, anchor="lm")

            # 2. 3D Enter Key Graphic
            p_key = spring(clamp((local_t - 1.2) / 0.5))
            key_w, key_h = 440, 180
            key_x = (WIDTH - key_w) // 2
            
            # Press down animation at t=1.8s
            is_pressed = (local_t >= 1.7)
            press_offset = 14 if is_pressed else 0
            key_y = int(820 + (1 - p_key) * 60 + press_offset)

            # 3D Depth bottom plate
            ss.rrect((key_x, key_y + 16, key_x + key_w, key_y + key_h + 16), radius=28, fill=(18, 14, 46))
            # Keycap face
            key_fill = (45, 30, 95) if is_pressed else (60, 40, 130)
            key_outline = YELLOW if is_pressed else PURPLE
            ss.rrect((key_x, key_y, key_x + key_w, key_y + key_h), radius=28, fill=key_fill, outline=key_outline, width=4)

            # Ripple pulse on press
            if is_pressed:
                rip_p = clamp((local_t - 1.7) / 0.8)
                rw = int(key_w + rip_p * 260)
                rh = int(key_h + rip_p * 140)
                ss.rrect(((WIDTH - rw) // 2, key_y - (rh - key_h) // 2, (WIDTH + rw) // 2, key_y + rh), radius=35, outline=YELLOW, width=max(1, int(4 * (1 - rip_p))))

            layer = ss.out()
            frame.paste(layer, (0, 0), layer)
            draw = ImageDraw.Draw(frame)

            draw.text((WIDTH // 2, key_y + key_h // 2 - 4), "↵  ENTER", fill=WHITE, font=FONT_TITLE, anchor="mm")
            draw.text((WIDTH // 2, 1100), "The 5-Step Journey of a Web Request", fill=DIM_TEXT, font=FONT_SUBTITLE, anchor="mm")

        # ===================================================================
        # SCENE 2: INTRO CARD (Official TechXKenil Brand Lock — Rule §6)
        # ===================================================================
        elif is_intro:
            ss = SS((WIDTH, HEIGHT))
            p_intro = spring(clamp(local_t / 0.5))

            # Ring circle at y=720, r=150
            ring_cx, ring_cy = WIDTH // 2, 720
            ring_r = int(150 * p_intro)
            ss.ellipse((ring_cx - ring_r, ring_cy - ring_r, ring_cx + ring_r, ring_cy + ring_r), outline=PURPLE, width=10)

            layer = ss.out()
            frame.paste(layer, (0, 0), layer)
            draw = ImageDraw.Draw(frame)

            # TXK inside ring
            draw.text((ring_cx, ring_cy - 4), "TXK", fill=WHITE, font=FONT_TXK, anchor="mm")
            # Brand Name at y=1000
            draw.text((WIDTH // 2, 1000), "TechXKenil", fill=WHITE, font=FONT_OUTRO_LOGO, anchor="mm")
            # Cyan tagline at y=1120
            draw.text((WIDTH // 2, 1120), "AI  •  TECH  •  CODE", fill=CYAN, font=FONT_OUTRO_TAG, anchor="mm")

        # ===================================================================
        # SCENE 3: STEP 1 — DNS LOOKUP
        # ===================================================================
        elif current_scene["id"] == "step1_dns":
            ss = SS((WIDTH, HEIGHT))
            draw_step_badge(draw, ss, "STEP 01 // THE INTERNET'S PHONE BOOK", CYAN, y=220)

            p = spring(clamp(local_t / 0.5))
            head_y = int(340 + (1 - p) * 40)
            draw.text((WIDTH // 2, head_y), "DOMAIN TO IP CONVERSION", fill=WHITE, font=FONT_TITLE, anchor="mm")

            # Left Card: Client Browser
            card_w, card_h = 360, 200
            c1_x, c1_y = 100, 520
            ss.rrect((c1_x, c1_y, c1_x + card_w, c1_y + card_h), radius=24, fill=DARK_CARD, outline=CYAN, width=3)

            # Right Card: DNS Root Server
            c2_x, c2_y = WIDTH - 100 - card_w, 520
            ss.rrect((c2_x, c2_y, c2_x + card_w, c2_y + card_h), radius=24, fill=DARK_CARD, outline=PURPLE, width=3)

            # Connecting Data Highway with Moving Packet
            line_y = 620
            ss.line([(c1_x + card_w, line_y), (c2_x, line_y)], fill=(50, 60, 110), width=6)

            # Glowing data packet traveling back and forth
            pulse_p = (local_t * 1.4) % 2.0
            if pulse_p < 1.0:
                pkt_x = int(lerp(c1_x + card_w, c2_x, pulse_p))
                ss.ellipse((pkt_x - 14, line_y - 14, pkt_x + 14, line_y + 14), fill=YELLOW)
            else:
                pkt_x = int(lerp(c2_x, c1_x + card_w, pulse_p - 1.0))
                ss.ellipse((pkt_x - 14, line_y - 14, pkt_x + 14, line_y + 14), fill=GREEN)

            # Big Resolved Address Card below
            p_res = spring(clamp((local_t - 1.2) / 0.5))
            res_w, res_h = 880, 260
            res_x = (WIDTH - res_w) // 2
            res_y = int(820 + (1 - p_res) * 50)
            ss.rrect((res_x, res_y, res_x + res_w, res_y + res_h), radius=28, fill=DARK_CARD, outline=GREEN, width=4)

            layer = ss.out()
            frame.paste(layer, (0, 0), layer)
            draw = ImageDraw.Draw(frame)

            # Text inside client / server cards
            draw.text((c1_x + card_w // 2, c1_y + 60), "BROWSER", fill=CYAN, font=FONT_CARD_H, anchor="mm")
            draw.text((c1_x + card_w // 2, c1_y + 120), "techxkenil.dev", fill=WHITE, font=FONT_CARD_B, anchor="mm")

            draw.text((c2_x + card_w // 2, c2_y + 60), "DNS SERVER", fill=PURPLE, font=FONT_CARD_H, anchor="mm")
            draw.text((c2_x + card_w // 2, c2_y + 120), "8.8.8.8 / 1.1.1.1", fill=WHITE, font=FONT_CARD_B, anchor="mm")

            # Resolved IP details
            draw.text((WIDTH // 2, res_y + 60), "RESOLVED DESTINATION IP", fill=GREEN, font=FONT_CARD_H, anchor="mm")
            draw.text((WIDTH // 2, res_y + 130), "104 . 21 . 78 . 192", fill=YELLOW, font=FONT_TITLE, anchor="mm")
            draw.text((WIDTH // 2, res_y + 195), "Found in browser cache in 12ms", fill=DIM_TEXT, font=FONT_CARD_B, anchor="mm")

        # ===================================================================
        # SCENE 4: STEP 2 — SECURE HTTPS / TLS HANDSHAKE
        # ===================================================================
        elif current_scene["id"] == "step2_https":
            ss = SS((WIDTH, HEIGHT))
            draw_step_badge(draw, ss, "STEP 02 // SECURE CONNECTION", GREEN, y=220)

            p = spring(clamp(local_t / 0.5))
            head_y = int(340 + (1 - p) * 40)
            draw.text((WIDTH // 2, head_y), "TLS HANDSHAKE & HTTPS", fill=WHITE, font=FONT_TITLE, anchor="mm")

            # Big Padlock Icon in Center
            pad_cx, pad_cy = WIDTH // 2, 680
            shackle_p = clamp(local_t / 1.0)
            # Shackle drops down into locked position
            shackle_drop = int(lerp(-35, 0, spring(shackle_p)))
            is_locked = (local_t >= 0.9)
            pad_color = GREEN if is_locked else YELLOW

            # Shackle arc
            ss.ellipse((pad_cx - 90, pad_cy - 160 + shackle_drop, pad_cx + 90, pad_cy - 20 + shackle_drop), outline=pad_color, width=22)
            # Padlock body
            body_w, body_h = 260, 200
            ss.rrect((pad_cx - body_w // 2, pad_cy - 40, pad_cx + body_w // 2, pad_cy + body_h - 40), radius=36, fill=DARK_CARD, outline=pad_color, width=6)
            # Keyhole
            ss.ellipse((pad_cx - 18, pad_cy + 25, pad_cx + 18, pad_cy + 61), fill=pad_color)
            ss.rrect((pad_cx - 9, pad_cy + 50, pad_cx + 9, pad_cy + 95), fill=pad_color)

            # Security Banner below padlock
            p_ban = spring(clamp((local_t - 1.1) / 0.5))
            ban_w, ban_h = 880, 230
            ban_x = (WIDTH - ban_w) // 2
            ban_y = int(930 + (1 - p_ban) * 50)
            ss.rrect((ban_x, ban_y, ban_x + ban_w, ban_y + ban_h), radius=28, fill=DARK_CARD, outline=GREEN, width=4)

            layer = ss.out()
            frame.paste(layer, (0, 0), layer)
            draw = ImageDraw.Draw(frame)

            draw.text((WIDTH // 2, ban_y + 55), "🔒 256-BIT ENCRYPTED CHANNEL", fill=GREEN, font=FONT_CARD_H, anchor="mm")
            draw.text((WIDTH // 2, ban_y + 115), "TLS 1.3 Asymmetric Key Exchange", fill=WHITE, font=FONT_CARD_B, anchor="mm")
            draw.text((WIDTH // 2, ban_y + 170), "Zero eavesdropping. Safe from ISP snooping.", fill=DIM_TEXT, font=FONT_CARD_B, anchor="mm")

        # ===================================================================
        # SCENE 5: STEP 3 & 4 — HTTP REQUEST & PAYLOAD (HTML, CSS, JS)
        # ===================================================================
        elif current_scene["id"] == "step3_payload":
            ss = SS((WIDTH, HEIGHT))
            draw_step_badge(draw, ss, "STEPS 03 & 04 // SERVER REPLIES", ORANGE, y=220)

            p = spring(clamp(local_t / 0.5))
            head_y = int(340 + (1 - p) * 40)
            draw.text((WIDTH // 2, head_y), "STREAMING THE ASSETS", fill=WHITE, font=FONT_TITLE, anchor="mm")

            # 3 Asset Pills flying into browser
            assets = [
                ("📄 index.html", "Structure & DOM Skeleton", ORANGE),
                ("🎨 styles.css", "Design, Colors & Flexbox", CYAN),
                ("⚡ bundle.js", "Logic, React & Interactions", YELLOW)
            ]

            card_start_y = 480
            card_w = 900
            card_h = 160
            card_x = (WIDTH - card_w) // 2

            for idx, (title_txt, sub_txt, acc) in enumerate(assets):
                card_t = max(0, local_t - idx * 0.6)
                card_pop = spring(clamp(card_t / 0.5))
                cy = int(card_start_y + idx * 190 + (1 - card_pop) * 60)
                ss.rrect((card_x, cy, card_x + card_w, cy + card_h), radius=24, fill=DARK_CARD, outline=acc, width=3)

            layer = ss.out()
            frame.paste(layer, (0, 0), layer)
            draw = ImageDraw.Draw(frame)

            for idx, (title_txt, sub_txt, acc) in enumerate(assets):
                card_t = max(0, local_t - idx * 0.6)
                if card_t > 0.05:
                    card_pop = spring(clamp(card_t / 0.5))
                    cy = int(card_start_y + idx * 190 + (1 - card_pop) * 60)
                    draw.text((card_x + 40, cy + 34), title_txt, fill=acc, font=FONT_CARD_H)
                    draw.text((card_x + 40, cy + 96), sub_txt, fill=DIM_TEXT, font=FONT_CARD_B)

            # Response header pill
            draw.text((WIDTH // 2, 1140), "HTTP/2 200 OK — 14.8 KB Transferred", fill=GREEN, font=FONT_SUBTITLE, anchor="mm")

        # ===================================================================
        # SCENE 6: STEP 5 — PIXEL PAINTING ON SCREEN
        # ===================================================================
        elif current_scene["id"] == "step5_render":
            ss = SS((WIDTH, HEIGHT))
            draw_step_badge(draw, ss, "STEP 05 // BROWSER RENDERING", PURPLE, y=220)

            p = spring(clamp(local_t / 0.5))
            head_y = int(340 + (1 - p) * 40)
            draw.text((WIDTH // 2, head_y), "PARSING & PAINTING PIXELS", fill=WHITE, font=FONT_TITLE, anchor="mm")

            # Phone / Screen Viewport Mockup
            phone_w, phone_h = 700, 680
            phone_x = (WIDTH - phone_w) // 2
            phone_y = 480
            ss.rrect((phone_x, phone_y, phone_x + phone_w, phone_y + phone_h), radius=36, fill=(14, 18, 40), outline=(120, 130, 180), width=4)

            # Simulated progressive website build
            # 1. Nav bar
            ss.rrect((phone_x + 24, phone_y + 24, phone_x + phone_w - 24, phone_y + 80), radius=16, fill=(28, 36, 75))
            # 2. Hero banner (pops at t=0.6s)
            p_hero = spring(clamp((local_t - 0.5) / 0.4))
            if p_hero > 0.05:
                hw = int((phone_w - 48) * p_hero)
                ss.rrect((phone_x + 24, phone_y + 105, phone_x + 24 + hw, phone_y + 300), radius=20, fill=(38, 22, 85), outline=PURPLE, width=2)
            # 3. Two content cards (pop at t=1.2s)
            p_cards = spring(clamp((local_t - 1.0) / 0.4))
            if p_cards > 0.05:
                ss.rrect((phone_x + 24, phone_y + 325, phone_x + 335, phone_y + 490), radius=18, fill=DARK_CARD, outline=CYAN, width=2)
                ss.rrect((phone_x + 365, phone_y + 325, phone_x + phone_w - 24, phone_y + 490), radius=18, fill=DARK_CARD, outline=GREEN, width=2)

            # Speed metric badge
            p_speed = spring(clamp((local_t - 1.5) / 0.4))
            if p_speed > 0.05:
                ss.rrect((phone_x + 60, phone_y + 530, phone_x + phone_w - 60, phone_y + 620), radius=22, fill=(24, 45, 36), outline=GREEN, width=3)

            layer = ss.out()
            frame.paste(layer, (0, 0), layer)
            draw = ImageDraw.Draw(frame)

            draw.text((phone_x + 45, phone_y + 52), "TechXKenil.dev", fill=WHITE, font=FONT_CARD_B, anchor="lm")
            if p_hero > 0.1:
                draw.text((phone_x + phone_w // 2, phone_y + 200), "WELCOME TO TECHXKENIL", fill=WHITE, font=FONT_CARD_H, anchor="mm")
            if p_cards > 0.1:
                draw.text((phone_x + 180, phone_y + 405), "AI & TECH", fill=CYAN, font=FONT_CARD_B, anchor="mm")
                draw.text((phone_x + 520, phone_y + 405), "CODE", fill=GREEN, font=FONT_CARD_B, anchor="mm")
            if p_speed > 0.1:
                draw.text((phone_x + phone_w // 2, phone_y + 575), "⚡ Full Paint Completed in 48ms", fill=GREEN, font=FONT_CARD_H, anchor="mm")

            draw.text((WIDTH // 2, 1220), "DOM Tree ➔ CSSOM ➔ Render Tree ➔ Paint", fill=DIM_TEXT, font=FONT_SUBTITLE, anchor="mm")

        # ===================================================================
        # SCENE 7: TECHXKENIL OUTRO (Official Brand Lock — Rule §6)
        # ===================================================================
        elif is_outro:
            ss = SS((WIDTH, HEIGHT))

            # TXK Ring Circle at y=700, r=150
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

            # Gentle pulse
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
        if not is_intro and not is_outro:
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

        proc.stdin.write(frame.tobytes())

        if f % 90 == 0 or f == total_frames - 1:
            progress = (f + 1) / total_frames * 100
            print(f"  Frame {f+1}/{total_frames} ({progress:.1f}%) rendered.")

    proc.stdin.close()
    proc.wait()
    print(f"\n✨ Short 6 render complete: {OUT_MP4}")

if __name__ == "__main__":
    render_short()

