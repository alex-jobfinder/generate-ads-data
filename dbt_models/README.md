# DBT Performance Metrics - Extended Campaign Performance

This DBT project replicates the calculated metrics logic from `services/performance_ext.py` using SQL transformations instead of Python. It generates the same extended performance metrics that populate the `campaign_performance_extended` table.

## 🚨 **Important Setup Note**

**If you encounter the error "No module named 'dbt.adapters.sqlite'"**, this means the SQLite adapter isn't installed. We've provided multiple solutions:

### **Solution 1: Use DuckDB (Recommended)**
1. Install DuckDB: `pip install duckdb`
2. Run the setup script: `python setup_duckdb.py`
3. This will copy your SQLite data to DuckDB for DBT processing

### **Solution 2: Install dbt-sqlite package**
```bash
pip install dbt-sqlite
```

### **Solution 3: Use alternative database**
See `profiles_alternatives.yml` for PostgreSQL, DuckDB, or other options.

## Project Structure

```
dbt_models/
├── dbt_project.yml              # DBT project configuration
├── profiles.yml                 # Database connection profiles (DuckDB)
├── profiles_alternatives.yml    # Alternative database configurations
├── packages.yml                 # External DBT packages
├── requirements.txt             # Python dependencies for setup
├── setup_duckdb.py             # Script to copy SQLite → DuckDB
├── macros/                     # Reusable SQL macros
│   ├── safe_division.sql       # Safe division (handles division by zero)
│   └── avg_watch_time_seconds.sql # Average watch time calculation
├── models/
│   ├── staging/                # Raw data staging
│   │   ├── stg_campaign_performance.sql
│   │   └── sources.yml
│   ├── intermediate/           # Calculated metrics
│   │   └── int_campaign_performance_calculated.sql
│   └── marts/                 # Final business-ready models
│       ├── mart_campaign_performance_extended.sql
│       └── schema.yml
├── tests/                      # Data quality tests
├── README.md                   # Comprehensive documentation
└── run_dbt_models.sh          # Execution script
```

## Key Features

### 1. **Exact Logic Replication**
All calculated metrics from the Python `ExtendedPerformanceMetrics` class are replicated exactly:

- **Fill Rate Extended**: `eligible_impressions / requests`
- **Viewability Rate**: `viewable_impressions / impressions`
- **Audibility Rate**: `audible_impressions / impressions`
- **Video Start Rate**: `video_start / impressions`
- **Video Completion Rate**: `video_q100 / video_start`
- **Video Skip Rate Extended**: `skips / video_start`
- **QR Scan Rate**: `qr_scans / impressions`
- **Interactive Rate**: `interactive_engagements / impressions`
- **Effective CPM**: `(spend * 1000) / impressions`
- **Average Watch Time**: Estimated from video quartiles using weighted segments
- **Auction Win Rate**: `auctions_won / eligible_impressions`
- **Error Rate**: `error_count / requests`
- **Timeout Rate**: `timeout_count / requests`
- **Supply Funnel Efficiency**: `eligible_impressions / requests`
- **CTR Recalculated**: `clicks / impressions`

### 2. **Safe Division Handling**
The `safe_division` macro handles division by zero gracefully, returning 0.0 when the denominator is zero or null.

### 3. **Complex Watch Time Calculation**
The `avg_watch_time_seconds` macro replicates the Python logic for estimating average watch time from video quartile data using weighted segments.

### 4. **Data Quality Tests**
Comprehensive testing for:
- Data type validation
- Range checks (e.g., rates between 0.0 and 1.0)
- Referential integrity
- Business logic constraints

## 🚀 **Quick Start (DuckDB Approach)**

### Prerequisites
- DBT Core installed: `pip install dbt-core`
- DuckDB: `pip install duckdb`
- Python 3.7+

### Setup Steps

1. **Navigate to the DBT project directory:**
   ```bash
   cd dbt_models
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up DuckDB from your existing SQLite data:**
   ```bash
   python setup_duckdb.py
   ```

4. **Install DBT dependencies:**
   ```bash
   dbt deps
   ```

5. **Run all models:**
   ```bash
   dbt run
   ```

6. **Run tests:**
   ```bash
   dbt test
   ```

7. **Generate documentation:**
   ```bash
   dbt docs generate
   dbt docs serve
   ```

### Alternative: Use the provided script
```bash
./run_dbt_models.sh
```

## Usage

### Running Specific Models

```bash
# Run only staging models
dbt run --select staging

# Run only intermediate models (calculated metrics)
dbt run --select intermediate

# Run only marts models
dbt run --select marts

# Run models with specific tags
dbt run --select tag:performance
```

### Running Tests

```bash
# Run all tests
dbt test

# Run tests for specific models
dbt test --select mart_campaign_performance_extended

# Run tests with specific tags
dbt test --select tag:performance
```

## Model Dependencies

```
stg_campaign_performance
    ↓
int_campaign_performance_calculated
    ↓
mart_campaign_performance_extended
```

## Data Flow

1. **Setup**: SQLite → DuckDB (via setup script)
2. **Staging**: Raw data from `campaign_performance` table
3. **Intermediate**: All calculated metrics computed using macros
4. **Marts**: Final business-ready model matching `CampaignPerformanceExtended` structure

## Comparison with Python Implementation

| Python Function | DBT Equivalent | Notes |
|----------------|----------------|-------|
| `safe_div()` | `safe_division()` macro | Handles division by zero |
| `avg_watch_time_seconds` property | `avg_watch_time_seconds()` macro | Weighted quartile calculation |
| All computed fields | SQL CASE statements + macros | Direct SQL translation |

## Benefits of DBT Approach

1. **Declarative**: SQL-based transformations are easier to understand and maintain
2. **Version Control**: All logic is tracked in Git
3. **Testing**: Built-in data quality testing
4. **Documentation**: Auto-generated documentation from schema files
5. **Lineage**: Clear data lineage tracking
6. **Reusability**: Macros can be reused across models
7. **Performance**: SQL transformations can be optimized by the database engine

## Troubleshooting

### Common Issues

1. **"No module named 'dbt.adapters.sqlite'"**
   - Use DuckDB approach (recommended)
   - Or install dbt-sqlite package

2. **"Database connection failed"**
   - Check profiles.yml configuration
   - Ensure database file exists
   - Verify file permissions

3. **"Macro not found"**
   - Run `dbt deps` to install dependencies
   - Check macro file paths

### Getting Help

- Check DBT logs for detailed error messages
- Verify database connection in profiles.yml
- Ensure all required packages are installed

## Maintenance

- **Adding new metrics**: Add to the intermediate model and update schema documentation
- **Modifying calculations**: Update the relevant macro or SQL logic
- **Data source changes**: Update the staging model and sources.yml

## Notes

- This DBT implementation runs in parallel with the existing Python code
- Both approaches generate identical results
- The DBT models can be used for analytics, reporting, and downstream consumption
- The Python code remains the source of truth for the application layer
- DuckDB approach provides better compatibility and performance than SQLite
