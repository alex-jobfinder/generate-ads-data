from __future__ import annotations

import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, validator


from ..enums import SP_AD_GROUPS_ENUMS


# ------------------------------------------------------------
# Exact DDL for sp_ad_groups (table + enum validation triggers)
# ------------------------------------------------------------
SP_AD_GROUPS_DDL: str = """
CREATE TABLE IF NOT EXISTS sp_ad_groups (
    ad_group_id            TEXT PRIMARY KEY,
    campaign_id            TEXT NOT NULL REFERENCES sp_campaigns(campaign_id) ON DELETE CASCADE,
    account_id             TEXT NOT NULL,

    ad_product             TEXT NOT NULL DEFAULT 'SPONSORED_PRODUCTS' CHECK (ad_product = 'SPONSORED_PRODUCTS'),
    name                   TEXT NOT NULL,

    state                  TEXT NOT NULL CHECK (state IN ('ENABLED','PAUSED','ARCHIVED')),
    delivery_status        TEXT,
    delivery_reasons       TEXT,

    default_bid            REAL,
    bid_currency_code      TEXT,

    creation_datetime      TEXT,
    last_updated_datetime  TEXT,

    extras                 TEXT
);

CREATE INDEX IF NOT EXISTS idx_sp_ad_groups_campaign ON sp_ad_groups(campaign_id);
CREATE INDEX IF NOT EXISTS idx_sp_ad_groups_state    ON sp_ad_groups(state);

DROP TRIGGER IF EXISTS trg_sp_ad_groups_validate_enums_ins;
DROP TRIGGER IF EXISTS trg_sp_ad_groups_validate_enums_upd;

CREATE TRIGGER IF NOT EXISTS trg_sp_ad_groups_validate_enums_ins
BEFORE INSERT ON sp_ad_groups
FOR EACH ROW
BEGIN
    -- ad_product
    SELECT CASE
        WHEN NEW.ad_product IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'ad_product'
              AND enum_value = NEW.ad_product
              AND enum_ad_product = NEW.ad_product
        ) THEN RAISE(ABORT, 'sp_ad_groups.ad_product not in enums_table')
    END;

    -- state
    SELECT CASE
        WHEN NEW.state IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'state'
              AND enum_ad_product = NEW.ad_product
              AND enum_value = NEW.state
        ) THEN RAISE(ABORT, 'sp_ad_groups.state not valid for ad_product')
    END;

    -- delivery_status
    SELECT CASE
        WHEN NEW.delivery_status IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'delivery_status'
              AND enum_ad_product = NEW.ad_product
              AND enum_value = NEW.delivery_status
        ) THEN RAISE(ABORT, 'sp_ad_groups.delivery_status not valid for ad_product')
    END;
END;

CREATE TRIGGER IF NOT EXISTS trg_sp_ad_groups_validate_enums_upd
BEFORE UPDATE ON sp_ad_groups
FOR EACH ROW
BEGIN
    -- ad_product
    SELECT CASE
        WHEN NEW.ad_product IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'ad_product'
              AND enum_value = NEW.ad_product
              AND enum_ad_product = NEW.ad_product
        ) THEN RAISE(ABORT, 'sp_ad_groups.ad_product not in enums_table')
    END;

    -- state
    SELECT CASE
        WHEN NEW.state IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'state'
              AND enum_ad_product = NEW.ad_product
              AND enum_value = NEW.state
        ) THEN RAISE(ABORT, 'sp_ad_groups.state not valid for ad_product')
    END;

    -- delivery_status
    SELECT CASE
        WHEN NEW.delivery_status IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM enums_table
            WHERE enum_name = 'delivery_status'
              AND enum_ad_product = NEW.ad_product
              AND enum_value = NEW.delivery_status
        ) THEN RAISE(ABORT, 'sp_ad_groups.delivery_status not valid for ad_product')
    END;
END;
"""


def utc_now_iso() -> str:
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


class AdGroupSP(BaseModel):
    ad_group_id: str
    campaign_id: str
    account_id: str
    name: str

    # Enums and state
    ad_product: str = Field(default="SPONSORED_PRODUCTS")
    state: str = Field(default="ENABLED")
    delivery_status: Optional[str] = None
    delivery_reasons: Optional[str] = None  # JSON string

    # Bidding
    default_bid: Optional[float] = None
    bid_currency_code: Optional[str] = None

    # Timestamps
    creation_datetime: str = Field(default_factory=utc_now_iso)
    last_updated_datetime: str = Field(default_factory=utc_now_iso)

    # Misc JSON
    extras: Optional[str] = None

    # Pydantic validators to enforce allowed enum values inline
    @validator("ad_product")
    def _validate_ad_product(cls, value: str) -> str:
        allowed = SP_AD_GROUPS_ENUMS["ad_product"]
        if value not in allowed:
            raise ValueError(f"ad_product must be one of {allowed}")
        return value

    @validator("state")
    def _validate_state(cls, value: str) -> str:
        allowed = SP_AD_GROUPS_ENUMS["state"]
        if value not in allowed:
            raise ValueError(f"state must be one of {allowed}")
        return value

    @validator("delivery_status")
    def _validate_delivery_status(cls, value: Optional[str], values) -> Optional[str]:
        if value is None:
            return value
        allowed = SP_AD_GROUPS_ENUMS["delivery_status"]
        if value not in allowed:
            raise ValueError(f"delivery_status must be one of {allowed}")
        return value


__all__ = [
    "AdGroupSP",
    "SP_AD_GROUPS_ENUMS",
    "SP_AD_GROUPS_DDL",
]


