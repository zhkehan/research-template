---
paths:
  - "scripts/**/*.py"
---

# Task Completion Verification Protocol

**After writing or editing any pipeline script, Claude MUST verify the output works correctly.**

## For Conversion Scripts (`01_`–`04_convert_*.py`)

1. If the source data exists, run on a single small state first:
   ```bash
   python scripts/01_convert_owner_transfer.py --name <small_state>
   ```
2. Confirm at least one `part_0000.parquet` was created in the expected `dst` directory
3. Check file size is non-zero
4. Report row count from the log file

If source data is not yet available:
- Confirm the script imports without errors: `python -c "import scripts.01_... "` (or dry-run)
- Note that full verification must wait until data arrives

## For Validation Script (`05_validate_parquet.py`)

1. Run: `python scripts/05_validate_parquet.py`
2. Confirm all layers show `[PASS]`
3. Check `logs/validation_*.txt` exists and shows `Overall: PASS`
4. Do NOT proceed to `06_build_duckdb.py` if any layer fails

## For DuckDB Build Script (`06_build_duckdb.py`)

1. Run only after validation passes
2. Confirm `[OK] View '...'` lines printed for each table
3. Query spot-check:
   ```python
   import duckdb
   con = duckdb.connect("corelogic.duckdb")
   print(con.execute("SELECT COUNT(*) FROM column_catalog").fetchone())
   ```

## Common Pitfalls

- **Assuming success**: Always verify part files exist AND have non-zero size
- **Wrong working directory**: Run scripts from project root, not from `scripts/`
- **Missing dependencies**: Check import errors before declaring success
- **Output path drift**: Assert `str(dst).startswith(str(PARQUET))` before any write

## Verification Checklist

```
[ ] Script runs without import errors
[ ] Expected output files created with non-zero size
[ ] Row count matches expectation (or logged for later comparison)
[ ] No output written outside PARQUET directory
```
