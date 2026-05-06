---
description: Plan-first protocol for complex data pipeline tasks. Apply whenever a
  task involves writing a new conversion script, restructuring the pipeline, or any
  multi-step work where ambiguity could cause significant rework.
---

# Plan-First Workflow

## When to Apply

Invoke this protocol before starting any task that is:
- **Multi-step**: involves more than 3 sequential actions
- **Ambiguous**: the deliverable or scope is not fully specified
- **Consequential**: errors would require significant rework (schema changes, re-conversion)
- **Novel**: not a routine task covered by an existing script

For simple, well-defined tasks (e.g., "add a column to column_catalog"), proceed directly.

## Protocol

### Step 1: Parse the Request

Before doing any work, extract:
- **Goal**: What is the user trying to achieve?
- **Deliverable**: What exactly should exist at the end?
- **Constraints**: Which tables? Which states? Memory limits?
- **Ambiguities**: What is unclear that, if assumed wrong, would waste significant effort?

### Step 2: Classify Ambiguities

- `CLEAR` — understood, no question needed
- `ASSUMED` — will proceed with stated assumption, user can correct
- `BLOCKED` — must confirm before proceeding

Only ask about `BLOCKED` items. Maximum 3 clarifying questions.

### Step 3: Draft a Plan

```
## Plan: [Task Name]

**Goal**: [One sentence]
**Deliverable**: [Specific output]
**Estimated steps**: [N steps]

### Assumptions
- [Assumption 1]

### Steps
1. [Action] → [Output]
2. [Action] → [Output]

### Questions (BLOCKED only)
1. [Question]?
```

### Step 4: Get Approval

Present the plan and wait for confirmation before executing.

### Step 5: Execute and Report

After each major step, briefly confirm before moving to the next.
Summarize what was done and what (if anything) remains.

## What Claude Decides Autonomously

- Column naming and dtype choices within schema
- Chunk size tuning within memory constraints
- Order of minor sub-tasks within a step
- Log message formatting

## What Always Requires User Input

- Dropping or redefining a join key
- Changing the deduplication logic
- Switching compression format or row group size project-wide
- Adding a new table to ALL_MANIFESTS
