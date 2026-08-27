---
description: Delegate a task to the Release & Reliability Team (6 agents).
argument-hint: <task for the Release & Reliability Team>
---

Task: $ARGUMENTS

Team: **Release & Reliability Team** — Deliver change safely and keep production healthy against explicit SLOs and error budgets.

Roster:

- `release-manager` — Release Manager: Get changes to production predictably, with the risk visible and the rollback ready.
- `site-reliability-engineer` — Site Reliability Engineer (SRE): Keep production reliable against explicit SLOs while enabling fast change.
- `incident-response-engineer` — Incident Response Engineer: Detect, contain, and resolve incidents quickly, then make the same failure impossible.
- `chaos-engineering-engineer` — Chaos Engineering Engineer: Find weaknesses by injecting controlled failure into real systems before reality does.
- `production-readiness-engineer` — Production Readiness Engineer: Ensure nothing reaches production without ownership, observability, and an operational plan.
- `release-lead` — Release & Reliability Lead: Own the outcome, sequencing, and standard of work for the Release & Reliability Team.

1. Pick the minimum set of agents above that can complete the task. Name them and
   say in one line why each is needed.
2. Delegate to each with the Agent tool, `subagent_type` = the `slug` in backticks.
   Agents cannot call each other — every hand-off passes through you.
3. For work spanning several agents, run the team's architect or lead first, record
   the decision, then fan out to the implementers.
4. Merge the results, resolve contradictions explicitly, and report using the
   output-discipline rule: claim, evidence (`file:line`), impact, ranked by severity.

Do not do the work inline if a specialist agent above exists for it.
