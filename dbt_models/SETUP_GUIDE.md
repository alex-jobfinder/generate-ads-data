# 🚀 DBT Setup Guide - Resolving Database Adapter Issues

This guide will help you resolve the "No module named 'dbt.adapters.sqlite'" error and get your DBT performance metrics working.

## 🚨 **The Problem**

When you ran the DBT models, you encountered this error:
```
Error importing adapter: No module named 'dbt.adapters.sqlite'
```

This happens because:
1. DBT doesn't include SQLite support by default
2. The `dbt-sqlite` package needs to be installed separately
3. SQLite support in DBT is limited

## ✅ **Recommended Solution: Use DuckDB**

We'll use DuckDB instead, which:
- ✅ Is fully supported by DBT
- ✅ Has better performance than SQLite
- ✅ Handles larger datasets efficiently
- ✅ Is more compatible with modern analytics workflows

## 🛠️ **Step-by-Step Setup**

### **Step 1: Install Dependencies**

```bash
# Navigate to DBT project directory
cd dbt_models

# Install Python dependencies
pip install duckdb dbt-core

# Or use requirements.txt
pip install -r requirements.txt
```

### **Step 2: Set Up DuckDB from Your SQLite Data**

```bash
# Run the setup script to copy SQLite → DuckDB
python setup_duckdb.py
```

This script will:
- Read your existing `ads.db` SQLite database
- Create a new `ads.duckdb` database
- Copy all tables and data
- Preserve the exact schema and data types

### **Step 3: Verify Setup**

```bash
# Test that everything is working
python test_setup.py
```

You should see:
- ✅ DuckDB connection successful
- ✅ Tables found and accessible
- ✅ Sample data readable
- ✅ DBT configuration files present

### **Step 4: Install DBT Dependencies**

```bash
# Install external DBT packages
dbt deps
```

### **Step 5: Run DBT Models**

```bash
# Run all models
dbt run

# Or use the provided script
./run_dbt_models.sh
```

## 🔧 **Alternative Solutions**

### **Option A: Install dbt-sqlite Package**

If you prefer to stick with SQLite:

```bash
pip install dbt-sqlite
```

Then update `profiles.yml`:
```yaml
ads_performance_metrics:
  target: dev
  outputs:
    dev:
      type: sqlite
      path: "../ads.db"
      schema: main
```

### **Option B: Use PostgreSQL**

If you have PostgreSQL available:

1. Install: `pip install dbt-postgres`
2. Update `profiles.yml` with your PostgreSQL credentials
3. Create a new database for the performance metrics

### **Option C: Use In-Memory DuckDB (Testing Only)**

For quick testing without persistent storage:

```yaml
ads_performance_metrics:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: ":memory:"
      schema: main
```

## 📊 **What the Setup Script Does**

The `setup_duckdb.py` script:

1. **Connects** to your existing SQLite database (`ads.db`)
2. **Discovers** all tables and their schemas
3. **Creates** corresponding tables in DuckDB
4. **Copies** all data row by row
5. **Preserves** data types and relationships
6. **Verifies** the copy was successful

## 🧪 **Testing Your Setup**

After running the setup script, test with:

```bash
# Test DuckDB connection
python test_setup.py

# Test DBT configuration
dbt debug

# Test model compilation
dbt compile

# Run a single model
dbt run --select stg_campaign_performance
```

## 🚨 **Troubleshooting Common Issues**

### **Issue 1: "duckdb module not found"**
```bash
pip install duckdb
```

### **Issue 2: "ads.db not found"**
- Ensure you're in the `dbt_models` directory
- Verify `ads.db` exists in the parent directory
- Check file permissions

### **Issue 3: "Permission denied"**
```bash
chmod +x setup_duckdb.py
chmod +x test_setup.py
chmod +x run_dbt_models.sh
```

### **Issue 4: "DBT command not found"**
```bash
pip install dbt-core
# Or
pip install --user dbt-core
```

## 📁 **File Structure After Setup**

```
dbt_models/
├── ads.duckdb              # ← New DuckDB database (created by setup)
├── setup_duckdb.py         # Setup script
├── test_setup.py           # Test script
├── profiles.yml            # DuckDB configuration
├── dbt_project.yml         # DBT project config
└── ... (other DBT files)
```

## 🔄 **Data Flow**

```
Your SQLite ads.db
        ↓
setup_duckdb.py (copies data)
        ↓
New DuckDB ads.duckdb
        ↓
DBT models process data
        ↓
Calculated metrics generated
```

## ✅ **Success Indicators**

You'll know everything is working when:

1. ✅ `python setup_duckdb.py` completes without errors
2. ✅ `python test_setup.py` shows all tests passing
3. ✅ `dbt run` executes successfully
4. ✅ You see new calculated metrics in your database

## 🎯 **Next Steps After Setup**

1. **Explore the models**: `dbt docs generate && dbt docs serve`
2. **Run tests**: `dbt test`
3. **Customize calculations**: Modify macros and models as needed
4. **Schedule runs**: Set up automated DBT runs
5. **Integrate with BI tools**: Connect to Tableau, Looker, etc.

## 💡 **Why This Approach Works**

- **No data loss**: Your original SQLite data remains untouched
- **Better performance**: DuckDB is faster for analytics workloads
- **Full DBT support**: All DBT features work without limitations
- **Easy migration**: Simple script handles the conversion
- **Reversible**: You can always go back to SQLite if needed

## 🆘 **Getting Help**

If you encounter issues:

1. Check the error messages carefully
2. Verify all dependencies are installed
3. Ensure file paths are correct
4. Run the test scripts to isolate issues
5. Check DBT logs for detailed error information

## 🎉 **You're Ready!**

Once setup is complete, you'll have:
- ✅ A working DBT environment
- ✅ All your performance data accessible
- ✅ Calculated metrics replicating Python logic exactly
- ✅ A foundation for advanced analytics and reporting

The DBT models will generate the same calculated metrics as your Python code, giving you two ways to compute performance metrics: your application layer and this analytics layer.
