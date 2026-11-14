---
name: real-ui
description: Use whenever you create or edit any video that shows real software, websites, tools, terminal commands, or operating system dialogs (e.g. GitHub, Terminal, Windows Defender, VS Code, ChatGPT). Enforces using REAL app screen captures and authentic UI assets instead of synthetic hand-drawn mockups.
---

# Real UI Capture Skill

## 1. Iron Rule
**NEVER hand-draw synthetic or fake mockups of existing websites, apps, or operating systems using Pillow shapes.**  
When a video explains GitHub, Terminal commands, Windows Defender, or developer tools, viewers want to see the **REAL UI**—identical to what they will see on their own computers.

## 2. UI Capture Pipelines

### A. Real Websites & Web Apps (GitHub, Hugging Face, ChatGPT, Docs)
Use `tools/capture_ui.py web` to capture a genuine headless Chromium screenshot at video resolution:
```bash
# Capture full 1920x1080 web page in dark mode
python tools/capture_ui.py web \
  --url "https://github.com/Anil-matcha/Open-Generative-AI" \
  --out "VideoFiles/<project_dir>/real_github_ui.png" \
  --width 1920 --height 1080
```
- Automatically handles network idle waiting.
- Emulates high-DPI retina display (`device_scale_factor=2`) for crisp text.

### B. Real Terminal Windows (macOS & Linux)
Use `tools/capture_ui.py terminal` to generate an authentic macOS Terminal window:
```bash
python tools/capture_ui.py terminal \
  --cmd "xattr -cr /Applications/Open-Higgsfield-AI.app" \
  --out "VideoFiles/<project_dir>/real_terminal_window.png" \
  --title "zsh — 80×24" \
  --width 1280 --height 720
```

### C. Authentic OS & Software Assets
For authentic system dialogs (e.g. Windows SmartScreen "Windows protected your PC", macOS Security, VS Code extensions):
- Always source authentic PNG assets or take genuine screen captures.
- Never improvise fake OS warnings with raw Pillow rectangles and default fonts.
