"""
Project: {{PROJECT_NAME}}
File:    scripts/05_validate_parquet.py
Purpose: Five-layer validation of converted Parquet files
Author:  Kehan
Date:    {{TODAY}}
"""
import sys
from datetime import datetime
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import LOGS, ALL_MANIFESTS, PARQUET

LOGS.mkdir(parents=True, exist_ok=True)
log_path = LOGS / f"validation_{datetime.now():%Y%m%d}.txt"
RESULTS  = []


def check(label: str, passed: bool, detail: str = ""):
    status = "PASS" if passed else "FAIL"
    line   = f"[{status}] {label}"
    if detail:
        line += f" — {detail}"
    RESULTS.append(line)
    print(line)
    return passed


def run():
    con        = duckdb.connect(database=":memory:")
    all_passed = True

    for manifest in ALL_MANIFESTS:
        dst_dir: Path = manifest["dst"]
        name          = dst_dir.name
        parts         = list(dst_dir.glob("part_*.parquet"))

        # Layer 1: Parts exist
        ok = check(f"L1 parts_exist [{name}]", len(parts) > 0,
                   f"{len(parts)} part files found")
        if not ok:
            all_passed = False
            continue

        glob_expr = str(dst_dir / "part_*.parquet").replace("\\", "/")

        # Layer 2: Row count > 0
        n_rows = con.execute(
            f"SELECT COUNT(*) FROM read_parquet('{glob_expr}')"
        ).fetchone()[0]
        ok = check(f"L2 row_count [{name}]", n_rows > 0, f"{n_rows:,} rows")
        if not ok:
            all_passed = False
            continue

        # Layer 3: String ID columns are non-null
        for col, dtype in manifest.get("dtypes", {}).items():
            if dtype == str:
                null_n = con.execute(
                    f"SELECT COUNT(*) FROM read_parquet('{glob_expr}') "
                    f"WHERE {col} IS NULL OR TRIM({col}) = ''"
                ).fetchone()[0]
                ok = check(f"L3 {col}_not_null [{name}]", null_n == 0,
                           f"{null_n:,} null/empty values")
                all_passed = all_passed and ok

        # Layer 4: Output files inside PARQUET dir
        ok = check(f"L4 output_in_parquet_dir [{name}]",
                   str(dst_dir).startswith(str(PARQUET)),
                   str(dst_dir))
        all_passed = all_passed and ok

        # Layer 5: No duplicate part numbers
        part_nums = [int(p.stem.split("_")[1]) for p in parts]
        ok = check(f"L5 no_duplicate_parts [{name}]",
                   len(part_nums) == len(set(part_nums)),
                   f"{len(parts)} parts, {len(set(part_nums))} unique")
        all_passed = all_passed and ok

    con.close()
    return all_passed


if __name__ == "__main__":
    print(f"=== Parquet Validation — {datetime.now():%Y-%m-%d %H:%M:%S} ===\n")
    passed = run()

    with open(log_path, "w") as f:
        f.write(f"Parquet Validation\nRun: {datetime.now()}\n\n")
        for line in RESULTS:
            f.write(line + "\n")
        f.write(f"\nOverall: {'PASS' if passed else 'FAIL'}\n")

    print(f"\nOverall: {'PASS' if passed else 'FAIL'}")
    print(f"Log: {log_path}")

    if not passed:
        print("\n[ERROR] Validation failed. Fix before running 06_build_duckdb.py.")
        sys.exit(1)
