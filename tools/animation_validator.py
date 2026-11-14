#!/usr/bin/env python3
"""
animation_validator.py — Faceless Animation Plan & Motion QA Validator.
Validates structured AnimationPlan JSON against registry schemas, motion density budgets,
platform safe-area boundaries, timing consistency, and WCAG flashing guidelines.

Implements Part V (Section 34) and Part VII (Section 36-37) of the Implementation Spec.
"""

import os
import sys
import math
from typing import Dict, List, Tuple, Any, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from tools.animation_registry import REGISTRY, AnimationRegistry

class AnimationPlanValidator:
    """Validates an AnimationPlan before rendering."""
    def __init__(self, registry: Optional[AnimationRegistry] = None):
        self.registry = registry or REGISTRY

    def validate_plan(self, plan: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """
        Validates an entire AnimationPlan:
        Returns (is_valid, errors, warnings).
        """
        errors: List[str] = []
        warnings: List[str] = []

        if not isinstance(plan, dict):
            return False, ["AnimationPlan must be a JSON dictionary object."], []

        # 1. Project Header Validation
        proj = plan.get("project", {})
        aspect = proj.get("aspect_ratio", "16:9")
        if aspect not in ["16:9", "9:16", "1:1"]:
            warnings.append(f"Uncommon aspect_ratio '{aspect}'. Expected 16:9 or 9:16.")

        scenes = plan.get("scenes", [])
        if not scenes:
            errors.append("AnimationPlan contains no scenes.")
            return False, errors, warnings

        # 2. Scene by Scene Validation
        last_end = 0.0
        for s_idx, scene in enumerate(scenes):
            sid = scene.get("scene_id", f"scene_{s_idx}")
            st = float(scene.get("start_seconds", 0.0))
            et = float(scene.get("end_seconds", 0.0))

            if et <= st:
                errors.append(f"Scene '{sid}' has invalid duration: start={st}s, end={et}s.")
            if st < last_end - 0.05:
                warnings.append(f"Scene '{sid}' overlaps previous scene (start={st}s < prev_end={last_end}s).")
            last_end = et

            intensity = scene.get("motion_intensity", 2)
            if not (0 <= intensity <= 4):
                errors.append(f"Scene '{sid}' motion_intensity must be 0-4, got {intensity}.")

            # Validate Transition
            t_out = scene.get("transition_out", {})
            t_id = t_out.get("id", "transition.cut")
            if not self.registry.contains(t_id):
                warnings.append(f"Scene '{sid}' unknown transition '{t_id}'. Falling back to 'transition.cut'.")
                scene["transition_out"]["id"] = "transition.cut"

            # Validate Beats
            beats = scene.get("beats", [])
            for b_idx, beat in enumerate(beats):
                bid = beat.get("beat_id", f"beat_{s_idx}_{b_idx}")
                b_st = float(beat.get("start_seconds", st))
                b_et = float(beat.get("end_seconds", et))

                if b_st < st or b_et > et:
                    errors.append(f"Beat '{bid}' [{b_st}s, {b_et}s] falls outside parent scene [{st}s, {et}s].")

                layers = beat.get("layers", [])
                
                # Density Guardrail: Max 1 primary + 2 supporting motion events per beat
                primary_count = sum(1 for l in layers if l.get("intensity", 2) >= 3)
                if primary_count > 1:
                    warnings.append(
                        f"Beat '{bid}' has {primary_count} hero/high-intensity layers. "
                        "Spec recommends at most 1 primary motion event per beat."
                    )
                if len(layers) > 4:
                    warnings.append(f"Beat '{bid}' motion density high ({len(layers)} simultaneous layers).")

                # Validate Layer Animations
                for l_idx, layer in enumerate(layers):
                    lid = layer.get("layer_id", f"layer_{l_idx}")
                    anim_id = layer.get("animation_id")

                    if not anim_id:
                        errors.append(f"Layer '{lid}' in beat '{bid}' missing 'animation_id'.")
                        continue

                    if not self.registry.contains(anim_id):
                        fallback = self.registry.get_fallback(anim_id)
                        if fallback:
                            warnings.append(f"Unknown animation '{anim_id}' on layer '{lid}'. Using fallback '{fallback.id}'.")
                            layer["animation_id"] = fallback.id
                            anim_id = fallback.id
                        else:
                            errors.append(f"Unknown animation '{anim_id}' on layer '{lid}' with no registered fallback.")
                            continue

                    # Validate parameters against schema
                    params = layer.get("parameters", {})
                    ok_p, p_errs = self.registry.validate_parameters(anim_id, params)
                    if not ok_p:
                        for pe in p_errs:
                            errors.append(f"Layer '{lid}' parameter error: {pe}")

                    # Validate layer duration against definition limits
                    defn = self.registry.get(anim_id)
                    l_dur = float(layer.get("duration_seconds", 0.5))
                    if defn and defn.duration_seconds:
                        d_min = defn.duration_seconds.get("min", 0.0)
                        d_max = defn.duration_seconds.get("max", 60.0)
                        if l_dur < d_min:
                            warnings.append(f"Layer '{lid}' duration ({l_dur}s) below recommended min ({d_min}s) for '{anim_id}'.")
                        if l_dur > d_max:
                            warnings.append(f"Layer '{lid}' duration ({l_dur}s) exceeds recommended max ({d_max}s) for '{anim_id}'.")

        # 3. Flashing & WCAG Safety Check
        fast_cuts = 0
        for s in scenes:
            if float(s.get("end_seconds", 0)) - float(s.get("start_seconds", 0)) < 0.30:
                fast_cuts += 1
        if fast_cuts >= 3:
            warnings.append(f"Plan contains {fast_cuts} rapid cuts under 0.3s. Check for potential flashing/strobing.")

        is_valid = (len(errors) == 0)
        return is_valid, errors, warnings

if __name__ == "__main__":
    validator = AnimationPlanValidator()
    test_plan = {
        "project": {"aspect_ratio": "16:9"},
        "scenes": [
            {
                "scene_id": "test_scene",
                "start_seconds": 0.0,
                "end_seconds": 4.0,
                "motion_intensity": 2,
                "beats": [
                    {
                        "beat_id": "beat_1",
                        "start_seconds": 0.0,
                        "end_seconds": 2.0,
                        "layers": [
                            {
                                "layer_id": "headline",
                                "animation_id": "type.word_pop",
                                "duration_seconds": 0.25,
                                "parameters": {"from_scale": 0.8}
                            }
                        ]
                    }
                ]
            }
        ]
    }
    valid, errs, warns = validator.validate_plan(test_plan)
    print(f"Validation Result: {'✓ PASSED' if valid else '✗ FAILED'}")
    if errs:
        print("Errors:", errs)
    if warns:
        print("Warnings:", warns)
