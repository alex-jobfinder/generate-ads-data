{{
  config(
    materialized='table',
    tags=['marts', 'performance', 'extended_metrics']
  )
}}

WITH calculated_performance AS (
    SELECT * FROM {{ ref('int_campaign_performance_calculated') }}
),

final AS (
    SELECT
        -- Primary key (will be auto-generated)
        campaign_id,
        hour_ts,
        
        -- Supply funnel
        requests,
        responses,
        eligible_impressions,
        auctions_won,
        impressions,
        
        -- Delivery quality
        viewable_impressions,
        audible_impressions,
        
        -- Video progression
        video_start AS video_starts,
        video_q25,
        video_q50,
        video_q75,
        video_q100,
        skips,
        avg_watch_time_seconds,
        
        -- Interactions
        clicks,
        qr_scans,
        interactive_engagements,
        
        -- Reach & frequency
        reach,
        frequency,
        
        -- Spend / pricing
        spend,
        effective_cpm,
        
        -- Errors
        error_count,
        timeout_count,
        
        -- Optional metadata
        'Generated via DBT calculated metrics' AS comment,
        
        -- Temporal breakdown columns
        human_readable,
        hour_of_day,
        minute_of_hour,
        second_of_minute,
        day_of_week,
        is_business_hour,
        
        -- ===== CALCULATED FIELDS (matching Python performance_ext.py exactly) =====
        ctr_recalc,
        viewability_rate,
        audibility_rate,
        video_start_rate,
        video_completion_rate,
        video_skip_rate_ext,
        qr_scan_rate,
        interactive_rate,
        auction_win_rate,
        error_rate,
        timeout_rate,
        supply_funnel_efficiency
        
    FROM calculated_performance
)

SELECT * FROM final
