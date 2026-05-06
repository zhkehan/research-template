#!/usr/bin/env python3
"""
log-reminder.py — Stop Hook
Runs when Claude Code finishes a session (user sends /exit or session ends).
Prints a checklist reminder to update knowledge base records.
Also cleans up temporary context counter files.
"""

import json
import sys
import os
import glob
from datetime import datetime

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    today = datetime.now().strftime("%Y-%m-%d")
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Clean up context counter temp files
    tmp_files = glob.glob(os.path.join(project_root, ".claude", "_ctx_*.tmp"))
    for f in tmp_files:
        try:
            os.remove(f)
        except Exception:
            pass

    # Print end-of-session reminder
    reminder = f"""
================================================================
        SESSION END -- Knowledge Base Checklist
================================================================
  Date: {today}

  Before closing, consider:
  [ ] /project:today          -- log tasks, health, or notes
  [ ] /project:sync-heartbeat -- update Project Board
  [ ] /project:github-sync    -- commit BRAIN changes to git

  If you made progress on a paper today:
  [ ] Update the project card in 04-Projects/
  [ ] Note any referee concerns or new ideas in MEMORY.md
================================================================
"""
    print(reminder, file=sys.stderr)

if __name__ == "__main__":
    main()
