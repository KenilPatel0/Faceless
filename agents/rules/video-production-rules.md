# Autonomous Faceless Video Production Rules

You are the video production agent for this autonomous faceless video production engine. Follow every rule below for all Shorts and long videos so production stays consistent in quality, timing, design, voice, and tone.

---

## 1. Channel Identity & Configuration
- Channel identity is loaded dynamically via `tools/channel_config.py`.
- If a custom channel profile is present (`Kenil/channel_profile.json`, `channel.json`, or environment variables), the engine adopts that identity (name, badge, intro/outro, narrator voice).
- If no profile is configured, default tech explainers settings apply.
- Tone: Honest, calm, practical. Zero scary or doom clickbait. No hype.
- Never invent personal claims, fake studies, or synthetic citations. Any illustrative example/number must be labeled on screen ("Illustrative numbers", "MADE-UP EXAMPLE").

---

## 2. Video Formats & Technical Standards
| Parameter | Short | Long Video | 4K UHD Standard |
|---|---|---|---|
| Canvas Size | 1080×1920 (9:16) | 1920×1080 (16:9) | **3840×2160** (16:9) / **2160×3840** (9:16) |
| Target FPS | 30 FPS / 60 FPS | 24–30 FPS / 60 FPS | **60.0 FPS** (fluid motion, $\Delta t = 16.67\text{ms}$) |
| Target Length | **30 seconds** (28–32s) | **8–10 minutes** | same |
| Codec | H.264 / QSV / NVENC, AAC 192k, +faststart | same | Unlocks YouTube VP09/AV01 premium bitrate |

- **Short Structure:** HOOK (first line, big visual payoff <= 1.5s) &rarr; INTRO card &rarr; Body scenes (dynamic micro-motion) &rarr; OUTRO card.
- **Long Structure:** HOOK &rarr; INTRO card &rarr; Content sections (each with chapter heading) &rarr; Recap/verdict &rarr; OUTRO card.
- **Narration Pace:** ~160–180 spoken words/min. Expand or trim scripts as required to maintain target durations without unnatural speedups.

---

## 3. Voice Engine
- Engine: **Kokoro v1.0 (ONNX)** via the Python package `kokoro-onnx`.
- Voice: Configurable per channel (default `am_michael` at 1.1x speed, `lang="en-us"`).
- Per-scene narration timing: add **0.18s** silence after each audio chunk, and **+0.45s** extra after the last beat of a long-video section.
- Scene length matches audio length so visuals stay perfectly synchronized.

---

## 4. Visual Design System
- **Background:** Vertical dark gradient `(8,12,28) -> (30,16,70)` with subtle 90px grid lines in `(22,28,58)`.
- **Typography:** Inter Display Bold for high-contrast crisp readability.
- **Palette (RGB):**
  - White `(255, 255, 255)` | Dim text `(185, 192, 225)`
  - Cyan `(70, 220, 255)` | Purple `(150, 110, 255)` | Yellow `(255, 205, 70)`
  - Green `(90, 235, 150)` | Red `(255, 70, 90)` | Subscribe Red `(255, 30, 50)`
- **Card Fills:** Sleek dark fills `(16, 20, 36)` with delicate 1px borders `(255, 255, 255, 30)` or subtle tinted accents.
- **Real UI Rule:** NEVER draw fake or synthetic mockups of existing websites, apps, or operating systems using raw Pillow rectangles. Always use genuine UI screen captures via `capture_ui.py` or authentic assets.

---

## 5. Captions
- ALL CAPS, white, black stroke outline, centered.
- **Shorts:** Size 66, stroke 8, centered at `y=1560`, about 4 words per chunk.
- **Long Videos:** Size 40, stroke 5, centered at `y=1010` (bottom center), one line max (width <= 1400px), at most 9 words per chunk.

---

## 6. QA Gate & Verification
Before delivering any video:
1. Validate MP4 stream: `ffmpeg -v error -i out.mp4 -f null -` must print zero errors.
2. Check duration: Short ~30s, Long 8–10 min.
3. Mastered loudness: Target -14 to -15 LUFS integrated via `master()`.
4. Inspect contact sheet for clipped text, overlapping elements, or static holds (>4s on Shorts, >9s on Long).

---

## 7. Outro Conversion & Safe Area Clearance
- **Subscribe Button Transition:** The outro card displays a red `(255, 30, 50)` `"SUBSCRIBE"` pill button. An authentic cursor glides in on a Bezier curve, clicks with a pulse and ripple ring exactly as the narration says "subscribe", and the button converts into emerald green `(35, 195, 110)` `"✓ SUBSCRIBED!"`.
- **Vertical Clearance:** Content bounds must strictly stay above `y = 915px`, reserving an 80px safe buffer above burned-in captions centered at `y = 1010`.
- **Harmonic Anti-Freeze Micro-Motion:** Active cards utilize subtle harmonic oscillations (`smooth_float` +/-3.5px) to maintain visual vitality and eliminate static holds.

