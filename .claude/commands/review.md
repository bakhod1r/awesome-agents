---
description: Review the current diff through correctness, security, and quality lenses.
---

1. Get the diff: `git diff` (and `git diff --staged`).
2. Delegate in parallel to `code-reviewer`, `application-security-engineer`, and the quality agent matching the changed area.
3. Deduplicate findings, rank by severity, and drop anything not backed by a concrete failure scenario.
4. Report file:line findings with fixes. State a merge recommendation.
