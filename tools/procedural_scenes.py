#!/usr/bin/env python3
"""
procedural_scenes.py — High-End Motion Graphics Procedural Visualizers
Eliminates static fallback cards by providing dedicated, frame-deterministic,
fully animated scenes for 'How AI Answers in Milliseconds':

1. render_hook_stopwatch: Terminal typing, millisecond stopwatch counter, GPU die schematic, FLOPs stamp.
2. render_token_fracture: Sentence breaking into token chips, 4096-dim vector expansion, 3D embedding space.
3. render_prefill_matrix: 16 Tensor Cores flashing, parallel Q x K^T GEMM calculation, 989 TFLOPS telemetry.
4. render_kv_cache_split: Naive O(N^2) recalculation loop vs KV Cache memory rack with deadbolt lock slots.
5. render_silicon_memory_stream: H100 floorplan, 140GB weight particle streams over HBM3 bus, bandwidth bottleneck.
6. render_speculative_race: Dual-lane draft vs target model racing, parallel verification sweep, 2.8x speedup.
7. render_verdict_recap: Architectural recap flow transitioning to authentic TechXKenil outro conversion.
"""

import math
from typing import Dict, Any, Optional, Tuple, List
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from tools.render_core import (
    OverscanCanvas, get_font, spring,
    WHITE, DIM, CYAN, PURPLE, YELLOW, GREEN, RED, DARK_CARD, CARD_BORDER
)

ACCENT_CYAN = CYAN
ACCENT_PURPLE = PURPLE
DIM_WHITE = DIM

def clamp(v: float, mn: float = 0.0, mx: float = 1.0) -> float:
    return max(mn, min(mx, v))

def lerp(a: float, b: float, p: float) -> float:
    return a + (b - a) * p


