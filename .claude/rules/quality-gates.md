---
description: Quality scoring rubric and enforcement gates for academic paper work.
  Apply whenever evaluating a paper section, full draft, or submission readiness.
  Scores are computed by the peer-review skill using specialized agents.
---

# Quality Gates — Academic Paper Standards

## Score Thresholds

| Score | Status | Meaning |
|-------|--------|---------|
| 95–100 | EXCELLENCE | Top-journal ready; aspirational standard |
| 85–94 | SUBMISSION_READY | Can be submitted; minor issues noted |
| 70–84 | DRAFT_READY | Safe to share with co-authors or advisors |
| 60–69 | REVISION_NEEDED | Specific rewrites required before sharing |
| < 60 | BLOCKED | Do not submit or share; address critical issues first |

## Scoring Dimensions

Each dimension is scored independently by a specialized agent.
The overall score is a weighted average.

| Dimension | Weight | Agent |
|-----------|--------|-------|
| Research Design & Identification | 30% | `identification-critic` |
| Literature Coverage & Positioning | 20% | `literature-auditor` |
| Data Quality & Empirical Execution | 20% | `data-quality-checker` |
| Writing & Communication | 15% | `economics-proofreader` |
| Abstract Quality | 15% | `abstract-scorer` |

## Automatic Failures (Score → 0 for that dimension)

The following issues cause an automatic zero for the relevant dimension,
regardless of other quality:

- **Identification**: OLS on an endogenous variable with no discussion
- **Identification**: Parallel trends assumed with no pre-trend test
- **Literature**: Missing a paper with >500 citations in the same narrow area
- **Data**: Sample sizes inconsistent between tables with no explanation
- **Data**: Dependent variable not defined
- **Writing**: Abstract contains no quantitative finding

## Enforcement Rules

1. **BLOCKED papers**: Claude will not draft submission cover letters or
   referee responses until the score reaches at least 70 (DRAFT_READY).

2. **SUBMISSION_READY threshold**: Required before `/project:career-submission`
   drafts a submission letter for a top-5 journal.

3. **Score reporting**: Every `peer-review` invocation must end with an
   explicit score summary table.

4. **Re-scoring**: After a major revision, re-run `peer-review` to get
   an updated score. Do not carry forward old scores.

## Score Report Format

Every quality assessment must end with:

```
## Quality Score Summary

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|---------|
| Research Design | XX/100 | 30% | XX.X |
| Literature | XX/100 | 20% | XX.X |
| Data Quality | XX/100 | 20% | XX.X |
| Writing | XX/100 | 15% | XX.X |
| Abstract | XX/100 | 15% | XX.X |
| **TOTAL** | | | **XX.X/100** |

**Status: [BLOCKED / REVISION_NEEDED / DRAFT_READY / SUBMISSION_READY / EXCELLENCE]**

Top priority fixes:
1. [Most impactful issue to address]
2. [Second most impactful]
3. [Third most impactful]
```
