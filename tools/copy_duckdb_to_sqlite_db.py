# import duckdb

# con = duckdb.connect("/home/alex/dbt_ads/z_dbt_ads_perf/dbt_refactor/dbt_refactor.duckdb")

# # Attach SQLite
# con.execute("ATTACH 'z_replica.sqlite' (TYPE SQLITE)")

# # Get attached DB alias
# aliases = con.execute("PRAGMA show_databases").fetchall()
# print("Databases:", aliases)
# sqlite_alias = aliases[-1][0]  # likely 'replica'

# # Copy all tables from DuckDB main schema to SQLite
# tables = con.execute("""
#     SELECT table_name
#     FROM information_schema.tables
#     WHERE table_schema='main'
# """).fetchall()

# for (table_name,) in tables:
#     con.execute(f'CREATE TABLE {sqlite_alias}."{table_name}" AS SELECT * FROM "{table_name}"')
#     print(f"Copied table: {table_name}")


# con.close()
# print("Replication complete.")







import argparse
import duckdb


def main() -> int:
    parser = argparse.ArgumentParser(description="Copy all DuckDB main tables into a SQLite database")
    parser.add_argument(
        "--duckdb",
        default="/home/alex/dbt_ads/z_dbt_ads_perf/dbt_refactor/dbt_refactor.duckdb",
        help="Path to DuckDB database file",
    )
    parser.add_argument(
        "--sqlite",
        default="/home/alex/dbt_ads/z_dbt_ads_perf/final_DDL/dbt_sp_v4.db",
        help="Path to destination SQLite database file",
    )
    args = parser.parse_args()

    con = duckdb.connect(args.duckdb)
    try:
        # Attach SQLite under alias 'replica' (DuckDB expects AS before TYPE)
        alias = 'replica'
        try:
            con.execute(f"ATTACH '{args.sqlite}' AS {alias} (TYPE SQLITE)")
        except Exception:
            # Fallback: attach without alias, then discover alias via PRAGMA
            con.execute(f"ATTACH '{args.sqlite}' (TYPE SQLITE)")
            aliases = con.execute("PRAGMA show_databases").fetchall()
            alias = aliases[-1][0]

        # Copy all tables from DuckDB main schema to SQLite, replacing if exist
        tables = con.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='main'
            """
        ).fetchall()

        for (table_name,) in tables:
            con.execute(f'DROP TABLE IF EXISTS {alias}."{table_name}"')
            con.execute(f'CREATE TABLE {alias}."{table_name}" AS SELECT * FROM "{table_name}"')
            print(f"Copied table: {table_name}")
    finally:
        con.close()
    print("Replication complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())




# import sqlite3
# import pandas as pd

# sqlite_path = "z_replica.sqlite"
# conn = sqlite3.connect(sqlite_path)

# # Step 1: Load titles
# df = pd.read_sql("SELECT rowid, title FROM stg_imdb WHERE title IS NOT NULL", conn)

# # Step 2: Franchise detection via substring match
# titles_lower = df["title"].str.lower()
# is_franchise_flags = [0] * len(df)

# for i, t in enumerate(titles_lower):
#     for j, other in enumerate(titles_lower):
#         if i != j and t in other:
#             is_franchise_flags[i] = 1
#             is_franchise_flags[j] = 1

# df["is_franchise"] = is_franchise_flags

# # Step 3: Add column if not exists
# try:
#     conn.execute("ALTER TABLE stg_imdb ADD COLUMN is_franchise INTEGER DEFAULT 0")
# except sqlite3.OperationalError:
#     # Column already exists, skip adding
#     pass

# # Step 4: Write back results
# for rowid, flag in zip(df["rowid"], df["is_franchise"]):
#     conn.execute("UPDATE stg_imdb SET is_franchise = ? WHERE rowid = ?", (flag, rowid))

# conn.commit()
# conn.close()

# print("✅ Franchise flag added based on substring matches.")
