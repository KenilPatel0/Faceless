import os, sys, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

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
scenes=[
 ("hook4","Chatbot or agent: what's the difference?"),
 ("intro","I'm Kenil, and this is TechXKenil."),
 ("chat4","A chatbot answers. An agent acts."),
 ("trip4","Ask a chatbot to plan a trip, and you get a plan. An agent searches flights, compares prices, and fills in the form."),
 ("loop4","It runs in a loop with tools: think, act, observe, repeat."),
 ("same4","Same model underneath. The difference is the loop and the tools."),
 ("guard4","That's why agents are powerful, and why they need guardrails. They can do wrong things too."),
 ("outro","Subscribe to TechXKenil for more AI and tech."),
]
meta=[];parts=[]
for n,t in scenes:
    s,sr=k.create(t,voice="am_michael",speed=1.1,lang="en-us")
    a=np.concatenate([s,np.zeros(int(sr*0.18),dtype=s.dtype)]); parts.append(a); meta.append(dict(name=n,text=t,dur=len(a)/sr))
sf.write(os.path.join(SCRIPT_DIR, "audio4.wav"), np.concatenate(parts), sr)
json.dump(meta, open(os.path.join(SCRIPT_DIR, "meta4.json"), "w"))
print(round(sum(m["dur"] for m in meta),1),[round(m["dur"],1) for m in meta])
