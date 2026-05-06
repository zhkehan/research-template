# Data Safety Rules

These rules are absolute — no exceptions.

## Source Data

- Source data is **read-only** — never modify, overwrite, or delete files in `RAW_*` directories
- Never pass source paths to any write operation
- If you need to inspect a source file, use `Read` or `pd.read_csv(..., nrows=100)` only

## Output Paths

- All output goes exclusively to the `PARQUET` directory defined in `config.py`
- Always assert before writing:
  ```python
  assert str(dst).startswith(str(PARQUET)), "Output path outside PARQUET directory"
  ```
- Never write processed files to `raw/`, `document/`, or project root

## ID Columns

- `clip` and `fipscode` must always be `str` — never coerce to int or float
- `clip` can be up to 52 characters; truncation causes silent data loss
- Always include these in the `dtypes` dict in each manifest entry

## State / FIPS Recodes

- Miami-Dade FIPS recode: always apply `12025 → 12086` (`FIPS_RECODE` in `config.py`)
- Vermont exclusion: no mortgage data for VT — exclude from mortgage-linked analyses

## Large State Warning

Do NOT run conversion scripts for very large states (CA, TX, FL, NY, PA, IL)
inside a Claude Code session without first checking file sizes.
Write the command and instruct the user to run it manually.

## Script Re-runs

- `06_build_duckdb.py` must be idempotent: views use `CREATE OR REPLACE`,
  catalog rows use `INSERT OR REPLACE`
- `05_validate_parquet.py` must pass before running `06_build_duckdb.py`
