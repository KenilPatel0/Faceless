#!/usr/bin/env python3
"""
branding_engine.py — High-Production Master Intro & Outro Studio for Faceless.
Renders consistent, reusable, broadcast-grade Intro and Outro video clips:
- Intro: Concentric glowing energy rings, spring physics logo badge, Inter Display typography, sub-bass riser, whoosh & lock chime.
- Outro: End-Screen safe layout, Bezier-curved cursor glide, tactile click, golden shockwave ripple, conversion to '✓ SUBSCRIBED!', and success chime.
- Formats: 1080p Horizontal, 4K UHD Horizontal, 1080p Vertical Shorts.
- Audio: Kokoro v1.0 ONNX speech synthesis, procedural SFX, dynamic sidechain ducking, mastered to -16.0 LUFS.
"""

import os
import sys
import math
import json
import shutil
import tempfile
import numpy as np
import soundfile as sf
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from tools.channel_config import get_channel_config
from tools.render_core import (
    OverscanCanvas, ResolutionProfile, PROFILES,
    draw_cursor, bezier_point, spring, get_font,
    CYAN, PURPLE, WHITE, GREEN, RED, YELLOW, DIM, SUB_RED, SUB_GREEN
)
from tools.video_pipeline import StreamingVideoPipeline
from tools.audio_director import KokoroTTSAdapter, SpeechRequest, AudioMixer, AudioCue
from tools.sound_engine import generate_sfx, generate_ambient_synth

BRANDING_DIR = os.path.join(REPO_ROOT, "media", "branding")


# ==============================================================================
# 1. AUDIO SYNTHESIS & MASTERING
# ==============================================================================
def generate_intro_audio(
    channel_cfg: Dict[str, Any],
    duration: float = 4.0,
    is_short: bool = False,
    output_wav: str = ""
) -> float:
    """Generates broadcast mastered audio for the Intro card."""
    channel_name = channel_cfg.get("channel_name", "TechXKenil")
    tts = KokoroTTSAdapter()
    mixer_target = -10.0 if is_short else -13.0
    mixer = AudioMixer(target_lufs=mixer_target, sample_rate=48000)

    # 1. TTS Narration
    if is_short:
        spoken_text = f"{channel_name}. Quick breakdown."
    else:
        spoken_text = f"Welcome to {channel_name}. Practical engineering deep dives."

    with tempfile.TemporaryDirectory() as tmp_dir:
        raw_speech = os.path.join(tmp_dir, "speech_raw.wav")
        res = tts.synthesize(SpeechRequest(text=spoken_text, speed=1.1), raw_speech)

        # 2. SFX Cues (Restrained gain for shorts to preserve speech headroom)
        whoosh_gain = -14.0 if is_short else -9.0
        chime_gain = -12.0 if is_short else -8.0
        cues = [
            AudioCue(cue_id="intro_whoosh", cue_type="whoosh", time_s=0.15, gain_db=whoosh_gain, reason="Scene entry sweep"),
            AudioCue(cue_id="intro_chime", cue_type="chime", time_s=0.85, gain_db=chime_gain, reason="Logo ring lock")
        ]

        # 3. 5-Stem Mix with sidechain ducking & -16 LUFS normalization
        mixer.mix_stems(
            voice_wav_path=raw_speech,
            output_master_path=output_wav,
            cues=cues,
            include_music=True,
            ducking_db=6.0
        )

    # Adjust master audio length to match target duration if needed
    data, sr = sf.read(output_wav, dtype="float32")
    target_samples = int(duration * sr)
    if len(data) < target_samples:
        pad = np.zeros(target_samples - len(data), dtype=np.float32)
        data = np.concatenate([data, pad])
        sf.write(output_wav, data, sr)
    elif len(data) > target_samples:
        data = data[:target_samples]
        # Smooth fade out over last 0.2s
        fade_len = int(0.2 * sr)
        fade = np.linspace(1.0, 0.0, fade_len, dtype=np.float32)
        data[-fade_len:] *= fade
        sf.write(output_wav, data, sr)

    return duration


