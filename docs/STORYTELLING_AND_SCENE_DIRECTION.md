# Storytelling & Scene Direction Architecture

## Narrative-First Staging
Videos are structured in layers before rendering:
1. **Story Brief**: Defines format, audience, core promise, tone, and duration target.
2. **Beat Analysis**: Breaks script into 12 narrative beat types (`hook`, `context`, `problem`, `mechanism`, `evidence`, `comparison`, `escalation`, `reveal`, `example`, `resolution`, `recap`, `cta`).
3. **Scene Archetypes**: Maps beats to visual archetypes (`flow_pipeline`, `system_overview`, `screen_recording_doc`, `comparison_board`, `recap_tableau`).
4. **Visual Bible**: Preserves visual consistency (Obsidian background, Inter typography, 3-stage layout, safe margins).
5. **Animation & Compositing**: Pushes scenes to declarative timeline frames.

## 14 Validation Contracts
Pre-render checks enforced by `tools/story_validator.py`:
- 100% beat-to-scene coverage.
- Positive scene durations and frame rates.
- Valid asset IDs resolved in `AssetRegistry`.
- Valid transition links to existing adjacent scenes.
- Subtitle safe zone clearance ($y \le 880\text{px}$).
- Strict pacing limits (Shorts $1.5–4.0\text{s}$ shots, Long $3.0–8.0\text{s}$ shots).
