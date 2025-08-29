# MetricFlow Cheat Sheet (dbt Semantic Layer)

Quick commands for defining, validating, and querying metrics via dbt’s Semantic Layer (dbt Cloud: `dbt sl ...`) and dbt Core (`mf ...`). Examples use this repo’s metrics/dimensions.

## Setup
- Install (dbt Cloud users skip): `pip install dbt-metricflow` (or `python -m pip install "dbt-metricflow[<adapter>]"`)
- Python: 3.8–3.11 supported
- Update graph after metric edits: `dbt parse` (updates `semantic_manifest.json`)
- Note: If `mf` errors and you have Metafont LaTeX installed, uninstall Metafont to run `mf` commands.

## Introspection
- List metrics: `dbt sl list metrics [--search <term>]` | `mf list metrics [--search <term>]`
- List dimensions (for metrics): `dbt sl list dimensions --metrics <m1[,m2]>` | `mf list dimensions --metrics <m1[,m2]>`
- List dimension values: `dbt sl list dimension-values --metrics <m> --dimension <d>` | `mf list dimension-values --metrics <m> --dimension <d>`
- List entities: `dbt sl list entities --metrics <m1[,m2]>` | `mf list entities --metrics <m1[,m2]>`
- List saved queries: `dbt sl list saved-queries [--show-exports | --show-parameters]`

## Validate & Health
- Validate configs: `dbt sl validate` | `mf validate-configs [--skip-dw] [--dw-timeout <secs>] [--show-all] [--verbose-issues] [--semantic-validation-workers N]`
- Health checks (Core): `mf health-checks`
- Tutorial (Core): `mf tutorial`

## Query (metrics/dimensions)
- dbt Cloud: `dbt sl query --metrics <m1[,m2]> --group-by <d1[,d2]> [--limit N] [--order-by <fields>] [--where <tpl>] [--compile]`
- dbt Core: `mf query --metrics <m1[,m2]> --group-by <d1[,d2]> [--limit N] [--order-by <fields>] [--where <tpl>] [--start-time <iso>] [--end-time <iso>] [--explain]`
- Time granularity: append `__day|__week|__month|__quarter|__year` to `metric_time` (example: `metric_time__month`).
- Where filter template helpers: `Dimension('dim')`, `TimeDimension('metric_time','week')`.

## Project Metrics & Dimensions (this repo)
- Metrics (examples): `total_impressions`, `total_clicks`, `total_spend`, `overall_ctr`, `cost_per_click`, `cost_per_mille`, `total_reach`, `response_rate_overall`, `viewability_rate`, `video_completion_rate_overall`, `win_rate`, ... (see `models/semantic_layer/metrics.yml`)
- Dimensions (examples): `campaign_id`, `hour_ts` (time), `hour_of_day`, `day_of_week`, `is_business_hour` (see `models/semantic_layer/semantic_models.yml`)

## Practical Examples (this repo)
- List metrics with dimensions:
  - Cloud: `dbt sl list metrics`
  - Core: `mf list metrics`
- List dimensions for multiple metrics (intersection):
  - `mf list dimensions --metrics total_impressions,overall_ctr`
- Query multiple metrics by time:
  - Cloud: `dbt sl query --metrics total_impressions,total_clicks --group-by metric_time`
  - Core: `mf query --metrics total_impressions,total_clicks --group-by metric_time`
- Query CTR by campaign and hour of day, latest 24h (Core):
  - `mf query --metrics overall_ctr --group-by campaign_id,hour_of_day --start-time '2025-08-28' --end-time '2025-08-29'`
- Filter and sort (Core):
  - `mf query --metrics cost_per_click --group-by campaign_id --where "{{ Dimension('campaign_id') }} IN (1,2,3)" --order-by -cost_per_click --limit 10`
- Time granularity (month):
  - `mf query --metrics cost_per_mille --group-by metric_time__month`
- Filter by business hours (Core):
  - `mf query --metrics total_impressions --group-by is_business_hour --where "{{ Dimension('is_business_hour') }} = 1"`
- Explain SQL instead of data (Core):
  - `mf query --metrics total_spend --group-by metric_time__day --explain --show-dataflow-plan`

## Saved Queries & Exports
- Run saved query (Cloud): `dbt sl query --saved-query <name>`
- Export (Cloud): `dbt sl export --saved-query <name> [--select <export_name>]`
- Export all (Cloud): `dbt sl export-all`

## Tips
- Always run `dbt parse` after changing metrics/semantic models so CLI queries reflect updates.
- In Core, `--start-time/--end-time` push down time filters for better performance.
- `--order-by` supports multiple fields, prefix with `-` for DESC (e.g., `--order-by -metric_time,-total_impressions`).
- When writing `--where`, reference only fields in the model using template wrappers (Dimension/TimeDimension).