def generate_outro_audio(
    channel_cfg: Dict[str, Any],
    duration: float = 7.0,
    is_short: bool = False,
    click_time: float = 2.2,
    output_wav: str = ""
) -> float:
    """Generates broadcast mastered audio for the Outro conversion sequence."""
    channel_name = channel_cfg.get("channel_name", "TechXKenil")
    tts = KokoroTTSAdapter()
    mixer_target = -10.0 if is_short else -13.0
    mixer = AudioMixer(target_lufs=mixer_target, sample_rate=48000)

    # 1. TTS Narration
    if is_short:
        spoken_text = f"Subscribe to {channel_name} for more engineering breakdowns."
    else:
        spoken_text = f"If you found this valuable, subscribe to {channel_name}, and I will see you in the next one."

    with tempfile.TemporaryDirectory() as tmp_dir:
        raw_speech = os.path.join(tmp_dir, "outro_speech_raw.wav")
        res = tts.synthesize(SpeechRequest(text=spoken_text, speed=1.1), raw_speech)

        # 2. SFX Cues (Whoosh entry, tactile click, success chime)
        cues = [
            AudioCue(cue_id="outro_whoosh", cue_type="whoosh", time_s=0.1, gain_db=-8.0, reason="Outro sweep"),
            AudioCue(cue_id="outro_click", cue_type="tick", time_s=click_time, gain_db=-4.0, reason="Subscribe mouse click"),
            AudioCue(cue_id="outro_chime", cue_type="chime", time_s=click_time + 0.15, gain_db=-6.0, reason="Subscribed success chime")
        ]

        # 3. 5-Stem Mix with sidechain ducking & -16 LUFS normalization
        mixer.mix_stems(
            voice_wav_path=raw_speech,
            output_master_path=output_wav,
            cues=cues,
            include_music=True,
            ducking_db=6.0
        )

    # Adjust master audio length to match target duration
    data, sr = sf.read(output_wav, dtype="float32")
    target_samples = int(duration * sr)
    if len(data) < target_samples:
        pad = np.zeros(target_samples - len(data), dtype=np.float32)
        data = np.concatenate([data, pad])
        sf.write(output_wav, data, sr)
    elif len(data) > target_samples:
        data = data[:target_samples]
        fade_len = int(0.25 * sr)
        fade = np.linspace(1.0, 0.0, fade_len, dtype=np.float32)
        data[-fade_len:] *= fade
        sf.write(output_wav, data, sr)

    return duration


