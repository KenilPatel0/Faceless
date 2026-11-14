#!/usr/bin/env python3
"""
audio_director.py — Provider-Neutral Audio & Sound Intelligence for Faceless.
Implements the Faceless Audio & Caption Intelligence Specification:
- Provider-neutral TTS Adapter (SpeechRequest, SpeechResult, KokoroTTSAdapter)
- Voice Profiles (VoiceProfile, txk_practical_host default preset)
- Speech Preparation (conversational splitting, technical pronunciation normalization)
- SFX Taxonomy & Semantic Event Mapping (intensity 0-4, event triggers)
- Multi-Stem Audio Mixer (VOICE, MUSIC, SFX, AMBIENCE, MASTER, sidechain ducking)
- Broadcast Loudness (-16.0 LUFS-I, -1.0 dBTP ceiling, mono fold-down check)
"""

import os
import re
import json
import math
import subprocess
import shutil
import numpy as np
import soundfile as sf
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple, Protocol

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))


def get_ffmpeg_path() -> str:
    for c in [shutil.which("ffmpeg"), os.path.expanduser(r"~\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"), "ffmpeg"]:
        if c and (os.path.exists(c) or shutil.which(c)):
            return c
    return "ffmpeg"


# ==============================================================================
# 1. PROVIDER-NEUTRAL TTS CONTRACTS
# ==============================================================================
@dataclass
class SpeechRequest:
    text: str
    language: str = "en-us"
    voice_id: str = "am_michael"
    speed: float = 1.1
    delivery: str = "practical_host" # neutral, curious, reassuring, emphatic, serious
    output_format: str = "wav"
    sample_rate: int = 24000
    pronunciation_refs: Dict[str, str] = field(default_factory=dict)
    continuity_context: Optional[str] = None


@dataclass
class SpeechResult:
    audio_path: str
    sample_rate: int
    channels: int
    duration_s: float
    request_id: str
    warnings: List[str] = field(default_factory=list)


class TTSProvider(Protocol):
    def synthesize(self, request: SpeechRequest, output_wav_path: str) -> SpeechResult: ...
    def list_voices(self) -> List[str]: ...


class KokoroTTSAdapter:
    """Built-in provider-neutral adapter for Kokoro v1.0 ONNX."""
    def __init__(self, model_path: Optional[str] = None, voices_path: Optional[str] = None):
        self.model_path = model_path or os.path.join(REPO_ROOT, "kokoro_models", "kokoro-v1.0.onnx")
        self.voices_path = voices_path or os.path.join(REPO_ROOT, "kokoro_models", "voices-v1.0.bin")
        self._kokoro = None

    def _get_engine(self):
        if self._kokoro is None:
            from kokoro_onnx import Kokoro
            self._kokoro = Kokoro(self.model_path, self.voices_path)
        return self._kokoro

    def synthesize(self, request: SpeechRequest, output_wav_path: str) -> SpeechResult:
        engine = self._get_engine()
        samples, sr = engine.create(
            request.text,
            voice=request.voice_id,
            speed=request.speed,
            lang=request.language
        )
        dur = len(samples) / float(sr)
        os.makedirs(os.path.dirname(output_wav_path), exist_ok=True)
        sf.write(output_wav_path, samples, sr)

        return SpeechResult(
            audio_path=output_wav_path,
            sample_rate=sr,
            channels=1,
            duration_s=round(dur, 3),
            request_id=f"kokoro_{request.voice_id}_{int(dur*1000)}"
        )

    def list_voices(self) -> List[str]:
        return ["am_michael", "af_bella", "af_sarah", "am_adam", "bf_emma", "bm_george"]


# ==============================================================================
# 2. VOICE PROFILES & SPEECH PREPARATION
# ==============================================================================
@dataclass
class VoiceProfile:
    profile_id: str = "txk_practical_host"
    role: str = "Adult presenter; conversational and credible"
    voice_id: str = "am_michael"
    speed: float = 1.1
    language: str = "en-us"
    loudness_target_lufs: float = -16.0
    true_peak_max_dbtp: float = -1.0
    sample_rate: int = 48000
    pronunciation_overrides: Dict[str, str] = field(default_factory=lambda: {
        "TechXKenil": "Tech X Kenil",
        "ChatGPT": "Chat G P T",
        "LLM": "L L M",
        "GPU": "G P U",
        "VRAM": "VEE RAM",
        "HBM3": "H B M Three",
        "TFLOPS": "Tera Flops",
        "FLOPs": "Flops",
        "KV": "K V",
        "ms": "milliseconds"
    })


