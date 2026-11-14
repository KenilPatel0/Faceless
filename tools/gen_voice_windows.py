#!/usr/bin/env python3
"""
gen_voice_windows.py — Production Windows Voice Engine (SAPI SpeechSynthesizer)
Generates high-quality, 100% offline local speech narration on Windows.
Supports beat-by-beat timeline generation, silence padding, and -14 LUFS loudness mastering.

Usage:
  python tools/gen_voice_windows.py --text "This is native 4K at sixty frames per second." --out test.wav
  python tools/gen_voice_windows.py --list-voices
"""

import os
import sys
import json
import argparse
import subprocess
import shutil
from typing import List, Dict, Any, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
FFMPEG = shutil.which("ffmpeg") or os.path.expanduser(r"~\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe")


def list_installed_voices() -> List[str]:
    """Returns list of installed Windows SAPI voices."""
    ps_cmd = """
    Add-Type -AssemblyName System.Speech;
    $s = New-Object System.Speech.Synthesis.SpeechSynthesizer;
    $s.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name };
    $s.Dispose();
    """
    res = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
    voices = [line.strip() for line in res.stdout.splitlines() if line.strip()]
    return voices


def get_audio_duration(path: str) -> float:
    """Gets audio duration in seconds using FFmpeg."""
    cmd = [FFMPEG, "-hide_banner", "-i", path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    import re
    m = re.findall(r"Duration:\s+(\d+):(\d+):([\d.]+)", res.stderr)
    if m:
        h, mn, s = m[0]
        return int(h) * 3600 + int(mn) * 60 + float(s)
    return 3.0


def speak_to_file(text: str, out_wav: str, voice: str = "Microsoft David Desktop", rate: int = 1):
    """Synthesizes text directly to a WAV file using Windows SpeechSynthesizer."""
    os.makedirs(os.path.dirname(os.path.abspath(out_wav)), exist_ok=True)
    clean_wav = out_wav.replace("\\", "/")
    clean_text = text.replace("'", "''")
    
    ps_script = f"""
    Add-Type -AssemblyName System.Speech;
    $s = New-Object System.Speech.Synthesis.SpeechSynthesizer;
    if ('{voice}') {{
        try {{ $s.SelectVoice('{voice}'); }} catch {{}}
    }}
    $s.SetOutputToWaveFile('{clean_wav}');
    $s.Rate = {rate};
    $s.Speak('{clean_text}');
    $s.Dispose();
    """
    res = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"SAPI voice generation failed: {res.stderr}")


def build_timeline_voice(
    scenes: List[Dict[str, Any]],
    output_dir: str,
    voice: str = "Microsoft David Desktop",
    rate: int = 1,
    target_lufs: float = -14.0
) -> Tuple[str, str, List[List[float]]]:
    """
    Generates beat-by-beat narration, precise silence padding, and mastered audio.
    Returns: (master_wav_path, tl_json_path, timeline_durations)
    """
    os.makedirs(output_dir, exist_ok=True)
    temp_wavs = []
    tl = []
    
    print(f"🎙️ Generating Windows Voice Narration ({voice}, rate={rate})...")
    beat_global_idx = 0
    
    for sc_idx, sc in enumerate(scenes):
        scene_durations = []
        beats = sc.get("beats", [])
        for b_idx, beat in enumerate(beats):
            beat_global_idx += 1
            text = beat[0] if isinstance(beat, (list, tuple)) else beat
            wav_path = os.path.join(output_dir, f"_temp_beat_{beat_global_idx}.wav")
            
            speak_to_file(text, wav_path, voice=voice, rate=rate)
            dur = get_audio_duration(wav_path)
            
            # Silence padding: 0.18s standard, +0.40s on chapter ends
            is_section_end = (b_idx == len(beats) - 1 and sc_idx < len(scenes) - 1)
            pad = 0.40 if is_section_end else 0.18
            final_dur = dur + pad
            
            padded_wav = os.path.join(output_dir, f"_padded_{beat_global_idx}.wav")
            subprocess.run([
                FFMPEG, "-y", "-i", wav_path,
                "-af", f"apad=pad_dur={pad}",
                "-c:a", "pcm_s16le", padded_wav
            ], capture_output=True, check=True)
            
            temp_wavs.append(padded_wav)
            scene_durations.append(round(final_dur, 3))
            try:
                os.remove(wav_path)
            except Exception:
                pass
                
        tl.append(scene_durations)

    # Concat all padded files
    concat_list = os.path.join(output_dir, "_concat.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        for tw in temp_wavs:
            clean_tw = tw.replace("\\", "/")
            f.write(f"file '{clean_tw}'\n")

    raw_wav = os.path.join(output_dir, "audio_raw.wav")
    subprocess.run([
        FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
        "-c:a", "pcm_s16le", raw_wav
    ], capture_output=True, check=True)

    # Master to YouTube standard -14 LUFS with peak limiter
    master_wav = os.path.join(output_dir, "audio_master.wav")
    print(f"🎚️ Mastering Audio to {target_lufs} LUFS + Peak Limiting...")
    subprocess.run([
        FFMPEG, "-y", "-i", raw_wav,
        "-af", f"loudnorm=I={target_lufs}:TP=-1.5:LRA=7,volume=2.0dB,alimiter=limit=-1.0dB:level=disabled",
        "-c:a", "pcm_s16le", master_wav
    ], capture_output=True, check=True)

    # Save tl.json
    tl_path = os.path.join(output_dir, "tl.json")
    with open(tl_path, "w", encoding="utf-8") as f:
        json.dump(tl, f, indent=2)

    total_sec = sum(sum(bd) for bd in tl)
    print(f"✓ Audio generation complete! Duration: {total_sec:.2f}s ({len(tl)} scenes)")
    print(f"  Mastered Audio: {master_wav}")
    print(f"  Timeline Data : {tl_path}")

    # Cleanup temp files
    try:
        os.remove(concat_list)
        for tw in temp_wavs:
            os.remove(tw)
    except Exception:
        pass

    return master_wav, tl_path, tl


def main():
    parser = argparse.ArgumentParser(description="Windows Voice Generator for Faceless Engine")
    parser.add_argument("--text", help="Direct text to speak")
    parser.add_argument("--out", default="voice_output.wav", help="Output WAV path")
    parser.add_argument("--voice", default="Microsoft David Desktop", help="Windows voice name")
    parser.add_argument("--rate", type=int, default=1, help="Speech rate (-10 to 10)")
    parser.add_argument("--list-voices", action="store_true", help="List available Windows voices")

    args = parser.parse_args()

    if args.list_voices:
        voices = list_installed_voices()
        print("Installed Windows SAPI Voices:")
        for v in voices:
            print(f"  • {v}")
        return

    if not args.text:
        parser.print_help()
        sys.exit(1)

    print(f"Synthesizing: \"{args.text}\" with voice '{args.voice}'...")
    speak_to_file(args.text, args.out, voice=args.voice, rate=args.rate)
    print(f"✓ Saved audio to: {args.out}")


if __name__ == "__main__":
    main()
