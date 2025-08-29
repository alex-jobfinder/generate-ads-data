#!/usr/bin/env python3
"""
Test script to verify DuckDB setup and DBT configuration.
Run this after setup_duckdb.py to ensure everything is working.
"""

import duckdb
import os
from pathlib import Path

def test_duckdb_setup():
    """Test that DuckDB is set up correctly with data."""
    
    current_dir = Path(__file__).parent
    duckdb_path = current_dir.parent / "ads.duckdb"
    
    print(f"🧪 Testing DuckDB setup...")
    print(f"   Database path: {duckdb_path}")
    
    if not duckdb_path.exists():
        print(f"❌ Error: DuckDB database not found at {duckdb_path}")
        print("   Please run setup_duckdb.py first")
        return False
    
    try:
        # Connect to DuckDB
        conn = duckdb.connect(str(duckdb_path))
        
        # Test basic connection
        print("✅ DuckDB connection successful")
        
        # Get list of tables
        result = conn.execute("SHOW TABLES").fetchall()
        tables = [row[0] for row in result]
        
        print(f"📋 Found {len(tables)} tables:")
        for table in tables:
            print(f"   - {table}")
        
        # Test campaign_performance table specifically
        if 'campaign_performance' in tables:
            print("✅ campaign_performance table found")
            
            # Check row count
            result = conn.execute("SELECT COUNT(*) FROM campaign_performance").fetchone()
            row_count = result[0]
            print(f"   📊 Row count: {row_count}")
            
            # Check sample data
            result = conn.execute("SELECT * FROM campaign_performance LIMIT 3").fetchall()
            if result:
                print("✅ Sample data accessible")
                print(f"   📝 Sample rows: {len(result)}")
            else:
                print("⚠️  Table appears to be empty")
        else:
            print("❌ campaign_performance table not found")
            return False
        
        # Test DBT configuration
        print("\n🔧 Testing DBT configuration...")
        
        # Check if dbt_project.yml exists
        dbt_project = current_dir / "dbt_project.yml"
        if dbt_project.exists():
            print("✅ dbt_project.yml found")
        else:
            print("❌ dbt_project.yml not found")
            return False
        
        # Check if profiles.yml exists
        profiles = current_dir / "profiles.yml"
        if profiles.exists():
            print("✅ profiles.yml found")
        else:
            print("❌ profiles.yml not found")
            return False
        
        # Check if macros exist
        macros_dir = current_dir / "macros"
        if macros_dir.exists():
            macro_files = list(macros_dir.glob("*.sql"))
            print(f"✅ Macros directory found with {len(macro_files)} macro files")
        else:
            print("❌ Macros directory not found")
            return False
        
        # Check if models exist
        models_dir = current_dir / "models"
        if models_dir.exists():
            model_files = list(models_dir.rglob("*.sql"))
            print(f"✅ Models directory found with {len(model_files)} model files")
        else:
            print("❌ Models directory not found")
            return False
        
        conn.close()
        
        print("\n🎉 All tests passed! Your DBT setup is ready.")
        print("\n🚀 Next steps:")
        print("   1. Run: dbt deps")
        print("   2. Run: dbt run")
        print("   3. Run: dbt test")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing setup: {e}")
        return False

if __name__ == "__main__":
    success = test_duckdb_setup()
    if not success:
        print("\n❌ Setup test failed. Please check the error messages above.")
        print("   You may need to run setup_duckdb.py first.")
