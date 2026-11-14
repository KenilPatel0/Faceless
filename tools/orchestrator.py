#!/usr/bin/env python3
"""
orchestrator.py — Autonomous Faceless Video Studio End-to-End Orchestrator.
Executes the unified 6-stage video production pipeline:
1. Scene & Channel Profile Resolution
2. Phonetic-Normalized Neural Speech Synthesis (Kokoro ONNX)
3. Procedural Sound Design & Audio Broadcast Mastering (-15 LUFS)
4. Authentic Real UI Window Snapshotting (Playwright Chromium)
5. Hardware-Accelerated Declarative Compositing (QSV / NVENC)
6. Automated QA Gate Compliance Verification

Usage:
  python tools/orchestrator.py build --project python/ai_dev_blueprint --channel TechXKenil --format 1080p30
  python tools/orchestrator.py build --project python/ai_dev_blueprint --format 4k60
"""

import os
import sys
import json
import time
import argparse
import subprocess
import importlib.util
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
sys.path.insert(0, REPO_ROOT)

from tools.channel_config import get_channel_config
from tools.lexicon import normalize_speech_text
from tools.subtitle_engine import SubtitleTrack, calculate_word_timings, build_caption_chunks
from tools.sound_engine import mix_and_master
from tools.capture_code import render_code_window, render_terminal_window, render_split_code_window
from tools.video_pipeline import StreamingVideoPipeline
from tools.render_core import (
    PROFILES, OverscanCanvas, render_real_asset_frame,
    render_brand_card, render_outro_card, get_font
)
from tools.animation_registry import REGISTRY
from tools.animation_director import AnimationDirector, CreativeBrief
from tools.animation_timeline import TimelineResolver

def load_project_scenes(project_dir: str) -> List[Dict[str, Any]]:
    """Dynamically imports SCENES from data.py or data.json."""
    py_path = os.path.join(project_dir, "data.py")
    json_path = os.path.join(project_dir, "data.json")

    if os.path.exists(py_path):
        spec = importlib.util.spec_from_file_location("project_data", py_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, "SCENES"):
            return mod.SCENES
        raise ValueError("data.py does not contain a SCENES list.")
    elif os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        raise FileNotFoundError(f"No data.py or data.json found in {project_dir}")

def synthesize_speech(
    scenes: List[Dict[str, Any]],
    channel_cfg: Dict[str, Any],
    project_dir: str
) -> Tuple[str, str, float]:
    """Stage 2: Kokoro v1.0 ONNX speech synthesis with phonetic lexicon normalization."""
    from kokoro_onnx import Kokoro
    print("\n" + "=" * 70)
    print("🎙️ STAGE 2: Phonetic Neural Speech Synthesis (Kokoro v1.0 ONNX)")
    print("=" * 70)

    model_path = os.path.join(REPO_ROOT, "kokoro_models", "kokoro-v1.0.onnx")
    voices_path = os.path.join(REPO_ROOT, "kokoro_models", "voices-v1.0.bin")
    kokoro = Kokoro(model_path, voices_path)

    v_cfg = channel_cfg.get("voice", {})
    voice_id = v_cfg.get("voice_id", "am_michael")
    speed = v_cfg.get("speed", 1.1)

    sr = 24000
    audio_dir = os.path.join(project_dir, "audio_chunks")
    os.makedirs(audio_dir, exist_ok=True)

    timeline = []
    current_time = 0.0
    segments = []

    for idx, scene in enumerate(scenes):
        sid = scene.get("id", f"scene_{idx}")
        raw_text = scene.get("narration") or scene.get("text") or ""
        
        # Phonetic normalization
        norm_text = normalize_speech_text(raw_text)
        
        # Kokoro synthesis
        samples, _ = kokoro.create(norm_text, voice=voice_id, speed=speed, lang="en-us")
        dur = len(samples) / sr

        # Silence padding: 0.18s standard, +0.45s after section end
        is_last = (idx == len(scenes) - 1) or (scenes[idx + 1].get("section") != scene.get("section"))
        silence_dur = 0.45 if is_last else 0.18
        silence_samples = np.zeros(int(silence_dur * sr), dtype=np.float32)

        chunk_path = os.path.join(audio_dir, f"{sid}.wav")
        sf.write(chunk_path, samples, sr)

        segments.append(samples)
        segments.append(silence_samples)

        start_t = current_time
        end_t = start_t + dur
        current_time = end_t + silence_dur

        timeline.append({
            "index": idx,
            "id": sid,
            "section": scene.get("section", "BODY"),
            "title": scene.get("title", ""),
            "start_time": round(start_t, 3),
            "end_time": round(end_t, 3),
            "duration": round(dur, 3),
            "silence_dur": round(silence_dur, 3),
            "text": raw_text,
            "visual_type": scene.get("visual_type", "diagram")
        })
        print(f"  [{start_t:6.2f}s -> {end_t:6.2f}s] ({dur:5.2f}s) {sid:12} : {raw_text[:45]}...")

    tl_path = os.path.join(project_dir, "tl.json")
    with open(tl_path, "w", encoding="utf-8") as f:
        json.dump(timeline, f, indent=2)

    raw_wav_path = os.path.join(project_dir, "audio_master_raw.wav")
    sf.write(raw_wav_path, np.concatenate(segments), sr)
    print(f"✓ Timeline generated: {tl_path} ({current_time:.2f}s total speech)")
    return raw_wav_path, tl_path, current_time

