---
name: youtube-metadata
description: Research-backed YouTube SEO and metadata generator for tech, AI, and faceless channels. Generates high-CTR titles (under 60 chars), 4-zone search-optimized descriptions with exact timestamps, categorized tag lists (under 500 chars), and engagement-driving pinned comments strictly adhering to YouTube algorithm best practices and channel brand guidelines.
---

# youtube-metadata — Research-Backed YouTube SEO & Metadata Engine

A production-ready framework and automated CLI for generating high-converting, algorithm-optimized metadata for YouTube videos and shorts. Calibrated specifically for authentic, calm, practical tech brand voices (honest, practical, calm, zero sensationalist hype) and modern YouTube search/recommendation mechanics.

---

## 1. Algorithmic Research & Ranking Mechanics

Based on retention analytics, YouTube Creator Insider documentation, and recommendation algorithm research:

### How YouTube Uses Metadata in 2025/2026:
1. **Multimodal Verification:** YouTube's AI models automatically transcribe the spoken audio and OCR on-screen visual text within the first 15 seconds. If the metadata promises something that is not verified in the spoken words, impression distribution stalls.
2. **Search vs. Browse Split:** Search accounts for initial velocity on new channels; **Browse and Suggested Videos drive 70%+ of long-term views**. Titles and thumbnails must appeal to human curiosity to trigger Browse impressions, while descriptions and tags seed the search index.
3. **The 1.5-Second Mobile Window:** Over 70% of YouTube impressions happen on mobile screens where titles truncate after **55–60 characters**. If the curiosity hook is not front-loaded in the first 30 characters, the click is lost.

---

## 2. Title Strategy & Archetypes

### Hard Rules:
- **Character Count:** **45 to 60 characters** (never exceed 65 chars to prevent mobile cut-off with `...`).
- **Front-Loading:** Place the core tension, curiosity hook, or primary subject in the **first 4 words**.
- **The Title + Thumbnail Synergy:** **Never repeat the thumbnail text in the title.** They must form a two-part conversation:
  - *Title:* "How AI Answers in Milliseconds (No Math, No Hype)"
  - *Thumbnail:* "140 TRILLION OPS IN 15ms"
- **Brand Rules:** Honest, calm, practical. No doom clickbait, no scary hype, no fake controversy.

### Four Proven Tech Title Archetypes:

| Archetype | Formula | Example |
|---|---|---|
| **1. The Impossible Paradox** | *[Fact that seems to violate standard logic] + [Context]* | `How AI Answers in Milliseconds (It Shouldn't Be Possible)` |
| **2. The "How It Actually Works"** | *How [Complex System] Actually Works ([Reassuring Constraint])* | `How ChatGPT Actually Works (No Math, No Hype)` |
| **3. The Hidden Mechanism** | *The [Hardware/Software Secret] Behind [Apparent Magic]* | `The Silicon Hardware Making AI Feel Instant` |
| **4. The Builder / Contrast Hook** | *[Comparison or Real-World Developer Shift]* | `Chatbot vs AI Agent: What's the Real Difference?` |

---

## 3. The 4-Zone Description Blueprint

A high-converting description is structured into 4 distinct functional zones:

```markdown
[ ZONE 1: The Above-the-Fold Search Hook (First 2-3 lines, ~150-180 chars) ]
A clear, compelling summary answering search intent before the "Show more" fold.

[ ZONE 2: Deep Context & Value Bullets ]
What you'll learn in this breakdown:
• Bullet 1 (Key technical takeaway)
• Bullet 2 (Hardware / architecture insight)
• Bullet 3 (Software / algorithm revelation)

[ ZONE 3: Exact Machine-Computed Chapters ]
⏱️ CHAPTERS:
00:00 The Millisecond Paradox
00:38 Intro
00:41 1. The Token Problem
...

[ ZONE 4: Community & Retention Loop ]
[Engagement Question prompt for comment velocity]
[Channel Subscribe line]
[8-10 Hashtags: #AI #ChannelTag #TopicSpecific]
```

### Chapter Formatting Rules:
- **Must start at `00:00`** (YouTube requires this for chapter generation).
- **Minimum 3 chapters**, each at least 10 seconds long.
- Automatically extracted from the final render cut (`tl.json` / `meta.json`).

---

## 4. The 500-Character Tag Framework

Tags act as secondary clues for the recommendation engine (Suggested Videos / "Up Next") and help match alternative phrasing and misspellings.

### Tag Rules:
- **Character Limit:** Strictly **under 500 characters** total.
- **Format:** Plain text, comma-separated. **NO `#` symbols** inside the tags box.
- **The 4-Tier Tag Hierarchy:**
  1. *Primary Exact Target:* `"how ai answers in milliseconds"`
  2. *Core Tech Entities:* `"tensor cores"`, `"kv caching"`, `"hbm3e"`, `"nvidia h100"`
  3. *Search Intent & Synonyms:* `"chatgpt speed"`, `"time to first token"`, `"why is ai so fast"`
  4. *Broad Niche & Channel Tag:* `"computer science"`, `"artificial intelligence"`, `"channelname"`

---

## 5. Pinned Comment Formula

Early comment velocity signals viewer satisfaction to the YouTube algorithm. Every video must launch with a pinned comment containing:
- An open-ended question that prompts debate or personal experience.
- Example:
  ```markdown
  Did you think AI was searching a database, or did you already know it calculates every word live? Drop your thoughts below! 👇
  ```

---

## 6. CLI Automation Tool: `tools/generate_metadata.py`

Generate a fully verified, copy-paste ready publishing pack using the included tool:

```bash
# Basic generation:
python3 tools/generate_metadata.py \
  --topic "AI Latency" \
  --hook "You press enter on an AI prompt, and in less than fifty milliseconds, words stream across your screen." \
  --out youtube/videos/ai_latency_metadata.md
```

### Integration in Video Pipeline:
When authoring a new video script (`longdata_*.py`), run:
```bash
python3 -c "
import json
from longdata_ms import SCENES
tl = json.load(open('tl_ms.json'))
t = 0.0
for sc, bd in zip(SCENES, tl):
    m, s = int(t // 60), int(t % 60)
    print(f'{m:02d}:{s:02d} ' + sc.get('heading', sc['name'].capitalize()))
    t += sum(bd)
"
```
This guarantees that timestamps in your publishing copy match the final MP4 cut down to the exact second.

