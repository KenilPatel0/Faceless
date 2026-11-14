#!/usr/bin/env python3
"""
subtitle_engine.py — High-Precision Syllable-Weighted Caption & Karaoke Engine.
Eliminates linear subtitle drift by calculating per-word durations based on syllable counts
and punctuation pauses, perfectly synchronizing text chunks with spoken narration.
"""

import re
import math
from typing import List, Tuple, Dict, Any, Optional
from PIL import ImageDraw, ImageFont

def count_syllables(word: str) -> int:
    """Estimates the syllable count of an English word."""
    clean = re.sub(r"[^a-zA-Z]", "", word.lower())
    if not clean:
        return 1
    if len(clean) <= 3:
        return 1
    # Count vowel groups
    vowels = re.findall(r"[aeiouy]+", clean)
    count = len(vowels)
    # Adjust for silent 'e' at end
    if clean.endswith("e") and not clean.endswith("le") and count > 1:
        count -= 1
    return max(1, count)

def calculate_word_timings(text: str, start_time: float, end_time: float) -> List[Dict[str, Any]]:
    """
    Calculates per-word start and end timestamps across [start_time, end_time]
    using syllable weighting and punctuation hold adjustments.
    """
    total_dur = max(0.01, end_time - start_time)
    words = text.strip().split()
    if not words:
        return []

    # Assign weights: syllables + punctuation hold
    weights = []
    for w in words:
        syl = count_syllables(w)
        extra = 0.0
        if w.endswith((".", "!", "?")):
            extra = 1.4  # sentence pause
        elif w.endswith((",", ";", ":", "—", "-")):
            extra = 0.8  # clause pause
        weights.append(syl + extra)

    total_weight = sum(weights)
    if total_weight <= 0:
        total_weight = float(len(words))
        weights = [1.0] * len(words)

    # Distribute duration proportionally
    out = []
    t = start_time
    for w, wt in zip(words, weights):
        w_dur = (wt / total_weight) * total_dur
        out.append({
            "word": w,
            "start": round(t, 3),
            "end": round(t + w_dur, 3),
            "duration": round(w_dur, 3)
        })
        t += w_dur

    return out

def build_caption_chunks(word_timings: List[Dict[str, Any]], is_short: bool = False) -> List[Dict[str, Any]]:
    """
    Groups words into human-edited caption chunks:
    - Shorts: 3 to 4 words per chunk
    - Long form: 6 to 9 words per chunk (max 1 line)
    """
    chunk_size = 4 if is_short else 8
    chunks = []
    
    for i in range(0, len(word_timings), chunk_size):
        slice_words = word_timings[i:i + chunk_size]
        text_chunk = " ".join([item["word"] for item in slice_words]).upper()
        c_start = slice_words[0]["start"]
        c_end = slice_words[-1]["end"]
        chunks.append({
            "text": text_chunk,
            "start": c_start,
            "end": c_end,
            "words": slice_words
        })
    return chunks

class SubtitleTrack:
    """Manages full video subtitle lookup and rendering."""
    def __init__(self, timeline: List[Dict[str, Any]], is_short: bool = False):
        self.is_short = is_short
        self.chunks: List[Dict[str, Any]] = []
        for scene in timeline:
            raw_text = scene.get("text") or scene.get("narration") or ""
            st = scene["start_time"]
            et = scene["end_time"]
            w_timings = calculate_word_timings(raw_text, st, et)
            scene_chunks = build_caption_chunks(w_timings, is_short=is_short)
            self.chunks.extend(scene_chunks)

    def get_active_chunk(self, t: float) -> Optional[Dict[str, Any]]:
        """Returns the active subtitle chunk at time t, or None if during silence."""
        for c in self.chunks:
            if c["start"] <= t <= c["end"]:
                return c
        return None

    def render_subtitle(
        self,
        draw: ImageDraw.Draw,
        t: float,
        center_x: int,
        center_y: int,
        font: ImageFont.FreeTypeFont,
        color: Tuple[int, int, int] = (255, 255, 255),
        active_color: Tuple[int, int, int] = (255, 205, 70),
        stroke_width: int = 5,
        stroke_color: Tuple[int, int, int] = (0, 0, 0)
    ):
        """Renders the synchronized subtitle at time t."""
        chunk = self.get_active_chunk(t)
        if not chunk:
            return

        if self.is_short:
            # Karaoke word bounce for Shorts
            words = chunk["words"]
            word_lens = [draw.textlength(item["word"].upper() + " ", font=font) for item in words]
            total_w = sum(word_lens)
            x_pos = center_x - total_w / 2.0
            
            for item, w_len in zip(words, word_lens):
                is_active = item["start"] <= t <= item["end"]
                fill_col = active_color if is_active else color
                # Subtle bounce when active
                y_offset = -4 if is_active else 0
                draw.text(
                    (x_pos, center_y + y_offset),
                    item["word"].upper(),
                    font=font,
                    fill=fill_col,
                    anchor="lm",
                    stroke_width=stroke_width,
                    stroke_fill=stroke_color
                )
                x_pos += w_len
        else:
            # Clean centered 1-line display for Long videos
            draw.text(
                (center_x, center_y),
                chunk["text"],
                font=font,
                fill=color,
                anchor="mm",
                stroke_width=stroke_width,
                stroke_fill=stroke_color
            )

if __name__ == "__main__":
    test_narration = "In this video, I am walking you through my exact four-step blueprint for writing clean, production-grade code with AI."
    timings = calculate_word_timings(test_narration, 0.0, 6.5)
    print("🧪 Syllable-Weighted Word Timings:")
    print("=" * 60)
    for wt in timings[:6]:
        print(f"  [{wt['start']:4.2f}s -> {wt['end']:4.2f}s] ({wt['duration']:4.2f}s) {wt['word']}")
    
    chunks = build_caption_chunks(timings, is_short=False)
    print("\n📦 Long-Form Caption Chunks:")
    for ch in chunks:
        print(f"  [{ch['start']:4.2f}s -> {ch['end']:4.2f}s] {ch['text']}")
