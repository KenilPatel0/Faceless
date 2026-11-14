# TechXKenil Animation Library and Prompt-to-Animation Decision Engine

By Claude for Kenil, TechXKenil. Version 1.0, 14 Nov 2026.

## 0. Read this first

**What this doc is.** A single spec that (1) lists the animation types that are working on Reels, Shorts and TikTok in 2026, (2) says when each one should and should not be used, and (3) defines how the video tool reads a prompt and decides which animations to apply.

**What I could not do.** GitHub blocks automated reading of github.com/techXkenil/faceless, and search did not surface it, so I have **not read the repo's code or README**. Everything in this doc about the current system comes from what you told me in this project (Kokoro am_michael voice, 30 fps, motion + editing skill, humanized skill, brand rules, real-world footage playbook). Section 8 therefore defines the integration as a *contract* (registry + planner + linter) that any renderer can satisfy, and ends with the exact files I need from the repo to turn it into code-level instructions. Paste the README and the folder tree and I will produce the mapping.

**How reliable is the research.** The trend sources are industry roundups and creator-tool blogs, not view-count leaderboards. Several (AutoAE, OpusClip, FluxNote, ClipSpeed) sell tools, and their retention percentages are vendor claims. I use them for *direction* (what styles exist, what pacing is typical), not as proof of exact lift. Numbers marked **[default]** are my own engineering starting points, to be tuned against your YouTube Studio retention graphs.

## 1. What the research says (short version)

1. **Text is the main character.** Kinetic typography is the most-cited motion trend of 2026, largely because most short-form video is watched muted and type carries the message.
2. **Authenticity over polish.** Grain, texture and handmade imperfection are rising; glossy over-produced looks and the heavily produced viral transitions of 2024 and early 2025 are losing ground.
3. **Vertical-first.** Motion is designed for 9:16 from the start (centered text, close framing, quick transitions), not cropped from horizontal.
4. **Each platform rewards a different grammar.** One 2026 guide summarizes it as: Reels tolerates polish, Shorts wants speed, TikTok wants rawness. For Shorts, tighter cuts and simpler motion beat overproduced graphics.
5. **Word-by-word animated captions are now the expected baseline**, not a bonus. Vendors claim 8-40% retention lifts; treat the exact figure as unproven, the direction as consistent.
6. **Retention anchors every 2-3 seconds.** Multiple sources describe a purposeful visual event (bold keyword, step number, underline, cut, zoom) every 2-3 seconds.
7. **Effort vs return.** For faceless channels, kinetic typography is the fastest format to produce and whiteboard/line-draw is the best-trusted for explainers. Complex motion graphics cost hours per short and are not worth it at your volume.
8. **Pick a lane and stay in it.** OpusClip's advice: keep one aesthetic for at least two weeks before judging. This must be balanced against your own rule to vary scenes per video (see section 5.4).

## 2. How the catalog is organized

Every animation has an **ID**, a **purpose**, **use when / avoid when**, **default timing**, **cost** (how heavy it is to render and how much it should be rationed), and **fit** for TechXKenil: **Core** (use constantly), **Situational** (use when the beat calls for it), **Rare** (budgeted, at most once per video), **Skip** (does not suit a faceless, honest-tone channel).

Families: **T** text and captions, **E** explainer visuals, **C** camera and transitions, **S** style layers, **F** format patterns.

## 3. The catalog

### 3.1 T: Text and captions

**T1 Word-highlight captions (karaoke).** Words appear as spoken; the current word is highlighted (yellow or brand purple), earlier words stay white. The most common 2026 caption standard. *Use:* all narration in shorts; long videos only for short bursts. *Avoid:* long videos as the default, since single-word pace gets tiring beyond about a minute (use T2). *Timing:* word-timestamp driven from the TTS or forced alignment; highlight in/out 0-2 frames. *Fit:* Core (shorts).

**T2 Two-line sentence captions.** Phrase or sentence shown in two lines, bottom center, small. *Use:* long videos (matches your rule: captions small at bottom center), and any short beat where T1 would fight another on-screen visual. *Fit:* Core (long).

**T3 Kinetic headline (hero text).** One to five big words that slide, stretch, or snap in, as the visual itself rather than a caption. *Use:* hooks, key claims, section titles, the one-line takeaway. *Avoid:* more than one per 4-5 seconds; text-heavy beats. *Timing:* in 250-350 ms with overshoot ease-out, hold, out 200 ms **[default]**. *Fit:* Core.

