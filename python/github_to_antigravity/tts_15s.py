import os, sys, json, numpy as np, soundfile as sf
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
        "id": "github_hook",
        "title": "REAL GITHUB REPO",
        "text": "Found a repo on GitHub? Don't install it manually.",
        "sfx": [(0.05, "whoosh", -18), (1.5, "pop", -15)]
    },
    {
        "id": "antigravity_setup",
        "title": "ANTIGRAVITY SETUP",
        "text": "Just paste the link into Antigravity. Its AI agent clones it, configures the environment, and runs it.",
        "sfx": [(0.05, "whoosh", -18), (1.8, "tick", -16), (4.2, "chime", -15)]
    },
    {
        "id": "outro",
        "title": "TECHXKENIL OUTRO",
        "text": "Zero setup needed. Subscribe to TechXKenil for more AI and tech.",
        "sfx": [(0.1, "whoosh", -20), (1.0, "chime", -14)]
    }
]

print("Generating Kokoro TTS narration for 15s Short...")
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
raw_wav = os.path.join(SCRIPT_DIR, "raw_15s.wav")
sf.write(raw_wav, raw_combined, sr)

print(f"Mixing {len(events)} sound effects...")
mixed = mix(raw_combined, sr, events=events, sfx_db=-15)
sf.write(raw_wav, mixed, sr)

mastered_wav = os.path.join(SCRIPT_DIR, "audio_15s.wav")
print(f"Mastering loudness to -14.0 LUFS (-1.5 dBTP)...")
master(raw_wav, mastered_wav, lufs=-14, tp=-1.5)
if os.path.exists(raw_wav):
    os.remove(raw_wav)

meta_json = os.path.join(SCRIPT_DIR, "meta_15s.json")
with open(meta_json, "w") as f:
    json.dump({"scenes": meta, "total_duration": current_time, "sample_rate": 48000}, f, indent=2)

print(f"Audio ready! Total duration: {current_time:.2f}s ({round(current_time, 1)}s)")

