from __future__ import annotations

from decimal import Decimal
import pytest

from models.enums import AdFormat, TargetingKey, CreativeMimeType
from models.registry import registry


def test_adformat_enum_includes_v2_values() -> None:
    assert AdFormat.binge_ads.value == "BINGE_ADS"
    assert AdFormat.pause_ads.value == "PAUSE_ADS"
    assert AdFormat.interactive_overlay.value == "INTERACTIVE_OVERLAY"
    assert AdFormat.sponsorship.value == "SPONSORSHIP"
    assert AdFormat.standard_video.value == "STANDARD_VIDEO"


def test_line_item_targeting_whitelist_accepts_known_keys() -> None:
    li = registry.LineItemCreate(
        name="LI V2",
        ad_format=AdFormat.standard_video,
        bid_cpm=Decimal("50.00"),
        pacing_pct=100,
        targeting={
            TargetingKey.DEVICE.value: ["TV"],
            TargetingKey.GEO_COUNTRY.value: ["US"],
            TargetingKey.CONTENT_GENRE.value: ["DRAMA"],
            TargetingKey.AGE_RANGE.value: [25, 34],
            TargetingKey.GENDER.value: "ALL",
            TargetingKey.HOUSEHOLD_INCOME.value: "MID",
        },
        creatives=[registry.CreativeCreate(asset_url="https://example.com/ad.mp4", mime_type=CreativeMimeType.mp4, duration_seconds=15)],
    )
    assert li.targeting[TargetingKey.DEVICE.value] == ["TV"]


def test_line_item_targeting_whitelist_rejects_unknown_keys() -> None:
    with pytest.raises(ValueError):
        registry.LineItemCreate(
            name="LI Bad",
            ad_format=AdFormat.standard_video,
            bid_cpm=Decimal("55.00"),
            pacing_pct=100,
            targeting={"unknown_key": True},
            creatives=[registry.CreativeCreate(asset_url="https://example.com/ad.mp4", mime_type=CreativeMimeType.mp4, duration_seconds=15)],
        )


