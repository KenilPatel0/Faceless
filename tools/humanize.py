"""TechXKenil humanized motion + audio helpers. Pillow / numpy / ffmpeg only (no paid APIs).
Import into any render script:  from humanize import *
"""
import math, random, re, subprocess
import numpy as np
from PIL import Image, ImageDraw

# ------------------------------------------------------------------ easing
def clamp(x): return 0.0 if x < 0 else 1.0 if x > 1 else x
def ease_out_expo(x): x = clamp(x); return 1.0 if x >= 1 else 1 - 2 ** (-10 * x)      # default ENTRANCE
def ease_out_quart(x): x = clamp(x); return 1 - (1 - x) ** 4                          # calmer entrance
def ease_in_cubic(x): x = clamp(x); return x ** 3                                     # EXIT
def ease_in_out(x): x = clamp(x); return x * x * x * (x * (6 * x - 15) + 10)          # moves A->B
def ease_out_back(x, s=0.9): x = clamp(x) - 1; return 1 + x * x * ((s + 1) * x + s)   # subtle overshoot (~4%); max 1 per scene
def lerp(a, b, p): return a + (b - a) * p
def frame_align(t, fps): return round(t * fps) / fps

def progress(t, start, dur, ease=ease_out_expo):
    return ease((t - start) / dur) if dur > 0 else 1.0

def stagger(i, t, start=0.0, delay=0.09, dur=0.35, jitter=0.02, seed=7, ease=ease_out_expo):
    """Progress of item i in a staggered group. Deterministic per-item jitter so it feels hand-timed, not machine-timed."""
    j = random.Random(seed * 1009 + i).uniform(-jitter, jitter)
    return ease((t - start - i * delay - j) / dur)

def arc_point(p0, p1, u, bend=0.18):
    """Point on a curved path (quadratic bezier) - use for cursors/flying objects instead of straight lines."""
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    cx, cy = mx - dy * bend, my + dx * bend
    return ((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * cx + u * u * p1[0],
            (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * cy + u * u * p1[1])

def smooth_float(t, freq=1.2, amp=4.0, phase=0.0):
    """Subtle harmonic micro-float (amplitude in px) keeping static visual elements alive."""
    return amp * math.sin(t * freq * 2 * math.pi + phase)

def draw_minimal_card(dr, box, radius=20, fill=(16, 20, 36), outline=(70, 80, 110), width=1):
    """Clean, subtle glassmorphic card with delicate 1px border."""
    dr.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def draw_pill(dr, xy, text, font, text_color, bg_color, outline_color=None, pad=(20, 8), radius=14):
    """Draw a clean, minimalist pill badge."""
    w = dr.textlength(text, font=font)
    h = font.size if hasattr(font, 'size') else 28
    x0, y0 = xy[0] - pad[0], xy[1] - pad[1]
    x1, y1 = xy[0] + w + pad[0], xy[1] + h + pad[1]
    dr.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=bg_color, outline=outline_color, width=1 if outline_color else 0)
    dr.text(xy, text, font=font, fill=text_color)
    return x1 + 16

# ------------------------------------------------------------------ camera + finish
def push_in(img, p, amount=0.04, drift=(0.0, 0.0)):
    """Slow camera push (p = 0..1 over the scene). Apply to the CONTENT layer BEFORE drawing captions/brand tag."""
    w, h = img.size; z = 1 + amount * p; cw, ch = w / z, h / z
    x0 = (w - cw) / 2 + drift[0] * p * w * 0.01; y0 = (h - ch) / 2 + drift[1] * p * h * 0.01
    return img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w, h), Image.BILINEAR)

