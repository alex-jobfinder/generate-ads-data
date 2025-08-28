"""
Pydantic schemas for inbound create requests (Advertiser, Campaign, LineItem, Creative).

Recommended improvements:
- Add stricter validators for relationships (e.g., creative duration vs ad_format policy).
- Consider schema versions and compatibility for future changes.
- Add examples/examples factory for documentation.
"""
from __future__ import annotations

from datetime import date, datetime
import os
from decimal import Decimal
from typing import Optional, Literal, List, Dict, Any

from pydantic import BaseModel, EmailStr, Field, conint, ConfigDict

from .enums import (
    Objective,
    CampaignStatus,
    BudgetType,
    FreqCapUnit,
    FreqCapScope,
    DspPartner,
    Currency,
    AdFormat,
    CreativeMimeType,
    TargetingKey,
    AdPlacement,
    FileFormat,
    FrameRate,
    FrameRateMode,
    AspectRatio,
    ScanType,
    VideoCodecH264Profile,
    VideoCodecProresProfile,
    ChromaSubsampling,
    ColorPrimaries,
    TransferFunction,
    AudioCodec,
    AudioChannels,
    AdServerType,
    PixelVendor,
    ProgrammaticBuyType,
    CleanRoomProvider,
    ContentAdjacencyTier,
    MeasurementPartner,
    Device,
    GeoTier,
    TargetingDefaults,
    is_valid_targeting_key,
    clamp_cpm_to_defaults,
    CreativeDefaults,
    PricingDefaults,
    ServingDefaults,
)


class AdvertiserCreate(BaseModel):
    name: str
    brand: Optional[str] = None
    contact_email: EmailStr
    agency_name: Optional[str] = None


class FrequencyCap(BaseModel):
    count: conint(ge=0)  # non-negative integer
    unit: FreqCapUnit
    scope: FreqCapScope = FreqCapScope.user


class Flight(BaseModel):
    start_date: date
    end_date: date


class Budget(BaseModel):
    amount: Decimal
    type: BudgetType
    currency: Currency = Currency.USD


class Targeting(BaseModel):
    device: List[Device] | None = None
    geo_country: List[str] | None = None
    geo_tier: GeoTier | None = None
    content_genre: List[str] | None = None
    age_range: List[int] | None = None
    gender: str | None = None
    household_income: str | None = None

    def model_post_init(self, __context: Any) -> None:
        if self.age_range is not None:
            if len(self.age_range) != 2:
                raise ValueError("age_range must be [min, max]")
            rng = (self.age_range[0], self.age_range[1])
            if rng not in TargetingDefaults.DEFAULT_AGE_RANGES:
                raise ValueError(f"age_range {rng} not in allowed buckets {list(TargetingDefaults.DEFAULT_AGE_RANGES)}")

class CreativeCreate(BaseModel):
    asset_url: str
    mime_type: CreativeMimeType
    # Expanded durations; keep tests compatible (15/30) while allowing others
    duration_seconds: int
    # Optional spec fields (v2+)
    placement: AdPlacement | None = None
    file_format: FileFormat | None = None
    width: int | None = None
    height: int | None = None
    frame_rate: FrameRate | None = None
    frame_rate_mode: FrameRateMode | None = None
    aspect_ratio: AspectRatio | None = None
    scan_type: ScanType | None = None
    video_codec_h264_profile: VideoCodecH264Profile | None = None
    video_codec_prores_profile: VideoCodecProresProfile | None = None
    chroma_subsampling: ChromaSubsampling | None = None
    color_primaries: ColorPrimaries | None = None
    transfer_function: TransferFunction | None = None
    bitrate_kbps: int | None = None
    file_size_bytes: int | None = None
    audio_codec: AudioCodec | None = None
    audio_channels: AudioChannels | None = None
    audio_sample_rate_hz: int | None = None
    audio_bit_depth: int | None = None
    safe_zone_ok: bool | None = None
    is_interactive: bool | None = None
    interactive_meta_json: Dict[str, Any] | None = None
    is_pause_ad: bool | None = None
    qr_code_url: str | None = None
    overlay_cta_text: str | None = Field(default=None, max_length=30)

    def model_post_init(self, __context: Any) -> None:
        # Non-negative checks
        if self.file_size_bytes is not None and self.file_size_bytes < 0:
            raise ValueError("file_size_bytes must be non-negative")
        if self.bitrate_kbps is not None and self.bitrate_kbps < 0:
            raise ValueError("bitrate_kbps must be non-negative")
        # LIVE placement requires 1920x1080 if provided
        if self.placement == AdPlacement.LIVE and (self.width is not None and self.height is not None):
            if not (self.width == 1920 and self.height == 1080):
                raise ValueError("LIVE placement requires resolution 1920x1080")


