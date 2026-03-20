from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class WhiteLabelConfig:
    agency_id: str
    custom_domain: str
    brand_logo_url: str
    brand_colors: dict[str, str]
    custom_email_from: str
    hide_forge_branding: bool = True


def apply_white_label(config: WhiteLabelConfig) -> dict[str, str | bool | dict[str, str]]:
    return {
        "agency_id": config.agency_id,
        "domain": config.custom_domain,
        "logo": config.brand_logo_url,
        "brand_colors": config.brand_colors,
        "email_from": config.custom_email_from,
        "hide_forge_branding": config.hide_forge_branding,
    }
