-- Test core calculation logic for key metrics
-- This test verifies that the calculated metrics follow basic business logic

WITH calculated_metrics AS (
    SELECT * FROM {{ ref('mart_campaign_performance_extended') }}
),

validation_checks AS (
    SELECT
        campaign_id,
        hour_ts,
        
        -- Test that rates are between 0 and 1 (allowing for small floating point precision issues)
        CASE 
            WHEN viewability_rate < -0.0001 OR viewability_rate > 1.0001 THEN 'viewability_rate out of range'
            WHEN audibility_rate < -0.0001 OR audibility_rate > 1.0001 THEN 'audibility_rate out of range'
            WHEN video_start_rate < -0.0001 OR video_start_rate > 1.0001 THEN 'video_start_rate out of range'
            WHEN video_completion_rate < -0.0001 OR video_completion_rate > 1.0001 THEN 'video_completion_rate out of range'
            WHEN video_skip_rate_ext < -0.0001 OR video_skip_rate_ext > 1.0001 THEN 'video_skip_rate_ext out of range'
            WHEN qr_scan_rate < -0.0001 OR qr_scan_rate > 1.0001 THEN 'qr_scan_rate out of range'
            WHEN interactive_rate < -0.0001 OR interactive_rate > 1.0001 THEN 'interactive_rate out of range'
            WHEN auction_win_rate < -0.0001 OR auction_win_rate > 1.0001 THEN 'auction_win_rate out of range'
            WHEN error_rate < -0.0001 OR error_rate > 1.0001 THEN 'error_rate out of range'
            WHEN timeout_rate < -0.0001 OR timeout_rate > 1.0001 THEN 'timeout_rate out of range'
            WHEN supply_funnel_efficiency < -0.0001 OR supply_funnel_efficiency > 1.0001 THEN 'supply_funnel_efficiency out of range'
            WHEN ctr_recalc < -0.0001 OR ctr_recalc > 1.0001 THEN 'ctr_recalc out of range'
            ELSE 'PASS'
        END AS rate_validation,
        
        -- Test that effective CPM is non-negative
        CASE 
            WHEN effective_cpm < 0 THEN 'effective_cpm negative'
            ELSE 'PASS'
        END AS cpm_validation,
        
        -- Test that average watch time is reasonable
        CASE 
            WHEN avg_watch_time_seconds < 0 OR avg_watch_time_seconds > 3600 THEN 'avg_watch_time_seconds out of range'
            ELSE 'PASS'
        END AS watch_time_validation
        
    FROM calculated_metrics
    -- Only test a sample to avoid overwhelming output
    LIMIT 1000
)

SELECT 
    campaign_id,
    hour_ts,
    rate_validation,
    cpm_validation,
    watch_time_validation
FROM validation_checks
WHERE rate_validation != 'PASS' 
   OR cpm_validation != 'PASS'
   OR watch_time_validation != 'PASS'
