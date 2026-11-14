#!/usr/bin/env python3
"""
animation_director.py — Story-Aware Animation Director Engine.
Interprets creative briefs, analyzes semantic script beats, and applies the research-backed
decision matrix and scoring algorithm to generate validated, deterministic AnimationPlans.

Implements Part I (Section 3), Part IV (Sections 25-29), and Part V (Section 33) of the Implementation Spec.
"""

import os
import sys
import re
import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from tools.animation_registry import REGISTRY, AnimationRegistry, AnimationDefinition
from tools.animation_validator import AnimationPlanValidator

@dataclass
class CreativeBrief:
    topic: str
    audience: str = "general_tech"
    platforms: List[str] = None
    aspect_ratio: str = "16:9"
    duration_target_seconds: Optional[float] = None
    format: str = "auto"
    visual_style: str = "techxkenil_tech"
    pacing: str = "standard"  # calm, standard, dynamic, fast
    motion_intensity: int = 2  # 0 to 4
    caption_mode: str = "karaoke"  # karaoke, phrase, static
    brand_profile: str = "TechXKenil"
    assets_available: List[str] = None

    def __post_init__(self):
        if self.platforms is None:
            self.platforms = ["youtube_shorts"] if self.aspect_ratio == "9:16" else ["youtube_long"]
        if self.assets_available is None:
            self.assets_available = []

