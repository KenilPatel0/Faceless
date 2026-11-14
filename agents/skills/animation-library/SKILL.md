---
name: animation-library
description: TechXKenil 2026 Animation Library and Prompt-to-Animation Decision Engine. Classifies script beats into 14 semantic categories and selects verified typography (T1-T8), explainer (E1-E11), camera/transition (C1-C8), and format (F1-F5) techniques based on research-backed retention rules.
---

# TechXKenil Animation Library & Prompt-to-Animation Decision Engine

Operational guide for autonomous agents producing TechXKenil Shorts and Long-Form Engineering Documentaries.

---

## 1. Core Principles (2026 Industry Baseline)
1. **Text is the Main Character:** Kinetic typography carries muted comprehension (Shorts = T1 karaoke word-highlight; Long = T2 two-line sentence captions).
2. **Authenticity over Polish:** Atmospheric obsidian dark `(8, 12, 28)` + 90px blueprint grid + genuine window captures (`capture_code.py`, `capture_ui.py`). Zero synthetic rectangles or fake mockups.
3. **Retention Anchors Every 2–3s (Shorts) / 6s (Long):** Purposeful visual event on spoken beats (bold keyword, punch-in, diagram build step, card slide).
4. **Zero-Static-Hold Mandate:** Continuous C1 slow push-in (`push_in(img, p, 0.035)`) covers all scenes so no pixel stays completely stationary.
5. **Honesty Gate:** No synthetic statistics or unverified benchmark numbers. Any numeric stat (T6/E5) requires an on-screen source annotation or must be rewritten qualitatively using T3.

---

## 2. Catalog Taxonomy (Registry IDs)

### 2.1 T: Typography & Captions
- **T1 Word-Highlight Captions (Karaoke):** Active word illuminates in Electric Yellow `(255, 205, 70)` with subtle $1.06\times$ scale bounce. *Baseline for all Shorts.*
- **T2 Two-Line Sentence Captions:** Bottom center, 40px/80px, at most 9 words per chunk, maintains $\ge 80\text{px}$ safe clearance from content. *Baseline for Long-form.*
- **T3 Kinetic Headline (Hero Text):** 1–5 big words snapping in with overshoot ease-out. Used for hooks, key claims, section payoffs.
- **T4 Keyword Emphasis:** Transient scale-pop ($1.15\times$) or accent cyan glow on the single most crucial word of a sentence.
- **T5 Typewriter / Terminal Text:** Monospace code or terminal typing with cursor jitter at $\sim 18\text{ cps}$.
- **T6 Stat Counter:** Numeric counter up/down with unit. *Honesty gate applies: requires verified source field.*
- **T7 Chat / Message UI:** Staggered conversational bubbles with typing dots for prompts and AI responses.
- **T8 Callout Label / Lower-Third:** Compact label pill with vector pointer line naming architectural components.

### 2.2 E: Explainer Visuals
- **E1 Line-Draw / Whiteboard Reveal:** Supersampled $2\times$ vector stroke reveals for definitions and core conceptual models.
- **E2 Diagram Build (Nodes & Arrows):** Staggered 80–120ms node entry, 400–600ms arrow drawing, active glow state machines.
- **E3 Split-Screen Comparison (A vs B):** Synchronized side-by-side attribute comparison with clean verdict banner.
- **E4 Numbered Cards (Listicle):** Step number + title card sliding into an active progress stack.
- **E5 Chart Reveal:** Bar/line data growth with key milestone callout. *Honesty gate applies.*
- **E6 Code View with Diff / Highlight:** Dark-mode VS Code window with green additions, red removals, and line spotlighting.
- **E7 Real UI / Screen Recording:** Authentic Chromium/Playwright or OS screen capture with Bezier cursor path and click ripples.
- **E8 Search / Prompt Box Animation:** Realistic input prompt bar typing out queries with auto-complete results.
- **E9 Timeline / Roadmap:** Sequential milestone line lighting up across historical beats.
- **E10 Metaphor Footage with Motion:** Authentic or public domain footage with Ken Burns push-in. *Capped at $\le 40\%$ runtime.*
- **E11 Abstract AI Visuals:** Token streams, attention matrices, and node network flows.

