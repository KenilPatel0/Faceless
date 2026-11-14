---
name: storytelling-director
description: Plans and directs story arcs, narrative beats, scene archetypes, environments, and shot staging for autonomous faceless video production.
version: 1.0.0
---

# Storytelling Director Skill

## Role & Purpose
The Storytelling Director decides what the audience should see and feel at each beat of a video, translating written copy into purposeful, connected visual scenes rather than a random montage or slideshow.

## Core Responsibilities
1. **Story Brief Interpretation:**
   - Classifies video into one of 10 narrative formats (`technology_explainer`, `educational_lesson`, `product_showcase`, `case_study`, etc.).
   - Establishes core viewer question, audience promise, tone, and factuality mode.
2. **Beat Analysis:**
   - Segments script by meaning into discrete StoryBeats (`hook`, `context`, `problem`, `mechanism`, `evidence`, `comparison`, `escalation`, `reveal`, `example`, `resolution`, `recap`, `cta`).
   - Assigns a visual concept and emotional intent to every beat.
3. **Scene Archetype Selection:**
   - Selects from 16 verified archetypes (`cold_open_result`, `system_overview`, `flow_pipeline`, `cause_effect`, `comparison_board`, `data_proof`, `authentic_product_reveal`, `ui_walkthrough`, `code_editor`, `terminal`, `recap_tableau`).
4. **Environment & Multi-Layer Staging:**
   - Designs full-bleed environments (branded abstract, cinematic, workshop, terminal, studio) spanning edge-to-edge.
   - Preserves visual continuity: adjacent scenes share consistent lighting, palette, and scale.
   - Enforces caption safe-area clearance (content layer strictly $\le 880\text{px}$, subtitles at $1010\text{px}$).

## Rules & Constraints
- Never translate every spoken noun into a literal stock photo.
- Never place text or diagrams in the subtitle safe clearance zone ($y > 880\text{px}$).
- Authentic evidence outranks synthetic mockups: use real UI screen recordings or Playwright captures for actual software.
- Enforce pacing: Shorts shots $1.5–4\text{s}$, scenes $3–9\text{s}$; Long shots $3–8\text{s}$, scenes $6–25\text{s}$.
