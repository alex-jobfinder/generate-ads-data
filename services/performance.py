"""
Basic performance generation utilities - RAW DATA ONLY.

This module generates only raw performance metrics without any calculated fields.
All derived metrics (rates, percentages) are computed elsewhere using Pydantic models.

Modeled effects (inspired by jafgen):
- Hour-of-day: Gaussian uplift during 09:00–17:00, peaking at 13:00.
- Day-of-week: Weekends less busy than weekdays (Fri 0.97, Sat 0.88, Sun 0.92).
- Flight ramp: Logistic S-curve (~0.85→1.15) with mild weekly undulation.
- Annual seasonality: Cosine by day-of-year (~0.8→1.0) for gentle yearly swings.

Public API
- generate_hourly_performance_raw(campaign_id, seed=None, replace=True) -> int
  Creates one row per hour (UTC boundary) across the campaign flight in
  `CampaignPerformance` with ONLY raw data. No calculated fields are generated.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import math
from random import Random
from typing import Iterable

from sqlalchemy import select, delete

from db_utils import session_scope
from models.registry import registry
from services.performance_utils import (
    get_campaign_and_flight,
    clear_existing_performance,
    batch_insert_performance,
    create_performance_row
)
import json


#!/usr/bin/env python3
"""
Create DataFrame with 24 hours of timestamp data
One row per second for the last 24 hours
"""

# import pandas as pd
# from datetime import datetime, timedelta

# """
# CREATE TABLE timestamp_data (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     unix_timestamp INTEGER NOT NULL,
#     human_readable TEXT NOT NULL,
#     hour_of_day INTEGER NOT NULL,
#     minute_of_hour INTEGER NOT NULL,
#     second_of_minute INTEGER NOT NULL,
#     day_of_week INTEGER NOT NULL,
#     is_business_hour BOOLEAN NOT NULL,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP
# );
# """

# class TimestampDataGenerator:
#     """Generate 24 hours of timestamp data as a DataFrame"""
    
#     def __init__(self):
#         self.df = None
    
#     def generate_data(self, hours_back=24):
#         """Generate timestamp data for the specified number of hours back"""
#         # Calculate start time
#         now = datetime.now()
#         start_time = now - timedelta(hours=hours_back)
        
#         # Generate timestamps
#         timestamps = []
#         current_time = start_time
        
#         while current_time <= now:
#             timestamps.append(current_time)
#             current_time += timedelta(seconds=1)
        
#         # Create DataFrame
#         self.df = pd.DataFrame({
#             'unix_timestamp': [int(ts.timestamp()) for ts in timestamps],
#             'human_readable': [ts.strftime('%Y-%m-%d %H:%M:%S') for ts in timestamps],
#             'hour_of_day': [ts.hour for ts in timestamps],
#             'minute_of_hour': [ts.minute for ts in timestamps],
#             'second_of_minute': [ts.second for ts in timestamps],
#             'day_of_week': [ts.weekday() for ts in timestamps],  # 0=Monday, 6=Sunday
#             'is_business_hour': [
#                 (ts.weekday() < 5 and 9 <= ts.hour < 17)  # Mon-Fri, 9 AM - 5 PM
#                 for ts in timestamps
#             ]
#         })
        
#         return self.df

