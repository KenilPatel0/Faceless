# Audio System Overview

## Purpose
The Faceless audio system treats sound as an essential storytelling dimension. Dialogue intelligibility outranks music and sound effects, and every sound event serves a clear narrative purpose.

## Architecture
The system operates on a 5-stem architecture:
- `VOICE`: Lead dialogue synthesized with Kokoro v1.0 ONNX or provider-neutral adapters.
- `MUSIC`: Ducked ambient synth pads or minimal electronic score.
- `SFX`: Purposeful tactical punctuation (clicks, pops, whooshes, chimes).
- `AMBIENCE`: Environmental tone and subtle atmospheric texture.
- `MASTER`: Summed, dynamic-range-controlled master conforming to broadcast standards.

## Core Modules
- `tools/audio_director.py`: Plans sound cues, handles voice profiles, and performs 5-stem mixing with speech-driven sidechain ducking.
- `tools/sound_engine.py`: Procedural SFX generation and broadcast audio mastering.
- `tools/lexicon.py`: Phonetic dictionary and technical term normalizer.
- `tools/audio_caption_qa.py`: Compliance verification for loudness, true peak, and mono phase stability.
