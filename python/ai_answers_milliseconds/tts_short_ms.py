import os, sys, json, re, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
TOOLS_DIR = os.path.join(REPO_ROOT, "python", "tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from humanize import master, mix

def find_file(filename):
    for candidate in [
        os.path.join(REPO_ROOT, filename),
        os.path.join(SCRIPT_DIR, filename),
        filename
    ]:
        if os.path.exists(candidate):
            return candidate
    return filename

k = Kokoro(find_file("kokoro.onnx"), find_file("voices.bin"))

scenes_def = [
    {
        "id": "hook",
        "title": "THE MILLISECOND PARADOX",
        "text": "You type a prompt, and AI answers in forty milliseconds. But how?",
        "sfx": [(0.05, "whoosh", -18), (1.6, "pop", -14)]
    },
    {
        "id": "intro",
        "title": "TXK INTRO",
        "text": "I'm Kenil, and this is TechXKenil.",
        "sfx": [(0.1, "whoosh", -20), (1.1, "chime", -16)]
    },
    {
        "id": "silicon_bandwidth",
        "title": "140 TRILLION OPS & HBM3E",
        "text": "Every single word takes one hundred forty billion math calculations. A normal PC freezes. But AI chips stream three terabytes of model weights every second using High Bandwidth Memory.",
        "sfx": [(0.05, "whoosh", -18), (1.2, "pop", -14), (4.5, "tick", -16), (8.0, "pop", -14)]
    },
    {
        "id": "kv_cache_outro",
        "title": "KV CACHE & OUTRO",
        "text": "Plus, the KV Cache saves past tokens so the AI never recalculates. Calculated live in silicon. Subscribe to TechXKenil for more AI and tech.",
        "sfx": [(0.05, "whoosh", -18), (2.0, "tick", -16), (5.5, "chime", -14)]
    }
]

print("Generating Kokoro TTS narration for TechXKenil 30s Short...")
parts = []
meta = []
events = []
current_time = 0.0

for s_idx, sc in enumerate(scenes_def):
    text = sc["text"]
    s, sr = k.create(text, voice="am_michael", speed=1.1, lang="en-us")
    pad_sec = 0.18
    pad = np.zeros(int(sr * pad_sec), dtype=s.dtype)
    audio_chunk = np.concatenate([s, pad])
    dur = len(audio_chunk) / sr
    
    # Store SFX events aligned to timeline
    for offset, sfx_kind, gain_db in sc["sfx"]:
        events.append((current_time + offset, sfx_kind, gain_db))
        
    meta.append({
        "id": sc["id"],
        "title": sc["title"],
        "text": text,
        "start": current_time,
        "dur": dur,
        "end": current_time + dur
    })
    
    parts.append(audio_chunk)
    current_time += dur
    print(f"  Scene {s_idx+1}: {sc['id']} ({dur:.2f}s) - {len(text.split())} words")

raw_combined = np.concatenate(parts)
raw_wav = os.path.join(SCRIPT_DIR, "raw_short_ms.wav")
sf.write(raw_wav, raw_combined, sr)

print(f"Mixing {len(events)} sound effects...")
mixed = mix(raw_combined, sr, events=events, sfx_db=-15)
sf.write(raw_wav, mixed, sr)

mastered_wav = os.path.join(SCRIPT_DIR, "audio_short_ms.wav")
print(f"Mastering loudness to -14.0 LUFS (-1.5 dBTP)...")
master(raw_wav, mastered_wav, lufs=-14, tp=-1.5)
if os.path.exists(raw_wav):
    os.remove(raw_wav)

meta_json = os.path.join(SCRIPT_DIR, "meta_short_ms.json")
with open(meta_json, "w") as f:
    json.dump({"scenes": meta, "total_duration": current_time, "sample_rate": 48000}, f, indent=2)

print(f"Audio ready! Total duration: {current_time:.2f}s ({round(current_time, 1)}s)")

