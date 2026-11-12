---
name: techxkenil-humanized-video
description: Use whenever you make, edit, review or export a TechXKenil short or long video (faceless AI/tech explainers). Adds the "human-made" layer on top of the base brand rules - varied scene design, natural motion and easing, editing rhythm, narration pacing, sound design, hand-made details, loudness mastering and a QA gate - so videos never look like one mass-produced template.
---

# TechXKenil Humanized Video Skill

**Read first:** `TechXKenil_Video_Rules.md` (brand lock: colors, font, voice `am_michael` @1.1, caption style, TXK intro/outro, formats, publishing copy). This skill sits ON TOP of it. Where the two disagree, the brand lock wins for identity (colors, voice, intro/outro, caption position) and this skill wins for motion, editing, sound and variation.

Helper code: `scripts/humanize.py` (easing, stagger, camera push, grain, hand-drawn lines, cursor, typing, karaoke captions, humanized narration, SFX, ducked mix, loudness master) and `scripts/qa.py` (QA gate). Sources and confidence levels: `references/research-notes.md`.

## 1. Why this exists
- YouTube clarified on 16 Jul 2026 that channels made from generic, repetitive, **template-based** videos with little variation between uploads can lose monetization. AI and faceless are allowed; mass-produced look-alikes are not. Reviews look at the whole channel.
- Test before every upload (the **swap test**): *could another channel swap in a different name and voice and publish essentially this same video?* If yes, add original value or variation.
- Make the channel's About section say who makes the videos and how (Kenil, 3 years as a developer; scripts and examples are his; narration is a synthetic voice; visuals are custom-animated).
- Faceless videos feel human when they show a real person's thinking: opinions, real experience, real screen recordings, honest mistakes, and motion that behaves like it was timed by hand.

## 2. Locked vs. variable
**Locked (brand, never change):** channel name, TXK intro and SUBSCRIBE outro cards, tagline "AI • TECH • CODE", palette, Inter Display Bold, voice `am_michael`, caption style and position, 30 s shorts / 8-10 min long.

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
Every video must include at least ONE thing only Kenil can provide:
- his own experience ("in my 3 years building apps..."), a mistake he made, or a real opinion ("my take"),
- a **real screen recording** (Flutter/IDE/AI tool) with a real cursor, or a real test result he ran,
- a custom diagram built for this exact idea.
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

## 5. Editing rhythm
- **Shorts (30 s):** first visual payoff <= 1.5 s; something visibly changes (new element, zoom step, highlight, cut) every **2-4 s**; no static hold > 4 s; narration ~160-180 wpm (the current voice at 1.1 is ~174 wpm - keep it).
- **Long (8-10 min):** first 60 s: a change every 5-10 s; after that a small change every 10-20 s (next bullet, highlight, zoom) and a bigger pattern interrupt (new scene type, demo, question, sound change) every 30-60 s; a teaser/open loop about every 90 s; a recap near the end. Don't over-edit calm explanations - shots of 20-40 s are fine **if something moves inside them**.
- **No static content-area hold > 4 s in shorts, > 9 s in long videos** (QA enforces this).
- **Reveal slightly ahead of the voice:** show each visual 0.1-0.2 s BEFORE the word it illustrates; cut on sentence ends.
- Keep on-screen words short (2-5 words); the narration carries the sentence.

## 6. Narration humanizing (same voice, less robotic)
Use `speak_humanized`: per-sentence speed variation of +/-4% around 1.1, ~5% slower on very short sentences, uneven pauses of 0.22-0.34 s between sentences, and an extra 0.4 s before the main reveal/payoff. Contractions always. No more than two sentences over 22 words in a row. Read the script aloud once; rewrite anything you would not say to a friend.

## 7. Sound design
- **Hierarchy:** voice > meaningful SFX > music. Fewer, better sounds beat constant whooshes.
- **Levels:** music -18 to -25 dB under speech (about -12 to -14 dB in gaps, via ducking `mix`); SFX around -12 to -18 dB, never louder than the voice; at most ~1 SFX per 3 s on average.
- **Use SFX for events only:** pop = text/icon appears, tick = list item, chime = success/check, whoosh = scene change ONLY. Silence during key numbers and punchlines. Vary the palette per video.
- **Music:** YouTube Audio Library or a track you have a licence for; keep it ambient. Synthetic/AI-generated music is on YouTube's list of things to disclose.
- **Master every export:** `master()` = two-pass loudnorm to about -14 to -15 LUFS integrated, true peak <= -1.5 dBTP, 48 kHz, AAC 192k. (The first four videos were -24 LUFS; mastered copies exist.)