class LineItemCreate(BaseModel):
    name: str
    ad_format: AdFormat
    bid_cpm: Decimal
    pacing_pct: conint(gt=ServingDefaults.PACING_PCT_MIN - 0, le=ServingDefaults.PACING_PCT_MAX) = ServingDefaults.PACING_PCT_MAX # type: ignore
    targeting: Dict[str, Any] = Field(default_factory=dict)
    creatives: List[CreativeCreate]
    # Additional delivery and serving metadata
    duration_seconds: int | None = None
    ad_server_type: AdServerType | None = None
    pixel_vendor: PixelVendor | None = None
    targeting_v2: Optional[Targeting] = None

    @staticmethod
    def allowed_targeting_keys() -> set[str]:
        return {k.value for k in TargetingKey}

    def model_post_init(self, __context: Any) -> None:
        # whitelist top-level targeting keys
        unknown = set(self.targeting.keys()) - self.allowed_targeting_keys()
        if unknown:
            raise ValueError(f"Unknown targeting keys: {sorted(unknown)}")
        # soft constraints: warn if pacing unusual or bid_cpm outside recommended pricing range
        try:
            # Only emit soft-constraint warnings when explicitly enabled
            warn_soft = os.getenv("ADS_WARN_SOFT_CONSTRAINTS", "0").lower() in {"1", "true", "yes", "on"}
            if warn_soft:
                from warnings import warn
                # CPM soft bounds warning
                min_cpm, max_cpm = PricingDefaults.CPM_RANGE_USD
                if self.bid_cpm is not None and (self.bid_cpm < min_cpm or self.bid_cpm > max_cpm):
                    warn(f"bid_cpm {self.bid_cpm} is outside typical CPM range {min_cpm}-{max_cpm}")
        except Exception:
            pass


class CampaignCreate(BaseModel):
    advertiser_id: Optional[int] = None
    name: str
    objective: Objective
    status: CampaignStatus = CampaignStatus.draft
    currency: Currency = Currency.USD
    target_cpm: Decimal
    frequency_cap: Optional[FrequencyCap] = None
    dsp_partner: DspPartner
    programmatic_buy_type: ProgrammaticBuyType | None = None
    programmatic_partner: DspPartner | None = None
    content_adjacency_tier: ContentAdjacencyTier | None = None
    brand_lift_enabled: bool | None = None
    attention_metrics_enabled: bool | None = None
    clean_room_provider: CleanRoomProvider | None = None
    measurement_partner: MeasurementPartner | None = None
    external_ref: str | None = None
    flight: Flight
    budget: Budget
    line_items: List[LineItemCreate]

Targeting.model_rebuild()


# ===== Performance Data Schemas =====

class PerformanceMetricsBase(BaseModel):
    """Base schema for performance metrics with raw data only."""
    
    campaign_id: int
    hour_ts: datetime
    impressions: int = Field(ge=0, description="Total ad impressions served")
    clicks: int = Field(ge=0, description="Total click-through interactions")
    ctr: float = Field(ge=0.0, le=1.0, description="Click-through rate (0.0-1.0)")
    completion_rate: int = Field(ge=0, le=100, description="Video completion rate as percentage (0-100)")
    render_rate: float = Field(ge=0.0, le=1.0, description="Render rate (0.0-1.0)")
    fill_rate: float = Field(ge=0.0, le=1.0, description="Fill rate (0.0-1.0)")
    response_rate: float = Field(ge=0.0, le=1.0, description="Response rate (0.0-1.0)")
    video_skip_rate: float = Field(ge=0.0, le=1.0, description="Video skip rate (0.0-1.0)")
    video_start: int = Field(ge=0, description="Video start count")
    frequency: int = Field(ge=1, description="Average frequency per user")
    reach: int = Field(ge=0, description="Unique users reached")
    audience_json: Optional[str] = Field(None, description="Audience composition JSON")
    
    # Temporal breakdown fields
    human_readable: str = Field(description="Human-readable timestamp string")
    hour_of_day: int = Field(ge=0, le=23, description="Hour of day (0-23)")
    minute_of_hour: int = Field(ge=0, le=59, description="Minute of hour (0-59)")
    second_of_minute: int = Field(ge=0, le=59, description="Second of minute (0-59)")
    day_of_week: int = Field(ge=0, le=6, description="Day of week (0=Monday, 6=Sunday)")
    is_business_hour: bool = Field(description="Whether this is during business hours")
    
    model_config = {"arbitrary_types_allowed": True}


