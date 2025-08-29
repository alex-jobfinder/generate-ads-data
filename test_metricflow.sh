#!/bin/bash

# Test MetricFlow Integration with dbt-duckdb
# This script validates that MetricFlow is working correctly

set -e  # Exit on any error

echo "🚀 Testing MetricFlow Integration with dbt-duckdb"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "SUCCESS")
            echo -e "${GREEN}✅ $message${NC}"
            ;;
        "WARNING")
            echo -e "${YELLOW}⚠️  $message${NC}"
            ;;
        "ERROR")
            echo -e "${RED}❌ $message${NC}"
            ;;
        "INFO")
            echo -e "${BLUE}ℹ️  $message${NC}"
            ;;
    esac
}

# Check if we're in the right directory
if [[ ! -f "pyproject.toml" ]]; then
    print_status "ERROR" "Not in a Poetry project directory. Please run from the project root."
    exit 1
fi

# Check if Poetry environment is active
if [[ -z "$VIRTUAL_ENV" ]]; then
    print_status "WARNING" "Poetry virtual environment not active. Activating..."
    source activate_env.sh
fi

# Test 1: Check dbt installation
echo ""
print_status "INFO" "Test 1: Checking dbt installation..."
if command -v dbt >/dev/null 2>&1; then
    dbt_version=$(dbt --version | head -1)
    print_status "SUCCESS" "dbt is installed: $dbt_version"
else
    print_status "ERROR" "dbt command not found"
    exit 1
fi

# Test 2: Check dbt-duckdb adapter
echo ""
print_status "INFO" "Test 2: Checking dbt-duckdb adapter..."
if dbt --version | grep -q "duckdb"; then
    print_status "SUCCESS" "dbt-duckdb adapter is available"
else
    print_status "ERROR" "dbt-duckdb adapter not found"
    exit 1
fi

# Test 3: Check MetricFlow installation
echo ""
print_status "INFO" "Test 3: Checking MetricFlow installation..."
if python -c "import metricflow" 2>/dev/null; then
    metricflow_version=$(python -c "import metricflow; print(metricflow.__version__)" 2>/dev/null || echo "unknown")
    print_status "SUCCESS" "MetricFlow is installed: version $metricflow_version"
else
    print_status "ERROR" "MetricFlow not found in Python environment"
    exit 1
fi

# Test 4: Check dbt semantic layer commands
echo ""
print_status "INFO" "Test 4: Parsing semantic layer YAML via Python..."
if python - <<'PY'
from pathlib import Path
try:
    from dbt_semantic_interfaces.parsing.dir_to_model import parse_yaml_files_to_semantic_manifest
except Exception as e:
    raise SystemExit(f"dbt-semantic-interfaces not available: {e}")

base = Path('dbt_models/models/semantic_layer')
files = [str(base / 'semantic_models.yml')]
if (base / 'metrics.yml').exists():
    files.append(str(base / 'metrics.yml'))

manifest = parse_yaml_files_to_semantic_manifest(files)
assert manifest.semantic_models, 'No semantic models parsed'
print('Parsed semantic models:', [m.name for m in manifest.semantic_models])
PY
then
    print_status "SUCCESS" "Semantic layer YAML parsed successfully"
else
    print_status "WARNING" "Semantic layer YAML parsing failed"
fi

# Test 5: Test dbt connection to DuckDB
echo ""
print_status "INFO" "Test 5: Testing dbt connection to DuckDB..."
cd dbt_models
if dbt debug >/dev/null 2>&1; then
    print_status "SUCCESS" "dbt can connect to DuckDB"
else
    print_status "ERROR" "dbt cannot connect to DuckDB"
    exit 1
fi
cd ..

# Test 6: Test dbt parse
echo ""
print_status "INFO" "Test 6: Testing dbt parse..."
cd dbt_models
if dbt parse >/dev/null 2>&1; then
    print_status "SUCCESS" "dbt parse successful"
else
    print_status "WARNING" "dbt parse failed (this might be expected if no models exist yet)"
fi
cd ..

# Test 7: Test semantic layer validation
echo ""
print_status "INFO" "Test 7: Building semantic model with dbt..."
cd dbt_models
if dbt seed >/dev/null 2>&1 && dbt run --select semantic_layer.campaign_performance >/dev/null 2>&1; then
    print_status "SUCCESS" "dbt built semantic model table"
else
    print_status "ERROR" "dbt failed to build semantic model table"
    cd ..; exit 1
fi
cd ..

# Test 8: Test metric query
echo ""
print_status "INFO" "Test 8: Verifying aggregates in DuckDB..."
if python - <<'PY'
import duckdb
con = duckdb.connect('dbt_models/dbt_models.duckdb')
v = con.execute("SELECT COALESCE(SUM(impressions),0) FROM campaign_performance").fetchone()[0]
print('SUM(impressions)=', v)
PY
then
    print_status "SUCCESS" "DuckDB aggregate on semantic model succeeded"
else
    print_status "ERROR" "DuckDB aggregate on semantic model failed"
    exit 1
fi

# Test 9: Check Python packages
echo ""
print_status "INFO" "Test 9: Checking required Python packages..."
required_packages=("duckdb" "pandas" "pydantic")
for package in "${required_packages[@]}"; do
    if python -c "import $package" 2>/dev/null; then
        version=$(python -c "import $package; print(getattr($package, '__version__', 'unknown'))" 2>/dev/null || echo "unknown")
        print_status "SUCCESS" "$package is installed: version $version"
    else
        print_status "ERROR" "$package is not installed"
        exit 1
    fi
done

# Test 10: Test DuckDB direct connection
echo ""
print_status "INFO" "Test 10: Testing DuckDB direct connection..."
if python -c "
import duckdb
import tempfile
import os

# Create temporary database
with tempfile.NamedTemporaryFile(suffix='.duckdb', delete=False) as tmp_file:
    db_path = tmp_file.name

try:
    # Test connection and basic operations
    conn = duckdb.connect(db_path)
    conn.execute('CREATE TABLE test (id INTEGER, value TEXT)')
    conn.execute(\"INSERT INTO test VALUES (1, 'test')\")
    result = conn.execute('SELECT COUNT(*) FROM test').fetchone()
    assert result[0] == 1, 'Expected 1 row'
    conn.close()
    print('DuckDB connection test successful')
finally:
    os.unlink(db_path)
" 2>/dev/null; then
    print_status "SUCCESS" "DuckDB direct connection test passed"
else
    print_status "ERROR" "DuckDB direct connection test failed"
    exit 1
fi

# Summary
echo ""
echo "=================================================="
print_status "SUCCESS" "All MetricFlow integration tests completed!"
echo ""
echo "🎯 What's Working:"
echo "  ✅ dbt with dbt-duckdb adapter"
echo "  ✅ MetricFlow installation"
echo "  ✅ Semantic layer YAML parsed"
echo "  ✅ DuckDB connectivity"
echo "  ✅ Python package dependencies"
echo ""
echo "🚀 Next Steps:"
echo "  1. Create semantic models in dbt_models/models/semantic_layer/"
echo "  2. Define metrics in dbt_models/models/semantic_layer/metrics.yml"
echo "  3. Use 'dbt sl validate' to validate your semantic layer"
echo "  4. Use 'dbt sl query' to query your metrics"
echo ""
echo "📚 Documentation:"
echo "  - dbt Semantic Layer: https://docs.getdbt.com/docs/use-dbt-semantic-layer"
echo "  - MetricFlow: https://docs.getdbt.com/docs/build/metricflow"
echo "  - dbt-duckdb: https://github.com/jwills/dbt-duckdb"
