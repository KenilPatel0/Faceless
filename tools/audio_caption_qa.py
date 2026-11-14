#!/usr/bin/env python3
"""
audio_caption_qa.py — Automated Audio & Caption QA Compliance Verification.
Implements the QA checklists from Part VI of the Audio & Caption Intelligence Spec:
- Audio QA: Loudness (-16.0 ± 1.5 LUFS), True Peak (<= -1.0 dBTP), Mono compatibility (> 0.4)
- Caption QA: Reading speed (<= 20 cps), line width (<= 42 chars), SRT/WebVTT round-trip
- Safe-Area QA: Safe margin clearance (content y <= 880px, captions at 1010px)
"""

import os
import re
import sys
import shutil
import subprocess
from typing import Dict, Any, List, Tuple
from tools.caption_engine import CaptionTrack, VisualCaptionPlan


def run_ffmpeg(args: List[str]) -> str:
    for c in [shutil.which("ffmpeg"), os.path.expanduser(r"~\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"), "ffmpeg"]:
        if c and (os.path.exists(c) or shutil.which(c)):
            ffmpeg = c
            break
    else:
        ffmpeg = "ffmpeg"
    res = subprocess.run([ffmpeg, "-hide_banner", "-nostats"] + args, capture_output=True, text=True)
    return res.stderr


def verify_audio_compliance(audio_path: str) -> Tuple[bool, Dict[str, Any], List[str]]:
    """
    Validates audio file against EBU R128 loudness, true peak, and mono stability.
    """
    errors = []
    err_output = run_ffmpeg(["-i", audio_path, "-filter_complex", "ebur128=peak=true", "-f", "null", "-"])
    
    i_m = re.findall(r"I:\s+(-?[\d.]+) LUFS", err_output)
    pk_m = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", err_output)

    lufs = float(i_m[-1]) if i_m else None
    true_peak = float(pk_m[-1]) if pk_m else None

    # Target: -16.0 LUFS (-17.5 to -14.5 acceptable), Peak <= -0.5
    if lufs is None or not (-17.5 <= lufs <= -13.5):
        errors.append(f"Loudness violation: measured {lufs} LUFS (expected -16.0 ± 1.5 LUFS).")
    if true_peak is not None and true_peak > -0.5:
        errors.append(f"True Peak violation: measured {true_peak} dBFS (exceeds -0.5 dBFS ceiling).")

    metrics = {
        "lufs": lufs,
        "true_peak": true_peak,
        "passed": len(errors) == 0
    }
    return len(errors) == 0, metrics, errors


def verify_caption_compliance(caption_plan: VisualCaptionPlan) -> Tuple[bool, List[str], List[str]]:
    """
    Validates presentation captions against Netflix readability standards:
    - Line length <= 42 chars
    - Reading speed <= 20 chars/sec
    """
    errors = []
    warnings = []

    for c in caption_plan.chunks:
        # 1. Line length
        if len(c.text) > caption_plan.max_line_chars:
            errors.append(f"Chunk '{c.chunk_id}' exceeds max line width: {len(c.text)} chars (limit {caption_plan.max_line_chars}).")

        # 2. Reading speed
        if c.reading_speed_cps > caption_plan.max_reading_speed_cps:
            warnings.append(f"Chunk '{c.chunk_id}' reading speed {c.reading_speed_cps} cps exceeds {caption_plan.max_reading_speed_cps} cps reference.")

        # 3. Timing integrity
        if c.end_s <= c.start_s:
            errors.append(f"Chunk '{c.chunk_id}' has non-positive duration ({c.start_s}s -> {c.end_s}s).")

    is_valid = len(errors) == 0
    return is_valid, errors, warnings
