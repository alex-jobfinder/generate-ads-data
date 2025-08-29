{{
  config(
    materialized='view',
    tags=['staging', 'performance']
  )
}}

WITH source AS (
    SELECT * FROM campaign_performance
),

renamed AS (
    SELECT
        -- Primary keys and grain
        id,
        campaign_id,
        hour_ts,
        
        -- Core metrics (NETFLIX CORE ADVERTISING METRICS)
        impressions,
        clicks,
        ctr,
        completion_rate,
        render_rate,
        fill_rate,
        response_rate,
        video_skip_rate,
        video_start,
        frequency,
        reach,
        audience_json,
        
        -- Extended raw metrics
        requests,
        responses,
        eligible_impressions,
        auctions_won,
        viewable_impressions,
        audible_impressions,
        video_q25,
        video_q50,
        video_q75,
        video_q100,
        skips,
        qr_scans,
        interactive_engagements,
        spend,
        error_count,
        timeout_count,
        
        -- Temporal fields
        human_readable,
        hour_of_day,
        minute_of_hour,
        second_of_minute,
        day_of_week,
        is_business_hour
        
    FROM source
)

SELECT * FROM renamed
