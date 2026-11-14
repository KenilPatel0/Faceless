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
# Capture full 4K UHD web page in dark mode (3840x2160, Retina 2x)
python tools/capture_ui.py web \
  --url "https://github.com/ollama/ollama" \
  --out "VideoFiles/<project_dir>/real_github_4k.png" \
  --4k
```
- Automatically handles network idle waiting.
- Emulates high-DPI retina display (`device_scale_factor=2`) for crisp text on 4K displays.

### B. Real Terminal Windows (macOS & Linux)
Use `tools/capture_ui.py terminal` to generate an authentic macOS Terminal window:
```bash
# Generate native 4K Terminal capture (2560x1440 active window canvas)
python tools/capture_ui.py terminal \
  --cmd "ollama run deepseek-r1:8b" \
  --out "VideoFiles/<project_dir>/real_terminal_4k.png" \
  --4k
```

### C. Authentic OS & Software Assets
For authentic system dialogs (e.g. Windows SmartScreen "Windows protected your PC", macOS Security, VS Code extensions):
- Always source authentic PNG assets or take genuine screen captures.
- Never improvise fake OS warnings with raw Pillow rectangles and default fonts.
