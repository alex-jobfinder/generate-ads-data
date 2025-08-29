#!/usr/bin/env python3
"""
Setup script to copy data from SQLite to DuckDB for DBT processing.
This allows DBT to work with your existing data without changing the source database.
"""

import sqlite3
import duckdb
import os
from pathlib import Path

def setup_duckdb_from_sqlite():
    """Copy data from SQLite to DuckDB for DBT processing."""
    
    # Paths
    current_dir = Path(__file__).parent
    sqlite_path = current_dir.parent / "ads.db"
    duckdb_path = current_dir.parent / "ads.duckdb"
    
    print(f"🔍 Setting up DuckDB from SQLite database...")
    print(f"   SQLite source: {sqlite_path}")
    print(f"   DuckDB target: {duckdb_path}")
    
    # Check if SQLite database exists
    if not sqlite_path.exists():
        print(f"❌ Error: SQLite database not found at {sqlite_path}")
        print("   Please ensure you have generated the ads.db file first")
        return False
    
    try:
        # Connect to SQLite
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_conn.row_factory = sqlite3.Row
        
        # Connect to DuckDB
        duckdb_conn = duckdb.connect(str(duckdb_path))
        
        # Get list of tables from SQLite
        cursor = sqlite_conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"📋 Found {len(tables)} tables in SQLite:")
        for table in tables:
            print(f"   - {table}")
        
        # Copy each table
        for table in tables:
            print(f"📥 Copying table: {table}")
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            
            # Get data
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            
            if rows:
                # Create table in DuckDB with same schema
                column_defs = []
                for col in columns:
                    col_name = col[1]
                    col_type = col[2]
                    # Map SQLite types to DuckDB types
                    if col_type.upper() in ['INTEGER', 'INT']:
                        col_type = 'INTEGER'
                    elif col_type.upper() in ['REAL', 'FLOAT', 'DOUBLE']:
                        col_type = 'DOUBLE'
                    elif col_type.upper() in ['TEXT', 'VARCHAR', 'CHAR']:
                        col_type = 'VARCHAR'
                    elif col_type.upper() in ['BLOB']:
                        col_type = 'BLOB'
                    else:
                        col_type = 'VARCHAR'  # Default to VARCHAR for unknown types
                    
                    column_defs.append(f"{col_name} {col_type}")
                
                create_sql = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(column_defs)})"
                duckdb_conn.execute(create_sql)
                
                # Insert data
                if rows:
                    # Convert rows to list of tuples
                    data = [tuple(row) for row in rows]
                    placeholders = ', '.join(['?' for _ in columns])
                    insert_sql = f"INSERT INTO {table} VALUES ({placeholders})"
                    
                    # Clear existing data
                    duckdb_conn.execute(f"DELETE FROM {table}")
                    
                    # Insert new data
                    duckdb_conn.executemany(insert_sql, data)
                    
                    print(f"   ✅ Copied {len(rows)} rows")
                else:
                    print(f"   ⚠️  Table {table} is empty")
            else:
                print(f"   ⚠️  Table {table} is empty")
        
        # Close connections
        sqlite_conn.close()
        duckdb_conn.close()
        
        print(f"🎉 Successfully set up DuckDB database at {duckdb_path}")
        print(f"   You can now run DBT models using this database")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up DuckDB: {e}")
        return False

if __name__ == "__main__":
    success = setup_duckdb_from_sqlite()
    if success:
        print("\n🚀 Next steps:")
        print("   1. Run: cd dbt_models")
        print("   2. Run: python setup_duckdb.py")
        print("   3. Run: ./run_dbt_models.sh")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