**T4 Keyword emphasis.** Inside narration, one word gets a scale-pop, color change, underline sweep, or box highlight. *Use:* the single most important word of a sentence. *Avoid:* more than one emphasized word per sentence. *Fit:* Core.

**T5 Typewriter / terminal text.** Characters type out with a cursor, optionally in a code or terminal frame. *Use:* prompts to an AI, commands, code, "watch what happens when I type this". *Fit:* Core for tech.

**T6 Stat counter.** A number counts up or down with unit and one-line label. *Use:* only for numbers you can verify (your rule: no unverified statistics). *Fit:* Situational.

**T7 Chat / message UI.** Messages appear in bubbles (user prompt, AI reply, typing dots). *Use:* chatbot vs agent explainers, prompt examples, "what you type vs what AI does". *Fit:* Core for AI topics.

**T8 Callout label / lower-third.** Small label with arrow or line pointing at something on screen. *Use:* naming parts of a diagram, a UI, a code block. *Fit:* Core.

### 3.2 E: Explainer visuals

**E1 Line-draw / whiteboard reveal.** Strokes draw in (supersampled, 2x, per your motion skill), simple icons and shapes appear as the voice explains them. *Use:* definitions, "what is X", simple concepts. Whiteboard has a high trust and education feel and works only for information, not entertainment. *Fit:* Core.

**E2 Diagram build (nodes and arrows).** Boxes pop in with a stagger, arrows draw between them, the active node glows. *Use:* any process or architecture: Think-Act-Observe loop, how a chatbot answers, request flow. *Timing:* stagger 80-120 ms per element, arrow draw 400-600 ms **[default]**. *Fit:* Core.

**E3 Split-screen comparison (A vs B).** Two panes, mirrored layout, same attribute rows revealed in sync, a verdict at the end. *Use:* "X vs Y", before/after, myth/fact. *Fit:* Core.

**E4 Numbered cards (listicle).** Large number plus short title, each card slides in; previous card shrinks to a progress stack. *Use:* "5 tips", "7 patterns". *Fit:* Core.

**E5 Chart reveal.** Bars grow or lines draw to the data with the key point highlighted. *Use:* verified numbers only. *Fit:* Situational.

**E6 Code view with diff / highlight.** Syntax-colored code, lines highlight one at a time, additions in green, removals in red, optional zoom on one line. *Use:* AI-writes-code topics, Flutter examples, before/after code. *Fit:* Core for tech.

**E7 Real UI / screen recording with cursor guidance.** A real recording (Playwright for websites, scrcpy or simulator for apps) with smooth cursor path, click ripple, and punch-in on the active region. *Use:* demos and tools. Fits your Real-World Footage Playbook (own captures first). *Fit:* Core for tool videos.

**E8 Search-bar / prompt-box animation.** A search or prompt field with text typed and a result appearing. *Use:* hooks that pose a question, "ask AI this". *Fit:* Situational.

**E9 Timeline / roadmap.** Horizontal or vertical line with milestones lighting up. *Use:* the 90-day plan, history, step sequences over time. *Fit:* Situational.

**E10 Metaphor footage / photo with motion.** Real or public-domain footage or still, slow push-in, used as a metaphor only (your cap: about 40% of runtime, license logged). *Use:* emotional or conceptual beats, scene-setting. *Fit:* Situational.

**E11 Abstract AI visuals (token stream, attention lines, network nodes).** Code-drawn particles, nodes, text tokens flowing into a box. *Use:* "how AI works" explainers where there is nothing real to film. *Avoid:* decoration with no meaning. *Fit:* Situational.

### 3.3 C: Camera and transitions

**C1 Slow push-in (Ken Burns).** 3-6 percent scale over the scene. Required so no frame is static (your max hold: 4 s short, 9 s long). *Fit:* Core, applied to every scene by default.

**C2 Punch-in on beat.** Quick 8-15 percent zoom on the key word or claim. *Use:* one per 5 seconds at most. *Fit:* Core.

**C3 Slide / push transition.** Next scene pushes the previous out along one axis with motion blur on moving layers. *Fit:* Core.

**C4 Match cut / morph.** A shape, icon or text block continues across the cut into the next scene. *Use:* connecting two ideas visually. *Fit:* Situational (higher effort).

