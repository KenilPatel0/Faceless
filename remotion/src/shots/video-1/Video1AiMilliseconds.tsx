import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  Sequence,
  useCurrentFrame,
} from 'remotion';
import {
  Zap,
  Cpu,
  Brain,
  Database,
  Layers,
  Flame,
  Gauge,
  CheckCircle2,
  Clock,
  Sparkles,
  ArrowRight,
  RefreshCw,
  Server,
  Activity,
} from 'lucide-react';
import { FONT_BODY, FONT_DISPLAY, FONT_MONO } from '../../fonts';
import { COLORS } from '../../brand';

// =============================================================================
// COMPOSITION CONFIGURATION (5-Minute 16:9 Widescreen Faceless Video)
// =============================================================================
export const compositionConfig = {
  id: 'Video1AiMilliseconds',
  durationInSeconds: 300, // 5 minutes
  fps: 30,
  width: 1920,
  height: 1080,
};

const CLAMP = { extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const };
const EASE_OUT = Easing.bezier(0.22, 1, 0.36, 1);
const EASE_INOUT = Easing.bezier(0.37, 0, 0.63, 1);

// Helper for card glow and border
const Card: React.FC<{
  children: React.ReactNode;
  style?: React.CSSProperties;
  borderColor?: string;
  glow?: string;
}> = ({ children, style, borderColor = 'rgba(255,255,255,0.1)', glow }) => (
  <div
    style={{
      backgroundColor: '#12141c',
      border: `1.5px solid ${borderColor}`,
      borderRadius: 20,
      padding: '28px 36px',
      boxShadow: glow ? `0 12px 48px ${glow}22, 0 4px 16px rgba(0,0,0,0.4)` : '0 12px 32px rgba(0,0,0,0.5)',
      ...style,
    }}
  >
    {children}
  </div>
);

// Progress pill banner
const ActBadge: React.FC<{ num: string; title: string }> = ({ num, title }) => (
  <div
    style={{
      position: 'absolute',
      top: 48,
      left: 80,
      display: 'flex',
      alignItems: 'center',
      gap: 14,
      backgroundColor: 'rgba(255, 255, 255, 0.06)',
      border: '1px solid rgba(255, 255, 255, 0.14)',
      borderRadius: 999,
      padding: '8px 24px',
      backdropFilter: 'blur(12px)',
    }}
  >
    <span
      style={{
        fontFamily: FONT_MONO,
        fontSize: 16,
        fontWeight: 700,
        color: COLORS.signal,
        letterSpacing: '0.08em',
      }}
    >
      {num}
    </span>
    <span
      style={{
        width: 4,
        height: 4,
        borderRadius: '50%',
        backgroundColor: 'rgba(255,255,255,0.4)',
      }}
    />
    <span
      style={{
        fontFamily: FONT_DISPLAY,
        fontSize: 18,
        fontWeight: 600,
        color: '#f0f3f8',
        letterSpacing: '0.04em',
        textTransform: 'uppercase',
      }}
    >
      {title}
    </span>
  </div>
);

