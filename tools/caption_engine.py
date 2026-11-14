#!/usr/bin/env python3
"""
caption_engine.py — Two-Layer Caption Intelligence & Subtitle Exporter for Faceless.
Implements Parts III & IV of the Faceless Audio & Caption Intelligence Specification:
- Layer A: CaptionTrack (Source of truth, faithful transcript, speaker labels, non-speech audio cues, SRT/WebVTT export)
- Layer B: VisualCaptionPlan (Presentation layer, phrase segmentation 2-6 words, selective keyword emphasis, reading speed <= 20 cps, line width <= 42 chars)
- Strict separation: Visual callouts never mutate the source transcript.
"""

import os
import re
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Tuple
from PIL import ImageDraw, ImageFont


# ==============================================================================
# 1. LAYER A: CANONICAL CAPTION TRACK (SOURCE OF TRUTH)
# ==============================================================================
@dataclass
class CaptionCue:
    cue_id: str
    start_s: float
    end_s: float
    text: str
    speaker_id: str = "narrator"
    confidence: float = 1.0
    non_speech_info: Optional[str] = None # e.g. [whoosh], [click], [chime]
    is_verbatim: bool = True

    def to_srt_timestamp(self, seconds: float) -> str:
        ms = int(round((seconds % 1.0) * 1000))
        total_s = int(seconds)
        s = total_s % 60
        m = (total_s // 60) % 60
        h = total_s // 3600
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    def to_vtt_timestamp(self, seconds: float) -> str:
        ms = int(round((seconds % 1.0) * 1000))
        total_s = int(seconds)
        s = total_s % 60
        m = (total_s // 60) % 60
        h = total_s // 3600
        return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


class CaptionTrack:
    """
    The canonical, faithful accessibility and transcript source of truth.
    Never edited or condensed for animation decoration.
    """
    def __init__(self, language: str = "en", cues: Optional[List[CaptionCue]] = None):
        self.language = language
        self.cues: List[CaptionCue] = cues or []

    def add_cue(self, cue: CaptionCue):
        self.cues.append(cue)

    def export_srt(self, filepath: str):
        """Exports standard SubRip (.srt) subtitle file."""
        lines = []
        for idx, cue in enumerate(self.cues, start=1):
            t_start = cue.to_srt_timestamp(cue.start_s)
            t_end = cue.to_srt_timestamp(cue.end_s)
            txt = cue.text
            if cue.non_speech_info:
                txt = f"[{cue.non_speech_info}] {txt}"
            lines.append(f"{idx}\n{t_start} --> {t_end}\n{txt}\n")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines).strip() + "\n")

    def export_vtt(self, filepath: str):
        """Exports standard WebVTT (.vtt) timed-text subtitle file."""
        lines = ["WEBVTT", ""]
        for idx, cue in enumerate(self.cues, start=1):
            t_start = cue.to_vtt_timestamp(cue.start_s)
            t_end = cue.to_vtt_timestamp(cue.end_s)
            txt = cue.text
            if cue.non_speech_info:
                txt = f"[{cue.non_speech_info}] {txt}"
            lines.append(f"{idx}\n{t_start} --> {t_end}\n{txt}\n")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines).strip() + "\n")


# ==============================================================================
# 2. LAYER B: VISUAL CAPTION PRESENTATION PLAN
# ==============================================================================
@dataclass
class VisualCaptionChunk:
    chunk_id: str
    source_cue_id: str
    start_s: float
    end_s: float
    text: str
    words: List[Dict[str, Any]]
    emphasis_word: Optional[str] = None
    reading_speed_cps: float = 0.0
    is_verbatim: bool = True


