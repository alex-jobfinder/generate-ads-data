from __future__ import annotations

import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, validator


from ..enums import SP_TARGETS_ENUMS


# ------------------------------------------------------------
# Exact DDL for sp_targets (table + enum validation triggers)
# ------------------------------------------------------------
SP_TARGETS_DDL: str = """
CREATE TABLE IF NOT EXISTS sp_targets (
    target_id                TEXT PRIMARY KEY,
    ad_group_id              TEXT NOT NULL REFERENCES sp_ad_groups(ad_group_id) ON DELETE CASCADE,
    campaign_id              TEXT NOT NULL REFERENCES sp_campaigns(campaign_id) ON DELETE CASCADE,
    account_id               TEXT NOT NULL,

    ad_product               TEXT NOT NULL DEFAULT 'SPONSORED_PRODUCTS' CHECK (ad_product = 'SPONSORED_PRODUCTS'),

    state                    TEXT NOT NULL CHECK (state IN ('ENABLED','PAUSED','ARCHIVED')),
    negative                 INTEGER CHECK (negative IN (0,1)),

    delivery_status          TEXT,
    delivery_reasons         TEXT,

    creation_datetime        TEXT,
    last_updated_datetime    TEXT,

    bid_amount               REAL,
    bid_currency_code        TEXT,

    target_type              TEXT,
    match_type               TEXT,
    keyword_text             TEXT,
    native_language_keyword  TEXT,
    native_language_locale   TEXT,

    expression               TEXT,
    resolved_expression      TEXT,

    product_category_id       TEXT,
    product_category_resolved TEXT,
    product_brand             TEXT,
    product_brand_resolved    TEXT,
    product_genre             TEXT,
    product_genre_resolved    TEXT,
    price_less_than           REAL,
    price_greater_than        REAL,
    rating_less_than          REAL,
    rating_greater_than       REAL,
    age_range                 TEXT,
    age_range_resolved        TEXT,
    prime_shipping_eligible   INTEGER CHECK (prime_shipping_eligible IN (0,1)),
    asin                      TEXT,
    event_type                TEXT,
    lookback_days             INTEGER,
    audience_id               TEXT,

    extras                   TEXT
);
CREATE INDEX IF NOT EXISTS idx_sp_targets_ad_group  ON sp_targets(ad_group_id);
CREATE INDEX IF NOT EXISTS idx_sp_targets_campaign  ON sp_targets(campaign_id);
CREATE INDEX IF NOT EXISTS idx_sp_targets_state     ON sp_targets(state);
CREATE INDEX IF NOT EXISTS idx_sp_targets_matchtype ON sp_targets(match_type);

DROP TRIGGER IF EXISTS trg_sp_targets_validate_enums_ins;
DROP TRIGGER IF EXISTS trg_sp_targets_validate_enums_upd;

CREATE TRIGGER IF NOT EXISTS trg_sp_targets_validate_enums_ins
BEFORE INSERT ON sp_targets
FOR EACH ROW
BEGIN
    -- ad_product
    SELECT CASE
        WHEN NEW.ad_product IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'ad_product'
              AND enum_value = NEW.ad_product
              AND enum_ad_product = NEW.ad_product
        ) THEN RAISE(ABORT, 'sp_targets.ad_product not in enums_table')
    END;

    -- state
    SELECT CASE
        WHEN NEW.state IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'state'
              AND enum_ad_product = NEW.ad_product
              AND enum_value = NEW.state
        ) THEN RAISE(ABORT, 'sp_targets.state not valid for ad_product')
    END;

    -- delivery_status
    SELECT CASE
        WHEN NEW.delivery_status IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'delivery_status'
              AND enum_ad_product = NEW.ad_product
              AND enum_value = NEW.delivery_status
        ) THEN RAISE(ABORT, 'sp_targets.delivery_status not valid for ad_product')
    END;

    -- target_type
    SELECT CASE
        WHEN NEW.target_type IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'target_type'
              AND enum_ad_product = NEW.ad_product
              AND enum_value = NEW.target_type
        ) THEN RAISE(ABORT, 'sp_targets.target_type not valid for ad_product')
    END;

    -- match_type
    SELECT CASE
        WHEN NEW.match_type IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'match_type'
              AND enum_ad_product = NEW.ad_product
              AND enum_value = NEW.match_type
        ) THEN RAISE(ABORT, 'sp_targets.match_type not valid for ad_product')
    END;
END;

CREATE TRIGGER IF NOT EXISTS trg_sp_targets_validate_enums_upd
BEFORE UPDATE ON sp_targets
FOR EACH ROW
BEGIN
    -- ad_product
    SELECT CASE
        WHEN NEW.ad_product IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'ad_product'
              AND enum_value = NEW.ad_product
              AND enum_ad_product = NEW.ad_product
        ) THEN RAISE(ABORT, 'sp_targets.ad_product not in enums_table')
    END;

    -- state
    SELECT CASE
        WHEN NEW.state IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'state'
              AND enum_ad_product = NEW.ad_product
              AND enum_value = NEW.state
        ) THEN RAISE(ABORT, 'sp_targets.state not valid for ad_product')
    END;

    -- delivery_status
    SELECT CASE
        WHEN NEW.delivery_status IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'delivery_status'
              AND enum_ad_product = NEW.ad_product
              AND enum_value = NEW.delivery_status
        ) THEN RAISE(ABORT, 'sp_targets.delivery_status not valid for ad_product')
    END;

    -- target_type
    SELECT CASE
        WHEN NEW.target_type IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'target_type'
              AND enum_ad_product = NEW.ad_product
              AND enum_value = NEW.target_type
        ) THEN RAISE(ABORT, 'sp_targets.target_type not valid for ad_product')
    END;

    -- match_type
    SELECT CASE
        WHEN NEW.match_type IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'match_type'
              AND enum_ad_product = NEW.ad_product
              AND enum_value = NEW.match_type
        ) THEN RAISE(ABORT, 'sp_targets.match_type not valid for ad_product')
    END;
END;
"""


