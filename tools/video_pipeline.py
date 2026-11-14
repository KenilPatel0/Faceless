#!/usr/bin/env python3
"""
video_pipeline.py — High-Performance Streaming Video Pipeline for Faceless Video Production
Supports native 4K 60FPS hardware-accelerated video encoding with automatic fallback:
h264_nvenc -> h264_qsv -> h264_mf -> libx264.
"""

import os
import sys
import time
import shutil
import subprocess
from typing import Optional, List, Dict, Tuple
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))


def find_ffmpeg() -> str:
    """Locates the system or WinGet FFmpeg executable."""
    candidate = shutil.which("ffmpeg")
    if candidate:
        return candidate
    winget_path = os.path.expanduser(r"~\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe")
    if os.path.exists(winget_path):
        return winget_path
    return "ffmpeg"


_CACHED_ENCODER_INFO: Optional[Dict[str, any]] = None


def probe_best_encoder(ffmpeg_exe: Optional[str] = None) -> Dict[str, any]:
    """
    Probes system encoders for 4K 60FPS encoding capability in order of priority:
    1. NVIDIA NVENC (h264_nvenc)
    2. Intel Quick Sync (h264_qsv)
    3. Windows Media Foundation (h264_mf)
    4. Software CPU (libx264 veryfast)
    """
    global _CACHED_ENCODER_INFO
    if _CACHED_ENCODER_INFO is not None:
        return _CACHED_ENCODER_INFO

    exe = ffmpeg_exe or find_ffmpeg()

    candidates = [
        {
            "name": "h264_nvenc",
            "type": "hardware_nvidia",
            "args": ["-c:v", "h264_nvenc", "-preset", "p4", "-cq", "20", "-pix_fmt", "yuv420p"]
        },
        {
            "name": "h264_qsv",
            "type": "hardware_intel",
            "args": ["-c:v", "h264_qsv", "-global_quality", "20", "-preset", "veryfast"]
        },
        {
            "name": "h264_mf",
            "type": "hardware_windows",
            "args": ["-c:v", "h264_mf", "-b:v", "22M"]
        },
        {
            "name": "libx264",
            "type": "software_cpu",
            "args": ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p"]
        }
    ]

    print("🔍 Probing available 4K 60FPS video encoders...")
    for cand in candidates:
        name = cand["name"]
        test_cmd = [
            exe, "-y", "-v", "error",
            "-f", "lavfi", "-i", "testsrc=size=3840x2160:rate=60",
            "-t", "0.2"
        ] + cand["args"] + ["-f", "null", "-"]

        try:
            res = subprocess.run(test_cmd, capture_output=True, text=True, timeout=10)
            if res.returncode == 0:
                print(f"  ✓ Encoder verified active: {name} ({cand['type']})")
                _CACHED_ENCODER_INFO = cand
                return cand
            else:
                err_msg = res.stderr.strip().splitlines()[-1] if res.stderr.strip() else "failed"
                print(f"  ✗ {name}: unsupported ({err_msg})")
        except Exception as e:
            print(f"  ✗ {name}: error probing ({e})")

    fallback = candidates[-1]
    _CACHED_ENCODER_INFO = fallback
    return fallback


class StreamingVideoPipeline:
    """
    Streaming video pipeline that ingests raw RGB frames from Python
    and streams directly to hardware-accelerated FFmpeg via stdin pipe.
    Maintains constant low memory footprint (< 350 MB RAM).
    """
    def __init__(
        self,
        output_path: str,
        width: int = 3840,
        height: int = 2160,
        fps: int = 60,
        audio_path: Optional[str] = None,
        total_frames: Optional[int] = None,
        ffmpeg_exe: Optional[str] = None
    ):
        self.output_path = os.path.abspath(output_path)
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        self.width = width
        self.height = height
        self.fps = fps
        self.audio_path = audio_path
        self.total_frames = total_frames
        self.ffmpeg_exe = ffmpeg_exe or find_ffmpeg()

        # Probe best encoder
        self.encoder_info = probe_best_encoder(self.ffmpeg_exe)
        self.cmd = self._build_ffmpeg_command()
        
        # Start FFmpeg subprocess
        self.proc = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        self.frame_count = 0
        self.t_start = time.time()

    def _build_ffmpeg_command(self) -> List[str]:
        cmd = [
            self.ffmpeg_exe, "-y",
            "-f", "rawvideo",
            "-pix_fmt", "rgb24",
            "-s", f"{self.width}x{self.height}",
            "-r", str(self.fps),
            "-i", "-"
        ]

        if self.audio_path and os.path.exists(self.audio_path):
            cmd.extend(["-i", self.audio_path])
        else:
            # Generate silent audio if no audio provided
            cmd.extend(["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"])

        # Video encoding flags
        cmd.extend(self.encoder_info["args"])

        # Audio & container flags
        cmd.extend([
            "-c:a", "aac",
            "-b:a", "192k"
        ])

        if self.total_frames:
            # Enforce exact duration alignment without abrupt mid-syllable truncation
            exact_dur = self.total_frames / float(self.fps)
            cmd.extend(["-t", f"{exact_dur:.3f}"])
        else:
            cmd.extend(["-shortest"])

        cmd.extend([
            "-movflags", "+faststart",
            self.output_path
        ])
        return cmd

    def write_frame(self, frame_or_bytes):
        """Streams a single frame to the FFmpeg stdin pipe."""
        if isinstance(frame_or_bytes, bytes):
            raw = frame_or_bytes
        elif isinstance(frame_or_bytes, Image.Image):
            raw = frame_or_bytes.tobytes()
        else:
            raise ValueError("Frame must be a PIL Image or bytes")

        self.proc.stdin.write(raw)
        self.frame_count += 1

        # Periodic progress report
        if self.frame_count % 300 == 0 or (self.total_frames and self.frame_count == self.total_frames):
            dt = max(0.001, time.time() - self.t_start)
            current_fps = self.frame_count / dt
            if self.total_frames:
                pct = (self.frame_count / self.total_frames) * 100.0
                eta = (self.total_frames - self.frame_count) / max(0.1, current_fps)
                print(f"  [Pipeline] Progress: {pct:5.1f}% ({self.frame_count}/{self.total_frames}) "
                      f"@ {current_fps:4.1f} FPS | ETA: {eta:4.1f}s")
            else:
                print(f"  [Pipeline] Rendered: {self.frame_count} frames @ {current_fps:4.1f} FPS")

    def close(self):
        """Flushes stdin and waits for FFmpeg to finish encoding."""
        stderr_output = ""
        if self.proc.stdin:
            self.proc.stdin.close()
        
        stdout_data, stderr_data = self.proc.communicate()
        if stderr_data:
            stderr_output = stderr_data.decode("utf-8", errors="replace")

        if self.proc.returncode != 0:
            err_tail = "\n".join(stderr_output.strip().splitlines()[-10:])
            raise RuntimeError(f"FFmpeg encoding failed (code {self.proc.returncode}):\n{err_tail}")

        total_time = time.time() - self.t_start
        avg_fps = self.frame_count / max(0.001, total_time)
        print(f"✓ Video pipeline complete! Rendered {self.frame_count} frames in {total_time:.1f}s ({avg_fps:.1f} avg FPS)")
        print(f"  Output saved: {self.output_path}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
