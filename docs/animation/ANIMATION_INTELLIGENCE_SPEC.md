---
title: "Faceless — Animation Intelligence & Motion Graphics System"
subtitle: "Research-backed taxonomy, decision system, implementation specification and QA contract"
date: "14 November 2026"
---

# Faceless — Animation Intelligence & Motion Graphics System

**Project:** TechXKenil / Faceless  
**Document:** Research-backed taxonomy, decision system, implementation specification and QA contract  
**Prepared:** 14 November 2026  
**Status:** Proposed engineering specification — repository source audit still required  
**Target outputs:** Instagram Reels, YouTube Shorts and configurable long-form video formats

---

## Executive summary

Faceless should not become a renderer that applies a large number of effects at random. It should become a **story-aware motion direction system**: the user provides a prompt, script or topic; the system interprets the communication goal; it plans scenes and visual beats; it selects a visual treatment and specific motion techniques; it schedules them against narration and music; and the existing renderer executes and validates the result.

The research leads to five design decisions:

1. **Separate editing grammar from animation primitives.** A jump cut, a kinetic caption, a shape morph and a camera push are different kinds of production decisions. They must not be mixed into one flat list.
2. **Choose motion to explain or emphasize meaning.** The subject, verb, number, comparison, emotion and story beat should drive the visual choice.
3. **Treat short-form patterns as adaptable formats, not viral guarantees.** Official YouTube guidance emphasizes hooks, concise standalone stories, captions, pacing experiments and analytics. Instagram directs creators to its evolving, personalized Best Practices guidance. Neither platform says that a particular transition or effect guarantees reach.
4. **Use a metadata-driven animation registry and a separate Animation Director.** The planner decides what should happen; the renderer performs deterministic frame calculations.
5. **Measure and review real outputs.** Generate contact sheets, previews and test renders; use channel analytics to learn which creative treatments work for the specific audience.

> **Core principle:** The Animation Director decides *what moves, why, when, and how strongly*. The motion/rendering engine decides *how to calculate and render that movement*.

## Research scope, method and limits

This specification synthesizes three kinds of evidence:

- **Platform guidance:** official Instagram/Meta and YouTube creator guidance about hooks, short-form storytelling, captions, vertical framing, creative experimentation and analytics.
- **Motion-design and animation practice:** established animation principles and current technical documentation from Adobe, Remotion, GSAP, Lottie, Rive and FFmpeg.
- **Engineering recommendations:** proposed architecture, schemas, selection rules and QA standards designed for Faceless. These are recommendations to implement and validate, not claims made by the platforms or libraries.

### Important scope note

There is no finite, authoritative list of every animation ever used in Instagram Reels or YouTube Shorts. New templates, editing styles and meme formats appear continuously, and trends differ by language, niche, creator and region. This document therefore provides a **broad, practical catalog of reusable techniques and short-form visual formats**, with a registry designed to grow over time.

This research did not perform an exhaustive scrape or statistically representative sample of Reels and Shorts. It does not claim that the listed techniques are the most-used or currently most-viral effects. Platform references are cited individually; engineering rules are explicitly presented as proposed defaults. The research log should be refreshed periodically using a small, manually reviewed sample of current videos from the channel's target niches.

---

# Part I — What the system is designing

## 1. A useful vocabulary: four distinct layers

The previous proposal grouped all visual motion into animation families. That is a useful start, but implementation needs a more precise model.

| Layer | Meaning | Examples | Owner |
|---|---|---|---|
| **Editorial grammar** | How shots and information are cut and arranged | Jump cut, cutaway, J-cut, L-cut, match cut, split screen, speed ramp | Scene/editor planner |
| **Visual format / treatment** | The overall way a story is represented | Text-led explainer, documentary B-roll, screen-recording tutorial, kinetic infographic, illustrated story | Style/format planner |
| **Animation treatment** | A recognizable motion behavior applied to an element or group | Word-pop caption, typewriter, bar-growth chart, phone mock-up reveal, parallax stack | Animation Director |
| **Motion primitive** | Low-level property or rendering operation | Position, scale, rotation, opacity, path, mask, blur, stroke reveal, particle update | Motion engine |

A style can contain multiple treatments; each treatment can use multiple primitives. A jump cut is not an animation primitive. A counter roll is not an entire visual style. Keeping these concepts separate avoids a bloated, confusing registry.

## 2. Short-form platform findings

### YouTube Shorts

YouTube's creator guidance describes short-form as a concise storytelling format: identify the strongest moment, use an engaging hook, make a Short understandable on its own, consider captions and text overlays, experiment with speed changes and audio, and review analytics. A YouTube creator interview discusses hooking a viewer in the first second; that is creator advice, not a universal platform guarantee. YouTube's 2025 Shorts advice also warns against depending on trends alone: trends can be a starting point, while distinct stories and a recognizable voice have longer-term value. [1][2][3]

YouTube currently documents Shorts as square or vertical videos up to three minutes for eligible uploads. Faceless should keep platform constraints in versioned export profiles rather than hardcoding a duration into the animation engine. [4]

### Instagram Reels

Meta's Instagram Best Practices hub covers creation, engagement, reach, monetization and guidelines, with personalized recommendations that may change over time. This is a reason to keep Reels export/profile settings configurable and to review current in-app guidance rather than treating a static blog post as a permanent algorithm rule. [5]

### Practical implications for Faceless

- Make the opening visual legible immediately: a strong statement, question, result, unusual image or active demonstration can be a hook. Do not automatically add a loud zoom or glitch to every opening.
- Give each Short a self-contained narrative arc: hook → context → development/proof → payoff/conclusion.
- Use captions as an accessibility and comprehension layer, not merely decoration. YouTube recommends captions/text overlays for short-form repurposing; keep them readable and positioned away from platform UI. [2]
- Prefer original visual interpretation over copying a creator's exact edit, footage, graphic layout or branded template. Study the technique, then create a new execution. YouTube's creator guidance recommends building a distinct path instead of leaning exclusively on trends. [1]
- Treat performance as an experiment. Record the selected style, hook type, visual density and motion treatments alongside retention/engagement outcomes. Do not label a style “viral” just because it looks energetic.
- Use a platform profile to control aspect ratio, safe areas, caption placement and output duration. Current UI overlays and platform rules can change.

## 3. Visual formats the prompt planner should recognize

These are **formats**, not one-off effects. A format is a reusable visual grammar that may combine footage, typography, graphics and transitions.

| Format ID | Format | Best suited to | Common visual language |
|---|---|---|---|
| `text_led_hook` | Large text-led hook | Contrarian claim, question, key fact | Oversized headline, selective word emphasis, supporting visual |
| `kinetic_explainer` | Kinetic typography explainer | Narration-led education | Phrase/word reveals, diagrams, callouts |
| `documentary_broll` | Documentary / cinematic B-roll | History, business, science, biography | Footage, slow reframing, labels, timelines, restrained transitions |
| `screen_tutorial` | Screen-recording tutorial | Software, coding, AI tools | Crop/pan, cursor focus, step labels, terminal/UI callouts |
| `ui_product_demo` | Product/interface showcase | App or feature explanation | Device frames, tap/click feedback, state changes, feature labels |
| `data_story` | Data-led explainer | Research, statistics, business | Counters, charts, scale comparisons, source labels |
| `process_diagram` | Process/architecture explainer | Workflows, systems, AI agents | Nodes, arrows, progressive connections, grouped stages |
| `illustrated_story` | Illustrated or cut-out story | Simple narratives and metaphors | 2D objects/characters, paper layers, scene changes |
| `myth_vs_fact` | Myth / fact comparison | Misconceptions, debunking | Side-by-side panels, strike-through, reveal, evidence card |
| `before_after` | Before/after transformation | Product, process, outcome | Split reveal, wipe, synchronized comparison |
| `ranked_list` | List/ranking | Tips, tools, top-N | Numbered cards, staggered reveals, progress marker |
| `timeline_story` | Timeline narrative | History, milestones, roadmaps | Date labels, line draw, image cards, camera travel |
| `visual_metaphor` | Conceptual metaphor | Abstract ideas | Physicalized objects, morphs, cause-and-effect |
| `meme_commentary` | Meme/reaction overlay | Humor or informal commentary | Reaction crops, labels, freeze frames, deliberate timing |
| `quote_story` | Quote / statement | A memorable claim or conclusion | Typography, attribution, subtle texture and emphasis |
| `looping_process` | Seamless loop | Repeatable process or satisfying sequence | Matched start/end states, continuous movement |

