#+ dbt Cheat Sheet

Quick reference for this repo’s dbt setup. Assumes running from `dbt_models/`.

## Core Setup

- Verify: `dbt --version`
- Parse: `dbt parse`
- Install packages: `dbt deps`
- Use local profile file: `--profiles-dir .`
- Project profile name (local): `dbt_models` (see `dbt_models/profiles.yml`)

## Common Workflows

- Build all (models, tests, snapshots):
  - `dbt build --profiles-dir . --profile dbt_models --threads 4`
- Run models only:
  - `dbt run --profiles-dir . --profile dbt_models --threads 4`
- Run tests only:
  - `dbt test --profiles-dir . --profile dbt_models`
- Seed CSVs (load into warehouse):
  - `dbt seed --profiles-dir . --profile dbt_models`
  - `dbt seed --profiles-dir . --profile dbt_models --select campaign_performance`
- Compile SQL without executing:
  - `dbt compile --profiles-dir . --profile dbt_models`
- Clean artifacts and installed packages:
  - `dbt clean`

## Selection Syntax (works with run/test/build)

- Single node: `--select my_model`
- By path: `--select path:models/semantic_layer`
- By tag: `--select tag:daily`
- Parents/children: `--select +my_model`, `my_model+`, `+my_model+`
- Subgraph: `--select @my_model`
- Config filter: `--select config.materialized:incremental`
- State-aware (changed + downstream): `--select state:modified+ --state ./target`

## Docs & Discovery

- Generate docs site: `dbt docs generate --profiles-dir . --profile dbt_models`
- Serve docs locally: `dbt docs serve --profiles-dir . --profile dbt_models`
- List nodes: `dbt list --profiles-dir . --profile dbt_models`
- List models only: `dbt list --resource-type model`

## Debugging & Performance

- Connection check: `dbt debug --profiles-dir . --profile dbt_models`
- Verbose logs: `dbt --log-level debug build --profiles-dir . --profile dbt_models`
- Fail fast: `dbt build --fail-fast`
- Threads (parallelism): `--threads N` (e.g., `--threads 4`)

## Seeds (CSV → Table)

- Configure types/tests in: `seeds/<name>.yml` (e.g., `seeds/campaign_performance.yml`)
- Load single seed: `dbt seed --select campaign_performance --profiles-dir . --profile dbt_models`
- Force reload: `dbt seed --full-refresh --profiles-dir . --profile dbt_models`

## Snapshots & Sources

- Run snapshots: `dbt snapshot --profiles-dir . --profile dbt_models`
- Source freshness: `dbt source freshness --profiles-dir . --profile dbt_models`

## Variables & Operations

- Pass vars: `dbt build --vars '{days: 7}' --profiles-dir . --profile dbt_models`
- Run macro only: `dbt run-operation macro_name --args '{key: "val"}' --profiles-dir . --profile dbt_models`

## Adapter Examples

### DuckDB

- Install adapter: `pip install dbt-duckdb`
- Example profile (see `dbt_models/profiles.yml`):
  ```yaml
  dbt_models:
    target: dev
    outputs:
      dev:
        type: duckdb
        path: ./dbt_models.duckdb
        threads: 4
  ```
- Typical commands:
  - `dbt deps`
  - `dbt seed --profiles-dir . --profile dbt_models`
  - `dbt build --profiles-dir . --profile dbt_models --threads 4`

### SQLite

- Install adapter: `pip install dbt-sqlite`
- Example profile:
  ```yaml
  ads_sqlite:
    target: dev
    outputs:
      dev:
        type: sqlite
        database: ./ads.db
        schema: main
        threads: 1
  ```
- Typical commands:
  - `dbt debug --profiles-dir . --profile ads_sqlite`
  - `dbt seed --profiles-dir . --profile ads_sqlite`
  - `dbt build --profiles-dir . --profile ads_sqlite`

## CI Hints (GitHub Actions)

```yaml
name: dbt
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - name: Install
        run: pip install dbt-core dbt-duckdb dbt-sqlite
      - name: Deps
        run: DBT_PROFILES_DIR=dbt_models dbt deps
      - name: Build
        run: DBT_PROFILES_DIR=dbt_models dbt build --profile dbt_models --threads 4 --fail-fast
```

## Quick Start (this project)

1) `cd dbt_models && dbt deps`
2) `dbt seed --profiles-dir . --profile dbt_models --select campaign_performance`
3) `dbt test --profiles-dir . --profile dbt_models --select campaign_performance`
4) `dbt build --profiles-dir . --profile dbt_models --threads 4`

