#!/usr/bin/env python3
"""
story_director.py — Storytelling & Scene Direction Intelligence for Faceless.
Implements the Faceless Storytelling, Scene Direction & Visual Production Specification:
- StoryBrief (format, audience, core promise, tone, factuality mode)
- BeatAnalyzer & StoryBeat (12 beat types: hook, context, problem, mechanism, etc.)
- VisualBible (palette, typography, camera language, environment presets)
- ScenePlan & ShotPlan (scene archetypes, multi-layer staging, transitions)
"""

import json
import uuid
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Tuple


# ==============================================================================
# 1. STORY FORMATS & NARRATIVE DEFINITIONS
# ==============================================================================
FORMAT_GRAMMAR = {
    "technology_explainer": {
        "arc": ["question", "context", "mechanism", "implication", "takeaway"],
        "recommended_treatments": ["motion_graphics_explainer", "screen_recording_doc", "isometric"],
        "archetypes": ["system_overview", "flow_pipeline", "data_proof", "recap_tableau"]
    },
    "educational_lesson": {
        "arc": ["learning_goal", "misconception", "explanation", "worked_example", "recap"],
        "recommended_treatments": ["motion_graphics_explainer", "whiteboard", "data_visualization"],
        "archetypes": ["step_build", "comparison_board", "worked_example", "recap_tableau"]
    },
    "product_showcase": {
        "arc": ["pain_point", "product_reveal", "workflow", "proof", "cta"],
        "recommended_treatments": ["product_showcase", "screen_recording_doc"],
        "archetypes": ["authentic_product_reveal", "ui_walkthrough", "feature_closeup", "proof_screen"]
    },
    "case_study": {
        "arc": ["baseline", "intervention", "evidence", "result", "lesson"],
        "recommended_treatments": ["data_visualization", "screen_recording_doc"],
        "archetypes": ["data_proof", "comparison_board", "timeline_chronology", "recap_tableau"]
    },
    "tutorial_walkthrough": {
        "arc": ["goal", "setup", "steps", "verification", "next_action"],
        "recommended_treatments": ["screen_recording_doc", "code_editor"],
        "archetypes": ["ui_walkthrough", "code_editor", "terminal", "proof_screen"]
    },
    "short_form_micro_story": {
        "arc": ["hook", "context", "proof", "payoff", "cta"],
        "recommended_treatments": ["typography_led", "motion_graphics_explainer", "product_showcase"],
        "archetypes": ["cold_open_result", "system_overview", "data_proof", "recap_tableau"]
    }
}

VALID_BEAT_TYPES = {
    "hook", "context", "problem", "mechanism", "evidence",
    "comparison", "escalation", "reveal", "example", "resolution", "recap", "cta"
}

VALID_SCENE_ARCHETYPES = {
    "cold_open_result", "establishing_environment", "system_overview",
    "exploded_view", "flow_pipeline", "cause_effect", "step_build",
    "comparison_board", "data_proof", "authentic_product_reveal",
    "ui_walkthrough", "feature_closeup", "code_editor", "terminal",
    "proof_screen", "recap_tableau"
}


# ==============================================================================
# 2. DATA CONTRACTS (STORY BRIEF, BEAT, SCENE, SHOT)
# ==============================================================================
@dataclass
class StoryBrief:
    project_id: str
    title: str
    format: str = "technology_explainer"
    target_platforms: List[str] = field(default_factory=lambda: ["youtube"])
    audience: str = "developers and technology professionals"
    viewer_question: str = ""
    core_promise: str = ""
    tone: List[str] = field(default_factory=lambda: ["clear", "calm", "practical"])
    factuality_mode: str = "evidence_required"
    duration_target_seconds: float = 60.0
    aspect_ratio: str = "16:9"
    visual_style_preset: str = "txk_tech_cinematic"
    channel_name: str = "TechXKenil"

    def validate(self) -> List[str]:
        errors = []
        if not self.title:
            errors.append("StoryBrief requires a non-empty title.")
        if self.format not in FORMAT_GRAMMAR:
            errors.append(f"Invalid format '{self.format}'. Must be one of: {list(FORMAT_GRAMMAR.keys())}")
        if self.aspect_ratio not in ["16:9", "9:16", "1:1"]:
            errors.append(f"Invalid aspect_ratio '{self.aspect_ratio}'. Must be '16:9', '9:16', or '1:1'.")
        return errors


