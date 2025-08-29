from __future__ import annotations

import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, validator


from ..enums import SP_ADS_ENUMS


# ------------------------------------------------------------
# Exact DDL for sp_ads (table + enum validation triggers)
# ------------------------------------------------------------
SP_ADS_DDL: str = """
CREATE TABLE IF NOT EXISTS sp_ads (
    ad_id                  TEXT PRIMARY KEY,
    ad_group_id            TEXT NOT NULL REFERENCES sp_ad_groups(ad_group_id) ON DELETE CASCADE,
    campaign_id            TEXT NOT NULL REFERENCES sp_campaigns(campaign_id) ON DELETE CASCADE,
    account_id             TEXT NOT NULL,

    ad_product             TEXT NOT NULL DEFAULT 'SPONSORED_PRODUCTS' CHECK (ad_product = 'SPONSORED_PRODUCTS'),
    ad_type                TEXT NOT NULL DEFAULT 'PRODUCT_AD' CHECK (ad_type = 'PRODUCT_AD'),

    state                  TEXT NOT NULL CHECK (state IN ('ENABLED','PAUSED','ARCHIVED')),
    delivery_status        TEXT,
    delivery_reasons       TEXT,

    creation_datetime      TEXT,
    last_updated_datetime  TEXT,

    ad_version_id          TEXT,
    creative               TEXT,
    creative_headline      TEXT,
    creative_brand_name    TEXT,
    creative_lp_type       TEXT,
    creative_lp_url        TEXT,

    product_id_type        TEXT,
    product_id             TEXT,
    asin                   TEXT,
    sku                    TEXT,

    extras                 TEXT
);
CREATE INDEX IF NOT EXISTS idx_sp_ads_ad_group ON sp_ads(ad_group_id);
CREATE INDEX IF NOT EXISTS idx_sp_ads_campaign ON sp_ads(campaign_id);
CREATE INDEX IF NOT EXISTS idx_sp_ads_state    ON sp_ads(state);

DROP TRIGGER IF EXISTS trg_sp_ads_validate_enums_ins;
DROP TRIGGER IF EXISTS trg_sp_ads_validate_enums_upd;

CREATE TRIGGER IF NOT EXISTS trg_sp_ads_validate_enums_ins
BEFORE INSERT ON sp_ads
FOR EACH ROW
BEGIN
    -- ad_product
    SELECT CASE
        WHEN NEW.ad_product IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'ad_product'
              AND enum_value = NEW.ad_product
              AND enum_ad_product = NEW.ad_product
        ) THEN RAISE(ABORT, 'sp_ads.ad_product not in enums_table')
    END;

    -- ad_type
    SELECT CASE
        WHEN NEW.ad_type IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'ad_type'
              AND enum_ad_product = NEW.ad_product
              AND enum_value = NEW.ad_type
        ) THEN RAISE(ABORT, 'sp_ads.ad_type not valid for ad_product')
    END;

    -- state
    SELECT CASE
        WHEN NEW.state IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'state'
              AND enum_ad_product = NEW.ad_product
              AND enum_value = NEW.state
        ) THEN RAISE(ABORT, 'sp_ads.state not valid for ad_product')
    END;

    -- delivery_status
    SELECT CASE
        WHEN NEW.delivery_status IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'delivery_status'
              AND enum_ad_product = NEW.ad_product
              AND enum_value = NEW.delivery_status
        ) THEN RAISE(ABORT, 'sp_ads.delivery_status not valid for ad_product')
    END;
END;

CREATE TRIGGER IF NOT EXISTS trg_sp_ads_validate_enums_upd
BEFORE UPDATE ON sp_ads
FOR EACH ROW
BEGIN
    -- ad_product
    SELECT CASE
        WHEN NEW.ad_product IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'ad_product'
              AND enum_value = NEW.ad_product
              AND enum_ad_product = NEW.ad_product
        ) THEN RAISE(ABORT, 'sp_ads.ad_product not in enums_table')
    END;

    -- ad_type
    SELECT CASE
        WHEN NEW.ad_type IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'ad_type'
              AND enum_ad_product = NEW.ad_product
              AND enum_value = NEW.ad_type
        ) THEN RAISE(ABORT, 'sp_ads.ad_type not valid for ad_product')
    END;

    -- state
    SELECT CASE
        WHEN NEW.state IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'state'
              AND enum_ad_product = NEW.ad_product
              AND enum_value = NEW.state
        ) THEN RAISE(ABORT, 'sp_ads.state not valid for ad_product')
    END;

    -- delivery_status
    SELECT CASE
        WHEN NEW.delivery_status IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'delivery_status'
              AND enum_ad_product = NEW.ad_product
              AND enum_value = NEW.delivery_status
        ) THEN RAISE(ABORT, 'sp_ads.delivery_status not valid for ad_product')
    END;
END;
"""


def utc_now_iso() -> str:
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


class AdSP(BaseModel):
    ad_id: str
    ad_group_id: str
    campaign_id: str
    account_id: str

    # Enums/state
    ad_product: str = Field(default="SPONSORED_PRODUCTS")
    ad_type: str = Field(default="PRODUCT_AD")
    state: str = Field(default="ENABLED")
    delivery_status: Optional[str] = None
    delivery_reasons: Optional[str] = None

    # Timestamps
    creation_datetime: str = Field(default_factory=utc_now_iso)
    last_updated_datetime: str = Field(default_factory=utc_now_iso)

    # Creative/product
    ad_version_id: Optional[str] = None
    creative: Optional[str] = None
    creative_headline: Optional[str] = None
    creative_brand_name: Optional[str] = None
    creative_lp_type: Optional[str] = None
    creative_lp_url: Optional[str] = None
    product_id_type: Optional[str] = None
    product_id: Optional[str] = None
    asin: Optional[str] = None
    sku: Optional[str] = None

    extras: Optional[str] = None

    # Validators
    @validator("ad_product")
    def _validate_ad_product(cls, value: str) -> str:
        allowed = SP_ADS_ENUMS["ad_product"]
        if value not in allowed:
            raise ValueError(f"ad_product must be one of {allowed}")
        return value

    @validator("ad_type")
    def _validate_ad_type(cls, value: str) -> str:
        allowed = SP_ADS_ENUMS["ad_type"]
        if value not in allowed:
            raise ValueError(f"ad_type must be one of {allowed}")
        return value

    @validator("state")
    def _validate_state(cls, value: str) -> str:
        allowed = SP_ADS_ENUMS["state"]
        if value not in allowed:
            raise ValueError(f"state must be one of {allowed}")
        return value

    @validator("delivery_status")
    def _validate_delivery_status(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        allowed = SP_ADS_ENUMS["delivery_status"]
        if value not in allowed:
            raise ValueError(f"delivery_status must be one of {allowed}")
        return value

    @validator("product_id_type")
    def _validate_product_id_type(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        allowed = SP_ADS_ENUMS["product_id_type"]
        if value not in allowed:
            raise ValueError(f"product_id_type must be one of {allowed}")
        return value


__all__ = [
    "AdSP",
    "SP_ADS_ENUMS",
    "SP_ADS_DDL",
]


