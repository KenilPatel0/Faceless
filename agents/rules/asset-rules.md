# Asset Intelligence & Provenance Rules

## Rule 1: Zero Fake Evidence
1. Never generate synthetic mockups of operating systems, developer tools (VS Code, Terminal), or web applications using basic canvas rectangles.
2. All code snippets and command lines must be rendered into authentic VS Code or Terminal dark-mode windows using Chromium (`tools/capture_code.py`).
3. Real web pages, GitHub repositories, and benchmarks must be captured via Playwright or authentic browser recordings.

## Rule 2: Asset Taxonomy & Provenance
1. Every asset used in a production must be registered in `AssetRegistry` (`tools/asset_registry.py`) with a verified `asset_type` and `source_type`.
2. Sourced media must record author, license name, source URL, and commercial use verification.
3. Every video project using Creative Commons or stock media must generate `license_log.json` and `attribution.txt`.

## Rule 3: 40% Originality Cap on Stock
1. Free stock footage (Pexels, Pixabay) must NEVER exceed $40\%$ of video runtime.
2. Every video requires primary original elements (creator screen recording, genuine diagram, or custom vector animation).
3. Stock media is strictly illustrative/atmospheric; never present stock actors or offices as real evidence of claims.
