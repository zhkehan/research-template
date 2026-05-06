# {{PROJECT_NAME}} — PLAN.md

## Overview

[One paragraph: what this project studies, what data it uses, current status.]
Data not yet migrated; update `config.py` source paths when data arrives.

---

## Data Inventory

| Dataset | Codebook | Format | Grain | Key ID |
|---------|----------|--------|-------|--------|
| {{DATASET_NAME}} | ? | pipe-delimited .txt | ? | ? |

---

## Source File Naming Conventions

```
# UPDATE when data arrives: document the actual filename pattern here
```

---

## Key Variable Reference

### {{DATASET_NAME}}

| Variable | Type | Description |
|----------|------|-------------|
| ?        | str  | ?           |

---

## Derived Variables

| Variable | Source | Logic |
|----------|--------|-------|
| ?        | ?      | ?     |

---

## Known Data Quirks

- [ ] Document encoding issues, FIPS recodes, state exclusions, duplicate handling, etc.

---

## DuckDB Catalog Plan

| View name | Parquet path | Description |
|-----------|-------------|-------------|
| {{DATASET_LOWER}} | `parquet/{{DATASET_LOWER}}/` | ? |

---

## Pipeline Execution Order

```
01_convert_{{DATASET_LOWER}}.py    # Source → Parquet
05_validate_parquet.py             # Five-layer validation
06_build_duckdb.py                 # Register views + column_catalog
```

---

## Progress Log

- **{{TODAY}}**: Project skeleton created. Data not yet migrated.
