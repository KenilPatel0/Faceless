# tts_higgsfield.py
import os
import sys
import json
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from data_higgsfield import SCENES

def find_file(filename):
    for candidate in [
        os.path.join(REPO_ROOT, filename),
        os.path.join(SCRIPT_DIR, filename),
        filename
    ]:
        if os.path.exists(candidate):
            return candidate
    return filename

print("Initializing Kokoro TTS...")
k = Kokoro(find_file("kokoro.onnx"), find_file("voices.bin"))
parts = []
tl = []

total_beats = sum(len(sc["beats"]) for sc in SCENES)
current_beat = 0

for sc in SCENES:
    bd = []
    print(f"\nProcessing scene: {sc['name']} ({len(sc['beats'])} beats)")
    for i, b in enumerate(sc["beats"]):
        current_beat += 1
        text = b[0]
        print(f"[{current_beat}/{total_beats}] Synthesizing: {text[:60]}...")
        samples, sr = k.create(text, voice="am_michael", speed=1.1, lang="en-us")
        pad = 0.18 + (0.45 if i == len(sc["beats"]) - 1 else 0)
        padded = np.concatenate([samples, np.zeros(int(sr * pad), dtype=samples.dtype)])
        parts.append(padded)
        dur = len(padded) / sr
        bd.append(dur)
    tl.append(bd)

combined = np.concatenate(parts)
output_wav = os.path.join(SCRIPT_DIR, "audio_higgsfield.wav")
tl_file = os.path.join(SCRIPT_DIR, "tl_higgsfield.json")
sf.write(output_wav, combined, sr)
with open(tl_file, "w") as f:
    json.dump(tl, f, indent=2)

total_duration = sum(map(sum, tl))
print(f"\nFinished TTS Generation!")
print(f"Total Video Duration: {round(total_duration, 2)} seconds ({int(total_duration // 60)}m {int(total_duration % 60)}s)")
print(f"WAV saved to: {output_wav}")
print(f"Timeline saved to: {tl_file}")

