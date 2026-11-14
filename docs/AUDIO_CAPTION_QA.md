# Audio & Caption QA Verification Gate

## Automated Quality Verification
Every render undergoes automated verification via `tools/audio_caption_qa.py`:

### Audio Checks
1. **Loudness**: $-16.0 \pm 1.5\text{ LUFS-I}$ measured via FFmpeg `ebur128`.
2. **True Peak**: $\le -1.0\text{ dBTP}$ maximum inter-sample ceiling.
3. **Mono Compatibility**: Phase correlation between channels $> 0.4$.

### Caption Checks
1. **Readability**: Maximum reading speed $\le 20\text{ cps}$.
2. **Line Width**: Maximum on-screen caption line $\le 42\text{ characters}$.
3. **Temporal Integrity**: All chunks must have positive duration ($t_{end} > t_{start}$).
4. **Sidecar Export**: Both `.srt` and `.vtt` must exist and parse with zero syntax errors.
