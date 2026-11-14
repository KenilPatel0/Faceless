"""motion.py - smooth animation, motion blur, transitions and YouTube-ready export (extends humanize.py).
Pillow + numpy + ffmpeg only.   from motion import *
"""
import math, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from humanize import *   # easing, stagger, push_in, finish, hand_line, typed, word_timings, mix/master ...

# ------------------------------------------------------------------ physics + keyframes
def spring(t, freq=2.2, zeta=0.72):
    """0 -> 1 with a natural ~4% overshoot. t = seconds since the motion started. Settles in ~0.6 s."""
    if t <= 0: return 0.0
    w = 2 * math.pi * freq; wd = w * math.sqrt(1 - zeta ** 2)
    return 1 - math.exp(-zeta * w * t) * (math.cos(wd * t) + zeta * w / wd * math.sin(wd * t))

def tween(t, keys):
    """Keyframes: [(time, value), (time, value, ease), ...]. The ease belongs to the segment ENDING at that key (default ease_in_out)."""
    if t <= keys[0][0]: return keys[0][1]
    for a, b in zip(keys, keys[1:]):
        if t <= b[0]:
            e = b[2] if len(b) > 2 else ease_in_out
            return lerp(a[1], b[1], e((t - a[0]) / (b[0] - a[0])))
    return keys[-1][1]

def drift(t, seed=0, amp=6.0):
    """Slow organic camera/object drift (pixels) from summed sines - never repeats obviously."""
    r = random.Random(seed); p = [r.uniform(0, 6.28) for _ in range(4)]
    return (amp * (math.sin(0.7 * t + p[0]) + 0.5 * math.sin(1.9 * t + p[1])),
            amp * (math.sin(0.6 * t + p[2]) + 0.5 * math.sin(1.7 * t + p[3])))

def pulse(t, at, amount=0.05, dur=0.3):
    """Emphasis punch: scale 1 -> 1+amount -> 1 around time `at`."""
    return 1 + amount * math.sin(math.pi * (t - at) / dur) if at <= t <= at + dur else 1.0

def count_up(t, start, dur, end, begin=0, fmt="{:,.0f}"):
    return fmt.format(lerp(begin, end, ease_out_quart((t - start) / dur)))

# ------------------------------------------------------------------ supersampled canvas (anti-aliased, sub-pixel positions)
class SS:
    """Draw with normal 1x coordinates; output is anti-aliased and moves smoothly at sub-pixel positions.
    ss = SS((W,H), S=2); f = ss.font(FONT, 64); ss.rrect(box, radius=30, fill=...); ss.text((x,y),'Hi',f); layer = ss.out()  (RGBA)"""
    def __init__(self, size, S=2):
        self.S = S; self.size = size
        self.img = Image.new("RGBA", (size[0] * S, size[1] * S), (0, 0, 0, 0)); self.d = ImageDraw.Draw(self.img, "RGBA")
    def font(self, path, size): return ImageFont.truetype(path, max(1, int(size * self.S)))
    def _p(self, pts):
        if isinstance(pts[0], (tuple, list)): return [(x * self.S, y * self.S) for x, y in pts]
        return [v * self.S for v in pts]
    def _kw(self, kw):
        if kw.get("width"): kw["width"] = max(1, int(kw["width"] * self.S))
        return kw
    def rrect(self, box, radius=0, **kw): self.d.rounded_rectangle(self._p(box), radius=radius * self.S, **self._kw(kw))
    def ellipse(self, box, **kw): self.d.ellipse(self._p(box), **self._kw(kw))
    def line(self, pts, **kw): self.d.line(self._p(pts), **self._kw(kw))
    def polygon(self, pts, **kw): self.d.polygon(self._p(pts), **kw)
    def text(self, xy, s, font, anchor="mm", stroke=0, **kw):
        self.d.text((xy[0] * self.S, xy[1] * self.S), s, font=font, anchor=anchor, stroke_width=int(stroke * self.S), **kw)
    def tlen(self, s, font): return self.d.textlength(s, font=font) / self.S
    def out(self): return self.img.resize(self.size, Image.LANCZOS)

def composite(base_rgb, *layers):
    """Stack RGBA layers over an RGB base (cached background). Returns RGB."""
    im = base_rgb.convert("RGBA")
    for l in layers: im = Image.alpha_composite(im, l)
    return im.convert("RGB")

