# MetricFlow Testing Framework

This document explains how to test and validate that MetricFlow is working correctly with dbt-duckdb in your project.

## 🧪 Test Files Created

### 1. **`tests/test_metricflow_integration.py`** - Comprehensive Python Tests
- **TestMetricFlowIntegration**: Tests core MetricFlow functionality
- **TestMetricFlowCommands**: Tests dbt semantic layer commands
- **Coverage**: Installation, connectivity, semantic models, metrics, DuckDB operations

### 2. **`test_metricflow.sh`** - Quick Validation Script
- Fast checks without relying on `dbt sl`
- Parses semantic YAML via `dbt-semantic-interfaces`
- Builds semantic model with `dbt seed` + `dbt run`
- Verifies aggregates directly in DuckDB

### 3. **`pytest.ini`** - Test Configuration
- **Pytest configuration** for consistent test execution
- **Test markers** for organizing and filtering tests
- **Output formatting** for better readability

## 🚀 Quick Start Testing

### Option 1: Run the Quick Test Script
```bash
# From project root
./test_metricflow.sh
```

This will:
- ✅ Check dbt installation
- ✅ Verify dbt-duckdb adapter
- ✅ Validate MetricFlow installation
- ✅ Test semantic layer commands
- ✅ Verify DuckDB connectivity
- ✅ Check Python dependencies

### Option 2: Run Python Tests with pytest
```bash
# Run all tests
pytest tests/ -v

# Run only MetricFlow tests
pytest tests/ -m metricflow -v

# Run only dbt tests
pytest tests/ -m dbt -v

# Run only DuckDB tests
pytest tests/ -m duckdb -v

# Run specific test class
pytest tests/test_metricflow_integration.py::TestMetricFlowIntegration -v

# Run specific test method
pytest tests/test_metricflow_integration.py::TestMetricFlowIntegration::test_dbt_installation -v
```

### Option 3: Run Tests Directly
```bash
# Run the test file directly
python tests/test_metricflow_integration.py
```

## 🎯 What the Tests Validate

### **Core Integration Tests**
1. **dbt Installation**: Verifies dbt is properly installed
2. **dbt-duckdb Adapter**: Confirms DuckDB adapter is available
3. **MetricFlow Installation**: Optionally checks MetricFlow import
4. **Semantic Layer Parsing**: Validates semantic YAML via Python API

### **Functionality Tests**
5. **DuckDB Connection**: Tests dbt can connect to DuckDB
6. **dbt Parse**: Validates dbt project parsing
7. **Semantic Build**: Builds semantic model table via dbt
8. **Metric Checks**: Verifies aggregates via DuckDB SQL

### **Dependency Tests**
9. **Python Packages**: Verifies required packages (duckdb, pandas, pydantic)
10. **DuckDB Direct**: Tests direct DuckDB operations

## 🔧 Test Configuration

### **Test Markers**
- `@pytest.mark.metricflow`: MetricFlow-specific tests
- `@pytest.mark.dbt`: dbt-specific tests
- `@pytest.mark.duckdb`: DuckDB-specific tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.unit`: Unit tests

### **Test Fixtures**
- `dbt_project_dir`: Path to dbt project
- `test_data`: Sample campaign performance data
- Automatic cleanup of test files and database objects

## 📊 Expected Test Results

### **✅ Success Indicators**
- All dbt commands execute successfully
- DuckDB connections work
- MetricFlow commands are available
- Semantic layer validation passes
- Python packages import correctly

### **⚠️ Expected Warnings**
- `dbt sl validate` might fail if no semantic models exist (normal)
- `dbt parse` might fail if no models exist (normal)

### **❌ Failure Indicators**
- dbt command not found
- dbt-duckdb adapter missing
- MetricFlow not installed
- DuckDB connection failures
- Missing Python packages

## 🛠️ Troubleshooting

### **Common Issues**

#### 1. **dbt Command Not Found**
```bash
# Ensure Poetry environment is active
source activate_env.sh

# Check dbt installation
poetry show dbt-duckdb
```

#### 2. **MetricFlow Not Found**
```bash
# Check MetricFlow installation
poetry run pip show dbt-metricflow

# Reinstall if needed
poetry run pip install dbt-metricflow
```

#### 3. **DuckDB Connection Failed**
```bash
# Check dbt profiles
cd dbt_models
dbt debug

# Verify profiles.yml configuration
cat profiles.yml
```

#### 4. **Python Package Import Errors**
```bash
# Check installed packages
poetry show

# Install missing packages
poetry add package-name
```

### **Debug Commands**
```bash
# Check Poetry environment
poetry env info

# Check dbt version and adapters
dbt --version

# Test dbt connection
cd dbt_models && dbt debug

# Test semantic layer parsing via Python
python -c "from dbt_semantic_interfaces.parsing.dir_to_model import parse_yaml_files_to_semantic_manifest as p; print(p(['dbt_models/models/semantic_layer/semantic_models.yml']))"
```

## 🚀 Advanced Testing

### **Custom Test Data**
Modify the `test_data` fixture in `test_metricflow_integration.py` to test different scenarios:

```python
@pytest.fixture(scope="class")
def test_data(self):
    """Create custom test data"""
    return pd.DataFrame({
        'campaign_id': [1, 2, 3],
        'impressions': [1000, 1500, 800],
        'clicks': [50, 75, 40],
        'spend': [100.0, 150.0, 80.0],
        'date': ['2024-01-01', '2024-01-01', '2024-01-01']
    })
```

### **Adding New Tests**
Create new test methods in the test classes:

```python
def test_custom_functionality(self):
    """Test custom MetricFlow functionality"""
    # Your test logic here
    assert True
```

### **Test Isolation**
Each test method is isolated and cleans up after itself:
- Test files are created and removed
- Database objects are cleaned up
- No persistent side effects

## 📚 Next Steps After Testing

Once tests pass:

1. **Create Semantic Models**: Define your data structure
2. **Define Metrics**: Create business metrics
3. **Validate Configuration**: Use `dbt sl validate`
4. **Query Metrics**: Use `dbt sl query`
5. **Integrate with BI Tools**: Connect downstream applications

## 🎉 Success Criteria

Your MetricFlow integration is working correctly when:

- ✅ All tests pass
- ✅ `dbt sl` commands work
- ✅ Semantic layer validation succeeds
- ✅ Metric queries execute
- ✅ DuckDB operations work
- ✅ No import or dependency errors

---

**Run `./test_metricflow.sh` to quickly validate your setup!** 🚀
