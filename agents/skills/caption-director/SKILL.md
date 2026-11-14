---
name: caption-director
description: Manages canonical two-layer caption architecture, faithful transcript export (SRT/WebVTT), readable phrase presentation, and platform safe-area layout.
version: 1.0.0
---

# Caption Director Skill

## Role & Purpose
The Caption Director enforces the strict separation of two distinct caption products: a faithful transcript source of truth for accessibility and search, and an on-screen presentation layer designed for readability.

## Core Responsibilities
1. **Layer A — Canonical `CaptionTrack` (Source of Truth):**
   - Faithful, timed representation of all spoken dialogue and meaningful non-speech audio cues (`[click]`, `[whoosh]`).
   - Automatically exports standard `.srt` and `.vtt` sidecar files for YouTube upload and accessibility.
   - Never edited or condensed for animation decoration.
2. **Layer B — `VisualCaptionPlan` (Presentation Layer):**
   - Segments cues into $2–6$ word phrase chunks.
   - Enforces Netflix English timed-text readability constraints:
     - Line length: $\le 42$ characters per line.
     - Adult reading speed: $\le 20$ characters per second.
   - Applies selective keyword emphasis (accent highlight on key nouns/numbers) without unreadable flickering.
3. **Safe-Area Layout & Collision Avoidance:**
   - Content clearance: content layers must remain strictly $\le 880\text{px}$ in $1080\text{p}$.
   - Subtitle positioning: safe lower center at $y = 1010\text{px}$ in $1080\text{p}$ ($2020\text{px}$ in $4\text{K}$).
   - Guarantees zero text collision between visual diagrams, code panels, and subtitles.
