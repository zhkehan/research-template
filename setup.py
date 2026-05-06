#!/usr/bin/env python3
"""
setup.py — Project Template Setup Script
Run once after cloning research-template to customize for a new project.
Replaces all {{PLACEHOLDER}} tokens, renames templated files, then removes itself.

Usage:
    python setup.py --name MyProject --root "C:/path/to/MyProject" [--datasets "TableA, TableB"]
"""

import argparse
import os
import re
import shutil
from datetime import date
from pathlib import Path


PLACEHOLDER_EXTENSIONS = {
    ".py", ".md", ".txt", ".json", ".yaml", ".yml", ".sql", ".cfg", ".ini",
}


def main():
    parser = argparse.ArgumentParser(description="Set up a new research project from template")
    parser.add_argument("--name",     required=True, help="Project name, e.g. HousingMarkets")
    parser.add_argument("--root",     required=True, help="Absolute root path of this project")
    parser.add_argument("--datasets", default="",    help="Comma-separated dataset names (data-pipeline only)")
    args = parser.parse_args()

    project_name = args.name
    root_path    = args.root.replace("\\", "\\\\")  # escape for Python string in config.py
    today        = date.today().isoformat()

    datasets = [d.strip() for d in args.datasets.split(",") if d.strip()] if args.datasets else []
    primary  = datasets[0] if datasets else "source_data"

    replacements = {
        "{{PROJECT_NAME}}":  project_name,
        "{{PROJECT_LOWER}}": project_name.lower(),
        "{{ROOT_PATH}}":     args.root,
        "{{ROOT_PATH_ESC}}": root_path,
        "{{TODAY}}":         today,
        "{{DATASET_LOWER}}": primary.lower().replace(" ", "_"),
        "{{DATASET_UPPER}}": primary.upper().replace(" ", "_"),
        "{{DATASET_NAME}}":  primary.replace("_", " ").title(),
    }

    root = Path(__file__).parent
    setup_path = Path(__file__).resolve()

    # ── Step 1: Replace content in text files ─────────────────────────────────
    for path in sorted(root.rglob("*")):
        if path.resolve() == setup_path:
            continue
        if ".git" in path.parts:
            continue
        if not path.is_file():
            continue
        if path.suffix not in PLACEHOLDER_EXTENSIONS and path.name not in {".gitkeep", ".gitignore"}:
            continue
        try:
            content = path.read_text(encoding="utf-8")
            new_content = content
            for ph, val in replacements.items():
                new_content = new_content.replace(ph, val)
            if new_content != content:
                path.write_text(new_content, encoding="utf-8")
        except (UnicodeDecodeError, IOError):
            pass

    # ── Step 2: Rename files/dirs that contain {{DATASET_LOWER}} ─────────────
    # Process deepest paths first to avoid renaming parent before child
    all_paths = sorted(root.rglob("*{{DATASET_LOWER}}*"), key=lambda p: len(p.parts), reverse=True)
    for path in all_paths:
        if ".git" in path.parts:
            continue
        new_name = path.name.replace("{{DATASET_LOWER}}", replacements["{{DATASET_LOWER}}"])
        path.rename(path.parent / new_name)

    # ── Step 3: Duplicate convert script for additional datasets ─────────────
    if len(datasets) > 1:
        scripts_dir = root / "scripts"
        primary_script = scripts_dir / f"01_convert_{replacements['{{DATASET_LOWER}}']}.py"
        if primary_script.exists():
            for i, dataset in enumerate(datasets[1:], start=2):
                ds_lower = dataset.lower().replace(" ", "_")
                ds_upper = dataset.upper().replace(" ", "_")
                ds_name  = dataset.replace("_", " ").title()
                dest = scripts_dir / f"0{i}_convert_{ds_lower}.py"
                content = primary_script.read_text(encoding="utf-8")
                content = content.replace(replacements["{{DATASET_LOWER}}"], ds_lower)
                content = content.replace(replacements["{{DATASET_UPPER}}"], ds_upper)
                content = content.replace(replacements["{{DATASET_NAME}}"],  ds_name)
                dest.write_text(content, encoding="utf-8")

    # ── Step 4: Print summary and remove self ─────────────────────────────────
    print(f"\n=== Project '{project_name}' configured ===")
    print(f"Root:     {args.root}")
    if datasets:
        print(f"Datasets: {', '.join(datasets)}")
    print("\nNext steps:")
    if (root / "config.py").exists():
        print("  1. Update config.py: set RAW_* paths to actual source data locations")
        print("  2. Fill in PLAN.md: data inventory, variable reference, known quirks")
        print("  3. python scripts/01_convert_*.py --resume")
        print("  4. python scripts/05_validate_parquet.py")
        print("  5. python scripts/06_build_duckdb.py")
    else:
        print("  1. Fill in PROJECT.md: research question, data schemas, milestones")
        print("  2. git init && git add -A && git commit -m 'init'")

    os.remove(setup_path)


if __name__ == "__main__":
    main()