// =============================================================================
// ACT 1: THE ILLUSION OF MAGIC (0:00 - 0:45 | Frames 0 - 1350)
// =============================================================================
const Act1TheIllusion: React.FC = () => {
  const frame = useCurrentFrame();

  // Stopwatch counting from 0.00ms to 48.25ms in the first 120 frames
  const elapsedMs = interpolate(frame, [15, 120], [0, 48.25], {
    ...CLAMP,
    easing: EASE_OUT,
  });

  const cardsOpacity = interpolate(frame, [60, 90], [0, 1], CLAMP);
  const cardsSlide = interpolate(frame, [60, 90], [40, 0], { ...CLAMP, easing: EASE_OUT });

  return (
    <AbsoluteFill style={{ backgroundColor: '#090b10', overflow: 'hidden' }}>
      {/* Background cyber grid */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundImage:
            'radial-gradient(circle at 50% 30%, rgba(99,102,241,0.18), transparent 70%), linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)',
          backgroundSize: '100% 100%, 60px 60px, 60px 60px',
        }}
      />

      <ActBadge num="ACT 01" title="The Millisecond Paradox" />

      {/* Main Title & Stopwatch */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100%',
          paddingTop: 40,
        }}
      >
        <div
          style={{
            fontFamily: FONT_BODY,
            fontSize: 22,
            letterSpacing: '0.2em',
            textTransform: 'uppercase',
            color: COLORS.warn,
            marginBottom: 16,
            fontWeight: 600,
          }}
        >
          Time To First Token
        </div>

        {/* Stopwatch Display */}
        <div
          style={{
            fontFamily: FONT_MONO,
            fontSize: 104,
            fontWeight: 800,
            color: '#ffffff',
            letterSpacing: '-0.02em',
            display: 'flex',
            alignItems: 'baseline',
            gap: 14,
            textShadow: `0 0 40px ${COLORS.signal}66`,
          }}
        >
          <span>{elapsedMs.toFixed(2)}</span>
          <span style={{ fontSize: 38, color: COLORS.signal, fontWeight: 600 }}>ms</span>
        </div>

        {/* Comparison Cards */}
        <div
          style={{
            display: 'flex',
            gap: 32,
            marginTop: 64,
            opacity: cardsOpacity,
            transform: `translateY(${cardsSlide}px)`,
          }}
        >
          <Card
            borderColor="rgba(232, 135, 159, 0.4)"
            glow="#e8879f"
            style={{ width: 420, textAlign: 'center' }}
          >
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 12 }}>
              <Clock size={36} color={COLORS.danger} />
            </div>
            <div style={{ fontFamily: FONT_MONO, fontSize: 38, fontWeight: 700, color: '#fff' }}>
              300 ms
            </div>
            <div style={{ fontFamily: FONT_BODY, fontSize: 18, color: '#9aa2b1', marginTop: 6 }}>
              Human Eye Blink
            </div>
          </Card>

          <Card
            borderColor="rgba(77, 184, 168, 0.5)"
            glow="#4db8a8"
            style={{ width: 420, textAlign: 'center' }}
          >
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 12 }}>
              <Zap size={36} color={COLORS.signal} />
            </div>
            <div style={{ fontFamily: FONT_MONO, fontSize: 38, fontWeight: 700, color: '#fff' }}>
              15 - 50 ms
            </div>
            <div style={{ fontFamily: FONT_BODY, fontSize: 18, color: '#9aa2b1', marginTop: 6 }}>
              AI First Response
            </div>
          </Card>

          <Card
            borderColor="rgba(99, 102, 241, 0.4)"
            glow="#6366f1"
            style={{ width: 420, textAlign: 'center' }}
          >
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 12 }}>
              <Brain size={36} color={COLORS.accent} />
            </div>
            <div style={{ fontFamily: FONT_MONO, fontSize: 38, fontWeight: 700, color: '#fff' }}>
              140 Trillion
            </div>
            <div style={{ fontFamily: FONT_BODY, fontSize: 18, color: '#9aa2b1', marginTop: 6 }}>
              Math Ops per Word
            </div>
          </Card>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// =============================================================================
// ACT 2: THE TOKEN PREDICTION ENGINE (0:45 - 1:35 | Frames 1350 - 2850)
// =============================================================================
const Act2TokenParadox: React.FC = () => {
  const frame = useCurrentFrame();
  const rel = frame % 1500;

  const promptText = "The cat sat on the";
  const tokens = [
    { text: 'mat', prob: '92.4%', color: COLORS.signal },
    { text: 'rug', prob: '4.8%', color: COLORS.warn },
    { text: 'couch', prob: '2.1%', color: '#94a3b8' },
    { text: 'moon', prob: '0.01%', color: COLORS.danger },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: '#090b10' }}>
      <ActBadge num="ACT 02" title="The Next-Token Autoregression" />

      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100%',
        }}
      >
        <div style={{ fontFamily: FONT_BODY, fontSize: 22, color: '#94a3b8', marginBottom: 20 }}>
          An LLM generates words one at a time by predicting probabilities
        </div>

        {/* Prompt Terminal Box */}
        <div
          style={{
            backgroundColor: '#161922',
            border: '1.5px solid rgba(255,255,255,0.12)',
            borderRadius: 16,
            padding: '24px 44px',
            fontFamily: FONT_MONO,
            fontSize: 42,
            color: '#fff',
            display: 'flex',
            alignItems: 'center',
            gap: 16,
          }}
        >
          <span>{promptText}</span>
          <span
            style={{
              padding: '6px 18px',
              backgroundColor: 'rgba(77, 184, 168, 0.2)',
              border: `2px dashed ${COLORS.signal}`,
              borderRadius: 8,
              color: COLORS.signal,
              fontWeight: 700,
            }}
          >
            [ NEXT TOKEN ? ]
          </span>
        </div>

        {/* Probability Distribution Cards */}
        <div style={{ display: 'flex', gap: 24, marginTop: 48 }}>
          {tokens.map((t, idx) => (
            <div
              key={t.text}
              style={{
                width: 220,
                backgroundColor: '#11141d',
                border: `1.5px solid ${idx === 0 ? COLORS.signal : 'rgba(255,255,255,0.08)'}`,
                borderRadius: 16,
                padding: '20px 24px',
                textAlign: 'center',
                boxShadow: idx === 0 ? `0 8px 30px ${COLORS.signal}33` : 'none',
              }}
            >
              <div
                style={{
                  fontFamily: FONT_MONO,
                  fontSize: 32,
                  fontWeight: 700,
                  color: t.color,
                }}
              >
                "{t.text}"
              </div>
              <div
                style={{
                  fontFamily: FONT_BODY,
                  fontSize: 20,
                  fontWeight: 600,
                  color: '#cbd5e1',
                  marginTop: 8,
                }}
              >
                {t.prob}
              </div>
              {idx === 0 && (
                <div
                  style={{
                    marginTop: 12,
                    fontSize: 13,
                    fontFamily: FONT_MONO,
                    color: COLORS.signal,
                    textTransform: 'uppercase',
                    letterSpacing: '0.08em',
                  }}
                >
                  SELECTED
                </div>
              )}
            </div>
          ))}
        </div>

        {/* 80-Layer Warning Banner */}
        <div
          style={{
            marginTop: 56,
            display: 'flex',
            alignItems: 'center',
            gap: 14,
            padding: '12px 28px',
            backgroundColor: 'rgba(232, 135, 159, 0.1)',
            border: '1px solid rgba(232, 135, 159, 0.3)',
            borderRadius: 999,
            color: COLORS.danger,
            fontFamily: FONT_BODY,
            fontSize: 18,
            fontWeight: 600,
          }}
        >
          <Layers size={22} />
          <span>Must repeat through 80+ Transformer Layers for EVERY single word</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// =============================================================================
