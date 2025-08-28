from __future__ import annotations

"""
Performance generation utilities.

Modeled effects (inspired by jafgen):
- Hour-of-day: Gaussian uplift during 09:00–17:00, peaking at 13:00.
- Day-of-week: Weekends less busy than weekdays (Fri 0.97, Sat 0.88, Sun 0.92).
- Flight ramp: Logistic S-curve (~0.85→1.15) with mild weekly undulation.
- Annual seasonality: Cosine by day-of-year (~0.8→1.0) for gentle yearly swings.
- Audience mix: Optional synthetic device/age/gender/life_stage/interest split.

Public API
- generate_hourly_performance(campaign_id, seed=None, replace=True) -> int
  Creates one row per hour (UTC boundary) across the campaign flight in
  `CampaignPerformance`. With a fixed seed, outputs are deterministic.
"""

from datetime import datetime, timedelta, timezone
import math
from random import Random
from typing import Iterable

from sqlalchemy import select, delete

from db_utils import session_scope
from models.orm import Campaign, Flight, CampaignPerformance
import json


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


def generate_hourly_performance(campaign_id: int, seed: int | None = None, replace: bool = True) -> int:
    """Generate hourly performance for a campaign across its flight window.

    Behavior:
    - Creates one row per hour between flight start and end (inclusive).
    - Stores `hour_ts` as UTC hour boundary.
    - `completion_rate` is an integer percentage in [0, 100].
    - `frequency` is an integer in [1, 5].
    - Impressions and related metrics are boosted using a bell curve during
      9:00–17:00 hours and a small additional weekend uplift.

    Args:
        campaign_id: Target campaign identifier to generate data for.
        seed: Optional RNG seed to make results reproducible.
        replace: If True, delete prior rows for the campaign before insert.

    Returns:
        Count of rows written for this campaign.
    """
    rng = Random(seed)
    with session_scope() as s:
        camp = s.execute(select(Campaign).where(Campaign.id == campaign_id)).scalar_one_or_none()
        if camp is None:
            return 0
        flight = s.execute(select(Flight).where(Flight.campaign_id == campaign_id)).scalar_one_or_none()
        if flight is None:
            return 0

        # Align bounds to whole hours in UTC. Start at 00:00, end at last full hour.
        start_dt = datetime.combine(flight.start_date, datetime.min.time(), tzinfo=timezone.utc)
        end_dt = datetime.combine(flight.end_date, datetime.max.time(), tzinfo=timezone.utc).replace(minute=0, second=0, microsecond=0)

        if replace:
            # Clear any previous synthetic rows for idempotent re-generation.
            s.execute(delete(CampaignPerformance).where(CampaignPerformance.campaign_id == campaign_id))

        rows = 0
        all_rows = []  # Collect all rows for batch insert
        for hour in _hours_between(start_dt, end_dt):
            # Seasonality & trends inspired by jafgen:
            # - Hour-of-day bell curve (prime hours peak)
            # - Day-of-week factor (weekends a bit less busy)
            # - Ramp factor over flight (store openings / audience growth)
            hod_factor = _hourly_boost(hour)             # ~1.0 - 1.5
            dow_factor = _dow_factor(hour)                # e.g., Sat/Sun < 1.0
            ramp = _ramp_factor(start_dt, hour, end_dt)   # ~0.85 → 1.15
            annual = _annual_factor(hour)                 # ~0.8 → 1.0

            factor = hod_factor * dow_factor * ramp * annual

            # Base draws provide variability, then scale by combined factor.
            base_impressions = rng.randint(1000, 10000)
            impressions = int(max(1, base_impressions * factor))

            # Generate clicks with realistic CTR (typically 0.1% to 2%)
            base_ctr = rng.uniform(0.001, 0.02)  # 0.1% to 2%
            ctr_variance = rng.uniform(0.8, 1.2)  # ±20% variation
            ctr = min(0.05, max(0.0001, base_ctr * ctr_variance * factor))  # Cap at 5%
            clicks = max(0, int(impressions * ctr))

            base_completion = rng.randint(70, 98)
            completion_bump = int(4 * min(1.0, max(0.0, factor - 1.0)))
            completion_rate = min(98, base_completion + completion_bump)

            # Generate render rate (typically 95-99%)
            base_render = rng.uniform(0.95, 0.99)
            render_rate = min(0.999, max(0.90, base_render * factor))

            # Generate fill rate (typically 85-98%)
            base_fill = rng.uniform(0.85, 0.98)
            fill_rate = min(0.999, max(0.80, base_fill * factor))

            # Generate response rate (typically 1-5% for interactive ads)
            base_response = rng.uniform(0.01, 0.05)
            response_rate = min(0.10, max(0.001, base_response * factor))

            # Generate video skip rate (typically 10-40%)
            base_skip = rng.uniform(0.10, 0.40)
            skip_rate = min(0.60, max(0.05, base_skip * (2.0 - factor)))  # Better performance = lower skip rate

            # Generate video start count (typically 80-95% of impressions for video ads)
            base_start_rate = rng.uniform(0.80, 0.95)
            start_rate = min(0.99, max(0.70, base_start_rate * factor))
            video_start = max(0, int(impressions * start_rate))

            base_frequency = rng.randint(1, 4)
            frequency = max(1, min(5, int(round(base_frequency * (1.0 + 0.15 * max(0.0, factor - 1.0))))))
            reach = max(1, impressions // max(1, frequency))

            perf = CampaignPerformance(
                campaign_id=campaign_id,
                hour_ts=hour,
                impressions=impressions,
                clicks=clicks,
                ctr=ctr,
                completion_rate=completion_rate,
                render_rate=render_rate,
                fill_rate=fill_rate,
                response_rate=response_rate,
                video_skip_rate=skip_rate,
                video_start=video_start,
                frequency=frequency,
                reach=reach,
            )
            # Optional: enrich with audience composition reflecting simple preferences
            perf.audience_json = json.dumps(_audience_mix(rng, hour, impressions))
            all_rows.append(perf)  # Collect instead of immediate add
            rows += 1
        
        # Batch insert all rows at once for better SQLite performance
        s.bulk_save_objects(all_rows)
        s.flush()
        
        return rows


def _hourly_boost(dt: datetime) -> float:
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


def _dow_factor(dt: datetime) -> float:
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


def _ramp_factor(start_dt: datetime, current_dt: datetime, end_dt: datetime) -> float:
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


def _annual_factor(dt: datetime) -> float:
    """Annual seasonality factor similar to jafgen's AnnualCurve.

    Cosine over day-of-year scaled to roughly [0.8, 1.0].
    """
    # Day of year in [1..366]; use 365 as baseline period
    yday = dt.timetuple().tm_yday
    x = 2.0 * math.pi * (yday - 1) / 365.0
    return (math.cos(x) + 1.0) / 10.0 + 0.8


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