### 2.3 C: Camera & Transitions
- **C1 Slow Push-In (Ken Burns):** Continuous 3–6% scale drift across the scene. Default for all scenes.
- **C2 Punch-In on Beat:** Quick 8–15% zoom pop on major spoken punchlines (max 1 per 5s).
- **C3 Slide / Push Transition:** Dynamic lateral slide with directional motion blur on moving layers.
- **C4 Match Cut / Morph:** Shared visual node or card morphing seamlessly across scene cuts.
- **C5 Glitch / RGB Split:** 4–8 frame chromatic aberration. *Budget: max 1x per video, never in first 2s.*
- **C6 Screen Shake:** Decaying camera shake on explosive impact. *Budget: max 1x per video, never in first 2s.*
- **C7 Stacked Split-Screen:** Multi-pane vertical layout for prompt vs response.
- **C8 J-Cut / L-Cut:** Audio leads visual cut by 0.15–0.30s for natural rhythm.

### 2.4 S: Style Layers
- **S1 Brand Dark (Default):** Deep Obsidian `(8, 12, 28)` + 90px grid + Sapphire/Amethyst ambient radial spotlights.
- **S2 Light Film Grain:** 2.5% Gaussian film grain eliminating digital color banding.
- **S3 Liquid Glass Cards:** Translucent dark surfaces `(16, 20, 36)` with 1px border outlines `(255, 255, 255, 30)`.
- *S4 Cutout / S5 Y2K:* Skipped (incompatible with calm developer explainer tone).

---

## 3. Beat-Type Decision Table (Section 4.3 Mapping)

| Beat Type | Primary Animation | Secondary | Strictly Avoid |
|---|---|---|---|
| `hook` | **T3** + **C2** on key word | **E8** or **T7** if question/prompt | E5, E9 |
| `definition` | **E1** or **T3** | **T8** labels | C5 |
| `comparison` | **E3** | **T4** on differing word | E1 stack |
| `process` | **E2** | **T8**, **C3** between steps | T3 over diagram |
| `list_item` | **E4** | **T4** | E2 |
| `stat` | **T6** or **E5** (with source) | **C2** | Unverified claims |
| `example_prompt` | **T7** or **T5** | **E8** | E10 |
| `code` | **E6** | **T8**, **E7** | T3 |
| `ui_demo` | **E7** | **T8**, **C2** | E11 |
| `myth_fact` | **E3** (strike-through myth) | **T4** | E2 |
| `analogy` | **E10** or **E1** icons | **C1** | T6 |
| `opinion` | **E10** (footage) or own capture | **T4** | E5, E11 |
| `payoff` | **T3** | **C2** | New complex visuals |
| `cta` | **outro_card** | none | All others |

---

## 4. Production Budgets & Linting Rules
- **Anchor Spacing:** New visual anchor $\le 3.0\text{s}$ (Shorts) or $\le 6.0\text{s}$ (Long).
- **Static Hold Ceiling:** Max static hold without movement is 4.0s (Shorts) / 9.0s (Long). Mitigated via C1.
- **Scene Length:** Shorts: 2.0–4.0s per scene. Long: 5.0–12.0s per scene.
- **Repeat Limits:** Never use the same primary ID or same transition more than twice consecutively.
- **Heavy Effect Cap:** C5 (glitch) and C6 (shake) max 1x per video each, strictly forbidden during the first 2.0s. C4 (morph) max 2x in Shorts.
- **Variety Mandate:** Compare with last 3 plans in `plans/history/`; differ by at least 3 scene-layer elements (hook type, primary visual, transitions, accent color, scene order) while keeping brand layer (S1, font, voice, outro) consistent.

---

## 5. Verification & Tooling
Before rendering any video, validate the generated `scene_plan.json` using the automated linter:
```bash
python agents/skills/animation-library/linter/check_plan.py <path/to/scene_plan.json>
```
If errors are reported, the planner must automatically adjust the scene plan to conform before proceeding to hardware video rendering.
