#!/usr/bin/env python3
"""
context-monitor.py — PostToolUse Hook
Tracks cumulative tool calls per session as a proxy for context usage.
Prints a warning when approaching likely context limits.
Uses a counter file to persist count across tool calls within a session.
"""

import json
import sys
import os

# Thresholds for warnings
WARN_THRESHOLD = 40   # First warning
CRITICAL_THRESHOLD = 70  # Critical warning — consider wrapping up or compacting

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    session_id = data.get("session_id", "default")

    # Counter file location
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    counter_file = os.path.join(project_root, ".claude", f"_ctx_{session_id[:8]}.tmp")

    # Read and increment counter
    count = 0
    if os.path.exists(counter_file):
        try:
            with open(counter_file, "r") as f:
                count = int(f.read().strip())
        except Exception:
            count = 0

    count += 1

    with open(counter_file, "w") as f:
        f.write(str(count))

    # Print warnings at thresholds
    if count == WARN_THRESHOLD:
        print(
            f"\n⚠️  [context-monitor] {count} tool calls this session. "
            "Context window filling up — consider saving progress with `/project:today` "
            "or `/project:sync-heartbeat` before continuing.",
            file=sys.stderr
        )
    elif count == CRITICAL_THRESHOLD:
        print(
            f"\n🔴 [context-monitor] {count} tool calls — context nearing limit. "
            "Recommend wrapping up current task and starting a new session. "
            "Key state will be saved automatically before compression.",
            file=sys.stderr
        )
    elif count > CRITICAL_THRESHOLD and count % 10 == 0:
        print(
            f"\n🔴 [context-monitor] {count} tool calls — deep into context. "
            "Start new session soon.",
            file=sys.stderr
        )

if __name__ == "__main__":
    main()