@dataclass
class StoryBeat:
    beat_id: str
    order: int
    text: str
    beat_type: str = "mechanism"
    viewer_question: str = ""
    takeaway: str = ""
    visual_concept: str = ""
    emotional_intent: str = "clarity"
    evidence_required: bool = False
    continuity_motif: str = ""

    def validate(self) -> List[str]:
        errors = []
        if not self.text.strip():
            errors.append(f"Beat {self.beat_id} has empty text.")
        if self.beat_type not in VALID_BEAT_TYPES:
            errors.append(f"Beat {self.beat_id} has invalid beat_type '{self.beat_type}'.")
        return errors


@dataclass
class VisualBible:
    preset_name: str = "txk_tech_cinematic"
    primary_color: Tuple[int, int, int] = (70, 220, 255)      # Cyan
    secondary_color: Tuple[int, int, int] = (150, 110, 255)   # Purple
    accent_color: Tuple[int, int, int] = (255, 205, 70)       # Electric Yellow
    bg_dark: Tuple[int, int, int] = (10, 13, 20)              # Obsidian
    card_fill: Tuple[int, int, int] = (16, 20, 36)
    card_border: Tuple[int, int, int] = (70, 220, 255, 60)
    title_font: str = "Inter Display Bold"
    body_font: str = "Inter"
    code_font: str = "JetBrains Mono"
    default_camera_push: float = 0.035
    safe_caption_y_1080p: int = 1010
    safe_content_max_y_1080p: int = 880


@dataclass
class ShotPlan:
    shot_id: str
    shot_type: str = "wide"       # wide, medium, closeup, extreme_closeup, split
    camera_movement: str = "push" # push, pull, pan, locked
    intensity: float = 0.25
    focal_target: str = "center"
    duration_s: float = 3.0


@dataclass
class ScenePlan:
    scene_id: str
    beat_ids: List[str]
    title: str
    archetype: str
    purpose: str
    viewer_takeaway: str
    start_time: float
    duration: float
    environment_type: str = "branded_abstract"
    visual_treatment: str = "motion_graphics_explainer"
    shots: List[ShotPlan] = field(default_factory=list)
    layers: List[Dict[str, Any]] = field(default_factory=list)
    audio_triggers: List[Dict[str, Any]] = field(default_factory=list)
    transition_out: Dict[str, Any] = field(default_factory=lambda: {"type": "direct_cut"})
    continuity_tags: List[str] = field(default_factory=list)

    def validate(self) -> List[str]:
        errors = []
        if not self.beat_ids:
            errors.append(f"Scene {self.scene_id} must link to at least one beat.")
        if self.archetype not in VALID_SCENE_ARCHETYPES:
            errors.append(f"Scene {self.scene_id} has invalid archetype '{self.archetype}'.")
        if self.duration <= 0.0:
            errors.append(f"Scene {self.scene_id} has invalid duration {self.duration}s.")
        return errors


