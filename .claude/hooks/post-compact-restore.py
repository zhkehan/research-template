#!/usr/bin/env python3
"""
post-compact-restore.py — SessionStart Hook
Fires after compaction to restore context from session-state.md.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

CYAN   = "\033[0;36m"
GREEN  = "\033[0;32m"
YELLOW = "\033[0;33m"
NC     = "\033[0m"


def get_session_state(project_dir: str) -> str | None:
    state_file = Path(project_dir) / ".claude" / "session-state.md"
    if state_file.exists():
        content = state_file.read_text(encoding="utf-8").strip()
        if content and "(No summary available" not in content:
            return content
    return None


def get_recent_plan() -> dict | None:
    plans_dir = Path.home() / ".claude" / "plans"
    if not plans_dir.exists():
        return None
    plan_files = sorted(plans_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not plan_files:
        return None
    latest = plan_files[0]
    content = latest.read_text(encoding="utf-8")
    current_task = None
    for line in content.splitlines():
        if "- [ ]" in line:
            current_task = line.replace("- [ ]", "").strip()
            break
    return {"name": latest.name, "current_task": current_task}


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError):
        hook_input = {}

    if hook_input.get("source", "") not in ("compact", "resume"):
        return 0

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        return 0

    session_state = get_session_state(project_dir)
    plan_info     = get_recent_plan()

    if not session_state and not plan_info:
        return 0

    lines = [f"\n{CYAN}[Context Restored After Compaction]{NC}", ""]

    if session_state:
        lines.append(f"{GREEN}Last Session State:{NC}")
        for line in session_state.splitlines()[:20]:
            lines.append(f"  {line}")
        lines.append("")

    if plan_info:
        lines.append(f"{GREEN}Active Plan:{NC}")
        lines.append(f"  File: {plan_info['name']}")
        if plan_info.get("current_task"):
            lines.append(f"  Next task: {plan_info['current_task']}")
        lines.append("")

    lines.append(f"{YELLOW}Recovery Actions:{NC}")
    lines.append("  1. Re-read PLAN.md for data inventory and pipeline state")
    lines.append("  2. Re-read config.py for paths and manifests")
    lines.append("  3. Check logs/ for most recent validation log")
    lines.append("")

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