**C5 Glitch / RGB split.** 4-8 frame distortion. *Use:* the one punchline or reveal, **at most once per video**. Too much reads as low effort and clashes with your honest tone. *Fit:* Rare.

**C6 Screen shake.** Short decaying shake on the climax. *Use:* at most once per video. *Fit:* Rare.

**C7 Stacked split-screen.** Two or three vertical layers. *Use:* only when two things must be seen at once (a prompt and its output). *Fit:* Rare for your channel.

**C8 J-cut / L-cut.** Audio leads or trails the visual cut. *Fit:* Core (already in your editing skill).

### 3.4 S: Style layers (applied per video, not per scene)

**S1 Brand dark (default).** Your dark navy/purple look with TXK logo, as in the intro/outro rules. *Fit:* Core.

**S2 Light film grain.** Subtle grain and slight color warmth. A 2026 reaction against AI sameness and over-polish. *Use:* real-world footage videos. *Fit:* Situational.

**S3 Liquid glass cards.** Translucent frosted cards with soft depth, matching the 2026 AI and tech brand look. Industry sources call broad adoption beyond Apple unconfirmed, so keep it a style option, not the identity. *Fit:* Situational.

**S4 Cutout / paper craft.** Handmade collage feel. High effort in code. *Fit:* Skip for now.

**S5 Y2K / VHS / chrome.** Ironic nostalgia. Does not fit your calm explainer tone. *Fit:* Skip.

### 3.5 F: Format patterns

These are not effects but structures the planner can select.

**F1 Hook pattern interrupt.** The first 1-2 seconds start mid-action or with a surprising claim, never with the intro card. Your shorts use a hook then a channel intro line, and long videos delay the TXK card until after 30-40 s. *Fit:* Core.

**F2 Seamless loop ending.** Last visual or line connects to the first. *Fit:* Situational for shorts.

**F3 Voice-over plus real footage / screen (Vox-style essay).** Calm voice, info-dense visuals every 8-10 seconds. *Fit:* Core for long videos.

**F4 POV scenario.** "POV: you ask AI to write your login screen". *Fit:* Situational; works with T7 and E6.

**F5 Brainrot stack, greenscreen presenter, hands-only ASMR, talking-head static, UGC review, audio-reactive AI.** All real 2026 aesthetics, but they need a presenter, hands, gameplay layers or trending audio. *Fit:* Skip. Brainrot stacking conflicts with your honest, no-clickbait tone.

## 4. Beat types: how the tool understands a prompt

The tool should not pick animations per prompt. It should split the script into **beats** (one idea each, about 2-6 seconds in a short), classify each beat, then choose animations per beat. The prompt only sets the format, topic and constraints.

### 4.1 Step 1: parse the prompt into a Brief

```json
{
  "format": "short | long",
  "duration_target_s": 30,
  "topic": "AI Agent vs Chatbot",
  "topic_type": "comparison | how_it_works | list | opinion | tool_demo | news | story | tutorial",
  "audience_level": "beginner",
  "has_real_assets": false,
  "style_pack": "S1",
  "constraints": ["no stats", "30 sec"]
}
```

Rules for the parser: if the prompt says "short" or a duration of 60 s or less, format is short (1080x1920); otherwise long (1920x1080). If the user gives a script, use it verbatim. If only a topic, write the script first, then segment. When a field is unclear, **assume the default and record the assumption** in the plan. Do not stop to ask.

### 4.2 Step 2: segment into beats and classify

Each sentence or clause group becomes a beat with exactly one **beat_type**. Detection cues (rule-based first, LLM fallback when ambiguous):

| Beat type | Cues in the text |
| --- | --- |
| hook | first beat; question, surprising claim, "nobody tells you", "why can't" |
| definition | "X is", "means", "simply put" |
| comparison | "vs", "versus", "difference", "while", "instead of", "unlike", "on the other hand" |
| process | "first", "then", "next", "loop", "step", "how it works", "pipeline" |
| list_item | "number one", "tip 3", enumerations |
| stat | a digit with a unit or percent (only if verified) |
| example_prompt | quoted prompt, "you type", "ask it" |
| code | function, class, language names, "commit", "test", "widget" |
| ui_demo | "open", "click", "in the app", tool or site names |
| myth_fact | "myth", "actually", "in reality", "people think" |
| analogy | "like a", "imagine", "think of it as" |
| opinion | "I think", "in my experience", "honestly" (needs an original element, see 5.4) |
| payoff | "so", "that's why", "the takeaway" |
| cta | "subscribe", "comment" |

