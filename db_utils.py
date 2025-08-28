"""
Database utilities: settings, logger, SQLAlchemy engine/session helpers.

Recommended improvements:
- Add structured JSON logging and per-request context (e.g., campaign_id) when applicable.
- Support multiple databases/environments via profiles; expose pool settings.
- Consider Alembic migrations if schema evolves beyond simple resets.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from contextlib import contextmanager
from typing import Iterator
from rich import print
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models.registry import registry


try:
    from colorlog import ColoredFormatter  # type: ignore
except Exception:
    ColoredFormatter = None  # type: ignore


@dataclass(frozen=True)
class Settings:
    ADS_DB_URL: str = os.getenv("ADS_DB_URL", "sqlite:///./ads.db")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


def get_settings() -> Settings:
    return Settings()


def get_logger(name: str = "ads") -> logging.Logger:
    logger = logging.getLogger(name)
    level_name = os.getenv("LOG_LEVEL", get_settings().LOG_LEVEL).upper()
    level = getattr(logging, level_name, logging.INFO)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        if ColoredFormatter is not None:
            fmt = ColoredFormatter(
                "%(log_color)s%(asctime)s %(levelname)s %(name)s - %(message)s",
                reset=True,
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
            )
        else:
            fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s - %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    return logger


# Database engine and session setup use the configured DB URL
DB_URL = get_settings().ADS_DB_URL
engine = create_engine(DB_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


# def init_db() -> None:
#     with engine.connect() as conn:
#         if DB_URL.startswith("sqlite"):
#             conn.execute(text("PRAGMA foreign_keys=ON"))
#             conn.execute(text("PRAGMA journal_mode=WAL"))
#     # Drop and recreate schemas for both primary models and test models
#     Base.metadata.drop_all(bind=engine)
#     # TestBase.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     # TestBase.metadata.create_all(bind=engine)





def init_db() -> None:
    with engine.connect() as conn:
        if DB_URL.startswith("sqlite"):
            conn.execute(text("PRAGMA foreign_keys=ON"))
            conn.execute(text("PRAGMA journal_mode=WAL"))

    registry.Base.metadata.drop_all(bind=engine)
    registry.Base.metadata.create_all(bind=engine)





def migrate_db() -> None:
    """
    Lightweight, Alembic-style migration shim for SQLite.

    Applies incremental changes without dropping data:
    - Add creatives.checksum column (nullable, TEXT/STRING)
    - Create ix_campaign_status_created index on campaigns(status, created_at)
    - Add new performance metrics columns to campaign_performance table

    Safe to run multiple times (idempotent checks).
    """
    with engine.begin() as conn:
        # 1) Add creatives.checksum if missing
        try:
            cols = [r[1] for r in conn.exec_driver_sql("PRAGMA table_info('creatives')").fetchall()]
            if "checksum" not in cols:
                conn.exec_driver_sql("ALTER TABLE creatives ADD COLUMN checksum TEXT")
        except Exception:
            # Table might not exist yet; skip gracefully
            pass

        # 2) Create composite index on campaigns(status, created_at) if missing
        try:
            idx_rows = conn.exec_driver_sql("PRAGMA index_list('campaigns')").fetchall()
            idx_names = {r[1] for r in idx_rows}  # r[1] = name
            if "ix_campaign_status_created" not in idx_names:
                conn.exec_driver_sql(
                    "CREATE INDEX ix_campaign_status_created ON campaigns(status, created_at)"
                )
        except Exception:
            pass

        # 3) Add new performance metrics columns to campaign_performance if missing
        try:
            perf_cols = [r[1] for r in conn.exec_driver_sql("PRAGMA table_info('campaign_performance')").fetchall()]
            new_columns = [
                ("clicks", "INTEGER NOT NULL DEFAULT 0"),
                ("ctr", "NUMERIC(5,4) NOT NULL DEFAULT 0.0"),
                ("render_rate", "NUMERIC(5,4) NOT NULL DEFAULT 0.0"),
                ("fill_rate", "NUMERIC(5,4) NOT NULL DEFAULT 0.0"),
                ("response_rate", "NUMERIC(5,4) NOT NULL DEFAULT 0.0"),
                ("video_skip_rate", "NUMERIC(5,4) NOT NULL DEFAULT 0.0"),
                ("video_start", "INTEGER NOT NULL DEFAULT 0"),
            ]
            
            for col_name, col_def in new_columns:
                if col_name not in perf_cols:
                    conn.exec_driver_sql(f"ALTER TABLE campaign_performance ADD COLUMN {col_name} {col_def}")
        except Exception:
            # Table might not exist yet; skip gracefully
            pass


@contextmanager
def session_scope() -> Iterator:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# ---------- Helper methods moved from cli.py ----------

def setup_env(log_level: str | None = None, db_url: str | None = None, seed: int | None = None) -> None:
    """Set common environment knobs for CLI commands."""
    if log_level:
        os.environ["LOG_LEVEL"] = log_level
    if db_url:
        os.environ["ADS_DB_URL"] = db_url
    if seed is not None:
        from factories.faker_providers import seed_all as faker_seed_all
        faker_seed_all(seed)


def safe_load_yaml(path: str) -> dict[str, any]:
    """Load a YAML file and ensure the root is a mapping."""
    try:
        import yaml
    except ImportError:
        raise ImportError("PyYAML is required: pip install pyyaml")
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            raise ValueError("YAML root must be a mapping (dict)")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {path}")
    except Exception as e:
        raise Exception(f"Failed to parse YAML: {e}")


def parse_date(value: any) -> str:
    """Coerce either a date or YYYY-MM-DD string into a date object."""
    from datetime import date
    
    if isinstance(value, date):
        return value
    if isinstance(value, str) and len(value.split("-")) == 3:
        try:
            y, m, d = map(int, value.split("-"))
            return date(y, m, d)
        except ValueError:
            pass
    raise ValueError(f"Invalid date: {value!r} (expected YYYY-MM-DD)")


def coerce_creative(c: dict[str, any]) -> any:
    """Convert a loosely-typed creative dict into a CreativeCreate schema."""
    from models.registry import registry
    
    return registry.CreativeCreate(
        asset_url=c.get("asset_url", "https://example.com/ad.mp4"),
        mime_type=c.get("mime_type", "VIDEO/MP4"),
        duration_seconds=int(c.get("duration_seconds", 15)),
    )


def build_auto_campaign(advertiser_id: int | None, profile: str | None) -> any:
    """Build a single demo campaign payload for an advertiser."""
    import random
    from decimal import Decimal
    from models.registry import registry
    from factories.faker_providers import (
        fake_campaign_dates, fake_budget_and_cpm, fake_line_item_name,
        fake_asset, fake_targeting_v2, profile_tuned_cpm, profile_tuned_budget,
        profile_tuned_targeting, make_profile_creative
    )
    
    start, end = fake_campaign_dates()
    
    if profile:
        amount, cpm = profile_tuned_budget(profile), profile_tuned_cpm(profile)
        btype = random.choice([registry.BudgetType.lifetime.value, registry.BudgetType.daily.value])
        targeting, creative = profile_tuned_targeting(profile), make_profile_creative(profile)
        objective = "AWARENESS"
    else:
        amount, btype, cpm = fake_budget_and_cpm()
        targeting = fake_targeting_v2()
        asset_url, mime, dur = fake_asset()
        creative = registry.CreativeCreate(asset_url=asset_url, mime_type=mime, duration_seconds=dur)
        objective = "AWARENESS"

    return registry.CampaignCreate(
        advertiser_id=advertiser_id,
        name=f"Campaign {fake_line_item_name()}",
        objective=objective,
        status="ACTIVE",
        target_cpm=Decimal(str(cpm)),
        dsp_partner="DV360",
        flight=registry.FlightSchema(start_date=start, end_date=end),
        budget=registry.BudgetSchema(amount=Decimal(str(amount)), type=btype, currency="USD"),
        line_items=[registry.LineItemCreate(
            name=fake_line_item_name(),
            ad_format="STANDARD_VIDEO",
            bid_cpm=Decimal(str(cpm)),
            pacing_pct=100,
            targeting=targeting,
            creatives=[creative],
        )],
    )

# db_utils.py (or a new utils module)
from sqlalchemy import insert, text



def persist_advertiser(payload: any) -> int:
    """Get-or-create an advertiser by unique contact_email; return its id."""
    from sqlalchemy import select
    from models.registry import registry
    from services.generator import create_advertiser_payload
    
    with session_scope() as s:
        existing = s.execute(
            select(registry.Advertiser).where(registry.Advertiser.contact_email == payload.contact_email)
        ).scalar_one_or_none()
        
        if existing:
            return existing.id
            
        adv = create_advertiser_payload(payload)
        s.add(adv)
        s.flush()
        s.refresh(adv)
        return adv.id


def persist_campaign(advertiser_id: int | None, payload: any, return_ids: bool = False) -> dict[str, any]:
    """Validate and persist a campaign and its children."""
    import json
    from sqlalchemy import select
    from models.registry import registry
    from services.generator import create_campaign_payload
    from services.validators import validate_campaign_v1
    
    if advertiser_id is None:
        print(json.dumps({"error": "advertiser_id is required"}))
        raise SystemExit(4)
    
    try:
        validate_campaign_v1(payload)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        raise SystemExit(2)

    with session_scope() as s:
        # Verify advertiser exists
        if not s.execute(select(registry.Advertiser).where(registry.Advertiser.id == advertiser_id)).scalar_one_or_none():
            print(json.dumps({"error": f"Advertiser with id {advertiser_id} not found"}))
            raise SystemExit(2)
        
        # Create campaign objects
        camp, flight, budget, freq, line_item, creatives = create_campaign_payload(payload)
        camp.advertiser_id = advertiser_id
        
        # Persist campaign hierarchy
        s.add(camp)
        s.flush()
        
        for obj in [flight, budget, line_item]:
            obj.campaign_id = camp.id
            s.add(obj)
        
        if freq:
            freq.campaign_id = camp.id
            s.add(freq)
        
        s.flush()
        
        # Add creatives
        for cr in creatives:
            s.add(registry.Creative(
                line_item_id=line_item.id,
                asset_url=cr.asset_url,
                mime_type=cr.mime_type,
                duration_seconds=int(cr.duration_seconds),
                qa_status=registry.QAStatus.approved.value,
            ))
        
        s.flush()
        result = {"campaign_id": camp.id, "line_item_id": line_item.id}
        
        if return_ids:
            result["advertiser_id"] = advertiser_id
        
        print(json.dumps(result))
        return result


# def process_from_yaml(path: str, log_level: str | None = None, db_url: str | None = None, 
#                      seed: int | None = None, generate_performance: bool = False) -> None:
#     """Process YAML config file to create entities."""
#     setup_env(log_level, db_url, seed)
#     config = safe_load_yaml(path)
    
#     # Process advertisers
#     for adv_config in config.get("advertisers", []):
#         from models.advertiser import AdvertiserCreate
#         payload = AdvertiserCreate(**adv_config)
#         adv_id = persist_advertiser(payload)
        
#         # Process campaigns for this advertiser
#         for camp_config in adv_config.get("campaigns", []):
#             from models.registry import registry
#             camp_payload = CampaignCreate(**camp_config)
#             result = persist_campaign(adv_id, camp_payload, return_ids=True)
            
#             if generate_performance and "campaign_id" in result:
#                 generate_hourly_performance(result["campaign_id"], seed=seed, replace=True)


def generate_hourly_performance(campaign_id: int, seed: int | None = None, replace: bool = True) -> int:
    """Generate synthetic hourly performance rows for a campaign."""
    from services.performance import generate_hourly_performance as _generate_hourly_performance
    return _generate_hourly_performance(campaign_id, seed=seed, replace=replace)


def generate_performance(campaign_id: int, seed: int | None = None, replace: bool = True) -> dict[str, any]:
    """Generate synthetic hourly performance rows for a campaign and return summary."""
    rows = generate_hourly_performance(campaign_id, seed=seed, replace=replace)
    return {"campaign_id": campaign_id, "rows": rows}


"""
CREATE TABLE advertisers (
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	status VARCHAR(8) DEFAULT 'ACTIVE' NOT NULL CHECK (status IN ('ACTIVE','INACTIVE','DELETED')), 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	brand VARCHAR(255), 
	contact_email VARCHAR(255) NOT NULL, 
	agency_name VARCHAR(255), 
	PRIMARY KEY (id), 
	UNIQUE (contact_email)
);

