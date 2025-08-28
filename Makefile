VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: venv install deps setup init-db run-config-seed seed-5x5-no-init clean test

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install "sqlalchemy>=2" "click>=8" "pydantic[email]>=2" "faker>=19" "pytest>=7" "colorlog>=6" "pyyaml>=6" "rich>=13"

deps: install

init-db: deps
	$(PY) cli.py init-db

setup: init-db
	@echo "Environment ready."

# Initialize DB, load config.yml, then seed 5x5 with performance
run-config-seed: init-db
	$(PY) cli.py create-from-config --path "config.yml" --generate-performance
	@for i in $$(seq 1 5); do \
	  ADV_ID=$$($(PY) -c 'import json,subprocess; p=subprocess.run(["$(PY)","cli.py","create-advertiser","--auto"], capture_output=True, text=True, check=True); print(json.loads(p.stdout)["advertiser_id"])'); \
	  echo "Created Advertiser $$i => ID=$$ADV_ID"; \
	  for j in $$(seq 1 5); do \
	    $(PY) cli.py create-campaign --advertiser-id $$ADV_ID --auto --generate-performance; \
	  done; \
	  echo "---"; \
	done

# Seed 5x5 without resetting DB (no init) - WITH performance generation
seed-5x5-no-init: deps
	@for i in $$(seq 1 5); do \
	  ADV_ID=$$($(PY) -c 'import json,subprocess; p=subprocess.run(["$(PY)","cli.py","create-advertiser","--auto"], capture_output=True, text=True, check=True); print(json.loads(p.stdout)["advertiser_id"])'); \
	  echo "Created Advertiser $$i => ID=$$ADV_ID"; \
	  for j in $$(seq 1 5); do \
	    $(PY) cli.py create-campaign --advertiser-id $$ADV_ID --auto --generate-performance; \
	  done; \
	  echo "---"; \
	done

# NEW: 5x5 seeding with batch performance generation (all-in-one command)
seed-5x5-batch: deps
	$(PY) cli.py create-from-config --seed-5x5 --generate-performance --performance-type both

# NEW: 5x5 seeding with normal performance only (batch inserts)
seed-5x5-normal: deps
	$(PY) cli.py create-from-config --seed-5x5 --generate-performance --performance-type normal

# NEW: 5x5 seeding with extended performance only (batch inserts)
seed-5x5-extended: deps
	$(PY) cli.py create-from-config --seed-5x5 --generate-performance --performance-type extended

# NEW: 5x5 seeding with custom seed for reproducible data
seed-5x5-reproducible: deps
	$(PY) cli.py create-from-config --seed-5x5 --generate-performance --performance-type both --seed 42

# NEW: Fresh setup with config + 5x5 + batch performance
run-config-seed-5x5: init-db
	$(PY) cli.py create-from-config --path "config.yml" --generate-performance
	$(PY) cli.py create-from-config --seed-5x5 --generate-performance --performance-type both

test: deps
	$(PY) -m pytest -q

clean:
	rm -f ads.db ads_p0.db ads_p0.db-shm ads_p0.db-wal
	rm -rf __pycache__ .pytest_cache $(VENV)

# # All tests passing
# make clean              # Clean up
# make init-db            # Reset database	
# make test

# # Streamlined workflow
# make run-config-seed    # Fresh setup with config + performance
# make seed-5x5-no-init   # Add more data with performance
# make clean              # Clean up
# make init-db            # Reset database	

# ===== NEW 5x5 SEEDING WITH BATCH PERFORMANCE =====
# These commands use the new CLI with batch insert optimization for SQLite
#
# make seed-5x5-batch          # 5x5 + both performance types (batch inserts)
# make seed-5x5-normal         # 5x5 + normal performance only (batch inserts)  
# make seed-5x5-extended       # 5x5 + extended performance only (batch inserts)
# make seed-5x5-reproducible   # 5x5 + both performance types + seed=42 (batch inserts)
# make run-config-seed-5x5     # Fresh DB + config + 5x5 + both performance types
#
# Performance benefits:
# - Normal performance: Uses services/performance.py with batch inserts
# - Extended performance: Uses services/performance_ext.py with batch inserts  
# - SQLite optimized: Single transaction per performance type instead of 25 individual
# - Faster execution: Especially noticeable for longer campaign flights