// ACT 3: SILICON & MEMORY BANDWIDTH (1:35 - 2:30 | Frames 2850 - 4500)
// =============================================================================
const Act3SiliconSuperhighways: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#090b10' }}>
      <ActBadge num="ACT 03" title="Silicon Hardware & Memory Bandwidth" />

      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100%',
        }}
      >
        <div style={{ fontFamily: FONT_DISPLAY, fontSize: 36, color: '#fff', fontWeight: 700 }}>
          The Real Bottleneck: Memory Bandwidth
        </div>
        <div style={{ fontFamily: FONT_BODY, fontSize: 20, color: '#94a3b8', marginTop: 10 }}>
          Reading 140GB of model parameters per token requires insane throughput
        </div>

        {/* Comparison Bars */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: 28,
            marginTop: 56,
            width: 1080,
          }}
        >
          {/* Standard DDR5 */}
          <div
            style={{
              backgroundColor: '#121520',
              border: '1px solid rgba(255,255,255,0.08)',
              borderRadius: 16,
              padding: '24px 32px',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
              <span style={{ fontFamily: FONT_BODY, fontSize: 20, color: '#94a3b8', fontWeight: 600 }}>
                Standard PC RAM (DDR5)
              </span>
              <span style={{ fontFamily: FONT_MONO, fontSize: 22, color: COLORS.warn, fontWeight: 700 }}>
                64 GB / sec
              </span>
            </div>
            <div style={{ height: 16, backgroundColor: 'rgba(255,255,255,0.06)', borderRadius: 8 }}>
              <div
                style={{
                  height: '100%',
                  width: '4%',
                  backgroundColor: COLORS.warn,
                  borderRadius: 8,
                }}
              />
            </div>
          </div>

          {/* AI Accelerator HBM3e */}
          <div
            style={{
              backgroundColor: '#121520',
              border: `1.5px solid ${COLORS.signal}`,
              borderRadius: 16,
              padding: '24px 32px',
              boxShadow: `0 8px 36px ${COLORS.signal}22`,
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
              <span style={{ fontFamily: FONT_BODY, fontSize: 20, color: '#fff', fontWeight: 600 }}>
                AI High-Bandwidth Memory (HBM3e)
              </span>
              <span style={{ fontFamily: FONT_MONO, fontSize: 22, color: COLORS.signal, fontWeight: 700 }}>
                3,350 GB / sec (3.35 TB/s)
              </span>
            </div>
            <div style={{ height: 16, backgroundColor: 'rgba(255,255,255,0.06)', borderRadius: 8 }}>
              <div
                style={{
                  height: '100%',
                  width: '98%',
                  backgroundColor: COLORS.signal,
                  borderRadius: 8,
                }}
              />
            </div>
          </div>
        </div>

        <div
          style={{
            marginTop: 48,
            fontFamily: FONT_MONO,
            fontSize: 22,
            color: '#fff',
            display: 'flex',
            alignItems: 'center',
            gap: 12,
          }}
        >
          <Sparkles color={COLORS.signal} />
          <span>50× Faster Data Transfer Directly Connected on 3D Interposers</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// =============================================================================
// ACT 4: THE 3 SPEED MIRACLES (2:30 - 3:45 | Frames 4500 - 6750)
// =============================================================================
const Act4ThreeEngineeringMiracles: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#090b10' }}>
      <ActBadge num="ACT 04" title="The Three Engineering Miracles" />

      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100%',
        }}
      >
        <div style={{ fontFamily: FONT_DISPLAY, fontSize: 40, color: '#fff', fontWeight: 700 }}>
          Software & Algorithmic Magic
        </div>

        <div style={{ display: 'flex', gap: 32, marginTop: 56, width: 1360 }}>
          {/* Miracle 1 */}
          <Card borderColor="rgba(77, 184, 168, 0.4)" glow="#4db8a8" style={{ flex: 1 }}>
            <div
              style={{
                fontFamily: FONT_MONO,
                fontSize: 16,
                color: COLORS.signal,
                fontWeight: 700,
                marginBottom: 12,
              }}
            >
              MIRACLE #1
            </div>
            <div style={{ fontFamily: FONT_DISPLAY, fontSize: 26, color: '#fff', fontWeight: 700 }}>
              KV Caching
            </div>
            <p style={{ fontFamily: FONT_BODY, fontSize: 16, color: '#94a3b8', lineHeight: 1.6, marginTop: 14 }}>
              Instead of recalculating all previous words on every step, past Attention Keys and Values
              are stored in GPU cache. Compute stays flat instead of exploding exponentially.
            </p>
          </Card>

          {/* Miracle 2 */}
          <Card borderColor="rgba(245, 215, 110, 0.4)" glow="#f5d76e" style={{ flex: 1 }}>
            <div
              style={{
                fontFamily: FONT_MONO,
                fontSize: 16,
                color: COLORS.warn,
                fontWeight: 700,
                marginBottom: 12,
              }}
            >
              MIRACLE #2
            </div>
            <div style={{ fontFamily: FONT_DISPLAY, fontSize: 26, color: '#fff', fontWeight: 700 }}>
              Speculative Decoding
            </div>
            <p style={{ fontFamily: FONT_BODY, fontSize: 16, color: '#94a3b8', lineHeight: 1.6, marginTop: 14 }}>
              A tiny 1B draft model guesses 5 words ahead instantly. The giant 70B model verifies all 5
              in parallel during a single forward pass—achieving 3x speedup.
            </p>
          </Card>

          {/* Miracle 3 */}
          <Card borderColor="rgba(99, 102, 241, 0.4)" glow="#6366f1" style={{ flex: 1 }}>
            <div
              style={{
                fontFamily: FONT_MONO,
                fontSize: 16,
                color: COLORS.accent,
                fontWeight: 700,
                marginBottom: 12,
              }}
            >
              MIRACLE #3
            </div>
            <div style={{ fontFamily: FONT_DISPLAY, fontSize: 26, color: '#fff', fontWeight: 700 }}>
              Quantization (INT4/FP8)
            </div>
            <p style={{ fontFamily: FONT_BODY, fontSize: 16, color: '#94a3b8', lineHeight: 1.6, marginTop: 14 }}>
              Compressing 16-bit weights into 4-bit integers halves memory bandwidth requirements,
              doubling throughput with near-zero intelligence degradation.
            </p>
          </Card>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// =============================================================================
// ACT 5: THE PSYCHOLOGY OF SPEED (3:45 - 4:40 | Frames 6750 - 8400)
// =============================================================================
const Act5PsychologyOfSpeed: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#090b10' }}>
      <ActBadge num="ACT 05" title="The Psychology of Speed: Streaming" />

      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100%',
        }}
      >
        <div style={{ fontFamily: FONT_DISPLAY, fontSize: 38, color: '#fff', fontWeight: 700 }}>
          Perception Beats Physics
        </div>
        <div style={{ fontFamily: FONT_BODY, fontSize: 20, color: '#94a3b8', marginTop: 10 }}>
          Why token streaming makes AI feel instantaneous
        </div>

        <div style={{ display: 'flex', gap: 48, marginTop: 64 }}>
          <Card style={{ width: 480, textAlign: 'center' }}>
            <div style={{ fontFamily: FONT_MONO, fontSize: 20, color: COLORS.danger, fontWeight: 700 }}>
              WITHOUT STREAMING
            </div>
            <div style={{ fontFamily: FONT_MONO, fontSize: 52, color: '#fff', fontWeight: 700, marginTop: 14 }}>
              4.2 sec
            </div>
            <div style={{ fontFamily: FONT_BODY, fontSize: 16, color: '#94a3b8', marginTop: 8 }}>
              Wait for entire 400-word response. Feels sluggish and broken.
            </div>
          </Card>

          <Card
            borderColor="rgba(77, 184, 168, 0.4)"
            glow="#4db8a8"
            style={{ width: 480, textAlign: 'center' }}
          >
            <div style={{ fontFamily: FONT_MONO, fontSize: 20, color: COLORS.signal, fontWeight: 700 }}>
              WITH TOKEN STREAMING
            </div>
            <div style={{ fontFamily: FONT_MONO, fontSize: 52, color: '#fff', fontWeight: 700, marginTop: 14 }}>
              0.03 sec
            </div>
            <div style={{ fontFamily: FONT_BODY, fontSize: 16, color: '#94a3b8', marginTop: 8 }}>
              First word arrives in 35ms. AI outputs faster than you can read!
            </div>
          </Card>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// =============================================================================
