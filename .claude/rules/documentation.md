---
description: Documentation expectations for every change.
---

# Documentation

- Docs ship in the **same change** as the code they describe. A follow-up ticket is not documentation.
- Every procedure is executed exactly as written before publishing. Untested steps do not ship.
- State prerequisites and the expected result for each task.
- Wrong docs are worse than missing docs. Delete stale content rather than letting it rot.
- Irreversible decisions get an ADR (`.claude/skills/adr`). Never delete an ADR — supersede it.
- Every service has: a README, a runbook per alert, and an owner. No owner, no launch.
