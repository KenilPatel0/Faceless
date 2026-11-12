#!/bin/bash
set -e

echo "=== TechXKenil Video Production Pipeline Setup ==="

# Check Python 3
if command -v python3.12 >/dev/null 2>&1; then
    PY=python3.12
elif [ -f "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3" ]; then
    PY="/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"
else
    PY=python3
fi

echo "Using Python: $($PY --version)"

# Create venv if not exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment in .venv..."
    $PY -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip
pip install kokoro-onnx soundfile numpy pillow

# Download Kokoro ONNX model files if missing
if [ ! -f "kokoro.onnx" ]; then
    echo "Downloading kokoro.onnx..."
    curl -L -o kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
fi

if [ ! -f "voices.bin" ]; then
    echo "Downloading voices.bin..."
    curl -L -o voices.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
fi

# Font check
if [ ! -f "fonts/InterDisplay-Bold.otf" ]; then
    echo "Downloading InterDisplay-Bold font..."
    mkdir -p fonts
    curl -L -o /tmp/inter.zip https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip
    unzip -j /tmp/inter.zip "*InterDisplay-Bold.otf" -d fonts/
    rm -f /tmp/inter.zip
fi

echo "=== Setup complete and ready to render! ==="
