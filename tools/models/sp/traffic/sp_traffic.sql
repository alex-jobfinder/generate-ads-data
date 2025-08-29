-- Aggregate traffic metrics from events seeds/sources into a view
with base as (
    select * from {{ ref('sp_events_base') }}
)
, clicks as (
    select idempotency_id, count(*) as clicks, round(sum(cost_of_click), 2) as cost
    from {{ ref('sp_events_clicks') }}
    group by 1
)
, imps as (
    select idempotency_id, count(*) as impressions
    from {{ ref('sp_events_impressions') }}
    group by 1
)
select
    b.idempotency_id,
    b.dataset_id,
    b.marketplace_id,
    b.currency,
    b.advertiser_id,
    b.campaign_id,
    b.ad_group_id,
    b.ad_id,
    b.keyword_id,
    b.keyword_text,
    b.match_type,
    b.placement,
    b.time_window_start,
    coalesce(c.clicks, 0) as clicks,
    coalesce(i.impressions, 0) as impressions,
    coalesce(c.cost, 0.0) as cost
from base b
left join clicks c using (idempotency_id)
left join imps i using (idempotency_id)


