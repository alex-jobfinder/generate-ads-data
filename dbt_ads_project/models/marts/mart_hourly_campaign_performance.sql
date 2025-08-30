{{ config(materialized='table') }}

-- Mart model for hourly campaign performance
-- This model builds upon the intermediate data and adds business logic,
-- performance flags, and additional aggregations for analysis and reporting

with intermediate as (
    select * from {{ ref('int_hourly_campaign_performance') }}
),

enriched as (
    select
        -- All base fields and calculated metrics from intermediate
        *,
        
        -- Additional time dimensions for analysis
        date_trunc('day', cast(hour_ts as timestamp)) as date_day,
        date_trunc('week', cast(hour_ts as timestamp)) as date_week,
        date_trunc('month', cast(hour_ts as timestamp)) as date_month,
        
        -- Performance flags based on calculated metrics
        case when ctr >= 0.02 then 1 else 0 end as high_ctr_flag,
        case when viewability_rate >= 0.7 then 1 else 0 end as high_viewability_flag,
        
        -- Business logic: rename calculated_ctr to ctr for consistency
        ctr as calculated_ctr
        
    from intermediate
)

select * from enriched
