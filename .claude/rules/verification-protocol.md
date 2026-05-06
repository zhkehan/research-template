---
paths:
  - "**/*.tex"
  - "**/*.do"
  - "**/*.py"
---

# Task Completion Verification Protocol

**At the end of EVERY task involving output files, Claude MUST verify the output works correctly.**

## For LaTeX Documents

1. Compile with `xelatex` (3-pass with bibtex if citations present)
2. Check for overfull hbox warnings
3. Confirm output PDF exists and has expected page count
4. Report any errors or warnings to user

## For Stata Scripts (.do files)

1. Note that Stata must be run manually — remind user to run the script
2. Confirm expected output files (`.dta`, `.log`, tables) exist after run
3. Spot-check key variable names and observation counts if log is available

## For Python Data Scripts

1. If the script can be run non-interactively, run it: `python path/to/script.py`
2. Confirm expected output files (`.csv`, `.pkl`, `.parquet`) were created
3. Check for non-zero file sizes

## Common Pitfalls

- **Assuming success**: Always verify output files exist AND contain correct content
- **Relative paths**: Confirm scripts run from the correct working directory
- **Missing dependencies**: Check import errors before declaring success

## Verification Checklist

```
[ ] Output file created successfully
[ ] No compilation/run errors
[ ] Key outputs spot-checked
[ ] Reported results to user
```
