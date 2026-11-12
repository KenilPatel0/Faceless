#!/usr/bin/env bash
# ==============================================================================
# TechXKenil — Autonomous Video Production Suite Setup
# Author: Kenil Ribadiya (https://kenilribadiya.in)
# License: MIT
# ==============================================================================
set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

echo "======================================================================"
echo "🎬 Setting up TechXKenil Autonomous Video Production Suite"
echo "   Main Contributor: Kenil Ribadiya (https://kenilribadiya.in)"
echo "======================================================================"

# 1. System Dependency Checks
echo "▶ Checking system dependencies..."
if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "❌ ERROR: ffmpeg is not installed or not on PATH."
    echo "   Please install ffmpeg:"
    echo "     macOS: brew install ffmpeg"
    echo "     Ubuntu/Debian: sudo apt update && sudo apt install -y ffmpeg"
    exit 1
else
    echo "  ✓ ffmpeg detected: $(ffmpeg -version | head -n 1 | cut -d ' ' -f 1-3)"
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ ERROR: python3 is not installed."
    exit 1
else
    echo "  ✓ python3 detected: $(python3 --version)"
fi

# 2. Virtual Environment Setup
echo "▶ Configuring Python virtual environment (.venv)..."
if [ ! -d ".venv" ]; then
    echo "  Creating virtual environment in .venv..."
    python3 -m venv .venv
fi

source .venv/bin/activate
echo "  ✓ Activated virtual environment: $(python --version)"

# 3. Python Packages Installation
echo "▶ Installing Python dependencies..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
playwright install chromium --quiet 2>/dev/null || true
echo "  ✓ Dependencies & Playwright browser installed successfully."

# 4. Download TTS Models (Kokoro ONNX)
echo "▶ Checking Kokoro ONNX Text-to-Speech models..."
mkdir -p "$REPO_DIR"

if [ ! -f "kokoro.onnx" ]; then
    echo "  Downloading kokoro.onnx (~310MB)..."
    curl -L --progress-bar -o kokoro.onnx \
        "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx"
else
    echo "  ✓ kokoro.onnx is ready."
fi

if [ ! -f "voices.bin" ]; then
    echo "  Downloading voices.bin (~27MB)..."
    curl -L --progress-bar -o voices.bin \
        "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"
else
    echo "  ✓ voices.bin is ready."
fi

# 5. Font Assets
echo "▶ Verifying typography assets..."
mkdir -p fonts

if [ ! -f "fonts/InterDisplay-Bold.otf" ]; then
    echo "  Downloading Inter Display Bold font..."
    curl -L -s -o /tmp/inter.zip "https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip"
    unzip -q -j /tmp/inter.zip "*InterDisplay-Bold.otf" -d fonts/
    rm -f /tmp/inter.zip
fi

if [ ! -f "fonts/BebasNeue-Regular.ttf" ]; then
    echo "  Downloading Bebas Neue font..."
    curl -L -s -o fonts/BebasNeue-Regular.ttf \
        "https://github.com/google/fonts/raw/main/ofl/bebasneue/BebasNeue-Regular.ttf"
fi
echo "  ✓ Typography assets ready in fonts/."

# 6. Directory Structure & Symlinks
echo "▶ Configuring workspace links..."
mkdir -p VideoFiles python/tools agents/skills agents/md_files

# Symlinks for tools and skills
[ ! -L "tools" ] && [ ! -d "tools" ] && ln -sf python/tools tools || true
[ ! -L ".agents" ] && [ ! -d ".agents" ] && ln -sf agents .agents || true

echo "======================================================================"
echo "✨ Setup Completed Successfully!"
echo "======================================================================"
echo ""
echo "🚀 How to Use with Antigravity:"
echo "   Simply open this repository in Antigravity and prompt:"
echo "   - 'Make a 30s Short about [Topic]'"
echo "   - 'Make an 8-minute video about [Topic]'"
echo ""
echo "💻 Manual Command Line Rendering:"
echo "   source .venv/bin/activate"
echo "   python python/ai_answers_milliseconds/render_short_ms.py"
echo "======================================================================"
