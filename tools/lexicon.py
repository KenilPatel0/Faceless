#!/usr/bin/env python3
"""
lexicon.py — Phonetic Normalization & Pronunciation Engine for Faceless Video Production.
Transforms technical terms, acronyms, camelCase names, and file extensions into
pronounceable phonetic strings for Kokoro v1.0 ONNX.
"""

import os
import re
import json
from typing import Dict, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LEXICON_PATH = os.path.join(SCRIPT_DIR, "lexicon.json")

def load_lexicon() -> Dict[str, str]:
    """Loads the phonetic dictionary from lexicon.json."""
    if not os.path.exists(LEXICON_PATH):
        return {}
    with open(LEXICON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Flatten categories into a single dictionary sorted by descending key length
    flat: Dict[str, str] = {}
    for cat in ["channels", "file_extensions", "tech_terms"]:
        if cat in data:
            flat.update(data[cat])
    return flat

_LEXICON_CACHE = load_lexicon()

def normalize_speech_text(text: str, custom_overrides: Optional[Dict[str, str]] = None) -> str:
    """
    Normalizes a text string for neural TTS synthesis:
    1. Replaces specific file names (e.g. spec.md -> spec dot M D)
    2. Replaces technical terms using word boundaries
    3. Handles RFC numbers (e.g. RFC 5322 -> R F C 5322)
    4. Handles custom overrides passed from channel profiles
    """
    if not text:
        return ""
    
    out = text

    # Merge custom overrides
    combined = dict(_LEXICON_CACHE)
    if custom_overrides:
        combined.update(custom_overrides)

    # Sort keys by length descending so longer terms match first (e.g. "VS Code" before "VS")
    sorted_keys = sorted(combined.keys(), key=len, reverse=True)

    for term in sorted_keys:
        replacement = combined[term]
        if term.startswith("."):
            # File extension pattern like .md or .py
            pattern = re.escape(term) + r"(?=\b|\s|[.,!?;]|$)"
            out = re.sub(pattern, " " + replacement, out)
        elif "." in term:
            # File name pattern like spec.md: match bounded by space, punctuation, or start/end of string
            pattern = r"(?:(?<=[\s,(\"'])|^)" + re.escape(term) + r"(?=[\s,.)\"'!?;]|$)"
            out = re.sub(pattern, replacement, out, flags=re.IGNORECASE)
        else:
            # Standard word boundary pattern
            pattern = r"\b" + re.escape(term) + r"\b"
            out = re.sub(pattern, replacement, out)

    # Additional standard regex rules for technical audio:
    # 1. RFC numbers: RFC 5322 -> R F C 5322
    out = re.sub(r"\bRFC\s+(\d+)\b", r"R F C \1", out, flags=re.IGNORECASE)
    # 2. Version numbers: v1.0 -> version 1 point 0
    out = re.sub(r"\bv(\d+)\.(\d+)\b", r"version \1 point \2", out, flags=re.IGNORECASE)
    # 3. Double dots or syntax punctuation: -> "dot"
    out = re.sub(r"(?<=[a-zA-Z0-9])\.(?=[a-zA-Z0-9])", " dot ", out)
    # 4. Clean excess whitespace
    out = re.sub(r"\s+", " ", out).strip()

    return out

if __name__ == "__main__":
    test_cases = [
        "In this video we reverse engineer with Aiwolfie using Playwright and Kokoro.",
        "Create a temporary file called spec.md, then run pytest on test_validator.py.",
        "We comply with RFC 5322 and avoid catastrophic regex polynomial backtracking.",
        "TechXKenil provides clean code without shipping garbage to production.",
        "Check stderr and stdout when compiling AST trees with PyTorch on CUDA."
    ]
    print("🧪 Testing Phonetic Speech Normalizer:")
    print("=" * 70)
    for t in test_cases:
        norm = normalize_speech_text(t)
        print(f"Original  : {t}")
        print(f"Normalized: {norm}\n")
