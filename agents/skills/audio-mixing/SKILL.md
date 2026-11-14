---
name: audio-mixing
description: Directs 5-stem audio mixing, sidechain ducking, stereo phase compatibility, and broadcast loudness mastering.
---

# Audio Mixing & Mastering Skill

The Audio Mixing skill manages the acoustic balance, spatial headroom, and broadcast loudness compliance across all stems.

## 1. 5-Stem Mix Architecture
1. **`VOICE`**: Primary narration dialogue; lead instrument that must remain intelligible even on low-volume mobile speakers.
2. **`MUSIC`**: Ambient synth beds and subtle musical accompaniment.
3. **`SFX`**: Event-anchored tactile punctuation (soft clicks, pops, whooshes, chimes).
4. **`AMBIENCE`**: Room tone and atmospheric hum.
5. **`MASTER`**: Summed mix with dynamic range control and broadcast compliance.

## 2. Dynamic Sidechain Ducking
- Whenever the `VOICE` stem is active, duck background `MUSIC` by $4.0–8.0\text{ dB}$ (default $6.0\text{ dB}$).
- Apply smooth envelope convolution ($120\text{ms}$ attack, $350–450\text{ms}$ release) to prevent audible acoustic pumping.
- Recover music bed gently during deliberate silent beats and visual holds.

## 3. Broadcast Mastering Gates
- **Integrated Loudness**: Target $-16.0 \pm 1.5\text{ LUFS-I}$ using EBU R128 two-pass normalization.
- **Maximum True Peak**: $\le -1.0\text{ dBTP}$ ceiling to prevent clipping and inter-sample distortion during YouTube/Instagram AAC compression.
- **Mono Compatibility**: Verify stereo phase correlation $> 0.4$ to guarantee dialogue clarity on mono phone speakers.
