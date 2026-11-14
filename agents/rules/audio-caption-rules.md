# Audio & Caption Intelligence Rules

## Rule 1: Narration is the Lead Instrument
1. Voice intelligibility outranks music, SFX, and visual animation.
2. Normalization must convert written copy into natural, spoken phrasing before TTS synthesis, expanding abbreviations, units, and technical acronyms.
3. Every scene maintains a pause of $0.18\text{s}$ after speech chunks and $+0.45\text{s}$ at section boundaries.

## Rule 2: SFX as Punctuation, Not Wallpaper
1. Every sound effect must have an explicit reason: explain, emphasize, connect, locate, or punctuate.
2. No automatic whoosh on every cut. SFX intensity defaults to level $1–2$ (subtle to normal).
3. All sound assets must have verified commercial license and provenance metadata in the Asset Registry.

## Rule 3: 5-Stem Mixing & Broadcast Loudness
1. Stems (`VOICE`, `MUSIC`, `SFX`, `AMBIENCE`, `MASTER`) must be mixed with automatic speech sidechain ducking ($4–8\text{ dB}$).
2. Master output must conform to $-16.0 \pm 1.5\text{ LUFS-I}$ with a True Peak ceiling of $-1.0\text{ dBTP}$ at $48\text{ kHz}$.
3. Stereo mix must pass mono fold-down check ($>0.4$ correlation) to ensure dialogue clarity on mobile phones.

## Rule 4: Two-Layer Caption Separation
1. Layer A (`CaptionTrack`) is the canonical source of truth for accessibility and search. It must represent all spoken words and meaningful non-speech cues, and automatically export `.srt` and `.vtt` sidecars.
2. Layer B (`VisualCaptionPlan`) handles on-screen presentation: phrase segmentation ($2–6$ words), selective keyword emphasis, line length $\le 42$ chars, and adult reading speed $\le 20\text{ chars/sec}$.
3. Visual styling and animated callouts must NEVER mutate, delete, or rewrite the source transcript.
