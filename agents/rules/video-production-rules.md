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

## 4. Visual Design System: Consistent Anchor & Topic-Specific Visual Worlds
- **Brand Consistency Rule (The Anchor):** ONLY the channel **Intro Card** and **Outro Card** are fixed and standardized across all videos for instant channel recognition and conversion.
- **Story-Driven Visual World Flexibility:** Apart from the intro and outro, the entire body of each video (background environment, color palette, card styling, and layout geometry) MUST be dynamically tailored to the specific topic. Never force every video into the exact same background or color theme.
- **Thematic Background Library (Topic-Specific):**
  - `blueprint_grid`: Technical architectural grid on deep indigo/slate gradient (for systems design, agent loops, backend architectures).
  - `silicon_interposer`: Integrated circuit/PCB traces, microgrid, bus lanes (for GPU hardware, VRAM, silicon, inference speed).
  - `cyber_terminal`: CRT scanline / phosphor matrix console atmosphere (for cybersecurity, Linux, terminal tooling).
  - `studio_gradient`: High-end smooth midnight-to-charcoal radial gradient (for modern developer tools, SaaS overviews).
  - `minimal_dark`: Ultra-clean graphite matte canvas with subtle perimeter guidelines (for clean code, algorithm tutorials).
  - `obsidian_atmospheric`: Deep obsidian with dual ambient spotlights and film grain (for cinematic technical documentaries).
  - `topic_custom`: Bespoke procedural visual atmosphere tailored directly to the video's script and story.
- **Typography:** Inter Display Bold for high-contrast crisp readability.
- **Dynamic Color Palettes:** Base accent color chosen per video theme (e.g. Electric Cyan, Matrix Emerald, Amber Orange, Neon Purple, Crimson Red, Royal Sapphire).
- **Card Fills & Surfaces:** Tailored to the theme (frosted glass, solid dark cards, blueprint bordered panels, or terminal frames).
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

