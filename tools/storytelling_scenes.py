#!/usr/bin/env python3
"""
storytelling_scenes.py — Master Storytelling Visual Scenes for 'How AI Answers in Milliseconds'
Features full-bleed 1920x1080 cinematic environments, life-sized expressive Stickman actor,
and relatable real-world physical metaphors:
1. The 10-Mile Library Sprint (Study desk, highway, towering library)
2. Slicing Words into Bread & The 3D Constellation Map (Bakery kitchen, cleaver chop, vector stars)
3. The 1,000-Worker Factory & Parallel Forklift (Warehouse, robotic crane claws, simultaneous prefill)
4. The Detective Corkboard & Golden Sticky Notes (Amnesia panic vs relaxed coffee KV cache)
5. The Canyon Suspension Bridge & Overloaded Truck (Delivery truck, traffic jam, idling chef)
6. The Wise Professor & The Hyperactive Intern (1B sprinter kid + 70B professor stamp)
7. The Olympic Relay Race & Victory Dropkick Outro (Stadium track, dropkick stomp, confetti burst)
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
# LIFE-SIZED VECTOR STICKMAN RIG (KENIL'S AVATAR)
# ==============================================================================
def draw_life_stickman(
    canvas: OverscanCanvas,
    x: float,                  # Base ground X
    y: float,                  # Base ground Y (feet contact)
    height: float = 340.0,     # Life-sized actor (300 to 440px)
    action: str = "idle",      # Poses: idle, typing, sprint, screech, chef_chop, pull_lever,
                               #        coffee_relax, panic_amnesia, push_truck, intern_dash,
                               #        professor_stamp, dropkick, celebrate
    mouth_open: float = 0.0,   # 0.0 (smile) to 1.0 (open talking)
    blink: float = 0.0,        # 0.0 (open eye) to 1.0 (blink)
    expr: str = "happy",       # happy, surprised, worried, determined, thinking
    look: Tuple[float, float] = (0.0, 0.0),
    hat: Optional[str] = None, # "chef", "sweatband", "goggles", "intern_cap", "professor_glasses"
    held_item: Optional[str] = None, # "pen", "cleaver", "coffee_mug", "baton", "rubber_stamp"
    facing_right: bool = True,
    frame_t: float = 0.0
):
    """
    Renders Kenil's life-sized, high-contrast expressive stickman actor matching the
    uploaded reference image and cozy storytelling art style:
    - Pure solid white filled head with bold dark ink outline
    - 3 spiky hair strands on top
    - Expressive dark eyebrows and blinkable oval pupils
    - Dynamic speaking mouth with interior color
    - Thick articulated ink limbs and cute sneaker shoes
    """
    sc = canvas.scale * (height / 340.0)
    lw = max(3, int(5.0 * sc))
    hr = int(44 * sc)
    flip = 1 if facing_right else -1

    # Base feet anchor to canvas pixels
    cx_pix, cy_pix = canvas.to_canvas(x, y)
    d = canvas.draw

    # Vertical hierarchy
    # Feet at cy_pix, Pelvis at cy_pix - 130*sc, Neck at cy_pix - 245*sc, Head at cy_pix - 290*sc
    hx = cx_pix
    hy = cy_pix - int(290 * sc)
    neck_y = cy_pix - int(245 * sc)
    pelvis_y = cy_pix - int(130 * sc)
    pelvis_x = cx_pix

    # Animation bobbing & idle breathing
    bob = int(math.sin(frame_t * 5.0) * (3.0 * sc))
    hy += bob
    neck_y += bob

    # --------------------------------------------------------------------------
    # 1. Torso & Spine
    # --------------------------------------------------------------------------
    torso_color = (25, 30, 45)
    d.line([hx, neck_y, pelvis_x, pelvis_y], fill=torso_color, width=lw)

    # --------------------------------------------------------------------------
    # 2. Legs & Sneaker Shoes
    # --------------------------------------------------------------------------
    hip_w = int(12 * sc)
    l_hip = (pelvis_x - hip_w, pelvis_y)
    r_hip = (pelvis_x + hip_w, pelvis_y)

    def draw_foot(fx: float, fy: float, f_flip: int):
        # Sneaker with white sole and red/blue upper
        shoe_w = int(24 * sc)
        shoe_h = int(10 * sc)
        d.rounded_rectangle(
            [fx - (shoe_w // 2 if f_flip > 0 else shoe_w // 3), fy - shoe_h,
             fx + (shoe_w // 2 if f_flip > 0 else shoe_w * 2 // 3), fy],
            radius=int(4 * sc), fill=(235, 60, 70), outline=torso_color, width=max(1, int(1.5 * sc))
        )
        d.line([fx - shoe_w // 2, fy, fx + shoe_w // 2, fy], fill=(255, 255, 255), width=max(2, int(2.5 * sc)))

    if action == "sprint" or action == "intern_dash":
        # Dynamic running stride
        stride_phase = frame_t * 14.0
        s_sin = math.sin(stride_phase)
        s_cos = math.cos(stride_phase)

        lkx = l_hip[0] + int(flip * s_sin * 35 * sc)
        lky = pelvis_y + int(60 * sc + abs(s_cos) * 15 * sc)
        lfx = lkx + int(flip * s_sin * 40 * sc)
        lfy = cy_pix - int(max(0.0, s_cos * 25 * sc))

        rkx = r_hip[0] - int(flip * s_sin * 35 * sc)
        rky = pelvis_y + int(60 * sc + abs(s_sin) * 15 * sc)
        rfx = rkx - int(flip * s_sin * 40 * sc)
        rfy = cy_pix - int(max(0.0, -s_cos * 25 * sc))

        d.line([l_hip[0], l_hip[1], lkx, lky, lfx, lfy], fill=torso_color, width=lw)
        d.line([r_hip[0], r_hip[1], rkx, rky, rfx, rfy], fill=torso_color, width=lw)
        draw_foot(lfx, lfy, flip)
        draw_foot(rfx, rfy, flip)

    elif action == "screech":
        # Braced back skid pose
        lfx, lfy = cx_pix - int(flip * 60 * sc), cy_pix
        rfx, rfy = cx_pix - int(flip * 20 * sc), cy_pix
        d.line([l_hip[0], l_hip[1], cx_pix - int(flip * 40 * sc), cy_pix - int(50 * sc), lfx, lfy], fill=torso_color, width=lw)
        d.line([r_hip[0], r_hip[1], cx_pix - int(flip * 10 * sc), cy_pix - int(50 * sc), rfx, rfy], fill=torso_color, width=lw)
        draw_foot(lfx, lfy, flip)
        draw_foot(rfx, rfy, flip)
        # Smoke skid lines on ground
        for k in range(3):
            sk_x = lfx - int(flip * (15 + k * 18) * sc)
            d.line([sk_x, cy_pix, sk_x + int(flip * 12 * sc), cy_pix], fill=(180, 190, 210), width=max(2, int(3 * sc)))

    elif action == "coffee_relax":
        # Seated with legs crossed
        lkx, lky = l_hip[0] + int(flip * 45 * sc), pelvis_y + int(50 * sc)
        lfx, lfy = lkx + int(flip * 15 * sc), cy_pix
        rkx, rky = r_hip[0] + int(flip * 55 * sc), pelvis_y + int(35 * sc) # crossed over
        rfx, rfy = rkx + int(flip * 25 * sc), pelvis_y + int(70 * sc)
        d.line([l_hip[0], l_hip[1], lkx, lky, lfx, lfy], fill=torso_color, width=lw)
        d.line([r_hip[0], r_hip[1], rkx, rky, rfx, rfy], fill=torso_color, width=lw)
        draw_foot(lfx, lfy, flip)
        draw_foot(rfx, rfy, flip)

    elif action == "dropkick":
        # Flying horizontal kick pose
        lfx, lfy = cx_pix + int(flip * 75 * sc), cy_pix - int(60 * sc)
        rfx, rfy = cx_pix + int(flip * 40 * sc), cy_pix - int(30 * sc)
        d.line([l_hip[0], l_hip[1], cx_pix + int(flip * 35 * sc), cy_pix - int(50 * sc), lfx, lfy], fill=torso_color, width=lw)
        d.line([r_hip[0], r_hip[1], cx_pix + int(flip * 15 * sc), cy_pix - int(25 * sc), rfx, rfy], fill=torso_color, width=lw)
        draw_foot(lfx, lfy, flip)
        draw_foot(rfx, rfy, flip)

    else:
        # Standard natural stance
        lfx, lfy = cx_pix - int(25 * sc), cy_pix
        rfx, rfy = cx_pix + int(25 * sc), cy_pix
        lkx, lky = cx_pix - int(22 * sc), pelvis_y + int(65 * sc)
        rkx, rkx_y = cx_pix + int(22 * sc), pelvis_y + int(65 * sc)
        d.line([l_hip[0], l_hip[1], lkx, lky, lfx, lfy], fill=torso_color, width=lw)
        d.line([r_hip[0], r_hip[1], rkx, rkx_y, rfx, rfy], fill=torso_color, width=lw)
        draw_foot(lfx, lfy, -1)
        draw_foot(rfx, rfy, 1)

    # --------------------------------------------------------------------------
    # 3. Head & Hair (Solid White Fill, Crisp Dark Ink Outline)
    # --------------------------------------------------------------------------
    # Hair strands (\ | /)
    hb_y = hy - hr + int(3 * sc)
    d.line([hx - int(14 * sc), hb_y, hx - int(28 * sc), hb_y - int(22 * sc)], fill=torso_color, width=max(2, int(3.5 * sc)))
    d.line([hx - int(4 * sc), hb_y - int(2 * sc), hx - int(7 * sc), hb_y - int(28 * sc)], fill=torso_color, width=max(2, int(3.5 * sc)))
    d.line([hx + int(8 * sc), hb_y - int(1 * sc), hx + int(16 * sc), hb_y - int(24 * sc)], fill=torso_color, width=max(2, int(3.5 * sc)))

    # Solid White Head Circle
    d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=(255, 255, 255), outline=torso_color, width=lw)

    # Eyebrows
    eb_y = hy - int(16 * sc)
    if expr == "surprised" or action == "screech":
        # Raised high in shock
        d.arc([hx - int(26 * sc), eb_y - int(18 * sc), hx - int(8 * sc), eb_y + int(2 * sc)], start=190, end=350, fill=torso_color, width=max(2, int(3 * sc)))
        d.arc([hx + int(8 * sc), eb_y - int(18 * sc), hx + int(26 * sc), eb_y + int(2 * sc)], start=190, end=350, fill=torso_color, width=max(2, int(3 * sc)))
        # Sweat droplet flying off head
        sw_x = hx + int(flip * (hr + 16 * sc))
        d.ellipse([sw_x - int(5 * sc), hy - int(20 * sc), sw_x + int(5 * sc), hy - int(10 * sc)], fill=(80, 210, 255), outline=torso_color, width=1)
    elif expr == "worried" or action == "panic_amnesia":
        # Slanted worried brows
        d.line([hx - int(24 * sc), eb_y, hx - int(8 * sc), eb_y - int(8 * sc)], fill=torso_color, width=max(2, int(3 * sc)))
        d.line([hx + int(8 * sc), eb_y - int(8 * sc), hx + int(24 * sc), eb_y], fill=torso_color, width=max(2, int(3 * sc)))
    elif expr == "determined":
        # Focused sharp inward slant
        d.line([hx - int(24 * sc), eb_y - int(8 * sc), hx - int(8 * sc), eb_y], fill=torso_color, width=max(2, int(3.5 * sc)))
        d.line([hx + int(8 * sc), eb_y, hx + int(24 * sc), eb_y - int(8 * sc)], fill=torso_color, width=max(2, int(3.5 * sc)))
    else:
        # Relaxed friendly arched brows
        d.arc([hx - int(24 * sc), eb_y - int(8 * sc), hx - int(8 * sc), eb_y + int(8 * sc)], start=200, end=340, fill=torso_color, width=max(2, int(2.5 * sc)))
        d.arc([hx + int(8 * sc), eb_y - int(8 * sc), hx + int(24 * sc), eb_y + int(8 * sc)], start=200, end=340, fill=torso_color, width=max(2, int(2.5 * sc)))

    # Eyes (Blinkable oval pupils)
    eye_y = hy - int(4 * sc)
    eye_h = max(1, int(15 * sc * (1.0 - blink)))
    eye_w = int(9 * sc)
    lx = hx - int(16 * sc) + int(look[0] * 5 * sc)
    rx = hx + int(16 * sc) + int(look[0] * 5 * sc)
    ly = eye_y + int(look[1] * 4 * sc)

    if blink < 0.8:
        d.ellipse([lx - eye_w // 2, ly - eye_h // 2, lx + eye_w // 2, ly + eye_h // 2], fill=torso_color)
        d.ellipse([rx - eye_w // 2, ly - eye_h // 2, rx + eye_w // 2, ly + eye_h // 2], fill=torso_color)
    else:
        d.line([lx - eye_w // 2, ly, lx + eye_w // 2, ly], fill=torso_color, width=max(2, int(3 * sc)))
        d.line([rx - eye_w // 2, ly, rx + eye_w // 2, ly], fill=torso_color, width=max(2, int(3 * sc)))

    # Mouth (Dynamic speaking or smiling)
    my = hy + int(18 * sc)
    if action == "screech" or action == "panic_amnesia":
        # Dropped jaw in shock
        mw, mh = int(24 * sc), int(30 * sc)
        d.ellipse([hx - mw // 2, my - mh // 2, hx + mw // 2, my + mh // 2], fill=(210, 45, 60), outline=torso_color, width=max(2, int(2.5 * sc)))
    elif mouth_open < 0.15:
        # Friendly wide smile
        d.arc([hx - int(24 * sc), my - int(14 * sc), hx + int(24 * sc), my + int(14 * sc)], start=25, end=155, fill=torso_color, width=max(2, int(3.5 * sc)))
    else:
        # Talking mouth chord with red interior and teeth
        mw = int(32 * sc)
        mh = int(lerp(10 * sc, 26 * sc, mouth_open))
        d.chord([hx - mw // 2, my - mh // 2, hx + mw // 2, my + mh // 2], start=0, end=180, fill=(225, 50, 70), outline=torso_color, width=max(2, int(2.5 * sc)))
        d.line([hx - mw // 2, my - mh // 2, hx + mw // 2, my - mh // 2], fill=torso_color, width=max(2, int(2.5 * sc)))
        # Upper white teeth strip
        d.rectangle([hx - mw // 3, my - mh // 2 + int(1 * sc), hx + mw // 3, my - mh // 2 + int(4 * sc)], fill=(255, 255, 255))

    # --------------------------------------------------------------------------
    # 4. Hats & Costume Accessories
    # --------------------------------------------------------------------------
    if hat == "chef":
        # Tall pleated chef's hat
        ch_y = hy - hr - int(8 * sc)
        ch_w = int(70 * sc)
        ch_h = int(55 * sc)
        # Puff top
        d.ellipse([hx - ch_w // 2, ch_y - ch_h, hx + ch_w // 2, ch_y - ch_h // 2], fill=(250, 250, 255), outline=torso_color, width=max(2, int(2.5 * sc)))
        # Band
        d.rectangle([hx - int(38 * sc), ch_y - ch_h // 2, hx + int(38 * sc), ch_y + int(4 * sc)], fill=(255, 255, 255), outline=torso_color, width=max(2, int(2.5 * sc)))

    elif hat == "sweatband":
        # Red runner's sweatband
        sb_y = hy - int(18 * sc)
        d.rectangle([hx - hr - int(2 * sc), sb_y - int(6 * sc), hx + hr + int(2 * sc), sb_y + int(6 * sc)], fill=(245, 50, 60), outline=torso_color, width=max(1, int(1.5 * sc)))

    elif hat == "intern_cap":
        # Backwards red baseball cap
        cp_y = hy - hr + int(10 * sc)
        d.chord([hx - hr - int(3 * sc), cp_y - int(25 * sc), hx + hr + int(3 * sc), cp_y + int(20 * sc)], start=180, end=360, fill=(235, 45, 60), outline=torso_color, width=max(2, int(2 * sc)))
        # Brim pointing backward
        d.polygon([hx - hr - int(2 * sc), cp_y, hx - hr - int(26 * sc), cp_y - int(6 * sc), hx - hr, cp_y + int(6 * sc)], fill=(235, 45, 60), outline=torso_color)

    elif hat == "professor_glasses":
        # Round reading glasses
        gy = hy - int(4 * sc)
        gr = int(12 * sc)
        d.ellipse([lx - gr, gy - gr, lx + gr, gy + gr], outline=torso_color, width=max(2, int(2.5 * sc)))
        d.ellipse([rx - gr, gy - gr, rx + gr, gy + gr], outline=torso_color, width=max(2, int(2.5 * sc)))
        d.line([lx + gr, gy, rx - gr, gy], fill=torso_color, width=max(2, int(2.5 * sc)))
        # Bowtie at neck
        d.polygon([hx - int(16 * sc), neck_y - int(6 * sc), hx + int(16 * sc), neck_y + int(6 * sc), hx, neck_y], fill=(235, 60, 70))
        d.polygon([hx + int(16 * sc), neck_y - int(6 * sc), hx - int(16 * sc), neck_y + int(6 * sc), hx, neck_y], fill=(235, 60, 70))

    # --------------------------------------------------------------------------
    # 5. Arms & Held Item Props
    # --------------------------------------------------------------------------
    sh_y = neck_y + int(15 * sc)

    if action == "sprint" or action == "intern_dash":
        # Pumping sprint arms
        arm_phase = frame_t * 14.0
        a_sin = math.sin(arm_phase)
        lex = hx - int(flip * a_sin * 35 * sc)
        ley = sh_y + int(25 * sc)
        lhx = lex - int(flip * a_sin * 25 * sc)
        lhy = ley - int(20 * sc)

        rex = hx + int(flip * a_sin * 35 * sc)
        rey = sh_y + int(25 * sc)
        rhx = rex + int(flip * a_sin * 25 * sc)
        rhy = rey - int(20 * sc)

        d.line([hx - int(10 * sc), sh_y, lex, ley, lhx, lhy], fill=torso_color, width=lw)
        d.line([hx + int(10 * sc), sh_y, rex, rey, rhx, rhy], fill=torso_color, width=lw)

        if held_item == "baton":
            # Golden relay baton in forward hand
            bx, by = (rhx, rhy) if flip * a_sin > 0 else (lhx, lhy)
            d.line([bx - int(15 * sc), by - int(10 * sc), bx + int(15 * sc), by + int(10 * sc)], fill=YELLOW, width=max(3, int(5 * sc)))

    elif action == "chef_chop":
        # Right arm holds cleaver high or chopping down
        chop_p = abs(math.sin(frame_t * 8.0))
        rex = hx + int(flip * 45 * sc)
        rey = sh_y - int(20 * sc + chop_p * 35 * sc)
        rhx = rex + int(flip * 25 * sc)
        rhy = rey + int(chop_p * 45 * sc)

        # Left arm stabilizing counter
        lex = hx - int(flip * 35 * sc)
        ley = sh_y + int(45 * sc)
        lhx = lex - int(flip * 20 * sc)
        lhy = cy_pix - int(20 * sc)

        d.line([hx - int(8 * sc), sh_y, lex, ley, lhx, lhy], fill=torso_color, width=lw)
        d.line([hx + int(8 * sc), sh_y, rex, rey, rhx, rhy], fill=torso_color, width=lw)

        # Steel Cleaver
        clv_w, clv_h = int(38 * sc), int(22 * sc)
        clv_x = rhx + int(flip * 15 * sc)
        clv_y = rhy - int(10 * sc)
        d.polygon([
            clv_x, clv_y,
            clv_x + int(flip * clv_w), clv_y,
            clv_x + int(flip * clv_w), clv_y + clv_h,
            clv_x, clv_y + clv_h - int(4 * sc)
        ], fill=(210, 220, 235), outline=torso_color, width=max(1, int(1.5 * sc)))
        # Wooden handle
        d.line([rhx - int(flip * 10 * sc), rhy, clv_x, clv_y + clv_h // 2], fill=(130, 80, 50), width=max(3, int(4 * sc)))

    elif action == "coffee_relax":
        # Left arm relaxed on lap, right hand holding steaming coffee mug
        lex = hx - int(flip * 30 * sc)
        ley = sh_y + int(40 * sc)
        lhx = lex + int(flip * 15 * sc)
        lhy = pelvis_y + int(20 * sc)

        rex = hx + int(flip * 35 * sc)
        rey = sh_y + int(30 * sc)
        rhx = rex + int(flip * 15 * sc)
        rhy = sh_y - int(10 * sc)

        d.line([hx - int(8 * sc), sh_y, lex, ley, lhx, lhy], fill=torso_color, width=lw)
        d.line([hx + int(8 * sc), sh_y, rex, rey, rhx, rhy], fill=torso_color, width=lw)

        # Ceramic Coffee Mug
        mw, mh = int(20 * sc), int(22 * sc)
        d.rectangle([rhx, rhy - mh // 2, rhx + mw, rhy + mh // 2], fill=(245, 245, 255), outline=torso_color, width=max(1, int(2 * sc)))
        d.arc([rhx + mw - int(2 * sc), rhy - mh // 3, rhx + mw + int(10 * sc), rhy + mh // 3], start=270, end=90, fill=torso_color, width=max(1, int(2 * sc)))
        # Steam swirls
        steam_y = rhy - mh // 2 - int(6 * sc)
        d.arc([rhx + int(4 * sc), steam_y - int(12 * sc), rhx + int(12 * sc), steam_y], start=180, end=360, fill=(200, 215, 235), width=max(1, int(1.5 * sc)))

    elif action == "pull_lever":
        # Right hand gripped to high lever, pulling down
        rex = hx + int(flip * 45 * sc)
        rey = sh_y - int(30 * sc)
        rhx = rex + int(flip * 30 * sc)
        rhy = rey - int(20 * sc)

        lex = hx - int(flip * 30 * sc)
        ley = sh_y + int(35 * sc)
        lhx = lex - int(flip * 15 * sc)
        lhy = pelvis_y + int(20 * sc)

        d.line([hx - int(8 * sc), sh_y, lex, ley, lhx, lhy], fill=torso_color, width=lw)
        d.line([hx + int(8 * sc), sh_y, rex, rey, rhx, rhy], fill=torso_color, width=lw)

    elif action == "professor_stamp":
        # Left hand holding paper, right hand holding giant wooden stamp slamming desk
        stamp_p = abs(math.sin(frame_t * 6.0))
        rex = hx + int(flip * 40 * sc)
        rey = sh_y - int(15 * sc + stamp_p * 35 * sc)
        rhx = rex + int(flip * 20 * sc)
        rhy = rey + int(stamp_p * 45 * sc)

        lex = hx - int(flip * 35 * sc)
        ley = sh_y + int(35 * sc)
        lhx = lex + int(flip * 15 * sc)
        lhy = cy_pix - int(50 * sc)

        d.line([hx - int(8 * sc), sh_y, lex, ley, lhx, lhy], fill=torso_color, width=lw)
        d.line([hx + int(8 * sc), sh_y, rex, rey, rhx, rhy], fill=torso_color, width=lw)

        # Giant Red Rubber Stamp
        st_w, st_h = int(24 * sc), int(28 * sc)
        d.rectangle([rhx - st_w // 2, rhy, rhx + st_w // 2, rhy + int(10 * sc)], fill=(220, 45, 55), outline=torso_color, width=max(1, int(1.5 * sc)))
        d.line([rhx, rhy, rhx, rhy - int(18 * sc)], fill=(120, 70, 40), width=max(3, int(5 * sc)))
        d.ellipse([rhx - int(6 * sc), rhy - int(24 * sc), rhx + int(6 * sc), rhy - int(14 * sc)], fill=(120, 70, 40))

    elif action == "dropkick":
        # Both arms back for aerodynamic kick
        d.line([hx - int(8 * sc), sh_y, hx - int(flip * 45 * sc), sh_y + int(15 * sc)], fill=torso_color, width=lw)
        d.line([hx + int(8 * sc), sh_y, hx - int(flip * 35 * sc), sh_y + int(30 * sc)], fill=torso_color, width=lw)

    elif action == "celebrate":
        # Both arms raised high in triumphant victory \o/
        d.line([hx - int(8 * sc), sh_y, hx - int(35 * sc), sh_y - int(40 * sc), hx - int(50 * sc), sh_y - int(80 * sc)], fill=torso_color, width=lw)
        d.line([hx + int(8 * sc), sh_y, hx + int(35 * sc), sh_y - int(40 * sc), hx + int(50 * sc), sh_y - int(80 * sc)], fill=torso_color, width=lw)

    else:
        # Relaxed natural talking gesture
        lex = hx - int(25 * sc)
        ley = sh_y + int(40 * sc)
        lhx = lex - int(15 * sc)
        lhy = pelvis_y + int(10 * sc)

        gest = math.sin(frame_t * 6.0) * (15.0 * sc)
        rex = hx + int(30 * sc)
        rey = sh_y + int(35 * sc)
        rhx = rex + int(flip * (25 * sc + gest))
        rhy = rey - int(25 * sc + gest)

        d.line([hx - int(8 * sc), sh_y, lex, ley, lhx, lhy], fill=torso_color, width=lw)
        d.line([hx + int(8 * sc), sh_y, rex, rey, rhx, rhy], fill=torso_color, width=lw)


# ==============================================================================
# SCENE 1: THE 10-MILE LIBRARY SPRINT (FULL-SCREEN HOOK)
# ==============================================================================
def render_story_library_sprint(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """
    Hook Story:
    Full-bleed twilight highway spanning (0, 0, 1920, 1080).
    Left: Cozy study room desk with warm banker's lamp.
    Center: Long asphalt highway with distance markers ("START", "MILE 5", "MILE 10").
    Right: Towering 70-Billion-card neoclassical library.
    Hero: Stickman typing at desk, then sprinting full stride, then screeching halt at 0.028s!
    """
    W, H = canvas.W, canvas.H
    ground_y = 800
    sc = canvas.scale

    # 1. Full-Screen Twilight Sky & Road Horizon
    canvas.draw_card((0, 0, W, ground_y), radius=0, fill=(12, 16, 26), outline=None)
    # Asphalt Highway across full width
    canvas.draw_card((0, ground_y, W, 920), radius=0, fill=(24, 28, 38), outline=None)
    # Yellow dashed highway center line
    for seg in range(0, W, 120):
        canvas.draw_card((seg + 20, ground_y + 55, seg + 80, ground_y + 63), radius=3, fill=(255, 205, 70), outline=None)

    # 2. Left Stage: Cozy Study Room (x=0 to 480)
    canvas.draw_card((0, 160, 460, ground_y), radius=0, fill=(20, 24, 36), outline=(70, 220, 255, 60), width=1)
    canvas.draw_pill((30, 190), "YOUR STUDY ROOM", size=18, text_color=CYAN, bg_color=(28, 35, 52))

    # Wooden desk & warm glowing banker's lamp
    desk_top_y = ground_y - 120
    canvas.draw_card((50, desk_top_y, 420, ground_y), radius=8, fill=(45, 32, 24), outline=(85, 62, 45), width=2)
    # Blank paper on desk
    canvas.draw_card((90, desk_top_y - 10, 220, desk_top_y + 70), radius=4, fill=(245, 245, 250), outline=(180, 180, 190), width=1)
    canvas.draw_text((105, desk_top_y + 12), "Essay: \"The...\"", size=18, fill=(30, 35, 45))
    # Brass desk lamp casting a warm cone
    lamp_x, lamp_y = 350, desk_top_y - 80
    canvas.draw.polygon([
        canvas.to_canvas(lamp_x - 30, lamp_y + 25),
        canvas.to_canvas(lamp_x + 30, lamp_y + 25),
        canvas.to_canvas(lamp_x + 70, desk_top_y),
        canvas.to_canvas(lamp_x - 70, desk_top_y)
    ], fill=(255, 220, 120, 45))

    # 3. Right Stage: The Colossal 70-Billion Library (x=1440 to 1920)
    lib_x0 = 1440
    canvas.draw_card((lib_x0, 140, W, ground_y), radius=0, fill=(18, 16, 28), outline=(150, 110, 255, 90), width=1)
    canvas.draw_pill((lib_x0 + 35, 175), "THE 70-BILLION LIBRARY", size=18, text_color=PURPLE, bg_color=(32, 26, 50))
    # Towering Classical Pillars & Shelves
    for p in range(4):
        px = lib_x0 + 40 + p * 105
        canvas.draw_card((px, 230, px + 45, ground_y), radius=6, fill=(35, 30, 52), outline=(100, 80, 145), width=1)
        canvas.draw_text((px + 8, 250), "17B", size=14, fill=DIM)

    # 4. Center Highway: Distance Road Signs
    canvas.draw_card((700, ground_y - 140, 840, ground_y - 50), radius=8, fill=(28, 80, 45), outline=WHITE, width=2)
    canvas.draw_text((770, ground_y - 110), "MILE 5", size=22, fill=WHITE, anchor="mm")
    canvas.draw_card((1150, ground_y - 140, 1290, ground_y - 50), radius=8, fill=(28, 80, 45), outline=WHITE, width=2)
    canvas.draw_text((1220, ground_y - 110), "MILE 10", size=22, fill=WHITE, anchor="mm")

    # 5. Overhead Headline & Digital Stopwatch
    canvas.draw_pill((W // 2 - 220, 75), "THE 10-MILE LIBRARY SPRINT ANALOGY", size=20, text_color=WHITE, bg_color=(25, 32, 54), outline_color=CYAN)

    # 6. Hero Stickman Actor Staging
    if rel_t < 1.8:
        # At desk writing
        draw_life_stickman(canvas, x=260, y=ground_y, height=330, action="typing",
                           mouth_open=0.7 * abs(math.sin(rel_t * 12)), expr="thinking", frame_t=rel_t)
    elif rel_t < 3.2:
        # Sprinting full stride down the highway in sneakers with red sweatband!
        sprint_progress = (rel_t - 1.8) / 1.4
        sprint_x = lerp(450, 1100, sprint_progress)
        draw_life_stickman(canvas, x=sprint_x, y=ground_y, height=340, action="sprint",
                           mouth_open=0.9, expr="determined", hat="sweatband", held_item="baton", frame_t=rel_t)
        # Comic speed lines
        for l in range(4):
            sl_x = sprint_x - 70 - l * 25
            sl_y = ground_y - 100 - l * 30
            canvas.draw.line([canvas.to_canvas(sl_x, sl_y), canvas.to_canvas(sl_x + 40, sl_y)], fill=(255, 255, 255, 180), width=int(3 * sc))
    else:
        # Screeches to a dead halt in shock at 28ms!
        draw_life_stickman(canvas, x=1050, y=ground_y, height=340, action="screech",
                           mouth_open=0.9, expr="surprised", look=(0.0, -0.6), hat="sweatband", frame_t=rel_t)

    # 7. Giant Digital Milestone Card (Center Upper)
    timer_box = (520, 160, 1400, 310)
    target_ms = 28.40
    curr_ms = target_ms if rel_t >= 3.2 else (target_ms * (rel_t / 3.2) ** 2)
    canvas.draw_card(timer_box, radius=18, fill=(16, 22, 38), outline=GREEN if curr_ms >= target_ms else CYAN, width=2)
    canvas.draw_text((W // 2, 195), "HUMAN REALITY: 3 HOURS PER WORD  vs  AI REALITY:", size=18, fill=DIM, anchor="mm")
    canvas.draw_text((W // 2, 245), f"{curr_ms:05.2f} MILLISECONDS", size=48, fill=GREEN if curr_ms >= target_ms else YELLOW, anchor="mm")
    canvas.draw_text((W // 2, 285), "140 Trillion calculations executed before you blink.", size=16, fill=WHITE, anchor="mm")


# ==============================================================================
# SCENE 2: SLICING LANGUAGE INTO MATH (BAKERY KITCHEN & 3D MAP)
# ==============================================================================
def render_story_token_slice(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """
    Story: Slicing the Sentence into Puzzle Pieces & The 3D Treasure Map.
    Full-width warm rustic kitchen counter with Stickman Chef in tall white hat.
    Cleaver chops sentence bread into 5 puzzle chips with price-tag numbers.
    Sky & blue float into 3D constellation map!
    """
    W, H = canvas.W, canvas.H
    counter_y = 750
    sc = canvas.scale

    # 1. Warm Rustic Kitchen Wall & Counter
    canvas.draw_card((0, 0, W, counter_y), radius=0, fill=(18, 16, 26), outline=None)
    # Heavy Wooden Butcher Counter spanning full width
    canvas.draw_card((0, counter_y, W, 920), radius=0, fill=(52, 36, 26), outline=(95, 68, 48), width=3)
    # Counter wood planks
    for px in range(0, W, 240):
        canvas.draw.line([canvas.to_canvas(px, counter_y), canvas.to_canvas(px, 920)], fill=(38, 25, 18), width=int(2 * sc))

    # Top Header Banner
    canvas.draw_pill((W // 2 - 240, 75), "THE SECRET TRANSLATOR: TOKENIZATION", size=20, text_color=WHITE, bg_color=(25, 32, 54), outline_color=CYAN)

    # 2. Stickman Chef on Left Stage (x=340, y=counter_y)
    draw_life_stickman(
        canvas, x=340, y=counter_y, height=360,
        action="chef_chop" if rel_t < 1.6 else "idle",
        mouth_open=0.7 * abs(math.sin(rel_t * 12)),
        expr="happy", hat="chef", held_item="cleaver", frame_t=rel_t
    )

    # Dynamic Comic Action Chop Starburst
    if 0.8 <= rel_t <= 1.4:
        cb_x, cb_y = 540, counter_y - 40
        canvas.draw_text((cb_x, cb_y - 50), "* CHOP! *", size=36, fill=YELLOW, anchor="mm", stroke_width=2, stroke_fill=(30, 20, 10))

    # 3. Chopped 5 Sliced Puzzle Blocks on Cutting Board
    tokens = [("Why", 1245), ("is", 318), ("the", 262), ("sky", 7891), ("blue", 4123)]
    board_box = (540, counter_y - 120, 1840, counter_y + 40)
    canvas.draw_card(board_box, radius=16, fill=(35, 25, 18), outline=(130, 95, 65), width=2)
    canvas.draw_text((570, counter_y - 95), "WOODEN CUTTING BOARD: \"Why is the sky blue?\"", size=18, fill=YELLOW)

    chip_w, chip_h = 220, 100
    start_x = 570
    for i, (tok, tid) in enumerate(tokens):
        t_enter = max(0.0, rel_t - 0.4 - i * 0.15)
        p_sp = min(1.0, spring(t_enter * 1.8))
        bx = start_x + i * (chip_w + 24)
        by = counter_y - 65 + (1.0 - p_sp) * 45

        is_pair = tok in ["sky", "blue"] and rel_t > 2.2
        c_fill = (45, 30, 65) if is_pair else (22, 28, 46)
        c_bord = PURPLE if is_pair else CYAN

        # Puzzle Block with Tab
        canvas.draw_card((bx, by, bx + chip_w, by + chip_h), radius=12, fill=c_fill, outline=c_bord, width=2)
        canvas.draw_text((bx + chip_w // 2, by + 32), f"\"{tok}\"", size=28, fill=WHITE, anchor="mm")
        # Barcode Price Tag
        canvas.draw_pill((bx + 25, by + 60), f"Token #{tid}", size=15, text_color=CYAN, bg_color=(32, 42, 68))

    # 4. Upper Right Stage: The 4,096-Dimensional Semantic Constellation Map
    map_box = (540, 150, 1840, 480)
    canvas.draw_card(map_box, radius=18, fill=(12, 16, 28), outline=(70, 220, 255, 120), width=1)
    canvas.draw_pill((570, 175), "4,096-DIMENSIONAL SEMANTIC TREASURE MAP", size=18, text_color=CYAN, bg_color=(24, 32, 52))
    canvas.draw_text((570, 230), "AI cannot read letters. It converts each puzzle piece into a 4,096-number GPS location.", size=18, fill=WHITE)

    # Celestial Neighbor Orbit
    canvas.draw_card((570, 280, 1800, 430), radius=14, fill=(18, 24, 40), outline=PURPLE, width=2)
    canvas.draw_text((610, 320), "🌟 Vector Space Proximity: [ 'sky' ] <--------------------> [ 'blue' ]", size=24, fill=YELLOW)
    canvas.draw_pill((610, 365), "Cosine Distance: 0.942 -> Next-door neighbors in vector space!", size=18, text_color=GREEN, bg_color=(20, 45, 30))


# ==============================================================================
# SCENE 3: THE 1,000-ARM FORKLIFT (PARALLEL WAREHOUSE PREFILL)
# ==============================================================================
def render_story_forklift_prefill(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """
    Story: The 1,000-Worker Factory / Parallel Robotic Forklift.
    Full warehouse floor with overhead crane gantry.
    Left: Slow human reading 1 word with a magnifying glass.
    Right: Massive 16-arm hydraulic crane lifting all words simultaneously in 0.2ms!
    Stickman Operator pulls red industrial power lever.
    """
    W, H = canvas.W, canvas.H
    ground_y = 780
    sc = canvas.scale

    # 1. High-Tech Industrial Warehouse Interior
    canvas.draw_card((0, 0, W, ground_y), radius=0, fill=(14, 18, 28), outline=None)
    # Concrete floor with yellow/black hazard stripes
    canvas.draw_card((0, ground_y, W, 920), radius=0, fill=(30, 34, 44), outline=None)
    for hz in range(0, W, 80):
        canvas.draw.polygon([
            canvas.to_canvas(hz, ground_y),
            canvas.to_canvas(hz + 35, ground_y),
            canvas.to_canvas(hz + 65, 920),
            canvas.to_canvas(hz + 30, 920)
        ], fill=(245, 195, 50, 180))

    # Top Header
    canvas.draw_pill((W // 2 - 250, 75), "PARALLEL POWER: THE 1,000-ARM ROBOTIC FORKLIFT", size=20, text_color=GREEN, bg_color=(18, 42, 28), outline_color=GREEN)

    # 2. Left Stage: The Slow Human Reader (x=0 to 450)
    canvas.draw_card((30, 160, 420, ground_y - 20), radius=16, fill=(22, 18, 20), outline=(255, 70, 90, 80), width=1)
    canvas.draw_pill((55, 185), "THE HUMAN WAY: SERIAL", size=18, text_color=RED, bg_color=(45, 20, 24))
    draw_life_stickman(
        canvas, x=220, y=ground_y - 20, height=330, action="coffee_relax",
        mouth_open=0.2, expr="worried", frame_t=rel_t
    )
    canvas.draw_text((220, ground_y - 140), "1 Word at a time...\nTakes hours!", size=20, fill=RED, anchor="mm")

    # 3. Center & Right Stage: The 16-Arm Robotic Crane Gantry (x=460 to 1880)
    crane_box = (460, 160, 1880, ground_y - 20)
    canvas.draw_card(crane_box, radius=18, fill=(16, 22, 36), outline=GREEN, width=2)
    canvas.draw_pill((490, 185), "GPU TENSOR CORES: PARALLEL PREFILL", size=18, text_color=GREEN, bg_color=(20, 45, 30))

    # Stickman Crane Operator on Catwalk
    draw_life_stickman(
        canvas, x=580, y=ground_y - 20, height=340, action="pull_lever",
        mouth_open=0.7 * abs(math.sin(rel_t * 12)), expr="happy", hat="goggles", frame_t=rel_t
    )

    # 5 Robotic Claws lifting all prompt tokens in a single parallel sweep
    words = ["Why", "is", "the", "sky", "blue"]
    claw_start_x = 760
    for i, w in enumerate(words):
        wx = claw_start_x + i * 215
        arm_lift = int(math.sin(rel_t * 5.0) * 14)
        # Steel Gantry Piston
        canvas.draw_card((wx + 45, 250, wx + 75, 410 + arm_lift), radius=6, fill=(60, 75, 105), outline=WHITE, width=1)
        # Hydraulic Claw
        canvas.draw_card((wx, 410 + arm_lift, wx + 160, 485 + arm_lift), radius=10, fill=(22, 42, 68), outline=CYAN, width=2)
        canvas.draw_text((wx + 80, 448 + arm_lift), f"\"{w}\"", size=28, fill=WHITE, anchor="mm")

    # Blue laser parallel scanline across all words
    laser_y = 445 + int(math.sin(rel_t * 5.0) * 14)
    canvas.draw.line([canvas.to_canvas(claw_start_x - 30, laser_y), canvas.to_canvas(claw_start_x + 1050, laser_y)], fill=(70, 220, 255), width=int(3 * sc))

    # Bottom Telemetry Plaque
    canvas.draw_card((760, ground_y - 180, 1820, ground_y - 60), radius=12, fill=(20, 32, 48), outline=GREEN, width=2)
    canvas.draw_text((1290, ground_y - 135), "⚡ PROMPT DIGESTED IN 0.2 MILLISECONDS (500,000 WORDS/SEC)", size=24, fill=GREEN, anchor="mm")
    canvas.draw_text((1290, ground_y - 95), "All cores fire at the exact same fraction of a microsecond.", size=16, fill=DIM, anchor="mm")


# ==============================================================================
# SCENE 4: THE GOLDEN STICKY NOTE MIRACLE (DETECTIVE CORKBOARD KV CACHE)
# ==============================================================================
def render_story_sticky_cache(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """
    Story: The Golden Sticky Note Miracle.
    Left: The Amnesia Nightmare (flying papers, panic stickman pulling hair out).
    Right: The Detective Corkboard (warm room, golden pinned notes, stickman sipping coffee).
    """
    W, H = canvas.W, canvas.H
    ground_y = 800
    sc = canvas.scale

    # 1. Left Half: The Amnesia Nightmare (x=0 to 930)
    canvas.draw_card((0, 0, 930, 920), radius=0, fill=(25, 14, 16), outline=RED, width=2)
    canvas.draw_pill((30, 75), "THE AMNESIA NIGHTMARE: NO CACHE", size=20, text_color=RED, bg_color=(48, 16, 20), outline_color=RED)

    # Panic Stickman buried under flying paper blizzard
    draw_life_stickman(
        canvas, x=460, y=ground_y, height=360, action="panic_amnesia",
        mouth_open=0.9, expr="worried", frame_t=rel_t
    )
    canvas.draw_text((460, 230), "\"WAIT! WHAT WAS WORD #1?!\"", size=32, fill=RED, anchor="mm")
    canvas.draw_pill((180, 290), "Exponential Re-reading: Drops to 1.2 Words/sec", size=18, text_color=RED, bg_color=(55, 18, 22))

    # Flying crumpled paper blizzard
    rng = np.random.default_rng(42)
    for _ in range(14):
        px = rng.integers(80, 850)
        py = rng.integers(340, 750)
        rot = rng.integers(-40, 40)
        canvas.draw_card((px, py, px + 55, py + 40), radius=4, fill=(240, 240, 245), outline=(180, 180, 190), width=1)

    # 2. Right Half: The Detective Corkboard & KV Cache (x=950 to W)
    canvas.draw_card((950, 0, W, 920), radius=0, fill=(14, 22, 28), outline=CYAN, width=2)
    canvas.draw_pill((980, 75), "THE SAVIOR: THE DETECTIVE CORKBOARD (KV CACHE)", size=20, text_color=CYAN, bg_color=(20, 38, 52), outline_color=CYAN)

    # Framed Wooden Corkboard Wall
    cork_box = (980, 150, 1880, 560)
    canvas.draw_card(cork_box, radius=16, fill=(45, 34, 22), outline=(135, 98, 62), width=3)

    # 5 Golden Sticky Notes neatly pinned with red thumbtacks
    notes = [("Word 1", "Why"), ("Word 2", "is"), ("Word 3", "the"), ("Word 4", "sky"), ("Word 5", "blue")]
    for idx, (lbl, w) in enumerate(notes):
        sx = 1010 + idx * 170
        sy = 240 + (idx % 2) * 45
        locked = rel_t > (0.4 + idx * 0.3)
        c_fill = (255, 215, 80) if locked else (70, 65, 55)
        c_txt = (30, 25, 10) if locked else DIM

        # Golden Sticky Note
        canvas.draw_card((sx, sy, sx + 150, sy + 140), radius=6, fill=c_fill, outline=(180, 140, 40), width=1)
        # Red Thumbtack on top
        canvas.draw.ellipse([canvas.to_canvas(sx + 70, sy - 8), canvas.to_canvas(sx + 80, sy + 4)], fill=RED, outline=torso_color if 'torso_color' in locals() else (20, 20, 20))
        canvas.draw_text((sx + 75, sy + 40), lbl, size=16, fill=c_txt, anchor="mm")
        canvas.draw_text((sx + 75, sy + 80), f"\"{w}\"", size=24, fill=c_txt, anchor="mm")
        canvas.draw_text((sx + 75, sy + 115), "📌 PINNED", size=14, fill=(140, 90, 20) if locked else DIM, anchor="mm")

    # Relaxed Stickman Sipping Coffee on Right
    draw_life_stickman(
        canvas, x=1420, y=ground_y + 20, height=350, action="coffee_relax",
        mouth_open=0.7 * abs(math.sin(rel_t * 12)), expr="happy", held_item="coffee_mug", frame_t=rel_t
    )
    canvas.draw_pill((1020, ground_y - 140), "Result: 85+ Tokens/sec (Never Re-read past thoughts!)", size=22, text_color=GREEN, bg_color=(18, 45, 30))


# ==============================================================================
# SCENE 5: PUSHING THE 140 GB MOUNTAIN (NARROW CANYON BRIDGE TRAFFIC JAM)
# ==============================================================================
def render_story_memory_mountain(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """
    Story: The One-Lane Bridge & Delivery Truck (Memory Bandwidth Bottleneck).
    Dramatic canyon spanning the entire 1920 width!
    Left cliff: The 140 GB VRAM Vault.
    Right cliff: The Supercompute Factory.
    Center: Narrow suspension bridge with heavy delivery truck crawling with 140 tons of cards!
    Chef tapping foot waiting for ingredients.
    """
    W, H = canvas.W, canvas.H
    bridge_y = 660
    ground_y = 780
    sc = canvas.scale

    # 1. Full-Screen Canyon Landscape
    canvas.draw_card((0, 0, W, 920), radius=0, fill=(12, 14, 22), outline=None)

    # Left Mountain Cliff (x=0 to 460)
    canvas.draw.polygon([
        canvas.to_canvas(0, 300), canvas.to_canvas(460, 300),
        canvas.to_canvas(420, 920), canvas.to_canvas(0, 920)
    ], fill=(24, 28, 42))
    canvas.draw_card((30, 200, 430, 380), radius=12, fill=(18, 22, 34), outline=CYAN, width=2)
    canvas.draw_text((230, 250), "VRAM STORAGE VAULT", size=20, fill=CYAN, anchor="mm")
    canvas.draw_text((230, 300), "140 GB MODEL WEIGHTS", size=24, fill=WHITE, anchor="mm")

    # Right Mountain Cliff (x=1460 to W)
    canvas.draw.polygon([
        canvas.to_canvas(1460, 300), canvas.to_canvas(W, 300),
        canvas.to_canvas(W, 920), canvas.to_canvas(1500, 920)
    ], fill=(24, 28, 42))
    canvas.draw_card((1490, 200, 1890, 380), radius=12, fill=(28, 20, 38), outline=PURPLE, width=2)
    canvas.draw_text((1690, 250), "GPU COMPUTE ENGINES", size=20, fill=PURPLE, anchor="mm")
    canvas.draw_text((1690, 300), "10,000 TENSOR CORES", size=24, fill=WHITE, anchor="mm")

    # 2. Narrow Suspension Bridge across Canyon (x=420 to 1500)
    canvas.draw_card((420, bridge_y - 10, 1500, bridge_y + 30), radius=4, fill=(45, 52, 70), outline=(70, 220, 255, 120), width=2)
    # Suspension Cables & Suspenders
    canvas.draw.arc([canvas.to_canvas(420, 280), canvas.to_canvas(1500, bridge_y + 100)], start=0, end=180, fill=(70, 220, 255), width=max(2, int(2.5 * sc)))
    for susp in range(480, 1450, 80):
        canvas.draw.line([canvas.to_canvas(susp, 460), canvas.to_canvas(susp, bridge_y - 10)], fill=(70, 220, 255, 140), width=max(1, int(1.5 * sc)))

    # Overhead Banner
    canvas.draw_pill((W // 2 - 250, 75), "THE PHYSICAL LIMIT: MEMORY BANDWIDTH TRAFFIC JAM", size=20, text_color=RED, bg_color=(45, 18, 22), outline_color=RED)

    # 3. Overloaded Red Delivery Cargo Truck on the Bridge
    truck_progress = (rel_t * 0.12) % 1.0
    truck_x = lerp(460, 1100, truck_progress)
    truck_w, truck_h = 320, 140
    truck_top = bridge_y - truck_h - 10

    # Red Truck Body & Cab
    canvas.draw_card((truck_x, truck_top + 40, truck_x + truck_w, bridge_y - 10), radius=12, fill=(215, 45, 55), outline=WHITE, width=2)
    # Wheels
    canvas.draw.ellipse([canvas.to_canvas(truck_x + 50, bridge_y - 25), canvas.to_canvas(truck_x + 95, bridge_y + 15)], fill=(20, 20, 20), outline=WHITE, width=2)
    canvas.draw.ellipse([canvas.to_canvas(truck_x + 230, bridge_y - 25), canvas.to_canvas(truck_x + 275, bridge_y + 15)], fill=(20, 20, 20), outline=WHITE, width=2)

    # Giant 140-Ton Steel Safe Block on the truck bed
    canvas.draw_card((truck_x + 20, truck_top - 50, truck_x + 210, truck_top + 50), radius=10, fill=(35, 40, 55), outline=YELLOW, width=2)
    canvas.draw_text((truck_x + 115, truck_top - 15), "140 GB", size=32, fill=WHITE, anchor="mm")
    canvas.draw_text((truck_x + 115, truck_top + 20), "FLASHCARDS", size=18, fill=YELLOW, anchor="mm")

    # Flashing Traffic Light on Bridge
    canvas.draw_card((W // 2 - 160, bridge_y - 210, W // 2 + 160, bridge_y - 120), radius=10, fill=(28, 16, 20), outline=RED, width=2)
    canvas.draw_text((W // 2, bridge_y - 175), "🚨 SILICON TRAFFIC JAM!", size=20, fill=RED, anchor="mm")
    canvas.draw_text((W // 2, bridge_y - 145), "Max Bridge Speed: 3.35 TB/s", size=15, fill=WHITE, anchor="mm")

    # 4. Right Cliff: Master Chef Stickman Tapping Foot Impatiently
    draw_life_stickman(
        canvas, x=1660, y=ground_y + 40, height=360, action="idle",
        mouth_open=0.7 * abs(math.sin(rel_t * 12)), expr="worried", hat="chef", frame_t=rel_t
    )
    canvas.draw_text((1660, ground_y - 100), "\"I CAN COOK IN 1 MICROSECOND!\nWHERE ARE MY INGREDIENTS?!\"", size=20, fill=YELLOW, anchor="mm")

    # 5. Bottom Telemetry Cards
    canvas.draw_pill((320, 800), "Compute Cores: 22% (STARVING / IDLE)", size=19, text_color=DIM, bg_color=(25, 30, 45))
    canvas.draw_pill((1150, 800), "Memory Bus: 100% MAXIMUM SATURATION", size=19, text_color=WHITE, bg_color=(235, 30, 50))


# ==============================================================================
# SCENE 6: THE PROFESSOR & THE HYPERACTIVE INTERN (SPECULATIVE DECODING)
# ==============================================================================
def render_story_intern_draft(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """
    Story: The Wise Professor & The Hyperactive Intern (Speculative Decoding).
    Full academic research lecture hall spanning 1920x1080.
    Left: Small, fast intern stickman in backwards cap throwing 4 drafted words in 3ms.
    Right: Wise professor stickman at grand mahogany desk with round glasses and bowtie
           slamming giant red rubber stamp: APPROVED ALL 4 AT ONCE!
    """
    W, H = canvas.W, canvas.H
    ground_y = 780
    sc = canvas.scale

    # 1. Grand University Study Room & Bookshelves
    canvas.draw_card((0, 0, W, ground_y), radius=0, fill=(18, 16, 26), outline=None)
    # Polished Parquet Hardwood Floor
    canvas.draw_card((0, ground_y, W, 920), radius=0, fill=(45, 30, 20), outline=(85, 60, 40), width=2)
    # Background Wood Bookshelves
    for bs in range(0, W, 320):
        canvas.draw_card((bs + 20, 140, bs + 300, ground_y - 40), radius=8, fill=(28, 22, 36), outline=(65, 50, 80), width=1)
        canvas.draw_text((bs + 160, 180), "RESEARCH ARCHIVE", size=16, fill=DIM, anchor="mm")

    # Top Header Banner
    canvas.draw_pill((W // 2 - 250, 75), "THE ULTIMATE HACK: SPECULATIVE DECODING", size=20, text_color=CYAN, bg_color=(20, 35, 55), outline_color=CYAN)

    # 2. Left Stage: The Hyperactive Intern (1B Draft Model)
    canvas.draw_pill((180, 230), "THE HYPERACTIVE INTERN (1B DRAFT MODEL)", size=18, text_color=CYAN, bg_color=(24, 38, 60))
    # Tiny fast intern dashing across the room
    intern_progress = (rel_t * 0.3) % 1.0
    intern_x = lerp(160, 780, intern_progress)
    draw_life_stickman(
        canvas, x=intern_x, y=ground_y, height=270, action="intern_dash",
        mouth_open=0.9, expr="happy", hat="intern_cap", frame_t=rel_t
    )
    canvas.draw_text((intern_x, ground_y - 120), "\"Here's 4 words!\"", size=18, fill=CYAN, anchor="mm")

    # 3. 4 Drafted Flying Word Cards
    words = ["the", "atmosphere", "scatters", "light"]
    for i, w in enumerate(words):
        bx = 820 + i * 220
        by = 280 + int(math.sin(rel_t * 4.0 + i) * 15)
        is_stamped = rel_t > (1.8 + i * 0.35)
        c_fill = (22, 45, 32) if is_stamped else (36, 26, 48)
        c_bord = GREEN if is_stamped else PURPLE

        canvas.draw_card((bx, by, bx + 195, by + 105), radius=12, fill=c_fill, outline=c_bord, width=2)
        canvas.draw_text((bx + 97, by + 35), f"\"{w}\"", size=24, fill=WHITE, anchor="mm")
        st_text = "✓ APPROVED!" if is_stamped else "DRAFTING..."
        canvas.draw_text((bx + 97, by + 75), st_text, size=18, fill=GREEN if is_stamped else YELLOW, anchor="mm")

    # 4. Right Stage: The Wise Professor (70B Giant Model)
    prof_x = 1720
    # Grand Mahogany Desk
    canvas.draw_card((prof_x - 180, ground_y - 140, prof_x + 180, ground_y), radius=10, fill=(55, 36, 24), outline=(100, 70, 45), width=2)
    draw_life_stickman(
        canvas, x=prof_x, y=ground_y, height=360, action="professor_stamp",
        mouth_open=0.7 * abs(math.sin(rel_t * 12)), expr="happy", hat="professor_glasses", held_item="rubber_stamp", frame_t=rel_t
    )
    canvas.draw_pill((prof_x - 160, 230), "THE WISE PROFESSOR (70B MODEL)", size=18, text_color=PURPLE, bg_color=(36, 26, 52))
    canvas.draw_text((prof_x, ground_y - 180), "\"Looks good to me.\n*STAMP!*\"", size=20, fill=WHITE, anchor="mm")

    # 5. Speedup Rocket Multiplier
    if rel_t > 2.8:
        canvas.draw_pill((W // 2 - 180, ground_y - 120), "🚀 3.0X INFERENCE ACCELERATION!", size=28, text_color=YELLOW, bg_color=(42, 34, 18), outline_color=YELLOW)


# ==============================================================================
# SCENE 7: THE OLYMPIC RELAY & VICTORY DROPKICK OUTRO
# ==============================================================================
def render_story_relay_outro(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any], logo_img: Optional[Image.Image] = None):
    """
    Story Outro:
    Olympic stadium under floodlights!
    First 2.5s: Stickman sprints forward with glowing golden relay baton.
    At 2.5s+: Winner's podium appears with red SUBSCRIBE button.
             Stickman leaps in a flying martial-arts dropkick, stomps button,
             confetti explodes, and stickman celebrates with hands raised!
    """
    W, H = canvas.W, canvas.H
    track_y = 750
    cx = W // 2
    cy = H // 2 - 20
    sc = canvas.scale

    # 1. Full-Screen Olympic Stadium at Night
    canvas.draw_card((0, 0, W, track_y), radius=0, fill=(12, 14, 24), outline=None)
    # Red Rubber Olympic Running Track spanning full width
    canvas.draw_card((0, track_y, W, 920), radius=0, fill=(185, 45, 55), outline=None)
    # White Lane Lines
    for ln in range(track_y + 35, 920, 50):
        canvas.draw.line([canvas.to_canvas(0, ln), canvas.to_canvas(W, ln)], fill=(255, 255, 255, 200), width=int(3 * sc))

    # Stadium Floodlights overhead
    for fl in [200, W - 200]:
        canvas.draw.line([canvas.to_canvas(fl, 80), canvas.to_canvas(fl - 150, track_y)], fill=(255, 255, 255, 25), width=int(120 * sc))
        canvas.draw.line([canvas.to_canvas(fl, 80), canvas.to_canvas(fl + 150, track_y)], fill=(255, 255, 255, 25), width=int(120 * sc))

    if rel_t < 2.5:
        # Part 1: The Coordinated Computer Relay Race
        canvas.draw_pill((cx - 240, 85), "THE ULTIMATE COMPUTER RELAY RACE", size=20, text_color=CYAN, bg_color=(18, 28, 48), outline_color=CYAN)
        canvas.draw_text((cx, 260), "AI speed isn't magic.\nIt's the most coordinated relay race ever engineered.", size=36, fill=WHITE, anchor="mm")

        # Stickman Hero Sprinting with Golden Baton
        relay_x = cx - 200 + int(rel_t * 160)
        draw_life_stickman(
            canvas, x=relay_x, y=track_y + 40, height=360, action="sprint",
            mouth_open=0.8, expr="happy", hat="sweatband", held_item="baton", frame_t=rel_t
        )

    else:
        # Part 2: Winner's Podium & Flying Dropkick Stomp Sequence
        rel_outro = rel_t - 2.5
        podium_box = (cx - 500, cy - 250, cx + 500, cy + 240)
        canvas.draw_card(podium_box, radius=24, fill=(16, 22, 38), outline=(255, 70, 90, 140), width=2)

        if logo_img:
            logo_sz = int(140 * sc)
            resized_logo = logo_img.resize((logo_sz, logo_sz), Image.Resampling.LANCZOS)
            lx, ly = canvas.to_canvas(cx - 70, cy - 210)
            canvas.frame.paste(resized_logo, (int(lx), int(ly)), resized_logo)

        canvas.draw_text((cx, cy - 45), "TECHXKENIL", size=44, fill=WHITE, anchor="mm")
        canvas.draw_text((cx, cy + 10), "AI • TECH • CODE", size=22, fill=(160, 180, 230), anchor="mm")

        btn_w, btn_h = 320, 75
        bx0, by0 = cx - btn_w // 2, cy + 85
        is_stomped = rel_outro >= 1.6

        if not is_stomped:
            # Red Subscribe Button before dropkick
            canvas.draw_card((bx0, by0, bx0 + btn_w, by0 + btn_h), radius=btn_h // 2, fill=(255, 30, 50), outline=None)
            canvas.draw_text((cx, by0 + btn_h // 2), "SUBSCRIBE", size=26, fill=WHITE, anchor="mm")

            # Stickman flying dropkick through the air!
            kick_progress = min(1.0, rel_outro / 1.6)
            kick_x = lerp(cx + 420, cx + 80, kick_progress)
            kick_y = lerp(cy - 80, by0 + 20, kick_progress)
            draw_life_stickman(
                canvas, x=kick_x, y=kick_y, height=340, action="dropkick",
                mouth_open=0.9, expr="determined", hat="sweatband", facing_right=False, frame_t=rel_t
            )
        else:
            # Emerald Green Button after stomp!
            canvas.draw_card((bx0, by0, bx0 + btn_w, by0 + btn_h), radius=btn_h // 2, fill=(35, 195, 110), outline=None)
            canvas.draw_text((cx, by0 + btn_h // 2), "✓ SUBSCRIBED!", size=26, fill=WHITE, anchor="mm")

            # Stickman Victorious Celebration on Podium!
            draw_life_stickman(
                canvas, x=cx + 300, y=cy + 160, height=350, action="celebrate",
                mouth_open=0.8, expr="happy", hat="sweatband", frame_t=rel_t
            )

            # Massive Gold & Emerald Confetti Explosion!
            rng = np.random.default_rng(77)
            for _ in range(80):
                px = rng.integers(100, W - 100)
                py = rng.integers(100, H - 120)
                col = [(255, 205, 70), (70, 220, 255), (90, 235, 150), (255, 110, 180)][rng.integers(0, 4)]
                sz = rng.integers(5, 11) * sc
                p_c = canvas.to_canvas(px, py)
                canvas.draw.ellipse([p_c[0] - sz, p_c[1] - sz, p_c[0] + sz, p_c[1] + sz], fill=col)
