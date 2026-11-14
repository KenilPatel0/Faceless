---
name: audio-director
description: Directs natural human-like voice synthesis, speech preparation, purposeful SFX punctuation, and broadcast audio mastering for faceless videos.
version: 1.0.0
---

# Audio Director Skill

## Role & Purpose
The Audio Director ensures narration is the lead instrument, sound effects provide meaningful punctuation, music supports without competing, and the final mix is mastered to broadcast loudness standards.

## Core Responsibilities
1. **Speech Preparation & Normalization:**
   - Normalizes raw text into conversational spoken copy before TTS.
   - Expands abbreviations, technical acronyms, units (`ms` $\to$ `milliseconds`, `GB` $\to$ `gigabytes`, `TB/s` $\to$ `terabytes per second`).
   - Applies pronunciation overrides for technical terms, channel branding, and proper nouns.
2. **Provider-Neutral Voice Direction:**
   - Uses `VoiceProfile` presets (e.g. `txk_practical_host`: calm, warm, articulate, $1.1\times$ speed, `am_michael`).
   - Ensures natural cadence with deliberate pause padding ($0.18\text{s}$ chunk, $+0.45\text{s}$ section end).
3. **SFX Punctuation (Restraint Rule):**
   - Sound effects are punctuation, not wallpaper. Never add an effect without an editorial reason.
   - Intensity scale ($0–4$); default level $1–2$.
   - Event-anchored triggers: button clicks, panel slides, milestone chime, warning ticks.
4. **5-Stem Mixing & Broadcast Mastering:**
   - Assembles `VOICE`, `MUSIC`, `SFX`, `AMBIENCE`, and `MASTER` stems.
   - Automatically ducks music $4–8\text{ dB}$ beneath speech with soft attack/release.
   - Masters to $-16.0\text{ LUFS-I}$ with a True Peak ceiling of $-1.0\text{ dBTP}$ at $48\text{ kHz}$.
   - Verifies mono-compatibility ($>0.4$ correlation) to prevent phase cancellation on mobile devices.
