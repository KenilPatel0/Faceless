#!/usr/bin/env python3
"""
capture_code.py — Authentic Real UI Code & Terminal Window Capture Engine.
Renders authentic, pixel-perfect dark mode VS Code and Terminal windows
using Playwright Chromium with real syntax highlighting, line numbers,
genuine macOS/Windows title bars, and glassmorphic drop shadows.

Eliminates synthetic Pillow drawing mockups forever.
"""

import os
import sys
import argparse
import html
from typing import Optional, List, Union, Tuple
import pygments
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter
from playwright.sync_api import sync_playwright

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@500;700&display=swap');

  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: transparent;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  }

  .window {
    width: __WIDTH__px;
    max-width: 95vw;
    background: rgba(16, 20, 30, 0.95);
    backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 16px;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.65), 0 0 1px rgba(255, 255, 255, 0.2);
    overflow: hidden;
  }

  .titlebar {
    height: 44px;
    background: rgba(24, 28, 42, 0.98);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    display: flex;
    align-items: center;
    padding: 0 18px;
    position: relative;
  }

  .traffic-lights {
    display: flex;
    gap: 8px;
  }
  .dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }
  .dot-red { background: #ff5f56; }
  .dot-yellow { background: #ffbd2e; }
  .dot-green { background: #27c93f; }

  .window-title {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    font-size: 13px;
    font-weight: 500;
    color: #94a3b8;
    letter-spacing: 0.3px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .file-badge {
    background: rgba(70, 220, 255, 0.15);
    color: #46dcff;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
  }

  .editor-body {
    padding: 20px 24px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 16px;
    line-height: 1.65;
    color: #e2e8f0;
    overflow-x: auto;
  }

  .split-container {
    display: flex;
    width: 100%;
  }
  .split-pane {
    flex: 1;
    overflow: hidden;
  }
  .split-pane:first-child {
    border-right: 1px solid rgba(255, 255, 255, 0.08);
  }
  .split-header {
    padding: 10px 18px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .split-left-header {
    background: rgba(255, 70, 90, 0.1);
    color: #ff465a;
    border-bottom: 1px solid rgba(255, 70, 90, 0.2);
  }
  .split-right-header {
    background: rgba(90, 235, 150, 0.1);
    color: #5aeb96;
    border-bottom: 1px solid rgba(90, 235, 150, 0.2);
  }

  .terminal-body {
    padding: 20px 24px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 15px;
    line-height: 1.6;
    color: #cbd5e1;
  }
  .term-prompt {
    color: #46dcff;
    font-weight: 700;
    margin-right: 8px;
  }
  .term-cmd {
    color: #ffffff;
    font-weight: 600;
  }
  .term-pass { color: #5aeb96; font-weight: 700; }
  .term-fail { color: #ff465a; font-weight: 700; }
  .term-info { color: #94a3b8; }
  .term-warn { color: #ffbd2e; }

  /* Pygments Token Overrides for Tokyo Night Dark Palette */
  pre { margin: 0; }
  .c, .c1, .ch, .cm { color: #6272a4; font-style: italic; } /* Comment */
  .k, .kd, .kn, .kp, .kr { color: #ff79c6; font-weight: bold; } /* Keyword */
  .s, .s1, .s2, .sa, .sb, .sc, .sd { color: #f1fa8c; } /* String */
  .f, .m, .mf, .mh, .mi, .mo { color: #bd93f9; } /* Number */
  .nf, .fm { color: #50fa7b; font-weight: bold; } /* Function */
  .nc, .nn { color: #8be9fd; } /* Class */
  .nb, .bp { color: #8be9fd; font-style: italic; } /* Builtin */
  .o, .ow { color: #ff79c6; } /* Operator */
  .linenos {
    color: #475569;
    padding-right: 16px;
    user-select: none;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
    margin-right: 16px;
  }
</style>
</head>
<body>
  <div class="window">
    <div class="titlebar">
      <div class="traffic-lights">
        <div class="dot dot-red"></div>
        <div class="dot dot-yellow"></div>
        <div class="dot dot-green"></div>
      </div>
      <div class="window-title">
        <span>__TITLE__</span>
        __BADGE_HTML__
      </div>
    </div>
    __BODY_HTML__
  </div>
</body>
</html>
"""

def highlight_code_snippet(code: str, lang: str = "python", line_numbers: bool = True) -> str:
    """Highlights code using Pygments into clean HTML with Tokyo Night token styling."""
    try:
        lexer = get_lexer_by_name(lang)
    except Exception:
        lexer = TextLexer()
    
    formatter = HtmlFormatter(
        linenos="inline" if line_numbers else False,
        noclasses=False,
        nowrap=True
    )
    return pygments.highlight(code, lexer, formatter)

def render_code_window(
    code_or_file: str,
    out_path: str,
    lang: str = "python",
    title: str = "main.py",
    badge: Optional[str] = None,
    line_numbers: bool = True,
    width: int = 1400,
    viewport_w: int = 1920,
    viewport_h: int = 1080,
    is_4k: bool = False
) -> str:
    """
    Renders an authentic, pixel-perfect VS Code window to high-res PNG.
    """
    if os.path.exists(code_or_file):
        with open(code_or_file, "r", encoding="utf-8") as f:
            code_text = f.read()
    else:
        code_text = code_or_file

    code_html = highlight_code_snippet(code_text, lang=lang, line_numbers=line_numbers)
    body_html = f'<div class="editor-body"><pre><code>{code_html}</code></pre></div>'
    badge_html = f'<span class="file-badge">{html.escape(badge)}</span>' if badge else ""

    rendered_html = HTML_TEMPLATE.replace("__WIDTH__", str(width))
    rendered_html = rendered_html.replace("__TITLE__", html.escape(title))
    rendered_html = rendered_html.replace("__BADGE_HTML__", badge_html)
    rendered_html = rendered_html.replace("__BODY_HTML__", body_html)

    return _render_html_to_png(rendered_html, out_path, viewport_w, viewport_h, is_4k=is_4k)

def render_terminal_window(
    command: str,
    output_lines: List[Union[str, Tuple[str, str]]],
    out_path: str,
    title: str = "Terminal — pytest",
    badge: str = "BASH",
    width: int = 1400,
    viewport_w: int = 1920,
    viewport_h: int = 1080,
    is_4k: bool = False
) -> str:
    """
    Renders an authentic dark mode Terminal window with genuine prompt and formatted output lines.
    """
    body_lines = [
        f'<div><span class="term-prompt">❯</span><span class="term-cmd">{html.escape(command)}</span></div>'
    ]

    for line in output_lines:
        if isinstance(line, tuple):
            text, style = line
            css_cls = f"term-{style}" if style in ["pass", "fail", "info", "warn", "prompt", "cmd"] else "term-info"
            body_lines.append(f'<div class="{css_cls}">{html.escape(text)}</div>')
        else:
            txt = str(line)
            css_cls = "term-info"
            if "PASSED" in txt or "✓" in txt or "passed" in txt:
                css_cls = "term-pass"
            elif "FAILED" in txt or "✗" in txt or "error" in txt.lower():
                css_cls = "term-fail"
            elif txt.startswith("=") or txt.startswith("-"):
                css_cls = "term-info"
            body_lines.append(f'<div class="{css_cls}">{html.escape(txt)}</div>')

    body_html = f'<div class="terminal-body">{"".join(body_lines)}</div>'
    badge_html = f'<span class="file-badge">{html.escape(badge)}</span>' if badge else ""

    rendered_html = HTML_TEMPLATE.replace("__WIDTH__", str(width))
    rendered_html = rendered_html.replace("__TITLE__", html.escape(title))
    rendered_html = rendered_html.replace("__BADGE_HTML__", badge_html)
    rendered_html = rendered_html.replace("__BODY_HTML__", body_html)

    return _render_html_to_png(rendered_html, out_path, viewport_w, viewport_h, is_4k=is_4k)

def render_split_code_window(
    code_left: str,
    title_left: str,
    code_right: str,
    title_right: str,
    out_path: str,
    lang: str = "python",
    title: str = "Split Architecture Comparison",
    width: int = 1680,
    viewport_w: int = 1920,
    viewport_h: int = 1080,
    is_4k: bool = False
) -> str:
    """
    Renders a side-by-side split comparison editor window.
    """
    html_left = highlight_code_snippet(code_left, lang=lang, line_numbers=True)
    html_right = highlight_code_snippet(code_right, lang=lang, line_numbers=True)

    body_html = f"""
    <div class="split-container">
      <div class="split-pane">
        <div class="split-header split-left-header">
          <span>{html.escape(title_left)}</span>
          <span>✗ REJECTED</span>
        </div>
        <div class="editor-body"><pre><code>{html_left}</code></pre></div>
      </div>
      <div class="split-pane">
        <div class="split-header split-right-header">
          <span>{html.escape(title_right)}</span>
          <span>✓ VERIFIED</span>
        </div>
        <div class="editor-body"><pre><code>{html_right}</code></pre></div>
      </div>
    </div>
    """

    rendered_html = HTML_TEMPLATE.replace("__WIDTH__", str(width))
    rendered_html = rendered_html.replace("__TITLE__", html.escape(title))
    rendered_html = rendered_html.replace("__BADGE_HTML__", '<span class="file-badge">COMPARISON</span>')
    rendered_html = rendered_html.replace("__BODY_HTML__", body_html)

    return _render_html_to_png(rendered_html, out_path, viewport_w, viewport_h, is_4k=is_4k)

def _render_html_to_png(html_str: str, out_path: str, vw: int, vh: int, is_4k: bool = False) -> str:
    """Invokes Playwright Chromium to snapshot the transparent DOM to high-res PNG."""
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    
    scale_factor = 2 if is_4k else 1
    actual_vw = 3840 if is_4k else vw
    actual_vh = 2160 if is_4k else vh

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': actual_vw, 'height': actual_vh},
            device_scale_factor=scale_factor
        )
        page = context.new_page()
        page.set_content(html_str, wait_until='networkidle')
        # Target the window element for exact bounds or take full viewport with transparency
        window_elem = page.locator(".window")
        window_elem.screenshot(path=out_path, omit_background=True)
        browser.close()

    return out_path

if __name__ == "__main__":
    test_code = """def validate_email(email: str) -> bool:
    if not isinstance(email, str) or len(email) > 254:
        return False
    parts = email.split('@')
    if len(parts) != 2:
        return False
    return True
"""
    test_out = os.path.join(REPO_ROOT, "tools", "test_code_window.png")
    print("🎨 Rendering Authentic VS Code Window...")
    render_code_window(test_code, test_out, title="clean_validator.py", badge="RFC 5322", width=1280)
    print(f"  ✓ Saved to: {test_out}")

    test_term_out = os.path.join(REPO_ROOT, "tools", "test_term_window.png")
    print("💻 Rendering Authentic Terminal Window...")
    render_terminal_window(
        "pytest -v test_validator.py",
        [
            ("============================= test session starts ==============================", "info"),
            ("collected 7 items", "info"),
            ("test_validator.py::test_standard_email PASSED                            [ 14%]", "pass"),
            ("test_validator.py::test_plus_address PASSED                             [ 28%]", "pass"),
            ("test_validator.py::test_catastrophic_backtracking PASSED                [100%]", "pass"),
            ("============================== 7 passed in 0.14s ===============================", "pass")
        ],
        test_term_out,
        width=1280
    )
    print(f"  ✓ Saved to: {test_term_out}")