class PerformanceMetricsCreate(PerformanceMetricsBase):
    """Schema for creating new performance metrics."""
    pass


class PerformanceMetricsRead(PerformanceMetricsBase):
    """Schema for reading performance metrics."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class ExtendedPerformanceMetricsBase(BaseModel):
    """Base schema for extended performance metrics with raw data only."""
    
    campaign_id: int
    hour_ts: datetime
    
    # Supply funnel
    requests: int = Field(ge=0, description="Total ad requests made")
    responses: int = Field(ge=0, description="Total responses received")
    eligible_impressions: int = Field(ge=0, description="Impressions eligible after targeting")
    auctions_won: int = Field(ge=0, description="Auctions won")
    impressions: int = Field(ge=0, description="Total ad impressions served")
    
    # Quality metrics
    viewable_impressions: int = Field(ge=0, description="Viewable impressions")
    audible_impressions: int = Field(ge=0, description="Audible impressions")
    
    # Video metrics
    video_starts: int = Field(ge=0, description="Video ads that began playing")
    video_q25: int = Field(ge=0, description="Video ads that reached 25% completion")
    video_q50: int = Field(ge=0, description="Video ads that reached 50% completion")
    video_q75: int = Field(ge=0, description="Video ads that reached 75% completion")
    video_q100: int = Field(ge=0, description="Video ads that reached 100% completion")
    skips: int = Field(ge=0, description="Video ads that were skipped")
    avg_watch_time_seconds: int = Field(ge=0, le=3600, description="Average watch time in seconds")
    
    # Interaction metrics
    clicks: int = Field(ge=0, description="Total click-through interactions")
    qr_scans: int = Field(ge=0, description="QR code scans")
    interactive_engagements: int = Field(ge=0, description="Interactive engagements")
    
    # Audience metrics
    reach: int = Field(ge=0, description="Unique users reached")
    frequency: int = Field(ge=1, le=10, description="Average frequency per user")
    
    # Spend metrics
    spend: int = Field(ge=0, description="Total spend in cents")
    effective_cpm: int = Field(ge=0, description="Effective CPM in cents")
    
    # Reliability metrics
    error_count: int = Field(ge=0, description="Error count")
    timeout_count: int = Field(ge=0, description="Timeout count")
    
    # Optional metadata
    comment: Optional[str] = Field(None, description="Additional notes or metadata")
    
    # Temporal breakdown fields
    human_readable: str = Field(description="Human-readable timestamp string")
    hour_of_day: int = Field(ge=0, le=23, description="Hour of day (0-23)")
    minute_of_hour: int = Field(ge=0, le=59, description="Minute of hour (0-59)")
    second_of_minute: int = Field(ge=0, le=59, description="Second of minute (0-59)")
    day_of_week: int = Field(ge=0, le=6, description="Day of week (0=Monday, 6=Sunday)")
    is_business_hour: bool = Field(description="Whether this is during business hours")
    
    # Calculated metrics
    ctr_recalc: float | None = Field(None, description="Recalculated CTR (clicks/impressions)")
    viewability_rate: float | None = Field(None, description="Viewability rate (viewable/impressions)")
    audibility_rate: float | None = Field(None, description="Audibility rate (audible/impressions)")
    video_start_rate: float | None = Field(None, description="Video start rate (starts/impressions)")
    video_completion_rate: float | None = Field(None, description="Video completion rate (q100/starts)")
    video_skip_rate_ext: float | None = Field(None, description="Extended video skip rate (skips/starts)")
    qr_scan_rate: float | None = Field(None, description="QR scan rate (scans/impressions)")
    interactive_rate: float | None = Field(None, description="Interactive engagement rate")
    auction_win_rate: float | None = Field(None, description="Auction win rate (won/eligible)")
    error_rate: float | None = Field(None, description="Error rate (errors/requests)")
    timeout_rate: float | None = Field(None, description="Timeout rate (timeouts/requests)")
    supply_funnel_efficiency: float | None = Field(None, description="Supply funnel efficiency (eligible/requests)")
        
    
    model_config = {"arbitrary_types_allowed": True}


class ExtendedPerformanceMetricsCreate(ExtendedPerformanceMetricsBase):
    """Schema for creating new extended performance metrics."""
    pass


class ExtendedPerformanceMetricsRead(ExtendedPerformanceMetricsBase):
    """Schema for reading extended performance metrics."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)

