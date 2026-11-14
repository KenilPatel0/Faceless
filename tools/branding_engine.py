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
    render_brand_card, render_outro_card,
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
    """Renders one high-fidelity frame of the Master Intro Card (Exact stop_paying_for_ai_local_llms design)."""
    channel_name = channel_cfg.get("channel_name", "TechXKenil")
    badge = channel_cfg.get("badge", "TXK")
    tagline = channel_cfg.get("tagline", "AI • TECH • CODE")

    render_brand_card(canvas, channel_name, tagline, badge, rel_t, logo_img=logo_img)
    p_scene = rel_t / max(0.001, dur)
    return canvas.slice_frame(p_scene, drift_amp=4.0)


def render_master_outro_frame(
    canvas: OverscanCanvas,
    rel_t: float,
    dur: float,
    channel_cfg: Dict[str, Any],
    logo_img: Optional[Image.Image] = None,
    click_time: float = 3.8
) -> Image.Image:
    """Renders one high-fidelity frame of the Master Outro conversion sequence (Exact stop_paying_for_ai_local_llms design)."""
    channel_name = channel_cfg.get("channel_name", "TechXKenil")
    tagline = channel_cfg.get("tagline", "AI • TECH • CODE")

    render_outro_card(canvas, channel_name, tagline, rel_t, duration=dur, logo_img=logo_img, click_time=click_time)
    p_scene = rel_t / max(0.001, dur)
    return canvas.slice_frame(p_scene, drift_amp=4.0)


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
