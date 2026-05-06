#!/usr/bin/env python3
"""
pre-compact.py — PreCompact Hook
Runs before Claude Code compresses the conversation context.
Saves a session snapshot to .claude/session-state.md so key context
survives compression and can be referenced in the next context window.
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

    summary = data.get("summary", "")
    session_id = data.get("session_id", "unknown")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    state_file = os.path.join(project_root, ".claude", "session-state.md")

    content = f"""# Session State Snapshot

> Auto-saved by pre-compact hook before context compression.
> Session: {session_id} | Time: {timestamp}

## What Claude Was Doing

{summary if summary else "(No summary available — check conversation history)"}

## Resume Checklist

When context is restored, Claude should:
- [ ] Re-read `AI-CONTEXT.md` for system rules
- [ ] Check `00-MOC/Project Board.md` for active projects
- [ ] Review `memory/MEMORY.md` for learned patterns
- [ ] Ask user to confirm current task if unclear

---
*This file is overwritten on each compression. For permanent notes, use `/project:today`.*
"""

    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    with open(state_file, "w", encoding="utf-8") as f:
        f.write(content)

    # Output to stderr so it shows in Claude's console without affecting hook behavior
    print(f"[pre-compact] Session state saved to .claude/session-state.md ({timestamp})", file=sys.stderr)

if __name__ == "__main__":
    main()