The Director may blend formats, but it should choose one **primary format per scene** and explain why. Avoid switching visual language every few seconds unless the script intentionally changes mode.

---

# Part II — Animation catalog

## 4. How to read the catalog

Each technique is a candidate for the registry. Not every catalog item requires a unique rendering implementation. Many should be parameterized presets built from a small number of primitives.

Complexity labels:

- **L** — low: transforms, opacity, simple text or vector properties.
- **M** — medium: masks, paths, chart geometry, multiple synchronized layers.
- **H** — high: 3D, dense particles, complex compositing, advanced tracking or character rigs.

For each animation, the registry should eventually record: ID, behavior, purpose, trigger signals, compatible assets, parameters, timing range, layer needs, complexity, fallback, and validation rules.

## 5. Typography and text animation

Use typography for meaning, emphasis and hierarchy. Keep the original sentence accurate; do not rewrite facts merely to make a visual effect fit.

| Technique | ID | Good use | Complexity |
|---|---|---|---|
| Word-by-word pop | `type.word_pop` | A key phrase or strongly paced spoken line | L |
| Karaoke progress highlight | `type.karaoke_highlight` | Speech-following captions | L |
| Phrase/chunk reveal | `type.phrase_reveal` | Captions that should remain readable as phrases | L |
| Character/typewriter reveal | `type.typewriter` | Terminal text, suspense, short labels | L |
| Character stagger | `type.character_stagger` | Short titles and hero words | L |
| Line-by-line reveal | `type.line_reveal` | Headlines and explanatory cards | L |
| Scale punch | `type.scale_punch` | One important word or number | L |
| Bounce/elastic entrance | `type.bounce_in` | Playful or energetic content | L |
| Slide/track reveal | `type.track_reveal` | Editorial headings and lower thirds | L |
| Masked text reveal | `type.mask_reveal` | Premium titles and transitions | M |
| Text wipe / clipping | `type.text_wipe` | Section changes and short labels | M |
| Split/duplicate typography | `type.split_type` | Comparison, contrast, multi-part title | M |
| Outline/stroke draw | `type.stroke_draw` | Technical labels and designed title cards | M |
| 3D flip / extrusion | `type.type_3d` | Hero title, selected impact moment | H |
| Rotating/rolling text | `type.roll` | Numeric or short label changes | M |
| Scramble/decode | `type.decode` | Code, security or digital reveal | M |
| Glitch typography | `type.glitch` | Digital failure or distortion context | M |
| Perspective/tilt type | `type.perspective` | High-impact editorial typography | M |
| Freeze + annotation | `type.freeze_annotation` | Explain a word/claim while holding a frame | L |
| Lower-third / nameplate | `type.lower_third` | Names, roles, sources, attribution | L |

**Rules:** captions should follow transcript/word timing when available; a phrase-level mode should be used when word-level movement harms readability. Emphasize only selected semantic words, not every word. Do not allow animated captions to collide with lower UI controls. Provide a stable static caption fallback.

Adobe's text animation documentation supports animating text as a whole or by character/range using text animators and selectors; it also notes that per-character 3D properties can add rendering cost. This supports a registry design with shared text primitives rather than one hand-coded preset per effect. [6]

## 6. Camera, framing and image movement

| Technique | ID | Good use | Complexity |
|---|---|---|---|
| Slow push-in | `camera.push_in` | Emphasis, subject reveal, dramatic detail | L |
| Pull-out | `camera.pull_out` | Reveal context or scale | L |
| Pan left/right | `camera.pan` | Move across a scene or screenshot | L |
| Tilt up/down | `camera.tilt` | Reveal height or vertical hierarchy | L |
| Ken Burns motion | `camera.ken_burns` | Still images and archival photos | L |
| Reframe / crop follow | `camera.reframe` | Focus on a UI or image detail | L–M |
| Parallax camera | `camera.parallax` | Separate foreground/midground/background | M |
| Orbit / arc move | `camera.orbit` | Product/illustration hero shot | M–H |
| Roll / dutch tilt | `camera.roll` | Unease or stylized transition | M |
| Handheld micro-jitter | `camera.handheld` | Documentary/live feel | M |
| Whip pan | `camera.whip_pan` | Energetic transition or action connection | M |
| Rack-focus simulation | `camera.focus_pull` | Focus shift between layers | M |
| Punch-in / punch-out | `camera.punch` | Emphasis or reaction beat | L |
| Split-screen reframe | `camera.split_reframe` | Compare two states | M |
| Motion-follow crop | `camera.follow_subject` | Follow object within a larger frame | H if tracking is needed |

**Rules:** the camera move must preserve the important subject and safe margins. A still image should not receive a push-in just because the system can do it. Use motion when the image contains visual detail to reveal or the narrative calls for focus or scale.

## 7. Object entrances, exits and choreography

| Technique | ID | Good use | Complexity |
|---|---|---|---|
| Fade in/out | `object.fade` | Quiet or neutral entrance | L |
| Slide in/out | `object.slide` | Cards, labels, panels | L |
| Scale in/out | `object.scale` | Icons, numbers, callouts | L |
| Pop with overshoot | `object.pop_overshoot` | Small emphasis, playful UI | L |
| Rotate in/out | `object.rotate` | Cards, logos, diagram pieces | L |
| Flip | `object.flip` | Two-sided card or state change | M |
| Drop / fall | `object.drop` | Object metaphor, impact | L–M |
| Float / drift | `object.float` | Background accents, calm scene | L |
| Follow-through | `object.follow_through` | Secondary elements settle after main object | M |
| Staggered group entrance | `object.stagger` | List, cards, diagram nodes | M |
| Path-follow movement | `object.motion_path` | Flow, travel, movement along a route | M |
| Orbiting object | `object.orbit` | Hub-and-spoke or planetary metaphor | M |
| Assembly / disassembly | `object.assemble` | Product, system, component explainer | M–H |
| State transformation | `object.state_change` | Before/after, process stages | M |
| Bounce/impact | `object.impact` | Physical metaphor or UI confirmation | M |

**Rules:** use anticipation for large moves, settle motion at the end, and avoid unnecessary bouncing. One primary object should lead; supporting objects can follow with smaller amplitude or a slight delay.

## 8. Shape, vector and line animation

| Technique | ID | Good use | Complexity |
|---|---|---|---|
| Stroke/path draw | `shape.path_draw` | Flow lines, icons, underlines | M |
| Trim-path reveal | `shape.trim_reveal` | Diagrams and icon drawing | M |
| Shape expansion | `shape.expand` | Highlight regions and cards | L |
| Shape collapse | `shape.collapse` | Dismissal or transition | L |
| Circle/ring reveal | `shape.iris_reveal` | Focus reveal or data ring | M |
| Rectangle/line wipe | `shape.wipe` | Simple transitions | L–M |
| Shape morph | `shape.morph` | Explain transformation or changing state | M–H |
| Liquid/goo morph | `shape.liquid_morph` | Playful, organic or fluid visual | H |
| Blob/organic movement | `shape.blob` | Abstract concept and background | M |
| Repeater / pattern build | `shape.repeater` | Multiplication, grids, repeated items | M |
| Grid draw | `shape.grid_draw` | Technical interface or layout | L |
| Animated underline | `shape.underline` | Emphasize word/title | L |
| Bracket/callout draw | `shape.callout_draw` | Point to a visual detail | L–M |
| Geometric split | `shape.split` | Reveal or comparison | M |
| Shape-based mask | `shape.mask` | Scene transition or photo reveal | M |

GSAP's MotionPath and MorphSVG documentation are useful references for path-following and SVG path morphing. These are technique references; adopting GSAP is not required for a Python/FFmpeg implementation. [7][8]

