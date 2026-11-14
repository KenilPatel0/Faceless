#!/usr/bin/env python3
"""
storytelling_scenes.py — Master Storytelling Visual Scenes for 'How AI Answers in Milliseconds'
Features the Professor & Intern analogy, the 10-Mile Library Sprint, the 1,000-Arm Forklift,
and the Golden Sticky Note Pegboard.
"""

import math
from typing import Dict, Any, Optional, Tuple, List
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from tools.render_core import (
    OverscanCanvas, get_font, spring,
    WHITE, DIM, CYAN, PURPLE, YELLOW, GREEN, RED, DARK_CARD, CARD_BORDER
)
from tools.stickman_director_scenes import draw_director_actor

def clamp(v: float, mn: float = 0.0, mx: float = 1.0) -> float:
    return max(mn, min(mx, v))

def lerp(a: float, b: float, p: float) -> float:
    return a + (b - a) * p


# ==============================================================================
# SCENE 1: THE 10-MILE LIBRARY SPRINT (HOOK)
# ==============================================================================
def render_story_library_sprint(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """
    Hook Story:
    Left: Stickman author at writing desk.
    Center: Towering library aisles stretching to infinity (70 Billion Cards).
    Right: Running track with Stickman sprinting with a baton, then screeching to a halt at 28.40ms!
    """
    cx = canvas.W // 2
    sc = canvas.scale

    canvas.draw_pill((cx - 160, 85), "THE IMPOSSIBLE ANALOGY", size=18, text_color=CYAN,
                     bg_color=(18, 24, 42), outline_color=(70, 220, 255, 120))

    # Writing Desk on Left
    desk_box = (cx - 520, 150, cx - 180, 480)
    canvas.draw_card(desk_box, radius=16, fill=(16, 20, 32), outline=(70, 220, 255, 100), width=1)
    canvas.draw_text((desk_box[0] + 30, desk_box[1] + 25), "YOUR WRITING DESK", size=18, fill=CYAN)
    
    # Wooden desk table
    canvas.draw_card((desk_box[0] + 30, 330, desk_box[2] - 30, 430), radius=8, fill=(35, 26, 20), outline=(80, 60, 45), width=2)
    canvas.draw_text((desk_box[0] + 60, 355), "Essay: \"The...\"", size=22, fill=WHITE)

    # Towering Library Shelves (Center)
    lib_box = (cx - 150, 150, cx + 180, 480)
    canvas.draw_card(lib_box, radius=16, fill=(14, 16, 26), outline=(150, 110, 255, 100), width=1)
    canvas.draw_text((lib_box[0] + 25, lib_box[1] + 25), "70-BILLION-CARD LIBRARY", size=18, fill=PURPLE)
    
    # Infinite bookshelf rows
    for r in range(5):
        sy = 210 + r * 50
        canvas.draw_card((lib_box[0] + 20, sy, lib_box[2] - 20, sy + 38), radius=4, fill=(24, 28, 44), outline=(75, 55, 110), width=1)
        canvas.draw_text((lib_box[0] + 35, sy + 10), f"Aisle {r+1}: 14 Billion Flashcards", size=14, fill=DIM)

    # Running Track on Right (Sprint to Library)
    track_box = (cx + 210, 150, cx + 520, 480)
    canvas.draw_card(track_box, radius=16, fill=(20, 16, 18), outline=(255, 70, 90, 100), width=1)
    canvas.draw_text((track_box[0] + 25, track_box[1] + 25), "THE 10-MILE SPRINT", size=18, fill=RED)
    canvas.draw_text((track_box[0] + 25, 230), "Human Reality:\n3 Hours per word!", size=22, fill=RED)

    # STICKMAN ACTOR
    if rel_t < 1.8:
        # At desk writing
        draw_director_actor(canvas, desk_box[0] + 160, 310, scale=0.75, action="typing",
                            mouth_open=0.7 * abs(math.sin(rel_t * 12)), expr="happy", frame_t=rel_t)
    elif rel_t < 3.0:
        # Sprinting down the track in sneakers
        sprint_x = track_box[0] + int((rel_t - 1.8) * 140)
        draw_director_actor(canvas, sprint_x, 370, scale=0.7, action="slam_enter",
                            mouth_open=0.9, expr="surprised", frame_t=rel_t)
    else:
        # Screeching to a halt in shock at 28ms!
        draw_director_actor(canvas, cx, 580, scale=0.8, action="idle",
                            mouth_open=0.8, expr="surprised", look=(0.0, -0.6), frame_t=rel_t)

    # Bottom Millisecond Miracle Stopwatch
    sw_box = (cx - 420, 520, cx + 420, 680)
    canvas.draw_card(sw_box, radius=18, fill=(16, 22, 38), outline=GREEN, width=2)
    target_ms = 28.40
    curr_ms = target_ms if rel_t >= 3.0 else (target_ms * (rel_t / 3.0) ** 2)
    canvas.draw_text((cx, 555), "AI REALITY: TIME-TO-FIRST-TOKEN", size=18, fill=CYAN, anchor="mm")
    canvas.draw_text((cx, 615), f"{curr_ms:05.2f} MILLISECONDS", size=48, fill=GREEN if curr_ms >= target_ms else YELLOW, anchor="mm")
    canvas.draw_text((cx, 660), "140 Trillion Math Calculations executed before you blink.", size=16, fill=DIM, anchor="mm")


# ==============================================================================
# SCENE 2: SLICING LANGUAGE INTO MATH (TOKENIZATION)
# ==============================================================================
def render_story_token_slice(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """
    Story: Slicing the Sentence into Puzzle Pieces & The 3D Treasure Map.
    Stickman as chef/navigator chopping sentence into 5 numbered puzzle blocks.
    """
    cx = canvas.W // 2
    sc = canvas.scale

    canvas.draw_pill((cx - 160, 85), "THE SECRET CODE: TOKENIZATION", size=18, text_color=CYAN,
                     bg_color=(18, 24, 42), outline_color=(70, 220, 255, 120))

    canvas.draw_text((cx + 60, 140), "\"Why is the sky blue?\"", size=32, fill=WHITE, anchor="mm")
    canvas.draw_text((cx + 60, 180), "English cannot enter the GPU. It must be sliced into puzzle pieces.", size=18, fill=DIM, anchor="mm")

    # STICKMAN CHEF CHOPPING ON LEFT
    if rel_t < 1.4:
        draw_director_actor(canvas, cx - 380, 200, scale=0.75, action="karate_chop",
                            mouth_open=0.5, expr="happy", frame_t=rel_t)
    else:
        draw_director_actor(canvas, cx - 400, 210, scale=0.75, action="idle",
                            mouth_open=0.7 * abs(math.sin(rel_t * 14)), expr="happy", look=(0.6, 0.0), frame_t=rel_t)

    # 5 Sliced Token Blocks
    tokens = [("Why", 1245), ("is", 318), ("the", 262), ("sky", 7891), ("blue", 4123)]
    chip_w, chip_h = 160, 95
    start_x = cx - 240
    for i, (tok, tid) in enumerate(tokens):
        t_enter = max(0.0, rel_t - 0.5 - i * 0.12)
        p_sp = min(1.0, spring(t_enter * 1.8))
        bx = start_x + i * (chip_w + 16)
        by = 230 + (1.0 - p_sp) * 40
        
        is_pair = tok in ["sky", "blue"] and rel_t > 2.5
        c_fill = (28, 20, 44) if is_pair else (16, 22, 38)
        c_bord = PURPLE if is_pair else CYAN

        canvas.draw_card((bx, by, bx + chip_w, by + chip_h), radius=12, fill=c_fill, outline=c_bord, width=2)
        canvas.draw_text((bx + chip_w // 2, by + 30), f"\"{tok}\"", size=24, fill=WHITE, anchor="mm")
        canvas.draw_pill((bx + 15, by + 55), f"Token #{tid}", size=14, text_color=CYAN, bg_color=(25, 34, 58))

    # The 3D Mathematical Treasure Map (Bottom)
    map_box = (cx - 460, 380, cx + 460, 680)
    canvas.draw_card(map_box, radius=18, fill=(12, 16, 28), outline=(70, 220, 255, 120), width=1)
    canvas.draw_text((map_box[0] + 35, map_box[1] + 30), "4,096-DIMENSIONAL SEMANTIC TREASURE MAP", size=20, fill=CYAN)

    canvas.draw_pill((cx, 490), "Every word is a GPS coordinate with 4,096 numbers.", size=19, text_color=WHITE, bg_color=(24, 32, 52))
    
    # Glowing semantic chord connecting sky and blue
    canvas.draw_pill((cx, 560), "Semantic Proximity ('sky' <-> 'blue'): 0.942 Cosine Distance", size=20,
                     text_color=YELLOW, bg_color=(36, 30, 20), outline_color=YELLOW)
    canvas.draw_text((cx, 640), "Words with related meanings land right next to each other in vector space.", size=17, fill=DIM, anchor="mm")


# ==============================================================================
# SCENE 3: THE THOUSAND-ARM FORKLIFT (PREFILL)
# ==============================================================================
def render_story_forklift_prefill(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """
    Story: The Thousand-Arm Forklift.
    Humans read 1 word at a time. The GPU deploys 1,000 math arms simultaneously,
    lifting the entire prompt in 0.2ms!
    """
    cx = canvas.W // 2
    sc = canvas.scale

    canvas.draw_pill((cx - 160, 85), "THE 1,000-ARM FORKLIFT: PREFILL PHASE", size=18, text_color=GREEN,
                     bg_color=(18, 38, 28), outline_color=GREEN)

    # Stickman Crane Operator on Left
    draw_director_actor(canvas, cx - 440, 240, scale=0.75, action="pull_lever",
                        mouth_open=0.7 * abs(math.sin(rel_t * 14)), expr="happy", frame_t=rel_t)

    # Giant 16-Arm Robotic Forklift Assembly
    fork_box = (cx - 360, 150, cx + 520, 480)
    canvas.draw_card(fork_box, radius=18, fill=(14, 20, 32), outline=GREEN, width=2)
    canvas.draw_text((fork_box[0] + 30, fork_box[1] + 25), "PARALLEL GPU FORKLIFT (TENSOR CORES)", size=20, fill=GREEN)

    # 16 Robotic Claw Arms lifting all tokens simultaneously
    words = ["Why", "is", "the", "sky", "blue"]
    for i, w in enumerate(words):
        wx = fork_box[0] + 80 + i * 145
        arm_lift = int(math.sin(rel_t * 4.0) * 12)
        # Hydraulic piston
        canvas.draw_card((wx + 30, 210, wx + 50, 310 + arm_lift), radius=4, fill=(40, 50, 75), outline=WHITE, width=1)
        # Claw gripping word block
        canvas.draw_card((wx, 310 + arm_lift, wx + 110, 370 + arm_lift), radius=8, fill=(20, 35, 55), outline=CYAN, width=2)
        canvas.draw_text((wx + 55, 340 + arm_lift), w, size=22, fill=WHITE, anchor="mm")

    canvas.draw_pill((cx + 80, 425), "16 Cuda Blocks lift all words in ONE parallel sweep!", size=17, text_color=GREEN, bg_color=(18, 42, 30))

    # Speed Telemetry (Bottom)
    t_box = (cx - 460, 510, cx + 460, 680)
    canvas.draw_card(t_box, radius=16, fill=(16, 22, 38), outline=GREEN, width=2)
    canvas.draw_text((cx, 550), "TIME ELAPSED: 0.2 MILLISECONDS", size=26, fill=GREEN, anchor="mm")
    canvas.draw_text((cx, 600), "Human Reading Speed: 250 words/min | GPU Prefill: 500,000 words/second", size=18, fill=WHITE, anchor="mm")
    canvas.draw_pill((cx, 645), "Status: 100% Core Saturation (Compute-Bound)", size=16, text_color=CYAN, bg_color=(25, 45, 75))


# ==============================================================================
# SCENE 4: THE GOLDEN STICKY NOTE MIRACLE (KV CACHE)
# ==============================================================================
def render_story_sticky_cache(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """
    Story: The Golden Sticky Note Miracle.
    Left: The Nightmare — Stickman buried in flying sticky notes frantically re-reading word 1.
    Right: The Golden Pegboard — Stickman sipping coffee, golden sticky notes locked in memory.
    """
    cx = canvas.W // 2
    sc = canvas.scale

    canvas.draw_pill((cx - 160, 85), "THE GOLDEN STICKY NOTE MIRACLE: KV CACHE", size=18, text_color=YELLOW,
                     bg_color=(38, 30, 18), outline_color=YELLOW)

    # 1. Left Side: The Nightmare (Re-reading past words)
    left_box = (cx - 520, 140, cx - 20, 680)
    canvas.draw_card(left_box, radius=18, fill=(24, 14, 16), outline=RED, width=2)
    canvas.draw_text((left_box[0] + 30, left_box[1] + 30), "THE NIGHTMARE: NO CACHE", size=20, fill=RED)

    # Buried panic stickman
    draw_director_actor(canvas, left_box[0] + 240, 390, scale=0.75, action="idle",
                        mouth_open=0.8, expr="worried", frame_t=rel_t)
    canvas.draw_text((left_box[0] + 240, 440), "\"WAIT! WHAT WAS WORD 1?!\"", size=18, fill=RED, anchor="mm")
    canvas.draw_pill((left_box[0] + 30, 545), "Exponential Slowdown: 1.2 Tokens/sec", size=17, text_color=RED, bg_color=(45, 15, 20))

    # 2. Right Side: The Golden Pegboard (KV Cache)
    right_box = (cx + 20, 140, cx + 520, 680)
    canvas.draw_card(right_box, radius=18, fill=(12, 22, 28), outline=CYAN, width=2)
    canvas.draw_text((right_box[0] + 30, right_box[1] + 30), "THE SAVIOR: THE KV CACHE", size=20, fill=CYAN)

    # Relaxed stickman on right
    draw_director_actor(canvas, right_box[0] + 380, 330, scale=0.75, action="idle",
                        mouth_open=0.7 * abs(math.sin(rel_t * 14)), expr="happy", look=(-0.6, 0.0), frame_t=rel_t)

    # Golden sticky notes neatly pegged on wall
    notes = [("Word 1", "Why"), ("Word 2", "is"), ("Word 3", "the"), ("Word 4", "sky"), ("Word 5", "blue")]
    for idx, (lbl, w) in enumerate(notes):
        sy = right_box[1] + 75 + idx * 56
        locked = rel_t > (0.6 + idx * 0.4)
        c_fill = (38, 30, 18) if locked else (24, 28, 36)
        c_stat = YELLOW if locked else DIM
        txt = "📌 SAVED TO VRAM" if locked else "PROCESSING..."
        canvas.draw_card((right_box[0] + 30, sy, right_box[0] + 290, sy + 46), radius=8, fill=c_fill, outline=c_stat, width=1)
        canvas.draw_text((right_box[0] + 45, sy + 13), f"{lbl}: \"{w}\"", size=16, fill=WHITE)
        canvas.draw_text((right_box[0] + 175, sy + 13), txt, size=14, fill=c_stat)

    canvas.draw_pill((right_box[0] + 30, 545), "Result: 85+ Tokens/sec (Never Re-read!)", size=17, text_color=GREEN, bg_color=(18, 42, 30))


# ==============================================================================
# SCENE 5: PUSHING THE 140 GB MOUNTAIN (MEMORY BANDWIDTH)
# ==============================================================================
def render_story_memory_mountain(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """
    Story: Pushing the 140 GB Mountain.
    For every single new word, all 140 GB of model weights must be moved from VRAM.
    Stickman pushing giant boulder across the silicon bridge.
    """
    cx = canvas.W // 2
    sc = canvas.scale

    canvas.draw_pill((cx - 160, 85), "THE PHYSICAL LIMIT: MEMORY BANDWIDTH", size=18, text_color=RED,
                     bg_color=(38, 18, 22), outline_color=RED)

    # H100 Silicon Interposer Highway
    chip_box = (cx - 520, 140, cx + 520, 480)
    canvas.draw_card(chip_box, radius=18, fill=(13, 17, 28), outline=CYAN, width=2)
    canvas.draw_text((chip_box[0] + 30, chip_box[1] + 25), "THE SILICON HIGHWAY: 140 GB PER TOKEN", size=20, fill=CYAN)

    bridge_y = 330
    canvas.draw_card((cx - 240, bridge_y - 20, cx + 240, bridge_y + 40), radius=8, fill=(28, 36, 56), outline=(70, 220, 255, 120), width=1)
    canvas.draw_text((cx, bridge_y + 10), "Ultra-Fast HBM3 Memory Bus (3.35 Terabytes/sec)", size=16, fill=CYAN, anchor="mm")

    # STICKMAN PUSHING 140 GB BOULDER
    push_x = cx - 120 + int(math.sin(rel_t * 2.0) * 15)
    draw_director_actor(canvas, push_x, bridge_y - 20, scale=0.7, action="pushing_heavy",
                        mouth_open=0.7 * abs(math.sin(rel_t * 14)), expr="worried", frame_t=rel_t)

    # Giant 140 GB Mountain Boulder
    boulder_x = push_x + 55
    canvas.draw_card((boulder_x, bridge_y - 105, boulder_x + 130, bridge_y + 15), radius=12, fill=(45, 20, 30), outline=(255, 70, 90), width=2)
    canvas.draw_text((boulder_x + 65, bridge_y - 65), "140 GB", size=26, fill=WHITE, anchor="mm")
    canvas.draw_text((boulder_x + 65, bridge_y - 30), "FLASHCARDS", size=16, fill=YELLOW, anchor="mm")

    # Telemetry Traffic Jam (Bottom)
    g_box = (cx - 520, 510, cx + 520, 680)
    canvas.draw_card(g_box, radius=16, fill=(16, 20, 32), outline=(255, 70, 90, 100), width=1)
    canvas.draw_text((cx, g_box[1] + 40), "The math cores are starving for data. The bottleneck is the speed of light in silicon wires.", size=18, fill=WHITE, anchor="mm")
    canvas.draw_pill((cx - 180, g_box[1] + 85), "Math Cores: 22% (IDLING)", size=18, text_color=DIM, bg_color=(24, 30, 48))
    canvas.draw_pill((cx + 10, g_box[1] + 85), "Memory Bus: 100% TRAFFIC JAM", size=18, text_color=WHITE, bg_color=(255, 30, 50))


# ==============================================================================
# SCENE 6: THE PROFESSOR & THE HYPERACTIVE INTERN (SPECULATIVE DECODING)
# ==============================================================================
def render_story_intern_draft(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """
    Story: The Professor & The Hyperactive Intern.
    A tiny 1B intern drafts 4 words ahead in 3ms.
    The 70B Professor glances once, stamps APPROVED in one single pass.
    """
    cx = canvas.W // 2
    sc = canvas.scale

    canvas.draw_pill((cx - 160, 85), "THE ULTIMATE HACK: SPECULATIVE DECODING", size=18, text_color=CYAN,
                     bg_color=(18, 28, 48), outline_color=CYAN)

    # 1. The Hyperactive Intern (Top Lane)
    l1_box = (cx - 520, 150, cx + 520, 310)
    canvas.draw_card(l1_box, radius=16, fill=(14, 22, 38), outline=CYAN, width=2)
    canvas.draw_text((l1_box[0] + 30, l1_box[1] + 25), "THE HYPERACTIVE INTERN (1B DRAFT MODEL) -> Sprints 4 Words Ahead", size=18, fill=CYAN)

    # Tiny intern stickman running across top lane
    sprinter_x = l1_box[0] + 120 + int((rel_t * 220) % 850)
    draw_director_actor(canvas, sprinter_x, l1_box[1] + 130, scale=0.45, action="slam_enter",
                        mouth_open=0.8, expr="happy", frame_t=rel_t)

    # 2. The Wise Professor (Bottom Lane)
    l2_box = (cx - 520, 340, cx + 520, 520)
    canvas.draw_card(l2_box, radius=16, fill=(22, 16, 36), outline=PURPLE, width=2)
    canvas.draw_text((l2_box[0] + 30, l2_box[1] + 25), "THE WISE PROFESSOR (70B MODEL) -> Stamps All 4 in One Glance", size=18, fill=PURPLE)

    # Professor Stickman with glasses and clipboard
    draw_director_actor(canvas, l2_box[0] + 80, l2_box[1] + 145, scale=0.7, action="referee_stamp",
                        mouth_open=0.7 * abs(math.sin(rel_t * 14)), expr="happy", show_sunglasses=True, frame_t=rel_t)

    # 4 Drafted Words Approved
    words = ["the", "architecture", "is", "scalable"]
    for i, w in enumerate(words):
        bx = l2_box[0] + 190 + i * 180
        by = l2_box[1] + 70
        is_verified = rel_t > (1.8 + i * 0.3)
        v_col = GREEN if is_verified else PURPLE
        v_txt = "✓ APPROVED" if is_verified else "DRAFTING..."
        canvas.draw_card((bx, by, bx + 160, by + 65), radius=10, fill=(28, 20, 46), outline=v_col, width=1)
        canvas.draw_text((bx + 80, by + 24), f"\"{w}\"", size=19, fill=WHITE, anchor="mm")
        canvas.draw_text((bx + 80, by + 48), v_txt, size=14, fill=v_col, anchor="mm")

    # Multiplier Rocket
    if rel_t > 3.0:
        canvas.draw_pill((cx - 150, 560), "🚀 3.0x INFERENCE SPEEDUP", size=26, text_color=YELLOW, bg_color=(36, 30, 18), outline_color=YELLOW)


# ==============================================================================
# SCENE 7: THE GRAND RELAY RACE VERDICT & OUTRO
# ==============================================================================
def render_story_relay_outro(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any], logo_img: Optional[Image.Image] = None):
    """
    Story Outro:
    The Grand Relay Race connecting Forklift -> Sticky Notes -> Intern.
    Stickman dropkicks Subscribe button into green confetti!
    """
    cx = canvas.W // 2
    cy = canvas.H // 2 - 20
    sc = canvas.scale

    if rel_t < 2.5:
        canvas.draw_pill((cx - 160, 85), "THE ULTIMATE COMPUTER RELAY RACE", size=18, text_color=CYAN,
                         bg_color=(18, 24, 42), outline_color=(70, 220, 255, 120))
        
        draw_director_actor(canvas, cx - 280 + int(rel_t * 60), 450, scale=0.8, action="idle",
                            mouth_open=0.7 * abs(math.sin(rel_t * 14)), expr="happy", frame_t=rel_t)
        canvas.draw_text((cx + 120, 320), "AI speed isn't magic.\nIt's the most coordinated relay race ever built.", size=30, fill=WHITE, anchor="mm")

    else:
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

        btn_w, btn_h = 280, 68
        bx0, by0 = cx - btn_w // 2, cy + 85
        is_clicked = rel_outro >= 2.0

        if not is_clicked:
            canvas.draw_card((bx0, by0, bx0 + btn_w, by0 + btn_h), radius=btn_h // 2, fill=(255, 30, 50), outline=None)
            canvas.draw_text((cx, by0 + btn_h // 2), "SUBSCRIBE", size=24, fill=WHITE, anchor="mm")
            # Stickman flying dropkick
            draw_director_actor(canvas, cx + 220 - int(rel_outro * 70), by0 - 20, scale=0.75, action="slam_enter",
                                mouth_open=0.8, expr="happy", frame_t=rel_t)
        else:
            canvas.draw_card((bx0, by0, bx0 + btn_w, by0 + btn_h), radius=btn_h // 2, fill=(35, 195, 110), outline=None)
            canvas.draw_text((cx, by0 + btn_h // 2), "✓ SUBSCRIBED!", size=24, fill=WHITE, anchor="mm")
            
            # Gold Confetti
            rng = np.random.default_rng(99)
            for _ in range(26):
                px = cx + rng.integers(-220, 220)
                py = by0 + rng.integers(-100, 100)
                col = [(255, 205, 70), (70, 220, 255), (90, 235, 150)][rng.integers(0, 3)]
                p_c = canvas.to_canvas(px, py)
                canvas.draw.ellipse([p_c[0] - 4 * sc, p_c[1] - 4 * sc, p_c[0] + 4 * sc, p_c[1] + 4 * sc], fill=col)

            draw_director_actor(canvas, cx + 240, by0 + 20, scale=0.75, action="celebrate",
                                mouth_open=0.8, expr="happy", frame_t=rel_t)