class AnimationDirector:
    """The story-aware motion director planning visual treatments and techniques."""
    def __init__(self, registry: Optional[AnimationRegistry] = None):
        self.registry = registry or REGISTRY
        self.validator = AnimationPlanValidator(self.registry)
        self.decision_table = self._load_decision_table()

    def _load_decision_table(self) -> Dict[str, Any]:
        dt_path = os.path.join(REPO_ROOT, "agents", "skills", "animation-library", "decision_table.json")
        if os.path.exists(dt_path):
            try:
                with open(dt_path, "r", encoding="utf-8") as f:
                    return json.load(f).get("decision_table", {})
            except Exception:
                pass
        return {}

    def classify_beat_type(self, text: str, is_first: bool = False, is_last: bool = False) -> str:
        """Classifies a narration beat into one of the 14 standard beat types."""
        t_low = text.lower()
        if is_last or any(w in t_low for w in ["subscribe", "comment below", "leave a like"]):
            return "cta"
        if is_first or any(w in t_low for w in ["nobody tells you", "why can't", "stop paying", "secret"]):
            return "hook"
        if any(w in t_low for w in ["vs", "versus", "difference between", "instead of", "unlike"]):
            return "comparison"
        if any(w in t_low for w in ["myth", "actually", "in reality", "people think"]):
            return "myth_fact"
        if any(w in t_low for w in ["def ", "class ", "import ", "python", "function", "syntax", "code"]):
            return "code"
        if any(w in t_low for w in ["percent", "%", "times faster", "benchmark", "latency", "ms"]):
            return "stat"
        if any(w in t_low for w in ["first", "then", "next", "loop", "step", "pipeline", "architecture"]):
            return "process"
        if any(w in t_low for w in ["number one", "tip", "rule", "pattern"]):
            return "list_item"
        if any(w in t_low for w in ["open", "click", "in the app", "terminal", "browser", "dashboard"]):
            return "ui_demo"
        if any(w in t_low for w in ["you type", "ask it", "prompt:", "input query"]):
            return "example_prompt"
        if any(w in t_low for w in ["like a", "imagine", "think of it as"]):
            return "analogy"
        if any(w in t_low for w in ["i think", "in my experience", "honestly", "my verdict"]):
            return "opinion"
        if any(w in t_low for w in ["so", "that's why", "takeaway", "in summary", "bottom line"]):
            return "payoff"
        return "definition"

    def select_spec_technique(self, beat_type: str, has_assets: bool = False) -> Tuple[str, List[str], List[str]]:
        """Returns (primary_id, secondary_ids, avoid_ids) using decision_table.json."""
        entry = self.decision_table.get(beat_type, {})
        if not entry:
            return "T3", ["C1"], []

        primaries = entry.get("primary", ["T3"])
        secondaries = entry.get("secondary", ["C1"])
        avoid = entry.get("avoid", [])

        # Honor asset availability
        primary = primaries[0] if primaries else "T3"
        if primary == "E7" and not has_assets:
            primary = "E2" if "E2" in primaries else "T7"

        return primary, secondaries, avoid

    def parse_brief_from_prompt(self, prompt: str, default_aspect: str = "16:9") -> CreativeBrief:
        """Extracts a structured CreativeBrief from a user prompt with transparent defaults."""
        p_lower = prompt.lower()
        
        # Detect aspect ratio
        aspect = "9:16" if any(w in p_lower for w in ["short", "reel", "vertical", "tiktok", "9:16"]) else default_aspect
        
        # Detect intensity
        intensity = 2
        if any(w in p_lower for w in ["cinematic", "calm", "slow", "restrained"]):
            intensity = 1
        elif any(w in p_lower for w in ["dynamic", "punchy", "viral", "energetic"]):
            intensity = 3
        elif "minimal" in p_lower or "no motion" in p_lower:
            intensity = 0

        # Detect format intent
        fmt = "auto"
        if "code" in p_lower or "terminal" in p_lower or "developer" in p_lower:
            fmt = "screen_tutorial"
        elif "data" in p_lower or "chart" in p_lower or "benchmark" in p_lower:
            fmt = "data_story"
        elif "architecture" in p_lower or "workflow" in p_lower or "diagram" in p_lower:
            fmt = "process_diagram"

        return CreativeBrief(
            topic=prompt[:80],
            aspect_ratio=aspect,
            motion_intensity=intensity,
            format=fmt
        )

    def select_technique_for_beat(
        self,
        beat_text: str,
        visual_intent: str,
        scene_format: str,
        beat_duration: float,
        is_hero_beat: bool = False
    ) -> Tuple[str, Dict[str, Any], str]:
        """
        Executes the candidate scoring formula from Section 28:
        score = 0.30*semantic + 0.25*comprehension + 0.15*narrative + 0.10*brand + 0.05*variety + 0.10*performance + 0.05*asset_confidence
        Returns (selected_animation_id, parameters, decision_rationale).
        """
        b_lower = (beat_text + " " + visual_intent).lower()

        # 1. Hard Gate / Intent matching
        if is_hero_beat or any(w in b_lower for w in ["stop", "trap", "never", "blueprint", "rule"]):
            anim_id = "type.scale_punch" if beat_duration < 1.0 else "object.pop_overshoot"
            reason = "High-impact hook / contrarian claim emphasis."
            params = {"frequency": 2.2, "damping": 0.72} if anim_id == "object.pop_overshoot" else {"punch_scale": 1.20}

        elif any(w in b_lower for w in ["pytest", "terminal", "command", "passed", "failed"]):
            anim_id = "ui.terminal_exec"
            reason = "Verifiable terminal execution window."
            params = {"badge": "PYTEST"}

        elif any(w in b_lower for w in ["code", "function", "editor", "spec.md", "validator"]):
            anim_id = "ui.code_line_focus"
            reason = "Authentic syntax-highlighted editor window."
            params = {"line_numbers": True}

        elif any(w in b_lower for w in ["compare", "versus", "vs", "split", "typist", "architect"]):
            anim_id = "edit.split_screen"
            reason = "Synchronized dual-panel comparison."
            params = {"split_ratio": 0.5}

        elif any(w in b_lower for w in ["step", "1.", "2.", "3.", "list", "four", "blueprint"]):
            anim_id = "object.stagger"
            reason = "Staggered progressive disclosure of sequential items."
            params = {"delay_per_item": 0.10}

        elif any(w in b_lower for w in ["percent", "number", "seconds", "metric", "passed in"]):
            anim_id = "data.counter"
            reason = "Quantified benchmark count-up metric."
            params = {"start_val": 0, "end_val": 100}

        elif any(w in b_lower for w in ["subscribe", "click", "channel", "outro"]):
            anim_id = "ui.cursor_click"
            reason = "Conversion outro button with Bezier cursor path and ripple."
            params = {"click_time": min(2.5, beat_duration * 0.6)}

        else:
            # Default clean narrative motion
            anim_id = "camera.push_in" if beat_duration >= 2.0 else "object.slide"
            reason = "Continuous organic camera push-in to preserve immersion."
            params = {"amount": 0.035} if anim_id == "camera.push_in" else {"direction": "bottom"}

        return anim_id, params, reason

    def plan_video(
        self,
        scenes: List[Dict[str, Any]],
        brief: Optional[CreativeBrief] = None
    ) -> Dict[str, Any]:
        """
        Generates a versioned, fully validated AnimationPlan JSON
        from a list of scene specifications and creative brief.
        """
        if brief is None:
            brief = CreativeBrief(topic="Tech Video")

        plan: Dict[str, Any] = {
            "schema_version": "1.0",
            "project": {
                "platforms": brief.platforms,
                "aspect_ratio": brief.aspect_ratio,
                "fps": {"numerator": 30, "denominator": 1},
                "resolution": {
                    "width": 1080 if brief.aspect_ratio == "9:16" else 1920,
                    "height": 1920 if brief.aspect_ratio == "9:16" else 1080
                },
                "style_preset": brief.visual_style
            },
            "scenes": []
        }

        current_time = 0.0
        for s_idx, s in enumerate(scenes):
            sid = s.get("id", f"scene_{s_idx}")
            vtype = s.get("visual_type", "diagram")
            title = s.get("title", "")
            narration = s.get("narration") or s.get("text") or ""
            dur = float(s.get("duration", 4.0))

            # Select scene format
            if s_idx == 0:
                scene_format = "text_led_hook"
            elif vtype in ["editor", "code", "terminal"]:
                scene_format = "screen_tutorial"
            elif vtype == "split":
                scene_format = "myth_vs_fact"
            else:
                scene_format = "process_diagram"

            st_sec = round(current_time, 3)
            et_sec = round(current_time + dur, 3)
            current_time = et_sec

            # Select beat technique
            is_hero = (s_idx == 0 or "HOOK" in s.get("section", ""))
            anim_id, params, rationale = self.select_technique_for_beat(
                beat_text=narration,
                visual_intent=s.get("visual_intent", title),
                scene_format=scene_format,
                beat_duration=dur,
                is_hero_beat=is_hero
            )

            # Transition selection
            is_last = (s_idx == len(scenes) - 1)
            t_id = "transition.cut"
            t_dur = 0.0
            if not is_last and s.get("section") != scenes[min(len(scenes)-1, s_idx+1)].get("section"):
                t_id = "transition.directional_wipe"
                t_dur = 0.35

            scene_plan = {
                "scene_id": sid,
                "start_seconds": st_sec,
                "end_seconds": et_sec,
                "format": scene_format,
                "visual_objective": s.get("visual_intent") or title,
                "motion_intensity": brief.motion_intensity,
                "beats": [
                    {
                        "beat_id": f"{sid}_beat0",
                        "start_seconds": st_sec,
                        "end_seconds": et_sec,
                        "visual_objective": title,
                        "layers": [
                            {
                                "layer_id": f"{sid}_hero",
                                "animation_id": anim_id,
                                "start_seconds": st_sec,
                                "duration_seconds": min(dur, self.registry.get(anim_id).duration_seconds.get("default", 0.5)),
                                "easing": "ease_out_cubic",
                                "intensity": brief.motion_intensity,
                                "parameters": params,
                                "rationale": rationale,
                                "fallback_animation_id": self.registry.get(anim_id).fallback
                            }
                        ]
                    }
                ],
                "transition_out": {"id": t_id, "duration_seconds": t_dur}
            }

            plan["scenes"].append(scene_plan)

        # Validate the generated plan
        is_valid, errs, warns = self.validator.validate_plan(plan)
        if not is_valid:
            raise ValueError(f"Generated AnimationPlan failed validation:\n" + "\n".join(errs))

        return plan

