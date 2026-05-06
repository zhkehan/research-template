# {{PROJECT_NAME}} — Claude Code Configuration

> **Read `PLAN.md` first.** It contains the full data inventory, variable
> reference, known quirks, and pipeline execution order.

---

## Before Any Session

1. Read `PLAN.md` — data inventory, variable reference, known quirks.
2. Read `config.py` — all paths and manifests.
3. Check `logs/` for most recent validation log.
4. If `{{PROJECT_LOWER}}.duckdb` exists, query `column_catalog` for pipeline state.

---

## Absolute Rules

1. **ID columns must stay strings** — never coerce to int/float. Check `dtypes`
   in each manifest entry in `config.py`.
2. **Output path safety**: always assert `str(dst).startswith(str(PARQUET))`
   before writing any file.
3. **Source data is read-only** — never modify, overwrite, or delete files in
   `RAW_*` directories.
4. **All output goes to `PARQUET/`** — never write processed files elsewhere.
5. **Run `05_validate_parquet.py` and confirm PASS before running `06_build_duckdb.py`.**

---

## Pipeline Scripts

| Script | Status | Purpose |
|--------|--------|---------|
| `scripts/01_convert_{{DATASET_LOWER}}.py` | Stub — fill in data reading logic | Source → Parquet |
| `scripts/05_validate_parquet.py` | Ready | Five-layer validation |
| `scripts/06_build_duckdb.py` | Ready | Register views + column_catalog |

Run order:
```bash
python scripts/01_convert_{{DATASET_LOWER}}.py --resume
python scripts/05_validate_parquet.py
python scripts/06_build_duckdb.py
```

---

## Git Policy

Never commit anything under `raw/` or `parquet/`.
Only commit: `.py`, `.md`, `.txt` (requirements), `.sql`.
