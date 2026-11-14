---
name: animation-director
description: Story-aware visual motion planning and AnimationPlan generation for YouTube Shorts, Reels, and long-form video explainers. Use whenever planning scenes, visual beats, motion treatments, or transitions.
---

# Animation Director

The Animation Director is the story-aware visual planner for the **Faceless Video Engine**. It decides *what moves, why, when, and how strongly*, leaving the rendering engine to calculate deterministic frames.

---

## 1. Core Operating Principles

1. **Editorial Grammar ≠ Animation Primitives:** A jump cut, kinetic caption, shape morph, and camera push are distinct layers of production decisions. Keep them separated.
2. **Motion Explains Meaning:** The subject, verb, number, comparison, and story beat must drive the visual choice. Motion must never be applied at random as mere decoration.
3. **Format Over Virality Guarantees:** Select structured short-form formats (`text_led_hook`, `screen_tutorial`, `data_story`, `myth_vs_fact`), rather than chasing fleeting "viral" tricks.
4. **Registry-Driven Selection:** Query `tools/animation_registry.py` for valid technique IDs and schemas. Never invent unregistered animation names or raw Pillow drawing loops.
5. **Deterministic Plans:** Generate a versioned `AnimationPlan` JSON that is strictly validated against schemas and platform safe zones before rendering.

---

## 2. 12-Step Direction Workflow

Whenever a video prompt, script, or scene list requires visual planning:

1. **Extract Creative Brief:** Parse topic, audience, platform (`youtube_shorts`, `instagram_reels`, `youtube_long`), aspect ratio (`9:16`, `16:9`), pacing, and intensity budget (0–4).
2. **Divide into Semantic Beats:** Break scenes into meaningful communication units (subject, action, concept, evidence, visual objective).
3. **Assign Primary Scene Format:** Choose one dominant visual language per scene from the 16 standard formats (e.g. `text_led_hook`, `kinetic_explainer`, `screen_tutorial`, `data_story`).
4. **Query Animation Registry:** Check `tools/animation_registry.py` for candidate techniques matching intent tags and content signals.
5. **Apply Candidate Scoring:** Use the research-backed decision formula:
   $$\text{Score} = 0.30 \times \text{Semantic} + 0.25 \times \text{Comprehension} + 0.15 \times \text{Narrative} + 0.10 \times \text{Brand} + 0.05 \times \text{Variety} + 0.10 \times \text{Perf} + 0.05 \times \text{Asset}$$
6. **Enforce Hard Constraints:** Reject any candidate that lacks required assets, misrepresents evidence, or exceeds safe boundaries.
7. **Control Motion Density:** Maximum **1 primary motion event per beat**; at most 2 supporting elements. Preserve stillness and calm holds where appropriate.
8. **Speech-Aligned Timing:** Anchor visual triggers to word/phrase timestamps from narration rather than arbitrary scene midpoints.
9. **Conservative Transitions:** Default to clean editorial hard cuts (`transition.cut`). Use designed transitions (`directional_wipe`, `dissolve`) only at major chapter boundaries.
10. **Validate Platform Safe Zones:**
    - **Shorts (9:16):** Avoid bottom 420px (platform UI) and top 260px (channel header). Captions at `y=3120` (4K) / `y=1560` (1080p).
    - **Long (16:9):** Maintain 80px safe clearance above captions at `y=2020` (4K) / `y=1010` (1080p). Content layer must never exceed `y=915px` (1080p) or `y=1830px` (4K).
11. **Flashing & Accessibility Safety:** Guarantee fewer than 3 high-contrast cuts/flashes per second (WCAG 2.2 compliant).
12. **Emit Versioned Plan:** Output the validated `AnimationPlan` JSON ready for `TimelineResolver` and the hardware streaming pipeline.

---

## 3. Motion Intensity Budget (0–4)

| Level | Name | Allowed Behavior |
|---|---|---|
| **0** | **Static** | Intentional still hold; only subtitle updates and required cuts. |
| **1** | **Subtle** | Sub-pixel camera drift (3.5%), low-amplitude fade, quiet dissolve. |
| **2** | **Standard** | Clean spring entrances, real UI window focus, list stagger, directional slide. |
| **3** | **Dynamic** | Scale punch hook, numeric count-up, terminal command execution, split comparison. |
| **4** | **Hero Impact** | Reserved for major hook payoff or conversion outro (Bezier cursor glide + ripple). |