def word_pop(ss, center, words, t, start, font, color=(255, 255, 255), delay=0.09, dur=0.35, rise=26, stroke=0):
    """Words slide up + fade in one after another (staggered). Use instead of whole-line fades."""
    ws = [ss.tlen(w + " ", font) for w in words]; x = center[0] - sum(ws) / 2
    for i, (w, wd) in enumerate(zip(words, ws)):
        p = clamp(stagger(i, t, start, delay, dur))
        if p > 0: ss.text((x, center[1] + rise * (1 - p)), w, font, anchor="lm", stroke=stroke, fill=(*color, int(255 * p)))
        x += wd

# ------------------------------------------------------------------ motion blur (temporal sub-frame accumulation)
def blur_layer(render_layer, t, fps, shutter=180, samples=6):
    """render_layer(t) -> RGBA image of ONLY the moving elements. Averages `samples` sub-frames over the shutter window
    (180 deg = half a frame, centred on t). Keep text/static UI OUT of this layer so it stays sharp."""
    exp = (shutter / 360.0) / fps; acc = None
    for k in range(samples):
        im = np.asarray(render_layer(t + exp * ((k + 0.5) / samples - 0.5)).convert("RGBA"), dtype=np.float32)
        a = im[..., 3:4] / 255.0; pm = np.concatenate([im[..., :3] * a, a], axis=2)
        acc = pm if acc is None else acc + pm
    acc /= samples; a = acc[..., 3:4]
    rgb = np.where(a > 1e-4, acc[..., :3] / np.maximum(a, 1e-4), 0)
    return Image.fromarray(np.concatenate([rgb, a * 255], axis=2).clip(0, 255).astype(np.uint8), "RGBA")

def speed_px(pos_fn, t, fps):
    """Pixels moved in one frame by pos_fn(t)->(x,y). Use it to skip the (expensive) blur when < ~1.5 px/frame."""
    (x0, y0), (x1, y1) = pos_fn(t), pos_fn(t + 1.0 / fps); return math.hypot(x1 - x0, y1 - y0)

def auto_samples(px_per_frame, shutter=180, lo=4, hi=28):
    """Enough sub-frames that neighbouring samples are <= ~1.5 px apart (otherwise you see 'echo' ghosts instead of smooth blur)."""
    return int(max(lo, min(hi, math.ceil(px_per_frame * shutter / 360.0 / 1.5))))

# ------------------------------------------------------------------ transitions between two RGB frames
def transition(a, b, p, kind="slide", ease=ease_in_out, axis="x"):
    """kinds: slide (push), wipe, scale_fade, iris. p = 0..1 progress. One primary + one accent kind per video."""
    p = ease(p); w, h = a.size
    if kind == "slide":
        out = Image.new("RGB", (w, h))
        if axis == "x": o = int(w * p); out.paste(a, (-o, 0)); out.paste(b, (w - o, 0))
        else: o = int(h * p); out.paste(a, (0, -o)); out.paste(b, (0, h - o))
        return out
    if kind == "wipe":
        out = a.copy(); out.paste(b.crop((0, 0, max(1, int(w * p)), h)), (0, 0)); return out
    if kind == "scale_fade":
        s = 1 + 0.08 * p; ca, cb = a.crop((0, 0, w, h)), b
        z = a.resize((int(w * s), int(h * s)), Image.BILINEAR); x0, y0 = (z.width - w) // 2, (z.height - h) // 2
        return Image.blend(z.crop((x0, y0, x0 + w, y0 + h)), cb, p)
    if kind == "iris":
        S = 2; m = Image.new("L", (w * S, h * S), 0); r = p * math.hypot(w, h) / 2 * S
        ImageDraw.Draw(m).ellipse([w * S / 2 - r, h * S / 2 - r, w * S / 2 + r, h * S / 2 + r], fill=255)
        return Image.composite(b, a, m.resize((w, h), Image.LANCZOS))
    raise ValueError(kind)

# ------------------------------------------------------------------ YouTube-ready encoder
def open_encoder(path, w, h, fps, audio=None, crf=14, preset="slow"):
    """Pipe raw RGB frames in (proc.stdin.write(img.tobytes())). H.264 High, yuv420p, BT.709 tagged + converted,
    closed GOP of 2 s, capped at 12 Mbps, faststart, AAC 192k / 48 kHz. Matches YouTube's upload guidance."""
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-"]
    if audio: cmd += ["-i", audio]
    cmd += ["-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", preset, "-profile:v", "high",
            "-crf", str(crf), "-maxrate", "12M", "-bufsize", "24M", "-g", str(int(fps * 2)), "-bf", "2", "-x264-params", "open-gop=0",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-movflags", "+faststart"]
    if audio: cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest"]
    return subprocess.Popen(cmd + [path], stdin=subprocess.PIPE)
