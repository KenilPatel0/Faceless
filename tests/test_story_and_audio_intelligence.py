#!/usr/bin/env python3
"""
test_story_and_audio_intelligence.py — Comprehensive Unit Test Suite for:
1. Faceless Storytelling, Scene Direction & Visual Production Intelligence Spec
2. Faceless Audio & Caption Intelligence Spec
"""

import os
import sys
import tempfile
import pytest
from dataclasses import asdict

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from tools.story_director import StoryDirector, StoryBrief, StoryBeat, VisualBible, ScenePlan, ShotPlan
from tools.asset_registry import AssetRegistry, AssetMetadata, LicenseInfo
from tools.story_validator import StoryValidator
from tools.audio_director import AudioDirector, VoiceProfile, prepare_spoken_script, AudioCue, KokoroTTSAdapter
from tools.caption_engine import CaptionTrack, CaptionCue, VisualCaptionPlan
from tools.audio_caption_qa import verify_caption_compliance


# ==============================================================================
# 1. STORYTELLING & SCENE DIRECTION TESTS
# ==============================================================================
def test_story_brief_validation():
    brief = StoryBrief(
        project_id="test_001",
        title="Understanding AI Inference",
        format="technology_explainer",
        aspect_ratio="16:9"
    )
    errs = brief.validate()
    assert len(errs) == 0

    bad_brief = StoryBrief(
        project_id="test_bad",
        title="",
        format="unsupported_format",
        aspect_ratio="21:9"
    )
    bad_errs = bad_brief.validate()
    assert len(bad_errs) >= 3


def test_story_beat_analysis_and_scene_planning():
    sample_scenes = [
        {"id": "scene_01", "section": "HOOK", "title": "The Latency Puzzle", "narration": "Why does AI take 28ms?", "duration": 4.5, "visual_type": "hook_stopwatch"},
        {"id": "scene_02", "section": "EXPLANATION", "title": "Tokenization", "narration": "Words become vectors.", "duration": 5.0, "visual_type": "token_fracture"},
        {"id": "scene_03", "section": "VERDICT", "title": "Recap", "narration": "Subscribe to TechXKenil.", "duration": 4.0, "visual_type": "outro_conversion"}
    ]
    director = StoryDirector()
    brief = director.create_brief_from_scenes("p_test", "Test Story", sample_scenes, format_override="technology_explainer")
    assert brief.format == "technology_explainer"

    beats = director.segment_script_into_beats(sample_scenes)
    assert len(beats) == 3
    assert beats[0].beat_type == "hook"
    assert beats[1].beat_type == "mechanism"
    assert beats[2].beat_type == "recap"

    plans = director.plan_scenes(brief, beats, sample_scenes)
    assert len(plans) == 3
    assert plans[0].archetype == "cold_open_result"
    assert plans[1].archetype == "flow_pipeline"
    assert plans[2].archetype == "recap_tableau"


def test_asset_registry_and_story_validator():
    registry = AssetRegistry()
    assert registry.get("bg_obsidian_atmospheric") is not None
    assert registry.get("sfx_procedural_chime") is not None

    # Custom Asset
    custom_asset = AssetMetadata(
        asset_id="chart_inference_latency",
        asset_type="vector_diagram",
        path="assets/chart_latency.png",
        source_type="authentic_capture",
        license=LicenseInfo(name="CC_BY_4.0", commercial_use_reviewed=True)
    )
    registry.register(custom_asset)
    assert registry.get("chart_inference_latency") is not None

    # Validator
    validator = StoryValidator(registry)
    brief = StoryBrief(project_id="p1", title="Test Story", format="technology_explainer")
    beats = [StoryBeat(beat_id="b1", order=0, text="Intro", beat_type="hook")]
    scenes = [ScenePlan(
        scene_id="s1",
        beat_ids=["b1"],
        title="Intro Scene",
        archetype="cold_open_result",
        purpose="Hook",
        viewer_takeaway="Takeaway",
        start_time=0.0,
        duration=5.0,
        layers=[{"layer_id": "bg", "asset_id": "bg_obsidian_atmospheric"}]
    )]

    valid, errs, warns = validator.validate_production_plan(brief, beats, scenes)
    assert valid is True
    assert len(errs) == 0


# ==============================================================================
# 2. AUDIO INTELLIGENCE TESTS
# ==============================================================================
def test_speech_preparation_normalization():
    raw_script = "However ChatGPT processes 70B parameters with 140 GB memory bus at 3.35 TB/s in 28 ms."
    prepared = prepare_spoken_script(raw_script)
    assert "However," in prepared
    assert "Chat G P T" in prepared
    assert "140 gigabytes" in prepared
    assert "3.35 terabytes per second" in prepared
    assert "28 milliseconds" in prepared


def test_audio_director_sfx_planning():
    timeline = [
        {"start_time": 0.0, "section": "INTRO", "visual_type": "hook_stopwatch"},
        {"start_time": 10.0, "section": "BODY", "visual_type": "token_fracture"},
        {"start_time": 20.0, "section": "OUTRO", "visual_type": "outro_conversion"}
    ]
    director = AudioDirector(sfx_intensity=2)
    cues = director.plan_audio_events(timeline)

    # Must contain section whooshes, pop, tick, and chime
    cue_types = [c.cue_type for c in cues]
    assert "whoosh" in cue_types
    assert "pop" in cue_types
    assert "chime" in cue_types
    assert "tick" in cue_types


