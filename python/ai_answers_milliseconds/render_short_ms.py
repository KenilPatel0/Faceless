import os, sys, json, math, time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
TOOLS_DIR = os.path.join(REPO_ROOT, "python", "tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from motion import SS, spring, count_up, word_pop, pulse, drift, finish, open_encoder, transition, blur_layer
from humanize import word_timings, push_in, ease_out_expo, ease_out_quart, clamp

W, H, FPS = 1080, 1920, 30
FONT_PATH = os.path.join(REPO_ROOT, "fonts", "InterDisplay-Bold.otf")
CAPTION_FONT_PATH = os.path.join(REPO_ROOT, "fonts", "BebasNeue-Regular.ttf")

# Channel Palette
BG1, BG2 = (8, 12, 28), (30, 16, 70)
WHITE = (255, 255, 255)
DIM = (185, 192, 225)
CYAN = (70, 220, 255)
YELLOW = (255, 205, 70)
GREEN = (90, 235, 150)
RED = (255, 70, 90)
PURPLE = (150, 110, 255)
SUB_RED = (255, 30, 50)

# Pre-render background gradient and grid
base_bg = Image.new("RGB", (W, H))
d_base = ImageDraw.Draw(base_bg)
for y in range(H):
    t_y = y / H
    col = tuple(int(BG1[i] + (BG2[i] - BG1[i]) * t_y) for i in range(3))
    d_base.line([(0, y), (W, y)], fill=col)
for x in range(0, W, 90):
    d_base.line([(x, 0), (x, H)], fill=(22, 28, 58))
for y in range(0, H, 90):
    d_base.line([(0, y), (W, y)], fill=(22, 28, 58))

meta = json.load(open(os.path.join(SCRIPT_DIR, "meta_short_ms.json")))
audio_file = os.path.join(SCRIPT_DIR, "audio_short_ms.wav")
output_mp4 = os.path.join(SCRIPT_DIR, "ai_answers_milliseconds_30s.mp4")

# Build caption chunks with per-word timings
caption_chunks = []
for sc in meta["scenes"]:
    wtimes = word_timings(sc["text"], sc["start"], sc["end"])
    i = 0
    while i < len(wtimes):
        chunk = wtimes[i:i+4]
        c_start = chunk[0][1]
        c_end = chunk[-1][2]
        caption_chunks.append({
            "words": chunk,
            "start": c_start,
            "end": c_end
        })
        i += 4

def draw_captions(ss, t):
    f_cap = ss.font(CAPTION_FONT_PATH, 82)
    for ch in caption_chunks:
        if ch["start"] <= t <= ch["end"]:
            words = ch["words"]
            wd_lens = [ss.tlen(w.upper() + " ", f_cap) for w, _, _ in words]
            tot_w = sum(wd_lens)
            cur_x = 540 - tot_w / 2
            for (w, s, e), wd in zip(words, wd_lens):
                is_active = (s <= t < e)
                color = YELLOW if is_active else WHITE
                ss.text((cur_x, 1560), w.upper(), f_cap, anchor="lm", stroke=3.5, fill=color, stroke_fill=(0, 0, 0))
                cur_x += wd
            break

def draw_brand_tag(ss):
    f_tag = ss.font(FONT_PATH, 52)
    ss.text((540, 150), "TechXKenil", f_tag, anchor="mm", fill=(160, 170, 210))

def render_content_layer(t):
    """Draws content on SS supersampled canvas (sub-pixel anti-aliasing)"""
    ss = SS((W, H), S=2)
    
    # Identify scene
    sc_idx = 0
    for idx, sc in enumerate(meta["scenes"]):
        if sc["start"] <= t <= sc["end"]:
            sc_idx = idx
            break
    sc = meta["scenes"][sc_idx]
    local_t = t - sc["start"]
    dur = sc["dur"]
    
    if sc_idx == 0:  # Hook: Millisecond Paradox
        draw_brand_tag(ss)
        s = spring(local_t, freq=2.2, zeta=0.72)
        
        # Pill badge
        f_pill = ss.font(FONT_PATH, 32)
        ss.rrect([540 - 280, 240, 540 + 280, 296], radius=28, fill=(18, 28, 54), outline=CYAN, width=2)
        ss.text((540, 268), "SPEED MYSTERY // 40 MILLISECONDS", f_pill, anchor="mm", fill=CYAN)
        
        # Kinetic headline
        f_head1 = ss.font(FONT_PATH, 74)
        f_head2 = ss.font(FONT_PATH, 80)
        word_pop(ss, (540, 380), ["HOW", "DOES", "AI"], local_t, 0.1, f_head1, color=WHITE, delay=0.1)
        word_pop(ss, (540, 470), ["ANSWER", "SO", "FAST?"], local_t, 0.4, f_head2, color=CYAN, delay=0.1)
        
        # Stopwatch hero card
        card_y = 660
        ss.rrect([540 - 430, card_y, 540 + 430, card_y + 400], radius=40, fill=(14, 20, 42), outline=CYAN, width=3)
        
        f_sub = ss.font(FONT_PATH, 34)
        ss.text((540, card_y + 60), "TIME TO FIRST TOKEN (TTFT)", f_sub, anchor="mm", fill=DIM)
        
        # Digital counter
        ms_val = min(42, int(local_t / 1.5 * 42)) if local_t < 1.5 else 42
        f_cnt = ss.font(FONT_PATH, 96)
        ss.text((540 - 80, card_y + 180), f"00:00:{ms_val:02d}", f_cnt, anchor="mm", fill=YELLOW)
        f_unit = ss.font(FONT_PATH, 56)
        ss.text((540 + 210, card_y + 180), "ms", f_unit, anchor="mm", fill=CYAN)
        
        # Smooth progress bar
        bar_w = 700
        p_bar = min(1.0, local_t / 1.5)
        ss.rrect([540 - bar_w/2, card_y + 270, 540 + bar_w/2, card_y + 284], radius=7, fill=(28, 36, 68))
        if p_bar > 0:
            ss.rrect([540 - bar_w/2, card_y + 270, 540 - bar_w/2 + bar_w * p_bar, card_y + 284], radius=7, fill=CYAN)
            
        f_stat = ss.font(FONT_PATH, 32)
        ss.text((540, card_y + 340), "● STREAMING TOKENS IN REAL-TIME", f_stat, anchor="mm", fill=GREEN)
        
        # Contrast comparison card
        comp_y = 1180
        ss.rrect([540 - 430, comp_y, 540 + 430, comp_y + 190], radius=32, fill=(20, 16, 46), outline=PURPLE, width=2)
        f_c1 = ss.font(FONT_PATH, 32)
        ss.text((540, comp_y + 50), "HUMAN EYE BLINK: 150 - 400 MS", f_c1, anchor="mm", fill=WHITE)
        f_c2 = ss.font(FONT_PATH, 42)
        ss.text((540, comp_y + 120), "AI FIRST WORD: 40 MS (4X FASTER!)", f_c2, anchor="mm", fill=GREEN)
        
    elif sc_idx == 1:  # Intro (Brand Lock)
        s = spring(local_t, freq=2.4, zeta=0.7)
        r = max(1, int(150 * s))
        # Purple ring circle
        ss.ellipse([540 - r, 720 - r, 540 + r, 720 + r], outline=PURPLE, width=18)
        f_txk = ss.font(FONT_PATH, max(1, int(84 * s)))
        ss.text((540, 720), "TXK", f_txk, anchor="mm", fill=WHITE)
        
        if local_t > 0.3:
            f_name = ss.font(FONT_PATH, 130)
            ss.text((540, 1000), "TechXKenil", f_name, anchor="mm", fill=WHITE)
            
        if local_t > 0.8:
            f_tag = ss.font(FONT_PATH, 48)
            ss.text((540, 1120), "AI  •  TECH  •  CODE", f_tag, anchor="mm", fill=CYAN)
            
    elif sc_idx == 2:  # Silicon & Bandwidth Paradox
        draw_brand_tag(ss)
        
        if local_t < 5.4:  # Part 1: Compute paradox
            f_p = ss.font(FONT_PATH, 32)
            ss.rrect([540 - 240, 240, 540 + 240, 296], radius=28, fill=(36, 30, 20), outline=YELLOW, width=2)
            ss.text((540, 268), "PART 1 // THE COMPUTE PARADOX", f_p, anchor="mm", fill=YELLOW)
            
            f_t = ss.font(FONT_PATH, 62)
            ss.text((540, 360), "140 BILLION MATH OPS", f_t, anchor="mm", fill=WHITE)
            f_sub = ss.font(FONT_PATH, 32)
            ss.text((540, 424), "REQUIRED FOR JUST ONE SINGLE WORD", f_sub, anchor="mm", fill=DIM)
            
            # Big Counter Card
            c_y = 520
            ss.rrect([540 - 440, c_y, 540 + 440, c_y + 360], radius=36, fill=(24, 20, 48), outline=YELLOW, width=3)
            f_clbl = ss.font(FONT_PATH, 34)
            ss.text((540, c_y + 60), "MATRIX CALCULATIONS PER TOKEN", f_clbl, anchor="mm", fill=DIM)
            
            val = min(140, int(local_t / 2.0 * 140)) if local_t < 2.0 else 140
            f_num = ss.font(FONT_PATH, 70)
            ss.text((540, c_y + 170), f"{val},000,000,000", f_num, anchor="mm", fill=YELLOW)
            f_pill2 = ss.font(FONT_PATH, 30)
            ss.text((540, c_y + 270), "140 TFLOPS OF TENSOR OPERATIONS", f_pill2, anchor="mm", fill=WHITE)
            
            # Bottleneck card
            b_y = 960
            ss.rrect([540 - 440, b_y, 540 + 440, b_y + 240], radius=32, fill=(34, 16, 26), outline=RED, width=3)
            f_bt = ss.font(FONT_PATH, 38)
            ss.text((540, b_y + 55), "STANDARD PC (DDR5 RAM)", f_bt, anchor="mm", fill=WHITE)
            f_bs = ss.font(FONT_PATH, 44)
            ss.text((540, b_y + 120), "SPEED: ~60 GB/S -> SYSTEM FREEZES!", f_bs, anchor="mm", fill=RED)
            f_bd = ss.font(FONT_PATH, 30)
            ss.text((540, b_y + 180), "Takes 30 seconds just to read model weights", f_bd, anchor="mm", fill=DIM)
            
        else:  # Part 2: HBM3e Silicon
            s2 = spring(local_t - 5.4, freq=2.2, zeta=0.72)
            f_p = ss.font(FONT_PATH, 32)
            ss.rrect([540 - 240, 240, 540 + 240, 296], radius=28, fill=(16, 32, 52), outline=CYAN, width=2)
            ss.text((540, 268), "PART 2 // MEMORY BANDWIDTH", f_p, anchor="mm", fill=CYAN)
            
            f_t = ss.font(FONT_PATH, 60)
            ss.text((540, 360), "HBM3e 3D-STACKED SILICON", f_t, anchor="mm", fill=WHITE)
            f_sub = ss.font(FONT_PATH, 30)
            ss.text((540, 424), "WEIGHTS STREAM DIRECTLY TO TENSOR CORES", f_sub, anchor="mm", fill=DIM)
            
            # Silicon Diagram
            d_y = 520
            ss.rrect([540 - 440, d_y, 540 + 440, d_y + 360], radius=36, fill=(14, 22, 42), outline=(50, 80, 130), width=2)
            # GPU Die center
            ss.rrect([540 - 150, d_y + 90, 540 + 150, d_y + 270], radius=20, fill=(24, 44, 86), outline=CYAN, width=3)
            f_gpu = ss.font(FONT_PATH, 36)
            ss.text((540, d_y + 160), "AI PROCESSOR", f_gpu, anchor="mm", fill=WHITE)
            f_core = ss.font(FONT_PATH, 26)
            ss.text((540, d_y + 205), "TENSOR CORES", f_core, anchor="mm", fill=CYAN)
            
            # Animated photon pulses along memory traces
            pulse_phase = (local_t * 3.0) % 1.0
            
            # HBM Stacks
            for idx, dy_hbm in enumerate([-80, 0, 80]):
                # Left HBM
                ss.rrect([540 - 390, d_y + 180 + dy_hbm - 24, 540 - 220, d_y + 180 + dy_hbm + 24], radius=10, fill=(30, 24, 60), outline=PURPLE, width=2)
                f_hbm = ss.font(FONT_PATH, 22)
                ss.text((540 - 305, d_y + 180 + dy_hbm), "HBM3e DIE", f_hbm, anchor="mm", fill=WHITE)
                ss.line([(540 - 220, d_y + 180 + dy_hbm), (540 - 150, d_y + 180 + dy_hbm)], fill=CYAN, width=3)
                
                # Glowing data pulse
                px_l = 540 - 220 + 70 * ((pulse_phase + idx * 0.33) % 1.0)
                ss.ellipse([px_l - 6, d_y + 180 + dy_hbm - 6, px_l + 6, d_y + 180 + dy_hbm + 6], fill=YELLOW)
                
                # Right HBM
                ss.rrect([540 + 220, d_y + 180 + dy_hbm - 24, 540 + 390, d_y + 180 + dy_hbm + 24], radius=10, fill=(30, 24, 60), outline=PURPLE, width=2)
                ss.text((540 + 305, d_y + 180 + dy_hbm), "HBM3e DIE", f_hbm, anchor="mm", fill=WHITE)
                ss.line([(540 + 150, d_y + 180 + dy_hbm), (540 + 220, d_y + 180 + dy_hbm)], fill=CYAN, width=3)
                
                px_r = 540 + 220 - 70 * ((pulse_phase + idx * 0.33) % 1.0)
                ss.ellipse([px_r - 6, d_y + 180 + dy_hbm - 6, px_r + 6, d_y + 180 + dy_hbm + 6], fill=YELLOW)
                
            f_dtop = ss.font(FONT_PATH, 28)
            ss.text((540, d_y + 40), "SILICON INTERPOSER BUS (ZERO WIRE DELAY)", f_dtop, anchor="mm", fill=DIM)
            
            # Bandwidth metric card
            m_y = 940
            ss.rrect([540 - 440, m_y, 540 + 440, m_y + 260], radius=32, fill=(16, 36, 58), outline=CYAN, width=3)
            f_mlbl = ss.font(FONT_PATH, 32)
            ss.text((540, m_y + 50), "STREAMING BANDWIDTH", f_mlbl, anchor="mm", fill=DIM)
            f_mnum = ss.font(FONT_PATH, 80)
            ss.text((540, m_y + 130), "3,350 GB / SEC", f_mnum, anchor="mm", fill=CYAN)
            f_mpill = ss.font(FONT_PATH, 34)
            ss.text((540, m_y + 205), "⚡ 55X FASTER THAN DDR5 RAM", f_mpill, anchor="mm", fill=GREEN)
            
    elif sc_idx == 3:  # KV Cache & Outro
        if local_t < 5.2:  # KV Cache
            draw_brand_tag(ss)
            f_p = ss.font(FONT_PATH, 32)
            ss.rrect([540 - 240, 240, 540 + 240, 296], radius=28, fill=(18, 38, 30), outline=GREEN, width=2)
            ss.text((540, 268), "PART 3 // ZERO RECALCULATION", f_p, anchor="mm", fill=GREEN)
            
            f_t = ss.font(FONT_PATH, 62)
            ss.text((540, 360), "THE KV CACHE ENGINE", f_t, anchor="mm", fill=WHITE)
            f_sub = ss.font(FONT_PATH, 32)
            ss.text((540, 424), "PAST TOKENS ARE LOCKED IN ULTRA-FAST SRAM", f_sub, anchor="mm", fill=DIM)
            
            # Architecture Card
            kv_y = 500
            ss.rrect([540 - 440, kv_y, 540 + 440, kv_y + 400], radius=36, fill=(16, 26, 44), outline=GREEN, width=3)
            
            # Step 1: Prompt Tokens
            ss.rrect([540 - 380, kv_y + 50, 540 + 380, kv_y + 120], radius=16, fill=(24, 38, 64), outline=CYAN, width=2)
            f_step1 = ss.font(FONT_PATH, 32)
            ss.text((540, kv_y + 85), "[ PROMPT TOKENS ]  -->  COMPUTED ONCE", f_step1, anchor="mm", fill=WHITE)
            
            # Step 2: KV Cache
            ss.rrect([540 - 380, kv_y + 160, 540 + 380, kv_y + 250], radius=16, fill=(34, 24, 60), outline=PURPLE, width=2)
            f_step2 = ss.font(FONT_PATH, 32)
            ss.text((540, kv_y + 190), "KEY & VALUE VECTORS LOCKED IN GPU CACHE", f_step2, anchor="mm", fill=YELLOW)
            f_substep = ss.font(FONT_PATH, 26)
            ss.text((540, kv_y + 225), "Zero recomputation of past words", f_substep, anchor="mm", fill=DIM)
            
            # Step 3: Result
            ss.rrect([540 - 380, kv_y + 290, 540 + 380, kv_y + 360], radius=16, fill=(18, 42, 30), outline=GREEN, width=2)
            f_step3 = ss.font(FONT_PATH, 34)
            ss.text((540, kv_y + 325), "NEW TOKEN OUTPUT: INSTANT STREAMING (40 ms)", f_step3, anchor="mm", fill=GREEN)
            
            # Fact card
            f_y = 960
            ss.rrect([540 - 440, f_y, 540 + 440, f_y + 220], radius=32, fill=(20, 18, 40), outline=PURPLE, width=2)
            f_f1 = ss.font(FONT_PATH, 36)
            ss.text((540, f_y + 60), "❌ NOT STORED IN A DATABASE", f_f1, anchor="mm", fill=WHITE)
            f_f2 = ss.font(FONT_PATH, 42)
            ss.text((540, f_y + 140), "⚡ CALCULATED LIVE IN SILICON!", f_f2, anchor="mm", fill=GREEN)
            
        else:  # Outro card (Brand Lock)
            p = pulse(local_t - 5.2, at=0.8, amount=0.06, dur=0.4)
            r = 130
            ss.ellipse([540 - r, 460 - r, 540 + r, 460 + r], outline=PURPLE, width=18)
            f_txk = ss.font(FONT_PATH, 76)
            ss.text((540, 460), "TXK", f_txk, anchor="mm", fill=WHITE)
            
            f_name = ss.font(FONT_PATH, 130)
            ss.text((540, 720), "TechXKenil", f_name, anchor="mm", fill=WHITE)
            f_tag = ss.font(FONT_PATH, 48)
            ss.text((540, 840), "AI  •  TECH  •  CODE", f_tag, anchor="mm", fill=CYAN)
            
            # Subscribe button with gentle pulse
            bw, bh = int(640 * p), int(170 * p)
            by = 1040
            ss.rrect([540 - bw/2, by - bh/2, 540 + bw/2, by + bh/2], radius=50, fill=SUB_RED)
            f_sub = ss.font(FONT_PATH, int(72 * p))
            ss.text((540, by), "SUBSCRIBE", f_sub, anchor="mm", fill=WHITE)
            
    # Subtitles
    draw_captions(ss, t)
    
    layer = ss.out()
    frame = base_bg.copy()
    frame.paste(layer, (0, 0), layer)
    return finish(frame, int(t * FPS), grain=1.5, vignette=0.12)

def main():
    total_duration = meta["total_duration"]
    total_frames = int(total_duration * FPS)
    print(f"Rendering 30s Short: {output_mp4}")
    print(f"Total Duration: {total_duration:.2f}s, Total Frames: {total_frames} @ {FPS} fps")
    
    enc = open_encoder(output_mp4, W, H, FPS, audio=audio_file, crf=14, preset="medium")
    
    start_wall = time.time()
    for frame_idx in range(total_frames):
        t = frame_idx / FPS
        img = render_content_layer(t)
        enc.stdin.write(img.tobytes())
        
        if (frame_idx + 1) % 90 == 0 or frame_idx == total_frames - 1:
            elapsed = time.time() - start_wall
            fps_render = (frame_idx + 1) / max(0.1, elapsed)
            percent = (frame_idx + 1) / total_frames * 100
            print(f"  Frame {frame_idx + 1}/{total_frames} ({percent:.1f}%) - {fps_render:.1f} fps - Elapsed: {elapsed:.1f}s")
            
    enc.stdin.close()
    enc.wait()
    print(f"\nRender complete! Output saved to: {output_mp4}")

if __name__ == "__main__":
    main()

