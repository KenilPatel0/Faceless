---
name: techxkenil-real-ui
description: Use whenever you create or edit any TechXKenil video that shows real software, websites, tools, terminal commands, or operating system dialogs (e.g. GitHub, Terminal, Windows Defender, VS Code, ChatGPT). Enforces using REAL app screen captures and authentic UI assets instead of synthetic hand-drawn mockups.
---

# TechXKenil Real UI Capture Skill

## 1. Iron Rule
**NEVER hand-draw synthetic or fake mockups of existing websites, apps, or operating systems using Pillow shapes.**  
When a video explains GitHub, Terminal commands, Windows Defender, or developer tools, viewers want to see the **REAL UI**—identical to what they will see on their own computers.

## 2. UI Capture Pipelines

### A. Real Websites & Web Apps (GitHub, Hugging Face, ChatGPT, Docs)
Use `python/tools/capture_ui.py web` to capture a genuine headless Chromium screenshot at video resolution:
```bash
# Capture full 1920x1080 web page in dark mode
python tools/capture_ui.py web \
  --url "https://github.com/Anil-matcha/Open-Generative-AI" \
  --out "python/<project_dir>/real_github_ui.png" \
  --width 1920 --height 1080
```
- Automatically handles network idle waiting.
- Emulates high-DPI retina display (`device_scale_factor=2`) for crisp text.

### B. Real Terminal Windows (macOS & Linux)
Use `python/tools/capture_ui.py terminal` to generate an authentic macOS Terminal window:
```bash
python tools/capture_ui.py terminal \
  --cmd "xattr -cr /Applications/Open-Higgsfield-AI.app" \
  --out "python/<project_dir>/real_terminal_ui.png" \
  --title "zsh — 80×24"
```
- Features genuine macOS window chrome: traffic lights (`#FF5F56`, `#FFBD2E`, `#27C93F`), title bar, and system Menlo/SF Mono font.

### C. Real Operating System Modals (Windows 11 / macOS)
- Pull authentic, high-resolution OS dialog assets from `media/library/ui/` (Windows 11 SmartScreen, Defender alert, macOS Gatekeeper).
- Never sketch fake dialog boxes with primitive PIL rectangles.

### D. Real VS Code Workbench
- Launch via `code serve-web --port 9400` and capture the real web workbench, or use high-resolution VS Code Dark Modern screenshots.

## 3. Compositing Real UI in Video Frames
When compositing a real UI capture into the video:
1. Place the UI inside a clean device or window mockup (e.g. floating laptop mockup or clean shadow container).
2. Apply smooth camera push-in: `push_in(ui_image, p, amount=0.04)` so the screenshot feels alive.
3. Add a highlight box or cursor ripple over the exact button being clicked (e.g. "Download DMG" or "More info").

