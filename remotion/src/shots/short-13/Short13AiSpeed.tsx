import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  Sequence,
  useCurrentFrame,
} from 'remotion';
import {
  BigTitle,
  Captions,
  Kicker,
  ProgressBar,
  ShortsBackdrop,
  StatChip,
  prog,
} from '../../lib/shorts';
import { FONT_BODY, FONT_DISPLAY, FONT_MONO } from '../../fonts';
import { VO } from './vo.gen';

// =============================================================================
// COMPOSITION CONFIGURATION (Vertical 9:16 Short)
// =============================================================================
export const compositionConfig = {
  id: 'Short13AiSpeed',
  durationInSeconds: 42,
  fps: 30,
  width: 1080,
  height: 1920,
};

const GOLD = '#f5d76e';
const GREEN = '#4db8a8';
const PINK = '#e8879f';
const BLUE = '#6366f1';
const EASE_OUT = Easing.bezier(0.22, 1, 0.36, 1);
const CLAMP = { extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const };

export default function Short13AiSpeed() {
  const frame = useCurrentFrame();

  // Stopwatch for the hook (0 to 3.4s)
  const stopwatchMs = interpolate(frame, [0, 90], [0, 15.2], {
    ...CLAMP,
    easing: EASE_OUT,
  });

  // HBM progress bar for hardware beat (frame 420 to 780)
  const hbmBar = interpolate(frame, [440, 560], [10, 95], {
    ...CLAMP,
    easing: EASE_OUT,
  });

  return (
    <AbsoluteFill style={{ backgroundColor: '#090b10' }}>
      <ShortsBackdrop />

      {/* Progress bar at the top */}
      <ProgressBar totalFrames={42 * 30} color={GREEN} />

      {/* Persistent Canvas Container */}
      <div
        style={{
          position: 'absolute',
          top: 360,
          left: 60,
          width: 960,
          height: 1000,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        {/* BEAT 1: HOOK (Frames 0 - 105 | 0 to 3.5s) */}
        {frame < 105 && (
          <div style={{ textAlign: 'center' }}>
            <Kicker text="AI LATENCY PARADOX" color={GOLD} />
            <div
              style={{
                fontFamily: FONT_MONO,
                fontSize: 108,
                fontWeight: 800,
                color: '#fff',
                marginTop: 20,
                textShadow: `0 0 50px ${GREEN}66`,
              }}
            >
              {stopwatchMs.toFixed(1)} <span style={{ fontSize: 44, color: GREEN }}>ms</span>
            </div>
            <div
              style={{
                fontFamily: FONT_BODY,
                fontSize: 32,
                color: '#cbd5e1',
                marginTop: 18,
                fontWeight: 600,
              }}
            >
              140 Trillion Math Ops
            </div>
          </div>
        )}

        {/* BEAT 2: THE 80 TRANSFORMER LAYERS (Frames 105 - 420 | 3.5s to 14s) */}
        {frame >= 105 && frame < 420 && (
          <div style={{ width: '100%', textAlign: 'center' }}>
            <Kicker text="EVERY SINGLE WORD" color={PINK} />
            <BigTitle title="80 LAYERS" subtitle="70 BILLION PARAMETERS" />
            <div
              style={{
                marginTop: 48,
                padding: '24px 32px',
                backgroundColor: 'rgba(255,255,255,0.06)',
                borderRadius: 20,
                border: '1.5px solid rgba(255,255,255,0.12)',
              }}
            >
              <div style={{ fontFamily: FONT_MONO, fontSize: 36, color: '#fff' }}>
                "The cat sat on the <span style={{ color: GREEN }}>[mat]</span>"
              </div>
              <div
                style={{
                  fontFamily: FONT_BODY,
                  fontSize: 22,
                  color: '#94a3b8',
                  marginTop: 14,
                }}
              >
                Computed one token at a time
              </div>
            </div>
          </div>
        )}

        {/* BEAT 3: HARDWARE RACE (Frames 420 - 780 | 14s to 26s) */}
        {frame >= 420 && frame < 780 && (
          <div style={{ width: '100%' }}>
            <Kicker text="SILICON BREAKTHROUGH" color={BLUE} />
            <div
              style={{
                marginTop: 24,
                backgroundColor: '#131622',
                borderRadius: 20,
                padding: '32px',
                border: `1.5px solid ${GREEN}`,
                boxShadow: `0 10px 40px ${GREEN}22`,
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontFamily: FONT_BODY, fontSize: 24, color: '#fff', fontWeight: 600 }}>
                  HBM3e Memory
                </span>
                <span style={{ fontFamily: FONT_MONO, fontSize: 26, color: GREEN, fontWeight: 700 }}>
                  3.35 TB/sec
                </span>
              </div>
              <div
                style={{
                  height: 20,
                  backgroundColor: 'rgba(255,255,255,0.08)',
                  borderRadius: 10,
                  marginTop: 16,
                  overflow: 'hidden',
                }}
              >
                <div
                  style={{
                    height: '100%',
                    width: `${hbmBar}%`,
                    backgroundColor: GREEN,
                    borderRadius: 10,
                  }}
                />
              </div>

              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginTop: 36,
                }}
              >
                <span style={{ fontFamily: FONT_BODY, fontSize: 24, color: '#94a3b8' }}>
                  Normal CPU RAM
                </span>
                <span style={{ fontFamily: FONT_MONO, fontSize: 24, color: PINK }}>
                  0.06 TB/sec
                </span>
              </div>
            </div>
          </div>
        )}

        {/* BEAT 4: KV-CACHE (Frames 780 - 1080 | 26s to 36s) */}
        {frame >= 780 && frame < 1080 && (
          <div style={{ width: '100%', textAlign: 'center' }}>
            <Kicker text="THE SECRET WEAPON" color={GOLD} />
            <BigTitle title="KV CACHE" subtitle="Zero Recalculation" />
            <div
              style={{
                marginTop: 40,
                display: 'flex',
                justifyContent: 'center',
                gap: 16,
              }}
            >
              <StatChip label="COMPUTE" value="O(1) FLAT" color={GREEN} />
              <StatChip label="THROUGHPUT" value="80 TOK/S" color={BLUE} />
            </div>
          </div>
        )}

        {/* BEAT 5: LOOP PAYOFF (Frames 1080 - 1260 | 36s to 42s) */}
        {frame >= 1080 && (
          <div style={{ textAlign: 'center' }}>
            <Kicker text="PURE MATHEMATICS" color={GREEN} />
            <div
              style={{
                fontFamily: FONT_DISPLAY,
                fontSize: 68,
                fontWeight: 800,
                color: '#fff',
                letterSpacing: '-0.02em',
                lineHeight: 1.15,
                marginTop: 16,
              }}
            >
              SPEED OF LIGHT
            </div>
            <div
              style={{
                fontFamily: FONT_MONO,
                fontSize: 48,
                color: GREEN,
                fontWeight: 700,
                marginTop: 24,
              }}
            >
              15.0 ms
            </div>
          </div>
        )}
      </div>

      {/* Captions positioned at safe bottom area */}
      <Captions lines={VO} />
    </AbsoluteFill>
  );
}