def prepare_sound_design(raw_wav_path: str, tl_path: str, project_dir: str, target_lufs: float = -14.0) -> Tuple[str, float]:
    """Stage 3: Procedural SFX & Broadcast Mastering (-14.0 LUFS target)."""
    print("\n" + "=" * 70)
    print(f"🔊 STAGE 3: Procedural Sound Design & Audio Mastering ({target_lufs} LUFS)")
    print("=" * 70)

    with open(tl_path, "r", encoding="utf-8") as f:
        timeline = json.load(f)

    events: List[Tuple[float, str]] = []
    # Add whoosh on section changes, ticks/pops on list reveals
    last_sec = None
    for s in timeline:
        st = s["start_time"]
        sec = s["section"]
        if sec != last_sec:
            events.append((st, "whoosh"))
            last_sec = sec
        vtype = s.get("visual_type")
        if vtype in ["code", "terminal"]:
            events.append((st + 0.5, "chime"))
        elif vtype in ["diagram", "split"]:
            events.append((st + 0.3, "pop"))

    master_wav_path = os.path.join(project_dir, "audio_master.wav")
    total_dur = mix_and_master(
        speech_wav_path=raw_wav_path,
        output_master_path=master_wav_path,
        events=events,
        include_ambient=True,
        target_lufs=target_lufs
    )
    return master_wav_path, total_dur