# ==============================================================================
# 3. CAPTION INTELLIGENCE TESTS (LAYER A & LAYER B)
# ==============================================================================
def test_two_layer_caption_engine():
    track = CaptionTrack(language="en")
    track.add_cue(CaptionCue(
        cue_id="cue_01",
        start_s=0.5,
        end_s=2.8,
        text="Why is the sky blue?",
        speaker_id="narrator"
    ))
    track.add_cue(CaptionCue(
        cue_id="cue_02",
        start_s=3.0,
        end_s=5.5,
        text="Sunlight scatters through atmospheric particles.",
        speaker_id="narrator"
    ))

    with tempfile.TemporaryDirectory() as tmp_dir:
        srt_file = os.path.join(tmp_dir, "test.srt")
        vtt_file = os.path.join(tmp_dir, "test.vtt")

        track.export_srt(srt_file)
        track.export_vtt(vtt_file)

        assert os.path.exists(srt_file)
        assert os.path.exists(vtt_file)

        with open(srt_file, "r", encoding="utf-8") as f:
            srt_content = f.read()
            assert "00:00:00,500 --> 00:00:02,800" in srt_content
            assert "Why is the sky blue?" in srt_content

        with open(vtt_file, "r", encoding="utf-8") as f:
            vtt_content = f.read()
            assert "WEBVTT" in vtt_content
            assert "00:00:00.500 --> 00:00:02.800" in vtt_content

    # Layer B: Presentation Plan
    vis_plan = VisualCaptionPlan(track, is_short=False)
    assert len(vis_plan.chunks) >= 2

    # Verify Netflix Readability limits
    valid, errs, warns = verify_caption_compliance(vis_plan)
    assert valid is True
    assert len(errs) == 0


def test_scene_director_safe_margins():
    """Verifies that scene content layers stay within safe zone (<= 880px) to clear captions at 1010px."""
    registry = AssetRegistry()
    validator = StoryValidator(registry)
    brief = StoryBrief(project_id="p2", title="Safe Margins Test", format="technology_explainer")
    beats = [StoryBeat(beat_id="b1", order=0, text="Intro", beat_type="hook")]
    
    # Safe scene
    safe_scene = ScenePlan(
        scene_id="s_safe",
        beat_ids=["b1"],
        title="Safe Scene",
        archetype="cold_open_result",
        purpose="Hook",
        viewer_takeaway="Takeaway",
        start_time=0.0,
        duration=4.0,
        layers=[{"layer_id": "content", "asset_id": "bg_obsidian_atmospheric", "bounds": {"y_max": 850}}]
    )
    valid, errs, warns = validator.validate_production_plan(brief, beats, [safe_scene])
    assert valid is True

    # Unsafe scene (exceeds 880px)
    unsafe_scene = ScenePlan(
        scene_id="s_unsafe",
        beat_ids=["b1"],
        title="Unsafe Scene",
        archetype="cold_open_result",
        purpose="Hook",
        viewer_takeaway="Takeaway",
        start_time=0.0,
        duration=4.0,
        layers=[{"layer_id": "content", "asset_id": "bg_obsidian_atmospheric", "bounds": {"y_max": 960}}]
    )
    u_valid, u_errs, u_warns = validator.validate_production_plan(brief, beats, [unsafe_scene])
    assert u_valid is False
    assert any("Caption clearance violation" in e for e in u_errs)


def test_asset_registry_license_tracking():
    registry = AssetRegistry()
    asset1 = AssetMetadata(
        asset_id="test_stock_clip",
        asset_type="footage_clip",
        path="assets/clip.mp4",
        source_type="licensed_stock",
        license=LicenseInfo(name="Pexels", commercial_use_reviewed=True, attribution_required=True, attribution_text="Video by Mixkit")
    )
    registry.register(asset1)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        log_path = os.path.join(tmp_dir, "license_log.json")
        attr_path = os.path.join(tmp_dir, "attribution.txt")
        
        # Write license log
        import json
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump([asdict(a) for a in registry.assets.values()], f, indent=2)
        assert os.path.exists(log_path)
        
        # Write attribution
        with open(attr_path, "w", encoding="utf-8") as f:
            for a in registry.assets.values():
                if a.license.attribution_required:
                    f.write(f"- {a.asset_id}: {a.license.attribution_text}\n")
        
        assert os.path.exists(attr_path)
        with open(attr_path, "r", encoding="utf-8") as f:
            content = f.read()
            assert "Video by Mixkit" in content


def test_voice_profile_and_audio_mono_check():
    from tools.audio_director import AudioMixer
    import numpy as np
    import soundfile as sf

    mixer = AudioMixer(target_lufs=-16.0)
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create a mono wav file
        mono_wav = os.path.join(tmp_dir, "test_mono.wav")
        data = np.sin(2 * np.pi * 440 * np.linspace(0, 1, 48000)).astype(np.float32)
        sf.write(mono_wav, data, 48000)

        is_compat, corr = mixer.check_mono_compatibility(mono_wav)
        assert is_compat is True
        assert corr == 1.0

        # Create a stereo in-phase wav
        stereo_wav = os.path.join(tmp_dir, "test_stereo.wav")
        stereo_data = np.stack([data, data * 0.9], axis=1)
        sf.write(stereo_wav, stereo_data, 48000)

        is_compat_stereo, corr_stereo = mixer.check_mono_compatibility(stereo_wav)
        assert is_compat_stereo is True
        assert corr_stereo > 0.95

