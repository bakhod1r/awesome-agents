---
description: Run the production readiness and release gate before shipping.
---

1. Delegate to `production-readiness-engineer` for the readiness checklist.
2. Delegate to `release-manager` for rollout plan, rollback path, and abort criteria.
3. Delegate to `site-reliability-engineer` for SLO and alerting confirmation.
4. Block on any missing owner, runbook, rollback, or alert. Report go/no-go with the blocking list.
