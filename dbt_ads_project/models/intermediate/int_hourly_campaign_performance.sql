{{ config(materialized='view') }}

-- Intermediate model for hourly campaign performance
-- This model handles common transformations and calculated metrics
-- that can be shared between staging and mart models

with staging as (
    select * from {{ ref('stg_hourly_campaign_performance') }}
),

base_calculations as (
    select
        *,
        -- Basic rate calculations (0-1 ratios)
        case 
            when impressions > 0 then round(cast(clicks as float) / impressions, 4)
            else 0 
        end as ctr,
        
        case 
            when video_start > 0 then round(cast(video_q100 as float) / video_start, 4)
            else 0 
        end as video_completion_rate,
        
        case 
            when video_start > 0 then round(cast(skips as float) / video_start, 4)
            else 0 
        end as video_skip_rate,
        
        case 
            when impressions > 0 then round(cast(video_start as float) / impressions, 4)
            else 0 
        end as video_start_rate,
        
        case 
            when impressions > 0 then round(cast(viewable_impressions as float) / impressions, 4)
            else 0 
        end as viewability_rate,
        
        case 
            when impressions > 0 then round(cast(audible_impressions as float) / impressions, 4)
            else 0 
        end as audibility_rate,
        
        case 
            when eligible_impressions > 0 then round(cast(auctions_won as float) / eligible_impressions, 4)
            else 0 
        end as win_rate,
        
        case 
            when requests > 0 then round(cast(eligible_impressions as float) / requests, 4)
            else 0 
        end as supply_funnel_efficiency,
        
        case 
            when eligible_impressions > 0 then round(cast(auctions_won as float) / eligible_impressions, 4)
            else 0 
        end as fill_rate,
        
        case 
            when requests > 0 then round(cast(responses as float) / requests, 4)
            else 0 
        end as response_rate,
        
        case 
            when requests > 0 then round(cast(error_count as float) / requests, 4)
            else 0 
        end as error_rate,
        
        case 
            when requests > 0 then round(cast(timeout_count as float) / requests, 4)
            else 0 
        end as timeout_rate,
        
        case 
            when impressions > 0 then round(cast(qr_scans as float) / impressions, 4)
            else 0 
        end as qr_scan_rate,
        
        case 
            when impressions > 0 then round(cast(interactive_engagements as float) / impressions, 4)
            else 0 
        end as interactive_rate,
        
        -- Cost metrics
        case 
            when spend > 0 and impressions > 0 then round(cast(spend as float) / impressions, 2)
            else 0 
        end as cpm,
        
        case 
            when spend > 0 and clicks > 0 then round(cast(spend as float) / clicks, 2)
            else 0 
        end as cpc,
        
        case 
            when spend > 0 and video_start > 0 then round(cast(spend as float) / video_start, 2)
            else 0 
        end as cpv,
        
        case 
            when impressions > 0 then round(cast(spend as float) * 1000 / impressions, 0)
            else 0 
        end as effective_cpm,
        
        -- Average watch time (estimated from quartiles)
        case 
            when video_start > 0 then
                round(
                    (
                        -- 0-25% segment
                        (video_start - video_q25) * 3.75 +
                        -- 25-50% segment  
                        (video_q25 - video_q50) * 11.25 +
                        -- 50-75% segment
                        (video_q50 - video_q75) * 18.75 +
                        -- 75-100% segment
                        (video_q75 - video_q100) * 26.25 +
                        -- 100% completion
                        video_q100 * 30.0
                    ) / video_start, 1
                )
            else 0 
        end as avg_watch_time_seconds
        
    from staging
)

select * from base_calculations
