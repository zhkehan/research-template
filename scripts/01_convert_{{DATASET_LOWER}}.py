"""
Project: {{PROJECT_NAME}}
File:    scripts/01_convert_{{DATASET_LOWER}}.py
Purpose: Convert {{DATASET_NAME}} source files to Parquet
Author:  Kehan
Date:    {{TODAY}}
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import (
    LOGS, ALL_MANIFESTS, PARQUET, PARQUET_COMPRESSION,
    PARQUET_ROW_GROUP_SIZE, ROWS_PER_PART, CSV_CHUNK_ROWS, DELIMITER,
)


def process_file(src_file: Path, dst_dir: Path, part_counter: list) -> int:
    """Read one source file and append rows to Parquet parts."""
    assert str(dst_dir).startswith(str(PARQUET)), "Output path outside PARQUET directory"
    dst_dir.mkdir(parents=True, exist_ok=True)

    rows_written = 0
    buffer       = []
    buffer_rows  = 0

    # TODO: Replace with correct reader for your source format.
    # pipe-delimited txt:  pd.read_csv(src_file, sep=DELIMITER, dtype=str, ...)
    # SAS:                 pyreadstat.read_file_in_chunks(src_file, chunksize=...)
    # Parquet:             pq.ParquetFile(src_file).iter_batches(batch_size=...)
    reader = pd.read_csv(
        src_file,
        sep=DELIMITER,
        dtype=str,
        low_memory=False,
        chunksize=CSV_CHUNK_ROWS,
        on_bad_lines="warn",
        encoding="latin-1",
    )

    for chunk in reader:
        chunk.columns = chunk.columns.str.lower().str.strip()

        # TODO: filter columns, apply recodes, enforce dtypes
        # chunk = chunk[KEEP_COLS].copy()

        buffer.append(chunk)
        buffer_rows  += len(chunk)
        rows_written += len(chunk)

        if buffer_rows >= ROWS_PER_PART:
            _flush(buffer, dst_dir, part_counter)
            buffer      = []
            buffer_rows = 0

    if buffer:
        _flush(buffer, dst_dir, part_counter)

    return rows_written


def _flush(buffer: list, dst_dir: Path, part_counter: list):
    df        = pd.concat(buffer, ignore_index=True)
    part_path = dst_dir / f"part_{part_counter[0]:04d}.parquet"
    table     = pa.Table.from_pandas(df, preserve_index=False)
    pq.write_table(
        table, part_path,
        compression=PARQUET_COMPRESSION,
        row_group_size=PARQUET_ROW_GROUP_SIZE,
    )
    part_counter[0] += 1


def main():
    parser = argparse.ArgumentParser(description="Convert source files to Parquet")
    parser.add_argument("--name",   help="Process only this table (matches manifest desc)")
    parser.add_argument("--resume", action="store_true", help="Skip tables already converted")
    args = parser.parse_args()

    LOGS.mkdir(parents=True, exist_ok=True)
    log_path   = LOGS / f"01_convert_{datetime.now():%Y%m%d_%H%M%S}.log"
    total_rows = 0

    with open(log_path, "w") as log:
        log.write(f"Start: {datetime.now()}\n\n")

        for manifest in ALL_MANIFESTS:
            if args.name and args.name not in manifest["desc"]:
                continue

            src_dir: Path = manifest["src"]
            dst_dir: Path = manifest["dst"]

            if args.resume and any(dst_dir.glob("part_*.parquet")):
                print(f"[SKIP] {dst_dir.name} — already converted")
                continue

            if not src_dir.exists():
                print(f"[ERROR] Source not found: {src_dir}")
                print("        Update config.py when data is migrated.")
                continue

            src_files   = sorted(src_dir.glob(manifest["glob"]))
            existing    = sorted(dst_dir.glob("part_*.parquet")) if dst_dir.exists() else []
            part_counter = [len(existing)]

            for src_file in tqdm(src_files, desc=dst_dir.name):
                n = process_file(src_file, dst_dir, part_counter)
                total_rows += n
                log.write(f"{src_file.name}: {n:,} rows\n")

        log.write(f"\nTotal: {total_rows:,} rows\nEnd: {datetime.now()}\n")

    print(f"\nDone. {total_rows:,} total rows. Log: {log_path}")


if __name__ == "__main__":
    main()
