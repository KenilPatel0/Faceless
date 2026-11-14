# Two-Layer Caption System

## Core Architectural Principle: Two Separate Layers
Accessibility and visual motion graphics must never conflict. The Faceless caption engine strictly separates canonical transcript data from visual rendering:

### Layer A: CaptionTrack (Source of Truth)
- Faithful, verbatim record of all spoken words and critical non-speech cues.
- Automatically exports standard `.srt` (SubRip) and `.vtt` (WebVTT) sidecars.
- Never modified, summarized, or truncated for visual decoration.

### Layer B: VisualCaptionPlan (Presentation Layer)
- Formats words into $2–6$ word phrases for optimal on-screen reading.
- Strictly adheres to broadcast and Netflix readability standards:
  - Line length $\le 42\text{ characters}$.
  - Reading speed $\le 20\text{ characters/second}$.
- Highlights selective keywords in Electric Yellow with subtle scale bounce.
- Reserved safe zone at $y = 1010\text{px}$ ($1080\text{p}$) with $80\text{px}+$ clearance above content ($y \le 880\text{px}$).
