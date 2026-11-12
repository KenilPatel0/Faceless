import os, sys, json, math, time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
TOOLS_DIR = os.path.join(REPO_ROOT, "python", "tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from motion import SS, spring, count_up, word_pop, pulse, drift, finish, open_encoder
from humanize import word_timings, push_in, ease_out_expo, ease_out_quart, clamp, draw_cursor, arc_point, typed

W, H, FPS = 1080, 1920, 30
FONT_PATH = os.path.join(REPO_ROOT, "fonts", "InterDisplay-Bold.otf")
CAPTION_FONT_PATH = os.path.join(REPO_ROOT, "fonts", "BebasNeue-Regular.ttf")

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

meta = json.load(open(os.path.join(SCRIPT_DIR, "meta_15s.json")))
audio_file = os.path.join(SCRIPT_DIR, "audio_15s.wav")
output_mp4 = os.path.join(SCRIPT_DIR, "github_to_antigravity_15s.mp4")

# Load Real App captures
CARD_W, CARD_H = 960, 600

# Create smooth rounded-corner mask for card images
card_mask = Image.new("L", (CARD_W * 2, CARD_H * 2), 0)
d_mask = ImageDraw.Draw(card_mask)
d_mask.rounded_rectangle([0, 0, CARD_W * 2, CARD_H * 2], radius=36, fill=255)
card_mask = card_mask.resize((CARD_W, CARD_H), Image.LANCZOS)

real_github_raw = Image.open(os.path.join(SCRIPT_DIR, "real_github.png")).convert("RGB")
real_antigravity_raw = Image.open(os.path.join(SCRIPT_DIR, "real_antigravity.png")).convert("RGB")

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

def render_frame_content(t):
    ss = SS((W, H), S=2)
    
    # Identify active scene
    sc_idx = 0
    for idx, sc in enumerate(meta["scenes"]):
        if sc["start"] <= t <= sc["end"]:
            sc_idx = idx
            break
    sc = meta["scenes"][sc_idx]
    local_t = t - sc["start"]
    dur = sc["dur"]
    
    card_x = (W - CARD_W) // 2
    card_y = 520
    
    # Active app image to paste
    active_app_img = None
    
    # Cursor variables
    cursor_pos = None
    cursor_click_p = 0.0
    
    if sc_idx == 0:  # Scene 1: Real GitHub Repo with Cursor & Dynamic Zoom
        draw_brand_tag(ss)
        
        # Pill badge
        f_pill = ss.font(FONT_PATH, 32)
        ss.rrect([540 - 260, 240, 540 + 260, 296], radius=28, fill=(18, 28, 54), outline=CYAN, width=2)
        ss.text((540, 268), "REAL APP // LIVE GITHUB REPO", f_pill, anchor="mm", fill=CYAN)
        
        # Headline
        f_head1 = ss.font(FONT_PATH, 70)
        f_head2 = ss.font(FONT_PATH, 36)
        ss.text((540, 360), "FOUND A REPO ON GITHUB?", f_head1, anchor="mm", fill=WHITE)
        ss.text((540, 420), "DON'T SPEND HOURS INSTALLING MANUALLY", f_head2, anchor="mm", fill=YELLOW)
        
        # Dynamic Camera Zoom & Scroll on GitHub UI (simulates zooming in on Clone button)
        p_cam = clamp(local_t / dur)
        zoom = 1.0 + 0.12 * ease_out_quart(p_cam)
        gw, gh = real_github_raw.size
        cw, ch = int(gw / zoom), int(gh / zoom)
        crop_x = int((gw - cw) * 0.6)  # bias towards right (Code button)
        crop_y = int((gh - ch) * 0.2)  # top header
        gh_cropped = real_github_raw.crop((crop_x, crop_y, crop_x + cw, crop_y + ch))
        gh_card = gh_cropped.resize((CARD_W, CARD_H), Image.LANCZOS).convert("RGBA")
        gh_card.putalpha(card_mask)
        active_app_img = gh_card
        
        # Card outer glowing outline
        ss.rrect([card_x - 6, card_y - 6, card_x + CARD_W + 6, card_y + CARD_H + 6], radius=24, outline=CYAN, width=4)
        
        # Cursor Animation on GitHub:
        # Cursor flies toward the green Code / Clone button at (card_x + 750, card_y + 190)
        target_pt = (card_x + 750, card_y + 190)
        start_pt = (card_x + 200, card_y + 520)
        
        if local_t >= 0.4:
            u_move = clamp((local_t - 0.4) / 1.2)
            cur_pos = arc_point(start_pt, target_pt, ease_out_quart(u_move), bend=0.22)
            cursor_pos = (int(cur_pos[0]), int(cur_pos[1]))
            
            # Click at t = 1.7s
            if local_t >= 1.7:
                cursor_click_p = clamp((local_t - 1.7) / 0.4)
                
            # Floating toast notification popping up after click
            if local_t >= 1.9:
                s_toast = spring(local_t - 1.9, freq=2.4, zeta=0.7)
                tx, ty = target_pt[0] - 120, target_pt[1] + 60
                tw, th = int(320 * s_toast), int(54 * s_toast)
                ss.rrect([tx - tw//2, ty - th//2, tx + tw//2, ty + th//2], radius=16, fill=(18, 48, 32), outline=GREEN, width=2)
                f_tst = ss.font(FONT_PATH, max(1, int(24 * s_toast)))
                ss.text((tx, ty), "✓ Copied Repo URL!", f_tst, anchor="mm", fill=GREEN)
                
        # Pill under card
        f_sub = ss.font(FONT_PATH, 34)
        ss.rrect([540 - 320, 1200, 540 + 320, 1270], radius=24, fill=(36, 16, 26), outline=RED, width=2)
        ss.text((540, 1235), "❌ NO MORE MANUAL DEPENDENCY ERRORS", f_sub, anchor="mm", fill=RED)
        
    elif sc_idx == 1:  # Scene 2: Real Antigravity IDE with Agent Execution & Typing
        draw_brand_tag(ss)
        
        # Pill badge
        f_pill = ss.font(FONT_PATH, 32)
        ss.rrect([540 - 280, 240, 540 + 280, 296], radius=28, fill=(24, 20, 52), outline=PURPLE, width=2)
        ss.text((540, 268), "REAL APP // ANTIGRAVITY AGENT IDE", f_pill, anchor="mm", fill=PURPLE)
        
        # Headline
        f_head1 = ss.font(FONT_PATH, 68)
        f_head2 = ss.font(FONT_PATH, 36)
        ss.text((540, 360), "PASTE IT INTO ANTIGRAVITY", f_head1, anchor="mm", fill=CYAN)
        ss.text((540, 420), "AI AGENT CLONES & RUNS EVERYTHING", f_head2, anchor="mm", fill=WHITE)
        
        # Camera push in on Antigravity
        p_cam = clamp(local_t / dur)
        zoom = 1.0 + 0.08 * ease_out_quart(p_cam)
        aw, ah = real_antigravity_raw.size
        cw, ch = int(aw / zoom), int(ah / zoom)
        crop_x = int((aw - cw) * 0.7)  # bias towards right (Agent pane)
        crop_y = int((ah - ch) * 0.3)
        ag_cropped = real_antigravity_raw.crop((crop_x, crop_y, crop_x + cw, crop_y + ch))
        ag_card = ag_cropped.resize((CARD_W, CARD_H), Image.LANCZOS).convert("RGBA")
        ag_card.putalpha(card_mask)
        active_app_img = ag_card
        
        # Card outer glowing outline
        ss.rrect([card_x - 6, card_y - 6, card_x + CARD_W + 6, card_y + CARD_H + 6], radius=24, outline=PURPLE, width=4)
        
        # Animated cursor moving to Antigravity Agent Pane
        agent_input_pt = (card_x + 680, card_y + 190)
        ag_start_pt = (card_x + 100, card_y + 100)
        
        if local_t >= 0.3:
            u_move = clamp((local_t - 0.3) / 1.0)
            cur_pos = arc_point(ag_start_pt, agent_input_pt, ease_out_quart(u_move), bend=-0.2)
            cursor_pos = (int(cur_pos[0]), int(cur_pos[1]))
            if local_t >= 1.3:
                cursor_click_p = clamp((local_t - 1.3) / 0.4)
                
        # Dynamic execution progress badges popping in over bottom
        badges = [
            ("1. Clone Repo", "✓ Cloned in 1.4s", 2.2, GREEN),
            ("2. Python Venv", "✓ Virtualenv Ready", 3.6, GREEN),
            ("3. Dependencies", "✓ 6 Packages Installed", 5.0, GREEN),
        ]
        
        f_b1 = ss.font(FONT_PATH, 26)
        f_b2 = ss.font(FONT_PATH, 24)
        for idx, (title_b, status_b, reveal_t, col_b) in enumerate(badges):
            if local_t >= reveal_t:
                s_b = spring(local_t - reveal_t, freq=2.6, zeta=0.7)
                bx = 540 - 320 + idx * 320
                by = 1235
                bw, bh = int(300 * s_b), int(64 * s_b)
                ss.rrect([bx - bw//2, by - bh//2, bx + bw//2, by + bh//2], radius=16, fill=(18, 32, 48), outline=col_b, width=2)
                ss.text((bx, by - 10), title_b, f_b1, anchor="mm", fill=WHITE)
                ss.text((bx, by + 14), status_b, f_b2, anchor="mm", fill=col_b)
                
    elif sc_idx == 2:  # Scene 3: Outro Card with Interactive Cursor Subscribe Click
        p = pulse(local_t, at=0.8, amount=0.06, dur=0.4)
        r = 130
        ss.ellipse([540 - r, 460 - r, 540 + r, 460 + r], outline=PURPLE, width=18)
        f_txk = ss.font(FONT_PATH, 76)
        ss.text((540, 460), "TXK", f_txk, anchor="mm", fill=WHITE)
        
        f_name = ss.font(FONT_PATH, 130)
        ss.text((540, 720), "TechXKenil", f_name, anchor="mm", fill=WHITE)
        f_tag = ss.font(FONT_PATH, 48)
        ss.text((540, 840), "AI  •  TECH  •  CODE", f_tag, anchor="mm", fill=CYAN)
        
        # Subscribe button
        bw, bh = int(640 * p), int(170 * p)
        by = 1040
        
        # Cursor moves to SUBSCRIBE button and clicks!
        sub_pt = (540, by)
        sub_start_pt = (200, 1400)
        
        if local_t >= 0.5:
            u_move = clamp((local_t - 0.5) / 1.3)
            cur_pos = arc_point(sub_start_pt, sub_pt, ease_out_quart(u_move), bend=-0.2)
            cursor_pos = (int(cur_pos[0]), int(cur_pos[1]))
            if local_t >= 1.8:
                cursor_click_p = clamp((local_t - 1.8) / 0.4)
                
        is_clicked = (local_t >= 2.0)
        btn_col = (40, 160, 90) if is_clicked else SUB_RED
        btn_txt = "✓ SUBSCRIBED!" if is_clicked else "SUBSCRIBE"
        
        ss.rrect([540 - bw/2, by - bh/2, 540 + bw/2, by + bh/2], radius=50, fill=btn_col)
        f_sub = ss.font(FONT_PATH, int(68 * p))
        ss.text((540, by), btn_txt, f_sub, anchor="mm", fill=WHITE)
        
    # Draw captions
    draw_captions(ss, t)
    
    # Base frame
    frame = base_bg.copy()
    
    # 1. Composite SS vector overlay over frame
    layer = ss.out()
    frame.paste(layer, (0, 0), layer)
    
    # 2. Paste the active screenshot
    if active_app_img is not None:
        frame.paste(active_app_img, (card_x, card_y), active_app_img)
        
    # 3. Draw animated cursor on the top layer
    if cursor_pos is not None:
        d_cursor = ImageDraw.Draw(frame)
        draw_cursor(d_cursor, cursor_pos, click_p=cursor_click_p)
        
    return finish(frame, int(t * FPS), grain=1.5, vignette=0.12)

def main():
    total_duration = meta["total_duration"]
    total_frames = int(total_duration * FPS)
    print(f"Rendering 15s Animated Real UI Short: {output_mp4}")
    print(f"Total Duration: {total_duration:.2f}s, Total Frames: {total_frames} @ {FPS} fps")
    
    enc = open_encoder(output_mp4, W, H, FPS, audio=audio_file, crf=14, preset="medium")
    
    start_wall = time.time()
    for frame_idx in range(total_frames):
        t = frame_idx / FPS
        img = render_frame_content(t)
        enc.stdin.write(img.tobytes())
        
        if (frame_idx + 1) % 60 == 0 or frame_idx == total_frames - 1:
            elapsed = time.time() - start_wall
            fps_render = (frame_idx + 1) / max(0.1, elapsed)
            percent = (frame_idx + 1) / total_frames * 100
            print(f"  Frame {frame_idx + 1}/{total_frames} ({percent:.1f}%) - {fps_render:.1f} fps - Elapsed: {elapsed:.1f}s")
            
    enc.stdin.close()
    enc.wait()
    print(f"\nRender complete! Output saved to: {output_mp4}")

if __name__ == "__main__":
    main()
