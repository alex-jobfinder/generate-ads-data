# Codex Tasks — Pytest Per-File Goals

Create or fix code so each test file passes in isolation.

- [ ] Pass `pytest -q tests/test_cli_new_features.py` — iterate with `pytest tests/test_cli_new_features.py -x`
- [ ] Pass `pytest -q tests/test_config_and_cli.py` — iterate with `pytest tests/test_config_and_cli.py -x`
- [ ] Pass `pytest -q tests/test_docs_campaign_api.py` — iterate with `pytest tests/test_docs_campaign_api.py -x`
- [ ] Pass `pytest -q tests/test_docs_cli.py` — iterate with `pytest tests/test_docs_cli.py -x`
- [ ] Pass `pytest -q tests/test_flows_v1.py` — iterate with `pytest tests/test_flows_v1.py -x`
- [ ] Pass `pytest -q tests/test_formats_and_targeting_v2.py` — iterate with `pytest tests/test_formats_and_targeting_v2.py -x`
- [ ] Pass `pytest -q tests/test_orm_persistence.py` — iterate with `pytest tests/test_orm_persistence.py -x`
- [ ] Pass `pytest -q tests/test_performance_metrics.py` — iterate with `pytest tests/test_performance_metrics.py -x`
- [ ] Pass `pytest -q tests/test_schema_tables_and_constraints.py` — iterate with `pytest tests/test_schema_tables_and_constraints.py -x`

Tips:
- Re-run last failures: `pytest --lf`
- Stop on first failure: `pytest -x`
- Focus a single test: `pytest tests/test_cli_new_features.py::TestClass::test_name`

<!-- python -m pytest tests/test_docs_cli.py -v --tb=short
python -m pytest tests/test_cli_new_features.py -v --tb=short
python -m pytest tests/test_docs_campaign_api.py -v --tb=short
python -m pytest tests/test_flows_v1.py -v --tb=short
python -m pytest tests/test_orm_persistence.py -v --tb=short
python -m pytest tests/test_performance_metrics.py -v --tb=short
python -m pytest tests/test_config_and_cli.py -v --tb=short
python -m pytest tests/test_formats_and_targeting_v2.py -v --tb=short
python -m pytest tests/test_schema_tables_and_constraints.py -v --tb=short -->