// ACT 6: CONCLUSION & OUTRO (4:40 - 5:00 | Frames 8400 - 9000)
// =============================================================================
const Act6Outro: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#090b10' }}>
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100%',
        }}
      >
        <div
          style={{
            fontFamily: FONT_MONO,
            fontSize: 22,
            letterSpacing: '0.2em',
            color: COLORS.signal,
            textTransform: 'uppercase',
            fontWeight: 700,
          }}
        >
          Key Takeaway
        </div>
        <div
          style={{
            fontFamily: FONT_DISPLAY,
            fontSize: 64,
            fontWeight: 800,
            color: '#fff',
            marginTop: 18,
            textAlign: 'center',
            letterSpacing: '-0.02em',
          }}
        >
          NOT STORED. CALCULATED.
        </div>
        <div
          style={{
            fontFamily: FONT_BODY,
            fontSize: 24,
            color: '#94a3b8',
            marginTop: 16,
            maxWidth: 800,
            textAlign: 'center',
            lineHeight: 1.5,
          }}
        >
          Answers aren't sitting on a shelf. They are mathematically materialized across thousands
          of tensor cores in microseconds.
        </div>

        {/* Subscribe Banner */}
        <div
          style={{
            marginTop: 64,
            display: 'flex',
            alignItems: 'center',
            gap: 16,
            padding: '16px 36px',
            backgroundColor: 'rgba(255,255,255,0.08)',
            border: '1px solid rgba(255,255,255,0.2)',
            borderRadius: 999,
          }}
        >
          <Sparkles color={COLORS.warn} size={28} />
          <span style={{ fontFamily: FONT_BODY, fontSize: 20, color: '#fff', fontWeight: 600 }}>
            Subscribe for more deep dives into computing architecture
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// =============================================================================
// ROOT 5-MINUTE COMPOSITION
// =============================================================================
export default function Video1AiMilliseconds() {
  return (
    <AbsoluteFill style={{ backgroundColor: '#090b10' }}>
      {/* Act 1: 0 to 45s (0 to 1350 frames) */}
      <Sequence from={0} durationInFrames={1350}>
        <Act1TheIllusion />
      </Sequence>

      {/* Act 2: 45s to 95s (1350 to 2850 frames) */}
      <Sequence from={1350} durationInFrames={1500}>
        <Act2TokenParadox />
      </Sequence>

      {/* Act 3: 95s to 150s (2850 to 4500 frames) */}
      <Sequence from={2850} durationInFrames={1650}>
        <Act3SiliconSuperhighways />
      </Sequence>

      {/* Act 4: 150s to 225s (4500 to 6750 frames) */}
      <Sequence from={4500} durationInFrames={2250}>
        <Act4ThreeEngineeringMiracles />
      </Sequence>

      {/* Act 5: 225s to 280s (6750 to 8400 frames) */}
      <Sequence from={6750} durationInFrames={1650}>
        <Act5PsychologyOfSpeed />
      </Sequence>

      {/* Act 6: 280s to 300s (8400 to 9000 frames) */}
      <Sequence from={8400} durationInFrames={600}>
        <Act6Outro />
      </Sequence>
    </AbsoluteFill>
  );
}

