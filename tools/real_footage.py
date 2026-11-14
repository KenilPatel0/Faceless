#!/usr/bin/env python3
"""
real_footage.py — Production utilities for authentic real-world footage integration.
Handles license logging, attribution generation, shotlist creation, and brand color grading.
"""

import os
import sys
import json
import csv
import shutil
import subprocess
from typing import Dict, List, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))


def find_ffmpeg() -> str:
    """Locates the system or WinGet FFmpeg executable."""
    candidate = shutil.which("ffmpeg")
    if candidate:
        return candidate
    winget_path = os.path.expanduser(r"~\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe")
    if os.path.exists(winget_path):
        return winget_path
    return "ffmpeg"


def validate_license_log(log_path: str, video_duration: float = 0.0) -> Dict[str, any]:
    """
    Validates license_log.json for compliance:
    - Verifies required schema keys
    - Checks that saved license artifacts exist
    - Flags forbidden licenses (CC BY-SA, CC BY-NC, CC BY-ND)
    - Verifies stock footage runtime cap (<= 40%)
    """
    if not os.path.exists(log_path):
        return {"valid": False, "errors": [f"Missing license log file: {log_path}"]}

    with open(log_path, "r", encoding="utf-8") as f:
        try:
            entries = json.load(f)
        except Exception as e:
            return {"valid": False, "errors": [f"Invalid JSON: {e}"]}

    if not isinstance(entries, list):
        entries = [entries]

    errors = []
    warnings = []
    stock_duration = 0.0
    forbidden_terms = ["by-sa", "by-nc", "by-nd", "sharealike", "noncommercial", "noderivatives"]

    for i, entry in enumerate(entries):
        scene = entry.get("scene", i + 1)
        file_name = entry.get("file", "unknown")
        lic = entry.get("license", "").lower()
        source = entry.get("source", "").lower()

        # Check required fields
        for req in ["file", "source", "url", "license"]:
            if req not in entry or not entry[req]:
                errors.append(f"Scene {scene} ({file_name}): missing required field '{req}'")

        # Check for forbidden licenses
        for ft in forbidden_terms:
            if ft in lic:
                errors.append(f"Scene {scene} ({file_name}): forbidden license '{entry.get('license')}'. Only CC0, CC BY, or approved commercial licenses allowed.")

        # Check saved license verification artifact
        saved_lic = entry.get("license_page_saved")
        if saved_lic:
            full_saved = os.path.join(os.path.dirname(log_path), saved_lic)
            if not os.path.exists(full_saved):
                # Check root licenses/ dir
                root_saved = os.path.join(REPO_ROOT, saved_lic)
                if not os.path.exists(root_saved):
                    warnings.append(f"Scene {scene}: saved license artifact not found on disk at '{saved_lic}'")

        # Track stock duration if provided
        dur = float(entry.get("duration", 0.0))
        if source in ["pexels", "pixabay", "mixkit", "coverr", "videvo"]:
            stock_duration += dur

    if video_duration > 0:
        pct = (stock_duration / video_duration) * 100.0
        if pct > 40.0:
            warnings.append(f"Stock footage runtime is {pct:.1f}% ({stock_duration:.1f}s / {video_duration:.1f}s). Playbook mandates stock cap at <= 40%.")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "entries_count": len(entries),
        "stock_duration": stock_duration
    }


def generate_attribution_file(log_path: str, output_txt: str) -> bool:
    """Generates clean attribution.txt text for YouTube video descriptions."""
    if not os.path.exists(log_path):
        return False

    with open(log_path, "r", encoding="utf-8") as f:
        entries = json.load(f)

    if not isinstance(entries, list):
        entries = [entries]

    attributions = []
    for entry in entries:
        if entry.get("attribution_required", False) or "by" in entry.get("license", "").lower():
            file_name = entry.get("file", "Footage clip")
            author = entry.get("author", "Unknown Creator")
            source = entry.get("source", "Web")
            url = entry.get("url", "")
            lic = entry.get("license", "CC BY")
            attributions.append(f"• {file_name} by {author} ({source}) — {lic}: {url}")

    with open(output_txt, "w", encoding="utf-8") as f:
        f.write("# Video Footage & Media Attributions\n\n")
        if attributions:
            f.write("The following openly licensed clips and media were used in this video:\n")
            for a in attributions:
                f.write(f"{a}\n")
        else:
            f.write("All media used is either original creator captures, public domain (CC0), or licensed for commercial use without attribution required.\n")

    return True


def create_shotlist_template(scenes: List[Dict], output_csv: str):
    """Generates a structured shotlist.csv template for video planning."""
    fields = ["scene", "narration", "visual_intent", "source_decision", "search_terms", "final_file", "notes"]
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for s in scenes:
            writer.writerow({
                "scene": s.get("scene", 1),
                "narration": s.get("narration", ""),
                "visual_intent": s.get("visual_intent", ""),
                "source_decision": s.get("source_decision", "1_OWN_CAPTURE / 2_DIAGRAM / 3_PUBLIC_DOMAIN / 4_FREE_STOCK"),
                "search_terms": s.get("search_terms", ""),
                "final_file": s.get("final_file", ""),
                "notes": s.get("notes", "")
            })


def grade_clip(input_mp4: str, output_mp4: str, is_short: bool = False) -> bool:
    """
    Standardizes raw stock / captured footage:
    - Scales and crops to target format (1080x1920 portrait or 1920x1080 landscape)
    - Strips audio (-an)
    - Applies subtle brand color grade (lifted blacks + gentle navy tint)
    """
    ffmpeg_exe = find_ffmpeg()
    if is_short:
        vf = "scale=-2:1920,crop=1080:1920,fps=30,eq=gamma=1.05:saturation=0.92"
    else:
        vf = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,eq=gamma=1.05:saturation=0.92"

    cmd = [
        ffmpeg_exe, "-y", "-i", input_mp4,
        "-vf", vf,
        "-an",
        "-c:v", "libx264",
        "-crf", "16",
        "-preset", "veryfast",
        output_mp4
    ]
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return res.returncode == 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/real_footage.py [validate <license_log.json> | attribution <license_log.json> <out.txt> | grade <in.mp4> <out.mp4> [--short]]")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "validate" and len(sys.argv) > 2:
        res = validate_license_log(sys.argv[2])
        print(f"Validation: {'PASSED' if res['valid'] else 'FAILED'}")
        for err in res["errors"]:
            print(f"  ✗ ERROR: {err}")
        for warn in res["warnings"]:
            print(f"  ⚠️ WARN: {warn}")
        sys.exit(0 if res["valid"] else 1)

    elif cmd == "attribution" and len(sys.argv) > 3:
        ok = generate_attribution_file(sys.argv[2], sys.argv[3])
        print(f"Attribution generation {'succeeded' if ok else 'failed'}")

    elif cmd == "grade" and len(sys.argv) > 3:
        is_sh = "--short" in sys.argv
        ok = grade_clip(sys.argv[2], sys.argv[3], is_short=is_sh)
        print(f"Clip grading {'succeeded' if ok else 'failed'}")
