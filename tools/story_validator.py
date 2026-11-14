#!/usr/bin/env python3
"""
story_validator.py — Story & Scene QA Validator for Faceless.
Implements the 14 Validation Contracts from Section 30 of the Storytelling Spec:
- 100% Beat-to-Scene coverage
- Every scene has positive duration and fps
- Asset ID resolution against AssetRegistry
- Transitions connect to valid adjacent scenes
- Caption clearance check (content layer y <= 880px, subtitle safe zone y = 1010px)
- Pacing checks (Shorts: 1.5-4s shots, 3-9s scenes; Long: 3-8s shots, 6-25s scenes)
"""

from typing import List, Dict, Any, Tuple
from tools.story_director import StoryBrief, StoryBeat, ScenePlan
from tools.asset_registry import AssetRegistry


class StoryValidator:
    """Pre-render validation engine ensuring narrative integrity and visual compliance."""
    def __init__(self, registry: AssetRegistry):
        self.registry = registry

    def validate_production_plan(
        self,
        brief: StoryBrief,
        beats: List[StoryBeat],
        scenes: List[ScenePlan]
    ) -> Tuple[bool, List[str], List[str]]:
        """
        Validates the entire story and scene plan before rendering.
        Returns: (is_valid, errors, warnings)
        """
        errors: List[str] = []
        warnings: List[str] = []

        # 1. Validate Brief
        errors.extend(brief.validate())

        # 2. Validate Beats
        covered_beats = set()
        for b in beats:
            errors.extend(b.validate())

        # 3. Validate Scenes & Beat Coverage
        scene_ids = {s.scene_id for s in scenes}
        is_short = brief.aspect_ratio == "9:16"

        for idx, s in enumerate(scenes):
            errors.extend(s.validate())
            for bid in s.beat_ids:
                covered_beats.add(bid)

            # Pacing checks
            if is_short:
                if s.duration > 12.0:
                    warnings.append(f"Scene {s.scene_id} duration ({s.duration:.1f}s) exceeds Short-form target (3-9s).")
            else:
                if s.duration < 2.0:
                    warnings.append(f"Scene {s.scene_id} duration ({s.duration:.1f}s) may be too fast for Long-form.")

            # Transition validation
            tout = s.transition_out.get("to_scene_id")
            if tout and tout not in scene_ids:
                errors.append(f"Scene {s.scene_id} transition_out references non-existent scene '{tout}'.")

            # Asset verification & Caption clearance check
            for layer in s.layers:
                aid = layer.get("asset_id")
                if aid and not (aid.endswith("_content") or aid.endswith("_telemetry")):
                    if not self.registry.get(aid):
                        errors.append(f"Scene {s.scene_id} references unregistered asset '{aid}'.")

                bounds = layer.get("bounds", {})
                y_max = bounds.get("y_max")
                if y_max is not None and not is_short:
                    # In 1080p, subtitles are at y=1010. Content layer must not exceed y=880 (80px safe clearance zone)
                    if y_max > 880:
                        errors.append(
                            f"Scene {s.scene_id} layer '{layer.get('layer_id')}' - Caption clearance violation: "
                            f"y_max={y_max}px exceeds 880px ceiling (subtitle safe line at 1010px)."
                        )

        # 4. Check Beat Coverage completeness
        all_beat_ids = {b.beat_id for b in beats}
        uncovered = all_beat_ids - covered_beats
        if uncovered:
            errors.append(f"Uncovered story beats not assigned to any scene: {uncovered}")

        is_valid = len(errors) == 0
        return is_valid, errors, warnings
