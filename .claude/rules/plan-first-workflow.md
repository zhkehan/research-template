---
description: Plan-first protocol for complex research tasks. Apply whenever a task
  involves writing a paper section, running a full peer review, designing a study,
  or any multi-step work where ambiguity could cause significant rework.
---

# Plan-First Workflow

## When to Apply

Invoke this protocol before starting any task that is:
- **Multi-step**: involves more than 3 sequential actions
- **Ambiguous**: the deliverable or scope is not fully specified
- **Consequential**: errors would require significant rework (paper sections, R&R responses)
- **Novel**: not a routine task covered by an existing skill

For simple, well-defined tasks (e.g., "score this abstract"), proceed directly.

## Protocol

### Step 1: Parse the Request

Before doing any work, extract:
- **Goal**: What is the user trying to achieve?
- **Deliverable**: What exactly should exist at the end?
- **Constraints**: Word limits, journal style, deadline, co-author preferences?
- **Ambiguities**: What is unclear that, if assumed wrong, would waste significant effort?

### Step 2: Classify Ambiguities

Label each ambiguity:
- `CLEAR` — understood, no question needed
- `ASSUMED` — will proceed with stated assumption, user can correct
- `BLOCKED` — must confirm before proceeding (would cause major rework if wrong)

Only ask about `BLOCKED` items. List `ASSUMED` items explicitly so the user
can correct them without being asked.

Maximum 3 clarifying questions. If more than 3 things are `BLOCKED`, ask only
the 3 most consequential ones.

### Step 3: Draft a Plan

Structure the plan as:

```
## Plan: [Task Name]

**Goal**: [One sentence]
**Deliverable**: [Specific output description]
**Estimated steps**: [N steps]

### Assumptions
- [Assumption 1]
- [Assumption 2]

### Steps
1. [Action] → [Output]
2. [Action] → [Output]
...

### Questions (BLOCKED items only)
1. [Question]?
```

### Step 4: Get Approval

Present the plan and wait for user confirmation before executing.
If the user says "go ahead" or similar, proceed with all assumptions as stated.

### Step 5: Execute and Report

After completing each major step, briefly confirm completion before moving to the next.
At the end, summarize what was done and what (if anything) remains.

## What Claude Decides Autonomously (No Asking)

- Grammar and phrasing choices within a section
- Which agent to invoke for a given dimension
- Order of minor sub-tasks within a step
- Whether to add a footnote for a tangential point
- Formatting details (table layout, equation numbering)

## What Always Requires User Input

- Substantive changes to the research design or contribution framing
- Choice between two materially different identification strategies
- Whether to drop or include a specific robustness check
- Target journal selection
- Tone of a referee response (conciliatory vs. firm)