## 9. Masks, reveals and transitions

Treat transitions as editorial decisions between two shots, not as decoration to attach to every cut.

| Technique | ID | Good use | Complexity |
|---|---|---|---|
| Hard cut | `transition.cut` | Default; maintain pace | L |
| Cross dissolve | `transition.dissolve` | Time passage or soft continuity | L |
| Fade through black/white | `transition.fade_color` | Chapter shift or pause | L |
| Dip to color | `transition.dip_color` | Brand accent or deliberate section break | L |
| Directional wipe | `transition.directional_wipe` | Movement into next scene | M |
| Push/slide transition | `transition.push` | Card/page movement | L–M |
| Zoom transition | `transition.zoom` | Connect detail to wider context | M |
| Whip-pan transition | `transition.whip_pan` | Fast action connection | M |
| Match cut | `transition.match_cut` | Similar shape, composition or action across scenes | M (planning) |
| Action match cut | `transition.action_match` | Continue an object/action across shots | M |
| Shape morph transition | `transition.morph` | Transform one graphic into another | M–H |
| Mask/occlusion wipe | `transition.occlusion` | Foreground object passes over lens | M |
| Iris/circle reveal | `transition.iris` | Focused reveal or playful format | M |
| Split-panel transition | `transition.split_panel` | Compare or reorganize information | M |
| Glitch/digital cut | `transition.glitch` | Technology/error context | M |
| Distortion/liquid transition | `transition.distortion` | Stylized change of scene | H |
| Light leak / flare | `transition.light_leak` | Filmic transition, used sparingly | M |
| Speed-ramp transition | `transition.speed_ramp` | Dynamic footage/action | M–H |
| Motion-blur smear | `transition.smear` | Directional high-speed movement | H |
| Freeze-frame cut | `transition.freeze_cut` | Pause, annotate, then continue | L–M |
| L-cut / J-cut | `transition.audio_lead_lag` | Audio continuity across visual change | L (audio timeline) |
| Seamless loop cut | `transition.loop_match` | Return to opening composition/action | M |

**Selection rule:** use a hard cut as the baseline. Choose a designed transition only when it expresses continuity, contrast, time, movement, emphasis or a section change. Limit complex transitions within a scene unless the requested style is intentionally high-energy.

## 10. Footage, photo and editorial motion

These techniques are important because a faceless video often combines motion graphics with real images or video clips.

| Technique | ID | Good use | Complexity |
|---|---|---|---|
| B-roll cutaway | `edit.broll_cutaway` | Show the thing being discussed | L (requires asset planning) |
| Jump cut | `edit.jump_cut` | Remove pauses and tighten speech | L |
| Punch-in jump cut | `edit.punch_cut` | Renew focus on a key phrase | L |
| Reaction cutaway | `edit.reaction_cut` | Humor, surprise, response | L |
| Freeze frame + label | `edit.freeze_label` | Explain a detail or emphasize a result | L |
| Speed-up | `edit.speed_up` | Compress repetitive action | M |
| Slow motion | `edit.slow_motion` | Emphasize a physical moment | M |
| Speed ramp | `edit.speed_ramp` | Move from fast to slow or slow to fast | M–H |
| Time remapping | `edit.time_remap` | Precisely shape clip speed | M |
| Reverse playback | `edit.reverse` | Reveal cause or undo an action | M |
| Loop/repeat | `edit.repeat` | Demonstrate a process or create emphasis | L |
| Split-screen comparison | `edit.split_screen` | Two versions/states at once | M |
| Picture-in-picture | `edit.picture_in_picture` | Evidence, screen recording, secondary source | M |
| Collage/montage | `edit.collage` | Multiple fast visual references | M |
| Contact sheet / grid reveal | `edit.grid_montage` | Many examples at once | M |
| Photo stack / editorial cards | `edit.photo_stack` | Archives, references, story beats | M |
| Pan-and-scan | `edit.pan_scan` | Reframe landscape media into vertical | L–M |
| Parallax still | `edit.parallax_still` | Add depth to a still image | M |

**Rules:** B-roll must illustrate the spoken subject, not simply fill empty space. Preserve real-world evidence and labels. Never fabricate a screenshot, chart, product UI or documentary image as if it were real evidence.

## 11. Captions, labels and screen annotations

Caption systems should be independent of the animation registry's general typography family because they have speech timing, wrapping and readability constraints.

- Word-synced karaoke captions.
- Phrase-level captions.
- Two-line subtitle blocks.
- Active-word color emphasis.
- Keyword callout captions.
- Speaker labels and lower thirds.
- Source/citation cards.
- Numbered step labels.
- Pointer arrows and circles.
- Magnifier windows.
- Highlight boxes and focus dimming.
- Underline, strike-through and bracket annotations.
- Progress indicators / chapter markers.
- Side notes and definition cards.

Caption timing must use actual word/phrase timestamps where possible. If speech recognition or alignment is uncertain, fall back to phrase-level captions rather than producing rapidly changing incorrect words. Do not treat the captions as the only carrier of critical information.

## 12. Charts, statistics and data visualization

| Technique | ID | Good use | Complexity |
|---|---|---|---|
| Count-up / count-down | `data.counter` | One key metric | L |
| Rolling number | `data.counter_roll` | Numeric reveal | M |
| Bar chart grow | `data.bar_grow` | Compare quantities | M |
| Stacked bar build | `data.stacked_bar` | Parts of a total | M |
| Line chart draw | `data.line_draw` | Change over time | M |
| Area chart reveal | `data.area_reveal` | Trend/volume | M |
| Pie/donut sweep | `data.donut_sweep` | Part-to-whole | M |
| Progress ring | `data.progress_ring` | Completion/percentage | M |
| Gauge / meter | `data.gauge` | Threshold or score | M |
| Ranking reveal | `data.ranking` | Leaderboard / top-N | M |
| Data callout | `data.callout` | Highlight one metric | L |
| Scale comparison | `data.scale_compare` | Size, time, money, capacity | M |
| Animated table | `data.table_reveal` | Small comparison table | M |
| Map / route draw | `data.map_route` | Geography or journey | H if geodata is needed |
| Timeline chart | `data.timeline` | Milestones and dates | M |

**Accuracy rules:** values, units, labels, source and time range must come from verified scene data. Never invent intermediate values to make an animation smooth. Interpolate only visual geometry between known data points; do not imply unprovided measurements.

## 13. Diagrams, technical and educational graphics

- Sequential process steps.
- Flowchart build/reveal.
- Node-and-edge network build.
- Architecture stack/layer build.
- Data packet / signal flow.
- Pipeline conveyor / stage handoff.
- Branching decision tree.
- Before/after system diagram.
- Component assembly/explosion.
- Callout and leader-line drawing.
- Cause-and-effect chain.
- Venn / overlap reveal.
- Pyramid/hierarchy build.
- Funnel conversion.
- Timeline with milestones.
- State machine / loop diagram.
- Formula/equation build.
- Code-to-output transformation.
- Terminal command/result sequence.
- Comparison matrix / feature grid.

Use progressive disclosure: reveal the portion being discussed, keep prior context visible when necessary, and avoid displaying an entire dense diagram before the viewer knows what to look at.

## 14. Software UI, product and coding animation

- Browser/window frame entrance.
- App/device mock-up reveal.
- Cursor move and click ripple.
- Tap/press feedback.
- Button state change.
- Dropdown/menu open and close.
- Modal/dialog reveal.
- Scroll through a page.
- Pan/zoom into a UI region.
- Feature highlight box.
- Tooltip/callout.
- Notification toast.
- Loading/progress state.
- Terminal typing and command execution.
- Code line highlight / current-line focus.
- Diff view / before-after code.
- Syntax token highlight.
- Error-state to resolved-state transition.
- API request/response visualization.
- Data flow between connected services.
- Device frame / screen replacement.

**Trust rule:** if the narration refers to a specific product, use the actual supplied/captured UI or a clearly labeled conceptual mock-up. The renderer must not invent an authentic-looking UI for a named product and present it as a real capture.

