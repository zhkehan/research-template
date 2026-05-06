"""
Project: {{PROJECT_NAME}}
File:    config.py
Purpose: Centralized path configuration and conversion settings
Author:  Kehan
Date:    {{TODAY}}
"""
from pathlib import Path

# ── Root ──────────────────────────────────────────────────────────────────────
ROOT    = Path(r"{{ROOT_PATH}}")
PARQUET = ROOT / "parquet"
LOGS    = ROOT / "logs"

# ── Source data directories ───────────────────────────────────────────────────
# UPDATE THESE when data is copied to this machine.
RAW_{{DATASET_UPPER}} = ROOT / "raw" / "{{DATASET_LOWER}}"
# Add one RAW_* variable per additional dataset.

# ── Manifest ──────────────────────────────────────────────────────────────────
# One entry per source dataset. Update src, glob, dtypes when data arrives.
{{DATASET_UPPER}}_MANIFEST = {
    "src":    RAW_{{DATASET_UPPER}},
    "dst":    PARQUET / "{{DATASET_LOWER}}",
    "glob":   "*.txt",          # UPDATE: actual filename pattern
    "dtypes": {},               # UPDATE: columns that must stay string (e.g., {"id": str})
    "desc":   "{{PROJECT_NAME}} — {{DATASET_NAME}} ({{TODAY[:4]}})",
}

ALL_MANIFESTS = [
    {{DATASET_UPPER}}_MANIFEST,
    # Add more manifests here
]

# ── Conversion settings ───────────────────────────────────────────────────────
DELIMITER              = "|"          # UPDATE if not pipe-delimited
CSV_CHUNK_ROWS         = 2_000_000   # reduce to 500_000 if OOM
PARQUET_COMPRESSION    = "snappy"
PARQUET_ROW_GROUP_SIZE = 1_000_000
ROWS_PER_PART          = 10_000_000

# ── DuckDB ────────────────────────────────────────────────────────────────────
DUCKDB_PATH = ROOT / "{{PROJECT_LOWER}}.duckdb"