CREATE TABLE campaigns (
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	status VARCHAR(8) DEFAULT 'ACTIVE' NOT NULL CHECK (status IN ('ACTIVE','INACTIVE','DELETED')), 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	advertiser_id INTEGER NOT NULL, 
	objective VARCHAR(13) NOT NULL CHECK (objective IN ('AWARENESS','CONSIDERATION','CONVERSION')), 
	currency VARCHAR(3) DEFAULT 'USD' NOT NULL CHECK (currency IN ('USD')), 
	target_cpm INTEGER NOT NULL, 
	dsp_partner VARCHAR(14) NOT NULL CHECK (dsp_partner IN ('DV360','GOOGLE_DV360','THE_TRADE_DESK','MAGNITE','MICROSOFT')), 
	programmatic_buy_type VARCHAR(23) CHECK (programmatic_buy_type IN ('DIRECT_GUARANTEED','PROGRAMMATIC_GUARANTEED','PROGRAMMATIC_PREFERRED','PRIVATE_MARKETPLACE')), 
	programmatic_partner VARCHAR(14) CHECK (programmatic_partner IN ('DV360','GOOGLE_DV360','THE_TRADE_DESK','MAGNITE','MICROSOFT')), 
	content_adjacency_tier VARCHAR(6) CHECK (content_adjacency_tier IN ('TIER_1','TIER_2','TIER_3')), 
	brand_lift_enabled INTEGER, 
	attention_metrics_enabled INTEGER, 
	clean_room_provider VARCHAR(9) CHECK (clean_room_provider IN ('SNOWFLAKE','INFOSUM','LIVERAMP')), 
	measurement_partner VARCHAR(18) CHECK (measurement_partner IN ('NIELSEN','KANTAR','LUCID','NCSOLUTIONS','AFFINITY_SOLUTIONS','EDO')), 
	external_ref VARCHAR(64), 
	PRIMARY KEY (id), 
	CONSTRAINT ck_campaign_brand_lift_bool CHECK (brand_lift_enabled IN (0,1) OR brand_lift_enabled IS NULL), 
	CONSTRAINT ck_campaign_attention_bool CHECK (attention_metrics_enabled IN (0,1) OR attention_metrics_enabled IS NULL), 
	FOREIGN KEY(advertiser_id) REFERENCES advertisers (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE line_items (
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	status VARCHAR(8) DEFAULT 'ACTIVE' NOT NULL CHECK (status IN ('ACTIVE','INACTIVE','DELETED')), 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	campaign_id INTEGER NOT NULL, 
	ad_format VARCHAR(19) NOT NULL CHECK (ad_format IN ('STANDARD_VIDEO','INTERACTIVE_OVERLAY','PAUSE_ADS','BINGE_ADS','SPONSORSHIP')), 
	bid_cpm INTEGER NOT NULL, 
	pacing_pct INTEGER NOT NULL, 
	targeting_json TEXT NOT NULL, 
	device_targets_json TEXT, 
	duration_seconds INTEGER, 
	ad_server_type VARCHAR(8) CHECK (ad_server_type IN ('VAST_TAG','DSP_TAG')), 
	pixel_vendor VARCHAR(12) CHECK (pixel_vendor IN ('IAS','DOUBLEVERIFY')), 
	geo_tier VARCHAR(7) CHECK (geo_tier IN ('COUNTRY','REGION','DMA','CITY')), 
	PRIMARY KEY (id), 
	FOREIGN KEY(campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE creatives (
	id INTEGER NOT NULL, 
	name VARCHAR(255), 
	status VARCHAR(8) DEFAULT 'ACTIVE' NOT NULL CHECK (status IN ('ACTIVE','INACTIVE','DELETED')), 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	line_item_id INTEGER NOT NULL, 
	asset_url TEXT NOT NULL, 
	checksum VARCHAR(64), 
	mime_type VARCHAR(15) NOT NULL CHECK (mime_type IN ('VIDEO/MP4','VIDEO/QUICKTIME')), 
	duration_seconds INTEGER NOT NULL, 
	qa_status VARCHAR(8) CHECK (qa_status IN ('PENDING','APPROVED','REJECTED')), 
	placement VARCHAR(8) CHECK (placement IN ('PRE_ROLL','MID_ROLL','LIVE')), 
	file_format VARCHAR(3) CHECK (file_format IN ('MP4','MOV')), 
	width INTEGER, 
	height INTEGER, 
	frame_rate VARCHAR(6) CHECK (frame_rate IN ('23_976','24','25','29_97','30')), 
	frame_rate_mode VARCHAR(8) CHECK (frame_rate_mode IN ('CONSTANT')), 
	aspect_ratio VARCHAR(5) CHECK (aspect_ratio IN ('R16_9')), 
	scan_type VARCHAR(11) CHECK (scan_type IN ('PROGRESSIVE')), 
	video_codec_h264_profile VARCHAR(8) CHECK (video_codec_h264_profile IN ('BASELINE','MAIN','HIGH')), 
	video_codec_prores_profile VARCHAR(13) CHECK (video_codec_prores_profile IN ('PRORES_422_HQ','PRORES_422','PRORES_422_LT')), 
	chroma_subsampling VARCHAR(9) CHECK (chroma_subsampling IN ('YUV_4_2_2','YUV_4_2_0')), 
	color_primaries VARCHAR(6) CHECK (color_primaries IN ('BT_709')), 
	transfer_function VARCHAR(6) CHECK (transfer_function IN ('BT_709')), 
	bitrate_kbps INTEGER, 
	file_size_bytes INTEGER, 
	audio_codec VARCHAR(6) CHECK (audio_codec IN ('PCM','AAC_LC')), 
	audio_channels VARCHAR(12) CHECK (audio_channels IN ('STEREO','SURROUND_5_1')), 
	audio_sample_rate_hz INTEGER, 
	audio_bit_depth INTEGER, 
	safe_zone_ok INTEGER, 
	is_interactive INTEGER, 
	interactive_meta_json TEXT, 
	is_pause_ad INTEGER, 
	qr_code_url TEXT, 
	overlay_cta_text VARCHAR(64), 
	PRIMARY KEY (id), 
	FOREIGN KEY(line_item_id) REFERENCES line_items (id) ON DELETE CASCADE ON UPDATE CASCADE
);

"""