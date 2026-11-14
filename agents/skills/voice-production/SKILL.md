---
name: voice-production
description: Prepares speakable scripts, manages pronunciation dictionaries, and handles provider-neutral TTS synthesis.
---

# Voice Production Skill

The Voice Production skill transforms written scripts into natural, broadcast-ready spoken narration.

## 1. Speech Preparation
1. **Conversational Phrasing**: Split long, convoluted sentences into bite-sized spoken thoughts. Replace stiff formalisms with natural conversational cadence.
2. **Pronunciation Normalization**:
   - Technical acronyms: Expand or phoneticize ambiguous terms (e.g. `LLM` $\to$ `L L M`, `API` $\to$ `A P I`, `JSON` $\to$ `JAY-sawn`, `VRAM` $\to$ `VEE-ram`).
   - Units and Numbers: Spell out units (`140 GB` $\to$ `140 gigabytes`, `35 ms` $\to$ `35 milliseconds`).
   - Channel identity: Ensure channel names (e.g. `TechXKenil` $\to$ `Tech X Kenil`) are pronounced flawlessly via `tools/lexicon.py`.
3. **Pacing and Pauses**:
   - Add $0.18\text{s}$ pause after each narrative chunk.
   - Add $+0.45\text{s}$ extra pause at section boundaries to let visual concepts settle.

## 2. Voice Profiles
- **`txk_practical_host`** (default):
  - Model: Kokoro v1.0 ONNX (`am_michael` at 1.1x speed, `en-us`).
  - Delivery: Calm, articulate, practical, credible presenter.
  - Zero fake urgency, zero cartoon hype.
- Provider Neutrality: Speech requests use `SpeechRequest` and can be fulfilled by `KokoroTTSAdapter` or external enterprise TTS providers.
