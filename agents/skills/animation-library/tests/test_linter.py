#!/usr/bin/env python3
"""
test_linter.py — Unit tests for the Scene Plan Linter and Rule Enforcer.
"""

import os
import sys
import pytest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
sys.path.insert(0, os.path.join(SKILL_DIR, "linter"))

from check_plan import ScenePlanLinter, load_json

@pytest.fixture
def linter():
    return ScenePlanLinter(SKILL_DIR)

def test_golden_short_plan(linter):
    plan_path = os.path.join(SKILL_DIR, "tests", "golden_short_plan.json")
    plan = load_json(plan_path)
    is_valid, errors, warnings = linter.lint(plan)
    assert is_valid, f"Golden short plan failed linting: {errors}"
    assert len(errors) == 0

def test_golden_long_plan(linter):
    plan_path = os.path.join(SKILL_DIR, "tests", "golden_long_plan.json")
    plan = load_json(plan_path)
    is_valid, errors, warnings = linter.lint(plan)
    assert is_valid, f"Golden long plan failed linting: {errors}"
    assert len(errors) == 0

def test_honesty_gate_violation(linter):
    plan_path = os.path.join(SKILL_DIR, "tests", "golden_long_plan.json")
    plan = load_json(plan_path)
    # Remove source from beat with T6
    for b in plan["beats"]:
        if b.get("primary") == "T6":
            b["source"] = ""
    is_valid, errors, warnings = linter.lint(plan)
    assert not is_valid
    assert any("Honesty Gate" in e for e in errors)

def test_heavy_effect_in_first_2s_violation(linter):
    plan_path = os.path.join(SKILL_DIR, "tests", "golden_short_plan.json")
    plan = load_json(plan_path)
    # Put C5 in beat 1 (starts at 0.0s)
    plan["beats"][0]["effects"] = ["C5:once"]
    is_valid, errors, warnings = linter.lint(plan)
    assert not is_valid
    assert any("C5" in e and "first 2 seconds" in e for e in errors)

def test_consecutive_primary_repeat_violation(linter):
    plan_path = os.path.join(SKILL_DIR, "tests", "golden_short_plan.json")
    plan = load_json(plan_path)
    # Set 3 beats in a row with E3
    plan["beats"][0]["primary"] = "E3"
    plan["beats"][1]["primary"] = "E3"
    plan["beats"][2]["primary"] = "E3"
    is_valid, errors, warnings = linter.lint(plan)
    assert not is_valid
    assert any("repeated more than twice consecutively" in e for e in errors)

def test_caption_format_mismatch(linter):
    plan_path = os.path.join(SKILL_DIR, "tests", "golden_short_plan.json")
    plan = load_json(plan_path)
    # Shorts must use T1, test T2 failure
    plan["beats"][0]["captions"] = "T2"
    is_valid, errors, warnings = linter.lint(plan)
    assert not is_valid
    assert any("Caption style is 'T2', expected 'T1'" in e for e in errors)