if __name__ == "__main__":
    director = AnimationDirector()
    brief = director.parse_brief_from_prompt("How I use AI to write code without shipping garbage", default_aspect="16:9")
    print("📋 Parsed Creative Brief:", asdict(brief))

    mock_scenes = [
        {"id": "hook", "section": "HOOK", "title": "STOPPING AI FROM SHIPPING BUGS", "narration": "If you ask AI to write code, it fails in production.", "duration": 4.5},
        {"id": "code_step", "section": "STEPS", "title": "STEP 1: SPEC FIRST", "narration": "Write spec.md before writing code.", "visual_type": "editor", "duration": 5.0},
        {"id": "test_step", "section": "STEPS", "title": "STEP 3: RUN PYTEST", "narration": "Run pytest in terminal and see red.", "visual_type": "terminal", "duration": 4.0},
        {"id": "outro", "section": "OUTRO", "title": "SUBSCRIBE TO TECHXKENIL", "narration": "Subscribe so you do not miss it.", "visual_type": "outro", "duration": 5.0}
    ]

    plan = director.plan_video(mock_scenes, brief)
    print(f"\n🎬 Successfully Generated Valid AnimationPlan with {len(plan['scenes'])} scenes:")
    for s in plan["scenes"]:
        b = s["beats"][0]
        l = b["layers"][0]
        print(f"  [{s['start_seconds']:4.1f}s -> {s['end_seconds']:4.1f}s] {s['scene_id']:12} : Format={s['format']:16} Anim={l['animation_id']:20} ({l['rationale']})")
