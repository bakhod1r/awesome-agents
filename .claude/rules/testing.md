---
description: What "tested" means in this repository.
---

# Testing Standard

- Push each test to the **lowest layer** that can still catch the defect.
- Tests assert **behaviour**, not implementation. A refactor must not break them.
- Every test covers the failure path, not only the happy path: invalid input, boundary, timeout, concurrent access.
- **No fixed sleeps.** Wait on an observable condition.
- Each test creates and destroys its own data. No shared mutable state, no order dependence.
- A test failing intermittently is quarantined within a day, then fixed or deleted. Never retried into green.
- Coverage is a diagnostic, never a target. A well-chosen 60 percent beats a padded 95 percent.
- Every fixed defect gains a regression test before the fix merges.