## 15. Illustration, character and paper/collage motion

- Flat vector illustration build.
- Icon draw-on.
- Hand-drawn doodle reveal.
- Whiteboard line drawing.
- Cut-paper / layered collage movement.
- Sticker/label placement.
- Puppet/rigged character motion.
- Simple character walk, point, nod or gesture.
- Facial expression change.
- Mouth-sync / talking character (only when voice and asset workflow support it).
- Object acting / personified object.
- Scene-to-scene illustration morph.
- Stop-motion-like stepped motion.
- Scribble / marker annotation.
- Silhouette-to-detail reveal.

Choose this family when a human explanation or concrete metaphor is clearer than abstract text. Character animation is a high-maintenance content style: reuse consistent rigs and limit generated one-off character assets.

## 16. Depth, 2.5D and 3D

**2.5D / layered depth:** foreground-background separation, camera parallax, depth-scaled layers, perspective card tilt, layered image fly-through, depth-of-field simulation, multi-plane scroll, and offset shadows.

**3D / pseudo-3D:** product turntable, object rotation, camera orbit, 3D title extrusion, cube/card rotation, exploded product view, object assembly, volumetric typography, lighting sweep and 3D scene fly-through.

Start with 2.5D when the source images can be separated reliably. Use full 3D only when the message benefits from geometry that cannot be represented credibly with 2D layers. Per-character 3D text and complex 3D effects should be treated as higher-cost operations. [6]

## 17. Effects, particles and compositing

- Motion blur.
- Directional blur.
- Gaussian/soft blur.
- Focus blur / depth-of-field simulation.
- Glow / bloom.
- Light streaks.
- Lens flare.
- Vignette.
- Film grain.
- Chromatic aberration.
- RGB split.
- Scanlines.
- Digital noise / static.
- Glitch displacement.
- Pixel sort / block displacement.
- Wave / ripple distortion.
- Heat haze / shimmer.
- Liquid distortion.
- Smoke/fog overlay.
- Dust / floating specks.
- Spark / embers.
- Energy burst.
- Digital rain / matrix-like data fall.
- Particle stream / trail.
- Particle dissolve / assemble.
- Confetti burst.
- Radial rays / burst.
- Light sweep.
- Reflection / sheen.
- Shadow / drop-shadow animation.
- Film burn / light leak.

Use effects to reinforce the visual concept. For example, scanline/glitch may fit a system error or corrupted-data scene; it is not a default treatment for a normal explanation. Keep flashes controlled and avoid repetitive high-contrast strobing.

## 18. Audio-reactive and sound-synchronized motion

- Beat-triggered scale pulse.
- Transient-triggered impact.
- Waveform / amplitude visualization.
- Spectrum/equalizer bars.
- Bass-driven camera or graphic pulse.
- Particle emission tied to audio energy.
- Word/phrase-synchronized caption emphasis.
- Sound-effect-synchronized pop, hit or reveal.
- Music-section transition marker.
- Silence/voice-pause hold.

**Priority order:** narration alignment first, meaningful sound effects second, music beat matching third. Do not move every visual to every beat. Avoid using copyrighted/trending tracks unless the user supplies or licenses them and the publishing workflow allows it.

## 19. Social-native editorial patterns

These patterns are included because many apparent “animations” in short-form videos are actually edits, compositing, and overlay conventions:

- Fast jump-cut narration.
- Punch-in on key phrase.
- Punch-out to reset context.
- B-roll over narration.
- Freeze-frame with annotation.
- Large headline + small supporting caption.
- Word-by-word or phrase-by-phrase captions.
- Two-column comparison.
- Split-screen reaction/response.
- Picture-in-picture demo.
- Listicle with numbered progress.
- Myth/fact reveal.
- Question → evidence → answer.
- “What changed?” before/after sequence.
- Screen-recording with cursor emphasis.
- POV / story-time text overlay.
- Meme/reaction cutaway.
- Fast montage / visual proof stack.
- Countdown / progress-to-payoff.
- Looping end-frame that connects to the opener.

These are not all appropriate for Faceless's default technical voice. Add them as selectable format presets with suitability rules.

---

# Part III — Principles, timing and visual grammar

## 20. Motion principles every preset must respect

Apply the classic principles of animation as quality constraints, adapted for motion graphics:

1. **Squash and stretch:** controlled deformation can imply impact, flexibility or weight; preserve visual identity and volume where appropriate.
2. **Anticipation:** prepare a major action with a small cue when it improves readability.
3. **Staging:** keep the primary subject visually dominant; composition, contrast and camera framing direct attention.
4. **Straight-ahead / pose-to-pose:** use deterministic key poses for planned motion; use continuous simulation only when necessary.
5. **Follow-through and overlap:** secondary elements can settle after the main object, rather than stopping mechanically together.
6. **Slow in / slow out:** acceleration and deceleration create a more intentional movement than constant-speed motion for most entrances.
7. **Arcs:** use curved paths when they represent natural or designed movement better than straight travel.
8. **Secondary action:** add only subordinate motion that supports, not competes with, the main action.
9. **Timing:** frame spacing controls perceived speed, weight and mood.
10. **Exaggeration:** amplify selectively for clarity and impact, not by default.
11. **Solid form / dimensional consistency:** maintain believable volume, perspective and layer relationships.
12. **Appeal:** visuals should be coherent, legible and memorable for the intended audience.

Adobe's overview describes these as foundational principles and explains their use in digital animation and motion design. [9]

Additional motion-design rules:

- Staging before ornament: the viewer should know where to look.
- Readability before speed: don't force a viewer to decode several moving elements simultaneously.
- Causal continuity: a moved object should have a reason to move.
- Visual hierarchy: one primary event per beat; supporting motion stays subordinate.
- Stable typography: keep line lengths, font weight, contrast and safe margins readable.
- Respect weight: a heavy card should not behave like a feather unless the style is intentionally surreal.
- Motion consistency: objects from one visual system should share related easing and physical behavior.
- Avoid randomization in render paths: the same input and frame should produce the same output.

## 21. Timing: do not hardcode one duration for every animation

The earlier proposal's timing ranges are useful as starting presets, but they are not universal rules. Actual durations must derive from available narration time, semantic importance, screen complexity, reading time and transition overlap.

Use this priority order:

1. **Speech timing:** anchor visuals to actual word/phrase timestamps when available.
2. **Semantic boundaries:** start a visual as the corresponding idea begins, not merely at an arbitrary scene midpoint.
3. **Reading time:** keep a text card visible long enough to read. Longer copy requires longer holds or fewer words.
4. **Action completion:** allow an animation to settle before asking the viewer to interpret its final state.
5. **Pacing:** faster cuts are a style choice, not a universal short-form requirement.
6. **Frame quantization:** author time in seconds, convert to integer frames using the active frame rate, and define rounding rules centrally.

### Initial timing presets (tunable, not platform rules)

| Motion class | Starting design range | Notes |
|---|---:|---|
| Tiny UI feedback | 0.10–0.25 s | Click, toggle, small highlight |
| Caption/word emphasis | 0.10–0.35 s | Must follow speech and remain readable |
| Text/card entrance | 0.20–0.55 s | Use less for simple UI, more for a dramatic title |
| Object entrance | 0.25–0.70 s | Include settle time if overshoot is used |
| Data/diagram build | 0.50–1.80 s | Match narration and information complexity |
| Camera reframe | 0.40–1.50 s | Use longer for cinematic travel |
| Major reveal | 0.35–1.20 s | Includes anticipation and settle where appropriate |
| Scene transition | 0.15–0.60 s | Hard cuts have zero transition duration |
| Long cinematic move | 1.00–3.00 s | Use only if the scene has enough visual detail |

These are initial values for first-run presets and must be tested with Faceless's renderer and actual voice styles. They are not claimed to be measured social-platform optimums.

### Timeline rules

