{{
  config(
    materialized='table',
    tags=['intermediate', 'performance', 'calculated_metrics']
  )
}}

WITH source AS (
    SELECT * FROM {{ ref('stg_campaign_performance') }}
),

calculated_metrics AS (
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
        is_business_hour,
        
        -- ===== CALCULATED METRICS (replicating Python logic exactly) =====
        
        -- Fill rate extended (eligible/requests)
        {{ safe_division('eligible_impressions', 'requests') }} AS fill_rate_ext,
        
        -- Viewability rate (viewable/impressions)
        {{ safe_division('viewable_impressions', 'impressions') }} AS viewability_rate,
        
        -- Audibility rate (audible/impressions)
        {{ safe_division('audible_impressions', 'impressions') }} AS audibility_rate,
        
        -- Video start rate (starts/impressions)
        {{ safe_division('video_start', 'impressions') }} AS video_start_rate,
        
        -- Video completion rate (q100/starts)
        {{ safe_division('video_q100', 'video_start') }} AS video_completion_rate,
        
        -- Video skip rate extended (skips/starts)
        {{ safe_division('skips', 'video_start') }} AS video_skip_rate_ext,
        
        -- QR scan rate (scans/impressions)
        {{ safe_division('qr_scans', 'impressions') }} AS qr_scan_rate,
        
        -- Interactive engagement rate (engagements/impressions)
        {{ safe_division('interactive_engagements', 'impressions') }} AS interactive_rate,
        
        -- Effective CPM in cents (spend*1000/impressions)
        CASE 
            WHEN impressions = 0 OR impressions IS NULL THEN 0
            ELSE CAST((spend * 1000) / impressions AS INTEGER)
        END AS effective_cpm,
        
        -- Average watch time in seconds (estimated from quartiles)
        {{ avg_watch_time_seconds('video_start', 'video_q25', 'video_q50', 'video_q75', 'video_q100', 30.0) }} AS avg_watch_time_seconds,
        
        -- Supply funnel efficiency (eligible/requests)
        {{ safe_division('eligible_impressions', 'requests') }} AS supply_funnel_efficiency,
        
        -- Auction win rate (won/eligible)
        {{ safe_division('auctions_won', 'eligible_impressions') }} AS auction_win_rate,
        
        -- Error rate (errors/requests)
        {{ safe_division('error_count', 'requests') }} AS error_rate,
        
        -- Timeout rate (timeouts/requests)
        {{ safe_division('timeout_count', 'requests') }} AS timeout_rate,
        
        -- CTR recalculated (clicks/impressions)
        {{ safe_division('clicks', 'impressions') }} AS ctr_recalc
        
    FROM source
)

SELECT * FROM calculated_metrics