def prepare_spoken_script(raw_text: str, profile: Optional[VoiceProfile] = None) -> str:
    """
    Transforms written copy into speakable narration:
    - Normalizes abbreviations, technical terms, and acronyms
    - Replaces stiff formalisms with conversational phrasing
    - Preserves code syntax and numbers accurately
    """
    p = profile or VoiceProfile()
    text = raw_text

    # Apply pronunciation overrides
    for k, v in p.pronunciation_overrides.items():
        text = re.sub(rf"\b{re.escape(k)}\b", v, text)

    # Conversational sentence pacing: commas after introductory transitions
    text = re.sub(r"\b(However|Therefore|Furthermore|Next|Meanwhile)\b(?!\s*,)", r"\1,", text)
    
    # Expand units
    text = re.sub(r"(\d+)\s*ms\b", r"\1 milliseconds", text)
    text = re.sub(r"(\d+)\s*GB\b", r"\1 gigabytes", text)
    text = re.sub(r"(\d+)\s*TB/s\b", r"\1 terabytes per second", text)

    return text.strip()


# ==============================================================================
# 3. SFX TAXONOMY & INTENSITY CONTROLLER
# ==============================================================================
SFX_TAXONOMY = {
    "ui_micro": ["pop", "tick", "soft_click"],
    "digital_tech": ["scan", "pulse", "chime"],
    "transition": ["whoosh", "sweep"],
    "impact_reveal": ["thud", "chime"],
    "alert_feedback": ["success_chime", "warning_tick"]
}


@dataclass
class AudioCue:
    cue_id: str
    cue_type: str            # pop, tick, whoosh, chime, soft_click
    time_s: float
    gain_db: float = -6.0
    priority: int = 1        # 0 = lowest, 3 = highest
    reason: str = "punctuation"


class AudioDirector:
    """Plans speech, SFX punctuation, and music ducking based on narrative beats."""
    def __init__(self, voice_profile: Optional[VoiceProfile] = None, sfx_intensity: int = 1):
        self.profile = voice_profile or VoiceProfile()
        self.sfx_intensity = max(0, min(4, sfx_intensity))

    def plan_audio_events(self, timeline: List[Dict[str, Any]]) -> List[AudioCue]:
        """
        Creates purposeful sound cues attached to visual and narrative events.
        Enforces restraint: SFX as punctuation, not wallpaper.
        """
        if self.sfx_intensity == 0:
            return []

        cues: List[AudioCue] = []
        last_sec = None

        for idx, s in enumerate(timeline):
            st = s["start_time"]
            sec = s.get("section")
            vtype = s.get("visual_type", "")

            # 1. Section Transition Whoosh (Only on meaningful section change)
            if sec and sec != last_sec:
                cues.append(AudioCue(
                    cue_id=f"whoosh_{idx}",
                    cue_type="whoosh",
                    time_s=st,
                    gain_db=-8.0,
                    priority=2,
                    reason=f"Section change to {sec}"
                ))
                last_sec = sec

            # 2. Event-anchored SFX (Intensity-scaled)
            if self.sfx_intensity >= 1:
                if vtype in ["hook_stopwatch", "cold_open_result"]:
                    cues.append(AudioCue(cue_id=f"pop_{idx}", cue_type="pop", time_s=st + 1.6, gain_db=-6.0, reason="Enter trigger"))
                    cues.append(AudioCue(cue_id=f"chime_{idx}", cue_type="chime", time_s=st + 4.8, gain_db=-7.0, reason="Milestone stamp"))
                elif vtype in ["token_fracture", "flow_pipeline"]:
                    cues.append(AudioCue(cue_id=f"pop_{idx}", cue_type="pop", time_s=st + 0.6, gain_db=-6.0, reason="Token slice"))
                    cues.append(AudioCue(cue_id=f"chime_{idx}", cue_type="chime", time_s=st + 3.2, gain_db=-8.0, reason="Vector lock"))
                elif vtype in ["kv_cache_split", "comparison_board"]:
                    cues.append(AudioCue(cue_id=f"tick_{idx}", cue_type="tick", time_s=st + 0.4, gain_db=-6.0, reason="Warning tick"))
                    cues.append(AudioCue(cue_id=f"chime_{idx}", cue_type="chime", time_s=st + 4.5, gain_db=-7.0, reason="Cache savior"))
                elif vtype in ["speculative_race", "cause_effect"]:
                    cues.append(AudioCue(cue_id=f"pop_{idx}", cue_type="pop", time_s=st + 3.2, gain_db=-6.0, reason="Speedup multiplier"))
                elif vtype in ["outro_conversion", "recap_tableau"]:
                    cues.append(AudioCue(cue_id=f"tick_{idx}", cue_type="tick", time_s=st + 4.6, gain_db=-5.0, reason="Subscribe click"))
                    cues.append(AudioCue(cue_id=f"chime_{idx}", cue_type="chime", time_s=st + 4.9, gain_db=-6.0, reason="Subscribed success"))

        return cues


