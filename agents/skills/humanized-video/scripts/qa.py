"""QA gate. Usage: python3 qa.py video.mp4 short|long      (exit code 1 = fix before upload)"""
import re, subprocess, sys
def run(args): return subprocess.run(["ffmpeg", "-hide_banner", "-nostats"] + args, capture_output=True, text=True).stderr
def decode_errors(p): return len([l for l in run(["-v", "error", "-i", p, "-f", "null", "-"]).splitlines() if l.strip()])
def loudness(p):
    s = run(["-i", p, "-filter_complex", "ebur128=peak=true", "-f", "null", "-"])
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", s); pk = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", s)
    return (float(i[-1]) if i else None, float(pk[-1]) if pk else None)
def freezes(p, kind):
    crop, d = (0.75, 4) if kind == "short" else (0.88, 9)          # ignore the caption band; flag static holds
    s = run(["-i", p, "-vf", f"crop=iw:ih*{crop}:0:0,freezedetect=n=0.002:d={d}", "-an", "-f", "null", "-"])
    st = re.findall(r"freeze_start: ([\d.]+)", s); du = re.findall(r"freeze_duration: ([\d.]+)", s)
    return [(float(a), float(b)) for a, b in zip(st, du)], d
if __name__ == "__main__":
    p, kind = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "short"); bad = False
    e = decode_errors(p); print(f"decode errors : {e}  {'OK' if e == 0 else 'FAIL'}"); bad |= e > 0
    lu, pk = loudness(p); ok = lu is not None and -16.5 <= lu <= -12.5 and (pk is None or pk <= -0.5)
    print(f"loudness      : {lu} LUFS, true peak {pk} dBFS (target -14 LUFS, <= -0.5 after AAC)  {'OK' if ok else 'FIX'}"); bad |= not ok
    fr, d = freezes(p, kind); print(f"static holds >{d}s (content area): {len(fr)}  {'OK' if not fr else 'FIX'}")
    for a, b in fr[:12]: print(f"   at {a:.1f}s for {b:.1f}s")
    bad |= bool(fr); sys.exit(1 if bad else 0)