- Store time in seconds in the authoring/plan format; convert to frames at render time using rational FPS (for example `30000/1001` when configured), not an assumed integer.
- Use half-open intervals `[start_frame, end_frame)` to avoid duplicated boundary frames.
- Clamp or explicitly define extrapolation outside a keyframe range.
- For overlapping timelines, use named labels and relative offsets rather than repeated hand-calculated delays.
- Keep transition overlap explicit so scene durations add up correctly.
- Distinguish source-clip time from project timeline time when speed ramps or retiming are used.
- Use deterministic seeds for procedural particle/variation effects and record the seed in the render manifest.

Remotion's documentation demonstrates frame-driven interpolation and spring calculations; GSAP's timeline documentation explains sequencing, labels and overlap. These are good reference models for deterministic timeline contracts even though Faceless may implement the calculations in Python. [10][11]

## 22. Motion intensity and density budget

Retain a 0–4 intensity scale, but define it behaviorally:

| Level | Name | Behavior |
|---|---|---|
| 0 | Static | Still frame or intentional hold; only required cuts/caption updates |
| 1 | Subtle | Small drift, restrained reveal, low-amplitude camera move |
| 2 | Standard | Clear entrances, ordinary text/diagram motion, moderate reframe |
| 3 | Dynamic | Stronger kinetic text, staggered builds, quicker cuts, deliberate impact |
| 4 | Hero impact | Short, exceptional accent for hook/payoff; not a continuous mode |

Track **motion density** separately from intensity. A scene can be Level 2 but still too crowded if many elements move simultaneously.

Initial proposed density guardrails:

- One primary motion event per beat.
- Up to two supporting motion events when they have distinct roles (for example, counter + pointer).
- Avoid concurrent camera moves on the same composite unless deliberately nested.
- Do not animate all captions, icons, particles and background layers at maximum amplitude at once.
- Reserve Level 4 for a limited number of meaningful events per video; tune by editorial review, not arbitrary quota enforcement.
- Allow low-motion and static scenes as intentional contrast.

## 23. Transitions and continuity rules

- Prefer a clean cut when the story changes subject or evidence.
- Prefer match cuts when the next scene visually or conceptually continues the previous one.
- Use J-cuts/L-cuts to keep narration or sound continuous across a visual edit.
- Use wipes/pushes when spatial movement or a chapter boundary is part of the visual story.
- Use morphs when one state genuinely transforms into another.
- Use glitches for digital interference, not as an all-purpose “tech” transition.
- Use speed ramps only when source motion supports retiming and audio is handled deliberately.
- Use loop matches when the content benefits from a seamless replay; do not compromise the final conclusion just to force a loop.

## 24. Audio and beat synchronization

The system should build an audio event map from the final narration/music mix or its component tracks.

- Speech words/phrases: caption timing and semantic visual triggers.
- Speech pauses: holds, scene changes or breathing room.
- Stressed syllables/phrases: selective text emphasis, not automatic zoom for every stress.
- Sound effects: visual impact at the actual transient, with a small intentional offset if needed.
- Music beats: optional rhythmic cuts, pulses or transitions.
- Musical sections: scene-level style changes when the structure supports it.

Never assume the strongest waveform peak is a beat or the narrator's semantic emphasis. Use separate signals and allow human overrides.

---

# Part IV — Prompt understanding and Animation Director

## 25. Prompt interpretation contract

When a user enters a prompt, the system should first infer a creative brief. It should not immediately select random animations.

Extract these fields:

```json
{
  "topic": "What the video explains",
  "audience": "Who should understand it",
  "platforms": ["youtube_shorts", "instagram_reels"],
  "aspect_ratio": "9:16",
  "duration_target_seconds": null,
  "format": "auto",
  "visual_style": "auto",
  "pacing": "auto",
  "motion_intensity": "auto",
  "caption_mode": "auto",
  "brand_profile": "techxkenil",
  "assets_available": [],
  "must_include": [],
  "must_avoid": [],
  "music_mode": "auto"
}
```

### Precedence rules

1. Explicit instructions in the current user prompt.
2. Explicit project/channel profile.
3. Chosen platform/export profile.
4. Topic and audience inferred by the planner.
5. Faceless defaults.

A user's explicit “minimal, no camera movement” must override a default “dynamic tech” preset. The system must not silently add a talking character, 3D sequence, music or a particular meme format if the user did not request it and it is not necessary.

### Ambiguous prompts

For “make this engaging,” use a balanced format with one clear hook treatment, relevant visual explanation and restrained motion. Do not equate “engaging” with maximum movement.

For “make it cinematic,” favor camera/framing, depth, sound and longer visual holds rather than word-pop captions on every word.

For “make it like a modern tech Reel,” use a configurable tech explainer preset: clean dark/light interface surfaces, concise captions, selective word emphasis, UI/callout motion, diagrams and controlled transitions. Do not copy a named creator's exact video.

For “make it viral,” do not promise virality. Interpret this as a request to improve clarity, hook, pace and visual variety; keep the user informed that actual distribution depends on audience response and platform systems.

If an essential creative constraint is missing and cannot be safely inferred, ask one focused question. Otherwise proceed with transparent defaults.

## 26. Beat analysis

Break each scene into semantic beats. A beat is a visual communication unit, not necessarily a sentence or fixed-duration slice.

For every beat, infer:

- `subject`: what or who is being discussed.
- `action`: what changes or happens.
- `concept`: abstract or concrete meaning.
- `evidence`: facts, numbers, screenshot, source or proof.
- `relation`: comparison, cause/effect, sequence, scale, hierarchy.
- `emotion`: curiosity, surprise, urgency, reassurance, humor, seriousness.
- `speech_anchor`: word/phrase time range.
- `visual_objective`: what the viewer should understand after this beat.
- `complexity`: how much information is on screen.
- `confidence`: confidence in the interpretation and asset availability.

The visual planner must distinguish factual evidence from metaphor. A metaphor can be illustrative, but must not be presented as literal evidence.

## 27. Decision matrix: what to use, when and when not to use it

| Content signal / intent | Preferred visual approach | Supporting motion | Avoid when |
|---|---|---|---|
| Hook / surprising claim | Strong headline or striking evidence frame | One short scale/position accent | The claim is unverified or the text is unreadable |
| Key definition | Term + concise explanation | Underline, bracket, simple reveal | Long paragraph captions would be required |
| Important number | Counter or data callout | Ring/bar/chart build | The source/value/unit is uncertain |
| Growth / decline | Line/bar chart | Line draw or bar growth | No valid data points exist |
| Comparison | Split screen or comparison card | Synchronized reveal | The two sides are not comparable |
| Sequential process | Step cards or flow diagram | Node/arrow reveal | Steps are not actually sequential |
| Software instruction | Real UI capture or clearly labeled mock-up | Cursor, crop, highlight | UI fidelity cannot be verified |
| Code explanation | Code frame + output | Line focus, type/terminal reveal | Too much code would be unreadable |
| Abstract concept | Visual metaphor | Object transformation, particles or shape morph | Metaphor could misstate the idea |
| Documentary/history | B-roll, archive, map, timeline | Ken Burns, label, transition | Image provenance/date is unclear |
| Emotional / reflective beat | Hold, restrained image motion | Subtle drift or quiet dissolve | Motion would undermine the mood |
| Humor | Freeze, reaction, caption timing | Punch-in, annotation | Humor/tone is not present in script |
| Final takeaway | Reprise headline or visual summary | Controlled hero reveal | It repeats without adding meaning |

## 28. Selection algorithm

Use hard constraints first, then ranked selection.

### Hard gates

Reject a candidate if:

- It requires an asset that is unavailable and cannot be safely generated or replaced.
- It would misrepresent a factual claim or product UI.
- It conflicts with the user's explicit style constraints.
- It cannot fit the available beat duration or safe area.
- The renderer does not support the required parameters.
- It violates a safety/flash/readability check.

### Candidate scoring (initial policy; tune through review)

For candidates that pass the hard gates, score 0–1 on:

- Semantic fit: 30%.
- Comprehension value: 25%.
- Narrative/emotional fit: 15%.
- Brand/style fit: 10%.
- Visual variety contribution: 5%.
- Render/performance fit: 10%.
- Asset confidence: 5%.

