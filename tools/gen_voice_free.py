#!/usr/bin/env python3
"""
gen_voice_free.py — Free local text-to-speech voice generator for YouTube faceless videos & shorts.
Works out-of-the-box on macOS using native high-quality voices (e.g. Daniel, Samantha, Oliver),
and automatically uses edge-tts if installed. No API keys required.

Usage:
  python3 tools/gen_voice_free.py --text "AI answers before your eye can blink." --out voice.aiff
  python3 tools/gen_voice_free.py --script videos/video-1-ai-milliseconds/script.md --out videos/video-1-ai-milliseconds/voice.aiff
"""

import argparse
import os
import re
import subprocess
import sys


def extract_narration_from_markdown(md_path):
    """Extracts only spoken narration from script markdown tables."""
    text_lines = []
    with open(md_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Match table rows with VO text inside quotes
            matches = re.findall(r'"([^"]+)"', line)
            if matches:
                # Filter out short labels
                vo_candidates = [m for m in matches if len(m) > 15 or m.endswith(('.', '!', '?'))]
                if vo_candidates:
                    text_lines.append(" ".join(vo_candidates))
    return " ".join(text_lines)


def generate_audio(text, output_path, voice="Daniel"):
    print(f"Generating audio ({len(text.split())} words) using macOS voice '{voice}'...")
    cmd = ["say", "-v", voice, text, "-o", output_path]
    subprocess.run(cmd, check=True)
    print(f"Successfully generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Free TTS generator")
    parser.add_argument("--text", help="Direct text to speak")
    parser.add_argument("--script", help="Path to script markdown file")
    parser.add_argument("--out", default="voice.aiff", help="Output audio file path")
    parser.add_argument("--voice", default="Daniel", help="macOS voice name (Daniel, Oliver, Samantha)")

    args = parser.parse_args()

    if args.text:
        content = args.text
    elif args.script:
        if not os.path.exists(args.script):
            sys.exit(f"Script file not found: {args.script}")
        content = extract_narration_from_markdown(args.script)
        if not content:
            # Fallback to reading file directly
            with open(args.script, "r", encoding="utf-8") as f:
                content = f.read()
    else:
        sys.exit("Please provide either --text or --script")

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    generate_audio(content, args.out, voice=args.voice)


if __name__ == "__main__":
    main()

