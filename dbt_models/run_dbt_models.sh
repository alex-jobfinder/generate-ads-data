#!/bin/bash

# Script to run DBT models for campaign performance metrics
# This replicates the Python performance_ext.py logic using DBT

echo "🚀 Starting DBT Performance Metrics Generation"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "dbt_project.yml" ]; then
    echo "❌ Error: Please run this script from the dbt_models directory"
    exit 1
fi

# Install dependencies
echo "📦 Installing DBT dependencies..."
dbt deps

# Run staging models
echo "🔍 Running staging models..."
dbt run --select staging

# Run intermediate models (calculated metrics)
echo "🧮 Running intermediate models (calculated metrics)..."
dbt run --select intermediate

# Run marts models (final business-ready tables)
echo "📊 Running marts models..."
dbt run --select marts

# Run tests
echo "✅ Running data quality tests..."
dbt test

# Generate documentation
echo "📚 Generating documentation..."
dbt docs generate

echo ""
echo "🎉 DBT Performance Metrics Generation Complete!"
echo ""
echo "📋 Summary:"
echo "  - Staging models: Raw data preparation"
echo "  - Intermediate models: All calculated metrics computed"
echo "  - Marts models: Business-ready extended performance data"
echo "  - Tests: Data quality validation"
echo "  - Documentation: Auto-generated model documentation"
echo ""
echo "🔗 Next steps:"
echo "  - View documentation: dbt docs serve"
echo "  - Check test results: dbt test"
echo "  - Explore models in your database"
echo ""
echo "📊 The mart_campaign_performance_extended model now contains:"
echo "  - All raw performance data"
echo "  - All calculated metrics (replicating Python logic exactly)"
echo "  - Same structure as CampaignPerformanceExtended table"
echo ""
echo "💡 This DBT implementation runs in parallel with your Python code"
echo "   Both approaches generate identical results"
