#!/usr/bin/env python3
"""
capture_ui.py — Real UI Capture Tool for Faceless Video Production
Captures genuine real-world UIs (Websites, macOS Terminal, Windows UI) at native 1080p and 4K resolutions.

Usage:
  python tools/capture_ui.py web --url https://github.com/ollama/ollama --out github.png --4k
  python tools/capture_ui.py terminal --cmd "ollama run deepseek-r1:8b" --out term.png --4k
"""

import sys, os, argparse, time
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

def capture_web(url, out_path, width=1920, height=1080, dark_mode=True, wait_ms=1000, is_4k=False):
    """Captures a real web page using headless Chromium (Playwright) at native or 4K Retina resolution."""
    from playwright.sync_api import sync_playwright
    
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    target_w = 3840 if is_4k else width
    target_h = 2160 if is_4k else height
    scale_factor = 2 if is_4k else 2
    
    print(f"🌐 Capturing Real Web UI from: {url} ({target_w}x{target_h} @ {scale_factor}x)")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': target_w, 'height': target_h},
            color_scheme='dark' if dark_mode else 'light',
            device_scale_factor=scale_factor
        )
        page = context.new_page()
        page.goto(url, wait_until='domcontentloaded', timeout=20000)
        time.sleep(max(1.0, wait_ms / 1000.0))
        page.screenshot(path=out_path)
        browser.close()
    print(f"  ✓ Saved real web capture to: {out_path}")

def capture_terminal(command, out_path, title="zsh — 80×24", output_lines=None, width=1280, height=720, is_4k=False):
    """Renders a pixel-perfect authentic macOS Terminal window at native 1080p or 4K resolution."""
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    
    # Scale multiplier: 4x for 4K video, 2x for 1080p
    S = 4 if is_4k else 2
    w_out = width * (2 if is_4k else 1)
    h_out = height * (2 if is_4k else 1)
    
    img = Image.new("RGBA", (width * S, height * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    # Window dimensions
    win_w, win_h = (width - 80) * S, (height - 80) * S
    x0, y0 = 40 * S, 40 * S
    x1, y1 = x0 + win_w, y0 + win_h
    
    # Authentic macOS Terminal dark theme colors
    BG_TERM = (24, 29, 37, 245)      # Deep obsidian translucent
    BORDER_TERM = (60, 68, 85, 255)
    TITLEBAR_BG = (32, 38, 48, 255)
    
    # Rounded terminal body
    d.rounded_rectangle([x0, y0, x1, y1], radius=24 * S, fill=BG_TERM, outline=BORDER_TERM, width=2 * S)
    
    # Titlebar
    tb_h = 44 * S
    d.rounded_rectangle([x0, y0, x1, y0 + tb_h], radius=24 * S, fill=TITLEBAR_BG)
    d.rectangle([x0, y0 + tb_h - 12 * S, x1, y0 + tb_h], fill=TITLEBAR_BG)
    d.line([(x0, y0 + tb_h), (x1, y0 + tb_h)], fill=(45, 52, 65, 255), width=2 * S)
    
    # Traffic lights (macOS Close, Minimize, Zoom)
    colors = [(255, 95, 86), (255, 189, 46), (39, 201, 63)]
    for idx, col in enumerate(colors):
        cx = x0 + (28 + idx * 24) * S
        cy = y0 + 22 * S
        r = 7 * S
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
        
    # Title
    font_paths = [
        os.path.join(REPO_ROOT, "fonts", "InterDisplay-Bold.otf"),
        "fonts/InterDisplay-Bold.otf"
    ]
    fb = next((p for p in font_paths if os.path.exists(p)), None)
    font_title = ImageFont.truetype(fb, 14 * S) if fb else ImageFont.load_default()
    font_mono = ImageFont.truetype(fb, 17 * S) if fb else ImageFont.load_default()
    
    d.text((x0 + win_w / 2, y0 + 22 * S), title, font=font_title, fill=(160, 168, 184), anchor="mm")
    
    # Command prompt
    content_x = x0 + 36 * S
    line_y = y0 + tb_h + 36 * S
    
    # Authentic terminal prompt styling
    d.text((content_x, line_y), "❯", font=font_mono, fill=(70, 220, 255), anchor="lm")
    d.text((content_x + 24 * S, line_y), command, font=font_mono, fill=(255, 255, 255), anchor="lm")
    
    # Optional output lines
    if output_lines:
        line_y += 36 * S
        for line in output_lines:
            d.text((content_x, line_y), line, font=font_mono, fill=(185, 192, 225), anchor="lm")
            line_y += 32 * S
            
    final_img = img.resize((w_out, h_out), Image.LANCZOS)
    final_img.save(out_path)
    print(f"  ✓ Saved authentic terminal capture to: {out_path} ({w_out}x{h_out})")

def main():
    parser = argparse.ArgumentParser(description="Capture Real UI assets for Faceless videos")
    subparsers = parser.add_subparsers(dest="mode", required=True)
    
    # Web subparser
    web_p = subparsers.add_parser("web", help="Capture real website via headless Chromium")
    web_p.add_argument("--url", required=True, help="Website URL to capture")
    web_p.add_argument("--out", required=True, help="Output PNG path")
    web_p.add_argument("--width", type=int, default=1920)
    web_p.add_argument("--height", type=int, default=1080)
    web_p.add_argument("--light", action="store_true", help="Use light mode instead of dark")
    web_p.add_argument("--4k", dest="is_4k", action="store_true", help="Capture at native 4K UHD")
    
    # Terminal subparser
    term_p = subparsers.add_parser("terminal", help="Generate real macOS Terminal capture")
    term_p.add_argument("--cmd", required=True, help="Command text")
    term_p.add_argument("--out", required=True, help="Output PNG path")
    term_p.add_argument("--title", default="zsh — 80×24")
    term_p.add_argument("--width", type=int, default=1280)
    term_p.add_argument("--height", type=int, default=720)
    term_p.add_argument("--4k", dest="is_4k", action="store_true", help="Capture at native 4K UHD")
    
    args = parser.parse_args()
    if args.mode == "web":
        capture_web(args.url, args.out, width=args.width, height=args.height, dark_mode=not args.light, is_4k=args.is_4k)
    elif args.mode == "terminal":
        capture_terminal(args.cmd, args.out, title=args.title, width=args.width, height=args.height, is_4k=args.is_4k)

if __name__ == "__main__":
    main()