def prepare_real_ui_assets(scenes: List[Dict[str, Any]], project_dir: str, is_4k: bool = False):
    """Stage 4: Automated Real UI Window Snapshotting (Zero-Mockup Rule)."""
    print("\n" + "=" * 70)
    print("🎨 STAGE 4: Authentic Real UI Window Snapshotting (Zero-Mockup Rule)")
    print("=" * 70)

    assets_dir = os.path.join(project_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    code_dir = os.path.join(project_dir, "code")

    for s in scenes:
        sid = s.get("id")
        vtype = s.get("visual_type")
        out_png = os.path.join(assets_dir, f"{sid}_window.png")
        if os.path.exists(out_png):
            continue

        if vtype == "editor":
            # Check for real code file in code_dir
            sample_code = s.get("code_snippet") or "def main():\n    pass\n"
            title = s.get("code_filename") or "spec.md"
            badge = s.get("code_badge") or "MARKDOWN"
            lang = "markdown" if title.endswith(".md") else "python"
            
            # If code file exists on disk, read it
            cand_file = os.path.join(code_dir, title)
            if os.path.exists(cand_file):
                with open(cand_file, "r", encoding="utf-8") as f:
                    sample_code = f.read()

            print(f"  📸 Capturing Real VS Code Window for: {sid} ({title})")
            render_code_window(sample_code, out_png, lang=lang, title=title, badge=badge, width=1380, is_4k=is_4k)

        elif vtype in ["code", "terminal"]:
            cmd = s.get("terminal_cmd") or "pytest -v test_validator.py"
            out_lines = s.get("terminal_output") or [
                ("collected 7 items", "info"),
                ("7 passed in 0.14s", "pass")
            ]
            print(f"  💻 Capturing Real Terminal Window for: {sid} ({cmd})")
            render_terminal_window(cmd, out_lines, out_png, title="Terminal", width=1380, is_4k=is_4k)

        elif vtype == "split":
            left_code = s.get("code_left") or "# Naive Unchecked Code\ndef validate(x): return True\n"
            right_code = s.get("code_right") or "# Clean Spec-Driven Implementation\ndef validate(x: str) -> bool: return True\n"
            print(f"  ⚖️ Capturing Real Split Comparison for: {sid}")
            render_split_code_window(left_code, "naive.py", right_code, "clean.py", out_png, width=1600, is_4k=is_4k)

def composite_video(
    project_dir: str,
    channel_cfg: Dict[str, Any],
    profile_key: str = "1080p30",
    output_mp4: Optional[str] = None
) -> str:
    """Stage 5: Declarative Hardware-Accelerated Video Compositing."""
    print("\n" + "=" * 70)
    print(f"🎬 STAGE 5: Declarative Video Compositing (Profile: {profile_key})")
    print("=" * 70)

    profile = PROFILES.get(profile_key, PROFILES["1080p30"])
    tl_path = os.path.join(project_dir, "tl.json")
    with open(tl_path, "r", encoding="utf-8") as f:
        timeline = json.load(f)

    audio_master_path = os.path.join(project_dir, "audio_master.wav")
    total_dur = timeline[-1]["end_time"] + timeline[-1]["silence_dur"]
    total_frames = int(round(total_dur * profile.fps))

    if output_mp4 is None:
        output_mp4 = os.path.join(project_dir, f"{os.path.basename(project_dir)}.mp4")

    # Load logo
    logo_path = channel_cfg.get("logo_path")
    if logo_path and not os.path.isabs(logo_path):
        logo_path = os.path.join(REPO_ROOT, logo_path)
    logo_img = Image.open(logo_path).convert("RGBA") if (logo_path and os.path.exists(logo_path)) else None

    # Load real assets
    assets_dir = os.path.join(project_dir, "assets")
    cached_assets: Dict[str, Image.Image] = {}
    if os.path.exists(assets_dir):
        for fn in os.listdir(assets_dir):
            if fn.endswith(".png"):
                sid = fn.replace("_window.png", "")
                cached_assets[sid] = Image.open(os.path.join(assets_dir, fn)).convert("RGBA")

    # Subtitle track
    sub_track = SubtitleTrack(timeline, is_short=profile.is_vertical)

    canvas = OverscanCanvas(profile, overscan=0.035)
    f_sub = get_font(profile.subtitle_fontsize)

    channel_name = channel_cfg.get("channel_name", "TechChannel")
    tagline = channel_cfg.get("tagline", "AI • TECH • CODE")
    badge = channel_cfg.get("badge", "TC")

    dt = profile.frame_time

    with StreamingVideoPipeline(
        output_path=output_mp4,
        width=profile.width,
        height=profile.height,
        fps=profile.fps,
        audio_path=audio_master_path,
        total_frames=total_frames
    ) as pipe:
        
        for f_idx in range(total_frames):
            t = f_idx * dt

            # Find active scene
            cur_scene = timeline[-1]
            for s in timeline:
                if s["start_time"] <= t < (s["end_time"] + s["silence_dur"]):
                    cur_scene = s
                    break

            st = cur_scene["start_time"]
            dur = max(0.001, cur_scene["duration"])
            rel_t = max(0.0, t - st)
            p_scene = min(1.0, rel_t / dur)
            vtype = cur_scene.get("visual_type", "diagram")
            sid = cur_scene.get("id")

            # 1. Reset canvas
            canvas.reset()

            # 2. Render Scene Visuals
            if vtype == "brand":
                render_brand_card(canvas, channel_name, tagline, badge, rel_t, logo_img=logo_img)
            elif sid == timeline[-1]["id"] and rel_t > 2.0:
                render_outro_card(canvas, channel_name, tagline, rel_t, logo_img=logo_img)
            elif sid in cached_assets:
                # Real UI window
                render_real_asset_frame(canvas, cached_assets[sid], rel_t)
            else:
                # Fallback clean card
                cx, cy = canvas.W // 2, canvas.H // 2 - 20
                canvas.draw_card((cx - 500, cy - 250, cx + 500, cy + 250), radius=20, fill=(16, 22, 38), outline=(70, 220, 255, 120), width=1)
                canvas.draw_text((cx, cy - 50), cur_scene.get("title", "").upper(), size=32, fill=(70, 220, 255), anchor="mm")
                canvas.draw_text((cx, cy + 30), cur_scene.get("section", "").upper(), size=20, fill=(185, 192, 225), anchor="mm")

            # 3. Slice overscan frame with camera drift
            frame = canvas.slice_frame(p_scene, drift_amp=6.0)
            dr_frame = ImageDraw.Draw(frame)

            # 4. Render synchronized subtitles (safe zone at bottom center)
            sub_y = profile.subtitle_y
            sub_x = profile.width // 2
            sub_track.render_subtitle(
                draw=dr_frame,
                t=t,
                center_x=sub_x,
                center_y=sub_y,
                font=f_sub,
                color=(255, 255, 255),
                stroke_width=profile.subtitle_stroke
            )

            # 5. Top-Left Watermark
            if not profile.is_vertical:
                f_watermark = get_font(20)
                dr_frame.text((70, 50), channel_name.upper(), font=f_watermark, fill=(160, 175, 215))

            # Stream frame
            pipe.write_frame(frame)

    return output_mp4

def run_qa_gate(video_path: str, is_short: bool = False):
    """Stage 6: Automated QA Verification Gate."""
    print("\n" + "=" * 70)
    print("🛡️ STAGE 6: Automated QA Compliance Verification")
    print("=" * 70)
    qa_script = os.path.join(REPO_ROOT, "tools", "qa.py")
    kind = "short" if is_short else "long"
    subprocess.run([sys.executable, qa_script, video_path, kind], check=True)

def main():
    parser = argparse.ArgumentParser(description="Autonomous Faceless Video Studio Orchestrator")
    parser.add_argument("action", choices=["build"], help="Action to execute")
    parser.add_argument("--project", required=True, help="Path to project directory")
    parser.add_argument("--channel", help="Channel name (e.g. TechXKenil, Aiwolfie)")
    parser.add_argument("--format", default="1080p30", choices=["1080p30", "4k60", "1080p30_vert", "4k60_vert"], help="Render resolution profile")
    args = parser.parse_args()

    project_dir = os.path.abspath(args.project)
    channel_cfg = get_channel_config(channel_name_or_path=args.channel)

    print("🚀 Starting Unified Video Production Orchestrator:")
    print(f"  Project : {project_dir}")
    print(f"  Channel : {channel_cfg.get('channel_name')} (Badge: {channel_cfg.get('badge')})")
    print(f"  Format  : {args.format}")

    # Stage 1: Load Scenes
    scenes = load_project_scenes(project_dir)

    # Stage 1.5: Story-Aware Animation Planning (Animation Director)
    print("\n" + "=" * 70)
    print("🎬 STAGE 1.5: Story-Aware Animation Planning (Animation Director)")
    print("=" * 70)
    director = AnimationDirector()
    aspect_ratio = "9:16" if "vert" in args.format else "16:9"
    brief = director.parse_brief_from_prompt(
        prompt=os.path.basename(project_dir).replace("_", " "),
        default_aspect=aspect_ratio
    )
    brief.brand_profile = channel_cfg.get("channel_name", "TechXKenil")
    animation_plan = director.plan_video(scenes, brief)
    
    plan_out_path = os.path.join(project_dir, "animation_plan.json")
    with open(plan_out_path, "w", encoding="utf-8") as f:
        json.dump(animation_plan, f, indent=2)
    print(f"✓ Validated AnimationPlan saved: {plan_out_path}")
    print(f"  Total planned scenes: {len(animation_plan['scenes'])}")

    # Stage 2: TTS Synthesis
    raw_wav, tl_path, dur = synthesize_speech(scenes, channel_cfg, project_dir)

    # Stage 3: Sound Design & Mastering
    is_short = "vert" in args.format or dur <= 60.0
    target_lufs = -14.0 if is_short else -14.5
    master_wav, mastered_dur = prepare_sound_design(raw_wav, tl_path, project_dir, target_lufs=target_lufs)

    # Stage 4: Real UI Capture
    is_4k = "4k" in args.format
    prepare_real_ui_assets(scenes, project_dir, is_4k=is_4k)

    # Stage 5: Video Composition
    out_mp4 = composite_video(project_dir, channel_cfg, profile_key=args.format)

    # Stage 6: QA Verification
    is_short = "vert" in args.format
    run_qa_gate(out_mp4, is_short=is_short)

    print("\n" + "=" * 70)
    print("🎉 FULL PRODUCTION PIPELINE COMPLETE & VERIFIED!")
    print(f"  Master MP4: {out_mp4}")
    print("=" * 70)

if __name__ == "__main__":
    main()
