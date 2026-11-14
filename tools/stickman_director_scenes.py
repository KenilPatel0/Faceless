#!/usr/bin/env python3
"""
stickman_director_scenes.py — Director-Grade Animated Stickman Explainer Scenes
Applies the B5 Character Explainer / Directing Stickman Videos principles:
- The stickman is an active, expressive narrator and physical comedy actor.
- Physical state changes and causal metaphors:
    1. Hook: Stickman types furiously, leaps & slams Enter, gets blown back in awe as stopwatch hits 28ms.
    2. Tokenization: Stickman karate-chops the sentence into 5 token blocks, holds up tokens, vector beam ignition.
    3. Prefill GEMM: Stickman pulls a massive industrial server lever, 16 Tensor Cores ignite, stickman dons cool sunglasses.
    4. KV Cache: Left side stickman buried under an avalanche of papers sweating; Right side stickman locking KV slots sipping coffee.
    5. Memory Bottleneck: Stickman physically pushes a giant 140 GB weight block across the HBM3 silicon bridge, sweating.
    6. Speculative Race: Referee stickman with whistle & clipboard stamps 4 checkmarks as mini 1B sprinter dashes past.
    7. Outro: Stickman leaps and stomps the red SUBSCRIBE button, triggering gold confetti and celebrating.
"""

import math
from typing import Dict, Any, Optional, Tuple, List
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from tools.render_core import (
    OverscanCanvas, get_font, spring,
    WHITE, DIM, CYAN, PURPLE, YELLOW, GREEN, RED, DARK_CARD, CARD_BORDER
)

def clamp(v: float, mn: float = 0.0, mx: float = 1.0) -> float:
    return max(mn, min(mx, v))

def lerp(a: float, b: float, p: float) -> float:
    return a + (b - a) * p


