#!/usr/bin/env python3
"""
channel_config.py — Modular Channel Identity & White-Label Loader for Faceless Video Engine.

Loads channel identity, voice profile, typography, colors, and branding from:
1. Environment variable `CHANNEL_CONFIG` (path to a custom JSON file)
2. `Kenil/channel_profile.json` (local private channel workspace, if present)
3. `channel.json` in project root (user-customized profile)
4. Default white-label fallback profile
"""

import json
import os
from typing import Dict, Any

DEFAULT_CHANNEL_CONFIG: Dict[str, Any] = {
    "channel_name": "TechChannel",
    "creator_name": "Creator",
    "channel_tag": "TechChannel",
    "niche": "AI and Tech",
    "tagline": "AI • TECH • CODE",
    "badge": "TC",
    "logo_path": "media/txk_logo.png",
    "experience_years": 3,
    "voice": {
        "engine": "kokoro-onnx",
        "voice_id": "am_michael",
        "speed": 1.1,
        "lang": "en-us"
    },
    "intro": {
        "text": "I'm {creator_name}, and this is {channel_name}.",
        "badge_text": "TC",
        "badge_ring_color": [150, 110, 255],
        "name_color": [255, 255, 255],
        "tagline_color": [70, 220, 255]
    },
    "outro": {
        "short_narration": "Subscribe to {channel_name} for more {niche}.",
        "button_text": "SUBSCRIBE",
        "button_color": [255, 30, 50],
        "tagline": "AI • TECH • CODE"
    },
    "branding_watermark": {
        "enabled": True,
        "text": "TechChannel",
        "color": [160, 170, 210]
    },
    "hashtags": [
        "#Shorts",
        "#AI",
        "#TechExplained",
        "#ArtificialIntelligence",
        "#ComputerScience"
    ]
}

def get_channel_config(root_dir: str = None, channel_name_or_path: str = None) -> Dict[str, Any]:
    """
    Resolves and returns the active channel profile dictionary.
    Supports explicit channel names ('TechXKenil', 'Aiwolfie') or JSON profile paths.
    """
    if root_dir is None:
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 0. Explicit channel_name_or_path argument
    if channel_name_or_path:
        # Check if direct JSON path
        if os.path.exists(channel_name_or_path):
            try:
                with open(channel_name_or_path, "r", encoding="utf-8") as f:
                    return {**DEFAULT_CHANNEL_CONFIG, **json.load(f)}
            except Exception:
                pass
        
        # Check folders: e.g. TechXKenil, Aiwolfie
        for sub in [channel_name_or_path, f"channels/{channel_name_or_path}"]:
            cand = os.path.join(root_dir, sub, "channel_profile.json")
            if os.path.exists(cand):
                try:
                    with open(cand, "r", encoding="utf-8") as f:
                        return {**DEFAULT_CHANNEL_CONFIG, **json.load(f)}
                except Exception:
                    pass
            cand_json = os.path.join(root_dir, f"{sub}.json")
            if os.path.exists(cand_json):
                try:
                    with open(cand_json, "r", encoding="utf-8") as f:
                        return {**DEFAULT_CHANNEL_CONFIG, **json.load(f)}
                except Exception:
                    pass

        # If named known profile like Aiwolfie, construct dynamic profile
        if channel_name_or_path.lower() in ["aiwolfie", "ai_wolfie"]:
            return {
                **DEFAULT_CHANNEL_CONFIG,
                "channel_name": "AI Wolfie",
                "creator_name": "Wolfie",
                "channel_tag": "Aiwolfie",
                "niche": "AI Reverse Engineering & Agent Systems",
                "tagline": "REVERSE ENGINEERING • AI • AGENTS",
                "badge": "AW",
                "voice": {
                    "engine": "kokoro-onnx",
                    "voice_id": "am_michael",
                    "speed": 1.1,
                    "lang": "en-us"
                }
            }

    # 1. Environment variable override
    env_config_path = os.environ.get("CHANNEL_CONFIG")
    if env_config_path and os.path.exists(env_config_path):
        try:
            with open(env_config_path, "r", encoding="utf-8") as f:
                return {**DEFAULT_CHANNEL_CONFIG, **json.load(f)}
        except Exception:
            pass

    # 2. Local personal channel private space (e.g. TechXKenil/ or Kenil/ if present locally)
    for folder in ["TechXKenil", "Kenil"]:
        profile_path = os.path.join(root_dir, folder, "channel_profile.json")
        if os.path.exists(profile_path):
            try:
                with open(profile_path, "r", encoding="utf-8") as f:
                    return {**DEFAULT_CHANNEL_CONFIG, **json.load(f)}
            except Exception:
                pass

    # 3. Project root user channel.json
    root_channel_path = os.path.join(root_dir, "channel.json")
    if os.path.exists(root_channel_path):
        try:
            with open(root_channel_path, "r", encoding="utf-8") as f:
                return {**DEFAULT_CHANNEL_CONFIG, **json.load(f)}
        except Exception:
            pass

    # 4. Fallback defaults
    return DEFAULT_CHANNEL_CONFIG

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Channel Profile Resolver")
    parser.add_argument("--channel", help="Channel name or path to profile JSON")
    args = parser.parse_args()

    cfg = get_channel_config(channel_name_or_path=args.channel)
    print(f"Loaded Channel: {cfg.get('channel_name')} (Badge: {cfg.get('badge')})")
    print(f"Voice: {cfg.get('voice', {}).get('voice_id')}")