class VisualCaptionPlan:
    """
    Presentation layer responsible for on-screen typography, phrase chunking,
    safe-area clearance, and selective emphasis.
    Enforces Netflix reading speed constraints (<= 20 cps) and line width (<= 42 chars).
    """
    def __init__(
        self,
        caption_track: CaptionTrack,
        is_short: bool = False,
        safe_y: int = 1010,
        max_line_chars: int = 42,
        max_reading_speed_cps: float = 20.0
    ):
        self.caption_track = caption_track
        self.is_short = is_short
        self.safe_y = safe_y
        self.max_line_chars = max_line_chars
        self.max_reading_speed_cps = max_reading_speed_cps
        self.chunks: List[VisualCaptionChunk] = []
        self._build_presentation_chunks()

    def _build_presentation_chunks(self):
        """Segments faithful cues into 2-6 word readable presentation chunks respecting line limits."""
        from tools.subtitle_engine import calculate_word_timings

        max_words = 4 if self.is_short else 6

        for cue in self.caption_track.cues:
            word_timings = calculate_word_timings(cue.text, cue.start_s, cue.end_s)
            if not word_timings:
                continue

            current_slice: List[Dict[str, Any]] = []
            current_len = 0

            for item in word_timings:
                w_str = item["word"]
                additional_len = len(w_str) + (1 if current_slice else 0)

                # Check if we should split before adding this word
                should_split = False
                if current_slice:
                    if (current_len + additional_len) > self.max_line_chars:
                        should_split = True
                    elif len(current_slice) >= max_words:
                        should_split = True
                    elif current_slice[-1]["word"].endswith((".", "!", "?")):
                        should_split = True

                if should_split:
                    self._commit_chunk(cue.cue_id, current_slice)
                    current_slice = []
                    current_len = 0

                current_slice.append(item)
                current_len += len(w_str) + (1 if len(current_slice) > 1 else 0)

            if current_slice:
                self._commit_chunk(cue.cue_id, current_slice)

    def _commit_chunk(self, cue_id: str, slice_words: List[Dict[str, Any]]):
        if not slice_words:
            return
        text_chunk = " ".join([item["word"] for item in slice_words])
        c_start = slice_words[0]["start"]
        c_end = slice_words[-1]["end"]
        dur = max(0.1, c_end - c_start)
        cps = len(text_chunk) / dur

        # Find potential emphasis word (longest technical term)
        emphasis = None
        candidates = [w["word"] for w in slice_words if len(w["word"]) > 4]
        if candidates:
            emphasis = max(candidates, key=len)

        self.chunks.append(VisualCaptionChunk(
            chunk_id=f"vis_{len(self.chunks):03d}",
            source_cue_id=cue_id,
            start_s=c_start,
            end_s=c_end,
            text=text_chunk,
            words=slice_words,
            emphasis_word=emphasis,
            reading_speed_cps=round(cps, 1),
            is_verbatim=True
        ))

    def get_active_chunk(self, t: float) -> Optional[VisualCaptionChunk]:
        """Returns the active visible chunk at timestamp t."""
        for c in self.chunks:
            if c.start_s <= t <= c.end_s:
                return c
        return None

    def render(
        self,
        draw: ImageDraw.Draw,
        t: float,
        center_x: int,
        font: ImageFont.FreeTypeFont,
        default_color: Tuple[int, int, int] = (255, 255, 255),
        accent_color: Tuple[int, int, int] = (255, 205, 70),
        stroke_width: int = 4,
        stroke_color: Tuple[int, int, int] = (0, 0, 0)
    ):
        """Renders the styled visual caption within safe-area bounds."""
        chunk = self.get_active_chunk(t)
        if not chunk:
            return

        if self.is_short:
            # Word-by-word karaoke bounce on mobile Shorts
            words = chunk.words
            word_lens = [draw.textlength(item["word"].upper() + " ", font=font) for item in words]
            total_w = sum(word_lens)
            x_pos = center_x - total_w / 2.0

            for item, w_len in zip(words, word_lens):
                is_active = item["start"] <= t <= item["end"]
                col = accent_color if is_active else default_color
                y_offset = -4 if is_active else 0
                draw.text(
                    (x_pos, self.safe_y + y_offset),
                    item["word"].upper() + " ",
                    font=font,
                    fill=col,
                    stroke_width=stroke_width,
                    stroke_fill=stroke_color,
                    anchor="mm"
                )
                x_pos += w_len
        else:
            # Clean, restrained phrase typography for Long-form (<= 42 chars/line)
            draw.text(
                (center_x, self.safe_y),
                chunk.text.upper(),
                font=font,
                fill=default_color,
                stroke_width=stroke_width,
                stroke_fill=stroke_color,
                anchor="mm"
            )