`score = 0.30*semantic + 0.25*comprehension + 0.15*narrative + 0.10*brand + 0.05*variety + 0.10*performance + 0.05*asset_confidence`

These weights are engineering starting points, not scientifically validated weights. Store the score breakdown for debugging. If the top candidates are close, prefer the simpler technique with higher comprehension and lower render cost.

### Selection output

The Director must state:

- Selected technique and why.
- Visual objective.
- Primary element and supporting elements.
- Start/end anchor.
- Intensity and density contribution.
- Required asset and source status.
- Fallback if the technique cannot render.
- Confidence score and warnings.

## 29. Style preset system

Style presets combine format, typography, color, camera language, transitions, density and sound behavior. They must be data configurations, not hardcoded branches in the renderer.

Recommended initial presets:

| Preset | Character |
|---|---|
| `techxkenil_tech` | Dark navy/purple, cyan accents, clean technical grids, selective kinetic type, UI/diagram motion |
| `minimal_editorial` | Restrained typography, whitespace, hard cuts, subtle image movement |
| `documentary_cinematic` | B-roll, slow reframing, restrained title cards, map/timeline elements |
| `data_explainer` | Charts, counters, source labels, progressive diagrams |
| `product_demo` | Real interface capture, device mock-ups, cursor focus and state transitions |
| `playful_illustrated` | Flat illustration, squash/stretch, sticker/cut-paper motion |
| `high_energy_social` | Tighter edit rhythm, selective punch-ins, short captions, strong but controlled emphasis |
| `analog_archive` | Film texture, archive cards, restrained grain and slow movement |
| `terminal_code` | Code/terminal treatment, cursor, line focus, clear syntax and output reveal |

For TechXKenil, preserve the supplied brand direction as configurable data: deep navy/purple backgrounds, cyan/purple accents, white primary text, Inter Display and Bebas Neue, technical grids and controlled cinematic lighting. Verify the exact current brand configuration in the repository before implementation.

---

# Part V — Data contracts and implementation

## 30. Proposed architecture

```text
User prompt / source script / assets
                |
                v
        Creative Brief Parser
                |
                v
     Script + Semantic Beat Planner
                |
                v
      Scene / Format Style Planner
                |
                v
         Animation Director
         |              |
         v              v
   Animation Registry  Timing / Audio Map
         |              |
         +-------+------+
                 |
                 v
        Animation Plan Validator
                 |
                 v
       Existing Motion / Compositor
                 |
                 v
          FFmpeg Pipeline
                 |
                 v
      Render QA + Contact Sheets
                 |
                 v
            Final Video
```

The Animation Director should not render frames and the renderer should not decide semantic intent. This separation makes the system testable and lets new animation presets be added without rewriting prompt logic.

## 31. Proposed modules and repository mapping

The previous project notes identify these existing areas: `tools/motion.py`, `tools/humanize.py`, `tools/render_core.py`, `tools/video_pipeline.py`, `tools/qa.py`, `agents/skills/motion-editing/`, `agents/rules/` and `docs/`. The current task environment could not clone or inspect the live GitHub source, so the mapping below is **provisional and based on the supplied project notes / prior README-level description**. Verify current branch, actual filenames, call signatures and tests before editing.

| Proposed responsibility | Suggested location | Integration intent |
|---|---|---|
| Animation registry | `tools/animation_registry.py` or current equivalent | Catalog IDs, metadata, parameter validation and lookup |
| Animation planner | `tools/animation_director.py` | Turn semantic beats into candidate/selected animation plans |
| Timeline resolver | `tools/animation_timeline.py` | Resolve seconds, frame boundaries, overlap and audio anchors |
| Animation plan validator | `tools/animation_validator.py` | Validate schema, constraints, layering, duration and supported capabilities |
| Preset metadata | `tools/animation_presets/` | JSON/YAML metadata grouped by family/style |
| Low-level motion | existing `tools/motion.py` | Reuse keyframes, springs, transforms, blur and interpolation primitives |
| Caption/audio behavior | existing `tools/humanize.py` | Reuse or extend caption timing, easing and SFX selection |
| Compositing | existing `tools/render_core.py` | Draw/composite planned vector and media layers |
| Encoding/orchestration | existing `tools/video_pipeline.py` | Preserve FFmpeg and hardware-encoder workflow |
| QA | existing `tools/qa.py` plus new animation checks | Add deterministic animation and visual QA gates |
| Skill | `agents/skills/animation-director/SKILL.md` | Prompt interpretation and plan-generation contract |
| Rules | `agents/rules/animation-selection.md`, `visual-rhythm.md`, `platform-safe-layout.md` | Short, always-applicable constraints |
| Documentation | `docs/animation/` | Taxonomy, schema, usage guide, decision matrix and test plan |

**Do not blindly create every suggested file.** First inspect the repository, reuse an existing equivalent where possible, and make a minimal diff. The repository audit is an explicit pre-implementation gate.

## 32. Animation registry contract

A registry entry should be declarative. Example:

```json
{
  "id": "type.word_pop",
  "family": "typography",
  "name": "Word pop",
  "description": "Emphasize a selected word with a short scale and opacity entrance.",
  "intent_tags": ["emphasis", "hook", "key_phrase"],
  "content_signals": ["important_phrase", "surprise", "contrast"],
  "complexity": "low",
  "default_intensity": 2,
  "duration_seconds": {"min": 0.12, "default": 0.22, "max": 0.40},
  "supports": ["scale", "opacity", "position", "easing"],
  "parameters": {
    "from_scale": {"type": "number", "default": 0.82, "min": 0.5, "max": 1.0},
    "overshoot": {"type": "number", "default": 0.04, "min": 0.0, "max": 0.15},
    "highlight_color": {"type": "color", "default": "brand.accent"}
  },
  "requires_assets": false,
  "audio_sync": ["word_timestamp", "sfx_transient"],
  "fallback": "type.phrase_reveal",
  "renderer": "motion.text_word_pop",
  "qa_tags": ["safe_area", "caption_readability", "no_layout_collision"]
}
```

Registry requirements:

- Stable unique IDs; IDs should not be renamed casually once referenced by saved projects.
- Versioned metadata and explicit deprecation/alias behavior.
- Parameter schema with types, defaults, min/max and valid enums.
- Supported renderer capability declaration.
- Asset requirements and license/provenance metadata.
- Cost and performance category.
- Fallback technique.
- Unit tests for parameter validation and deterministic output.
- Discovery/filtering by semantic tag, style, duration, format, asset requirements and performance.

## 33. Animation plan contract

A plan should be structured JSON, not natural-language instructions that the renderer must interpret. The schema should be versioned and validated before execution.

```json
{
  "schema_version": "1.0",
  "project": {
    "platforms": ["youtube_shorts", "instagram_reels"],
    "aspect_ratio": "9:16",
    "fps": {"numerator": 30, "denominator": 1},
    "resolution": {"width": 1080, "height": 1920},
    "style_preset": "techxkenil_tech"
  },
  "scenes": [
    {
      "scene_id": "scene_02",
      "start_seconds": 4.2,
      "end_seconds": 9.8,
      "format": "process_diagram",
      "visual_objective": "Show tokens moving through an AI model.",
      "motion_intensity": 2,
      "beats": [
        {
          "beat_id": "beat_02a",
          "start_seconds": 4.35,
          "end_seconds": 5.5,
          "speech_anchor": {"start_word_id": "w018", "end_word_id": "w024"},
          "visual_objective": "Establish token input and direction.",
          "layers": [
            {
              "layer_id": "tokens",
              "asset_ref": "asset.tokens_stream",
              "animation_id": "object.motion_path",
              "start_seconds": 4.35,
              "duration_seconds": 1.0,
              "easing": "ease_out_cubic",
              "intensity": 2,
              "z_order": 2,
              "anchor": "model.input",
              "parameters": {"path_ref": "path.token_input", "stagger_seconds": 0.04},
              "audio_sync": {"mode": "none"},
              "fallback_animation_id": "object.slide"
            }
          ]
        }
      ],
      "transition_out": {"id": "transition.cut", "duration_seconds": 0}
    }
  ]
}
```