# ==============================================================================
# PARAMETRIC STICKMAN ACTOR RIG WITH EMOTION MARKS
# ==============================================================================
def draw_director_actor(
    canvas: OverscanCanvas,
    x: float,
    y: float,
    scale: float = 1.0,
    action: str = "idle",
    mouth_open: float = 0.0,
    blink: float = 0.0,
    expr: str = "happy",
    look: Tuple[float, float] = (0.0, 0.0),
    frame_t: float = 0.0,
    show_sunglasses: bool = False
):
    """
    Renders Kenil's iconic stickman actor with articulated skeletal actions,
    facial expressions, emotion marks (shock lines, sweat drops), and props.
    All coordinates in canvas space.
    """
    sc = canvas.scale * scale
    lw = max(2, int(4.5 * sc))
    hr = int(38 * sc)
    
    # Map (x, y) as the base pelvis/feet anchor
    cx_pix, cy_pix = canvas.to_canvas(x, y)
    hx = cx_pix
    hy = cy_pix - int(95 * sc)

    d = canvas.draw

    # 1. Hair strands on top of head (\ | /)
    hb_y = hy - hr + int(2 * sc)
    d.line([hx - int(12 * sc), hb_y, hx - int(24 * sc), hb_y - int(18 * sc)], fill=WHITE, width=max(2, int(3 * sc)))
    d.line([hx - int(4 * sc), hb_y - int(2 * sc), hx - int(6 * sc), hb_y - int(24 * sc)], fill=WHITE, width=max(2, int(3 * sc)))
    d.line([hx + int(6 * sc), hb_y - int(1 * sc), hx + int(12 * sc), hb_y - int(20 * sc)], fill=WHITE, width=max(2, int(3 * sc)))

    # 2. Head Circle (White outline, dark navy fill)
    d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=(16, 22, 38), outline=WHITE, width=lw)

    # 3. Eyebrows & Emotion Marks
    eb_y = hy - int(14 * sc)
    if expr == "surprised":
        # Shocked raised eyebrows
        d.arc([hx - int(22 * sc), eb_y - int(14 * sc), hx - int(6 * sc), eb_y + int(2 * sc)], start=200, end=340, fill=WHITE, width=max(2, int(2.5 * sc)))
        d.arc([hx + int(6 * sc), eb_y - int(14 * sc), hx + int(22 * sc), eb_y + int(2 * sc)], start=200, end=340, fill=WHITE, width=max(2, int(2.5 * sc)))
        # Shock lines around head
        d.line([hx - hr - int(8 * sc), hy - int(18 * sc), hx - hr - int(22 * sc), hy - int(26 * sc)], fill=YELLOW, width=max(2, int(3 * sc)))
        d.line([hx + hr + int(8 * sc), hy - int(18 * sc), hx + hr + int(22 * sc), hy - int(26 * sc)], fill=YELLOW, width=max(2, int(3 * sc)))
        d.line([hx, hy - hr - int(6 * sc), hx, hy - hr - int(20 * sc)], fill=YELLOW, width=max(2, int(3 * sc)))
    elif expr == "worried":
        # Angled downward eyebrows
        d.line([hx - int(22 * sc), eb_y - int(2 * sc), hx - int(6 * sc), eb_y - int(10 * sc)], fill=WHITE, width=max(2, int(2.5 * sc)))
        d.line([hx + int(6 * sc), eb_y - int(10 * sc), hx + int(22 * sc), eb_y - int(2 * sc)], fill=WHITE, width=max(2, int(2.5 * sc)))
        # Animated sweat drop
        sw_x = hx + hr + int(8 * sc)
        sw_y = hy - int(12 * sc) + int(math.sin(frame_t * 6.0) * 4 * sc)
        d.polygon([(sw_x, sw_y - int(8 * sc)), (sw_x + int(6 * sc), sw_y + int(4 * sc)), (sw_x - int(6 * sc), sw_y + int(4 * sc))], fill=CYAN)
        d.ellipse([sw_x - int(6 * sc), sw_y, sw_x + int(6 * sc), sw_y + int(8 * sc)], fill=CYAN)
    else:
        # Confident happy eyebrows
        d.arc([hx - int(22 * sc), eb_y - int(6 * sc), hx - int(6 * sc), eb_y + int(6 * sc)], start=200, end=340, fill=WHITE, width=max(2, int(2.5 * sc)))
        d.arc([hx + int(6 * sc), eb_y - int(6 * sc), hx + int(22 * sc), eb_y + int(6 * sc)], start=200, end=340, fill=WHITE, width=max(2, int(2.5 * sc)))

    # 4. Eyes or Sunglasses
    eye_y = hy - int(3 * sc)
    if show_sunglasses:
        # Cool black sunglasses
        sg_w = int(24 * sc)
        sg_h = int(14 * sc)
        d.rounded_rectangle([hx - int(26 * sc), eye_y - sg_h // 2, hx - int(2 * sc), eye_y + sg_h // 2], radius=4, fill=(10, 10, 15), outline=WHITE, width=1)
        d.rounded_rectangle([hx + int(2 * sc), eye_y - sg_h // 2, hx + int(26 * sc), eye_y + sg_h // 2], radius=4, fill=(10, 10, 15), outline=WHITE, width=1)
        d.line([hx - int(2 * sc), eye_y, hx + int(2 * sc), eye_y], fill=WHITE, width=2)
    else:
        eye_h = max(1, int(13 * sc * (1.0 - blink)))
        eye_w = int(8 * sc)
        if expr == "surprised":
            eye_w, eye_h = int(14 * sc), int(18 * sc)
        
        lx = hx - int(14 * sc) + int(look[0] * 4 * sc)
        rx = hx + int(14 * sc) + int(look[0] * 4 * sc)
        ly = eye_y + int(look[1] * 3 * sc)

        if blink < 0.75 or expr == "surprised":
            d.ellipse([lx - eye_w // 2, ly - eye_h // 2, lx + eye_w // 2, ly + eye_h // 2], fill=WHITE)
            d.ellipse([rx - eye_w // 2, ly - eye_h // 2, rx + eye_w // 2, ly + eye_h // 2], fill=WHITE)
        else:
            d.line([lx - eye_w // 2, ly, lx + eye_w // 2, ly], fill=WHITE, width=max(2, int(2.5 * sc)))
            d.line([rx - eye_w // 2, ly, rx + eye_w // 2, ly], fill=WHITE, width=max(2, int(2.5 * sc)))

    # 5. Mouth (Dynamic Lip-Sync Chord)
    my = hy + int(15 * sc)
    if mouth_open < 0.15:
        if expr == "worried":
            d.arc([hx - int(16 * sc), my - int(4 * sc), hx + int(16 * sc), my + int(12 * sc)], start=200, end=340, fill=WHITE, width=max(2, int(2.5 * sc)))
        else:
            d.arc([hx - int(22 * sc), my - int(10 * sc), hx + int(22 * sc), my + int(12 * sc)], start=25, end=155, fill=WHITE, width=max(2, int(3 * sc)))
    else:
        mw = int(28 * sc)
        mh = int(8 * sc + 18 * sc * mouth_open)
        d.chord([hx - mw // 2, my - mh // 2, hx + mw // 2, my + mh // 2], start=0, end=180, fill=(240, 50, 70), outline=WHITE, width=max(2, int(2.5 * sc)))
        d.line([hx - mw // 2, my - mh // 2, hx + mw // 2, my - mh // 2], fill=WHITE, width=max(2, int(2.5 * sc)))

    # 6. Spine / Torso
    neck_y = hy + hr
    pelvis_y = cy_pix + int(15 * sc)
    d.line([hx, neck_y, hx, pelvis_y], fill=WHITE, width=lw)
    
    # 7. Action-Specific Limbs & Choreography
    sy = neck_y + int(10 * sc)

    if action == "typing":
        # Rapid typing on keyboard
        bob_arm = math.sin(frame_t * 18.0) * 6 * sc
        d.line([hx, sy, hx + int(25 * sc), sy + int(25 * sc)], fill=WHITE, width=lw)
        d.line([hx + int(25 * sc), sy + int(25 * sc), hx + int(48 * sc), sy + int(20 * sc) + bob_arm], fill=WHITE, width=lw)
        d.line([hx, sy, hx + int(15 * sc), sy + int(30 * sc)], fill=WHITE, width=lw)
        d.line([hx + int(15 * sc), sy + int(30 * sc), hx + int(40 * sc), sy + int(24 * sc) - bob_arm], fill=WHITE, width=lw)
        # Standing legs
        d.line([hx, pelvis_y, hx - int(22 * sc), cy_pix + int(90 * sc)], fill=WHITE, width=lw)
        d.line([hx, pelvis_y, hx + int(22 * sc), cy_pix + int(90 * sc)], fill=WHITE, width=lw)

    elif action == "slam_enter":
        # Mid-air jump slam down on Enter key
        d.line([hx, sy, hx - int(25 * sc), sy - int(20 * sc)], fill=WHITE, width=lw)
        d.line([hx - int(25 * sc), sy - int(20 * sc), hx + int(45 * sc), sy + int(38 * sc)], fill=WHITE, width=lw)
        d.line([hx, sy, hx - int(10 * sc), sy - int(25 * sc)], fill=WHITE, width=lw)
        d.line([hx - int(10 * sc), sy - int(25 * sc), hx + int(50 * sc), sy + int(40 * sc)], fill=WHITE, width=lw)
        # Tucked jumping legs
        d.line([hx, pelvis_y, hx - int(35 * sc), cy_pix + int(45 * sc)], fill=WHITE, width=lw)
        d.line([hx - int(35 * sc), cy_pix + int(45 * sc), hx - int(15 * sc), cy_pix + int(70 * sc)], fill=WHITE, width=lw)
        d.line([hx, pelvis_y, hx - int(15 * sc), cy_pix + int(50 * sc)], fill=WHITE, width=lw)
        d.line([hx - int(15 * sc), cy_pix + int(50 * sc), hx + int(5 * sc), cy_pix + int(75 * sc)], fill=WHITE, width=lw)

    elif action == "karate_chop":
        # Right arm high in karate chop stance
        d.line([hx, sy, hx - int(45 * sc), sy + int(20 * sc)], fill=WHITE, width=lw)
        d.line([hx - int(45 * sc), sy + int(20 * sc), hx - int(70 * sc), sy + int(10 * sc)], fill=WHITE, width=lw)
        d.line([hx, sy, hx + int(35 * sc), sy - int(30 * sc)], fill=WHITE, width=lw)
        d.line([hx + int(35 * sc), sy - int(30 * sc), hx + int(75 * sc), sy - int(65 * sc)], fill=WHITE, width=lw)
        # Martial arts wide stance legs
        d.line([hx, pelvis_y, hx - int(45 * sc), cy_pix + int(90 * sc)], fill=WHITE, width=lw)
        d.line([hx, pelvis_y, hx + int(45 * sc), cy_pix + int(90 * sc)], fill=WHITE, width=lw)

    elif action == "pull_lever":
        # Two arms reaching up and pulling lever
        d.line([hx, sy, hx - int(20 * sc), sy - int(35 * sc)], fill=WHITE, width=lw)
        d.line([hx - int(20 * sc), sy - int(35 * sc), hx - int(55 * sc), sy - int(55 * sc)], fill=WHITE, width=lw)
        d.line([hx, sy, hx - int(10 * sc), sy - int(40 * sc)], fill=WHITE, width=lw)
        d.line([hx - int(10 * sc), sy - int(40 * sc), hx - int(48 * sc), sy - int(58 * sc)], fill=WHITE, width=lw)
        # Braced pulling legs
        d.line([hx, pelvis_y, hx - int(35 * sc), cy_pix + int(90 * sc)], fill=WHITE, width=lw)
        d.line([hx, pelvis_y, hx + int(25 * sc), cy_pix + int(90 * sc)], fill=WHITE, width=lw)

    elif action == "pushing_heavy":
        # Deep 35-degree forward lean pushing against weight block
        d.line([hx, sy, hx + int(50 * sc), sy - int(5 * sc)], fill=WHITE, width=lw)
        d.line([hx + int(50 * sc), sy - int(5 * sc), hx + int(95 * sc), sy - int(5 * sc)], fill=WHITE, width=lw)
        d.line([hx, sy, hx + int(45 * sc), sy + int(12 * sc)], fill=WHITE, width=lw)
        d.line([hx + int(45 * sc), sy + int(12 * sc), hx + int(90 * sc), sy + int(12 * sc)], fill=WHITE, width=lw)
        # Deep stride pushing legs
        d.line([hx, pelvis_y, hx - int(65 * sc), cy_pix + int(90 * sc)], fill=WHITE, width=lw)
        d.line([hx, pelvis_y, hx + int(20 * sc), cy_pix + int(90 * sc)], fill=WHITE, width=lw)

    elif action == "referee_stamp":
        # Left hand holding clipboard, right arm stamping down
        d.line([hx, sy, hx - int(30 * sc), sy + int(15 * sc)], fill=WHITE, width=lw)
        d.line([hx - int(30 * sc), sy + int(15 * sc), hx - int(50 * sc), sy - int(10 * sc)], fill=WHITE, width=lw)
        # Clipboard box
        d.rounded_rectangle([hx - int(65 * sc), sy - int(25 * sc), hx - int(38 * sc), sy + int(12 * sc)], radius=3, fill=(30, 42, 65), outline=WHITE, width=2)
        # Stamping right arm
        d.line([hx, sy, hx + int(35 * sc), sy - int(10 * sc)], fill=WHITE, width=lw)
        d.line([hx + int(35 * sc), sy - int(10 * sc), hx + int(65 * sc), sy + int(20 * sc)], fill=WHITE, width=lw)
        # Legs
        d.line([hx, pelvis_y, hx - int(22 * sc), cy_pix + int(90 * sc)], fill=WHITE, width=lw)
        d.line([hx, pelvis_y, hx + int(22 * sc), cy_pix + int(90 * sc)], fill=WHITE, width=lw)

    elif action == "celebrate":
        # Arms high in V-shape celebration, jumping slightly
        d.line([hx, sy, hx - int(35 * sc), sy - int(30 * sc)], fill=WHITE, width=lw)
        d.line([hx - int(35 * sc), sy - int(30 * sc), hx - int(55 * sc), sy - int(75 * sc)], fill=WHITE, width=lw)
        d.line([hx, sy, hx + int(35 * sc), sy - int(30 * sc)], fill=WHITE, width=lw)
        d.line([hx + int(35 * sc), sy - int(30 * sc), hx + int(55 * sc), sy - int(75 * sc)], fill=WHITE, width=lw)
        # Jumping legs
        d.line([hx, pelvis_y, hx - int(25 * sc), cy_pix + int(80 * sc)], fill=WHITE, width=lw)
        d.line([hx, pelvis_y, hx + int(25 * sc), cy_pix + int(80 * sc)], fill=WHITE, width=lw)

    else:
        # Confident speaking presenter with gesturing hands
        arm_bob = math.sin(frame_t * 6.0) * 8 * sc
        d.line([hx, sy, hx - int(38 * sc), sy - int(15 * sc)], fill=WHITE, width=lw)
        d.line([hx - int(38 * sc), sy - int(15 * sc), hx - int(70 * sc), sy - int(35 * sc) + arm_bob], fill=WHITE, width=lw)
        d.line([hx, sy, hx + int(38 * sc), sy - int(15 * sc)], fill=WHITE, width=lw)
        d.line([hx + int(38 * sc), sy - int(15 * sc), hx + int(70 * sc), sy - int(35 * sc) - arm_bob], fill=WHITE, width=lw)
        d.line([hx, pelvis_y, hx - int(22 * sc), cy_pix + int(90 * sc)], fill=WHITE, width=lw)
        d.line([hx, pelvis_y, hx + int(22 * sc), cy_pix + int(90 * sc)], fill=WHITE, width=lw)


# ==============================================================================
# 7 DIRECTOR-GRADE SCENES WITH DIRECT ACTOR PARTICIPATION
# ==============================================================================

def render_director_scene_01(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """Scene 1: Hook with Stickman frantically typing, slamming Enter, in shock at 28ms."""
    cx = canvas.W // 2
    sc = canvas.scale

    canvas.draw_pill((cx - 160, 85), "STAGE 0: THE LATENCY PUZZLE", size=18, text_color=CYAN,
                     bg_color=(18, 24, 42), outline_color=(70, 220, 255, 120))

    # Terminal prompt window (shifted slightly right to stage actor on left)
    term_box = (cx - 360, 150, cx + 520, 290)
    canvas.draw_card(term_box, radius=16, fill=(14, 18, 30), outline=(50, 70, 110), width=2)
    
    # Prompt text typing
    full_prompt = "Why is the sky blue?"
    type_p = clamp(rel_t / 1.4)
    typed = full_prompt[:int(len(full_prompt) * type_p)]
    caret = "█" if (int(rel_t * 3.0) % 2 == 0 or rel_t < 1.4) else ""
    canvas.draw_text((term_box[0] + 40, term_box[1] + 55), f"> {typed}{caret}", size=30, fill=WHITE)

    # Enter Button on right of terminal
    enter_pressed = rel_t >= 1.6
    enter_col = CYAN if enter_pressed else (45, 60, 95)
    canvas.draw_pill((term_box[2] - 150, term_box[1] + 52), "[ENTER ↵]", size=18, text_color=WHITE, bg_color=enter_col)

    # STICKMAN ACTOR ON LEFT OF TERMINAL
    if rel_t < 1.5:
        # Frantically typing
        draw_director_actor(canvas, term_box[0] - 65, term_box[1] + 85, scale=0.75, action="typing",
                            mouth_open=0.7 * abs(math.sin(rel_t * 12)), expr="happy", frame_t=rel_t)
    elif rel_t < 1.9:
        # Jumping and slamming Enter key
        draw_director_actor(canvas, term_box[2] - 140, term_box[1] + 10, scale=0.8, action="slam_enter",
                            mouth_open=0.9, expr="surprised", frame_t=rel_t)
        # Shockwave ripple
        rx, ry = canvas.to_canvas(term_box[2] - 90, term_box[1] + 70)
        canvas.draw.ellipse([rx - 120 * sc, ry - 120 * sc, rx + 120 * sc, ry + 120 * sc], outline=(70, 220, 255), width=3)
    else:
        # Blown back in shock at 28.40ms
        draw_director_actor(canvas, term_box[0] - 70, term_box[1] + 90, scale=0.75, action="idle",
                            mouth_open=0.8 * abs(math.sin(rel_t * 14)), expr="surprised", look=(0.6, 0.4), frame_t=rel_t)

    # Millisecond Stopwatch HUD (Left Center)
    sw_box = (cx - 460, 320, cx - 70, 520)
    canvas.draw_card(sw_box, radius=18, fill=(16, 22, 38), outline=(70, 220, 255, 140), width=2)
    canvas.draw_text((sw_box[0] + 30, sw_box[1] + 30), "TIME-TO-FIRST-TOKEN", size=18, fill=CYAN)

    target_ms = 28.40
    curr_ms = target_ms if rel_t >= 3.0 else (target_ms * ((rel_t - 1.6) / 1.4) ** 1.8 if rel_t >= 1.6 else 0.00)
    ms_color = YELLOW if curr_ms < target_ms else GREEN
    canvas.draw_text((sw_box[0] + 30, sw_box[1] + 75), f"{curr_ms:05.2f} ms", size=56, fill=ms_color)
    canvas.draw_text((sw_box[0] + 30, sw_box[1] + 150), "Sub-human reaction threshold", size=16, fill=DIM)

    # H100 Silicon Die Schematic (Right Center)
    die_box = (cx - 30, 320, cx + 460, 680)
    canvas.draw_card(die_box, radius=18, fill=(13, 17, 28), outline=(150, 110, 255, 140), width=2)
    canvas.draw_text((die_box[0] + 30, die_box[1] + 30), "SILICON COMPUTE HARDWARE", size=18, fill=PURPLE)
    canvas.draw_text((die_box[0] + 180, die_box[1] + 140), "H100 SXM5", size=24, fill=WHITE, anchor="mm")
    canvas.draw_text((die_box[0] + 180, die_box[1] + 175), "70 Billion Parameters", size=18, fill=CYAN, anchor="mm")

    # 140 Trillion FLOPs Banner
    if rel_t > 4.5:
        b_box = (cx - 460, 550, cx - 70, 680)
        canvas.draw_card(b_box, radius=18, fill=(28, 22, 16), outline=YELLOW, width=2)
        canvas.draw_text((b_box[0] + 25, b_box[1] + 30), "COMPUTATIONAL LOAD", size=18, fill=YELLOW)
        canvas.draw_text((b_box[0] + 25, b_box[1] + 70), "140 TRILLION", size=36, fill=YELLOW)
        canvas.draw_text((b_box[0] + 25, b_box[1] + 115), "Floating point ops in 28ms", size=16, fill=DIM)


def render_director_scene_02(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """Scene 2: Tokenization — Stickman karate-chops sentence into tokens, holds vector chips."""
    cx = canvas.W // 2
    sc = canvas.scale

    canvas.draw_pill((cx - 160, 85), "STAGE 1: TOKENIZATION & EMBEDDING", size=18, text_color=CYAN,
                     bg_color=(18, 24, 42), outline_color=(70, 220, 255, 120))

    # Sentence banner
    canvas.draw_text((cx + 50, 145), "\"Why is the sky blue?\"", size=32, fill=WHITE, anchor="mm")
    canvas.draw_text((cx + 50, 185), "Fractured into 5 discrete integer IDs", size=18, fill=DIM, anchor="mm")

    # STICKMAN KARATE CHOPPING ON LEFT
    if rel_t < 1.2:
        draw_director_actor(canvas, cx - 380, 200, scale=0.75, action="karate_chop",
                            mouth_open=0.5, expr="happy", frame_t=rel_t)
    else:
        draw_director_actor(canvas, cx - 400, 210, scale=0.75, action="idle",
                            mouth_open=0.7 * abs(math.sin(rel_t * 14)), expr="happy", look=(0.6, 0.0), frame_t=rel_t)

    # 5 Token Chips
    tokens = [("Why", 1245), ("is", 318), ("the", 262), ("sky", 7891), ("blue", 4123)]
    chip_w, chip_h = 160, 95
    start_x = cx - 240
    for i, (tok, tid) in enumerate(tokens):
        t_enter = max(0.0, rel_t - 0.6 - i * 0.12)
        p_sp = min(1.0, spring(t_enter * 1.8))
        bx = start_x + i * (chip_w + 16)
        by = 240 + (1.0 - p_sp) * 40
        
        is_highlight = tok in ["sky", "blue"] and rel_t > 3.0
        c_fill = (26, 20, 42) if is_highlight else (16, 22, 38)
        c_bord = PURPLE if is_highlight else CYAN

        canvas.draw_card((bx, by, bx + chip_w, by + chip_h), radius=12, fill=c_fill, outline=c_bord, width=2)
        canvas.draw_text((bx + chip_w // 2, by + 30), f"\"{tok}\"", size=24, fill=WHITE, anchor="mm")
        canvas.draw_pill((bx + 15, by + 55), f"ID: {tid}", size=14, text_color=CYAN, bg_color=(25, 34, 58))

    # 4096-Dim Embedding Hyperspace Grid (Bottom)
    vec_box = (cx - 460, 380, cx + 460, 680)
    canvas.draw_card(vec_box, radius=18, fill=(12, 16, 28), outline=(70, 220, 255, 100), width=1)
    canvas.draw_text((vec_box[0] + 35, vec_box[1] + 30), "4096-DIMENSIONAL EMBEDDING HYPERSPACE (d_model = 4096)", size=20, fill=CYAN)

    # Cosine Similarity Vector between 'sky' and 'blue'
    canvas.draw_pill((cx - 10, 520), "Cosine Similarity ('sky' <-> 'blue'): 0.942", size=20,
                     text_color=YELLOW, bg_color=(36, 30, 20), outline_color=YELLOW)
    canvas.draw_text((cx, 610), "Language is mapped into pure geometry.", size=18, fill=DIM, anchor="mm")


def render_director_scene_03(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """Scene 3: Prefill GEMM — Stickman pulls industrial server lever, Tensor Cores flash, dons sunglasses."""
    cx = canvas.W // 2
    sc = canvas.scale

    canvas.draw_pill((cx - 160, 85), "STAGE 2: PREFILL PHASE (COMPUTE-BOUND)", size=18, text_color=GREEN,
                     bg_color=(18, 38, 28), outline_color=GREEN)

    # STICKMAN ON FAR LEFT BESIDE INDUSTRIAL LEVER
    lever_down = rel_t >= 1.2
    if not lever_down:
        draw_director_actor(canvas, cx - 440, 240, scale=0.75, action="pull_lever",
                            mouth_open=0.6, expr="worried", frame_t=rel_t)
    else:
        draw_director_actor(canvas, cx - 440, 240, scale=0.75, action="idle",
                            mouth_open=0.7 * abs(math.sin(rel_t * 14)), expr="happy",
                            show_sunglasses=True, frame_t=rel_t)

    # Giant Industrial Power Lever
    lev_x = cx - 360
    canvas.draw_card((lev_x, 150, lev_x + 35, 310), radius=6, fill=(24, 30, 45), outline=WHITE, width=1)
    lever_angle = 35 if not lever_down else -35
    rad = math.radians(lever_angle)
    p_handle = (lev_x + 17 + math.sin(rad) * 70, 230 - math.cos(rad) * 70)
    p0 = canvas.to_canvas(lev_x + 17, 230)
    p1 = canvas.to_canvas(p_handle[0], p_handle[1])
    canvas.draw.line([p0[0], p0[1], p1[0], p1[1]], fill=(255, 70, 90), width=max(2, int(6 * sc)))
    canvas.draw.ellipse([p1[0] - 10 * sc, p1[1] - 10 * sc, p1[0] + 10 * sc, p1[1] + 10 * sc], fill=(255, 30, 50))
    canvas.draw_pill((lev_x - 30, 325), "PARALLEL GEMM", size=13, text_color=YELLOW, bg_color=(30, 25, 15))

    # Tensor Core Grid (Middle)
    tc_box = (cx - 280, 140, cx + 80, 680)
    canvas.draw_card(tc_box, radius=18, fill=(12, 18, 26), outline=GREEN, width=2)
    canvas.draw_text((tc_box[0] + 25, tc_box[1] + 25), "16 TENSOR CORE BLOCKS", size=18, fill=GREEN)
    
    # 4x4 Grid of cores
    for row in range(4):
        for col in range(4):
            bx = tc_box[0] + 25 + col * 75
            by = tc_box[1] + 65 + row * 85
            p_glow = 0.5 + 0.5 * math.sin(rel_t * 6.0 + (row * 4 + col) * 0.3)
            c_fill = (18, int(35 + 25 * p_glow), 30) if lever_down else (20, 24, 32)
            c_bord = (90, 235, 150, int(150 + 105 * p_glow)) if lever_down else (60, 75, 95)
            canvas.draw_card((bx, by, bx + 65, by + 70), radius=6, fill=c_fill, outline=c_bord, width=1)
            canvas.draw_text((bx + 32, by + 25), f"TC-{row*4+col+1:02d}", size=14, fill=WHITE, anchor="mm")
            status = "ACTIVE" if lever_down else "IDLE"
            canvas.draw_text((bx + 32, by + 50), status, size=11, fill=GREEN if lever_down else DIM, anchor="mm")

    # Attention Matrix Scanline (Right)
    mat_box = (cx + 110, 140, cx + 520, 680)
    canvas.draw_card(mat_box, radius=18, fill=(14, 18, 30), outline=CYAN, width=2)
    canvas.draw_text((mat_box[0] + 25, mat_box[1] + 25), "Q * K^T / sqrt(d) ATTENTION", size=18, fill=CYAN)
    canvas.draw_text((mat_box[0] + 25, mat_box[1] + 120), "All tokens processed\nin a single parallel step.", size=18, fill=WHITE)
    canvas.draw_pill((mat_box[0] + 25, 480), "Throughput: 989 TFLOPS", size=18, text_color=GREEN, bg_color=(20, 42, 30))
    canvas.draw_pill((mat_box[0] + 25, 545), "Status: 100% Core Saturation", size=18, text_color=WHITE, bg_color=(25, 45, 75))


def render_director_scene_04(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """Scene 4: KV Cache Split — Left: Stickman buried under papers sweating. Right: Stickman locking KV cache sipping coffee."""
    cx = canvas.W // 2
    sc = canvas.scale

    canvas.draw_pill((cx - 160, 85), "THE BOTTLENECK & THE KV CACHE FIX", size=18, text_color=YELLOW,
                     bg_color=(38, 30, 18), outline_color=YELLOW)

    # 1. Left Side: Naive O(N^2) Avalanche
    left_box = (cx - 520, 140, cx - 20, 680)
    canvas.draw_card(left_box, radius=18, fill=(24, 14, 16), outline=RED, width=2)
    canvas.draw_text((left_box[0] + 30, left_box[1] + 30), "WITHOUT CACHE (NAIVE O(N^2))", size=20, fill=RED)

    # Stickman buried under recalculation papers
    paper_cy = 380
    draw_director_actor(canvas, left_box[0] + 240, paper_cy + 15, scale=0.75, action="idle",
                        mouth_open=0.8, expr="worried", frame_t=rel_t)
    
    # Pile of papers covering stickman up to chest
    for px, py, pw in [(180, 420, 120), (240, 410, 140), (160, 435, 160), (250, 440, 130)]:
        canvas.draw_card((left_box[0] + px, py, left_box[0] + px + pw, py + 30), radius=4, fill=(240, 240, 245), outline=(150, 50, 60), width=1)
        canvas.draw_text((left_box[0] + px + 15, py + 8), "RE-COMPUTE ⚠️", size=13, fill=(180, 30, 40))

    canvas.draw_pill((left_box[0] + 30, 545), "Result: 1.2 Tokens/sec (Laggy Crash)", size=17, text_color=RED, bg_color=(45, 15, 20))

    # 2. Right Side: With KV Cache Memory Slots
    right_box = (cx + 20, 140, cx + 520, 680)
    canvas.draw_card(right_box, radius=18, fill=(12, 22, 28), outline=CYAN, width=2)
    canvas.draw_text((right_box[0] + 30, right_box[1] + 30), "WITH KV CACHE (LINEAR O(1))", size=20, fill=CYAN)

    # Stickman standing beside memory rack
    draw_director_actor(canvas, right_box[0] + 370, 330, scale=0.75, action="idle",
                        mouth_open=0.7 * abs(math.sin(rel_t * 14)), expr="happy", look=(-0.6, 0.0), frame_t=rel_t)

    # Memory slots locking into place
    words = [("Token 1", "Why"), ("Token 2", "is"), ("Token 3", "the"), ("Token 4", "sky"), ("Token 5", "blue")]
    for idx, (lbl, w) in enumerate(words):
        sy = right_box[1] + 75 + idx * 56
        locked = rel_t > (0.6 + idx * 0.4)
        c_fill = (18, 32, 40) if locked else (24, 28, 36)
        c_stat = GREEN if locked else YELLOW
        txt = "🔒 KV CACHED" if locked else "COMPUTING..."
        canvas.draw_card((right_box[0] + 30, sy, right_box[0] + 280, sy + 46), radius=8, fill=c_fill, outline=c_stat, width=1)
        canvas.draw_text((right_box[0] + 45, sy + 13), f"{lbl}: \"{w}\"", size=16, fill=WHITE)
        canvas.draw_text((right_box[0] + 175, sy + 13), txt, size=14, fill=c_stat)

    canvas.draw_pill((right_box[0] + 30, 545), "Speed: 85+ Tokens/sec (3.35 TB/s Bus)", size=17, text_color=GREEN, bg_color=(18, 42, 30))


def render_director_scene_05(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """Scene 5: Memory Bottleneck — Stickman physically pushing 140 GB weight block across silicon bridge."""
    cx = canvas.W // 2
    sc = canvas.scale

    canvas.draw_pill((cx - 160, 85), "STAGE 3: THE DECODE BOTTLENECK", size=18, text_color=RED,
                     bg_color=(38, 18, 22), outline_color=RED)

    # H100 Floorplan
    chip_box = (cx - 520, 140, cx + 520, 480)
    canvas.draw_card(chip_box, radius=18, fill=(13, 17, 28), outline=CYAN, width=2)
    canvas.draw_text((chip_box[0] + 30, chip_box[1] + 25), "NVIDIA H100 SILICON INTERPOSER BRIDGE", size=20, fill=CYAN)

    # Left HBM3 Stack
    canvas.draw_card((chip_box[0] + 30, chip_box[1] + 70, chip_box[0] + 220, chip_box[3] - 40), radius=12, fill=(20, 28, 52), outline=CYAN, width=2)
    canvas.draw_text((chip_box[0] + 50, chip_box[1] + 100), "HBM3 VRAM\n40 GB", size=20, fill=WHITE)

    # Right HBM3 Stack
    canvas.draw_card((chip_box[2] - 220, chip_box[1] + 70, chip_box[2] - 30, chip_box[3] - 40), radius=12, fill=(20, 28, 52), outline=CYAN, width=2)
    canvas.draw_text((chip_box[2] - 200, chip_box[1] + 100), "HBM3 VRAM\n40 GB", size=20, fill=WHITE)

    # Center Silicon Bridge (Interposer)
    bridge_y = 330
    canvas.draw_card((cx - 180, bridge_y - 20, cx + 180, bridge_y + 40), radius=8, fill=(28, 36, 56), outline=(70, 220, 255, 120), width=1)
    canvas.draw_text((cx, bridge_y + 10), "Silicon Interposer Highway (3.35 TB/s)", size=16, fill=CYAN, anchor="mm")

    # STICKMAN PUSHING HEAVY 140 GB BOULDER BLOCK
    push_pos_x = cx - 110 + int(math.sin(rel_t * 2.0) * 20)
    draw_director_actor(canvas, push_pos_x, bridge_y - 20, scale=0.7, action="pushing_heavy",
                        mouth_open=0.7 * abs(math.sin(rel_t * 14)), expr="worried", frame_t=rel_t)

    # Giant 140 GB Weight Block
    block_x = push_pos_x + 55
    canvas.draw_card((block_x, bridge_y - 95, block_x + 110, bridge_y + 15), radius=10, fill=(45, 20, 30), outline=(255, 70, 90), width=2)
    canvas.draw_text((block_x + 55, bridge_y - 55), "140 GB", size=24, fill=WHITE, anchor="mm")
    canvas.draw_text((block_x + 55, bridge_y - 25), "WEIGHTS", size=16, fill=YELLOW, anchor="mm")

    # Bottleneck telemetry gauges (Bottom)
    g_box = (cx - 520, 510, cx + 520, 680)
    canvas.draw_card(g_box, radius=16, fill=(16, 20, 32), outline=(255, 70, 90, 100), width=1)
    canvas.draw_text((cx, g_box[1] + 40), "Every single token requires streaming all 140 GB of model weights through silicon.", size=19, fill=WHITE, anchor="mm")
    canvas.draw_pill((cx - 180, g_box[1] + 85), "Compute Cores: 22% (IDLING)", size=18, text_color=DIM, bg_color=(24, 30, 48))
    canvas.draw_pill((cx + 10, g_box[1] + 85), "Memory Bus: 100% SATURATED", size=18, text_color=WHITE, bg_color=(255, 30, 50))


def render_director_scene_06(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """Scene 6: Speculative Race — Referee Stickman stamping checkmarks as mini 1B sprinter dashes past."""
    cx = canvas.W // 2
    sc = canvas.scale

    canvas.draw_pill((cx - 160, 85), "THE SUPERCHARGER: SPECULATIVE DECODING", size=18, text_color=CYAN,
                     bg_color=(18, 28, 48), outline_color=CYAN)

    # 1. Lane 1: 1B Draft Model Sprinter
    l1_box = (cx - 520, 150, cx + 520, 310)
    canvas.draw_card(l1_box, radius=16, fill=(14, 22, 38), outline=CYAN, width=2)
    canvas.draw_text((l1_box[0] + 30, l1_box[1] + 25), "1B DRAFT MODEL (LIGHTNING SPRINTER) -> Generates 4 Candidate Tokens", size=18, fill=CYAN)

    # Mini 1B Sprinter Stickman running fast across top lane
    sprinter_x = l1_box[0] + 120 + int((rel_t * 220) % 850)
    draw_director_actor(canvas, sprinter_x, l1_box[1] + 130, scale=0.45, action="slam_enter",
                        mouth_open=0.8, expr="happy", frame_t=rel_t)

    # 2. Lane 2: 70B Target Model Validation & Referee Stickman
    l2_box = (cx - 520, 340, cx + 520, 520)
    canvas.draw_card(l2_box, radius=16, fill=(22, 16, 36), outline=PURPLE, width=2)
    canvas.draw_text((l2_box[0] + 30, l2_box[1] + 25), "70B TARGET MODEL (ONE-SHOT VERIFICATION)", size=18, fill=PURPLE)

    # Referee Stickman stamping checkmarks
    draw_director_actor(canvas, l2_box[0] + 80, l2_box[1] + 145, scale=0.7, action="referee_stamp",
                        mouth_open=0.7 * abs(math.sin(rel_t * 14)), expr="happy", frame_t=rel_t)

    # Candidate Tokens with checkmarks
    words = ["the", "architecture", "is", "scalable"]
    for i, w in enumerate(words):
        bx = l2_box[0] + 190 + i * 180
        by = l2_box[1] + 70
        is_verified = rel_t > (1.8 + i * 0.3)
        v_col = GREEN if is_verified else PURPLE
        v_txt = "✓ ACCEPTED" if is_verified else "PENDING..."
        canvas.draw_card((bx, by, bx + 160, by + 65), radius=10, fill=(28, 20, 46), outline=v_col, width=1)
        canvas.draw_text((bx + 80, by + 24), f"\"{w}\"", size=19, fill=WHITE, anchor="mm")
        canvas.draw_text((bx + 80, by + 48), v_txt, size=14, fill=v_col, anchor="mm")

    # Multiplier Badge
    if rel_t > 3.0:
        canvas.draw_pill((cx - 150, 560), "⚡ 2.8x INFERENCE SPEEDUP", size=26, text_color=YELLOW, bg_color=(36, 30, 18), outline_color=YELLOW)


def render_director_scene_07(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any], logo_img: Optional[Image.Image] = None):
    """Scene 7: Outro — Stickman jumps and stomps the red SUBSCRIBE button, confetti explosion, cheers."""
    cx = canvas.W // 2
    cy = canvas.H // 2 - 20
    sc = canvas.scale

    if rel_t < 2.5:
        # Architecture recap
        canvas.draw_pill((cx - 160, 85), "THE 5 PILLARS OF MILLISECOND AI", size=18, text_color=CYAN,
                         bg_color=(18, 24, 42), outline_color=(70, 220, 255, 120))
        
        # Stickman walking across recap stage
        draw_director_actor(canvas, cx - 280 + int(rel_t * 60), 450, scale=0.8, action="idle",
                            mouth_open=0.7 * abs(math.sin(rel_t * 14)), expr="happy", frame_t=rel_t)
        canvas.draw_text((cx + 120, 320), "AI speed isn't magic.\nIt's the pinnacle of computer architecture.", size=30, fill=WHITE, anchor="mm")

    else:
        # Official Outro Conversion Card with Stickman Stomping Subscribe Button
        rel_outro = rel_t - 2.5
        card_box = (cx - 460, cy - 250, cx + 460, cy + 250)
        canvas.draw_card(card_box, radius=24, fill=(16, 22, 38), outline=(255, 70, 90, 140), width=2)

        if logo_img:
            logo_sz = int(140 * sc)
            resized_logo = logo_img.resize((logo_sz, logo_sz), Image.Resampling.LANCZOS)
            lx, ly = canvas.to_canvas(cx - 70, cy - 200)
            canvas.frame.paste(resized_logo, (int(lx), int(ly)), resized_logo)

        canvas.draw_text((cx, cy - 35), "TECHXKENIL", size=42, fill=WHITE, anchor="mm")
        canvas.draw_text((cx, cy + 15), "AI • TECH • CODE", size=20, fill=(150, 170, 220), anchor="mm")

        # The Subscribe Button
        btn_w, btn_h = 280, 68
        bx0, by0 = cx - btn_w // 2, cy + 85
        is_clicked = rel_outro >= 2.0

        if not is_clicked:
            canvas.draw_card((bx0, by0, bx0 + btn_w, by0 + btn_h), radius=btn_h // 2, fill=(255, 30, 50), outline=None)
            canvas.draw_text((cx, by0 + btn_h // 2), "SUBSCRIBE", size=24, fill=WHITE, anchor="mm")
            # Stickman jumping towards the button
            draw_director_actor(canvas, cx + 220 - int(rel_outro * 70), by0 - 20, scale=0.75, action="slam_enter",
                                mouth_open=0.8, expr="happy", frame_t=rel_t)
        else:
            # Button stomped into green
            canvas.draw_card((bx0, by0, bx0 + btn_w, by0 + btn_h), radius=btn_h // 2, fill=(35, 195, 110), outline=None)
            canvas.draw_text((cx, by0 + btn_h // 2), "✓ SUBSCRIBED!", size=24, fill=WHITE, anchor="mm")
            
            # Gold Confetti burst particles
            rng = np.random.default_rng(77)
            for _ in range(24):
                px = cx + rng.integers(-220, 220)
                py = by0 + rng.integers(-100, 100)
                col = [(255, 205, 70), (70, 220, 255), (90, 235, 150)][rng.integers(0, 3)]
                p_c = canvas.to_canvas(px, py)
                canvas.draw.ellipse([p_c[0] - 4 * sc, p_c[1] - 4 * sc, p_c[0] + 4 * sc, p_c[1] + 4 * sc], fill=col)

            # Stickman standing on button cheering happily
            draw_director_actor(canvas, cx + 240, by0 + 20, scale=0.75, action="celebrate",
                                mouth_open=0.8, expr="happy", frame_t=rel_t)