def utc_now_iso() -> str:
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


class TargetSP(BaseModel):
    target_id: str
    ad_group_id: str
    campaign_id: str
    account_id: str

    # Enums/state
    ad_product: str = Field(default="SPONSORED_PRODUCTS")
    state: str = Field(default="ENABLED")
    delivery_status: Optional[str] = None
    delivery_reasons: Optional[str] = None
    negative: Optional[int] = None

    # Timestamps
    creation_datetime: str = Field(default_factory=utc_now_iso)
    last_updated_datetime: str = Field(default_factory=utc_now_iso)

    # Bids/Targeting
    bid_amount: Optional[float] = None
    bid_currency_code: Optional[str] = None
    target_type: Optional[str] = None
    match_type: Optional[str] = None
    keyword_text: Optional[str] = None
    native_language_keyword: Optional[str] = None
    native_language_locale: Optional[str] = None

    # Expressions and attributes
    expression: Optional[str] = None
    resolved_expression: Optional[str] = None
    product_category_id: Optional[str] = None
    product_category_resolved: Optional[str] = None
    product_brand: Optional[str] = None
    product_brand_resolved: Optional[str] = None
    product_genre: Optional[str] = None
    product_genre_resolved: Optional[str] = None
    price_less_than: Optional[float] = None
    price_greater_than: Optional[float] = None
    rating_less_than: Optional[float] = None
    rating_greater_than: Optional[float] = None
    age_range: Optional[str] = None
    age_range_resolved: Optional[str] = None
    prime_shipping_eligible: Optional[int] = None
    asin: Optional[str] = None
    event_type: Optional[str] = None
    lookback_days: Optional[int] = None
    audience_id: Optional[str] = None

    extras: Optional[str] = None

    # Validators
    @validator("ad_product")
    def _validate_ad_product(cls, value: str) -> str:
        allowed = SP_TARGETS_ENUMS["ad_product"]
        if value not in allowed:
            raise ValueError(f"ad_product must be one of {allowed}")
        return value

    @validator("state")
    def _validate_state(cls, value: str) -> str:
        allowed = SP_TARGETS_ENUMS["state"]
        if value not in allowed:
            raise ValueError(f"state must be one of {allowed}")
        return value

    @validator("delivery_status")
    def _validate_delivery_status(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        allowed = SP_TARGETS_ENUMS["delivery_status"]
        if value not in allowed:
            raise ValueError(f"delivery_status must be one of {allowed}")
        return value

    @validator("target_type")
    def _validate_target_type(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        allowed = SP_TARGETS_ENUMS["target_type"]
        if value not in allowed:
            raise ValueError(f"target_type must be one of {allowed}")
        return value

    @validator("match_type")
    def _validate_match_type(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        allowed = SP_TARGETS_ENUMS["match_type"]
        if value not in allowed:
            raise ValueError(f"match_type must be one of {allowed}")
        return value


__all__ = [
    "TargetSP",
    "SP_TARGETS_ENUMS",
    "SP_TARGETS_DDL",
]