class TimestampDataGenerator:
    """Generate temporal factors for performance data generation."""
    
    def __init__(self):
        pass
    
    def hourly_boost(self, dt: datetime) -> float:
        """Return a multiplicative uplift factor for the given hour.

        Uses a Gaussian centered at 13:00 with sigma=2.5 between 9:00 and 17:00,
        yielding a maximum uplift of ~1.5 at the peak and tapering near edges.
        Outside that window, returns 1.0 (no boost).
        """
        hour = dt.hour
        if 9 <= hour <= 17:
            mu = 13.0
            sigma = 2.5
            x = (hour - mu) / sigma
            g = math.exp(-0.5 * x * x)
            return 1.0 + 0.45 * g
        return 1.0
    
    def dow_factor(self, dt: datetime) -> float:
        """Day-of-week multiplier: weekends slightly less busy than weekdays.

        Mon..Thu ~ 1.00, Fri 0.97, Sat 0.88, Sun 0.92
        """
        wd = dt.weekday()  # Mon=0 .. Sun=6
        if wd == 4:  # Fri
            return 0.97
        if wd == 5:  # Sat
            return 0.88
        if wd == 6:  # Sun
            return 0.92
        return 1.00
    
    def ramp_factor(self, start_dt: datetime, current_dt: datetime, end_dt: datetime) -> float:
        """Smooth ramp over the flight to emulate 'store openings' or audience growth.

        Uses a logistic-like S-curve scaled to ~[0.85, 1.15] across the flight,
        with slight weekly undulation to mimic weekly cycles.
        """
        total_hours = max(1.0, (end_dt - start_dt).total_seconds() / 3600.0)
        t = min(1.0, max(0.0, (current_dt - start_dt).total_seconds() / 3600.0 / total_hours))
        # Logistic-ish curve centered at mid-flight
        x = (t - 0.5) * 6.0
        s = 1.0 / (1.0 + math.exp(-x))  # 0..1
        ramp = 0.85 + 0.30 * s          # 0.85..1.15
        # Mild weekly undulation (period ~168 hours)
        weekly = 1.0 + 0.03 * math.sin(2.0 * math.pi * (current_dt - start_dt).total_seconds() / (168.0 * 3600.0))
        return ramp * weekly
    
    def annual_factor(self, dt: datetime) -> float:
        """Annual seasonality factor similar to jafgen's AnnualCurve.

        Cosine over day-of-year scaled to roughly [0.8, 1.0].
        """
        # Day of year in [1..366]; use 365 as baseline period
        yday = dt.timetuple().tm_yday
        x = 2.0 * math.pi * (yday - 1) / 365.0
        return (math.cos(x) + 1.0) / 10.0 + 0.8
    
    def calculate_temporal_factor(self, start_dt: datetime, current_dt: datetime, end_dt: datetime) -> float:
        """Calculate combined temporal factor from all components."""
        hod_factor = self.hourly_boost(current_dt)
        dow_factor = self.dow_factor(current_dt)
        ramp_factor = self.ramp_factor(start_dt, current_dt, end_dt)
        annual_factor = self.annual_factor(current_dt)
        
        return hod_factor * dow_factor * ramp_factor * annual_factor


def _hours_between(start_dt: datetime, end_dt: datetime) -> Iterable[datetime]:
    """Yield hourly timestamps inclusive between start_dt and end_dt.

    - Timestamps are assumed to be timezone-aware and aligned by caller.
    - End is inclusive because hourly reporting typically includes the
      terminal hour for same-day flights.
    """
    current = start_dt
    while current <= end_dt:
        yield current
        current = current + timedelta(hours=1)


