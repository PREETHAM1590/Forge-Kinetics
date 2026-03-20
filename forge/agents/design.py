from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DesignAgent:
    async def extract_spec_from_screenshot(self, image_bytes: bytes) -> dict:
        _ = image_bytes
        return {
            "spec": "layout:grid; spacing:8px; colors:#facc15,#1d4ed8,#111827",
            "pass": 1,
        }

    async def build_from_spec(self, spec: dict) -> str:
        return f"Built UI from spec: {spec.get('spec', '')}"

    async def visual_verify(self, original_image: bytes, rendered_url: str) -> float:
        _ = original_image
        _ = rendered_url
        return 0.88
