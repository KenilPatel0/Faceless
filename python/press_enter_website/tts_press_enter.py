#!/usr/bin/env python3
"""
tts_press_enter.py — Voice synthesis and audio mastering for:
Short 6: "What Happens When You Press Enter on a Website"
Target Duration: exactly ~29.5s (28-32s safe zone)
Voice: Kokoro ONNX (am_michael, speed 1.1)
"""

import os
import sys
import json
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TOOLS_DIR = os.path.join(REPO_ROOT, "python", "tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from motion import make_sfx, mix, master, word_timings

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SR = 24000

SCENES = [
    {
        "id": "hook",
        "title": "WHAT HAPPENS WHEN YOU PRESS ENTER?",
        "step_num": 0,
        "label": "ENTER KEY",
        "text": "What happens when you type a website and press Enter?",
    },
    {
        "id": "intro",
        "title": "TECHXKENIL INTRO",
        "step_num": 0,
        "label": "TECHXKENIL",
        "text": "I'm Kenil, and this is TechXKenil.",
    },
    {
        "id": "step1_dns",
        "title": "STEP 1 // DNS LOOKUP",
        "step_num": 1,
        "label": "DNS LOOKUP",
        "text": "Step one: your browser asks DNS to turn that name into an IP address.",
    },
    {
        "id": "step2_https",
        "title": "STEP 2 // SECURE HTTPS & TLS",
        "step_num": 2,
        "label": "HTTPS LOCK",
        "text": "Step two: it connects to the server and sets up secure HTTPS.",
    },
    {
        "id": "step3_payload",
        "title": "STEP 3 & 4 // HTML, CSS & JAVASCRIPT",
        "step_num": 3,
        "label": "HTTP PAYLOAD",
        "text": "Steps three and four: the server replies with HTML, CSS, and JavaScript.",
    },
    {
        "id": "step5_render",
        "title": "STEP 5 // PIXEL PAINTING",
        "step_num": 5,
        "label": "DOM RENDER",
        "text": "Step five: your browser builds the page on your screen. In milliseconds.",
    },
    {
        "id": "outro",
        "title": "TECHXKENIL OUTRO",
        "step_num": 0,
        "label": "SUBSCRIBE",
        "text": "Subscribe to TechXKenil for more tech, explained fast.",
    },
]

def main():
    print(f"\n=======================================================")
    print(f"🎬 Generating Audio for Short 6: Press Enter on a Website")
    print(f"=======================================================")

    kokoro_path = os.path.join(REPO_ROOT, "kokoro.onnx")
    voices_path = os.path.join(REPO_ROOT, "voices.bin")
    kokoro = Kokoro(kokoro_path, voices_path)

    timeline = []
    current_time = 0.0
    audio_chunks = []

    for i, sc in enumerate(SCENES):
        text = sc["text"]
        print(f"  [{i+1}/{len(SCENES)}] Synthesizing: {sc['title']}")
        samples, sr = kokoro.create(text, voice="am_michael", speed=1.1, lang="en-us")
        dur = len(samples) / sr

        # Exact word boundaries using t0 and t1 (strictly monotonic)
        words = word_timings(text, current_time, current_time + dur)

        pause = 0.20 if i < len(SCENES) - 1 else 0.45
        entry = {
            **sc,
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
    print(f"  Total Voice Track Duration: {total_duration:.2f}s (Target: ~29-30s)")

    # Sound design events
    sfx_events = []
    for sc in timeline:
        t = sc["start"]
        sfx_events.append((t, "whoosh", -10))

        if sc["id"] == "step1_dns":
            sfx_events.append((t + 0.8, "tick", -6))
            sfx_events.append((t + 1.4, "pop", -6))
        elif sc["id"] == "step2_https":
            sfx_events.append((t + 1.1, "pop", -5))   # Secure padlock lock
        elif sc["id"] == "step3_payload":
            sfx_events.append((t + 0.9, "pop", -6))   # HTML
            sfx_events.append((t + 1.4, "pop", -6))   # CSS
            sfx_events.append((t + 1.9, "pop", -6))   # JS
        elif sc["id"] == "step5_render":
            sfx_events.append((t + 1.2, "pop", -6))
        elif sc["id"] == "outro":
            sfx_events.append((sc["end"] - 1.2, "chime", -6))

    mixed_audio = mix(voice_track, SR, events=sfx_events)

    raw_path = os.path.join(OUT_DIR, "audio_press_enter_raw.wav")
    master_path = os.path.join(OUT_DIR, "audio_press_enter.wav")
    meta_path = os.path.join(OUT_DIR, "meta_press_enter.json")

    sf.write(raw_path, mixed_audio, SR)
    master(raw_path, master_path, lufs=-14.0)

    with open(meta_path, "w") as f:
        json.dump({
            "total_duration": total_duration,
            "scenes": timeline
        }, f, indent=2)

    print(f"  ✓ Audio Master: {master_path}")
    print(f"  ✓ Metadata JSON: {meta_path}")

if __name__ == "__main__":
    main()
