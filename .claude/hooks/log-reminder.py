#!/usr/bin/env python3
"""
log-reminder.py — Stop Hook
Runs when Claude Code finishes a session.
Prints a pipeline checklist and cleans up temp counter files.
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

    today        = datetime.now().strftime("%Y-%m-%d")
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    for f in glob.glob(os.path.join(project_root, ".claude", "_ctx_*.tmp")):
        try:
            os.remove(f)
        except Exception:
            pass

    reminder = f"""
================================================================
      SESSION END — {{PROJECT_NAME}} Pipeline Checklist
================================================================
  Date: {today}

  Before closing, consider:
  [ ] Scripts changed?    → saved and syntax-checked
  [ ] New data converted? → run 05_validate_parquet.py
  [ ] DuckDB updated?     → verify column_catalog is current
  [ ] Update PLAN.md Progress Log with today's notes
  [ ] Commit scripts:
        git add scripts/ *.md && git commit -m "<description>"
================================================================
"""
    print(reminder, file=sys.stderr)

if __name__ == "__main__":
    main()
