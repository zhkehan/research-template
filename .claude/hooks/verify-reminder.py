#!/usr/bin/env python3
"""
Verification Reminder Hook (BRAIN edition)

Non-blocking reminder that fires on Write/Edit to research output files
(.tex, .do, .py) to remind about compiling/running before marking a task done.

Hook Event: PostToolUse (matcher: "Write|Edit")
Returns: Exit code 0 (non-blocking)

Skips: config files, markdown notes, data files, .claude/ internals
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

# Files that need verification after editing
VERIFY_EXTENSIONS = {
    ".tex": "compile with xelatex before marking done",
    ".do":  "run in Stata to verify output",
    ".py":  "run to verify output (if data/analysis script)",
}

# Extensions to always skip
SKIP_EXTENSIONS = [
    ".md", ".txt", ".rst", ".bib", ".cls", ".sty",
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg",
    ".lock", ".env", ".gitignore",
    ".svg", ".png", ".jpg", ".pdf", ".dta", ".csv",
]

# Directories to always skip
SKIP_DIRS = [
    "/.claude/", "/memory/", "/00-MOC/", "/01-Inbox/",
    "/02-System/", "/03-现实/", "/04-Projects/", "/05-模板/",
    "/06-Life/", "/07-Archive/", "/templates/",
]


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

    now = time.time()
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

    tool_input = hook_input.get("tool_input", {})
    file_path  = tool_input.get("file_path", "")

    if not file_path or should_skip(file_path):
        return 0

    suffix = Path(file_path).suffix.lower()
    action = VERIFY_EXTENSIONS.get(suffix)
    if not action:
        return 0

    if was_recently_reminded(file_path):
        return 0

    filename = Path(file_path).name
    print(f"\n{CYAN}Verification reminder:{NC} {filename}")
    print(f"   → {GREEN}{action}{NC}\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
