import json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
from longdata_ms import SCENES

k = Kokoro("kokoro.onnx", "voices.bin")
parts = []
tl = []

print("Generating Kokoro TTS narration for TechXKenil long video...")
for s_idx, sc in enumerate(SCENES):
    bd = []
    print(f"  Scene {s_idx + 1}/{len(SCENES)}: {sc['name']}")
    for i, b in enumerate(sc["beats"]):
        s, sr = k.create(b[0], voice="am_michael", speed=1.1, lang="en-us")
        pad = 0.18 + (0.45 if i == len(sc["beats"]) - 1 else 0)
        a = np.concatenate([s, np.zeros(int(sr * pad), dtype=s.dtype)])
        parts.append(a)
        bd.append(len(a) / sr)
    tl.append(bd)

combined = np.concatenate(parts)
sf.write("audio_ms.wav", combined, sr)
json.dump(tl, open("tl_ms.json", "w"))

total_sec = round(sum(map(sum, tl)), 1)
print(f"Finished audio generation! Total duration: {total_sec} sec ({round(total_sec / 60, 2)} minutes)")

