"""
Project: {{PROJECT_NAME}}
File:    scripts/06_build_duckdb.py
Purpose: Register Parquet views in {{PROJECT_LOWER}}.duckdb and create column_catalog.
         Idempotent — safe to re-run at any time.
Author:  Kehan
Date:    {{TODAY}}
"""
import sys
from datetime import datetime
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import DUCKDB_PATH, LOGS, ALL_MANIFESTS

LOGS.mkdir(parents=True, exist_ok=True)


def main():
    print(f"=== Building {DUCKDB_PATH.name} — {datetime.now():%Y-%m-%d %H:%M:%S} ===\n")
    con = duckdb.connect(str(DUCKDB_PATH))

    # Create column_catalog table
    con.execute("""
        CREATE TABLE IF NOT EXISTS column_catalog (
            table_name      VARCHAR NOT NULL,
            column_name     VARCHAR NOT NULL,
            description     VARCHAR NOT NULL,
            dtype_parquet   VARCHAR NOT NULL,
            example_values  VARCHAR NOT NULL,
            null_rate_pct   DOUBLE,
            source_format   VARCHAR NOT NULL,
            notes           VARCHAR NOT NULL,
            alt_column_name VARCHAR,
            PRIMARY KEY (table_name, column_name)
        )
    """)
    print("[OK] column_catalog table ready")

    # Register one view per manifest
    for manifest in ALL_MANIFESTS:
        dst_dir: Path  = manifest["dst"]
        view_name      = dst_dir.name
        parts          = list(dst_dir.glob("part_*.parquet"))

        if not parts:
            print(f"[SKIP] View '{view_name}' — no parts in {dst_dir}")
            continue

        glob_expr = str(dst_dir / "part_*.parquet").replace("\\", "/")
        con.execute(f"""
            CREATE OR REPLACE VIEW {view_name} AS
            SELECT * FROM read_parquet('{glob_expr}')
        """)
        n = con.execute(f"SELECT COUNT(*) FROM {view_name}").fetchone()[0]
        print(f"[OK] View '{view_name}' — {n:,} rows")

    # TODO: Populate column_catalog with INSERT OR REPLACE entries
    # after running conversion and validation steps.

    n_catalog = con.execute("SELECT COUNT(*) FROM column_catalog").fetchone()[0]
    print(f"\n[OK] column_catalog — {n_catalog} entries")
    con.close()
    print(f"\nDatabase: {DUCKDB_PATH}")


if __name__ == "__main__":
    main()
