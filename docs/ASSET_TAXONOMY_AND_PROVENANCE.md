# Asset Taxonomy & Provenance Tracking

## Centralized Asset Management
All media assets in Faceless are tracked with structured metadata and licensing information in `AssetRegistry` (`tools/asset_registry.py`).

## Provenance Fields
- `asset_id`: Unique identifier (e.g. `bg_tech_obsidian_01`, `code_window_transformer_01`).
- `asset_type`: One of 10 valid asset categories.
- `source_type`: `authentic_capture`, `procedural_vector`, `generated`, or `licensed_stock`.
- `license`:
  - `name`: License type (e.g. `MIT`, `CC0`, `Pexels License`, `Proprietary`).
  - `commercial_use_reviewed`: Boolean confirming commercial rights.
  - `attribution_required`: Boolean.
  - `attribution_text`: Exact text to include in video description.
  - `evidence_path`: Local path to license certificate or snapshot.

## Zero Fake Evidence Policy
Synthetic mockups of real software, web pages, or terminals created with basic rectangles are strictly forbidden. Authentic screen captures or Chromium snapshots via `tools/capture_code.py` must be used.
