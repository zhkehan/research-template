#!/usr/bin/env python3
"""
setup.py — Project Template Setup Script
Run once after cloning research-template to customize for a new project.
Replaces all {{PLACEHOLDER}} tokens in all text files, then removes itself.

Usage:
    python setup.py --name MyPaper --root "C:/path/to/MyPaper"
"""

import argparse
import os
from datetime import date
from pathlib import Path

PLACEHOLDER_EXTENSIONS = {
    ".py", ".md", ".txt", ".json", ".yaml", ".yml", ".sql", ".cfg", ".ini",
}


def main():
    parser = argparse.ArgumentParser(description="Set up a new academic project from template")
    parser.add_argument("--name", required=True, help="Project name, e.g. HousingInequality")
    parser.add_argument("--root", required=True, help="Absolute root path of this project")
    args = parser.parse_args()

    replacements = {
        "{{PROJECT_NAME}}":  args.name,
        "{{PROJECT_LOWER}}": args.name.lower(),
        "{{ROOT_PATH}}":     args.root,
        "{{TODAY}}":         date.today().isoformat(),
    }

    root       = Path(__file__).parent
    setup_path = Path(__file__).resolve()

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

    print(f"\n=== Project '{args.name}' configured ===")
    print(f"Root: {args.root}")
    print("\nNext steps:")
    print("  1. Fill in PROJECT.md: research question, identification, data schemas")
    print("  2. git init && git add -A && git commit -m 'init'")
    print("  3. Create GitHub repo and push: git remote add origin <url> && git push -u origin main")
    print("  4. Add data sources under code/data_prepare/ as needed")

    os.remove(setup_path)


if __name__ == "__main__":
    main()
