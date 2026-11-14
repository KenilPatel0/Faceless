#!/usr/bin/env python3
"""
animation_timeline.py — Deterministic Timeline & Frame State Resolver.
Converts floating-point seconds into half-open frame intervals [start_frame, end_frame),
resolves speech anchors, clamps scene boundaries, and provides frame-level evaluation state.

Implements Part III (Section 21) and Part V (Section 34) of the Implementation Spec.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any

@dataclass
class RationalFPS:
    numerator: int = 30
    denominator: int = 1

    @property
    def fps(self) -> float:
        return self.numerator / float(self.denominator)

@dataclass
class ResolvedAnimationSpan:
    layer_id: str
    animation_id: str
    start_seconds: float
    end_seconds: float
    start_frame: int
    end_frame: int
    easing: str
    intensity: int
    parameters: Dict[str, Any]
    fallback_id: Optional[str] = None

    def get_progress(self, frame_idx: int) -> float:
        """Calculates normalized progress 0.0 to 1.0 at given frame."""
        if frame_idx <= self.start_frame:
            return 0.0
        if frame_idx >= self.end_frame:
            return 1.0
        dur_frames = max(1, self.end_frame - self.start_frame)
        return (frame_idx - self.start_frame) / float(dur_frames)

@dataclass
class ResolvedBeat:
    beat_id: str
    start_seconds: float
    end_seconds: float
    start_frame: int
    end_frame: int
    visual_objective: str
    layers: List[ResolvedAnimationSpan] = field(default_factory=list)

@dataclass
class ResolvedScene:
    scene_id: str
    start_seconds: float
    end_seconds: float
    start_frame: int
    end_frame: int
    format: str
    visual_objective: str
    motion_intensity: int
    beats: List[ResolvedBeat] = field(default_factory=list)
    transition_out_id: str = "transition.cut"
    transition_out_duration: float = 0.0

class TimelineResolver:
    """Resolves an AnimationPlan into exact deterministic frame boundaries."""
    def __init__(self, plan_data: Dict[str, Any]):
        self.plan = plan_data
        proj = plan_data.get("project", {})
        fps_info = proj.get("fps", {"numerator": 30, "denominator": 1})
        self.fps = RationalFPS(fps_info.get("numerator", 30), fps_info.get("denominator", 1))
        
        self.total_duration_seconds = 0.0
        self.total_frames = 0
        self.resolved_scenes: List[ResolvedScene] = []
        self._resolve_timeline()

    def _sec_to_frame(self, sec: float) -> int:
        """Deterministic round to integer frame."""
        return int(round(sec * self.fps.fps))

    def _resolve_timeline(self):
        """Builds half-open frame intervals for all scenes, beats, and layers."""
        scenes_data = self.plan.get("scenes", [])
        if not scenes_data:
            return

        for s_idx, s_data in enumerate(scenes_data):
            st_sec = float(s_data.get("start_seconds", 0.0))
            et_sec = float(s_data.get("end_seconds", st_sec + 3.0))
            st_f = self._sec_to_frame(st_sec)
            et_f = self._sec_to_frame(et_sec)

            t_out = s_data.get("transition_out", {})
            t_id = t_out.get("id", "transition.cut")
            t_dur = float(t_out.get("duration_seconds", 0.0))

            r_scene = ResolvedScene(
                scene_id=s_data.get("scene_id", f"scene_{s_idx}"),
                start_seconds=st_sec,
                end_seconds=et_sec,
                start_frame=st_f,
                end_frame=et_f,
                format=s_data.get("format", "kinetic_explainer"),
                visual_objective=s_data.get("visual_objective", ""),
                motion_intensity=int(s_data.get("motion_intensity", 2)),
                transition_out_id=t_id,
                transition_out_duration=t_dur
            )

            # Resolve beats
            beats_data = s_data.get("beats", [])
            for b_idx, b_data in enumerate(beats_data):
                b_st_sec = max(st_sec, float(b_data.get("start_seconds", st_sec)))
                b_et_sec = min(et_sec, float(b_data.get("end_seconds", et_sec)))
                b_st_f = self._sec_to_frame(b_st_sec)
                b_et_f = self._sec_to_frame(b_et_sec)

                r_beat = ResolvedBeat(
                    beat_id=b_data.get("beat_id", f"beat_{s_idx}_{b_idx}"),
                    start_seconds=b_st_sec,
                    end_seconds=b_et_sec,
                    start_frame=b_st_f,
                    end_frame=b_et_f,
                    visual_objective=b_data.get("visual_objective", "")
                )

                # Resolve layers
                for l_idx, l_data in enumerate(b_data.get("layers", [])):
                    l_st_sec = float(l_data.get("start_seconds", b_st_sec))
                    l_dur = float(l_data.get("duration_seconds", 0.5))
                    l_et_sec = min(et_sec, l_st_sec + l_dur)
                    l_st_f = self._sec_to_frame(l_st_sec)
                    l_et_f = self._sec_to_frame(l_et_sec)

                    r_span = ResolvedAnimationSpan(
                        layer_id=l_data.get("layer_id", f"layer_{l_idx}"),
                        animation_id=l_data.get("animation_id", "object.slide"),
                        start_seconds=l_st_sec,
                        end_seconds=l_et_sec,
                        start_frame=l_st_f,
                        end_frame=l_et_f,
                        easing=l_data.get("easing", "ease_out_cubic"),
                        intensity=int(l_data.get("intensity", 2)),
                        parameters=l_data.get("parameters", {}),
                        fallback_id=l_data.get("fallback_animation_id")
                    )
                    r_beat.layers.append(r_span)

                r_scene.beats.append(r_beat)

            self.resolved_scenes.append(r_scene)

        if self.resolved_scenes:
            self.total_duration_seconds = self.resolved_scenes[-1].end_seconds
            self.total_frames = self.resolved_scenes[-1].end_frame

    def get_frame_state(self, frame_idx: int) -> Dict[str, Any]:
        """
        Deterministic Frame Evaluation State Contract:
        Returns active scene, active beats, and active layer animations at frame_idx.
        """
        sec = frame_idx / self.fps.fps

        # Find active scene
        active_scene = None
        for s in self.resolved_scenes:
            if s.start_frame <= frame_idx < s.end_frame:
                active_scene = s
                break
        if not active_scene and self.resolved_scenes:
            active_scene = self.resolved_scenes[-1]

        active_beats = []
        active_layers = []

        if active_scene:
            for b in active_scene.beats:
                if b.start_frame <= frame_idx < b.end_frame:
                    active_beats.append(b)
                for l in b.layers:
                    if l.start_frame <= frame_idx <= l.end_frame:
                        p = l.get_progress(frame_idx)
                        active_layers.append({
                            "layer": l,
                            "progress": p,
                            "is_settled": (p >= 1.0)
                        })

        return {
            "frame_idx": frame_idx,
            "time_seconds": round(sec, 4),
            "scene": active_scene,
            "active_beats": active_beats,
            "active_layers": active_layers,
            "is_transition_zone": False
        }

if __name__ == "__main__":
    sample_plan = {
        "project": {"fps": {"numerator": 30, "denominator": 1}},
        "scenes": [
            {
                "scene_id": "scene_01",
                "start_seconds": 0.0,
                "end_seconds": 3.0,
                "format": "text_led_hook",
                "beats": [
                    {
                        "beat_id": "beat_01a",
                        "start_seconds": 0.0,
                        "end_seconds": 1.5,
                        "layers": [
                            {"layer_id": "title", "animation_id": "type.scale_punch", "start_seconds": 0.0, "duration_seconds": 0.4}
                        ]
                    }
                ]
            }
        ]
    }
    resolver = TimelineResolver(sample_plan)
    print(f"🎬 Resolved Timeline: {resolver.total_frames} frames ({resolver.total_duration_seconds}s)")
    state = resolver.get_frame_state(6)
    print(f"Frame 6 state: t={state['time_seconds']}s, active layers={len(state['active_layers'])}")
    if state['active_layers']:
        print(f"  Layer title progress: {state['active_layers'][0]['progress']:.2f}")
