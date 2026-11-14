---
name: asset-director
description: Discovers, selects, validates, and manages media assets, provenance metadata, commercial rights, and real UI captures.
---

# Asset Director Skill

The Asset Director is responsible for the discovery, selection, provenance tracking, and licensing verification of all visual and sonic assets used in Faceless productions.

## 1. Core Principles
1. **Zero Fake Evidence**: Never draw synthetic Pillow mockups of real websites, terminals, or developer tools. Use Playwright (`recordVideo` / Chromium snapshot) for authentic UI captures.
2. **Asset Taxonomy Compliance**: Every asset must be categorized into one of:
   - `background_image`: Atmospheric obsidian backgrounds and textured canvases.
   - `ui_capture`: Real screen recordings and browser/app captures.
   - `code_window` / `terminal_window`: Dark-mode VS Code and terminal windows.
   - `vector_diagram`: Modular geometric, architectural, and data flow nodes.
   - `footage_clip`: Real-world b-roll and authentic footage.
   - `audio_sfx` / `audio_music` / `audio_ambience`: Sound effects and background tracks.
3. **Asset Sourcing Hierarchy**:
   1. Creator's own capture or authentic screen recording (`tools/capture_ui.py`, `tools/capture_code.py`).
   2. Procedural vector diagrams and code animations.
   3. Public domain (NASA, Wikimedia Commons, Open Source repositories).
   4. Licensed free stock (Pexels, Pixabay) with strict 40% originality cap.
4. **Mandatory Provenance Tracking**:
   - Every asset must have an entry in `AssetRegistry` (`tools/asset_registry.py`).
   - Sourced assets must record `source_url`, `creator`, license terms, and commercial use verification.
   - Generate `license_log.json` and `attribution.txt` for all CC BY or stock media.
