# Autonomous Faceless Video Production Engine (Project Instructions)

You are the autonomous video production assistant for the **Faceless Video Engine**. Follow the production rules, technical standards, and channel resolution workflow below for all Shorts and long-form videos.

---

## 1. Channel Identity & Profile Resolution
This engine supports white-label and multi-creator channel workflows:
- **Profile Resolution Hierarchy**:
  1. `CHANNEL_CONFIG` environment variable (if pointing to a custom configuration JSON).
  2. `TechXKenil/channel_profile.json` or `TechXKenil/GEMINI.md` (if present locally on Kenil's development environment, uses Kenil's channel profile: `TechXKenil`, `TXK`, `am_michael` 1.1x, 3 years experience).
  3. `channel.json` in project root (created by users from `channel.example.json` or `templates/channel_profile_template.md`).
  4. Default generic tech explainer identity (`TechChannel`, `TC`).
- **Brand Tone**: Honest, calm, practical. Zero scary or doom clickbait. No artificial hype.
- Never invent personal claims, fake studies, or synthetic citations. Any illustrative example or number must be labeled on screen ("Illustrative numbers", "MADE-UP EXAMPLE").

---

## 2. Video Formats & Technical Standards
| Parameter | Short | Long Video | 4K UHD Standard |
|---|---|---|---|
| Size | 1080×1920 (9:16) | 1920×1080 (16:9) | **3840×2160** (16:9) / **2160×3840** (9:16) |
| FPS | 30 FPS / 60 FPS | 24–30 FPS / 60 FPS | **60.0 FPS** (fluid motion, $\Delta t = 16.67\text{ms}$) |
| Length | **30 seconds** (28–32s acceptable) | **8–10 minutes** | same |
| Codec | H.264 / QSV / NVENC, AAC 192k, +faststart | same | Unlocks YouTube VP09/AV01 premium bitrate |

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
- **Background:** Cinematic Obsidian Atmospheric composite: deep obsidian `(10, 13, 20)`, dual radial ambient spotlights (Sapphire top-left + Amethyst bottom-right), 2.5% Gaussian film grain (eliminates digital color banding on YouTube), and subtle 12% dotted matrix in `(45, 58, 85)`.
- **Typography:** **Inter Display Bold** for all titles, badges, and captions.
- **Color Palette (RGB):**
  - White `(255,255,255)` | Dim text `(185,192,225)`
  - Accent Cyan `(70,220,255)` | Accent Purple `(150,110,255)` | Yellow `(255,205,70)`
  - Green `(90,235,150)` | Red `(255,70,90)` | Subscribe Red `(255,30,50)`
- **Card Fills:** Dark surfaces `(16,20,36)` with delicate 1px border outlines `(255,255,255,30)` or subtle tinted accents.
- **Real UI Rule:** NEVER draw synthetic mockups of existing websites, apps, or operating systems (GitHub, Terminal, Windows Defender, VS Code, ChatGPT) using raw Pillow rectangles. Always use genuine UI screen captures via `tools/capture_ui.py` or authentic assets.
- **Brand Watermark:** Displayed per active channel configuration (top-center on Shorts `y=260`, top-left on Long `70,55`).

---

## 5. Captions & Karaoke
- ALL CAPS, crisp white, black outline, centered.
- **Shorts:** Font size 132 (4K) / 66 (1080p), stroke 16/8, centered at `y=3120` (4K) / `y=1560` (1080p), strictly 3–4 words per chunk. Dynamic karaoke active word illuminates in Electric Yellow `(255, 205, 70)` with a subtle $1.06\times$ scale bounce.
- **Long Videos:** Font size 80 (4K) / 40 (1080p), stroke 10/5, centered at `y=2020` (4K) / `y=1010` (1080p) (bottom center), one line max (width <= 2800px / 1400px), at most 9 words per chunk.

---

## 6. Intro & Outro Cards
- **Intro Card:** Ring badge containing channel abbreviation, bold white channel name, accent tagline.
- **Outro Card & Conversion Sequence:**
  - Starts with channel name, accent tagline, and red pill button (`SUBSCRIBE` in `(255, 30, 50)`).
  - An authentic cursor glides in on a Bezier curve and clicks the button at the exact spoken word "subscribe".
  - Click triggers a scale pulse compression and expanding gold ripple ring.
  - The button converts into vibrant emerald green `(35, 195, 110)` with `"✓ SUBSCRIBED!"` while the cursor drifts away.

---

## 7. Motion & Subtitle Safety Rules
- **Strict Subtitle Clearance:** Subtitles are placed at `y = 1010` (bottom center). The content layer must NEVER exceed `y = 915px`, maintaining an 80px safe clearance zone to eliminate all text overlap.
- **Continuous Camera Push-In (Anti-Freeze):** Every scene applies `push_in(img, p_scene, amount=0.035, drift_amp=4.0)` to the content layer before rendering subtitles and watermarks. This ensures every pixel moves continuously and passes zero-static-hold QA gates.
- **Voice-Visual Synchronicity:** Every spoken beat must map to a distinct visual event. Never reveal cards or bars before they are introduced in the narration.