# ==============================================================================
# SCENE 1: THE MILLISECOND ILLUSION (HOOK)
# ==============================================================================
def render_hook_stopwatch(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """
    Renders terminal typing 'Why is the sky blue?', Enter ripple shockwave,
    rolling millisecond stopwatch (0.00ms -> 28.40ms), H100 GPU die schematic,
    parameter counter (70B), and 140 Trillion FLOPs badge.
    """
    cx = canvas.W // 2
    cy = canvas.H // 2 - 20
    sc = canvas.scale

    # 1. Top Section Pill
    canvas.draw_pill((cx - 160, 90), "STAGE 0: THE LATENCY PUZZLE", size=18, text_color=ACCENT_CYAN,
                     bg_color=(18, 24, 42), outline_color=(70, 220, 255, 120))

    # 2. Terminal Prompt Window (y = 150 to 300)
    term_box = (cx - 460, 150, cx + 460, 290)
    canvas.draw_card(term_box, radius=16, fill=(14, 18, 30), outline=(50, 70, 110), width=2)
    
    # Terminal top dots
    tx0, ty0 = canvas.to_canvas(term_box[0] + 25, term_box[1] + 22)
    for i, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        canvas.draw.ellipse([tx0 + i * 22 * sc - 6 * sc, ty0 - 6 * sc, tx0 + i * 22 * sc + 6 * sc, ty0 + 6 * sc], fill=col)

    # Terminal prompt text typing
    full_prompt = data.get("prompt_text", "Why is the sky blue?")
    type_p = clamp(rel_t / 1.4)
    n_chars = int(len(full_prompt) * type_p)
    typed = full_prompt[:n_chars]
    
    # Blinking caret
    caret = "█" if (int(rel_t * 3.0) % 2 == 0 or rel_t < 1.4) else ""
    canvas.draw_text((term_box[0] + 120, term_box[1] + 55), f"> {typed}{caret}", size=30, fill=WHITE)

    # Enter key button on right
    enter_pressed = rel_t >= 1.6
    enter_col = (70, 220, 255) if enter_pressed else (45, 60, 95)
    canvas.draw_pill((term_box[2] - 150, term_box[1] + 52), "[ENTER ↵]", size=18, text_color=WHITE, bg_color=enter_col)

    # Shockwave ripple on Enter click
    if rel_t > 1.6:
        rip_t = rel_t - 1.6
        rip_rad = min(420, int(rip_t * 320))
        rip_alpha = max(0, int(180 * (1.0 - rip_t / 1.5)))
        if rip_alpha > 0:
            rx, ry = canvas.to_canvas(term_box[2] - 90, term_box[1] + 70)
            canvas.draw.ellipse([rx - rip_rad * sc, ry - rip_rad * sc, rx + rip_rad * sc, ry + rip_rad * sc],
                                outline=(70, 220, 255, rip_alpha), width=max(1, int(2 * sc)))

    # 3. Center Left: High-Precision Millisecond Stopwatch HUD
    sw_box = (cx - 460, 320, cx - 70, 520)
    canvas.draw_card(sw_box, radius=18, fill=(16, 22, 38), outline=(70, 220, 255, 140), width=2)
    canvas.draw_text((sw_box[0] + 30, sw_box[1] + 30), "TIME-TO-FIRST-TOKEN", size=18, fill=ACCENT_CYAN)

    target_ms = data.get("target_ms", 28.40)
    if rel_t < 1.6:
        curr_ms = 0.00
    elif rel_t < 3.2:
        p_roll = (rel_t - 1.6) / 1.6
        curr_ms = target_ms * (p_roll ** 1.8)
    else:
        curr_ms = target_ms

    ms_str = f"{curr_ms:05.2f} ms"
    ms_color = YELLOW if curr_ms < target_ms else GREEN
    canvas.draw_text((sw_box[0] + 30, sw_box[1] + 75), ms_str, size=56, fill=ms_color)
    canvas.draw_text((sw_box[0] + 30, sw_box[1] + 150), "Sub-human reaction threshold", size=16, fill=DIM_WHITE)

    # 4. Center Right: H100 Silicon Die Schematic & FLOPs
    die_box = (cx - 30, 320, cx + 460, 680)
    canvas.draw_card(die_box, radius=18, fill=(13, 17, 28), outline=(150, 110, 255, 140), width=2)
    canvas.draw_text((die_box[0] + 30, die_box[1] + 30), "SILICON COMPUTE HARDWARE", size=18, fill=ACCENT_PURPLE)

    # Animated circuit traces
    c_center_x, c_center_y = die_box[0] + (die_box[2] - die_box[0]) // 2, die_box[1] + 180
    die_w, die_h = 180, 140
    canvas.draw_card((c_center_x - die_w // 2, c_center_y - die_h // 2, c_center_x + die_w // 2, c_center_y + die_h // 2),
                     radius=10, fill=(20, 26, 46), outline=(150, 110, 255), width=2)
    canvas.draw_text((c_center_x, c_center_y - 10), "H100 SXM5", size=22, fill=WHITE, anchor="mm")
    canvas.draw_text((c_center_x, c_center_y + 20), "70B FP16", size=16, fill=ACCENT_CYAN, anchor="mm")

    # Circuit rays radiating outwards
    t_pulse = rel_t * 4.0
    for ang in np.linspace(0, 2 * math.pi, 8, endpoint=False):
        dx, dy = math.cos(ang), math.sin(ang)
        r0 = 90
        r1 = 120 + 15 * math.sin(t_pulse + ang * 2)
        x_a, y_a = canvas.to_canvas(c_center_x + dx * r0, c_center_y + dy * r0)
        x_b, y_b = canvas.to_canvas(c_center_x + dx * r1, c_center_y + dy * r1)
        canvas.draw.line([x_a, y_a, x_b, y_b], fill=(150, 110, 255, 180), width=max(1, int(2 * sc)))

    # Parameter counter badge
    p_params = clamp((rel_t - 2.5) / 2.0)
    val_params = int(70 * p_params)
    canvas.draw_pill((die_box[0] + 30, die_box[3] - 70), f"Active Parameters: {val_params} Billion", size=18,
                     text_color=WHITE, bg_color=(35, 25, 60), outline_color=(150, 110, 255, 150))

    # 5. Bottom Stamp: 140 Trillion FLOPs Banner
    if rel_t > 5.0:
        stamp_t = rel_t - 5.0
        p_stamp = min(1.0, spring(stamp_t * 1.6))
        b_box = (cx - 460, 550, cx - 70, 680)
        canvas.draw_card(b_box, radius=18, fill=(28, 22, 16), outline=(255, 205, 70, int(180 * p_stamp)), width=2)
        canvas.draw_text((b_box[0] + 25, b_box[1] + 30), "COMPUTATIONAL LOAD", size=18, fill=YELLOW)
        canvas.draw_text((b_box[0] + 25, b_box[1] + 70), "140 TRILLION", size=36, fill=YELLOW)
        canvas.draw_text((b_box[0] + 25, b_box[1] + 115), "Floating point ops in 28ms", size=16, fill=DIM_WHITE)


# ==============================================================================
# SCENE 2: TOKENIZATION & VECTOR SPACE
# ==============================================================================
def render_token_fracture(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """
    Renders sentence shattering into 5 glowing token chips with IDs,
    4096-dim vector expansion, and 3D isometric embedding coordinate space.
    """
    cx = canvas.W // 2
    sc = canvas.scale

    canvas.draw_pill((cx - 160, 85), "STAGE 1: TOKENIZATION & EMBEDDING", size=18, text_color=ACCENT_CYAN,
                     bg_color=(18, 24, 42), outline_color=(70, 220, 255, 120))

    # 1. Top Raw Prompt Sentence
    canvas.draw_text((cx, 145), "\"Why is the sky blue?\"", size=32, fill=WHITE, anchor="mm")
    canvas.draw_text((cx, 185), "Language Conversion: English String -> Discrete Integer IDs", size=18, fill=DIM_WHITE, anchor="mm")

    # 2. 5 Token Chips with IDs
    tokens = data.get("tokens", [("Why", 1245), ("is", 318), ("the", 262), ("sky", 7891), ("blue", 4123)])
    n = len(tokens)
    chip_w, chip_h = 180, 110
    total_w = n * chip_w + (n - 1) * 24
    start_x = cx - total_w // 2

    for i, (tok, tid) in enumerate(tokens):
        # Staggered spring entrance
        t_enter = max(0.0, rel_t - 0.4 - i * 0.12)
        p_spring = min(1.0, spring(t_enter * 1.5))
        
        # Position with drop-down animation
        bx0 = start_x + i * (chip_w + 24)
        by0 = 230 + (1.0 - p_spring) * 40
        bx1 = bx0 + chip_w
        by1 = by0 + chip_h

        is_highlight = (tok in ["sky", "blue"]) and rel_t > 4.0
        border_col = (150, 110, 255) if is_highlight else (70, 220, 255, 140)
        fill_col = (26, 20, 42) if is_highlight else (16, 22, 38)

        canvas.draw_card((bx0, by0, bx1, by1), radius=14, fill=fill_col, outline=border_col, width=2)
        canvas.draw_text((bx0 + chip_w // 2, by0 + 35), f"\"{tok}\"", size=26, fill=WHITE, anchor="mm")
        canvas.draw_pill((bx0 + 20, by0 + 65), f"ID: {tid}", size=15, text_color=ACCENT_CYAN, bg_color=(25, 34, 58))

    # 3. Embedding Vector Expansion (y = 380 to 680)
    vec_box = (cx - 520, 380, cx + 520, 680)
    canvas.draw_card(vec_box, radius=18, fill=(12, 16, 28), outline=(70, 220, 255, 100), width=1)
    
    canvas.draw_text((vec_box[0] + 35, vec_box[1] + 30), "4096-DIMENSIONAL EMBEDDING HYPERSPACE (d_model = 4096)", size=20, fill=ACCENT_CYAN)
    
    # 3D Coordinate Grid Projection Simulation
    grid_cx, grid_cy = cx, 540
    # Draw isometric coordinate axes
    for ang, label in [(210, "X (Semantics)"), (330, "Y (Syntax)"), (90, "Z (Context)")]:
        rad = math.radians(ang)
        x_end = grid_cx + math.cos(rad) * 220
        y_end = grid_cy + math.sin(rad) * 110
        ax0, ay0 = canvas.to_canvas(grid_cx, grid_cy)
        ax1, ay1 = canvas.to_canvas(x_end, y_end)
        canvas.draw.line([ax0, ay0, ax1, ay1], fill=(55, 75, 115), width=max(1, int(1.5 * sc)))
        canvas.draw_text((x_end + math.cos(rad) * 25, y_end + math.sin(rad) * 15), label, size=14, fill=DIM_WHITE, anchor="mm")

    # Animated Vector Cluster Nodes
    node_coords = [
        (-140, -40, "Why"),
        (-60, 20, "is"),
        (20, -60, "the"),
        (130, -25, "sky"),
        (165, -15, "blue")
    ]
    for dx, dy, label in node_coords:
        nx, ny = grid_cx + dx, grid_cy + dy
        is_pair = label in ["sky", "blue"]
        col = (255, 205, 70) if is_pair else (70, 220, 255)
        
        # Draw node circle
        px, py = canvas.to_canvas(nx, ny)
        r = 8 * sc
        canvas.draw.ellipse([px - r, py - r, px + r, py + r], fill=col)
        canvas.draw_text((nx, ny - 20), label, size=16, fill=WHITE, anchor="mm")

    # Semantic affinity vector connecting 'sky' and 'blue'
    if rel_t > 3.5:
        p_line = clamp((rel_t - 3.5) / 1.0)
        p1 = canvas.to_canvas(grid_cx + 130, grid_cy - 25)
        p2 = canvas.to_canvas(grid_cx + 165, grid_cy - 15)
        px_end = lerp(p1[0], p2[0], p_line)
        py_end = lerp(p1[1], p2[1], p_line)
        canvas.draw.line([p1[0], p1[1], px_end, py_end], fill=(255, 205, 70), width=max(1, int(3 * sc)))
        if p_line >= 1.0:
            canvas.draw_pill((grid_cx + 100, grid_cy + 30), "Cosine Similarity: 0.942", size=16,
                             text_color=YELLOW, bg_color=(36, 30, 20), outline_color=(255, 205, 70, 160))


# ==============================================================================
# SCENE 3: THE PARALLEL PREFILL BLITZ
# ==============================================================================
def render_prefill_matrix(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """
    Renders 16 Tensor Core blocks firing, parallel Q x K^T attention matrix computation,
    sweeping laser scanlines, and 989 TFLOPS compute-bound telemetry.
    """
    cx = canvas.W // 2
    sc = canvas.scale

    canvas.draw_pill((cx - 160, 85), "STAGE 2: PREFILL PHASE (COMPUTE-BOUND)", size=18, text_color=GREEN,
                     bg_color=(18, 38, 28), outline_color=(90, 235, 150, 140))

    # 1. Left Stage: 16 Tensor Core Compute Array (4x4 Grid)
    tc_box = (cx - 520, 140, cx - 100, 680)
    canvas.draw_card(tc_box, radius=18, fill=(12, 18, 26), outline=(90, 235, 150, 120), width=2)
    canvas.draw_text((tc_box[0] + 30, tc_box[1] + 30), "TENSOR CORE CLUSTER (16 SM BLOCKS)", size=20, fill=GREEN)
    
    grid_x0, grid_y0 = tc_box[0] + 30, tc_box[1] + 75
    core_w, core_h = 85, 75
    gap = 14

    for row in range(4):
        for col in range(4):
            idx = row * 4 + col + 1
            bx0 = grid_x0 + col * (core_w + gap)
            by0 = grid_y0 + row * (core_h + gap)
            
            # Pulsing active green LED
            p_glow = 0.5 + 0.5 * math.sin(rel_t * 5.0 + idx * 0.4)
            c_fill = (18, int(35 + 25 * p_glow), 30)
            c_border = (90, 235, 150, int(120 + 130 * p_glow))

            canvas.draw_card((bx0, by0, bx0 + core_w, by0 + core_h), radius=8, fill=c_fill, outline=c_border, width=1)
            canvas.draw_text((bx0 + core_w // 2, by0 + 26), f"TC-{idx:02d}", size=15, fill=WHITE, anchor="mm")
            canvas.draw_text((bx0 + core_w // 2, by0 + 52), "98% ACT", size=13, fill=GREEN, anchor="mm")

    canvas.draw_pill((tc_box[0] + 30, tc_box[3] - 70), "Throughput: 989 TFLOPS (FP16 Tensor Cores)", size=17,
                     text_color=GREEN, bg_color=(20, 42, 30))

    # 2. Right Stage: Parallel Attention Matrix Heatmap Q x K^T
    mat_box = (cx - 60, 140, cx + 520, 680)
    canvas.draw_card(mat_box, radius=18, fill=(14, 18, 30), outline=(70, 220, 255, 120), width=2)
    canvas.draw_text((mat_box[0] + 30, mat_box[1] + 30), "PARALLEL ATTENTION MATRIX (Q * K^T / sqrt(d))", size=20, fill=ACCENT_CYAN)

    # 5x5 Attention Heatmap Grid
    m_x0, m_y0 = mat_box[0] + 50, mat_box[1] + 80
    cell_sz = 68
    words = ["Why", "is", "the", "sky", "blue"]

    # Header labels
    for j, w in enumerate(words):
        canvas.draw_text((m_x0 + j * (cell_sz + 8) + cell_sz // 2, m_y0 - 20), w, size=15, fill=ACCENT_CYAN, anchor="mm")
        canvas.draw_text((m_x0 - 25, m_y0 + j * (cell_sz + 8) + cell_sz // 2), w, size=15, fill=ACCENT_CYAN, anchor="mm")

    # Heatmap values simulation
    rng = np.random.default_rng(99)
    weights = rng.uniform(0.1, 0.95, (5, 5))
    weights[3, 4] = 0.96 # sky -> blue
    weights[4, 3] = 0.96

    # Sweeping laser scanline
    scan_y = (rel_t * 1.8) % 6.0
    for r in range(5):
        for c in range(5):
            val = weights[r, c]
            cx0 = m_x0 + c * (cell_sz + 8)
            cy0 = m_y0 + r * (cell_sz + 8)
            
            # Color interpolates based on attention weight
            intensity = int(val * 220)
            cell_col = (int(intensity * 0.3), int(intensity * 0.8), intensity)
            
            # Glow if scanline passes
            if abs(r - scan_y) < 0.8:
                cell_col = (int(intensity * 0.4), 255, 230)

            canvas.draw_card((cx0, cy0, cx0 + cell_sz, cy0 + cell_sz), radius=6, fill=cell_col, outline=(70, 220, 255, 90), width=1)
            canvas.draw_text((cx0 + cell_sz // 2, cy0 + cell_sz // 2), f"{val:.2f}", size=16, fill=WHITE, anchor="mm")

    canvas.draw_pill((mat_box[0] + 50, mat_box[3] - 70), "Status: 100% Core Saturation (Compute-Bound)", size=17,
                     text_color=WHITE, bg_color=(25, 45, 75))


# ==============================================================================
# SCENE 4: THE KV CACHE MIRACLE (SPLIT SCREEN)
# ==============================================================================
def render_kv_cache_split(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """
    Renders Split Screen comparison:
    Left: Red O(N^2) naive recalculation disaster loop with hazard alert.
    Right: Cyan/Green KV Cache memory rack locking past tokens into HBM3 at 3.35 TB/s.
    """
    cx = canvas.W // 2
    sc = canvas.scale

    canvas.draw_pill((cx - 160, 85), "THE BOTTLENECK & THE KV CACHE FIX", size=18, text_color=YELLOW,
                     bg_color=(38, 30, 18), outline_color=(255, 205, 70, 140))

    # 1. Left Side: Naive Recalculation (O(N^2) Lag)
    left_box = (cx - 520, 140, cx - 20, 680)
    canvas.draw_card(left_box, radius=18, fill=(24, 14, 16), outline=(255, 70, 90, 140), width=2)
    canvas.draw_text((left_box[0] + 30, left_box[1] + 30), "WITHOUT CACHE (NAIVE O(N^2))", size=20, fill=RED)
    
    # Red redundant computation cycle diagram
    circ_cx, circ_cy = left_box[0] + (left_box[2] - left_box[0]) // 2, 330
    rot = rel_t * 3.5
    for i in range(6):
        a = rot + i * (math.pi / 3)
        rx, ry = circ_cx + math.cos(a) * 90, circ_cy + math.sin(a) * 90
        canvas.draw_pill((rx - 45, ry - 18), f"Token {i+1}", size=15, text_color=WHITE, bg_color=(75, 20, 25))

    canvas.draw_text((circ_cx, circ_cy), "RE-COMPUTE\nEVERY TOKEN", size=18, fill=RED, anchor="mm")
    canvas.draw_pill((left_box[0] + 30, 480), "Complexity: O(N^2) Quadratic Blowup", size=17, text_color=RED, bg_color=(45, 15, 20))
    canvas.draw_pill((left_box[0] + 30, 545), "Result: 1.2 Tokens / Second (Unusable)", size=17, text_color=WHITE, bg_color=(45, 15, 20))

    # 2. Right Side: With KV Cache (HBM3 Memory Slots)
    right_box = (cx + 20, 140, cx + 520, 680)
    canvas.draw_card(right_box, radius=18, fill=(12, 22, 28), outline=(70, 220, 255, 140), width=2)
    canvas.draw_text((right_box[0] + 30, right_box[1] + 30), "WITH KV CACHE (LINEAR O(1) STEP)", size=20, fill=ACCENT_CYAN)

    # Memory Rack with locked slots
    slot_words = [("Token 1", "Why"), ("Token 2", "is"), ("Token 3", "the"), ("Token 4", "sky"), ("Token 5", "blue")]
    s_x0, s_y0 = right_box[0] + 30, right_box[1] + 80
    slot_w, slot_h = 440, 52

    for idx, (tlabel, twrd) in enumerate(slot_words):
        sy = s_y0 + idx * (slot_h + 12)
        is_locked = rel_t > (0.6 + idx * 0.4)
        
        status_text = "[KV CACHED ✓]" if is_locked else "[COMPUTING...]"
        status_col = GREEN if is_locked else YELLOW
        bg_col = (18, 32, 40) if is_locked else (24, 28, 36)

        canvas.draw_card((s_x0, sy, s_x0 + slot_w, sy + slot_h), radius=8, fill=bg_col,
                         outline=(90, 235, 150, 120) if is_locked else (80, 100, 130), width=1)
        canvas.draw_text((s_x0 + 20, sy + 16), f"{tlabel}: \"{twrd}\"", size=17, fill=WHITE)
        canvas.draw_text((s_x0 + slot_w - 140, sy + 16), status_text, size=16, fill=status_col)

    canvas.draw_pill((right_box[0] + 30, 545), "Speed: 85+ Tokens / Sec (3.35 TB/s HBM3)", size=17,
                     text_color=GREEN, bg_color=(18, 42, 30))


# ==============================================================================
# SCENE 5: THE MEMORY BANDWIDTH BOTTLENECK
# ==============================================================================
def render_silicon_memory_stream(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """
    Renders H100 GPU Floorplan, showing 140 GB weight data particle streams
    rushing across the Silicon Interposer, and the Arithmetic Intensity bottleneck.
    """
    cx = canvas.W // 2
    sc = canvas.scale

    canvas.draw_pill((cx - 160, 85), "STAGE 3: THE DECODE BOTTLENECK", size=18, text_color=RED,
                     bg_color=(38, 18, 22), outline_color=(255, 70, 90, 140))

    # 1. H100 Silicon Floorplan
    chip_box = (cx - 520, 140, cx + 520, 480)
    canvas.draw_card(chip_box, radius=18, fill=(13, 17, 28), outline=(70, 220, 255, 120), width=2)
    canvas.draw_text((chip_box[0] + 30, chip_box[1] + 25), "NVIDIA H100 PHYSICAL SILICON TOPOLOGY", size=20, fill=ACCENT_CYAN)

    # Left HBM3 Stack
    hbm_left = (chip_box[0] + 40, chip_box[1] + 70, chip_box[0] + 240, chip_box[3] - 40)
    canvas.draw_card(hbm_left, radius=12, fill=(20, 28, 52), outline=(70, 220, 255), width=2)
    canvas.draw_text((hbm_left[0] + 20, hbm_left[1] + 30), "HBM3 STACK\n40 GB VRAM", size=20, fill=WHITE)
    canvas.draw_text((hbm_left[0] + 20, hbm_left[1] + 120), "3.35 TB/s\nBandwidth", size=17, fill=ACCENT_CYAN)

    # Right HBM3 Stack
    hbm_right = (chip_box[2] - 240, chip_box[1] + 70, chip_box[2] - 40, chip_box[3] - 40)
    canvas.draw_card(hbm_right, radius=12, fill=(20, 28, 52), outline=(70, 220, 255), width=2)
    canvas.draw_text((hbm_right[0] + 20, hbm_right[1] + 30), "HBM3 STACK\n40 GB VRAM", size=20, fill=WHITE)
    canvas.draw_text((hbm_right[0] + 20, hbm_right[1] + 120), "3.35 TB/s\nBandwidth", size=17, fill=ACCENT_CYAN)

    # Center Compute Die (Streaming Multiprocessors)
    compute_die = (cx - 150, chip_box[1] + 70, cx + 150, chip_box[3] - 40)
    canvas.draw_card(compute_die, radius=12, fill=(26, 20, 42), outline=(150, 110, 255), width=2)
    canvas.draw_text((cx, chip_box[1] + 120), "COMPUTE DIE", size=22, fill=WHITE, anchor="mm")
    canvas.draw_text((cx, chip_box[1] + 155), "144 SM Cores", size=18, fill=ACCENT_PURPLE, anchor="mm")

    # Animated streaming data particles across Silicon Interposer
    t_stream = rel_t * 600
    for lane in range(6):
        py = chip_box[1] + 110 + lane * 30
        # Left stream into center
        px_left = (hbm_left[2] + int(t_stream + lane * 40)) % (compute_die[0] - hbm_left[2])
        p_c1 = canvas.to_canvas(hbm_left[2] + px_left, py)
        canvas.draw.ellipse([p_c1[0] - 4 * sc, p_c1[1] - 4 * sc, p_c1[0] + 4 * sc, p_c1[1] + 4 * sc], fill=(70, 220, 255))

        # Right stream into center
        px_right = (hbm_right[0] - int(t_stream + lane * 40))
        if px_right < compute_die[2]:
            px_right = hbm_right[0] - (hbm_right[0] - px_right) % (hbm_right[0] - compute_die[2])
        p_c2 = canvas.to_canvas(px_right, py)
        canvas.draw.ellipse([p_c2[0] - 4 * sc, p_c2[1] - 4 * sc, p_c2[0] + 4 * sc, p_c2[1] + 4 * sc], fill=(150, 110, 255))

    # 2. Bottom Comparative Bottleneck Gauges (y = 510 to 680)
    g_box = (cx - 520, 510, cx + 520, 680)
    canvas.draw_card(g_box, radius=16, fill=(16, 20, 32), outline=(255, 70, 90, 100), width=1)
    
    # Left Gauge: Compute cores idle
    canvas.draw_text((g_box[0] + 40, g_box[1] + 30), "GPU TENSOR CORES UTILIZATION (MATH)", size=18, fill=DIM_WHITE)
    canvas.draw_card((g_box[0] + 40, g_box[1] + 65, g_box[0] + 460, g_box[1] + 95), radius=8, fill=(24, 30, 48), outline=None)
    canvas.draw_card((g_box[0] + 40, g_box[1] + 65, g_box[0] + 140, g_box[1] + 95), radius=8, fill=(80, 100, 140), outline=None)
    canvas.draw_text((g_box[0] + 155, g_box[1] + 72), "22% (Cores Idling)", size=16, fill=DIM_WHITE)

    # Right Gauge: Memory bandwidth saturated
    canvas.draw_text((cx + 40, g_box[1] + 30), "HBM3 MEMORY BUS (WEIGHT TRANSFER)", size=18, fill=YELLOW)
    canvas.draw_card((cx + 40, g_box[1] + 65, cx + 460, g_box[1] + 95), radius=8, fill=(24, 30, 48), outline=None)
    canvas.draw_card((cx + 40, g_box[1] + 65, cx + 450, g_box[1] + 95), radius=8, fill=(255, 70, 90), outline=None)
    canvas.draw_text((cx + 400, g_box[1] + 72), "100% SATURATED", size=16, fill=WHITE)

    canvas.draw_text((cx, g_box[1] + 130), "Every single token requires streaming all 140 GB of model weights through silicon.", size=17, fill=WHITE, anchor="mm")


# ==============================================================================
# SCENE 6: SPECULATIVE DECODING RACE
# ==============================================================================
def render_speculative_race(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any]):
    """
    Renders Dual-Lane raceway:
    Lane 1: 1B Draft Model sprint-generating 4 tokens in 4ms.
    Lane 2: 70B Target Model verifying all 4 tokens in 1 parallel pass with green checkmarks.
    """
    cx = canvas.W // 2
    sc = canvas.scale

    canvas.draw_pill((cx - 160, 85), "THE SUPERCHARGER: SPECULATIVE DECODING", size=18, text_color=ACCENT_CYAN,
                     bg_color=(18, 28, 48), outline_color=(70, 220, 255, 140))

    # 1. Lane 1: 1B Draft Model
    l1_box = (cx - 520, 150, cx + 520, 310)
    canvas.draw_card(l1_box, radius=16, fill=(14, 22, 38), outline=(70, 220, 255, 140), width=2)
    canvas.draw_text((l1_box[0] + 30, l1_box[1] + 25), "FAST DRAFT MODEL (1B PARAMETERS) -> Speculates 4 Tokens", size=18, fill=ACCENT_CYAN)

    draft_words = data.get("draft_tokens", ["the", "architecture", "is", "scalable"])
    w_x0 = l1_box[0] + 260
    for i, w in enumerate(draft_words):
        bx = w_x0 + i * 180
        t_w = max(0.0, rel_t - 0.2 - i * 0.15)
        p_sp = min(1.0, spring(t_w * 2.0))
        by = l1_box[1] + 65 + (1.0 - p_sp) * 20
        canvas.draw_card((bx, by, bx + 160, by + 65), radius=10, fill=(20, 32, 56), outline=(70, 220, 255), width=1)
        canvas.draw_text((bx + 80, by + 32), f"\"{w}\"", size=20, fill=WHITE, anchor="mm")

    # 2. Lane 2: 70B Target Model Parallel Validation
    l2_box = (cx - 520, 340, cx + 520, 520)
    canvas.draw_card(l2_box, radius=16, fill=(22, 16, 36), outline=(150, 110, 255, 140), width=2)
    canvas.draw_text((l2_box[0] + 30, l2_box[1] + 25), "TARGET MODEL (70B PARAMETERS) -> Single Parallel Verification", size=18, fill=ACCENT_PURPLE)

    # Verification Laser sweep
    if rel_t > 2.0:
        sweep_p = clamp((rel_t - 2.0) / 1.5)
        laser_x = lerp(w_x0, w_x0 + 4 * 180, sweep_p)
        lx0, ly0 = canvas.to_canvas(laser_x, l2_box[1] + 55)
        lx1, ly1 = canvas.to_canvas(laser_x, l2_box[3] - 25)
        canvas.draw.line([lx0, ly0, lx1, ly1], fill=(90, 235, 150), width=max(1, int(4 * sc)))

    for i, w in enumerate(draft_words):
        bx = w_x0 + i * 180
        by = l2_box[1] + 65
        is_verified = rel_t > (2.2 + i * 0.25)
        v_col = GREEN if is_verified else (150, 110, 255)
        v_txt = "✓ ACCEPTED" if is_verified else "PENDING..."

        canvas.draw_card((bx, by, bx + 160, by + 65), radius=10, fill=(28, 20, 46), outline=v_col, width=1)
        canvas.draw_text((bx + 80, by + 24), f"\"{w}\"", size=19, fill=WHITE, anchor="mm")
        canvas.draw_text((bx + 80, by + 48), v_txt, size=14, fill=v_col, anchor="mm")

    # 3. Speed Multiplier Badge (y = 550 to 680)
    if rel_t > 3.5:
        p_pop = min(1.0, spring((rel_t - 3.5) * 1.5))
        m_box = (cx - 360, 560, cx + 360, 670)
        canvas.draw_card(m_box, radius=18, fill=(26, 22, 14), outline=(255, 205, 70, int(200 * p_pop)), width=2)
        canvas.draw_text((cx, 595), "⚡ 2.8x INFERENCE SPEEDUP", size=32, fill=YELLOW, anchor="mm")
        canvas.draw_text((cx, 635), "4 Tokens Generated in the Time of 1 Forward Pass", size=18, fill=WHITE, anchor="mm")


# ==============================================================================
# SCENE 7: VERDICT RECAP & CONVERSION OUTRO
# ==============================================================================
def render_verdict_recap(canvas: OverscanCanvas, rel_t: float, dur: float, data: Dict[str, Any], logo_img: Optional[Image.Image] = None):
    """
    Renders 5-stage inference pipeline recap (first 2.5s)
    then transitions smoothly to official TechXKenil obsidian outro conversion card.
    """
    cx = canvas.W // 2
    cy = canvas.H // 2 - 20
    sc = canvas.scale

    if rel_t < 2.5:
        # 5-Stage Architecture Summary Flow
        canvas.draw_pill((cx - 160, 85), "THE 5 PILLARS OF MILLISECOND AI", size=18, text_color=ACCENT_CYAN,
                         bg_color=(18, 24, 42), outline_color=(70, 220, 255, 120))
        
        stages = [
            ("1. Tokenizer", "0.2ms Vector Warp", ACCENT_CYAN),
            ("2. Prefill GEMM", "Parallel Attention", GREEN),
            ("3. KV Cache", "Zero Re-computation", YELLOW),
            ("4. HBM3 Bus", "3.35 TB/s Streaming", RED),
            ("5. Speculative", "2.8x Multiplier", ACCENT_PURPLE)
        ]
        s_w, s_h = 200, 360
        total_w = 5 * s_w + 4 * 16
        x_start = cx - total_w // 2

        for i, (title, sub, col) in enumerate(stages):
            sx0 = x_start + i * (s_w + 16)
            canvas.draw_card((sx0, 160, sx0 + s_w, 160 + s_h), radius=14, fill=(16, 20, 32), outline=col, width=2)
            canvas.draw_text((sx0 + s_w // 2, 220), title, size=20, fill=WHITE, anchor="mm")
            canvas.draw_text((sx0 + s_w // 2, 280), sub, size=15, fill=col, anchor="mm")
            canvas.draw_text((sx0 + s_w // 2, 440), f"Pillar 0{i+1}", size=14, fill=DIM_WHITE, anchor="mm")

    else:
        # Official TechXKenil Outro Conversion Card
        rel_outro = rel_t - 2.5
        p_scale = min(1.0, spring(rel_outro * 1.5))
        card_box = (cx - 420, cy - 250, cx + 420, cy + 250)
        canvas.draw_card(card_box, radius=24, fill=(16, 22, 38), outline=(255, 70, 90, 140), width=2)

        # Ring logo
        if logo_img:
            logo_sz = int(140 * sc)
            resized_logo = logo_img.resize((logo_sz, logo_sz), Image.Resampling.LANCZOS)
            lx, ly = canvas.to_canvas(cx - 70, cy - 200)
            canvas.frame.paste(resized_logo, (int(lx), int(ly)), resized_logo)

        canvas.draw_text((cx, cy - 35), "TECHXKENIL", size=42, fill=WHITE, anchor="mm")
        canvas.draw_text((cx, cy + 15), "AI • TECH • CODE", size=20, fill=(150, 170, 220), anchor="mm")

        # Interactive conversion sequence: Click at t = 2.4s after outro start
        is_clicked = rel_outro >= 2.4
        btn_w, btn_h = 280, 68
        bx0, by0 = cx - btn_w // 2, cy + 85
        
        btn_scale = 0.92 if (2.4 <= rel_outro <= 2.6) else 1.0
        cur_w, cur_h = int(btn_w * btn_scale), int(btn_h * btn_scale)
        b_box = (cx - cur_w // 2, (by0 + btn_h // 2) - cur_h // 2, cx + cur_w // 2, (by0 + btn_h // 2) + cur_h // 2)

        if not is_clicked:
            canvas.draw_card(b_box, radius=cur_h // 2, fill=(255, 30, 50), outline=None)
            canvas.draw_text((cx, by0 + btn_h // 2), "SUBSCRIBE", size=24, fill=WHITE, anchor="mm")
        else:
            canvas.draw_card(b_box, radius=cur_h // 2, fill=(35, 195, 110), outline=None)
            canvas.draw_text((cx, by0 + btn_h // 2), "✓ SUBSCRIBED!", size=24, fill=WHITE, anchor="mm")
            
            # Gold expanding ripple
            rip_t = rel_outro - 2.4
            rip_r = min(160, int(rip_t * 220))
            rx, ry = canvas.to_canvas(cx, by0 + btn_h // 2)
            canvas.draw.ellipse([rx - rip_r * sc, ry - rip_r * sc, rx + rip_r * sc, ry + rip_r * sc],
                                outline=(255, 205, 70, max(0, int(180 * (1.0 - rip_t / 1.0)))), width=max(1, int(3 * sc)))

        # Animated cursor gliding in
        p_cur = clamp(rel_outro / 2.4)
        cur_x = lerp(cx + 420, cx, p_cur)
        cur_y = lerp(cy + 240, by0 + btn_h // 2 + 10, p_cur)
        if rel_outro < 3.2:
            cx_pix, cy_pix = canvas.to_canvas(cur_x, cur_y)
            # Draw pointer cursor arrow
            canvas.draw.polygon([
                (cx_pix, cy_pix),
                (cx_pix + 18 * sc, cy_pix + 24 * sc),
                (cx_pix + 8 * sc, cy_pix + 25 * sc),
                (cx_pix, cy_pix + 35 * sc)
            ], fill=WHITE, outline=(0, 0, 0))