## 8. Visual finish and hand-made details
- `finish()` adds grain (2-4%) and vignette (12-18%) on export; soft shadows under cards (blur ~20, ~35% alpha); consistent corner radii; max two accent colors per scene; at least two text sizes for hierarchy.
- Slight card rotation (+/-1 deg) is allowed on "sticker" elements only. Keep text upright.
- Hand-drawn underline/circle for emphasis (`hand_line`), cursor demos, typing animations, and real screenshots/recordings beat decorative shapes.
- Layout safety in our grids: shorts keep content inside x 90-990, y 220-1500 (brand tag at y 150, captions at y 1560); long keeps content above y 960 (captions at y 1010).
- Captions: shorts may use word highlight (`word_timings` + `draw_karaoke`, active word yellow); long videos keep calm small captions without karaoke.

## 9. Workflow
1. Script -> check section 3 (original value) and section 2 (variation budget; note which options you picked in a one-line `design_notes` comment in the data file).
2. Narration with `speak_humanized` (keep sentence timings for captions/visual cues).
3. Render with push-in + staggered reveals + `finish`; place SFX events on reveals; `mix` -> `master`.
4. Mux and run QA.
5. Deliver MP4 + publishing copy + the AI-disclosure note (section 10).

## 10. QA gate (must pass before delivery)
Run `python3 scripts/qa.py video.mp4 short|long`. Must show: decode errors 0; loudness -16.5 to -12.5 LUFS (target ~-15) with true peak <= -0.5 dBFS after AAC; no static holds (> 4 s short, > 9 s long). Then:
- contact sheet: one frame per scene; no clipped, overlapping or misspelled text; captions never collide with content,
- variation check (section 2) and swap test (section 1),
- listen once with eyes closed: voice clear, no stacked SFX, music never competes.

## 11. YouTube Studio checklist
- Answer the **altered/synthetic content** question honestly at upload. YouTube asks for disclosure of realistic synthetic media (examples on its page include cloning someone else's voice and synthetically generated music). A clearly synthetic stock narration over custom animation is not realistic footage and is generally not required, but it is Kenil's responsibility to check the current wording each upload. Disclosure does not reduce reach or monetization eligibility, per YouTube.
- Keep the channel About text honest about the production method.

## 12. Anti-patterns (do not do)
Identical scene layout for every video; every scene entering with the same fade; linear motion; bounce/elastic; whoosh on every cut; loud or constant music; unmastered audio; static frames over 4 s (short) / 9 s (long); fake sources or numbers; same hook structure three times in a row; pushing out many near-identical videos in a short time.

## 13. Clean, Minimal & Smooth Motion Standards (The "Anti-Clutter" Rule)
To ensure videos never look cheap, boxy, or wireframed:
1. **Generous Breathing Room & Whitespace:** Never cram the frame with bulky boxes. Leave at least 60-100 px of padding around key elements. One primary visual focal point per beat.
2. **Subtle, Delicate Card Borders (1px max, low contrast):** Banned: heavy 4-6 px bright saturated borders. Modern cards use sleek dark fills `(16, 20, 36)` with delicate 1 px borders `(255, 255, 255, 30)` or subtle tinted accents.
3. **One Accent Color Rule:** Each scene features ONE hero accent color (e.g., Electric Cyan for Tokens, Emerald Green for Silicon, Warm Amber for Bandwidth, Violet for Tricks). All other elements are Crisp White or Muted Slate `(150, 160, 195)`. Never mix 4 primary saturated neon colors in one screen.
4. **Smooth Micro-Motion & Soft Easing:**
   - Elements enter using `ease_out_quart` over 0.5-0.7 s with a subtle 20-30 px vertical drift (never abrupt 100 px snaps).
   - Once revealed, elements maintain gentle harmonic floating micro-motion (`smooth_float`, +/-3-4 px) to keep the frame dynamically alive and eliminate static holds.
5. **Visual Metaphors Over Generic Bullet Lists:** Always prefer clean, intuitive diagrams—such as token chips, parallel core arrays, data pipe gauges, and milestone steppers—over dense text bullets. Explanations must be visually obvious in 2 seconds.
