import os, sys, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from longdata import SCENES

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
parts=[]; tl=[]
for sc in SCENES:
    bd=[]
    for i,b in enumerate(sc["beats"]):
        s,sr=k.create(b[0],voice="am_michael",speed=1.1,lang="en-us")
        pad=0.18+(0.45 if i==len(sc["beats"])-1 else 0)
        a=np.concatenate([s,np.zeros(int(sr*pad),dtype=s.dtype)])
        parts.append(a); bd.append(len(a)/sr)
    tl.append(bd)
sf.write(os.path.join(SCRIPT_DIR, "audio_long.wav"), np.concatenate(parts), sr)
json.dump(tl, open(os.path.join(SCRIPT_DIR, "tl.json"), "w"))
print(round(sum(map(sum,tl)),1),"sec")