Schema decisions still required during implementation:

- Whether assets are identified by project-local IDs, immutable paths, or a media manifest.
- Whether speech anchors refer to word IDs, phrase IDs or sample timestamps.
- Whether duration is stored as start/end or start/duration (choose one canonical internal representation).
- How nested groups, parent transforms and masks are represented.
- How a transition consumes/overlaps adjacent scene time.
- How style tokens resolve to actual fonts/colors/spacing.

Do not let LLM output contain executable Python, shell commands or arbitrary FFmpeg filter expressions. The model should select validated registry IDs and typed parameters only.

## 34. Timeline and renderer responsibilities

### Animation Director

- Read the brief and semantic beat map.
- Choose scene format and style preset.
- Select animation IDs from the registry.
- Set anchors, intended duration, intensity and supported parameters.
- Explain selection and include confidence/warnings.
- Output the versioned plan.

### Timeline resolver

- Convert speech anchors and seconds into frame ranges.
- Resolve overlap and transition duration.
- Clamp timing against scene and project boundaries.
- Resolve rational frame rates.
- Provide a deterministic `frame_state(frame_index)` or equivalent contract.

### Motion renderer

- Execute only registered animation implementations.
- Evaluate property values from the current frame, not wall-clock time.
- Use deterministic randomness where procedural motion is needed.
- Preserve correct transform origin, coordinate space, parent/child transforms and z-order.
- Reuse compositing, supersampling and hardware encoding already present where verified.

### Validator

- Validate schema and registry IDs.
- Reject unsupported parameters and invalid ranges.
- Detect invalid/negative/zero duration where not explicitly allowed.
- Detect scene overflow and unresolved overlaps.
- Verify assets exist and have usage permission.
- Check safe areas and text bounds.
- Emit warnings separately from hard errors.

---

# Part VI — Skills and rules

## 35. Proposed `animation-director` skill

Create a focused skill at `agents/skills/animation-director/SKILL.md` after auditing the existing skill conventions. Suggested skill contract:

```markdown
# Animation Director

Use this skill whenever a video prompt, script or scene requires visual planning.

1. Read the project brief, brand profile, platform profile and available assets.
2. Analyze script meaning and divide scenes into semantic beats.
3. Determine the visual objective for each beat.
4. Select a primary visual format for each scene.
5. Query the animation registry; never invent renderer IDs.
6. Select the simplest technique that communicates the idea clearly.
7. Set speech-aligned timing, intensity and visual-density budget.
8. Add supporting motion only when it has a separate communication purpose.
9. Prefer a clean cut unless a designed transition communicates continuity or meaning.
10. Validate asset provenance, platform safe areas, readability and render cost.
11. Output the versioned AnimationPlan JSON and an explanation/warning summary.
12. Never emit executable renderer code or arbitrary filter expressions.
```

### Suggested rules files

- `animation-selection.md`: semantic triggers, preferred treatments and negative rules.
- `visual-rhythm.md`: intensity, density, repetition avoidance and static contrast.
- `platform-safe-layout.md`: output profile, text-safe regions and overlay collision checks.
- `motion-physics.md`: easing, anticipation, overshoot, settle and deterministic frame behavior.
- `asset-truthfulness.md`: distinguish supplied footage, generated illustration, conceptual UI and verified product captures.

Do not duplicate the current `motion-editing` skill. Extend it where it already owns renderer-level instructions; let the new Animation Director skill own planning and selection.

---

# Part VII — Quality, safety and evaluation

## 36. Visual QA checklist

### Story and semantics

- Does every major visual correspond to the narration or the intended story beat?
- Are numbers, dates, units, names, UI labels and chart values accurate?
- Is an illustrative metaphor clearly illustrative rather than false evidence?
- Does each scene have one understandable visual objective?

### Motion

- Is the primary event obvious?
- Does movement have appropriate acceleration/deceleration and settle behavior?
- Is there unwanted jitter, flicker, popping, clipping or one-frame discontinuity?
- Are two camera transforms fighting each other?
- Is movement used only where it adds meaning, focus or energy?
- Does a long hold feel intentional rather than like a failed animation?

### Typography and layout

- Is text large enough for a phone display?
- Are captions synchronized and readable?
- Are line lengths and wraps intentional?
- Are captions and key information inside the platform profile's safe region?
- Are UI controls, platform overlays and right/bottom interaction zones avoided by critical text?
- Are font fallbacks and glyph coverage validated?

### Audio

- Are word/phrase anchors aligned with narration?
- Do sound effects support the scene without masking speech?
- Does a speed ramp preserve or deliberately alter audio?
- Are visual impacts synchronized with the intended transient?

### Render/performance

- No missing assets or unsupported IDs.
- No unbounded particle count.
- No avoidable full-frame expensive effect repeated on every layer.
- No broken alpha/premultiplication edges.
- Frame count/duration and audio/video end times agree.
- Existing hardware-encoder fallback remains functional.

## 37. Flashing, movement and accessibility

Use conservative flashing rules. WCAG 2.2 includes a three-flashes-or-below-threshold success criterion and a pause/stop/hide requirement for certain automatically moving content on web pages; these are web accessibility requirements, not a complete video-platform specification. Faceless should nevertheless apply the three-flashes guidance as a safety baseline and avoid strobing, rapid red flashes, repeated high-contrast flicker and unnecessary camera shake. Provide reduced-motion rendering options for product previews and any interactive editor UI. [12]

## 38. Automated test matrix

| Test type | Example tests | Pass condition |
|---|---|---|
| Registry unit tests | Unknown ID, invalid parameter, missing fallback | Clear validation error, no silent failure |
| Determinism tests | Render same frame twice | Identical values/pixels within accepted tolerance |
| Timing tests | Start/end, overlap, frame rounding | No off-by-one, negative or overflowing range |
| Text tests | Long words, two-line text, mixed scripts | No clipping or missing glyphs |
| Layout tests | 9:16 safe area, device overlays | Critical text remains unobstructed |
| Motion tests | Ease, spring, path, mask, transition | Expected endpoints and no discontinuity |
| Audio tests | Word sync, transient sync, end padding | Timing errors within configured tolerance |
| Integration tests | Render one sample per family | Valid video and audio, no unsupported effects |
| Regression tests | Golden frame/contact sheet | Reviewable visual diff, no unexpected regression |
| Performance tests | Low/medium/high complexity scene | Meets target render budget on supported hardware |

Build a compact benchmark set: a 15-second text-led hook, a 30-second technical explainer, a 45–60-second documentary/data story and a 90-second software tutorial. Include scenes with no animation to test intentional stillness.

## 39. Evaluation after publishing

Store the following metadata with each render:

- Format/style preset.
- Hook format and first visual event.
- Caption mode.
- Motion intensity and density distribution.
- Transition types and count.
- Use of B-roll, UI, chart, illustration and 3D.
- Video duration and frame rate.
- Render time and warnings.

Compare these with platform analytics available to the creator: viewed/swiped signals where offered, retention/average view duration, completion, replay and engagement. The purpose is to learn what works for this channel and audience, not to optimize toward a supposed universal “viral animation.” Platform algorithms, distribution and audience tastes can change.

---

# Part VIII — Delivery plan

## 40. Recommended implementation phases

### Phase 0 — Repository audit (mandatory)

- Connect/read the actual repository branch and inspect the README, dependency manifests, motion, compositing, audio, rendering, QA and skill files.
- Identify all existing animation functions and supported parameters.
- Trace how narration timing and visual scenes currently enter the renderer.
- Map existing tests and rendering performance.
- Produce a no-duplication change plan.

**Exit gate:** verified module map and baseline render successfully reproduced.

### Phase 1 — Taxonomy and registry

- Add stable IDs for the highest-value animation techniques.
- Define metadata and parameter schemas.
- Implement lookup, validation, aliases and fallback behavior.
- Add one minimal test per animation family.

**Exit gate:** registry can discover and validate presets independently of the LLM.

### Phase 2 — Animation Plan and Director skill