def generate_hourly_performance_raw(campaign_id: int, seed: int | None = None, replace: bool = True) -> int:
    """Generate hourly performance for a campaign across its flight window.

    This function generates ONLY raw data - no calculated fields like CTR, rates, etc.
    All derived metrics should be computed using Pydantic models elsewhere.

    Behavior:
    - Creates one row per hour between flight start and end (inclusive).
    - Stores `hour_ts` as UTC hour boundary.
    - Generates raw counts and values only.
    - Impressions and related metrics are boosted using temporal factors.

    Args:
        campaign_id: Target campaign identifier to generate data for.
        seed: Optional RNG seed to make results reproducible.
        replace: If True, delete prior rows for the campaign before insert.

    Returns:
        Count of rows written for this campaign.
    """
    rng = Random(seed)
    timestamp_generator = TimestampDataGenerator()
    
    with session_scope() as s:
        # Get campaign and flight data using shared utility
        camp, flight = get_campaign_and_flight(s, campaign_id)
        if camp is None or flight is None:
            return 0

        # Align bounds to whole hours in UTC. Start at 00:00, end at last full hour.
        start_dt = datetime.combine(flight.start_date, datetime.min.time(), tzinfo=timezone.utc)
        end_dt = datetime.combine(flight.end_date, datetime.max.time(), tzinfo=timezone.utc).replace(minute=0, second=0, microsecond=0)

        if replace:
            # Clear any previous synthetic rows for idempotent re-generation.
            clear_existing_performance(s, registry.CampaignPerformance, campaign_id)

        rows = 0
        all_rows = []  # Collect all rows for batch insert
        for hour in _hours_between(start_dt, end_dt):
            # Calculate temporal factors using the generator
            factor = timestamp_generator.calculate_temporal_factor(start_dt, hour, end_dt)

            # ===== RAW DATA GENERATION ONLY =====
            # Base draws provide variability, then scale by combined factor.
            base_impressions = rng.randint(1000, 10000)
            impressions = int(max(1, base_impressions * factor))

            # Generate raw click count (not CTR)
            base_ctr = rng.uniform(0.001, 0.02)  # 0.1% to 2%
            ctr_variance = rng.uniform(0.8, 1.2)  # ±20% variation
            raw_ctr = min(0.05, max(0.0001, base_ctr * ctr_variance * factor))  # Cap at 5%
            clicks = max(0, int(impressions * raw_ctr))

            # Generate raw completion count (not rate)
            base_completion = rng.randint(70, 98)
            completion_bump = int(4 * min(1.0, max(0.0, factor - 1.0)))
            completion_count = min(98, base_completion + completion_bump)

            # Generate raw render count (not rate)
            base_render = rng.uniform(0.95, 0.99)
            render_factor = min(0.999, max(0.90, base_render * factor))
            render_count = int(impressions * render_factor)

            # Generate raw fill count (not rate)
            base_fill = rng.uniform(0.85, 0.98)
            fill_factor = min(0.999, max(0.80, base_fill * factor))
            fill_count = int(impressions * fill_factor)

            # Generate raw response count (not rate)
            base_response = rng.uniform(0.01, 0.05)
            response_factor = min(0.10, max(0.001, base_response * factor))
            response_count = int(impressions * response_factor)

            # Generate raw video skip count (not rate)
            base_skip = rng.uniform(0.10, 0.40)
            skip_factor = min(0.60, max(0.05, base_skip * (2.0 - factor)))  # Better performance = lower skip rate
            skips = int(impressions * skip_factor)

            # Generate raw video start count (not rate)
            base_start_rate = rng.uniform(0.80, 0.95)
            start_factor = min(0.99, max(0.70, base_start_rate * factor))
            video_start = max(0, int(impressions * start_factor))

            # Generate raw frequency and reach
            base_frequency = rng.randint(1, 4)
            frequency = max(1, min(5, int(round(base_frequency * (1.0 + 0.15 * max(0.0, factor - 1.0))))))
            reach = max(1, impressions // max(1, frequency))

            # Create performance row using shared utility
            base_fields = {
                # Basic performance metrics
                "impressions": impressions,
                "clicks": clicks,
                "ctr": raw_ctr,  # This is already a rate (0.0-0.05)
                "completion_rate": completion_count,  # This is a percentage (0-100)
                "render_rate": render_factor,  # This is already a rate (0.0-1.0)
                "fill_rate": fill_factor,      # This is already a rate (0.0-1.0)
                "response_rate": response_factor,  # This is already a rate (0.0-1.0)
                "video_skip_rate": skip_factor,    # This is already a rate (0.0-1.0)
                "video_start": video_start,
                "frequency": frequency,
                "reach": reach,
                
                # Extended performance metrics (raw data only)
                "requests": int(impressions * rng.uniform(1.1, 1.8)),
                "responses": int(impressions * rng.uniform(0.92, 1.04)),
                "eligible_impressions": int(impressions * rng.uniform(0.85, 0.99)),
                "auctions_won": int(impressions * rng.uniform(0.90, 1.02)),
                "viewable_impressions": int(impressions * max(0.70, min(0.99, rng.uniform(0.80, 0.98) * factor))),
                "audible_impressions": int(impressions * max(0.20, min(0.95, rng.uniform(0.35, 0.80) * (1.05 if hour.hour >= 18 or hour.hour <= 22 else 0.95)))),
                "video_q25": int(video_start * max(0.60, min(0.98, rng.uniform(0.70, 0.95)))),
                "video_q50": int(video_start * max(0.40, min(0.90, rng.uniform(0.55, 0.90)))),
                "video_q75": int(video_start * max(0.25, min(0.80, rng.uniform(0.40, 0.80)))),
                "video_q100": int(video_start * max(0.10, min(0.70, rng.uniform(0.25, 0.70)))),
                "skips": int(video_start * max(0.05, min(0.60, rng.uniform(0.10, 0.40) * (2.0 - min(1.5, factor))))),
                "qr_scans": int(impressions * rng.uniform(0.0003, 0.006)),
                "interactive_engagements": int(impressions * rng.uniform(0.001, 0.02)),
                "spend": int((impressions * rng.randint(1200, 4500) * rng.uniform(0.9, 1.1) * (0.95 + 0.1 * min(1.5, factor))) // 1000),
                "error_count": int(impressions * rng.uniform(0.0005, 0.004)),
                "timeout_count": int(impressions * rng.uniform(0.0005, 0.003)),
            }
            
            # Optional: enrich with audience composition reflecting simple preferences
            audience_data = _audience_mix(rng, hour, impressions)
            base_fields["audience_json"] = json.dumps(audience_data)
            
            perf = create_performance_row(
                registry.CampaignPerformance,
                campaign_id,
                hour,
                base_fields
            )
            
            all_rows.append(perf)  # Collect instead of immediate add
            rows += 1
        
        # Batch insert all rows at once for better SQLite performance
        batch_insert_performance(s, all_rows)
        
        return rows


def _audience_mix(rng: Random, dt: datetime, impressions: int) -> dict:
    """Generate a simple audience composition snapshot aligned with preferences.

    Returns percentages (0..1) across segments. Sums may be ~1.0 after rounding.
    """
    # Device preferences: more CTV evenings/weekends, more MOBILE weekdays daytime
    is_weekend = dt.weekday() in (5, 6)
    evening = dt.hour >= 18 or dt.hour <= 22
    base_device = {
        "CTV": 0.45 if (is_weekend or evening) else 0.30,
        "DESKTOP": 0.20 if (is_weekend or evening) else 0.30,
        "MOBILE": 0.35 if (is_weekend or evening) else 0.40,
    }
    # Age buckets skew slightly older weekday daytime, younger evenings/weekends
    base_age = {
        "18-24": 0.16 if (is_weekend or evening) else 0.12,
        "25-34": 0.24,
        "35-44": 0.22,
        "45-54": 0.18,
        "55-64": 0.13,
        "65+": 0.07,
    }
    # Normalize helper
    def _normalize(d: dict[str, float]) -> dict[str, float]:
        s = sum(d.values()) or 1.0
        return {k: v / s for k, v in d.items()}

    device = _normalize(base_device)
    age = _normalize(base_age)
    gender = {"F": 0.5, "M": 0.5}
    life_stage = {"SINGLE": 0.35, "PARENT": 0.40, "EMPTY_NEST": 0.25}
    interest = {"SPORTS": 0.20, "ENTERTAINMENT": 0.30, "FOOD": 0.20, "TECH": 0.15, "TRAVEL": 0.15}

    return {
        "device": device,
        "age": age,
        "gender": gender,
        "life_stage": life_stage,
        "interest": interest,
    }


# Legacy function name for backward compatibility
def generate_hourly_performance(campaign_id: int, seed: int | None = None, replace: bool = True) -> int:
    """Legacy function that calls the new raw data generator."""
    return generate_hourly_performance_raw(campaign_id, seed, replace)