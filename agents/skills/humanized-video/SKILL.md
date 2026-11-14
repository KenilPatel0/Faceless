---
name: humanized-video
description: Use whenever you make, edit, review or export an AI/tech faceless video (Shorts or long explainers). Adds the "human-made" layer on top of base channel rules — varied scene design, natural motion and easing, editing rhythm, narration pacing, sound design, hand-made details, loudness mastering and an automated QA gate — so videos never look like mass-produced templates.
---

# Humanized Video Skill

**Read first:** Channel configuration (`channel_config.py`, which resolves `Kenil/channel_profile.json`, `channel.json`, or environment variables) for brand identity: channel name, colors, voice, caption position, and intro/outro cards. This skill sits ON TOP of it. Where the two interact, brand configuration defines identity and this skill governs motion, editing, sound, and natural variation.

Helper code: `scripts/humanize.py` (easing, stagger, camera push, grain, hand-drawn lines, cursor, typing, karaoke captions, humanized narration, SFX, ducked mix, loudness master) and `scripts/qa.py` (QA gate). Sources and confidence levels: `references/research-notes.md`.

## 1. Why this exists
- YouTube rules clarify that channels made from generic, repetitive, **template-based** videos with little variation between uploads can lose monetization. AI and faceless are allowed; mass-produced look-alikes are not. Reviews evaluate the whole channel.
- Test before every upload (the **swap test**): *could another channel swap in a different name and voice and publish essentially this same video?* If yes, add original value or variation.
- Make the channel's About section say who makes the videos and how (the creator's real development/tech experience; scripts and examples are original; narration is a synthetic voice; visuals are custom-animated).
- Faceless videos feel human when they show a real person's thinking: opinions, real experience, authentic screen recordings, honest mistakes, and motion that behaves like it was timed by hand.

## 2. Locked vs. variable
**Locked (brand profile from channel configuration):** channel name, intro and SUBSCRIBE outro cards, tagline, palette, typography, voice model, caption style, 30 s shorts / 8-10 min long.

**Variable (change on purpose every video):**
| Element | Options (rotate) |
|---|---|
| Hook visual | big-word slam, question bubbles, split compare, live "typing" prompt, number counter |
| Body scene types | list+icon, before/after bars, diagram/loop, phone/screen mockup, code/terminal typing, chart/bars, comparison cards (use >= 3 different types per video; never the same type 3 scenes in a row) |
| Transition | slide, push, wipe, scale-fade, iris (pick ONE primary + one accent per video) |
| Accent order | rotate which palette color leads (cyan / green / yellow / purple) |
| SFX palette | choose 3 of: pop, tick, chime, whoosh, soft click |
| Opening line | question / bold claim / mini-story / surprising number (not the same as the previous 3 videos) |
**Variation budget:** each new video must differ from the previous three in at least **3** of: hook visual, scene-type mix, transition, accent order, demo/example type, opening-line style.

## 3. Original-value rules (the human signal)
Every video must include at least ONE thing only the creator can provide:
- developer's own hands-on experience, a genuine mistake made, or a strong informed opinion,
- a **real screen recording** (IDE/terminal/AI tool) with an authentic cursor, or real test results,
- a custom diagram built specifically for that exact insight.
Script style: first person, contractions, short sentences, one small aside per minute; ban stock phrases ("In today's video", "Let's dive in", "game-changer", "you won't believe"). Never invent studies, quotes or citations; label illustrative examples ("Illustrative", "MADE-UP EXAMPLE"). No AI persona giving health, finance or legal advice.

## 4. Motion design spec
- **Durations (seconds):** feedback 0.12-0.15; normal reveal 0.30-0.40; big entrance 0.50-0.80; exits = 75% of the entrance. Snap every start/end to a frame (`frame_align`).
- **Easing:** entrances `ease_out_expo` (or quart for calm), exits `ease_in_cubic`, moves A->B `ease_in_out`. **Never linear** except progress bars and spinners.
- **Overshoot:** subtle only (`ease_out_back`, ~3%), on ONE key element per scene. No elastic or bouncy motion.
- **Stagger:** groups enter 60-120 ms apart with +/-20 ms deterministic jitter (`stagger`), total stagger <= 0.6 s. Not everything moves in perfect lockstep.
- **Anticipation + settle:** for emphasis do a 1.00 -> 1.04 -> 1.00 scale pulse over ~0.25 s; draw lines on (`hand_line`) instead of fading them in.
- **Arcs, not straight lines:** cursors and flying objects follow `arc_point` paths; clicks get a ripple (`draw_cursor`).
- **Camera:** every scene gets a slow push-in of 3-5% (`push_in`, p = scene progress); alternate push-in / push-out / slight drift between scenes. Apply it to the content layer BEFORE drawing the brand tag and captions. No frame is ever truly static.
- **One primary motion per beat.** Don't animate everything (animation fatigue). Secondary motion (glow, shadow, dim of previous items) supports it quietly.
- **Typing:** code/prompt text types at 8-14 chars/s with uneven rhythm (`typed`).
- **Transitions:** 0.25-0.40 s, placed on a sentence end; overlap exit and next entrance by ~0.1 s.