- Write the AnimationPlan schema.
- Create the `animation-director` skill and concise selection rules.
- Add prompt parsing into a CreativeBrief.
- Build deterministic rule-based candidate filtering and selection; allow the model to rank only candidates exposed by the registry.

**Exit gate:** same script/style inputs produce a valid plan with explainable decisions.

### Phase 3 — High-value animation pack

Implement in this order:

1. Text/caption treatments.
2. Camera/reframe and still-image motion.
3. Object entrances, callouts and shape/line reveals.
4. Charts and process diagrams.
5. UI/cursor/code interactions.
6. Masks, transitions and split-screen.
7. Particle/atmospheric effects.
8. Advanced 2.5D/3D and character styles.

This order prioritizes common technical/educational short-form needs and the greatest reuse from a small primitive set.

### Phase 4 — Audio-aware timeline

- Integrate word/phrase timing.
- Add sound-effect anchors and optional beat map.
- Resolve transitions and overlap in frame space.
- Add deterministic replay and caching.

### Phase 5 — QA, presets and analytics loop

- Add validation/contact sheets.
- Tune style presets and motion budgets.
- Compare render time and visual quality.
- Store animation metadata in output manifests.
- Review real channel results and refresh research examples.

## 41. Minimum viable release (MVP) acceptance criteria

Do not call the system complete until all are true:

1. The prompt is converted into a structured CreativeBrief.
2. A script is split into semantic visual beats.
3. Every beat has a visual objective and, where appropriate, a selected format/treatment.
4. The Director selects only registered animation IDs.
5. The plan is versioned, validated and deterministic.
6. Captions can use phrase or word timing without making readability worse.
7. Scene/transition timing resolves correctly to frames.
8. Unsupported assets/animations have safe fallbacks.
9. At least one test video is rendered for each supported family added to the MVP.
10. Contact sheets and automated QA are produced.
11. Existing Faceless workflows still render successfully.
12. The user can override style, intensity, caption mode and motion preferences in the prompt.
13. There is an explicit no-animation/static option.
14. No generated output claims that an effect guarantees virality.

## 42. First MVP library recommendation

Do not implement the entire catalog before validating the architecture. Begin with roughly 25 reusable treatments built from the existing verified primitives:

- `type.word_pop`
- `type.karaoke_highlight`
- `type.phrase_reveal`
- `type.typewriter`
- `type.scale_punch`
- `type.lower_third`
- `camera.push_in`
- `camera.pull_out`
- `camera.pan`
- `camera.ken_burns`
- `camera.punch`
- `object.fade`
- `object.slide`
- `object.pop_overshoot`
- `object.stagger`
- `object.motion_path`
- `shape.path_draw`
- `shape.wipe`
- `shape.morph` (if renderer can support it)
- `data.counter`
- `data.bar_grow`
- `data.line_draw`
- `diagram.node_reveal`
- `ui.cursor_click`
- `ui.code_line_focus`
- `edit.freeze_label`
- `edit.split_screen`
- `transition.cut`
- `transition.dissolve`
- `transition.directional_wipe`

This is a recommended first pack, not a claim that all 30 are currently present or already implemented.

---

# Appendix A — Research references

The source list below separates platform guidance from engineering references. Accessed/reviewed for this specification on 14 November 2026 where the web results exposed current pages; individual publication dates are stated where available.

1. **YouTube Blog — “Five tips to master Shorts” (4 August 2025).** Creator and former Shorts product-lead discussion; authenticity, personal storytelling, use trends as a tool rather than a crutch.  
   https://blog.youtube/creator-and-artist-stories/five-tips-to-master-shorts/
2. **YouTube Blog — “From epic edits to quick clips: Transitioning your long-form content to YouTube Shorts” (16 April 2025).** Hook selection, concise standalone content, 9:16 cropping, captions/text overlays, speed changes, audio and analytics experimentation.  
   https://blog.youtube/creator-and-artist-stories/transitioning-your-long-form-content-to-youtube-shorts/
3. **YouTube Blog — “YouTube Shorts deep dive” (28 January 2025).** Creator interview discussing the first-second hook, mini-stories and short-form narrative. Treat the one-second hook as creator advice rather than a performance guarantee.  
   https://blog.youtube/creator-and-artist-stories/youtube-shorts-deep-dive/
4. **YouTube Help — “Understand three-minute YouTube Shorts.”** Official square/vertical format and current length eligibility; verify platform rules again at export time.  
   https://support.google.com/youtube/answer/15424877
5. **Meta — “Introducing Best Practices, an Education Hub for Creators on Instagram” (October 2024).** Instagram Professional Dashboard guidance across creation, engagement, reach, monetization and guidelines; personalized tips may change.  
   https://about.fb.com/news/2024/10/best-practices-education-hub-creators-instagram/
6. **Adobe After Effects Help — “Animating text” (updated 30 April 2026).** Whole-layer and per-character/range text animation, selectors, and per-character 3D performance caveat.  
   https://helpx.adobe.com/after-effects/desktop/animating-text/text-animation/animating-text.html
7. **GSAP — MotionPathPlugin documentation.** Reference for animating elements along paths.  
   https://gsap.com/docs/v3/Plugins/MotionPathPlugin/
8. **GSAP — MorphSVGPlugin documentation.** Reference for SVG path morphing and curve matching.  
   https://gsap.com/docs/v3/Plugins/MorphSVGPlugin/
9. **Adobe — “The essential principles of animation every creator should know.”** Overview of the 12 animation principles and their application to motion.  
   https://www.adobe.com/in/creativecloud/roc/blog/video/animation-principles.html
10. **Remotion — `interpolate()` documentation.** Frame-driven interpolation, easing, extrapolation/clamping and keyframe ranges.  
    https://www.remotion.dev/docs/interpolate
11. **GSAP — Timeline documentation.** Timeline sequencing, labels, relative offsets and intentional overlap.  
    https://gsap.com/docs/v3/GSAP/Timeline/
12. **W3C — Web Content Accessibility Guidelines (WCAG) 2.2.** Flashing and pause/stop/hide criteria; apply as a conservative safety reference while respecting the scope of the web standard.  
    https://www.w3.org/TR/WCAG22/
13. **Remotion — `spring()` documentation.** Physics-based spring animation parameters and frame/FPS input.  
    https://www.remotion.dev/docs/spring
14. **Lottie Animation Format specification.** JSON-based vector animation format reference; useful when importing/validating vector animation assets.  
    https://lottie.github.io/lottie-spec/dev/
15. **Rive — State Machines runtime documentation.** Reference for state-driven transitions between named animations using boolean/number inputs and triggers.  
    https://github.com/rive-app/help-center/blob/master/runtimes/state-machines.md
16. **FFmpeg — Filters documentation.** Reference for text rendering, overlays and video filter/compositing capabilities.  
    https://ffmpeg.org/ffmpeg-filters.html
17. **Adobe After Effects Help — Animation basics.** Keyframes, interpolation, expressions and Graph Editor concepts.  
    https://helpx.adobe.com/after-effects/desktop/animate-in-after-effects/animation-basics/animation-basics.html

## Appendix B — Repository audit checklist

Before implementation, record the following from the actual checked-out repository:

- [ ] Branch and commit hash.
- [ ] README and architecture documentation current state.
- [ ] Existing animation functions and public APIs.
- [ ] Existing `motion.py` keyframe/spring/easing support.
- [ ] Existing `humanize.py` caption/audio behavior.
- [ ] Existing `render_core.py` layer/composite model.
- [ ] Existing `video_pipeline.py` timing/FPS/encoder flow.
- [ ] Existing `qa.py` checks and test commands.
- [ ] Existing agent skill conventions and rule loading.
- [ ] Dependencies and supported Python/FFmpeg versions.
- [ ] Current sample video and baseline performance.
- [ ] Exact brand profile source and platform export profile source.
- [ ] Duplicate functionality to reuse instead of rebuilding.

## Appendix C — Final engineering reminder

Do not optimize for the number of animations in the registry. Optimize for the number of clearly communicated ideas the system can produce with reliable, reusable motion.

A smaller, well-designed set of composable primitives plus strong selection intelligence will outperform a large collection of unrelated presets.
