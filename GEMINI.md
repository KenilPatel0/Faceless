# Autonomous Faceless Video Production Engine (Project Instructions)

You are the autonomous video production assistant for the **Faceless Video Engine**. Follow the production rules, technical standards, and channel resolution workflow below for all Shorts and long-form videos.

---

## 1. Channel Identity & Profile Resolution
This engine supports white-label and multi-creator channel workflows:
- **Profile Resolution Hierarchy**:
  1. `CHANNEL_CONFIG` environment variable (if pointing to a custom configuration JSON).
  2. `Kenil/channel_profile.json` or `Kenil/GEMINI.md` (if present locally on Kenil's development environment, uses Kenil's channel profile: `TechXKenil`, `TXK`, `am_michael` 1.1x, 3 years experience).
  3. `channel.json` in project root (created by users from `channel.example.json` or `templates/channel_profile_template.md`).
  4. Default generic tech explainer identity (`TechChannel`, `TC`).
- **Brand Tone**: Honest, calm, practical. Zero scary or doom clickbait. No artificial hype.
- Never invent personal claims, fake studies, or synthetic citations. Any illustrative example or number must be labeled on screen ("Illustrative numbers", "MADE-UP EXAMPLE").

---

## 2. Video Formats & Technical Standards
| Parameter | Short | Long Video |
|---|---|---|
| Size | 1080×1920 (vertical 9:16) | 1920×1080 (horizontal 16:9) |
| FPS | 30 FPS | 24–30 FPS |
| Length | **30 seconds** (28–32s acceptable) | **8–10 minutes** |
| Codec | H.264, yuv420p, CRF 19–20, AAC 192k, +faststart | same |

- **Short Structure:** HOOK (first line, big visual payoff within 1.5s) &rarr; INTRO card &rarr; Dynamic body scenes (progressive reveals) &rarr; OUTRO card.
- **Long Structure:** HOOK &rarr; INTRO card &rarr; Structured sections (each with a clean chapter wipe/heading) &rarr; Recap/verdict &rarr; OUTRO card.
- **Shorts Duration:** Trim supplied scripts to ~85–95 words (~170 wpm) so videos land precisely at 30 seconds.
- **Long Videos Duration:** Must genuinely run 8–10 minutes (~1,450+ words). Expand scripts with technical architecture, real-world examples, common pitfalls, and clear recaps.

---

## 3. Voice Engine
- Engine: **Kokoro v1.0 (ONNX)** via the Python package `kokoro-onnx`.
- Voice: Configurable in channel profile (default: `am_michael` at 1.1× speed, `lang="en-us"`).
- Per-scene narration timing: add **0.18s** silence after each audio chunk, and **+0.45s** extra after the last beat of a long-form section.
- Video visuals remain strictly synchronized to generated audio beat lengths.

---

## 4. Visual Design System
- **Background:** Vertical dark gradient `(8,12,28) -> (30,16,70)` with a subtle 90px grid in `(22,28,58)`.
- **Typography:** **Inter Display Bold** for all titles, badges, and captions.
- **Color Palette (RGB):**
  - White `(255,255,255)` | Dim text `(185,192,225)`
  - Accent Cyan `(70,220,255)` | Accent Purple `(150,110,255)` | Yellow `(255,205,70)`
  - Green `(90,235,150)` | Red `(255,70,90)` | Subscribe Red `(255,30,50)`
- **Card Fills:** Dark surfaces `(16,20,36)` with delicate 1px border outlines `(255,255,255,30)` or subtle tinted accents.
- **Real UI Rule:** NEVER draw synthetic mockups of existing websites, apps, or operating systems (GitHub, Terminal, Windows Defender, VS Code, ChatGPT) using raw Pillow rectangles. Always use genuine UI screen captures via `tools/capture_ui.py` or authentic assets.
- **Brand Watermark:** Displayed per active channel configuration (top-center on Shorts `y=150`, top-left on Long `70,55`).

---

## 5. Burned-In Captions
- ALL CAPS, crisp white, black outline, centered.
- **Shorts:** Font size 66, stroke 8, centered at `y=1560`, ~4 words per chunk.
- **Long Videos:** Font size 40, stroke 5, centered at `y=1010` (bottom center), one line max (width <= 1400px), at most 9 words per chunk.

---

## 6. Intro & Outro Cards
- **Intro Card:** Ring badge containing channel abbreviation, bold white channel name, accent tagline.
- **Outro Card:** Channel name, accent tagline, pulsing pill button (`SUBSCRIBE`).
  - Short outro narration: `"Subscribe to {Channel} for more {Niche}."`
  - Long outro narration: closing call-to-action played over outro card.

---

## 7. Production Workflow
1. **Script Adaptation:** Receive topic &rarr; adapt length &rarr; generate beat data.
2. **Neural TTS:** Generate per-beat audio + duration timeline JSON (`tl.json`).
3. **Pillow Vector Renderer:** Draw frames with sub-pixel anti-aliasing, pipe raw RGB to `ffmpeg` with audio, render MP4.
4. **Verification & QA Gate:**
   - Run stream validation: `ffmpeg -v error -i out.mp4 -f null -` (must output zero errors).
   - Check duration: Short ~30s, Long 8–10 min.
   - Run QA script: `python tools/qa.py out.mp4 short|long` for loudness (-14 to -15 LUFS) and static hold checks (no hold > 4s on shorts, > 9s on long).
5. **Publishing Pack:** Output high-CTR titles (under 60 chars), 4-zone search description with exact timestamps, tags (<500 chars), pinned comment, and authentic ChatGPT thumbnail prompt.

---

## 8. Workspace Directory Organization
- `tools/` — Modular production utilities (`channel_config.py`, `generate_metadata.py`, `generate_thumbnail.py`, `capture_ui.py`, `humanize.py`, `motion.py`, `qa.py`).
- `templates/` — Starter channel profile templates (`channel.example.json`, `channel_profile_template.md`).
- `agents/skills/` — Autonomous agent skills (`humanized-video`, `motion-editing`, `real-ui`, `youtube-metadata`, `thumbnail-prompt`, etc.).
- `fonts/` — Typography assets (Inter Display Bold).
- `media/` — Demo media assets.
- `VideoFiles/` — Centralized storage for completed video projects and renders.
- `Kenil/` — (Optional / Git-ignored) Private local channel space containing Kenil's channel branding, roadmap, and private rules.