### 4.3 Step 3: beat type to animation (the decision table)

| Beat type | Primary | Secondary | Avoid |
| --- | --- | --- | --- |
| hook | T3 + C2 on the key word | E8 or T7 if it is a question | E5, E9 |
| definition | E1 or T3 | T8 labels | C5 |
| comparison | E3 | T4 on the differing word | E1 stack of many items |
| process | E2 | T8, C3 between steps | T3 over a diagram |
| list_item | E4 | T4 | E2 |
| stat | T6 or E5 | C2 | unverified numbers |
| example_prompt | T7 or T5 | E8 | E10 |
| code | E6 | T8, E7 | T3 |
| ui_demo | E7 | T8, C2 | E11 |
| myth_fact | E3 (two panes, strike-through on the myth) | T4 | E2 |
| analogy | E10 or E1 icons | C1 | T6 |
| opinion | E10 (footage) or own recording | T4 | E5, E11 |
| payoff | T3 | C2 | new complex visuals |
| cta | outro card | none | everything else |

Captions run underneath all beats: **T1 for shorts, T2 for long**. If a beat's primary visual occupies the lower third, move captions to the safe zone above it instead of dropping them.

### 4.4 Step 4: apply budgets and variety rules

The planner may not output a plan that breaks these (the linter in section 8 enforces them):

- **Retention anchor:** a visible new event (scene change, hero text, emphasis, zoom, diagram step) at least every 3 s in shorts **[default, sources say 2-3 s]** and every 6 s in long videos **[default]**.
- **Max static hold:** 4 s short, 9 s long (your existing rule); C1 push-in covers this when nothing else moves.
- **Scene length:** shorts 2-4 s per scene; long 5-12 s.
- **Heavy effect budget:** C5 and C6 at most once per video each, never in the first 2 s; C4 at most twice in a short.
- **Repeat limit:** the same primary animation ID not more than twice in a row; same transition not more than twice in a row.
- **One idea per screen:** no more than one hero text (T3) visible at once; no T3 during an E2 diagram step.
- **Sound off safe:** every beat must be understandable from visuals plus captions with audio muted.
- **Honesty gate:** T6/E5 require a source note in the plan; otherwise the planner replaces them with T3 (qualitative wording).

## 5. Timing, platform and brand rules

### 5.1 Duration targets

One guide recommends roughly 8-15 s for Shorts motion pieces and 12-20 s for Reels and TikTok; your shorts are 30 s as a deliberate choice, so build them as 8-10 beats of about 3 s. Long videos target 8-10 minutes with the sections already defined in your long-video format.

### 5.2 Platform tuning (same master, small differences)

- **YouTube Shorts:** fastest cuts, simplest motion, T1 captions, no heavy stylization.
- **Instagram Reels:** may add S2 grain or S3 glass for polish; slightly longer holds are fine.
- **TikTok:** rawer feel; allow one extra C2 punch-in; keep text safe from UI overlays. If you publish one master everywhere, render for Shorts and re-time nothing.

### 5.3 Safe zones