## 5. Editing rhythm & Voice-Visual Synchronization
- **Strict Voice-Visual Sync:** Never reveal visual elements before the voice introduces them. Every spoken beat MUST have a synchronized visual focal point:
  - If a beat introduces a concept, enter that specific card.
  - If a beat expands on an existing point, highlight the active card brightly while softly dimming previous ones.
  - Never allow "silent beats" where the narration speaks for 10+ seconds over an unchanged screen.
- **Shorts (30 s):** first visual payoff <= 1.5 s; something visibly changes (new element, zoom step, highlight, cut) every **2-4 s**; no static hold > 4 s; narration ~160-180 wpm (voice at 1.1 is ~174 wpm).
- **Long (8-10 min):** a visual progression every 5-15 s; active cards use `smooth_float` harmonic breathing (+/-3.5px) so no scene ever produces a static hold > 9s.
- **Reveal slightly ahead of the voice:** show each visual 0.1-0.2 s BEFORE the word it illustrates; cut on sentence ends.
- Keep on-screen words short (2-5 words); the narration carries the sentence.

## 6. Narration humanizing (same voice, less robotic)
Use `speak_humanized`: per-sentence speed variation of +/-4% around 1.1, ~5% slower on very short sentences, uneven pauses of 0.22-0.34 s between sentences, and an extra 0.4 s before the main reveal/payoff. Contractions always. No more than two sentences over 22 words in a row. Read the script aloud once; rewrite anything you would not say to a friend.

## 7. Sound design
- **Hierarchy:** voice > meaningful SFX > music. Fewer, better sounds beat constant whooshes.
- **Levels:** music -18 to -25 dB under speech (about -12 to -14 dB in gaps, via ducking `mix`); SFX around -12 to -18 dB, never louder than the voice; at most ~1 SFX per 3 s on average.
- **Use SFX for events only:** pop = text/icon appears, tick = list item, chime = success/check, whoosh = scene change ONLY. Silence during key numbers and punchlines. Vary the palette per video.
- **Music:** YouTube Audio Library or a track you have a licence for; keep it ambient. Synthetic/AI-generated music is on YouTube's list of things to disclose.
- **Master every export:** `master()` = two-pass loudnorm to about -14 to -15 LUFS integrated, true peak <= -1.5 dBTP, 48 kHz, AAC 192k.

## 8. Visual finish and hand-made details
- `finish()` adds grain (2-4%) and vignette (12-18%) on export; soft shadows under cards (blur ~20, ~35% alpha); consistent corner radii; max two accent colors per scene; at least two text sizes for hierarchy.
- Slight card rotation (+/-1 deg) is allowed on "sticker" elements only. Keep text upright.
- Hand-drawn underline/circle for emphasis (`hand_line`), cursor demos, typing animations, and real screenshots/recordings beat decorative shapes.
- Layout safety: shorts keep content inside x 90-990, y 220-1500 (brand tag at y 150, captions at y 1560); long keeps content strictly above y 915 (captions centered at y 1010, ensuring an 80px safe clearance zone).
- Captions: shorts may use word highlight (`word_timings` + `draw_karaoke`, active word yellow); long videos keep calm small captions without karaoke.

## 9. Workflow
1. Script -> check section 3 (original value) and section 2 (variation budget).
2. Narration with `speak_humanized` (keep sentence timings for captions/visual cues).
3. Render with push-in + staggered reveals + `finish`; place SFX events on reveals; `mix` -> `master`.
4. Mux and run QA.
5. Deliver MP4 + publishing copy + the AI-disclosure note.

## 10. QA gate (must pass before delivery)
Run `python3 scripts/qa.py video.mp4 short|long`. Must show: decode errors 0; loudness -16.5 to -12.5 LUFS (target ~-15) with true peak <= -0.5 dBFS after AAC; no static holds (> 4 s short, > 9 s long). Then:
- contact sheet: one frame per scene; no clipped, overlapping or misspelled text; captions never collide with content,
- variation check (section 2) and swap test (section 1),
- listen once with eyes closed: voice clear, no stacked SFX, music never competes.

