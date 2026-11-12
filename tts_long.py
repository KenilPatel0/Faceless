import json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
from longdata import SCENES
k=Kokoro("kokoro.onnx","voices.bin"); parts=[]; tl=[]
for sc in SCENES:
    bd=[]
    for i,b in enumerate(sc["beats"]):
        s,sr=k.create(b[0],voice="am_michael",speed=1.1,lang="en-us")
        pad=0.18+(0.45 if i==len(sc["beats"])-1 else 0)
        a=np.concatenate([s,np.zeros(int(sr*pad),dtype=s.dtype)])
        parts.append(a); bd.append(len(a)/sr)
    tl.append(bd)
sf.write("audio_long.wav",np.concatenate(parts),sr); json.dump(tl,open("tl.json","w"))
print(round(sum(map(sum,tl)),1),"sec")
