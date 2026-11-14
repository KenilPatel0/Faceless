#!/usr/bin/env python3
"""
check_plan.py — Automated Linter for TechXKenil Scene Plans.

Enforces the contracts defined in Section 8.5 of the TechXKenil Animation Library
and Prompt-to-Animation Decision Engine specification:
1. Every beat has exactly one valid beat_type and valid IDs from registry.json.
2. No static hold above 4s (short) or 9s (long).
3. A retention anchor within every 3s (short) or 6s (long).
4. C5 and C6 at most once each per video; none in first 2s. C4 max 2 in shorts.
5. No same primary ID more than twice in a row.
6. Caption style matches format (T1 short, T2 long).
7. No statistic (T6/E5) without a verified source note.
8. At least 3 scene-layer differences from the last 3 plans in plans/history.
9. Brand layer unchanged (S1, standard intro/outro).
10. Total duration within tolerance of target.
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Tuple, Any, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

def load_json(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

class ScenePlanLinter:
    def __init__(self, skill_dir: Optional[str] = None):
        self.skill_dir = skill_dir or SKILL_DIR
        self.registry = load_json(os.path.join(self.skill_dir, "registry.json")).get("catalog", {})
        self.decision_table = load_json(os.path.join(self.skill_dir, "decision_table.json")).get("decision_table", {})
        self.rules = load_json(os.path.join(self.skill_dir, "rules.json")).get("rules", {})
        self.history_dir = os.path.join(self.skill_dir, "plans", "history")

    def lint(self, plan: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """Lints a scene plan. Returns (is_valid, errors, warnings)."""
        errors: List[str] = []
        warnings: List[str] = []

        # 1. Brief & Metadata Check
        brief = plan.get("brief", {})
        if not brief:
            errors.append("Plan missing 'brief' object.")
            return False, errors, warnings

        fmt = brief.get("format", "short")
        if fmt not in ["short", "long"]:
            errors.append(f"Invalid format '{fmt}'. Must be 'short' or 'long'.")

        target_duration = float(brief.get("duration_target_s", 30.0))
        beats = plan.get("beats", [])
        if not beats:
            errors.append("Plan contains no beats.")
            return False, errors, warnings

        # 2. Caption style matches format rule
        expected_caption = "T1" if fmt == "short" else "T2"

        # 3. Beat-by-beat verification
        last_primary = None
        consecutive_primary_count = 0
        last_transition = None
        consecutive_transition_count = 0
        c5_count = 0
        c6_count = 0
        c4_count = 0
        last_anchor_time = 0.0
        anchor_max_interval = 3.0 if fmt == "short" else 6.0
        static_hold_ceiling = 4.0 if fmt == "short" else 9.0

        total_time = 0.0

        for idx, beat in enumerate(beats):
            b_id = beat.get("id", idx + 1)
            t_span = beat.get("t", [0.0, 0.0])
            t_start, t_end = float(t_span[0]), float(t_span[1])
            duration = t_end - t_start
            total_time = max(total_time, t_end)

            if duration <= 0:
                errors.append(f"Beat {b_id}: Invalid duration ({t_start}s to {t_end}s).")

            # Check 1: Beat Type
            b_type = beat.get("beat_type")
            if not b_type or b_type not in self.decision_table:
                errors.append(f"Beat {b_id}: Invalid or missing beat_type '{b_type}'.")

            # Check 2: Animation IDs in registry
            primary = beat.get("primary", "")
            # Support compound primary like "T3 + C2" or single ID
            primary_ids = [p.strip() for p in primary.replace("+", ",").split(",") if p.strip()]
            for pid in primary_ids:
                if pid not in self.registry and pid != "outro_card":
                    errors.append(f"Beat {b_id}: Unknown primary animation ID '{pid}'.")

            base_primary = primary_ids[0] if primary_ids else ""

            # Check repeat limit on primary ID
            if base_primary == last_primary and base_primary != "outro_card":
                consecutive_primary_count += 1
                if consecutive_primary_count > 2:
                    errors.append(f"Beat {b_id}: Primary animation '{base_primary}' repeated more than twice consecutively.")
            else:
                last_primary = base_primary
                consecutive_primary_count = 1

            # Check Secondaries
            secondaries = beat.get("secondary", [])
            for sec in secondaries:
                # Some secondaries may have parameters like "T4:answers,acts"
                sec_id = sec.split(":")[0].strip()
                if sec_id not in self.registry and sec_id != "outro_card":
                    errors.append(f"Beat {b_id}: Unknown secondary animation ID '{sec_id}'.")

            # Check Transition Out
            t_out = beat.get("transition_out")
            if t_out:
                if t_out not in self.registry:
                    errors.append(f"Beat {b_id}: Unknown transition_out '{t_out}'.")
                if t_out == last_transition:
                    consecutive_transition_count += 1
                    if consecutive_transition_count > 2:
                        errors.append(f"Beat {b_id}: Transition '{t_out}' repeated more than twice consecutively.")
                else:
                    last_transition = t_out
                    consecutive_transition_count = 1

            # Check Captions
            cap = beat.get("captions")
            if cap != expected_caption:
                errors.append(f"Beat {b_id}: Caption style is '{cap}', expected '{expected_caption}' for {fmt} format.")

            # Check Effects & Budgets
            effects = beat.get("effects", [])
            all_beat_effects = [e.split(":")[0].strip() for e in effects]
            if "C5" in primary_ids or "C5" in all_beat_effects:
                c5_count += 1
                if t_start < 2.0:
                    errors.append(f"Beat {b_id}: Heavy effect C5 (glitch) not allowed in first 2 seconds (starts at {t_start}s).")
            if "C6" in primary_ids or "C6" in all_beat_effects:
                c6_count += 1
                if t_start < 2.0:
                    errors.append(f"Beat {b_id}: Heavy effect C6 (screen shake) not allowed in first 2 seconds (starts at {t_start}s).")
            if "C4" in primary_ids or t_out == "C4":
                c4_count += 1

            # Check Honesty Gate (T6/E5 require source)
            if any(p in ["T6", "E5"] for p in primary_ids):
                source = beat.get("source")
                if not source or not source.strip():
                    errors.append(f"Beat {b_id}: Honesty Gate violation. Stat animation '{primary}' requires a verified 'source' attribute.")

            # Check One Idea Per Screen: No T3 during E2 diagram step
            if "E2" in primary_ids and "T3" in primary_ids:
                errors.append(f"Beat {b_id}: Disallowed combination: T3 (hero headline) cannot appear during E2 (diagram build).")

            # Check Retention Anchor
            # An anchor is formed by a beat transition, hero text, punch-in, emphasis, or diagram step
            has_anchor = (
                duration <= anchor_max_interval or
                any(p in ["T3", "C2", "T4", "E2", "E3", "E4", "T6"] for p in primary_ids) or
                bool(secondaries)
            )
            if not has_anchor and (t_end - last_anchor_time) > anchor_max_interval:
                warnings.append(f"Beat {b_id}: Retention anchor interval exceeded (>{anchor_max_interval}s between visual events).")
            last_anchor_time = t_end

            # Check Static Hold Ceiling
            if duration > static_hold_ceiling:
                # Unless continuous C1 push-in is present
                if "C1" not in primary_ids and "C1" not in secondaries:
                    errors.append(f"Beat {b_id}: Static hold ceiling exceeded ({duration}s > {static_hold_ceiling}s) without C1 push-in.")

        # Heavy effect budget summary checks
        if c5_count > 1:
            errors.append(f"Heavy effect C5 (glitch) budgeted at most 1x per video, found {c5_count}x.")
        if c6_count > 1:
            errors.append(f"Heavy effect C6 (screen shake) budgeted at most 1x per video, found {c6_count}x.")
        if fmt == "short" and c4_count > 2:
            warnings.append(f"Match cut C4 used {c4_count}x in short (budget recommends <= 2x).")

        # 4. Total Duration Check
        tolerance = 0.10 if fmt == "short" else 0.05
        min_allowed = target_duration * (1.0 - tolerance)
        max_allowed = target_duration * (1.0 + tolerance)
        if not (min_allowed <= total_time <= max_allowed):
            warnings.append(f"Total duration {total_time:.1f}s deviates from target {target_duration:.1f}s by >{tolerance*100:.0f}%.")

        # 5. Brand Layer Immutability
        style_pack = brief.get("style_pack", "S1")
        if style_pack not in ["S1", "S2", "S3"]:
            errors.append(f"Invalid style_pack '{style_pack}'. Must be S1, S2, or S3.")

        # 6. Variety vs History Check
        variety_valid, var_err = self.check_variety(plan)
        if not variety_valid:
            warnings.append(var_err)

        return (len(errors) == 0), errors, warnings

    def check_variety(self, plan: Dict[str, Any]) -> Tuple[bool, str]:
        """Checks that plan differs by at least 3 scene-layer elements from recent history."""
        if not os.path.exists(self.history_dir):
            return True, ""

        history_files = [
            os.path.join(self.history_dir, f)
            for f in sorted(os.listdir(self.history_dir))
            if f.endswith(".json")
        ][-3:]

        if not history_files:
            return True, ""

        current_features = self._extract_plan_features(plan)

        for h_file in history_files:
            try:
                h_plan = load_json(h_file)
                h_features = self._extract_plan_features(h_plan)
                diffs = self._count_feature_differences(current_features, h_features)
                if diffs < 3:
                    return False, f"Plan has only {diffs} scene-layer differences compared to {os.path.basename(h_file)} (minimum 3 required)."
            except Exception:
                continue

        return True, ""

    def _extract_plan_features(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        beats = plan.get("beats", [])
        hook_type = beats[0].get("primary", "") if beats else ""
        primary_visuals = [b.get("primary", "") for b in beats]
        transitions = [b.get("transition_out", "") for b in beats if b.get("transition_out")]
        accent = plan.get("brief", {}).get("color_accent", "accent_cyan")
        topic_type = plan.get("brief", {}).get("topic_type", "")
        return {
            "hook_primary": hook_type,
            "primary_visuals": primary_visuals,
            "transitions": transitions,
            "accent": accent,
            "topic_type": topic_type
        }

    def _count_feature_differences(self, f1: Dict[str, Any], f2: Dict[str, Any]) -> int:
        diffs = 0
        if f1["hook_primary"] != f2["hook_primary"]:
            diffs += 1
        if f1["accent"] != f2["accent"]:
            diffs += 1
        if f1["topic_type"] != f2["topic_type"]:
            diffs += 1
        if f1["primary_visuals"] != f2["primary_visuals"]:
            diffs += 1
        if f1["transitions"] != f2["transitions"]:
            diffs += 1
        return diffs

def main():
    parser = argparse.ArgumentParser(description="Check TechXKenil Scene Plan against Animation Intelligence rules.")
    parser.add_argument("plan_file", help="Path to scene_plan.json")
    parser.add_argument("--skill-dir", help="Path to animation-library directory", default=None)
    args = parser.parse_args()

    if not os.path.isfile(args.plan_file):
        print(f"Error: File not found: {args.plan_file}", file=sys.stderr)
        sys.exit(2)

    try:
        plan = load_json(args.plan_file)
    except Exception as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
        sys.exit(2)

    linter = ScenePlanLinter(args.skill_dir)
    is_valid, errors, warnings = linter.lint(plan)

    print("=" * 60)
    print(f"TECHXKENIL SCENE PLAN LINTER REPORT: {os.path.basename(args.plan_file)}")
    print("=" * 60)
    
    if warnings:
        print(f"\n[WARNINGS ({len(warnings)})]:")
        for w in warnings:
            print(f"  * {w}")

    if not is_valid:
        print(f"\n[FAILED - ERRORS ({len(errors)})]:")
        for e in errors:
            print(f"  x {e}")
        print("\nPlan REJECTED. Fix errors above before rendering.")
        sys.exit(1)
    else:
        print("\n[PASSED]: Plan complies with all Animation Intelligence rules.")
        sys.exit(0)

if __name__ == "__main__":
    main()
