---
name: generate-thumbnail
description: Generate high-CTR (click-through rate) 1280x720 YouTube thumbnails for tech, coding, and faceless channels using free AI image tools and automated Python/Pillow typography. Covers thumbnail psychology, safe zones, mobile contrast, and automated thumbnail creation.
---

# generate-thumbnail — High-CTR YouTube Thumbnail Generation Engine

A complete guide and automated tool for producing high-converting 1280×720 (16:9) YouTube thumbnails for tech, AI, and faceless video channels. Combines free AI visual generation with deterministic, brand-consistent typography.

---

## 1. The Anatomy of a High-CTR Tech Thumbnail

Based on YouTube algorithm research and retention analytics across top tech creators (Veritasium, Fireship, ColdFusion):

### The Rule of Three Visual Elements (Max)
Viewers browse YouTube on mobile screens where thumbnails appear smaller than a postage stamp. If a thumbnail has more than 3 distinct visual elements, the human eye cannot parse it in the critical 1.5-second browsing window.

1. **Element 1: High-Contrast Focal Graphic**
   - A single striking visual object: glowing microchip, stopwatch, code block, or comparative icon.
2. **Element 2: Ultra-Short Text Hook (2 to 4 words max)**
   - Bold, high-contrast sans-serif font (Inter Display Bold).
   - **Never repeat the video title.** The thumbnail text should provoke curiosity or present a paradox that complements the title.
     - *Title:* "How AI Answers in Milliseconds"
     - *Thumbnail Text:* "HOW SO FAST?" or "140 TRILLION OPS"
3. **Element 3: Tension / Stat Chip**
   - A pill badge displaying an extreme number or metric (e.g. `15 ms`, `3.35 TB/s`, `0.01%`).

---

## 2. YouTube Safe Zones (Crucial)

```
+--------------------------------------------------------------+
| [Kicker Badge]                                 [Channel Tag] |
|                                                              |
|   BIG HOOK TEXT               ( FOCAL VISUAL )               |
|   LINE TWO                     Glowing Chip /                |
|                                Stopwatch / Icon              |
|   [STAT PILL BADGE]                                          |
|                                             +--------------+ |
|                                             | YOUTUBE TIME | |
|                                             | BADGE 05:03  | |
+--------------------------------------------------------------+
```

- **Bottom-Right Corner (180px × 60px):** **NEVER** put critical text, faces, or numbers here. YouTube permanently covers this area with the video duration badge (`05:03` / `SHORTS`).
- **Outer Padding:** Keep all essential elements at least 40px away from the edges to avoid cropping on mobile carousel layouts.

---

## 3. High-Converting Color Palettes

Tech and AI videos perform highest with **dark background + vivid electric accents**:

| Role | Color | Hex / RGB | Purpose |
|---|---|---|---|
| **Background Dark** | Obsidian Navy | `#080c1c` / `(8, 12, 28)` | Provides infinite depth for neon lights |
| **Primary Text** | Crisp White | `#ffffff` / `(255, 255, 255)` | Maximum readability at small mobile sizes |
| **Accent Glow** | Electric Cyan | `#46dcff` / `(70, 220, 255)` | High tech, AI, latency, speed |
| **Hook Highlight** | Golden Yellow | `#ffcd46` / `(255, 205, 70)` | Draws the eye first |
| **Danger / Alert** | Coral Red | `#ff465a` / `(255, 70, 90)` | Warnings, errors, bugs, comparison |
| **Badge Fill** | Deep Violet / Teal | `#1e103c` / `#0f3c50` | Contained pill buttons |

---

## 4. Free Tooling Stack (Zero Cost, No API Keys)

1. **Free AI Generation (Pollinations.ai):**
   - URL: `https://image.pollinations.ai/prompt/{prompt}?width=1280&height=720&model=flux&nologo=true`
   - Unlimited, free, zero sign-up, powered by Flux and SDXL.
   - Ideal for generating background artwork, 3D microchips, circuit boards, and futuristic abstract patterns.
2. **Deterministic Typography (Python + Pillow):**
   - AI generators consistently fail at spelling and aligning exact text.
   - The included tool `tools/generate_thumbnail.py` layers pixel-perfect stroked text using **Inter Display Bold** on top of the AI artwork.
3. **Procedural Fallback:**
   - When offline or when a clean vector graphic look is preferred, the script renders the signature 90px grid, gradient, and radial cyber glow with zero external dependencies.

---

## 5. How to Generate Thumbnails with the CLI Tool

From the project root:

```bash
# 1. 100% Procedural Branded Thumbnail (Clean Tech look)
.venv/bin/python tools/generate_thumbnail.py \
  --line1 "HOW AI ANSWERS" \
  --line2 "IN MILLISECONDS" \
  --badge "THE HARDWARE SECRET" \
  --stat "140 TRILLION OPS" \
  --out youtube/videos/thumb_procedural.png

# 2. AI-Assisted Background (Photorealistic 3D Chip / Flux artwork)
.venv/bin/python tools/generate_thumbnail.py \
  --line1 "HOW AI ANSWERS" \
  --line2 "IN MILLISECONDS" \
  --badge "FASTER THAN A BLINK" \
  --stat "70B PARAMS · 15ms" \
  --ai "futuristic glowing NVIDIA AI microchip with cyan circuits and holographic matrices" \
  --out youtube/videos/thumb_ai.png
```

---

## 6. Prompt Engineering Guide for Tech Backgrounds

When passing `--ai "<prompt>"`, follow this structure:
```text
"<central subject>, dark cyberpunk lighting, neon cyan and amber accents, volumetric studio lighting, deep obsidian background, octane render style, minimalist composition, no text"
```

### Proven Examples:
- **Algorithms / Speed:** `"glowing stopwatch floating beside neon silicon data highways, deep blue dark background, octane render"`
- **Datacenter / Cloud:** `"massive glowing futuristic server rack array with neon teal fiber optic cables, cinematic perspective"`
- **Coding / Bugs:** `"futuristic hologram terminal showing glowing code matrices with red warning error pulses"`
- **AI Models / Neural Networks:** `"glowing 3D synaptic neural network brain connected to microchip circuits, volumetric lights"`