_VIG = {}
def finish(img, frame_idx, grain=3.0, vignette=0.15):
    """Subtle film grain + vignette so flat vector frames feel less 'generated'. Apply last (before captions if you want crisp text)."""
    a = np.asarray(img.convert("RGB"), dtype=np.float32)
    key = (img.size, vignette)
    if key not in _VIG:
        w, h = img.size; y, x = np.ogrid[:h, :w]
        r = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2) / 1.414
        _VIG[key] = (1 - vignette * np.clip(r, 0, 1) ** 2.2)[..., None].astype(np.float32)
    a *= _VIG[key]
    if grain > 0:
        rng = np.random.default_rng(frame_idx // 2)          # grain changes every 2 frames
        a += rng.normal(0, grain, a.shape[:2] + (1,)).astype(np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

# ------------------------------------------------------------------ hand-made touches
def hand_line(dr, x0, x1, y, p, color, width=8, seed=1, wobble=3.0):
    """Hand-drawn underline that draws on (p = 0..1). Stable wobble per seed."""
    rng = random.Random(seed); ph = rng.uniform(0, 6.28); n = 40; pts = []
    for k in range(int(n * clamp(p)) + 1):
        u = k / n
        pts.append((x0 + (x1 - x0) * u, y + wobble * math.sin(u * 9 + ph) + rng.uniform(-0.6, 0.6)))
    if len(pts) > 1: dr.line(pts, fill=color, width=width, joint="curve")

def draw_cursor(dr, pos, click_p=0.0, color=(255, 255, 255), ripple=(255, 205, 70)):
    x, y = pos
    dr.polygon([(x, y), (x, y + 34), (x + 9, y + 26), (x + 16, y + 40), (x + 22, y + 37), (x + 15, y + 24), (x + 27, y + 24)],
               fill=color, outline=(0, 0, 0))
    if 0 < click_p < 1:
        r = 10 + 40 * click_p; dr.ellipse([x - r, y - r, x + r, y + r], outline=ripple, width=4)

def typed(text, t, cps=11.0, seed=3):
    """Typing animation at human speed with uneven rhythm and small pauses after spaces."""
    rng = random.Random(seed); clock = 0.0; n = 0
    for ch in text:
        clock += (1.0 / cps) * rng.uniform(0.6, 1.5) + (0.12 if ch == " " else 0)
        if clock > t: break
        n += 1
    return text[:n]

# ------------------------------------------------------------------ captions with word highlight
def _syl(w): return max(1, len(re.findall(r"[aeiouy]+", w.lower())))
def word_timings(text, t0, t1):
    """Estimate per-word times from syllables + punctuation (better than character count)."""
    words = text.split(); wts = []
    for w in words:
        extra = 1.2 if w.endswith((".", "?", "!")) else 0.6 if w.endswith((",", ":", ";")) else 0.0
        wts.append(_syl(re.sub(r"[^A-Za-z']", "", w) or "a") + extra)
    tot = sum(wts); out = []; t = t0
    for w, x in zip(words, wts):
        d = (t1 - t0) * x / tot; out.append((w, t, t + d)); t += d
    return out

def draw_karaoke(dr, center, words, t, font, color=(255, 255, 255), active=(255, 205, 70), stroke=8):
    """words = [(word,start,end)] of ONE caption chunk. Active word is highlighted (use for Shorts)."""
    wd = [dr.textlength(w.upper() + " ", font=font) for w, _, _ in words]; x = center[0] - sum(wd) / 2
    for (w, a, b), d in zip(words, wd):
        dr.text((x, center[1]), w.upper(), font=font, fill=active if a <= t < b else color,
                anchor="lm", stroke_width=stroke, stroke_fill=(0, 0, 0)); x += d

# ------------------------------------------------------------------ narration humanizing (Kokoro)
def speak_humanized(kokoro, text, voice="am_michael", base=1.1, seed=0, jitter=0.04, pause=(0.22, 0.34)):
    """Per-sentence speed variation (+/-4%) and uneven pauses, same voice. Returns (audio, sr, [(sentence,t0,t1)])."""
    rng = random.Random(seed); parts = []; timings = []; t = 0.0
    for s in re.split(r"(?<=[.!?])\s+", text.strip()):
        sp = base * (1 + rng.uniform(-jitter, jitter)) * (0.95 if len(s.split()) <= 4 else 1.0)
        a, sr = kokoro.create(s, voice=voice, speed=sp, lang="en-us")
        gap = np.zeros(int(sr * rng.uniform(*pause)), dtype=a.dtype)
        timings.append((s, t, t + len(a) / sr)); parts += [a, gap]; t += (len(a) + len(gap)) / sr
    return np.concatenate(parts), sr, timings

# ------------------------------------------------------------------ sound design (all synthesized = no licence issues)
def db(x): return 10 ** (x / 20)
def _env(n, sr, attack, decay):
    t = np.arange(n) / sr; return np.minimum(t / attack, 1) * np.exp(-t / decay)

def make_sfx(kind, sr=24000, seed=0):
    """kinds: pop (text/icon appears), tick (list item), whoosh (scene change ONLY), chime (success/check)."""
    rng = np.random.default_rng(seed)
    if kind == "pop":
        n = int(sr * 0.14); t = np.arange(n) / sr; f = 700 * np.exp(-t * 18) + 250
        x = np.sin(2 * np.pi * np.cumsum(f) / sr) * _env(n, sr, 0.002, 0.04)
    elif kind == "tick":
        n = int(sr * 0.05); x = np.diff(rng.normal(0, 1, n), prepend=0) * _env(n, sr, 0.0005, 0.012)
    elif kind == "whoosh":
        n = int(sr * 0.45); x = np.convolve(rng.normal(0, 1, n), np.ones(24) / 24, "same") * np.sin(np.linspace(0, np.pi, n)) ** 2.2
    elif kind == "chime":
        n = int(sr * 0.6); t = np.arange(n) / sr
        x = (np.sin(2 * np.pi * 880 * t) + 0.5 * np.sin(2 * np.pi * 1320 * t)) * _env(n, sr, 0.003, 0.18)
    else: raise ValueError(kind)
    return (x / (np.max(np.abs(x)) + 1e-9) * 0.9).astype(np.float32)

def voice_envelope(v, sr, win=0.05, attack=0.05, release=0.4, thresh_db=-40):
    hop = int(sr * win); n = len(v) // hop + 1
    r = np.array([np.sqrt(np.mean(v[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(n)])
    on = (20 * np.log10(r + 1e-9) > thresh_db).astype(float); out = np.zeros(n); cur = 0.0
    a, rl = 1 - math.exp(-win / attack), 1 - math.exp(-win / release)
    for i in range(n):
        cur += (a if on[i] > cur else rl) * (on[i] - cur); out[i] = cur
    return np.interp(np.arange(len(v)) / sr, np.arange(n) * win, out)

def mix(voice, sr, events=(), music=None, music_db=(-14, -24), sfx_db=-16):
    """Voice on top, SFX on meaningful events, music ducked under speech.
    events = [(time_sec, 'pop'|'tick'|'whoosh'|'chime'[, gain_db])]. music_db = (level in gaps, level under voice) relative to voice peak."""
    v = voice / (np.max(np.abs(voice)) + 1e-9) * db(-3); out = v.copy(); env = voice_envelope(v, sr)
    if music is not None:
        m = np.resize(music, len(v)).astype(np.float32); m /= (np.max(np.abs(m)) + 1e-9)
        gain = db(music_db[0]) + (db(music_db[1]) - db(music_db[0])) * env
        fade = np.minimum(1, np.minimum(np.arange(len(v)), len(v) - 1 - np.arange(len(v))) / sr)   # 1 s fades
        out += m * gain * fade
    for ev in events:
        t, kind = ev[0], ev[1]; g = ev[2] if len(ev) > 2 else sfx_db
        s = make_sfx(kind, sr) * db(g); i = int(t * sr)
        if 0 <= i < len(out): out[i:i + len(s)] += s[:len(out) - i]
    pk = np.max(np.abs(out)); return out / pk * 0.97 if pk > 0.97 else out

def master(in_wav, out_wav, lufs=-14, tp=-1.5, lra=7):
    """YouTube-ready loudness: two-pass loudnorm to -14 LUFS target, -1.5 dBTP (headroom for AAC), 48 kHz."""
    import json
    f = f"loudnorm=I={lufs}:TP={tp}:LRA={lra}"
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", in_wav, "-af", f + ":print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    f2 = f + f":measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", in_wav, "-af", f2, "-ar", "48000", out_wav], check=True)
