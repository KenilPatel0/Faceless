#!/usr/bin/env python3
"""
animation_registry.py — Faceless Animation Intelligence Registry.
Declarative metadata-driven catalog of validated motion graphics techniques,
parameter schemas, audio synchronization triggers, performance costs, and fallbacks.

Implements Part II and Part V (Section 32) of the Animation Intelligence Implementation Spec.
"""

import os
import sys
import json
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Union, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

@dataclass
class ParameterSchema:
    name: str
    type: str  # "number", "string", "boolean", "color", "choice"
    default: Any
    min: Optional[float] = None
    max: Optional[float] = None
    choices: Optional[List[Any]] = None
    description: str = ""

@dataclass
class AnimationDefinition:
    id: str
    family: str  # typography, camera, object, shape, data, diagram, ui, editorial, transition, effects
    name: str
    description: str
    intent_tags: List[str]
    content_signals: List[str]
    complexity: str  # low, medium, high
    default_intensity: int  # 0 to 4
    duration_seconds: Dict[str, float]  # min, default, max
    supports: List[str]  # scale, opacity, position, path, mask, easing
    parameters: Dict[str, Dict[str, Any]]
    requires_assets: bool = False
    audio_sync: List[str] = field(default_factory=list)  # word_timestamp, sfx_transient, speech_pause, beat
    fallback: Optional[str] = None
    renderer: str = ""
    qa_tags: List[str] = field(default_factory=list)