## 11. Clean, Minimal & Smooth Motion Standards (The "Anti-Clutter" Rule)
To ensure videos never look cheap, boxy, or wireframed:
1. **Generous Breathing Room & Whitespace:** Never cram the frame with bulky boxes. Leave at least 60-100 px of padding around key elements. One primary visual focal point per beat.
2. **Subtle, Delicate Card Borders (1px max, low contrast):** Modern cards use sleek dark fills `(16, 20, 36)` with delicate 1 px borders `(255, 255, 255, 30)` or subtle tinted accents.
3. **One Accent Color Rule:** Each scene features ONE hero accent color (e.g., Electric Cyan for Tokens, Emerald Green for Silicon, Warm Amber for Bandwidth, Violet for Tricks). All other elements are Crisp White or Muted Slate `(150, 160, 195)`. Never mix 4 primary saturated neon colors in one screen.
4. **Smooth Micro-Motion & Soft Easing:**
   - Elements enter using `ease_out_quart` over 0.5-0.7 s with a subtle 20-30 px vertical drift (never abrupt 100 px snaps).
   - Once revealed, elements maintain gentle harmonic floating micro-motion (`smooth_float`, +/-3-4 px) to keep the frame dynamically alive and eliminate static holds.
5. **Visual Metaphors Over Generic Bullet Lists:** Always prefer clean, intuitive diagrams—such as token chips, parallel core arrays, data pipe gauges, and milestone steppers—over dense text bullets. Explanations must be visually obvious in 2 seconds.

## 12. Native 4K 60FPS Production Standards (tools/render_core.py & tools/video_pipeline.py)
To deliver cinema-grade clarity and unlock YouTube's premium VP09/AV01 codecs:
1. **Resolution & Temporal Frequency:**
   - Long Video: `3840×2160` (16:9 4K UHD) @ `60.0 FPS`.
   - Shorts: `2160×3840` (9:16 4K Vertical) @ `60.0 FPS`.
   - Frame delta: $\Delta t = 1/60 = 0.01667\text{s}$.
2. **Typography Scaling ($S = 2.0\times$):**
   - Title / Hook: Font 208, stroke 16.
   - Headings / Badges: Font 96, stroke 8.
   - Card Titles: Font 88. Body: Font 56.
   - Subtitles (Long Video): Font 80, stroke 10, centered at $y = 2020\text{px}$.
   - Subtitles (Shorts): Font 132, stroke 16, centered at $y = 3120\text{px}$.
3. **Strict 4K Subtitle Clearance Invariant:**
   - On 4K horizontal video ($3840 \times 2160$), content layer must NEVER exceed **$y = 1830\text{px}$**, maintaining a strict 160px safe clearance buffer above subtitles at $y = 2020\text{px}$.
4. **Zero-Resize Overscan Camera Push-In:**
   - Render dynamic scenes at $1.035\times$ overscan ($3974 \times 2235$).
   - Slice direct $3840 \times 2160$ crop windows with continuous sub-pixel harmonic drift (`OverscanCanvas.slice_frame()`).
   - Achieves 120+ FPS frame generation speed in Python by eliminating CPU bilinear resize overhead.
5. **Hardware-Accelerated Streaming Encoding (`tools/video_pipeline.py`):**
   - Direct raw RGB streaming pipe into FFmpeg (`pipe:0`). Peak RAM remains < 350 MB.
   - Encoder priority cascade: `h264_nvenc` &rarr; `h264_qsv` (Intel Iris Xe) &rarr; `h264_mf` (Media Foundation) &rarr; `libx264`.

## 13. Human-Crafted Visual Standards & High-Retention Shorts
To prevent videos from looking like automated AI templates:
1. **Zero-Synthetic Real-World Asset Rule:**
   - When referencing software, OS, benchmarks, games, or real hardware, NEVER draw synthetic mockups using Pillow rectangles.
   - Use authentic high-DPI screenshots via `tools/capture_ui.py --4k` (terminal / browser) or transparent hardware cutouts via `tools/cutout.py`.
2. **Cinematic Obsidian Background:**
   - Replaces flat 2-color linear gradients with a multi-stop depth composite: deep obsidian `(10, 13, 20)`, dual radial ambient spotlights (Sapphire top-left + Amethyst bottom-right), 2.5% Gaussian film grain (eliminates YouTube gradient banding), and subtle 12% dotted matrix.
3. **High-Retention Shorts Pacing (1.5s–2.5s Rule):**
   - First 1.5 seconds must feature an immediate visual payoff and high-contrast hero badge.
   - Shift the visual focal point every 1.5 to 2.5 seconds using step reveals, hero dimming/highlighting, or camera punch-ins.
4. **Dynamic Karaoke Captions (Word-by-Word Highlight):**
   - Limit subtitles on Shorts to 3–4 words per chunk.
   - Active spoken word illuminates in Electric Yellow `(255, 205, 70)` or Electric Cyan `(70, 220, 255)` with a subtle $1.06\times$ scale bounce, centered at safe coordinates ($y = 3120$ in 4K / $y = 1560$ in 1080p).