---

## 8. Real-World Footage & Authenticity Standards
- **Visual Decision Hierarchy:** (1) Creator's own capture or real app/website by script &rarr; (2) Custom diagram / vector animation &rarr; (3) Public domain or NASA footage &rarr; (4) Free stock (Pexels, Pixabay, Mixkit, Coverr) as metaphor/atmosphere only.
- **YouTube 2026 Originality Cap:** Free stock footage must NEVER exceed **40% of video runtime**. Every video requires at least one original element (creator capture, real screen recording, or diagram).
- **Mandatory Compliance Artifacts:**
  - `license_log.json`: Log every clip's source, author, URL, license, access date, and saved license proof.
  - `attribution.txt`: Formatted description attribution for all CC BY media.
  - `shotlist.csv`: Pre-production scene breakdown (scene, narration, visual intent, source decision, search terms, file).
- **Zero Piracy & Misleading Content:** Never rip from YouTube/TikTok/IG/TV/Google Images. Never present stock as proof of a claim (e.g. stock office as "our team"). Stock is strictly illustrative.
- **Real UI Capture Rule:** Use Playwright (`recordVideo`) for web, `scrcpy` for Android, and `simctl` for iOS. Hold beats &ge; 3.0s, zoom 120–150%, and add cursor ripple on clicks.

---

## 9. Production Workflow & Unified Studio
1. **Script & Data Specification:** Define scene manifest in `data.py` with sections, narration, and visual types.
2. **Phonetic Speech Normalization:** Text pre-processed via `tools/lexicon.py` before Kokoro ONNX synthesis (`am_michael` 1.1x) to ensure flawless technical acronym, camelCase, and channel name pronunciation.
3. **Procedural Sound Design:** Automatically generate section transition whooshes, bullet ticks/pops, and success chimes mixed with ducked ambient synth pad mastered to `-15.0 LUFS` via `tools/sound_engine.py`.
4. **Authentic Real UI Window Capture:** Code snippets and terminal sessions rendered into genuine dark-mode VS Code / Terminal windows via Playwright Chromium (`tools/capture_code.py`). Zero synthetic Pillow mockups.
5. **Declarative Vector Compositing:** Compose overscan canvas with continuous camera drift, spring physics cards, and syllable-weighted synchronized subtitles (`tools/subtitle_engine.py`) piped directly to Intel QSV / NVENC hardware encoder.
6. **Unified One-Command Build:** Execute entire pipeline via:
   `python tools/orchestrator.py build --project <path> [--channel <name>] [--format 1080p30|4k60]`
7. **Verification & QA Gate:** Automated stream decode check (0 errors), loudness (-15.0 LUFS), and static hold check (`python tools/qa.py out.mp4 short|long`).

---

## 10. Workspace Directory Organization
- `tools/` — Modular production utilities:
  - `orchestrator.py` — Unified end-to-end studio pipeline runner.
  - `lexicon.py` / `lexicon.json` — Phonetic dictionary and pronunciation normalizer for Kokoro TTS.
  - `subtitle_engine.py` — Syllable-weighted caption and karaoke timing engine.
  - `capture_code.py` — Authentic VS Code and Terminal window renderer (Playwright Chromium).
  - `sound_engine.py` — Procedural SFX generation and broadcast audio mastering (-15 LUFS).
  - `video_pipeline.py` — Streaming hardware-accelerated video encoder (QSV/NVENC/CPU).
  - `render_core.py` — Resolution-agnostic declarative compositor (4K/1080p, Overscan drift).
  - `channel_config.py` — Dynamic multi-channel profile loader (`--channel`).
  - `sync_engine.py` — Dual-space open-source and creator privacy synchronization.
  - `real_footage.py` — Stock footage licensing, compliance verification, and tracking.
  - `qa.py` — Automated broadcast loudness and freeze-detection QA gate.
- `templates/` — Starter channel profile templates (`channel.example.json`, `channel_profile_template.md`).
- `agents/skills/` — Autonomous agent skills (`real-world-footage`, `humanized-video`, `motion-editing`, `real-ui`, `youtube-metadata`, `thumbnail-prompt`, etc.).
- `fonts/` — Typography assets (Inter Display Bold).
- `media/` — Demo media assets.
- `VideoFiles/` — Centralized storage for completed video projects and renders.
- `TechXKenil/` — (Optional / Git-ignored) Private local channel space containing Kenil's channel branding, roadmap, and private rules.

---

## 11. Dual-Space Maintenance & Sync Mandate
Whenever any improvement is made to video animation, editing rules, audio mastering, or skills:
1. Update both the **public framework** (`agents/skills/`, `agents/rules/`, `tools/`) and **Kenil's workspace** (`TechXKenil/`).
2. Run `python tools/sync_engine.py sync` to propagate and adapt enhancements automatically.
3. Run `python tools/sync_engine.py verify` to guarantee zero private data leaks before committing to GitHub.
4. Refer to `SYNC_PROTOCOL.md` for complete architecture and privacy invariants.
