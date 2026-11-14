# Human-Crafted Video Design & Motion Architecture
**Faceless Video Engine — Visual Standards, Real-World Assets & High-Retention Shorts**

---

## 1. The Anti-AI Editing Manifesto

Viewers instantly recognize and swipe away from generic "AI-generated" video templates (flat saturated neon rectangles, procedural line grids, robotic whole-line subtitle fades, and cheesy sci-fi holograms). 

To achieve high retention, authority, and monetization safety, every video produced by the **TechXKenil Engine** must look and feel **meticulously hand-edited by a senior tech editor**:

```
[ AI-Generated / Template Video ]                 [ TechXKenil Human-Craft Standard ]
-----------------------------------------         -----------------------------------------
• Fake Pillow shapes imitating real apps          • Authentic Real UI (Playwright & OS captures)
• Cheesy sci-fi holograms & glowing brains        • Tactile real-world objects & editorial photos
• Flat, harsh 2-color linear gradients            • Cinematic obsidian atmospheric depth & grain
• Static frames held for 8+ seconds               • 1.5–2.5s rapid visual progression & camera drift
• Monolithic whole-sentence subtitles             • Dynamic karaoke word-pop with active bounce
• Predictable, mechanical linear motion           • Physics-based spring overshoot & Bezier arcs
```

---

## 2. Pillar I: Real-World Assets & Zero-Synthetic Mockup Rule

When an explanation refers to a real-world concept (an operating system, app, framework, hardware component, physical object, nature, or game), **synthetic procedural drawings are strictly prohibited**.

### 2.1 Software, Developer Tools & Web Apps
* **Iron Rule:** NEVER draw fake terminal windows, mock GitHub cards, or synthetic VS Code editors using Pillow rectangles.
* **Pipeline:**
  - Real Terminal: Captured via `tools/capture_ui.py terminal --cmd "<command>" --4k` (authentic SF Mono / Inter typography, macOS traffic lights, deep translucent dark mode).
  - Real Websites (GitHub, HuggingFace, Docs): Captured via `tools/capture_ui.py web --url "<url>" --4k` using headless Chromium at Retina 2× device scale factor.
  - Authentic App Window Framing: Place captured assets inside floating glassmorphic windows with subtle 1px border `rgba(255,255,255,0.12)`, 24px corner radius, and realistic drop shadow ($\sigma=32\text{px}$, 35% opacity).

### 2.2 Physical Hardware & Real-World Analogies
* When explaining technical hardware architecture (e.g., Apple M-series Unified Memory, NVIDIA VRAM, DDR5 bus speeds, chip dies, or server racks):
  - Use high-resolution, genuine editorial photography of the actual silicon chip, motherboard, or wafer.
  - Apply `tools/cutout.py` to isolate the hardware component on a transparent layer with a subtle white sticker edge or soft shadow.
* When using real-world analogies (e.g., memory bandwidth like an 8-lane highway vs a narrow pipe; quantization like audio MP3 compression or a book summary):
  - Use authentic high-definition imagery or video clips of the real object (real highways, real printed books, real vinyl records). Never use generic AI cartoon clipart.

### 2.3 Games, OS Dialogs & Nature
* Authentic Game Benchmarks: Real gameplay clips or benchmark HUD overlays (e.g. Cyberpunk 2077 benchmark metrics, RT cores) when comparing GPU performance.
* Authentic System Dialogs: Genuine Windows Defender, macOS Gatekeeper, or Linux bash prompts.

---

## 3. Pillar II: The TechXKenil Cinematic Background System

The background must never feel like a cheap procedural computer grid. For an **AI • Tech • Code** channel, the environment should evoke a **high-end developer workstation at dusk**—moody, deep, tactile, and cinematic.

### 3.1 Color Palette & Atmospheric Depth
Instead of a single harsh linear gradient, the canvas uses a **3-Layer Depth Composite**:

1. **Layer 0 (Base Obsidian Surface):**
   - Deep Obsidian Core: `RGB(10, 13, 20)` (`#0a0d14`).
   - Dual-Stop Ambient Radial Lighting:
     - Top-Left Glow: Deep Sapphire / Slate `(20, 32, 60)` with soft 1200px radial falloff.
     - Bottom-Right Accent: Subtle Amethyst / Twilight `(32, 22, 54)` with soft 1000px radial falloff.
2. **Layer 1 (Subtle Micro-Texture & Film Grain):**
   - 2.5% organic Gaussian monochrome noise across the entire background.
   - **Crucial Purpose:** Eliminates digital color banding on YouTube after video re-encoding, giving dark gradients an expensive, 35mm film-like roll-off.
3. **Layer 2 (Technical Ambient Elements):**
   - Ultra-subtle dotted matrix or isometric grid (points at 160px spacing, opacity 12–15%, color `(50, 65, 100)`).
   - Soft out-of-focus background bokeh (blurred floating hex particles or dim mono code comments at 8% opacity).
4. **Layer 3 (Vignette Roll-off):**
   - 15% edge darkening with smooth cosine roll-off to draw the viewer's eyes irresistibly toward the center focal elements.

### 3.2 Continuous Organic Lighting Drift
The ambient light spots do not sit perfectly frozen. Over the course of a scene, the light centers gently oscillate using dual-sine harmonic drift ($0.05\text{ Hz}$, amplitude $\pm 15\text{px}$), creating the sensation of subtle room lighting alive behind the content.

