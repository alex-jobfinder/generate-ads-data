## generate-ads-data

CLI-driven Netflix Ads domain model with Pydantic (v2), SQLAlchemy (v2), and Faker, persisting to SQLite. Enums and constants provide a single source of truth; optional colorized logging is supported.

### Directory layout
- `db_utils.py`: Settings + logger (`colorlog` if available) + SQLAlchemy engine/session + `init_db` + `session_scope`.
- `models/enums.py`: All enums with UPPERCASE values; centralized domain constants and `TargetingKey`.
- `models/schemas.py`: Pydantic v2 request models using enums (`CreativeMimeType`) and deriving allowed targeting keys from `TargetingKey`.
- `models/orm.py`: SQLAlchemy ORM models with timestamps and constraints.
- `factories/faker_providers.py`: Faker helpers referencing enums/constants (no hardcoded numbers/keys).
- `services/generator.py`: Maps Pydantic payloads → ORM rows; handles cents conversion.
- `services/validators.py`: Cross-field checks using constants from enums.
- `cli.py`: Click-based CLI to init DB and create advertiser/campaign; respects `LOG_LEVEL` and `ADS_DB_URL`.
- `tests/`: 15 tests for CLI, schema, targeting, and ORM persistence.

### Enums and constants
- Enums: `Objective`, `CampaignStatus`, `AdFormat`, `BudgetType`, `FreqCapUnit`, `FreqCapScope`, `PacingType`, `QAStatus`, `DspPartner`, `Currency`, `CreativeMimeType`, `TargetingKey`.
- Constants (in `models/enums.py`): `DEFAULT_CPM_MIN/MAX`, `DEFAULT_BUDGET_MIN/MAX`, `ALLOWED_CREATIVE_DURATIONS`, date offsets, image dims, CPM Gaussian params, age ranges, and `DECIMAL`.

### Mapping and validation
- Money stored as cents (integers) in ORM; Decimal used in schemas.
- Targeting keys are validated from `TargetingKey`; factories emit uppercase keys/values.
- Mime types enforced via `CreativeMimeType`.
- Validators use `DEFAULT_CPM_MIN/MAX` for bounds.

### CLI commands
- `init-db`: create SQLite tables.
- `create-advertiser [--auto | --name --email --brand --agency]`.
- `create-campaign --advertiser-id <id> [--auto]`.

### Makefile targets
- `make deps` / `make install`: create `.venv` and install deps (includes `colorlog`).
- `make init-db`: initialize schema.
- `make run`: full demo (init-db → create advertiser → create campaign).
- `make run-colorlog`: same as run, with `LOG_LEVEL=INFO` to showcase colorized logging.
- `make test`, `make test-one FILE=...`: run tests.
- `make clean`: remove DB and venv/cache artifacts.

### Testing
- 15 tests; run `make test`. Validates:
  - Env overrides for config/logger
  - CLI exit codes and JSON outputs
  - ORM schema integrity (timestamps, cents columns, FKs)
  - Enum and targeting key expectations

### Usage
```bash
make deps
make init-db
python cli.py create-advertiser --auto
python cli.py create-campaign --advertiser-id 1 --auto

# or with colorized logging
make run-colorlog
```

### Future enhancements
- Metrics simulation and reporting commands
- Structured JSON logging and richer log contexts
- Configurable Faker profiles (awareness/consideration/conversion)
# generate-ads-data
