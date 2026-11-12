#!/usr/bin/env python3
"""
tts_black_hole.py — Synthesizes narration & audio master for Black Hole demo videos:
1. 15s Vertical Short (1080x1920)
2. 40s Horizontal Explainer (1920x1080)
"""

import os
import sys
import json
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import make_sfx, mix, master, word_timings

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SR = 24000

# ---------------------------------------------------------------------------
# 1. 15-SECOND VERTICAL SCRIPT (Calibrated exactly ~15.0s)
# ---------------------------------------------------------------------------
VERTICAL_BEATS = [
    {
        "id": "hook",
        "title": "WHAT IS A BLACK HOLE?",
        "subtitle": "GRAVITY BENDS LIGHT",
        "text": "What is a black hole? An object where gravity is so intense, even light cannot escape.",
    },
    {
        "id": "physics",
        "title": "HOW IT FORMS // STELLAR COLLAPSE",
        "subtitle": "SINGULARITY & EVENT HORIZON",
        "text": "When a massive star dies, gravity crushes its core into a Singularity behind the Event Horizon.",
    },
    {
        "id": "outro",
        "title": "SUBSCRIBE TO TECHXKENIL",
        "subtitle": "AI • TECH • CODE",
        "text": "Subscribe to TechXKenil for more deep science.",
    },
]

# ---------------------------------------------------------------------------
# 2. 40-SECOND HORIZONTAL SCRIPT (Calibrated exactly ~40.0s)
# ---------------------------------------------------------------------------
HORIZONTAL_BEATS = [
    {
        "id": "definition",
        "act": "PART 01 // COSMIC EXTREMES",
        "title": "What is a Black Hole?",
        "subtitle": "Infinite density warped into a single point of zero volume",
        "text": "Imagine squeezing three million Earths into a sphere smaller than a city. That is a black hole: an astronomical object packed so densely that gravity warps space and time itself.",
    },
    {
        "id": "collapse",
        "act": "PART 02 // STELLAR COLLAPSE",
        "title": "How Black Holes Form",
        "subtitle": "When massive stars run out of nuclear fuel",
        "text": "It begins when a giant star twenty times heavier than our Sun burns out its fuel. Without outward pressure to fight gravity, the core collapses at a quarter the speed of light.",
    },
    {
        "id": "anatomy",
        "act": "PART 03 // ANATOMY OF GRAVITY",
        "title": "The Point of No Return",
        "subtitle": "The Singularity and Event Horizon boundary",
        "text": "Around the Singularity lies the Event Horizon: the cosmic point of no return. Cross this boundary, and the required escape velocity exceeds the speed of light.",
    },
    {
        "id": "verdict",
        "act": "PART 04 // THE VERDICT",
        "title": "Pure Gravity in Action",
        "subtitle": "Subscribe to TechXKenil for deep dive explainers",
        "text": "Black holes are not cosmic vacuums. They are gravity in its purest, most extreme form. Subscribe to TechXKenil for more deep science.",
    },
]

def generate_track(beats, prefix):
    print(f"\n=======================================================")
    print(f"🎬 Generating Audio for: {prefix}")
    print(f"=======================================================")
    kokoro = Kokoro("kokoro.onnx", "voices.bin")
    
    timeline = []
    current_time = 0.0
    audio_chunks = []
    
    for i, b in enumerate(beats):
        text = b["text"]
        print(f"  [{i+1}/{len(beats)}] Synthesizing: {b['title']}")
        samples, sr = kokoro.create(text, voice="am_michael", speed=1.1, lang="en-us")
        dur = len(samples) / sr
        
        # Calculate word boundaries
        words = word_timings(text, current_time, current_time + dur)
        
        pause = 0.20 if i < len(beats) - 1 else 0.40
        entry = {
            **b,
            "start": current_time,
            "duration": dur,
            "end": current_time + dur,
            "words": words,
        }
        timeline.append(entry)
        
        audio_chunks.append(samples)
        silence_samples = int(pause * sr)
        audio_chunks.append(np.zeros(silence_samples, dtype=np.float32))
        
        current_time += dur + pause
    
    voice_track = np.concatenate(audio_chunks)
    total_duration = len(voice_track) / SR
    print(f"  Voice track duration: {total_duration:.2f}s")
    
    # Mix dynamic sound effects
    sfx_layers = []
    for b in timeline:
        t = b["start"]
        # Scene transition whoosh
        sfx_layers.append((t, "whoosh", -8))
        # Accent pops
        if b["id"] in ("collapse", "physics"):
            sfx_layers.append((t + 0.8, "pop", -6))
        elif b["id"] in ("event_horizon", "anatomy"):
            sfx_layers.append((t + 1.2, "pop", -6))
        elif b["id"] in ("outro", "verdict"):
            sfx_layers.append((b["end"] - 1.0, "chime", -6))
            
    mixed_audio = mix(voice_track, SR, events=sfx_layers)
    
    # Save raw temporary audio and master to -14.0 LUFS
    raw_path = os.path.join(OUT_DIR, f"{prefix}_raw.wav")
    master_path = os.path.join(OUT_DIR, f"{prefix}_audio.wav")
    meta_path = os.path.join(OUT_DIR, f"{prefix}_meta.json")
    
    sf.write(raw_path, mixed_audio, SR)
    master(raw_path, master_path, lufs=-14.0)
    if os.path.exists(raw_path):
        os.remove(raw_path)
        
    with open(meta_path, "w") as f:
        json.dump({"total_duration": total_duration, "beats": timeline}, f, indent=2)
        
    print(f"  ✓ Audio mastered to: {master_path}")
    print(f"  ✓ Metadata saved to: {meta_path}")
    return total_duration

if __name__ == "__main__":
    dur_vert = generate_track(VERTICAL_BEATS, "black_hole_vertical")
    dur_horiz = generate_track(HORIZONTAL_BEATS, "black_hole_horizontal")
    print(f"\n=======================================================")
    print(f"✨ Audio generation complete!")
    print(f"   Vertical Short: {dur_vert:.2f}s (Target: ~15s)")
    print(f"   Horizontal Explainer: {dur_horiz:.2f}s (Target: ~40s)")
    print(f"=======================================================")
