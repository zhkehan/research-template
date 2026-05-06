#!/usr/bin/env python3
"""
verify-reminder.py — PostToolUse Hook
Non-blocking reminder after writing/editing Python pipeline scripts
to run them and verify output before marking a task done.

Hook Event: PostToolUse (matcher: "Write|Edit")
"""

from __future__ import annotations

import json
import os
import sys
import time
import hashlib
from pathlib import Path

CYAN  = "\033[0;36m"
GREEN = "\033[0;32m"
NC    = "\033[0m"

VERIFY_EXTENSIONS = {
    ".py": "run to verify output (if conversion/validation script)",
}

SKIP_EXTENSIONS = [
    ".md", ".txt", ".rst", ".json", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".lock", ".env", ".gitignore",
    ".png", ".jpg", ".pdf", ".parquet", ".dta", ".csv",
]

SKIP_DIRS = ["/.claude/", "/logs/", "/parquet/"]


def get_cache_file() -> Path:
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    key = hashlib.md5(project_dir.encode()).hexdigest()[:8] if project_dir else "default"
    cache_dir = Path.home() / ".claude" / "sessions" / key
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / "verify-reminder-cache.json"


def should_skip(file_path: str) -> bool:
    path = Path(file_path)
    if path.suffix.lower() in SKIP_EXTENSIONS:
        return True
    for skip_dir in SKIP_DIRS:
        if skip_dir in file_path.replace("\\", "/"):
            return True
    return False


def was_recently_reminded(file_path: str) -> bool:
    cache_file = get_cache_file()
    try:
        cache = json.loads(cache_file.read_text()) if cache_file.exists() else {}
    except (json.JSONDecodeError, IOError):
        cache = {}
    now  = time.time()
    last = cache.get(file_path, 0)
    cache[file_path] = now
    cache = {k: v for k, v in cache.items() if now - v < 300}
    try:
        cache_file.write_text(json.dumps(cache))
    except IOError:
        pass
    return (now - last) < 60


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError):
        return 0

    file_path = hook_input.get("tool_input", {}).get("file_path", "")
    if not file_path or should_skip(file_path):
        return 0

    suffix = Path(file_path).suffix.lower()
    action = VERIFY_EXTENSIONS.get(suffix)
    if not action:
        return 0

    if was_recently_reminded(file_path):
        return 0

    print(f"\n{CYAN}Verification reminder:{NC} {Path(file_path).name}")
    print(f"   → {GREEN}{action}{NC}\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
