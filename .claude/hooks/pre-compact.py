#!/usr/bin/env python3
"""
pre-compact.py — PreCompact Hook
Saves a session snapshot to .claude/session-state.md before context compression.
"""

import json
import sys
import os
from datetime import datetime

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    summary    = data.get("summary", "")
    session_id = data.get("session_id", "unknown")
    timestamp  = datetime.now().strftime("%Y-%m-%d %H:%M")

    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    state_file   = os.path.join(project_root, ".claude", "session-state.md")

    content = f"""# Session State Snapshot

> Auto-saved by pre-compact hook before context compression.
> Session: {session_id} | Time: {timestamp}

## What Claude Was Doing

{summary if summary else "(No summary available — check conversation history)"}

## Resume Checklist

When context is restored, Claude should:
- [ ] Re-read `PLAN.md` for data inventory and pipeline state
- [ ] Re-read `config.py` for paths and manifests
- [ ] Check `logs/` for most recent validation log
- [ ] Ask user to confirm current task if unclear

---
*This file is overwritten on each compression.*
"""

    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    with open(state_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[pre-compact] Session state saved ({timestamp})", file=sys.stderr)

if __name__ == "__main__":
    main()