# ==============================================================================
# 3. STORY DIRECTING & SCENE PLANNING ENGINE
# ==============================================================================
class StoryDirector:
    """
    Translates raw script text or scene dictionaries into a fully structured,
    storyboard-directed ScenePlan adhering to narrative pacing and visual grammar.
    """
    def __init__(self, bible: Optional[VisualBible] = None):
        self.bible = bible or VisualBible()

    def create_brief_from_scenes(
        self,
        project_id: str,
        title: str,
        scenes: List[Dict[str, Any]],
        aspect_ratio: str = "16:9",
        channel_name: str = "TechXKenil",
        format_override: Optional[str] = None
    ) -> StoryBrief:
        """Constructs a StoryBrief automatically from scene metadata."""
        total_dur = sum(s.get("duration", 4.0) for s in scenes)
        is_short = aspect_ratio == "9:16" or total_dur <= 35.0
        fmt = format_override or ("short_form_micro_story" if is_short else "technology_explainer")
        
        return StoryBrief(
            project_id=project_id,
            title=title,
            format=fmt,
            target_platforms=["youtube_shorts"] if is_short else ["youtube"],
            aspect_ratio=aspect_ratio,
            duration_target_seconds=total_dur,
            channel_name=channel_name
        )

    def segment_script_into_beats(self, scenes: List[Dict[str, Any]]) -> List[StoryBeat]:
        """Analyzes scene narration and extracts discrete narrative story beats."""
        beats: List[StoryBeat] = []
        for idx, s in enumerate(scenes):
            sid = s.get("id") or s.get("name") or f"scene_{idx:02d}"
            text = s.get("narration") or s.get("text") or ""
            if not text and "beats" in s and isinstance(s["beats"], list):
                text = " ".join([b[0] for b in s["beats"] if isinstance(b, (list, tuple)) and len(b) > 0 and isinstance(b[0], str)])
            section = (s.get("section") or s.get("kind") or "EXPLANATION").upper()
            title = s.get("title") or s.get("heading") or s.get("name") or f"Beat {idx+1}"
            
            # Infer beat type from section or index
            if idx == 0 or "HOOK" in section or "INTRO" in section:
                b_type = "hook"
            elif idx == len(scenes) - 1 or "VERDICT" in section or "OUTRO" in section:
                b_type = "recap"
            elif "PROBLEM" in section or "BOTTLENECK" in section or "LIMIT" in section:
                b_type = "problem"
            elif "HACK" in section or "SECRET" in section or "SOLUTION" in section:
                b_type = "reveal"
            elif "PROOF" in section or "EVIDENCE" in section or "SPEED" in section:
                b_type = "evidence"
            else:
                b_type = "mechanism"

            beats.append(StoryBeat(
                beat_id=f"beat_{idx:02d}",
                order=idx,
                text=text,
                beat_type=b_type,
                viewer_question=f"What happens in {title}?",
                takeaway=title,
                visual_concept=s.get("visual_type", "diagram"),
                emotional_intent="clarity"
            ))
        return beats

    def plan_scenes(
        self,
        brief: StoryBrief,
        beats: List[StoryBeat],
        raw_scenes: List[Dict[str, Any]]
    ) -> List[ScenePlan]:
        """
        Transforms beats into fully directed ScenePlan objects with camera shots,
        layers, and audio event hooks.
        """
        scene_plans: List[ScenePlan] = []
        current_t = 0.0

        for idx, (b, raw) in enumerate(zip(beats, raw_scenes)):
            sid = raw.get("id") or raw.get("name") or f"scene_{idx:02d}"
            dur = float(raw.get("duration", 4.0))
            vtype = raw.get("visual_type") or raw.get("kind", "diagram")
            title = raw.get("title") or raw.get("heading") or raw.get("name") or f"Scene {idx+1}"

            # Map visual_type to standard scene archetype
            archetype = "system_overview"
            if vtype in ["hook_stopwatch", "cold_open"]:
                archetype = "cold_open_result"
            elif vtype in ["token_fracture", "flow"]:
                archetype = "flow_pipeline"
            elif vtype in ["prefill_matrix", "parallel"]:
                archetype = "step_build"
            elif vtype in ["kv_cache_split", "split"]:
                archetype = "comparison_board"
            elif vtype in ["silicon_memory_stream", "bottleneck"]:
                archetype = "data_proof"
            elif vtype in ["speculative_race", "race"]:
                archetype = "cause_effect"
            elif vtype in ["outro_conversion", "verdict"]:
                archetype = "recap_tableau"
            elif vtype in ["code", "terminal"]:
                archetype = "terminal" if vtype == "terminal" else "code_editor"

            # Create default shots
            shots = [
                ShotPlan(
                    shot_id=f"{sid}_shot_01",
                    shot_type="wide_to_medium" if idx > 0 else "wide",
                    camera_movement="push",
                    intensity=self.bible.default_camera_push,
                    duration_s=dur
                )
            ]

            plan = ScenePlan(
                scene_id=sid,
                beat_ids=[b.beat_id],
                title=title,
                archetype=archetype,
                purpose=raw.get("section") or raw.get("kind", "Explanation"),
                viewer_takeaway=b.takeaway,
                start_time=current_t,
                duration=dur,
                environment_type="branded_abstract",
                visual_treatment="motion_graphics_explainer",
                shots=shots,
                layers=[
                    {"layer_id": "background", "asset_id": "bg_obsidian_atmospheric", "z": 0},
                    {"layer_id": "content", "asset_id": f"{sid}_content", "z": 10},
                    {"layer_id": "telemetry", "asset_id": f"{sid}_telemetry", "z": 20}
                ],
                transition_out={"type": "direct_cut" if idx < len(beats)-1 else "fade_black"}
            )
            scene_plans.append(plan)
            current_t += dur

        return scene_plans
