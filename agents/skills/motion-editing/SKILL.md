---
name: motion-editing
description: Use whenever you animate, render, edit or export a short or long faceless video and want smooth, professional motion — spring/eased animation, staggered reveals, anti-aliased sub-pixel rendering, motion blur on moving elements, clean transitions, editing craft (J/L cuts, rhythm, emphasis) and YouTube-correct encoding. Pairs with humanized-video and channel brand configuration.
---

# Motion + Editing Skill

Layer order: **channel brand profile** -> **humanized layer** (`humanized-video`: variation, sound, QA) -> **this skill** (how motion is built, rendered, edited and exported). Code: `scripts/motion.py` (+ `humanize.py`, `qa.py`). Reference demo: `scripts/demo_smooth.py smooth|naive`. Sources and confidence: `references/research-notes.md`.

## 1. The five things that make motion look smooth (in priority order)
1. **Right easing/physics** - never linear. Entrances `ease_out_expo`, exits `ease_in_cubic`, moves `ease_in_out`, "alive" objects `spring()` (freq 2.2, zeta 0.72, about 4% overshoot, settles in ~0.6 s).
2. **Sub-pixel, anti-aliased drawing** - positions are floats; draw through `SS` (2x supersampled canvas, LANCZOS down) so edges and text glide instead of snapping to whole pixels. Integer positions + aliased edges = the "jittery generated" look.
3. **Motion blur on moving elements** - temporal sub-frame accumulation (`blur_layer`): average several sub-frames inside a 180-degree shutter (half a frame, centred on the frame time). Use `auto_samples(px_per_frame)` so sub-samples are <= ~1.5 px apart (too few samples = visible echo ghosts). Put only moving shapes in the blur layer; keep static text/UI out so it stays sharp. Skip blur when speed < 1.5 px/frame.
4. **Staggering and overlap** - group items enter 60-120 ms apart with small deterministic jitter (`stagger`); next entrance starts before the previous one finishes. Never everything at once.
5. **Frame rate and encode** - 30 fps for everything with moving text/graphics (24 fps judders on fast text; 60 only for heavy UI motion). YouTube wants the frame rate the video was made in (24-60 accepted).

## 2. Timing table
| Use | Duration |
|---|---|
| tiny feedback (tick, ripple) | 0.12-0.15 s |
| normal reveal (bullet, card, word) | 0.30-0.40 s |
| big entrance / scene intro | 0.50-0.80 s |
| exit | 75% of the matching entrance |
| transition between scenes | 0.25-0.40 s |
| stagger step | 0.06-0.12 s (total <= 0.6 s) |
Snap start/end times to frames (`frame_align`). Hold finished states for >= 0.4 s so the eye can read them.

## 3. Animation toolkit (what to use when)
- **Text:** word-by-word slide-up + fade (`word_pop`) for headlines; per-letter only for ONE key word per video; typing (`typed`) for prompts/code; number counters (`count_up`, ease-out-quart); hand-drawn underline (`hand_line`) for emphasis. Never fade whole paragraphs.
- **Cards/UI:** spring in from the side with stagger; settle with a 1.00 -> 1.04 -> 1.00 `pulse` on the active one; dim previous items rather than removing them.
- **Diagrams/loops:** draw lines on progressively; highlight the active node in sync with the narration; arrows move along arcs (`arc_point`), not straight lines.
- **Camera:** every scene gets a slow `push_in` (3-5%) or `drift`; add a `pulse`-style punch-in (4-6%, 0.3 s) on the single most important word/number; alternate directions between scenes. Apply camera to the content layer BEFORE captions and brand tag.
- **Parallax:** 2-3 layers moving at different speeds (background 0.3x, mid 0.6x, foreground 1x) for hook and transition scenes only.
- **Transitions** (`transition(a,b,p,kind)`): `slide` (continuation), `wipe` (new topic), `scale_fade` (zoom into a detail), `iris` (reveal/answer). One primary + one accent per video; always on a sentence end; never the same transition three times in a row. ffmpeg equivalents for clip editing: `xfade=transition=slideleft|wipeleft|circleopen|fadeblack:duration=0.3:offset=T`.
- **Restraint:** one primary motion per beat; secondary motion (glow, shadow, dimming) supports it. If two things move, one must be slower and smaller.

## 4. Editing craft
- **Cut on sentence ends; show visuals 0.1-0.2 s before the word they illustrate** (the eye leads the ear).
- **J-cut / L-cut:** start the next scene's visual 0.15-0.30 s before the previous narration ends (J), or let the old visual linger under the first words of the next line (L). It hides the seams between separately generated narration chunks.
- **Rhythm:** alternate fast and slow beats; give the key insight a pause (0.4 s of silence) and a slower, larger visual; never make every beat the same length.
- **Emphasis stack (max one per 10 s):** punch-in OR color flash OR SFX OR underline - not all together.
- **Speed ramps** are for screen recordings only: ease a boring 3 s wait into 0.5 s (`setpts` with an eased curve), return to 1x before the result appears.
- **Screen recordings:** crop to the relevant area, zoom to 120-150% on the action, add a cursor ripple on clicks, mute system sounds, keep real mistakes if you explain them.
- **Typography/layout:** two sizes minimum (headline vs label), generous margins, one accent color per scene leading, consistent corner radius, 8-pt spacing grid; keep content inside the safe areas in the humanized skill.
- **Color:** grade by contrast only (slightly lifted blacks, no pure #000 on gradients) and add grain (2-3%) - it also prevents banding in dark gradients after YouTube re-encodes.
- **Chapter cards (long videos):** a 0.8 s heading wipe at each new section keeps viewers oriented and matches the chapter list in the description.

## 5. Rendering performance (1 CPU core)
- Cache the static background; render only moving layers at 2x; run blur with `auto_samples` only while something moves.
- Typical cost: a 3.5 s 720x1280 smooth demo renders in about a minute; a 30 s short in a few minutes; an 8-10 min long video in 15-30 min with blur and supersampling (use `S=1` for text-only list scenes if time matters).