Keep captions and hero text inside the central area of the 9:16 frame, clear of the bottom roughly 15 percent and right edge where platform buttons sit **[default, verify against each app's current UI]**.

### 5.4 Variety vs consistency (your rule vs the research)

Research says keep one recognizable lane; your humanized skill says change at least 3 elements versus the previous 3 videos. Reconcile them like this: **the brand layer never changes** (S1 look, intro and outro, voice, caption style family), **the scene layer does** (hook type, primary visual per beat, transition set, color accent, scene order). The planner reads the last 3 plan files and must differ in at least 3 scene-layer elements. Also include at least one original element per video (own recording, own experience, or a clear opinion), as in your humanized rules.

## 6. Prompt-to-plan: the planner contract

### 6.1 Planner system prompt (paste into the tool's planning step)

```text
You are the TechXKenil video planner. Input: a Brief and a script.
Task: split the script into beats, classify each beat, and choose animations ONLY from animations/registry.json.
Rules:
1. One beat_type per beat, from the allowed list.
2. Choose primary and secondary animation IDs using decision_table.json; never invent IDs.
3. Obey budgets in rules.json (anchors, holds, heavy effects, repeats).
4. Captions: T1 for shorts, T2 for long. Brand layer is fixed.
5. Compare with the last 3 plans in /plans/history and differ in at least 3 scene-layer elements.
6. No statistic without a source field. If none, rewrite qualitatively.
7. If the prompt is ambiguous, pick the default, add it to "assumptions", and continue.
8. Output valid JSON matching scene_plan.schema.json and nothing else.
```

### 6.2 Scene plan schema (example)

Prompt: "Make a 30 sec short: AI agent vs chatbot."

```json
{
  "brief": {"format": "short", "duration_target_s": 30, "topic_type": "comparison", "style_pack": "S1"},
  "assumptions": ["beginner audience", "no statistics", "standard intro and outro cards"],
  "beats": [
    {"id": 1, "t": [0.0, 3.0], "beat_type": "hook",
     "text": "Chatbot or agent: what is the difference?",
     "primary": "T3", "secondary": ["C2"], "transition_out": "C3", "captions": "T1"},
    {"id": 2, "t": [3.0, 8.0], "beat_type": "comparison",
     "text": "A chatbot answers. An agent acts.",
     "primary": "E3", "secondary": ["T4:answers,acts"], "transition_out": "C3", "captions": "T1"},
    {"id": 3, "t": [8.0, 15.0], "beat_type": "process",
     "text": "An agent loops: think, act, observe.",
     "primary": "E2", "secondary": ["T8"], "transition_out": "C4", "captions": "T1"},
    {"id": 4, "t": [15.0, 21.0], "beat_type": "example_prompt",
     "text": "Ask: book me a flight.",
     "primary": "T7", "secondary": ["T5"], "transition_out": "C3", "captions": "T1"},
    {"id": 5, "t": [21.0, 25.0], "beat_type": "payoff",
     "text": "Tools and guardrails make it safe.",
     "primary": "T3", "secondary": ["C2"], "effects": ["C5:once"]}
  ],
  "outro": "standard"
}
```

The numbers and timings above are illustrative; the renderer fills real times from the TTS word timestamps.

### 6.3 Fallbacks

- Unknown beat type: treat as definition, use T3 + C1.
- Missing asset (no screen recording available): E7 falls back to E2 or T7; log the swap.
- Renderer does not support an ID yet: replace with the nearest Core ID (E4 to T3, C4 to C3) and flag it in the report.

## 7. Animation specs: the shared motion language

Use one set of primitives so every animation feels like the same studio made it. These are starting values **[default]**.

- **Frame rate:** 30 fps. **Resolution:** 1080x1920 (short), 1920x1080 (long). BT.709 H.264 (already in your skill).
- **Easing:** ease-out-cubic for entrances, ease-in-out for moves, spring (damping about 0.7) for pops and overshoots; never linear except progress bars and counters.
- **Durations:** pop-in 180-250 ms; slide 300-400 ms; stagger 60-90 ms per word or 80-120 ms per node; hold at least 400 ms before an element leaves; transitions 250-350 ms.
- **Motion blur:** only on fast-moving layers (already in your skill); never on text at rest.
- **Supersampling:** 2x for line-draw and vector shapes.
- **Text:** one display font and one body font; hero text 10-14 percent of frame height in shorts; max about 6 words on screen at once for T3.
- **Color:** brand navy/purple base, one accent per video (the varying scene-layer element), highlight color for T1 consistent across all videos.
- **Audio sync:** animation events snap to word timestamps (+/- 2 frames); SFX only on events; music ducked; master about -15 LUFS (already in your humanized skill).
- **Determinism:** every animation takes `(params, start_frame, duration)` and renders the same output each time, so renders are repeatable.

## 8. Implementation plan

### 8.1 Proposed structure (renderer-agnostic)

```text
skills/animation-library/
  SKILL.md                    # how and when to use the library (section 4 and 5 condensed)
  registry.json               # all animation IDs, params, defaults, cost, fit
  decision_table.json         # beat_type -> primary/secondary/avoid (section 4.3)
  rules.json                  # budgets and variety rules (section 4.4)
  scene_plan.schema.json      # JSON schema for plans
  planner_prompt.md           # section 6.1
  animations/                 # one module per ID (T1..T8, E1..E11, C1..C8)
  linter/check_plan.py        # rejects plans that break rules.json
  tests/                      # golden plans and render smoke tests
  plans/history/              # last N plans for variety checks
```

### 8.2 Registry entry contract

```json
{
  "id": "E2",
  "name": "Diagram build",
  "family": "explainer",
  "fit": "core",
  "beat_types": ["process", "comparison"],
  "avoid_beat_types": ["hook"],
  "min_duration_s": 3, "max_duration_s": 12,
  "params": {"nodes": "array", "edges": "array", "highlight_order": "array"},
  "needs_assets": false,
  "cost": "medium",
  "max_per_video": null,
  "formats": ["short", "long"]
}
```

### 8.3 Build order (phases)

1. **Phase 1, foundations (highest value):** T1, T2, T3, T4, C1, C2, C3, E3, E4, plus planner, registry, linter. This alone covers most 2026 patterns for a faceless explainer.
2. **Phase 2, explainer power:** E1, E2, E6, T5, T7, T8, C8.
3. **Phase 3, real-world:** E7 (Playwright, scrcpy, simulator capture with cursor path and punch-in), E10 with license log.
4. **Phase 4, polish and rare:** E5, E8, E9, E11, C4, C5, C6, S2, S3.
5. **Phase 5, learning loop:** after each publish, log retention per beat type and animation ID in a sheet; promote or demote animations by evidence, not trend articles.

### 8.4 Open-source references worth reusing (verify license before copying)

- **Remotion** (React to MP4), with the official `template-tiktok` for Whisper.cpp-based TikTok-style captions, and a community resource list including animation helpers such as remotion-animate-text and remotion-subtitle, and component libraries such as Onda (reported 70 components and 18 transitions) and Remotion Bits. **Licensing note:** Remotion says some entities need a company license; check whether your use falls under it before building on it.
- **HyperFrames** (HTML, CSS and seekable animations to deterministic MP4), with agent skills including a faceless-explainer, motion-graphics and embedded-captions skill. Its HTML-first model suits agent-driven workflows. Check its license and maturity.
- **SwiftClip** (open-source Remotion templates, Claude Code plugin). Its Apple-light styling does not match your dark brand, so use it for structure, not looks.
- Your earlier reference list (short-video-maker, MoneyPrinterTurbo, OpenReels) remains valid for pipeline ideas.

If your current tool is Python/FFmpeg based rather than Remotion or HyperFrames, keep the same registry and planner and implement each animation module in your renderer; the contract does not change.

### 8.5 Linter checks (automated)

1. Every beat has one beat_type and valid IDs from the registry.
2. No static hold above 4 s (short) or 9 s (long).
3. A retention anchor within every 3 s (short) or 6 s (long).
4. C5 and C6 at most once each; none in the first 2 s.
5. No same primary ID more than twice in a row.
6. Caption style matches format (T1 short, T2 long).
7. No stat without source.
8. At least 3 scene-layer differences from the last 3 plans; brand layer unchanged.
9. Intro and outro match the brand rules.
10. Total duration within 5 percent of target.

### 8.6 Acceptance tests

- Same prompt run twice gives valid plans that differ in scene-layer elements only when history changes.
- A comparison prompt yields E3 in the comparison beat; a process prompt yields E2; a prompt with a quoted prompt yields T7 or T5.
- A prompt with no assets never selects E7.
- A prompt containing an unverified number is rewritten without the number.
- Muted playback of the render still communicates every beat.

## 9. What I need from the repo to finish the mapping

Please paste: (1) the README, (2) the folder tree, (3) how a scene or script is currently defined (a sample input file), (4) which renderer it uses (Python with FFmpeg or Pillow, Remotion, HTML-to-video, or something else), and (5) where the caption and transition code lives. With those I will convert sections 7 and 8 into file-level tasks and a ready SKILL.md plus registry.json for Antigravity.

## 10. Sources used

- AutoAE, Motion Graphics Trends 2026 (compiles Envato, GraphicDesignJunction, MonkyVision, Senate Media, Clipchamp, NewEngen).
- GraphicDesignJunction, Video and Motion Creative Trends 2026.
- OpusClip, 11 Editing Aesthetics Dominating Short-Form in 2026, and the OpusClip brainrot-style guide.
- Mirra, AI Motion Graphics for Social Media (platform grammar and duration guidance).
- FluxNote, Animated Shorts 2026 guide (effort and format comparison) and its caption guides (vendor claims).
- Influencers Time, Kinetic Typography articles (retention anchors every 2-3 seconds).
- Eliro, 12 Caption Styles (word-highlight vs sentence captions).
- Remotion docs resource list and template-tiktok; HyperFrames repository descriptions; SwiftClip repository.
- github.com/techXkenil/faceless: **not readable by automated access, not reviewed**.
