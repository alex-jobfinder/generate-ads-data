#!/usr/bin/env python3
"""
PyIceberg SQLite Catalog Demo

This script demonstrates how to set up and use PyIceberg with a SQLite catalog,
including creating tables, loading data, performing operations, and querying with snapshots.

Based on the article: "PyIceberg — Trying out the SQLite Catalog" by Tyler White
"""

import ibis
import pandas as pd
from pyiceberg.catalog import load_catalog
from pyiceberg.expressions import EqualTo


def main():
    print("🚀 PyIceberg SQLite Catalog Demo")
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
    
    # Step 7: Delete droids to create a new snapshot
    print("\n🤖 Deleting droids to demonstrate snapshots...")
    table.delete(EqualTo("species", "Droid"))
    final_count = table.inspect.partitions()["record_count"][0].as_py()
    print(f"Record count after deleting droids: {final_count}")
    print(f"Droids removed: {new_count - final_count}")
    
    # Step 8: Query with different snapshots
    print("\n🔍 Querying with different snapshots...")
    
    # Query latest snapshot (without droids)
    latest_data = table.scan(selected_fields=("name", "species")).to_pandas()
    print(f"Latest snapshot - Characters with species info: {len(latest_data)}")
    print("Top 5 characters from latest snapshot:")
    print(latest_data.head())
    
    # Query previous snapshot (with droids) if available
    if len(snapshots) > 1:
        previous_snapshot_id = snapshots[0].snapshot_id
        previous_data = table.scan(
            selected_fields=("name", "species"), 
            snapshot_id=previous_snapshot_id
        ).to_pandas()
        print(f"\nPrevious snapshot - Characters with species info: {len(previous_data)}")
        print("Top 5 characters from previous snapshot (including droids):")
        print(previous_data.head())
    
    # Step 9: Demonstrate DuckDB integration
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
    
    print("\n✅ Demo completed successfully!")
    print("\nKey features demonstrated:")
    print("- SQLite catalog setup and configuration")
    print("- Table creation and data loading")
    print("- Snapshot functionality and time travel")
    print("- Data deletion with snapshot preservation")
    print("- DuckDB integration for analytics")
    print("- PyArrow table integration")


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


if __name__ == "__main__":
    main()
