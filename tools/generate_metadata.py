#!/usr/bin/env python3
"""
generate_metadata.py — Automated High-CTR YouTube Metadata & SEO Engine.
Strictly calibrated for TechXKenil channel rules & modern YouTube algorithms (2025/2026).

Features:
- Generates 3 title archetypes (Curiosity Paradox, How It Works, Developer Perspective)
- Validates title lengths (<= 60 chars to prevent mobile truncation)
- Auto-computes timestamped chapters directly from timeline files (tl.json / meta.json)
- Formats 4-zone description (Above-the-fold search hook, value bullets, chapters, community loop)
- Generates categorized tags (< 500 chars limit enforced, no '#' symbols)
- Generates engagement-driving pinned comment prompt
"""

import argparse
import json
import os
import sys

CHANNEL_NAME = "TechXKenil"
CHANNEL_TAG = "TechXKenil"

def format_time(seconds):
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"

def extract_chapters_from_timeline(tl_path, scene_names):
    """Computes exact timestamps from duration array and scene list."""
    with open(tl_path, "r", encoding="utf-8") as f:
        durations = json.load(f)
    
    chapters = []
    current_time = 0.0
    for idx, (scene_title, beat_durs) in enumerate(zip(scene_names, durations)):
        timestamp = format_time(current_time)
        chapters.append(f"{timestamp} {scene_title}")
        current_time += sum(beat_durs)
    return "\n".join(chapters)

def build_metadata(
    topic,
    hook_summary,
    bullets,
    chapters_str=None,
    custom_titles=None,
    tags_list=None,
    pinned_question=None,
    is_short=False
):
    # Titles
    if custom_titles:
        titles = custom_titles
    else:
        titles = [
            f"How {topic} Actually Works (No Math, No Hype)",
            f"The Real Engineering Behind {topic}",
            f"Why {topic} Is Faster Than You Think"
        ]

    # Validate title lengths
    validated_titles = []
    for t in titles:
        status = "✅" if len(t) <= 60 else f"⚠️ ({len(t)} chars > 60)"
        validated_titles.append((t, status))

    # Tags formatting & 500-char verification
    if not tags_list:
        tags_list = [
            topic.lower(),
            f"how {topic.lower()} works",
            f"{topic.lower()} explained",
            "computer science",
            "artificial intelligence",
            "tech explained",
            "software engineering",
            "techxkenil"
        ]
    
    tags_string = ", ".join(tags_list)
    if len(tags_string) > 500:
        # Trim while preserving whole tags
        trimmed = []
        curr_len = 0
        for tag in tags_list:
            if curr_len + len(tag) + 2 <= 495:
                trimmed.append(tag)
                curr_len += len(tag) + 2
            else:
                break
        tags_string = ", ".join(trimmed)

    # Bullet points formatting
    formatted_bullets = "\n".join([f"• {b}" for b in bullets])

    # Default pinned comment
    if not pinned_question:
        pinned_question = f"What part of {topic} surprised you the most? Drop your perspective below! 👇"

    # Assemble Markdown Output
    output = []
    output.append(f"# YouTube Publishing Metadata: {topic}\n")
    
    output.append("## 1. High-CTR Titles (Mobile-Optimized <= 60 Chars)")
    output.append("```text")
    for t, stat in validated_titles:
        output.append(f"{t}")
    output.append("```\n")

    output.append("## 2. Description (Above-the-Fold + Chapters + SEO)")
    output.append("```markdown")
    output.append(hook_summary.strip())
    output.append("\nWhat you'll learn in this breakdown:")
    output.append(formatted_bullets)
    
    if chapters_str:
        output.append("\n⏱️ CHAPTERS:")
        output.append(chapters_str)
        
    output.append(f"\n{pinned_question.split('?')[0]}? Let me know in the comments.")
    output.append(f"\nSubscribe to {CHANNEL_NAME} for practical, honest tech and AI breakdowns.")
    output.append("\n#AI #TechXKenil #TechExplained #ComputerScience #SoftwareEngineering")
    output.append("```\n")

    output.append(f"## 3. Tags ({len(tags_string)}/500 characters, no hashtags)")
    output.append("```text")
    output.append(tags_string)
    output.append("```\n")

    output.append("## 4. Pinned Comment")
    output.append("```markdown")
    output.append(pinned_question)
    output.append("```\n")

    output.append("## 5. ChatGPT Thumbnail Prompt (Non-AI Look & High Curiosity)")
    output.append("```text")
    output.append(f"A documentary-style macro photograph of a real industrial server motherboard resting on an engineer's wooden workbench, shallow depth of field. In sharp focus is an authentic matte-black silicon {topic} processor with exposed copper heatpipes and micro-printed circuit numbers. Resting right beside the chip is an authentic vintage analog mechanical stopwatch, its red needle frozen at a critical moment. Directional tungsten desk lamp lighting, natural soft shadows, subtle film grain. Clean empty space on the left third for text overlay. Absolutely no cheesy sci-fi holograms, no glowing neon particles, no glossy 3D plastic render, no text.")
    output.append("```\n")
    output.append("**Recommended Text Overlay for Thumbnail (Place on left side):**")
    output.append("```text")
    output.append("HOW SO FAST?")
    output.append("```")

    return "\n".join(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Metadata Generator")
    parser.add_argument("--topic", default="AI Latency", help="Video topic")
    parser.add_argument("--hook", default="Here is how modern AI calculates answers in milliseconds.", help="Above-the-fold hook")
    parser.add_argument("--out", default="metadata.md", help="Output path")
    args = parser.parse_args()

    sample_bullets = [
        "The core mathematical constraints",
        "Hardware parallelism: CPUs vs GPUs",
        "Memory bandwidth breakthroughs",
        "The 3 software acceleration tricks"
    ]
    
    res = build_metadata(args.topic, args.hook, sample_bullets)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(res)
    print(f"Metadata generated: {args.out}")