---

## 4. Pillar III: Ultra-High-Retention Shorts Design (9:16 Vertical)

YouTube Shorts viewers make the decision to stay or swipe within **1.2 to 1.5 seconds**. Every millisecond must be engineered for high visual velocity, retention, and clarity.

```
+-------------------------------------------------------------+
|                      TOP BRAND SAFE ZONE                    |
|   Watermark / Category Pill (y: 260px - 380px)              |
+-------------------------------------------------------------+
|                                                             |
|                                                             |
|                   DYNAMIC HERO STAGE                        |
|   - Real UI App Captures (scaled to fit width <= 1840px)   |
|   - High-contrast visual progression (every 1.5 - 2.5s)     |
|   - Punchy metrics, comparison cards & tactile cutouts      |
|                                                             |
|                                                             |
+-------------------------------------------------------------+
|                  180px SUBTITLE CLEARANCE                   |
+-------------------------------------------------------------+
|                DYNAMIC KARAOKE CAPTION ZONE                 |
|   - Centered at y = 3120px (4K) / y = 1560px (1080p)        |
|   - Max 3-4 words per chunk                                 |
|   - Active spoken word: Electric Yellow / Cyan with bounce  |
+-------------------------------------------------------------+
|             BOTTOM YOUTUBE SHORTS UI SAFE ZONE              |
|   (Reserved for YouTube Title, Channel & Audio Info)        |
+-------------------------------------------------------------+
```

### 4.1 The 1.5-Second Payoff Hook
* The first frame must contain:
  1. A **bold visual slam** (e.g. a sliced credit card or a real 48 tok/s terminal running).
  2. A high-contrast hero badge (`$0 AI SETUP` or `STOP PAYING`).
  3. Spoken hook line synchronized to the visual payoff within $\le 1.2\text{s}$.

### 4.2 The 1.5–2.5s Visual Progression Rule (Never Static)
To guarantee high retention and zero viewer fatigue, the screen MUST introduce a new visual event every **1.5 to 2.5 seconds**:
* **Technique A (Staggered Step Reveal):** Reveal cards or code blocks one-by-one as the voice mentions them.
* **Technique B (Focal Punch-In):** Apply a quick 6–8% punch-in scale on key spoken numbers or terms.
* **Technique C (Hero Highlighting):** Keep previous cards on screen, but softly dim them to 40% opacity while the active spoken card glows with an Electric Cyan or Amber border.
* **Technique D (Dynamic Cut):** Cut cleanly between high-angle overview and extreme close-up on authentic code/metrics.

### 4.3 Dynamic Karaoke Captions (Word-Pop)
* **Chunk Length:** Strictly **3 to 4 words maximum** per chunk. Never display two long lines of text on a Short.
* **Typography:** Inter Display Bold, font size 132 (at 4K) / 66 (at 1080p), heavy black stroke (16px / 8px).
* **Word Synchronization:**
  - Inactive words: Crisp Pure White `(255, 255, 255)`.
  - Active spoken word: Illuminates instantly in **Electric Yellow `(255, 205, 70)`** or **Electric Cyan `(70, 220, 255)`**.
  - Word arrival triggers a subtle $1.06\times$ scale bounce (`pulse()`) that settles in 100ms.

---

## 5. Pillar IV: Human Motion & Physics Craft

Motion in human-edited videos behaves like physical objects with weight, inertia, and momentum:

### 5.1 Physics Over Linear Math
* **Entrances (`spring`):** Natural dampening with 3–4% overshoot settling in 0.5s ($f=2.2\text{ Hz}, \zeta=0.72$).
* **Cursor Motions (`bezier_point`):** Real human hands move in smooth arcs, never straight laser lines. Cursors follow quadratic or cubic Bezier trajectories.
* **Breathing Micro-Motion (`smooth_float`):** Resting cards maintain gentle harmonic floating ($\pm 3.5\text{px}$ at $1.2\text{ Hz}$) so the video never triggers a static hold QA flag.

### 5.2 Editing Rhythm: J-Cuts & Audio-Visual Lead
* **Visual Leads Audio (0.15s Lead):** The eye processes visual information faster than the ear processes speech. Visual cards and highlights appear **0.12–0.18s before the spoken word**.
* **J-Cuts on Scene Changes:** Sound effects (pop, whoosh, click) and the next scene's visual background begin 0.15s before the previous sentence's audio tail fades out.

---

## 6. Implementation Roadmap

| Phase | Milestone | Deliverable |
|---|---|---|
| **Phase 1** | **Cinematic Background Shader** | Implement multi-stop radial atmospheric lighting + 2.5% film grain in `tools/render_core.py`. |
| **Phase 2** | **Real Asset Library Integration** | Integrate high-DPI web/terminal captures and transparent hardware cutouts into standard scene templates. |
| **Phase 3** | **Dynamic Karaoke Shorts Engine** | Build `render_karaoke_shorts()` in `tools/render_core.py` with word-by-word active highlight and 1.06x bounce. |
| **Phase 4** | **Humanized Pilot Short (9:16 4K60)** | Produce a 30-second vertical Short demonstrating real UI, dynamic karaoke, rapid 2s visual switching, and organic background depth. |
| **Phase 5** | **Dual-Space Sync & Verification** | Update public skills (`humanized-video`, `motion-editing`, `real-ui`) and sync to `TechXKenil/`. |
