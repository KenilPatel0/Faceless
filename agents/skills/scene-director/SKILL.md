---
name: scene-director
description: Plans and directs visual scenes, multi-layer spatial staging, scene archetypes, and transitions based on narrative beats.
---

# Scene Director Skill

The Scene Director turns story beats into concrete scene and shot plans. It answers:
**What specific scene archetype, environment, visual treatment, camera motion, and visual assets communicate this beat most clearly?**

## 1. Core Responsibilities
1. **Scene Archetype Selection**: Choose from standard archetypes:
   - *Opening & Narrative*: `cold_open_result`, `problem_agitation`, `concept_origin`, `hook_stopwatch`
   - *Explanation*: `system_overview`, `flow_pipeline`, `step_build`, `mechanism_reveal`, `token_fracture`, `kv_cache_split`
   - *Demonstration & Evidence*: `screen_recording_doc`, `comparison_board`, `data_proof`, `speculative_race`
   - *Story & Atmosphere*: `metaphor_visual`, `environmental_context`, `recap_tableau`, `outro_conversion`
2. **Multi-Layer Staging**: Compose every scene with explicit depth planes:
   - `background`: Dark obsidian canvas with radial ambient spotlights and subtle matrix dots.
   - `environment`: Floor plane, grid, context frames.
   - `subject`: The primary hero element (diagram node, terminal, code window, card).
   - `accent`: Highlights, glows, arrows, connecting energy beams.
   - `overlay`: Floating tags, badges, stat labels.
   - `captions`: Reserved at $y = 1010\text{px}$ (never obstructed; content layer $\le 880\text{px}$).
3. **Camera Language**: Apply purposeful, continuous camera motion:
   - `push_in`: Focus attention or increase tension.
   - `drift_pan`: Guide the eye across horizontal stages (left $\to$ right).
   - `pull_back`: Reveal scale, context, or systemic architecture.
   - `static_hold`: Reserved strictly for intricate code or high-density data examination.
4. **Purposeful Transitions**:
   - `direct_cut`: Standard default for editorial clarity between scenes.
   - `directional_push`: Continuous flow across connected process steps.
   - `zoom_punch`: Highlight a microscopic detail or internal silicon mechanism.

## 2. Information Density & Screen Clearance
- Maintain balanced 3-stage layout: Left Stage (Input / Context), Center Stage (Mechanism / Hero), Right Stage (Output / Payoff).
- Strictly enforce the $80\text{px}+$ caption clearance zone: content layer bounds must NEVER exceed $y = 880\text{px}$ in $1080\text{p}$ ($1760\text{px}$ in $4\text{K}$).
