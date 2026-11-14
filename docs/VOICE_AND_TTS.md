# Voice & TTS Production

## Target Voice: `txk_practical_host`
- Adult presenter: conversational, articulate, calm, and practical.
- Speaks with natural sentence rhythm, pacing down for complex code, numbers, and technical terminology.
- No synthetic hype, cartoon excitement, or aggressive clickbait urgency.

## Speech Preparation Pipeline
Before text is sent to Kokoro TTS or external providers, it passes through `prepare_spoken_script()` in `tools/audio_director.py`:
1. Expands technical acronyms and units (`140 GB` $\to$ `140 gigabytes`, `ms` $\to$ `milliseconds`).
2. Inserts conversational breath pauses after transitional clauses.
3. Applies phonetic lexicon overrides via `tools/lexicon.py` and `lexicon.json`.
4. Adds standard $0.18\text{s}$ chunk pause and $+0.45\text{s}$ section boundary breathing room.
