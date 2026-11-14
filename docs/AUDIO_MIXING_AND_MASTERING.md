# Audio Mixing & Broadcast Mastering

## Mix Bus Structure
The mix is constructed across 5 discrete stems:
- `VOICE` (Center, reference gain)
- `MUSIC` (Stereo, dynamic sidechain ducking $-4\text{ dB}$ to $-8\text{ dB}$)
- `SFX` (Event-anchored, restrained gain $-6\text{ dB}$ to $-12\text{ dB}$)
- `AMBIENCE` (Subtle bed $-18\text{ dB}$ to $-24\text{ dB}$)
- `MASTER` (EBU R128 loudness normalization and limiting)

## Standards & Compliance
- **Integrated Loudness**: $-16.0 \pm 1.5\text{ LUFS-I}$
- **True Peak**: $\le -1.0\text{ dBTP}$ ceiling ($48\text{ kHz}$)
- **Mono Fold-down Correlation**: $> 0.4$ (zero destructive phase cancellation)
- **Sample Rate**: $48\text{ kHz}$ / $24\text{-bit}$ or float32 PCM
