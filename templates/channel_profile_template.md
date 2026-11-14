# Channel Profile & Production Rules Template

Use this template to configure your custom channel branding, persona, design language, and video rules.

---

## 1. Channel Identity
- **Channel Name:** `YourChannelName`
- **Creator / Host Name:** `YourName`
- **Niche:** AI, Tech, Software Engineering, or Science Explainers
- **Tagline:** `AI • TECH • CODE`
- **Logo / Intro Badge:** 2-3 letter abbreviation (e.g. `YCN`)
- **Tone:** Honest, calm, practical, zero clickbait / doom hype.

---

## 2. Voice Configuration
- **TTS Engine:** Kokoro v1.0 (ONNX) via `kokoro-onnx`
- **Voice Model:** `am_michael` (or other Kokoro voices: `af_bella`, `af_nicole`, `am_adam`, `bm_george`, etc.)
- **Speed:** `1.1` (Shorts), `1.05 - 1.1` (Long explainers)
- **Language:** `en-us`

---

## 3. Brand Design System
- **Background:** Vertical dark gradient `(8,12,28) -> (30,16,70)` with subtle 90px grid lines `(22,28,58)`
- **Typography:** Inter Display Bold (captions, headlines, badges)
- **Palette:**
  - Accent Cyan: `(70, 220, 255)`
  - Accent Purple: `(150, 110, 255)`
  - Warning Yellow: `(255, 205, 70)`
  - Success Green: `(90, 235, 150)`
  - Alert Red: `(255, 70, 90)`

---

## 4. Hook, Intro & Outro Structure
- **Shorts (30s):**
  - Beat 1: Hook (first line, big visual, immediate intrigue)
  - Beat 2: Intro Card: Badge ring (`YCN`), Channel Name, Tagline (`"I'm {Name}, and this is {Channel}."`)
  - Beats 3-6: Core dynamic beats (progressive reveal, sub-pixel physics, karaoke captions)
  - Final Beat: Outro Card: Subscribe button with pulse + `"Subscribe to {Channel} for more {Niche}."`
- **Long Videos (8-10m):**
  - Section-based breakdown with chapter timestamps, real UI screen captures, and master loudness (-14 LUFS).

---

## 5. How to Activate Your Profile
1. Copy `channel.example.json` to `channel.json` in the root folder.
2. Edit the values with your channel name, badge, and voice settings.
3. When using Antigravity or CLI scripts, your channel profile is loaded automatically!

