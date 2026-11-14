# Research notes (12 Nov 2026) - what each rule is based on, and how much to trust it

Confidence: A = YouTube's own page; B = reputable news/analysis; C = vendor/creator blogs (directional only, numbers vary and are often self-reported).

## Policy and "human" signal
- A. YouTube Help, "Disclosing use of altered or synthetic content" - https://support.google.com/youtube/answer/14328491?hl=en : disclose realistic synthetic/altered media; list of examples to disclose includes cloning someone else's voice and synthetically generating music; no need to disclose unrealistic content or minor edits; disclosure does not limit audience or monetization eligibility.
- B. YouTube clarified "inauthentic content" on 16 Jul 2026 (three categories incl. generic/repetitive/template-based videos with little variation): https://mediacopilot.ai/youtube-ai-slop-monetization-policy/ , https://logie.ai/news/youtube-ai-slop-crackdown-2026-monetization/ , https://www.tunepocket.com/how-youtube-decides-what-channels-can-be-monetized/ (AI/faceless allowed; originality and variation matter; reviewers look at the whole channel; About section should explain who makes the content and how).
- C. https://hackernoon.com/youtubes-ai-slop-crackdown-cant-tell-a-directed-ai-film-from-a-bot-farm : opinion that detection leans on whether a human appears on camera. Unverified; treat as a risk to monitor, not a rule. Mitigation used here: real screen recordings, real opinions, visible variation.

## Editing rhythm
- C. https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8 : tighter resets early (10-20 s), wider (25-40 s) later; over-editing can hurt; sound design as a retention tool.
- C. https://fluxnote.io/guides/faceless-shorts-retention-tips-2026 : scene change every 2-4 s for faceless shorts; voiceover 160-180 wpm (self-reported dataset).
- C. https://pixflow.net/blog/?p=93140 , https://www.gofaceless.ai/en/blog/optimize-video-engagement-pattern-breaks : change something every 5-7 s early, new element every 8-12 s in shorts. Numbers conflict between sources (3-5 s up to 45-60 s) so the spec uses ranges and the QA gate uses conservative static-hold limits.

## Motion
- C. Motion-design references (impeccable motion-design.md, LottieFiles motion-design skill, Editframe motion process): 100/300/500 ms rule; ease-out for entrances, ease-in for exits, never default "ease"/linear; exits ~75% of entrance; stagger with capped total; sources disagree on bounce - one calls it dated, one allows 10-20% for "playful". This skill chooses the conservative option (<= ~3% overshoot, once per scene).

## Sound
- C. https://www.overseeros.com/blog/youtube-sound-design , https://www.overseeros.com/blog/background-music-volume-under-voiceover , https://pixflow.net/blog/audio-mixing-premiere-pro/ , https://dj-master-web.vercel.app/en/blog/youtube-loudness-standard-en : voice > key SFX > music; music about 18-25 dB under speech with ducking; SFX about -12 to -18 dB; -14 LUFS integrated, true peak about -1 dBTP; voice-led content at about -16 LUFS is fine; do not add a whoosh to everything.

## Measured on the channel's first four videos (12 Nov 2026)
- Loudness: about -24 LUFS (short 1, short 4, long 5, long 2) - roughly 9-10 LU quieter than the -14 LUFS target. Mastered copies (about -15 LUFS, TP about -1.3 dB) were produced; decode check clean.
- Static holds: long 2 and long 5 each have ~22 stretches of 9-12 s where the content area does not change (list scenes between reveals); shorts have none over 4 s. The motion/camera rules in the skill target exactly this.