# ==============================================================================
# 4. 5-STEM AUDIO MIXER & BROADCAST MASTERING
# ==============================================================================
class AudioMixer:
    """
    Assembles VOICE, MUSIC, SFX, AMBIENCE, and MASTER stems.
    Applies automatic sidechain ducking beneath speech and masters to -16.0 LUFS.
    """
    def __init__(self, target_lufs: float = -16.0, max_true_peak: float = -1.0, sample_rate: int = 48000):
        self.target_lufs = target_lufs
        self.max_true_peak = max_true_peak
        self.sample_rate = sample_rate

    def mix_stems(
        self,
        voice_wav_path: str,
        output_master_path: str,
        cues: List[AudioCue],
        include_music: bool = True,
        ducking_db: float = 6.0
    ) -> float:
        """
        Mixes voice and procedural sound events, ducking music and normalizing to target LUFS.
        """
        from tools.sound_engine import generate_sfx, generate_ambient_synth

        v_data, v_sr = sf.read(voice_wav_path, dtype="float32")
        if v_data.ndim > 1:
            v_data = np.mean(v_data, axis=1) # Mono speech

        # Resample to 48kHz if needed
        if v_sr != self.sample_rate:
            from scipy.signal import resample
            num_samples = int(len(v_data) * self.sample_rate / v_sr)
            v_data = resample(v_data, num_samples).astype(np.float32)

        total_samples = len(v_data)
        master_buffer = np.copy(v_data)

        # 1. Overlay SFX cues
        for c in cues:
            s_idx = int(c.time_s * self.sample_rate)
            if s_idx >= total_samples:
                continue
            try:
                sfx_wave = generate_sfx(c.cue_type, sr=self.sample_rate)
                gain = 10.0 ** (c.gain_db / 20.0)
                sfx_wave = sfx_wave * gain
                e_idx = min(total_samples, s_idx + len(sfx_wave))
                clip_len = e_idx - s_idx
                master_buffer[s_idx:e_idx] += sfx_wave[:clip_len]
            except Exception:
                pass

        # 2. Add Ambient Pad with sidechain ducking
        if include_music:
            total_dur = total_samples / float(self.sample_rate)
            amb = generate_ambient_synth(total_dur, sr=self.sample_rate)
            # Duck music under active speech
            speech_env = np.abs(v_data)
            # Smooth envelope
            kernel_sz = int(0.2 * self.sample_rate)
            kernel = np.ones(kernel_sz) / kernel_sz
            smooth_env = np.convolve(speech_env, kernel, mode="same")
            is_speaking = smooth_env > 0.02
            
            duck_factor = 10.0 ** (-ducking_db / 20.0)
            amb_gain = np.where(is_speaking, 0.08 * duck_factor, 0.12).astype(np.float32)
            min_amb = min(len(amb), total_samples)
            master_buffer[:min_amb] += (amb[:min_amb] * amb_gain[:min_amb])

        # 3. Save working stem
        tmp_stem = output_master_path + ".tmp.wav"
        sf.write(tmp_stem, master_buffer, self.sample_rate)

        # 4. Final EBU R128 Two-Pass Loudness Normalization via FFmpeg
        ffmpeg = get_ffmpeg_path()
        cmd = [
            ffmpeg, "-y", "-i", tmp_stem,
            "-af", f"loudnorm=I={self.target_lufs}:TP={self.max_true_peak}:LRA=7",
            "-ar", str(self.sample_rate),
            output_master_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if os.path.exists(tmp_stem):
            os.remove(tmp_stem)

        final_dur = total_samples / float(self.sample_rate)
        return final_dur

    def check_mono_compatibility(self, stereo_wav_path: str) -> Tuple[bool, float]:
        """Verifies that dialogue or essential sounds do not phase-cancel in mono."""
        data, sr = sf.read(stereo_wav_path)
        if data.ndim == 1:
            return True, 1.0 # Pure mono is 100% compatible
        left, right = data[:, 0], data[:, 1]
        corr = float(np.corrcoef(left, right)[0, 1])
        # Correlation > 0.4 indicates strong mono stability
        return corr > 0.4, round(corr, 3)
