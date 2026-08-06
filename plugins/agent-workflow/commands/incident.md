---
description: Drive an active incident from detection to postmortem.
argument-hint: <symptom or alert>
---

Incident: $ARGUMENTS

1. `incident-response-engineer` takes command: establish impact, severity, and timeline.
2. **Mitigate before diagnosing.** If a recent change is implicated, roll back first.
3. Pull in `site-reliability-engineer` for SLO impact and `soc-analyst` if compromise is suspected.
4. Preserve evidence while acting: capture logs, metrics, and state before remediation.
5. After resolution, produce a blameless postmortem via the `postmortem` skill with owned, dated action items.
