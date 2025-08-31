#!/usr/bin/env python3
"""
PyIceberg SQLite Catalog Basic Demo

This script demonstrates the basic setup and usage of PyIceberg with a SQLite catalog,
focusing on core functionality that works reliably.
"""

import ibis
import pandas as pd
from pyiceberg.catalog import load_catalog


def main():
    print("🚀 PyIceberg SQLite Catalog Basic Demo")
    print("=" * 50)
    
    # Step 1: Load the starwars data using Ibis
    print("\n📊 Loading StarWars dataset...")
    starwars = ibis.examples.starwars.fetch().to_pyarrow()
    print(f"Loaded {len(starwars)} characters from StarWars dataset")
    print(f"Schema: {starwars.schema}")
    
    # Step 2: Connect to the catalog
    print("\n🔗 Connecting to SQLite catalog...")
    catalog = load_catalog("default")
    print("✅ Connected to catalog successfully")
    
    # Step 3: Create namespace and table
    print("\n📁 Creating namespace and table...")
    catalog.create_namespace_if_not_exists("default")
    catalog.create_table_if_not_exists("default.starwars", starwars.schema)
    print("✅ Table 'default.starwars' created")
    
    # Step 4: Load table and check initial state
    print("\n📋 Loading table and checking initial state...")
    table = catalog.load_table("default.starwars")
    
    # Check if table has any snapshots (data)
    try:
        initial_count = table.inspect.partitions()["record_count"][0].as_py()
        print(f"Initial record count: {initial_count}")
    except ValueError:
        print("Initial record count: 0 (empty table)")
        initial_count = 0
    
    # Step 5: Append data to the table
    print("\n📝 Appending StarWars data to table...")
    table.append(starwars)
    new_count = table.inspect.partitions()["record_count"][0].as_py()
    print(f"New record count: {new_count}")
    
    # Step 6: Demonstrate snapshot functionality
    print("\n📸 Snapshot information:")
    snapshots = table.snapshots()
    print(f"Number of snapshots: {len(snapshots)}")
    for i, snapshot in enumerate(snapshots):
        print(f"  Snapshot {i+1}: {snapshot.snapshot_id}")
    
    # Step 7: Show table metadata
    print("\n📊 Table metadata:")
    print(f"Table name: {table.identifier}")
    print(f"Table location: {table.location()}")
    print(f"Table schema: {table.schema()}")
    
    # Step 8: Demonstrate DuckDB integration for analytics
    print("\n🦆 Demonstrating DuckDB integration...")
    
    # Count species using DuckDB
    con = ibis.duckdb.connect()
    species_counts = count_species(catalog, con)
    print("Species counts:")
    print(species_counts)
    
    # Count homeworlds using DuckDB
    homeworld_counts = count_homeworlds(catalog, con)
    print("\nHomeworld counts:")
    print(homeworld_counts)
    
    # Step 9: Show some sample data using DuckDB
    print("\n📋 Sample data from the table:")
    sample_data = get_sample_data(catalog, con)
    print(sample_data)
    
    print("\n✅ Demo completed successfully!")
    print("\nKey features demonstrated:")
    print("- SQLite catalog setup and configuration")
    print("- Table creation and data loading")
    print("- Snapshot functionality")
    print("- DuckDB integration for analytics")
    print("- PyArrow table integration")
    print("- Table metadata inspection")


def count_species(catalog, connection):
    """Count species using DuckDB integration"""
    table = catalog.load_table("default.starwars")
    table.scan(selected_fields=(["species"])).to_duckdb(
        "starwars_species", connection=connection.con
    )
    expr = (
        connection.table("starwars_species")
        .group_by("species")
        .aggregate(species_count=_.species.count())
        .order_by(_.species_count.desc())
        .limit(10)
    )
    return expr.to_pandas()


def count_homeworlds(catalog, connection):
    """Count homeworlds using DuckDB integration"""
    table = catalog.load_table("default.starwars")
    table.scan(selected_fields=(["homeworld"])).to_duckdb(
        "starwars_homeworlds", connection=connection.con
    )
    expr = (
        connection.table("starwars_homeworlds")
        .group_by("homeworld")
        .aggregate(homeworld_count=_.homeworld.count())
        .order_by(_.homeworld_count.desc())
        .limit(10)
    )
    return expr.to_pandas()


def get_sample_data(catalog, connection):
    """Get sample data using DuckDB integration"""
    table = catalog.load_table("default.starwars")
    table.scan(selected_fields=(["name", "species", "homeworld"])).to_duckdb(
        "starwars_sample", connection=connection.con
    )
    expr = connection.table("starwars_sample").limit(10)
    return expr.to_pandas()


if __name__ == "__main__":
    main()
