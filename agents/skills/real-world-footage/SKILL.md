---
name: real-world-footage
description: Autonomous real-world footage integration, licensing compliance, and authentic UI recording for faceless video production.
---

# Real-World Footage Skill

This skill guides autonomous video production agents on how to build high-retention videos using authentic real-world material: real applications and websites, creator-filmed shots, nature, sky, ocean, and properly licensed B-roll, strictly complying with YouTube's 2026 authenticity guidelines.

---

## 1. Visual Hierarchy (Order of Decision)
For every video beat or scene, the agent must evaluate visual decisions in this strict order:
1. **Creator's Own Captures**: Authentic screen recordings of local apps or creator-filmed B-roll (hands typing, desk setup, physical props, nature) stored in `creator_footage/`.
2. **Real Software Captured by Script**: Scripted browser captures via Playwright (`recordVideo`), Android `scrcpy`, or iOS `simctl` simulator recordings.
3. **Public-Domain & NASA Footage**: NASA media (`images.nasa.gov`), Prelinger Archive, or CC0/CC BY from Wikimedia Commons.
4. **Free Stock Footage (Metaphor Only)**: Pexels, Pixabay, Mixkit, Coverr. **Must be capped at <= 40% of video runtime.** Never use stock as literal proof of a claim.
5. **Fallback to Custom Diagrams**: If no authentic footage matches after 4 search attempts, render a vector diagram or insert a `[CREATOR: capture ...]` placeholder.

---

## 2. Licensing Compliance & Verification
- **Zero Piracy Rule**: Never download clips from YouTube, TikTok, Instagram, TV, films, or Google Images. No `yt-dlp` scraping.
- **Allowed Stock Licenses**: CC0, Public Domain, Pexels License, Pixabay License, Mixkit free commercial, Coverr free commercial.
- **Forbidden Licenses**: **Do NOT use CC BY-SA, CC BY-NC, or CC BY-ND** without explicit approval from the channel creator.
- **Mandatory Artifacts for Every Video**:
  1. `license_log.json`: Structured log recording `scene`, `file`, `source`, `url`, `author`, `license`, `accessed`, and `license_page_saved`.
  2. `attribution.txt`: Clean formatted attribution text ready to paste directly into YouTube video descriptions for any CC BY material.
  3. `shotlist.csv`: Scene breakdown containing `scene`, `narration`, `visual_intent`, `source_decision`, `search_terms`, and `final_file`.

---

## 3. Real UI Capture Protocols

### Websites via Playwright
- Viewport: $1920 \times 1080$ for horizontal widescreen, or $390 \times 844$ for 9:16 vertical Shorts.
- Humanized interaction: Move mouse in discrete curved steps with 400–900ms pauses between clicks. Scroll smoothly and wait for network idle before capturing.
- Context finalization: Always close browser context to ensure the `.webm` recording flushes completely, then crop and encode via FFmpeg.

### Mobile & Simulator Captures
- Android: Record via `scrcpy --record=clip.mp4` with clean demo state.
- iOS: Record via `xcrun simctl io booted recordVideo --codec h264 clip.mp4`.
- Frame mobile captures inside a Pillow vector phone mockup on the atmospheric studio background.

### UI Retention Enhancements
- Hold each UI beat for at least **3.0 seconds** to allow viewer comprehension.
- Apply dynamic punch-in zoom (**120% to 150%**) onto the active form, button, or code snippet.
- Add cursor scale compression ripples on clicks and glowing outline highlights on interactive elements.

---

## 4. Metaphor & Concept Library
When illustrating abstract concepts, use physical real-world metaphors:
- **Tokens & Embeddings**: Lego bricks, puzzle pieces, sorting beads.
- **Context Window & Memory**: Papers on a wooden desk, sticky notes, filing cabinet drawers.
- **Probabilities & Sampling**: Dice rolling in slow motion, water ripples, scattering seeds.
- **Agent Loops**: Flowing river water, water wheels, conveyor belts, mechanical clock gears.
- **Reasoning & Planning**: Hands typing at a mechanical keyboard, conducting an orchestra.
- **Calm & Resolution**: Deep misty pine forest, mountain peaks, serene lake reflection.

---

## 5. Automated Footage Grading
All imported clips must be color-graded to match the active channel design system:
- **Lifted Blacks & Tint**: Apply a gentle ambient color grade matching channel profile spotlights.
- **Sub-pixel Motion**: Apply continuous camera push-in or harmonic drift (`push_in(img, amount=0.035)`) so stock clips never freeze.
- **Subtitle Contrast Gradient**: Apply a 35% to 50% vertical alpha gradient across the bottom $200\text{px}$ to guarantee 100% subtitle legibility.
- **Audio Stripping**: Strip all raw audio tracks from stock clips (`-an`). Synthesize pure neural narration and duck background audio to -22 dBFS.