# ==============================================================================
# 2. PROCEDURAL FRAME RENDERING
# ==============================================================================
def render_master_intro_frame(
    canvas: OverscanCanvas,
    rel_t: float,
    dur: float,
    channel_cfg: Dict[str, Any],
    logo_img: Optional[Image.Image] = None
) -> Image.Image:
    """Renders one high-fidelity frame of the Intro Card."""
    cx = canvas.W // 2
    cy = int(canvas.H * 0.44) if canvas.profile.is_vertical else (canvas.H // 2 - 15)
    sc = canvas.scale

    channel_name = channel_cfg.get("channel_name", "TechXKenil").upper()
    badge = channel_cfg.get("badge", "TXK").upper()
    tagline = channel_cfg.get("tagline", "AI • TECH • CODE").upper()

    # Damped spring entry for center card
    p_spring = min(1.0, spring(rel_t * 1.8))
    card_w = min(480, int(canvas.W * 0.44))
    card_h = 270 if not canvas.profile.is_vertical else 320

    # 1. Outer Concentric Energy Rings
    rot_deg = rel_t * 60.0
    ring_r = int(145 * sc * p_spring)
    ring_cx, ring_cy = canvas.to_canvas(cx, cy - (85 if not canvas.profile.is_vertical else 105))

    # Ambient Glow
    glow_box = [ring_cx - ring_r - 20, ring_cy - ring_r - 20, ring_cx + ring_r + 20, ring_cy + ring_r + 20]
    canvas.draw.ellipse(glow_box, outline=(70, 220, 255, 60), width=int(4 * sc))

    # Cyan Outer Ring Arc
    canvas.draw.arc(
        [ring_cx - ring_r, ring_cy - ring_r, ring_cx + ring_r, ring_cy + ring_r],
        start=rot_deg, end=rot_deg + 240,
        fill=CYAN, width=max(2, int(3 * sc))
    )
    # Purple Inner Ring Arc (counter-rotating)
    inner_r = int(ring_r * 0.82)
    canvas.draw.arc(
        [ring_cx - inner_r, ring_cy - inner_r, ring_cx + inner_r, ring_cy + inner_r],
        start=-rot_deg * 1.4, end=-rot_deg * 1.4 + 210,
        fill=PURPLE, width=max(2, int(2.5 * sc))
    )

    # 2. Main Frosted Obsidian Card
    bx0, by0 = cx - int(card_w * p_spring), cy - int(card_h * p_spring)
    bx1, by1 = cx + int(card_w * p_spring), cy + int(card_h * p_spring)
    canvas.draw_card(
        (bx0, by0, bx1, by1),
        radius=int(28 * sc),
        fill=(14, 18, 32),
        outline=(70, 220, 255, 140),
        width=max(1, int(2 * sc))
    )

    # 3. Logo or Badge
    if logo_img:
        logo_sz = int(170 * sc * p_spring)
        if logo_sz > 10:
            resized_logo = logo_img.resize((logo_sz, logo_sz), Image.Resampling.LANCZOS)
            lx, ly = canvas.to_canvas(cx - int(85 * p_spring), cy - (170 if not canvas.profile.is_vertical else 190))
            canvas.frame.paste(resized_logo, (int(lx), int(ly)), resized_logo)
    else:
        badge_y = cy - (90 if not canvas.profile.is_vertical else 110)
        canvas.draw_pill(
            (cx - 65, badge_y),
            badge,
            size=int(32 * sc),
            text_color=CYAN,
            bg_color=(22, 28, 48),
            outline_color=CYAN
        )

    # 4. Channel Name & Tagline
    text_alpha = min(1.0, max(0.0, (rel_t - 0.2) / 0.5))
    name_y = cy + (75 if not canvas.profile.is_vertical else 70)
    canvas.draw_text(
        (cx, name_y),
        channel_name,
        size=int(46 * sc),
        fill=(255, 255, 255),
        anchor="mm"
    )

    tagline_y = name_y + int(50 * sc)
    canvas.draw_text(
        (cx, tagline_y),
        f"♦  {tagline}  ♦",
        size=int(20 * sc),
        fill=CYAN,
        anchor="mm"
    )

    # 5. Quality Badge Pill
    quality_text = "PRACTICAL TECH EXPLAINERS • 4K UHD" if not canvas.profile.is_vertical else "ENGINEERING SHORTS"
    pill_y = tagline_y + int(48 * sc)
    canvas.draw_pill(
        (cx - int(160 * sc), pill_y),
        quality_text,
        size=int(14 * sc),
        text_color=(190, 200, 235),
        bg_color=(18, 22, 38),
        outline_color=(70, 220, 255, 100)
    )

    # Slice frame with continuous camera drift push-in
    p_scene = rel_t / dur
    return canvas.slice_frame(p_scene, drift_amp=6.0)


def render_master_outro_frame(
    canvas: OverscanCanvas,
    rel_t: float,
    dur: float,
    channel_cfg: Dict[str, Any],
    logo_img: Optional[Image.Image] = None,
    click_time: float = 2.2
) -> Image.Image:
    """Renders one high-fidelity frame of the Outro conversion sequence."""
    cx = canvas.W // 2
    cy = int(canvas.H * 0.44) if canvas.profile.is_vertical else (canvas.H // 2 - 15)
    sc = canvas.scale

    channel_name = channel_cfg.get("channel_name", "TechXKenil").upper()
    badge = channel_cfg.get("badge", "TXK").upper()
    tagline = channel_cfg.get("tagline", "AI • TECH • CODE").upper()

    # 1. YouTube End Screen Safe Boxes (Horizontal 16:9 only)
    if not canvas.profile.is_vertical:
        box_w, box_h = int(380 * sc), int(214 * sc)
        # Left End Card Safe Zone (Recommended Video)
        lx0, ly0 = int(120 * sc), cy - box_h // 2
        canvas.draw_card((lx0, ly0, lx0 + box_w, ly0 + box_h), radius=int(18 * sc), fill=(14, 18, 30), outline=(70, 220, 255, 70), width=int(1.5 * sc))
        canvas.draw_text((lx0 + box_w // 2, ly0 + box_h // 2 - 15), "▶  RECOMMENDED VIDEO", size=int(17 * sc), fill=CYAN, anchor="mm")
        canvas.draw_text((lx0 + box_w // 2, ly0 + box_h // 2 + 18), "(YouTube End Screen Safe Zone)", size=int(12 * sc), fill=DIM, anchor="mm")

        # Right End Card Safe Zone (Playlist)
        rx0, ry0 = canvas.W - int(120 * sc) - box_w, cy - box_h // 2
        canvas.draw_card((rx0, ry0, rx0 + box_w, ry0 + box_h), radius=int(18 * sc), fill=(14, 18, 30), outline=(150, 110, 255, 70), width=int(1.5 * sc))
        canvas.draw_text((rx0 + box_w // 2, ry0 + box_h // 2 - 15), "📋  BEST PLAYLIST", size=int(17 * sc), fill=PURPLE, anchor="mm")
        canvas.draw_text((rx0 + box_w // 2, ry0 + box_h // 2 + 18), "(YouTube End Screen Safe Zone)", size=int(12 * sc), fill=DIM, anchor="mm")

    # 2. Center Hero Conversion Card
    card_w = min(460, int(canvas.W * 0.42))
    card_h = 280 if not canvas.profile.is_vertical else 330
    is_clicked = rel_t >= click_time

    border_col = (35, 195, 110, 180) if is_clicked else (255, 70, 90, 140)
    canvas.draw_card(
        (cx - card_w, cy - card_h, cx + card_w, cy + card_h),
        radius=int(28 * sc),
        fill=(14, 18, 32),
        outline=border_col,
        width=max(1, int(2 * sc))
    )

    # Logo / Badge at top
    if logo_img:
        logo_sz = int(130 * sc)
        resized_logo = logo_img.resize((logo_sz, logo_sz), Image.Resampling.LANCZOS)
        lx, ly = canvas.to_canvas(cx - int(65 * sc), cy - (190 if not canvas.profile.is_vertical else 220))
        canvas.frame.paste(resized_logo, (int(lx), int(ly)), resized_logo)
    else:
        badge_y = cy - (120 if not canvas.profile.is_vertical else 140)
        canvas.draw_pill((cx - 50, badge_y), badge, size=int(26 * sc), text_color=WHITE, bg_color=(24, 32, 54), outline_color=(70, 220, 255))

    # Channel Name & Tagline
    canvas.draw_text((cx, cy - (30 if not canvas.profile.is_vertical else 40)), channel_name, size=int(40 * sc), fill=WHITE, anchor="mm")
    canvas.draw_text((cx, cy + (15 if not canvas.profile.is_vertical else 10)), f"♦ {tagline} ♦", size=int(18 * sc), fill=DIM, anchor="mm")

    # 3. Conversion Subscribe Button Animation
    btn_col = (35, 195, 110) if is_clicked else (255, 30, 50)
    btn_txt = "✓ SUBSCRIBED!" if is_clicked else "SUBSCRIBE"

    # Pulse scale on click (t_click -> t_click + 0.35s)
    click_pulse = 1.0
    if 0 <= (rel_t - click_time) < 0.35:
        click_pulse = 1.0 - 0.10 * math.sin(math.pi * (rel_t - click_time) / 0.35)

    bw = int(185 * sc * click_pulse)
    bh = int(36 * sc)
    btn_y = cy + (100 if not canvas.profile.is_vertical else 115)

    canvas.draw_card(
        (cx - bw, btn_y - bh, cx + bw, btn_y + bh),
        radius=int(24 * sc),
        fill=btn_col,
        outline=(255, 255, 255, 200),
        width=max(1, int(2 * sc))
    )
    canvas.draw_text(
        (cx, btn_y),
        btn_txt,
        size=int(24 * sc),
        fill=WHITE,
        anchor="mm"
    )

    # 4. Expanding Golden Shockwave Ripple Ring
    if is_clicked and (rel_t - click_time) < 1.0:
        rip_p = (rel_t - click_time) / 1.0
        rip_r = int(120 * sc * rip_p)
        rx, ry = canvas.to_canvas(cx, btn_y)
        alpha = int(255 * (1.0 - rip_p))
        canvas.draw.ellipse(
            [rx - rip_r, ry - rip_r, rx + rip_r, ry + rip_r],
            outline=(255, 205, 70, alpha),
            width=max(2, int(4 * sc))
        )

    # 5. Golden Notification Bell Badge (Appears when subscribed)
    if is_clicked:
        bell_x = cx + bw + int(36 * sc)
        canvas.draw_pill(
            (bell_x - int(20 * sc), btn_y - int(18 * sc)),
            "🔔",
            size=int(18 * sc),
            text_color=YELLOW,
            bg_color=(28, 34, 56),
            outline_color=YELLOW
        )

    # 6. Smooth Bezier Mouse Cursor Glide
    p0 = (canvas.W - int(120 * sc), canvas.H - int(100 * sc))
    p1 = (cx + int(90 * sc), btn_y + int(120 * sc))
    p2 = (cx + int(10 * sc), btn_y + int(10 * sc))
    p_cur = min(1.0, rel_t / click_time)
    
    # After click, cursor gently drifts away to bottom right
    if rel_t > click_time:
        drift_p = min(1.0, (rel_t - click_time) / (dur - click_time))
        cur_x, cur_y = bezier_point(p2, (cx + int(150 * sc), btn_y + int(80 * sc)), (canvas.W - int(140 * sc), canvas.H - int(110 * sc)), drift_p)
    else:
        cur_x, cur_y = bezier_point(p0, p1, p2, p_cur)

    cx_draw, cy_draw = canvas.to_canvas(cur_x, cur_y)
    draw_cursor(canvas.draw, (cx_draw, cy_draw), scale=canvas.scale)

    # Slice frame with continuous camera drift push-in
    p_scene = rel_t / dur
    return canvas.slice_frame(p_scene, drift_amp=6.0)


# ==============================================================================
# 3. BATCH CLIP GENERATOR & MASTER SUITE BUILDER
# ==============================================================================
def render_branding_clip(
    clip_type: str,            # "intro" or "outro"
    profile_key: str,          # "1080p30", "4k60", "1080p30_vert"
    output_mp4: str,
    channel_cfg: Dict[str, Any]
) -> Dict[str, Any]:
    """Renders a single standalone master intro or outro clip."""
    profile = PROFILES[profile_key]
    is_short = profile.is_vertical

    # Determine duration & click timing
    if clip_type == "intro":
        duration = 2.2 if is_short else 4.0
        click_time = 0.0
    else:
        duration = 3.8 if is_short else 7.0
        click_time = 1.0 if is_short else 2.2

    # Load Logo
    logo_path = channel_cfg.get("logo_path")
    logo_img = None
    if logo_path and os.path.exists(logo_path):
        try:
            logo_img = Image.open(logo_path).convert("RGBA")
        except Exception:
            logo_img = None
    elif os.path.exists("media/txk_logo.png"):
        try:
            logo_img = Image.open("media/txk_logo.png").convert("RGBA")
        except Exception:
            logo_img = None

    # 1. Synthesize and master audio
    os.makedirs(os.path.dirname(output_mp4), exist_ok=True)
    temp_wav = output_mp4 + ".audio.wav"
    if clip_type == "intro":
        generate_intro_audio(channel_cfg, duration=duration, is_short=is_short, output_wav=temp_wav)
    else:
        generate_outro_audio(channel_cfg, duration=duration, is_short=is_short, click_time=click_time, output_wav=temp_wav)

    # 2. Encode video frames
    total_frames = int(round(duration * profile.fps))
    print(f"🎬 Rendering {clip_type.upper()} ({profile_key}): {total_frames} frames ({duration}s @ {profile.fps}fps)...")

    pipeline = StreamingVideoPipeline(
        output_path=output_mp4,
        width=profile.width,
        height=profile.height,
        fps=profile.fps,
        audio_path=temp_wav,
        total_frames=total_frames
    )

    canvas = OverscanCanvas(profile)
    poster_frame = None

    with pipeline:
        for f_idx in range(total_frames):
            rel_t = f_idx / float(profile.fps)
            canvas.reset()

            if clip_type == "intro":
                frame_img = render_master_intro_frame(canvas, rel_t, duration, channel_cfg, logo_img)
            else:
                frame_img = render_master_outro_frame(canvas, rel_t, duration, channel_cfg, logo_img, click_time=click_time)

            pipeline.write_frame(frame_img)
            if f_idx == int(total_frames * 0.45):
                poster_frame = frame_img

    if os.path.exists(temp_wav):
        os.remove(temp_wav)

    print(f"  ✓ Saved master clip: {output_mp4}")
    return {
        "clip_type": clip_type,
        "profile": profile_key,
        "path": output_mp4,
        "duration": duration,
        "fps": profile.fps,
        "resolution": f"{profile.width}x{profile.height}",
        "poster_frame": poster_frame
    }


def build_all_branding_assets(channel_name_or_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Renders and stores the complete consistent branding suite into `media/branding/`:
    - intro_1080p.mp4 (16:9, 1080p30)
    - intro_4k.mp4 (16:9, 4k60)
    - intro_short.mp4 (9:16, 1080p30)
    - outro_1080p.mp4 (16:9, 1080p30)
    - outro_4k.mp4 (16:9, 4k60)
    - outro_short.mp4 (9:16, 1080p30)
    - Previews: intro_preview.jpg, outro_preview.jpg
    - Manifest: branding_manifest.json
    """
    cfg = get_channel_config(channel_name_or_path=channel_name_or_path)
    os.makedirs(BRANDING_DIR, exist_ok=True)

    manifest_records = {}

    targets = [
        ("intro", "1080p30", "intro_1080p.mp4"),
        ("intro", "4k60", "intro_4k.mp4"),
        ("intro", "1080p30_vert", "intro_short.mp4"),
        ("outro", "1080p30", "outro_1080p.mp4"),
        ("outro", "4k60", "outro_4k.mp4"),
        ("outro", "1080p30_vert", "outro_short.mp4"),
    ]

    intro_poster = None
    outro_poster = None

    for ctype, prof, filename in targets:
        out_file = os.path.join(BRANDING_DIR, filename)
        info = render_branding_clip(ctype, prof, out_file, cfg)
        manifest_records[f"{ctype}_{prof}"] = {
            "path": out_file,
            "duration": info["duration"],
            "resolution": info["resolution"],
            "fps": info["fps"]
        }
        if ctype == "intro" and prof == "1080p30":
            intro_poster = info["poster_frame"]
        elif ctype == "outro" and prof == "1080p30":
            outro_poster = info["poster_frame"]

    # Save Previews
    if intro_poster:
        p_intro = os.path.join(BRANDING_DIR, "intro_preview.jpg")
        intro_poster.save(p_intro, quality=95)
        print(f"✓ Saved intro preview: {p_intro}")
    if outro_poster:
        p_outro = os.path.join(BRANDING_DIR, "outro_preview.jpg")
        outro_poster.save(p_outro, quality=95)
        print(f"✓ Saved outro preview: {p_outro}")

    # Write Manifest
    manifest_path = os.path.join(BRANDING_DIR, "branding_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({
            "channel": cfg.get("channel_name"),
            "badge": cfg.get("badge"),
            "tagline": cfg.get("tagline"),
            "assets": manifest_records
        }, f, indent=2)

    print(f"\n🎉 CONSISTENT BRANDING SUITE BUILT & SAVED: {manifest_path}")
    return manifest_records


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Master Intro & Outro Studio")
    parser.add_argument("--channel", help="Channel name or path to profile JSON")
    args = parser.parse_args()

    build_all_branding_assets(channel_name_or_path=args.channel)
