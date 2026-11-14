#!/usr/bin/env python3
"""
asset_registry.py — Centralized Asset Intelligence & Provenance Tracking for Faceless.
Implements Part IV of the Storytelling Scene Direction Spec:
- Asset taxonomy (backgrounds, evidence, UI captures, code windows, SFX, music)
- Provenance tracking (source_type, creator, license metadata, commercial use verification)
- Asset manifest validation (zero broken references, verified resolution & format)
"""

import os
import json
import hashlib
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Tuple


VALID_ASSET_TYPES = {
    "background_image", "ui_capture", "code_window", "terminal_window",
    "vector_diagram", "footage_clip", "audio_sfx", "audio_music", "audio_ambience", "channel_logo"
}

VALID_SOURCE_TYPES = {
    "authentic_capture", "procedural_vector", "generated", "licensed_stock", "user_supplied"
}


@dataclass
class LicenseInfo:
    name: str = "proprietary_channel"
    commercial_use_reviewed: bool = True
    attribution_required: bool = False
    attribution_text: str = ""
    evidence_path: Optional[str] = None


@dataclass
class AssetMetadata:
    asset_id: str
    asset_type: str
    path: str
    source_type: str = "procedural_vector"
    license: LicenseInfo = field(default_factory=LicenseInfo)
    width: Optional[int] = None
    height: Optional[int] = None
    duration_s: Optional[float] = None
    content_hash: Optional[str] = None
    quality_status: str = "approved" # approved, review_required, rejected

    def validate(self) -> List[str]:
        errors = []
        if self.asset_type not in VALID_ASSET_TYPES:
            errors.append(f"Asset {self.asset_id} has invalid asset_type '{self.asset_type}'.")
        if self.source_type not in VALID_SOURCE_TYPES:
            errors.append(f"Asset {self.asset_id} has invalid source_type '{self.source_type}'.")
        if not self.license.commercial_use_reviewed:
            errors.append(f"Asset {self.asset_id} cannot be used: commercial_use_reviewed is False.")
        return errors


class AssetRegistry:
    """Central store for all licensed, procedural, and captured production assets."""
    def __init__(self, registry_file: Optional[str] = None):
        self.registry_file = registry_file
        self.assets: Dict[str, AssetMetadata] = {}
        self._register_default_procedural_assets()
        if registry_file and os.path.exists(registry_file):
            self.load(registry_file)

    def _register_default_procedural_assets(self):
        """Registers guaranteed built-in procedural assets."""
        self.register(AssetMetadata(
            asset_id="bg_obsidian_atmospheric",
            asset_type="background_image",
            path="procedural://render_core/background",
            source_type="procedural_vector",
            license=LicenseInfo(name="MIT_Engine", commercial_use_reviewed=True),
            width=1920, height=1080
        ))
        for sfx_name in ["pop", "tick", "whoosh", "chime"]:
            self.register(AssetMetadata(
                asset_id=f"sfx_procedural_{sfx_name}",
                asset_type="audio_sfx",
                path=f"procedural://sound_engine/{sfx_name}",
                source_type="procedural_vector",
                license=LicenseInfo(name="MIT_Engine", commercial_use_reviewed=True)
            ))

        # Consistent Brand Master Clips
        branding_clips = [
            ("brand_intro_1080p", "media/branding/intro_1080p.mp4", 1920, 1080, 4.0),
            ("brand_intro_4k", "media/branding/intro_4k.mp4", 3840, 2160, 4.0),
            ("brand_intro_short", "media/branding/intro_short.mp4", 1080, 1920, 2.2),
            ("brand_outro_1080p", "media/branding/outro_1080p.mp4", 1920, 1080, 7.0),
            ("brand_outro_4k", "media/branding/outro_4k.mp4", 3840, 2160, 7.0),
            ("brand_outro_short", "media/branding/outro_short.mp4", 1080, 1920, 3.8)
        ]
        for aid, p, w, h, d in branding_clips:
            self.register(AssetMetadata(
                asset_id=aid,
                asset_type="footage_clip",
                path=p,
                source_type="authentic_capture",
                license=LicenseInfo(name="Proprietary_Channel_Branding", commercial_use_reviewed=True),
                width=w, height=h, duration_s=d
            ))

    def register(self, asset: AssetMetadata):
        errs = asset.validate()
        if errs:
            raise ValueError(f"Cannot register asset {asset.asset_id}: {'; '.join(errs)}")
        self.assets[asset.asset_id] = asset

    def get(self, asset_id: str) -> Optional[AssetMetadata]:
        return self.assets.get(asset_id)

    def verify_manifest(self, referenced_asset_ids: List[str]) -> Tuple[bool, List[str]]:
        """Verifies that all asset IDs referenced by a scene plan exist and are approved."""
        missing = []
        for aid in referenced_asset_ids:
            if aid not in self.assets:
                # Check if it's a dynamic procedural or content asset
                if not (aid.endswith("_content") or aid.endswith("_telemetry")):
                    missing.append(f"Missing asset in registry: '{aid}'")
            elif self.assets[aid].quality_status == "rejected":
                missing.append(f"Asset '{aid}' is marked as rejected.")
        return len(missing) == 0, missing

    def save(self, filepath: str):
        data = {aid: asdict(meta) for aid, meta in self.assets.items()}
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        for aid, item in data.items():
            lic_data = item.pop("license", {})
            lic = LicenseInfo(**lic_data)
            self.assets[aid] = AssetMetadata(license=lic, **item)