class AnimationRegistry:
    """Singleton registry holding all registered animations."""
    def __init__(self):
        self._entries: Dict[str, AnimationDefinition] = {}
        self._aliases: Dict[str, str] = {}
        self._register_core_mvp_pack()
        self._register_spec_2026_pack()

    def register(self, definition: AnimationDefinition, aliases: Optional[List[str]] = None):
        """Registers a new animation definition."""
        self._entries[definition.id] = definition
        if aliases:
            for al in aliases:
                self._aliases[al] = definition.id

    def get(self, animation_id: str) -> Optional[AnimationDefinition]:
        """Looks up an animation definition by ID or alias."""
        resolved = self._aliases.get(animation_id, animation_id)
        return self._entries.get(resolved)

    def contains(self, animation_id: str) -> bool:
        resolved = self._aliases.get(animation_id, animation_id)
        return resolved in self._entries

    def query(
        self,
        family: Optional[str] = None,
        intent: Optional[str] = None,
        signal: Optional[str] = None,
        max_complexity: Optional[str] = None,
        max_intensity: Optional[int] = None,
        requires_assets: Optional[bool] = None
    ) -> List[AnimationDefinition]:
        """Discovers animations matching filters."""
        complexity_ranks = {"low": 1, "medium": 2, "high": 3}
        max_c_rank = complexity_ranks.get(max_complexity, 3) if max_complexity else 3

        results = []
        for defn in self._entries.values():
            if family and defn.family != family:
                continue
            if intent and intent not in defn.intent_tags:
                continue
            if signal and signal not in defn.content_signals:
                continue
            if complexity_ranks.get(defn.complexity, 1) > max_c_rank:
                continue
            if max_intensity is not None and defn.default_intensity > max_intensity:
                continue
            if requires_assets is not None and defn.requires_assets != requires_assets:
                continue
            results.append(defn)
        return results

    def validate_parameters(self, animation_id: str, params: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validates parameters against definition schema."""
        defn = self.get(animation_id)
        if not defn:
            return False, [f"Unknown animation ID: {animation_id}"]

        errors = []
        for p_name, p_val in params.items():
            if p_name not in defn.parameters:
                errors.append(f"Unknown parameter '{p_name}' for animation '{animation_id}'")
                continue
            schema = defn.parameters[p_name]
            p_type = schema.get("type")
            if p_type == "number":
                if not isinstance(p_val, (int, float)):
                    errors.append(f"Parameter '{p_name}' must be a number, got {type(p_val).__name__}")
                else:
                    p_min = schema.get("min")
                    p_max = schema.get("max")
                    if p_min is not None and p_val < p_min:
                        errors.append(f"Parameter '{p_name}' ({p_val}) below minimum {p_min}")
                    if p_max is not None and p_val > p_max:
                        errors.append(f"Parameter '{p_name}' ({p_val}) above maximum {p_max}")
            elif p_type == "choice":
                choices = schema.get("choices", [])
                if p_val not in choices:
                    errors.append(f"Parameter '{p_name}' value '{p_val}' not in allowed choices: {choices}")

        return (len(errors) == 0), errors

    def get_fallback(self, animation_id: str) -> Optional[AnimationDefinition]:
        """Returns the fallback definition if configured."""
        defn = self.get(animation_id)
        if defn and defn.fallback:
            return self.get(defn.fallback)
        return None

    def export_catalog(self) -> Dict[str, Any]:
        """Serializes catalog for API or inspection."""
        return {k: asdict(v) for k, v in self._entries.items()}

    def _register_core_mvp_pack(self):
        """Populates the 28 core MVP techniques from Section 42 of the specification."""
        
        # 1. Typography Family
        self.register(AnimationDefinition(
            id="type.word_pop",
            family="typography",
            name="Word Pop",
            description="Word enters with a spring scale bounce and opacity reveal, tied to speech timing.",
            intent_tags=["emphasis", "hook", "key_phrase"],
            content_signals=["important_phrase", "contrast", "punch"],
            complexity="low",
            default_intensity=2,
            duration_seconds={"min": 0.12, "default": 0.22, "max": 0.38},
            supports=["scale", "opacity", "color"],
            parameters={
                "from_scale": {"type": "number", "default": 0.82, "min": 0.5, "max": 1.0},
                "overshoot": {"type": "number", "default": 0.06, "min": 0.0, "max": 0.15},
                "color": {"type": "color", "default": "brand.accent"}
            },
            requires_assets=False,
            audio_sync=["word_timestamp", "sfx_transient"],
            fallback="type.phrase_reveal",
            renderer="render_core.render_word_pop",
            qa_tags=["caption_readability", "safe_area"]
        ))

        self.register(AnimationDefinition(
            id="type.karaoke_highlight",
            family="typography",
            name="Karaoke Highlight",
            description="Active spoken word illuminates in accent yellow/cyan with a subtle scale bounce.",
            intent_tags=["caption", "speech_follow", "retention"],
            content_signals=["narration", "continuous_speech"],
            complexity="low",
            default_intensity=2,
            duration_seconds={"min": 0.10, "default": 0.25, "max": 0.80},
            supports=["color", "scale"],
            parameters={
                "active_scale": {"type": "number", "default": 1.06, "min": 1.0, "max": 1.20},
                "active_color": {"type": "color", "default": [255, 205, 70]}
            },
            requires_assets=False,
            audio_sync=["word_timestamp"],
            fallback="type.phrase_reveal",
            renderer="render_core.render_karaoke_shorts",
            qa_tags=["caption_readability", "safe_area"]
        ))

        self.register(AnimationDefinition(
            id="type.phrase_reveal",
            family="typography",
            name="Phrase Reveal",
            description="Complete semantic clause or subtitle chunk appears smoothly with opacity/fade.",
            intent_tags=["caption", "clarity", "educational"],
            content_signals=["definition", "context", "long_sentence"],
            complexity="low",
            default_intensity=1,
            duration_seconds={"min": 0.20, "default": 0.35, "max": 0.60},
            supports=["opacity", "position"],
            parameters={"fade_duration": {"type": "number", "default": 0.20, "min": 0.05, "max": 0.50}},
            requires_assets=False,
            audio_sync=["speech_pause"],
            fallback=None,
            renderer="render_core.render_subtitles",
            qa_tags=["safe_area"]
        ))

        self.register(AnimationDefinition(
            id="type.typewriter",
            family="typography",
            name="Typewriter Character Reveal",
            description="Characters appear sequentially with humanized rhythmic jitter and cursor blink.",
            intent_tags=["code", "terminal", "suspense"],
            content_signals=["command", "code_snippet", "raw_text"],
            complexity="low",
            default_intensity=2,
            duration_seconds={"min": 0.30, "default": 0.80, "max": 2.50},
            supports=["typed_progress", "cursor"],
            parameters={
                "chars_per_second": {"type": "number", "default": 18.0, "min": 5.0, "max": 40.0},
                "cursor_blink": {"type": "boolean", "default": True}
            },
            requires_assets=False,
            audio_sync=["sfx_transient"],
            fallback="type.phrase_reveal",
            renderer="humanize.typed",
            qa_tags=["text_bounds"]
        ))

        self.register(AnimationDefinition(
            id="type.scale_punch",
            family="typography",
            name="Scale Punch Headline",
            description="High-impact scale punch from 1.25x down to 1.0x with firm settle.",
            intent_tags=["hook", "impact", "headline"],
            content_signals=["contrarian_claim", "major_fact"],
            complexity="low",
            default_intensity=3,
            duration_seconds={"min": 0.25, "default": 0.40, "max": 0.70},
            supports=["scale", "easing"],
            parameters={"punch_scale": {"type": "number", "default": 1.25, "min": 1.05, "max": 1.50}},
            requires_assets=False,
            audio_sync=["sfx_transient"],
            fallback="type.word_pop",
            renderer="motion.pulse",
            qa_tags=["safe_area"]
        ))

        self.register(AnimationDefinition(
            id="type.lower_third",
            family="typography",
            name="Lower-Third Pill & Nameplate",
            description="Minimal glassmorphic pill slides in with title, category badge, or attribution.",
            intent_tags=["attribution", "citation", "section_label"],
            content_signals=["source_credit", "speaker_name", "chapter"],
            complexity="low",
            default_intensity=1,
            duration_seconds={"min": 0.30, "default": 0.45, "max": 0.80},
            supports=["slide", "opacity"],
            parameters={"slide_direction": {"type": "choice", "default": "left", "choices": ["left", "bottom"]}},
            requires_assets=False,
            audio_sync=["speech_pause"],
            fallback="type.phrase_reveal",
            renderer="render_core.draw_pill",
            qa_tags=["safe_area"]
        ))

        # 2. Camera Family
        self.register(AnimationDefinition(
            id="camera.push_in",
            family="camera",
            name="Slow Camera Push-In",
            description="Zero-resize overscan camera pushes inward smoothly by 3.5% with organic drift.",
            intent_tags=["anti_freeze", "immersion", "focus"],
            content_signals=["continuous_scene", "emphasis", "real_asset"],
            complexity="low",
            default_intensity=1,
            duration_seconds={"min": 1.5, "default": 4.0, "max": 15.0},
            supports=["zoom", "drift"],
            parameters={
                "amount": {"type": "number", "default": 0.035, "min": 0.01, "max": 0.08},
                "drift_amp": {"type": "number", "default": 6.0, "min": 0.0, "max": 12.0}
            },
            requires_assets=False,
            audio_sync=[],
            fallback=None,
            renderer="render_core.OverscanCanvas.slice_frame",
            qa_tags=["zero_static_holds", "safe_margins"]
        ))

        self.register(AnimationDefinition(
            id="camera.pull_out",
            family="camera",
            name="Camera Pull-Out Context Reveal",
            description="Widens framing from detail crop to full context stage.",
            intent_tags=["context", "big_picture", "resolution"],
            content_signals=["architecture", "summary", "zoom_out"],
            complexity="low",
            default_intensity=1,
            duration_seconds={"min": 1.0, "default": 2.5, "max": 6.0},
            supports=["zoom"],
            parameters={"start_zoom": {"type": "number", "default": 1.15, "min": 1.05, "max": 1.30}},
            requires_assets=False,
            audio_sync=[],
            fallback="camera.push_in",
            renderer="render_core.OverscanCanvas.slice_frame",
            qa_tags=["safe_margins"]
        ))

        self.register(AnimationDefinition(
            id="camera.punch",
            family="camera",
            name="Camera Punch-In / Reset",
            description="Instant or rapid 4-frame punch-in cut renewing viewer visual focus on key phrase.",
            intent_tags=["editorial_punch", "beat_accent"],
            content_signals=["sudden_turn", "key_evidence"],
            complexity="low",
            default_intensity=3,
            duration_seconds={"min": 0.15, "default": 0.25, "max": 0.40},
            supports=["scale"],
            parameters={"punch_amount": {"type": "number", "default": 1.08, "min": 1.03, "max": 1.20}},
            requires_assets=False,
            audio_sync=["sfx_transient"],
            fallback="camera.push_in",
            renderer="motion.pulse",
            qa_tags=["safe_margins"]
        ))

        # 3. Object & Cards Family
        self.register(AnimationDefinition(
            id="object.pop_overshoot",
            family="object",
            name="Spring Pop Entrance with Overshoot",
            description="Card or element pops in from 0.7x to 1.04x overshoot before settling in 0.5s.",
            intent_tags=["entrance", "ui_card", "tactile"],
            content_signals=["card_reveal", "metric_pill", "dialog"],
            complexity="low",
            default_intensity=2,
            duration_seconds={"min": 0.30, "default": 0.50, "max": 0.80},
            supports=["scale", "spring", "opacity"],
            parameters={
                "frequency": {"type": "number", "default": 2.2, "min": 1.0, "max": 4.0},
                "damping": {"type": "number", "default": 0.72, "min": 0.4, "max": 1.0}
            },
            requires_assets=False,
            audio_sync=["sfx_transient"],
            fallback="object.slide",
            renderer="render_core.spring",
            qa_tags=["no_layout_collision"]
        ))

        self.register(AnimationDefinition(
            id="object.slide",
            family="object",
            name="Smooth Directional Slide Entrance",
            description="Card glides in along X or Y axis with cubic ease-out deceleration.",
            intent_tags=["entrance", "panels", "clean"],
            content_signals=["list_item", "spec_item"],
            complexity="low",
            default_intensity=2,
            duration_seconds={"min": 0.25, "default": 0.45, "max": 0.75},
            supports=["position", "opacity"],
            parameters={"direction": {"type": "choice", "default": "bottom", "choices": ["bottom", "left", "right", "top"]}},
            requires_assets=False,
            audio_sync=["sfx_transient"],
            fallback=None,
            renderer="render_core.ease_out_cubic",
            qa_tags=["safe_margins"]
        ))

        self.register(AnimationDefinition(
            id="object.stagger",
            family="object",
            name="Staggered List Group Reveal",
            description="Children elements enter sequentially with 80-120ms delays and deterministic jitter.",
            intent_tags=["list", "steps", "multi_point"],
            content_signals=["ordered_steps", "comparison_items", "feature_grid"],
            complexity="medium",
            default_intensity=2,
            duration_seconds={"min": 0.60, "default": 1.20, "max": 3.00},
            supports=["stagger_delay", "spring"],
            parameters={"delay_per_item": {"type": "number", "default": 0.10, "min": 0.05, "max": 0.30}},
            requires_assets=False,
            audio_sync=["sfx_transient"],
            fallback="object.slide",
            renderer="humanize.stagger",
            qa_tags=["no_layout_collision"]
        ))

        self.register(AnimationDefinition(
            id="object.motion_path",
            family="object",
            name="Bezier Motion Path Travel",
            description="Object or cursor glides along a smooth quadratic Bezier curve path.",
            intent_tags=["travel", "cursor", "flow"],
            content_signals=["cursor_click", "data_packet", "signal_flow"],
            complexity="medium",
            default_intensity=2,
            duration_seconds={"min": 0.50, "default": 1.20, "max": 2.50},
            supports=["bezier", "position"],
            parameters={"bend": {"type": "number", "default": 0.18, "min": -0.5, "max": 0.5}},
            requires_assets=False,
            audio_sync=[],
            fallback="object.slide",
            renderer="render_core.bezier_point",
            qa_tags=["safe_margins"]
        ))

        # 4. Shape & Line Family
        self.register(AnimationDefinition(
            id="shape.path_draw",
            family="shape",
            name="Stroke / Path Trim Draw",
            description="Line or arrow draws from start to end with stable organic hand wobble.",
            intent_tags=["flow", "connection", "underline"],
            content_signals=["arrow", "divider", "flow_connection"],
            complexity="medium",
            default_intensity=2,
            duration_seconds={"min": 0.30, "default": 0.60, "max": 1.20},
            supports=["trim_start", "trim_end", "wobble"],
            parameters={"wobble": {"type": "number", "default": 2.5, "min": 0.0, "max": 8.0}},
            requires_assets=False,
            audio_sync=["sfx_transient"],
            fallback=None,
            renderer="humanize.hand_line",
            qa_tags=["visual_continuity"]
        ))

        self.register(AnimationDefinition(
            id="shape.wipe",
            family="shape",
            name="Linear / Iris Shape Wipe",
            description="Reveals layer underneath via expanding geometric boundary.",
            intent_tags=["reveal", "mask", "transition"],
            content_signals=["state_change", "before_after"],
            complexity="medium",
            default_intensity=2,
            duration_seconds={"min": 0.30, "default": 0.50, "max": 0.80},
            supports=["wipe_progress", "direction"],
            parameters={"direction": {"type": "choice", "default": "right", "choices": ["right", "circle", "down"]}},
            requires_assets=False,
            audio_sync=["sfx_transient"],
            fallback="transition.cut",
            renderer="motion.transition",
            qa_tags=["visual_continuity"]
        ))

        # 5. Data & Numbers Family
        self.register(AnimationDefinition(
            id="data.counter",
            family="data",
            name="Numeric Count-Up with Quartic Easing",
            description="Number smoothly counts up from 0 to target metric with humanized ease-out.",
            intent_tags=["metric", "statistic", "proof"],
            content_signals=["measured_number", "benchmark_time", "speed_multiplier"],
            complexity="low",
            default_intensity=2,
            duration_seconds={"min": 0.40, "default": 0.90, "max": 2.00},
            supports=["count_progress", "format"],
            parameters={
                "start_val": {"type": "number", "default": 0},
                "end_val": {"type": "number", "default": 100},
                "format_str": {"type": "string", "default": "{:,.0f}"}
            },
            requires_assets=False,
            audio_sync=["sfx_transient"],
            fallback="type.phrase_reveal",
            renderer="motion.count_up",
            qa_tags=["data_accuracy"]
        ))

        self.register(AnimationDefinition(
            id="data.bar_grow",
            family="data",
            name="Data Bar Horizontal / Vertical Growth",
            description="Benchmark or data bar expands smoothly to represent quantified value.",
            intent_tags=["benchmark", "comparison", "data"],
            content_signals=["benchmark_comparison", "percentage", "growth"],
            complexity="medium",
            default_intensity=2,
            duration_seconds={"min": 0.50, "default": 1.00, "max": 1.80},
            supports=["progress", "color"],
            parameters={"max_width": {"type": "number", "default": 600, "min": 100, "max": 1800}},
            requires_assets=False,
            audio_sync=["sfx_transient"],
            fallback="data.counter",
            renderer="render_core.OverscanCanvas.draw_card",
            qa_tags=["data_accuracy"]
        ))

        # 6. Real UI & Code Family
        self.register(AnimationDefinition(
            id="ui.cursor_click",
            family="ui",
            name="Cursor Move, Click & Expanding Ripple",
            description="Realistic cursor glides to button, triggers click scale pulse and expanding ring.",
            intent_tags=["conversion", "action", "subscribe"],
            content_signals=["subscribe_callout", "ui_interaction", "button_press"],
            complexity="medium",
            default_intensity=3,
            duration_seconds={"min": 1.20, "default": 2.50, "max": 4.00},
            supports=["cursor_pos", "ripple_radius", "button_state"],
            parameters={"click_time": {"type": "number", "default": 2.5, "min": 0.5, "max": 5.0}},
            requires_assets=False,
            audio_sync=["sfx_transient"],
            fallback=None,
            renderer="render_core.render_outro_card",
            qa_tags=["safe_margins"]
        ))

        self.register(AnimationDefinition(
            id="ui.code_line_focus",
            family="ui",
            name="Authentic VS Code Window & Line Focus",
            description="Displays genuine dark-mode VS Code window with Tokyo Night syntax highlighting and line focus.",
            intent_tags=["code", "architecture", "senior_dev"],
            content_signals=["code_review", "diff_audit", "syntax_highlight"],
            complexity="medium",
            default_intensity=2,
            duration_seconds={"min": 2.00, "default": 5.00, "max": 15.00},
            supports=["code_snippet", "highlight_lines", "filename"],
            parameters={"line_numbers": {"type": "boolean", "default": True}},
            requires_assets=True,
            audio_sync=[],
            fallback="type.typewriter",
            renderer="capture_code.render_code_window",
            qa_tags=["zero_synthetic_mockups", "code_fidelity"]
        ))

        self.register(AnimationDefinition(
            id="ui.terminal_exec",
            family="ui",
            name="Authentic Terminal Window Execution",
            description="Displays genuine dark-mode Terminal window with prompt, command, and passing test results.",
            intent_tags=["terminal", "test_runner", "pytest"],
            content_signals=["pytest_pass", "cli_command", "git_diff"],
            complexity="medium",
            default_intensity=2,
            duration_seconds={"min": 2.00, "default": 4.50, "max": 12.00},
            supports=["command", "output_lines"],
            parameters={"badge": {"type": "string", "default": "BASH"}},
            requires_assets=True,
            audio_sync=["sfx_transient"],
            fallback=None,
            renderer="capture_code.render_terminal_window",
            qa_tags=["zero_synthetic_mockups"]
        ))

        # 7. Editorial & Transitions Family
        self.register(AnimationDefinition(
            id="edit.split_screen",
            family="editorial",
            name="Split-Screen Side-by-Side Comparison",
            description="Compares rejected vs verified approaches in synchronized dual panels.",
            intent_tags=["comparison", "typist_vs_architect", "myth_vs_fact"],
            content_signals=["side_by_side", "before_after", "contrast"],
            complexity="medium",
            default_intensity=2,
            duration_seconds={"min": 2.50, "default": 6.00, "max": 20.00},
            supports=["left_asset", "right_asset"],
            parameters={"split_ratio": {"type": "number", "default": 0.5, "min": 0.2, "max": 0.8}},
            requires_assets=False,
            audio_sync=[],
            fallback=None,
            renderer="capture_code.render_split_code_window",
            qa_tags=["no_layout_collision"]
        ))

        self.register(AnimationDefinition(
            id="transition.cut",
            family="transition",
            name="Clean Editorial Hard Cut",
            description="Zero-duration crisp cut to maintain natural visual pace across scene changes.",
            intent_tags=["cut", "pace", "default"],
            content_signals=["scene_change", "new_topic"],
            complexity="low",
            default_intensity=0,
            duration_seconds={"min": 0.0, "default": 0.0, "max": 0.0},
            supports=[],
            parameters={},
            requires_assets=False,
            audio_sync=[],
            fallback=None,
            renderer="direct_frame_switch",
            qa_tags=["visual_continuity"]
        ))

        self.register(AnimationDefinition(
            id="transition.dissolve",
            family="transition",
            name="Cross Dissolve Continuity Fade",
            description="Smooth 8-12 frame cross dissolve between two continuous visual scenes.",
            intent_tags=["continuity", "calm", "time_passage"],
            content_signals=["chapter_change", "mood_shift"],
            complexity="low",
            default_intensity=1,
            duration_seconds={"min": 0.20, "default": 0.35, "max": 0.60},
            supports=["cross_fade"],
            parameters={"duration": {"type": "number", "default": 0.35, "min": 0.15, "max": 0.80}},
            requires_assets=False,
            audio_sync=["sfx_transient"],
            fallback="transition.cut",
            renderer="motion.composite",
            qa_tags=["visual_continuity"]
        ))

        self.register(AnimationDefinition(
            id="transition.directional_wipe",
            family="transition",
            name="Horizontal Directional Push / Wipe",
            description="Pushes old scene off-canvas with whoosh sound effect on major chapter boundary.",
            intent_tags=["chapter_wipe", "energy"],
            content_signals=["section_boundary", "blueprint_step"],
            complexity="medium",
            default_intensity=2,
            duration_seconds={"min": 0.25, "default": 0.40, "max": 0.65},
            supports=["push_direction"],
            parameters={"axis": {"type": "choice", "default": "x", "choices": ["x", "y"]}},
            requires_assets=False,
            audio_sync=["sfx_transient"],
            fallback="transition.cut",
            renderer="motion.transition",
            qa_tags=["visual_continuity"]
        ))

    def _register_spec_2026_pack(self):
        """Loads and registers the 2026 TechXKenil Animation Library specification taxonomy (T1-T8, E1-E11, C1-C8, S1-S5, F1-F5)."""
        spec_path = os.path.join(REPO_ROOT, "agents", "skills", "animation-library", "registry.json")
        if not os.path.exists(spec_path):
            return

        try:
            with open(spec_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            catalog = data.get("catalog", {})
        except Exception:
            return

        spec_to_internal_aliases = {
            "T1": ["type.karaoke_highlight"],
            "T2": ["type.phrase_reveal"],
            "T3": ["type.scale_punch"],
            "T4": ["type.word_pop"],
            "T5": ["type.typewriter"],
            "T6": ["data.stat_counter"],
            "T8": ["type.lower_third"],
            "E2": ["diagram.step_reveal"],
            "E3": ["edit.split_screen"],
            "E4": ["card.staggered_column"],
            "E5": ["data.bar_reveal"],
            "E6": ["ui.code_line_focus"],
            "C1": ["camera.drift"],
            "C2": ["camera.punch"],
            "C3": ["transition.directional_wipe"],
            "cta": ["brand.outro_cta", "outro_card"]
        }

        for item_id, item in catalog.items():
            cost = item.get("cost", "low")
            complexity = "high" if cost == "heavy" else ("medium" if cost == "medium" else "low")
            params = item.get("params", {})
            schema_params = {}
            if isinstance(params, dict):
                for p_name, p_val in params.items():
                    if isinstance(p_val, dict):
                        schema_params[p_name] = p_val
                    else:
                        schema_params[p_name] = {"default": p_val}

            defn = AnimationDefinition(
                id=item_id,
                family=item.get("family", "explainer"),
                name=item.get("name", item_id),
                description=item.get("timing_spec", "") or item.get("reason", ""),
                intent_tags=item.get("beat_types", []),
                content_signals=item.get("formats", []),
                complexity=complexity,
                default_intensity=2,
                duration_seconds={
                    "min": item.get("min_duration_s", 0.5),
                    "default": item.get("default_duration_s", 2.0),
                    "max": item.get("max_duration_s", 10.0)
                },
                supports=["scale", "opacity", "position"],
                parameters=schema_params,
                requires_assets=item.get("needs_assets", False),
                audio_sync=["word_timestamp"] if item_id == "T1" else ["sfx_transient"],
                fallback=None,
                renderer=item.get("renderer_binding", ""),
                qa_tags=[item.get("fit", "core")]
            )
            aliases = spec_to_internal_aliases.get(item_id, [])
            self.register(defn, aliases=aliases)

            # Also ensure internal IDs alias back to spec IDs
            for alias in aliases:
                self._aliases[alias] = item_id

        # Also register 'outro_card' alias to cta if not present
        self._aliases["outro_card"] = "cta"

# Global registry instance
REGISTRY = AnimationRegistry()

if __name__ == "__main__":
    print(f"📦 Animation Registry initialized with {len(REGISTRY._entries)} core techniques:")
    for k, v in REGISTRY._entries.items():
        print(f"  [{v.complexity.upper():6}] {v.id:26} : {v.name}")
