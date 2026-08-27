---
description: Delegate a task to the Engineering Excellence Team (5 agents).
argument-hint: <task for the Engineering Excellence Team>
---

Task: $ARGUMENTS

Team: **Engineering Excellence Team** — Raise the floor of engineering practice through documentation, standards, and measurement.

Roster:

- `technical-writer` — Technical Writer: Produce documentation that gets a reader to a correct outcome quickly.
- `engineering-intelligence-reporting-engineer` — Engineering Intelligence & Reporting Engineer: Measure engineering health with metrics that drive better decisions, not scoreboards.
- `modernization-engineer` — Modernization Engineer: Make legacy systems safe to change again, incrementally and without a rewrite.
- `engineering-standards-engineer` — Engineering Standards Engineer: Turn engineering standards into automated defaults rather than documents nobody reads.
- `excellence-lead` — Engineering Excellence Lead: Own the outcome, sequencing, and standard of work for the Engineering Excellence Team.

1. Pick the minimum set of agents above that can complete the task. Name them and
   say in one line why each is needed.
2. Delegate to each with the Agent tool, `subagent_type` = the `slug` in backticks.
   Agents cannot call each other — every hand-off passes through you.
3. For work spanning several agents, run the team's architect or lead first, record
   the decision, then fan out to the implementers.
4. Merge the results, resolve contradictions explicitly, and report using the
   output-discipline rule: claim, evidence (`file:line`), impact, ranked by severity.

Do not do the work inline if a specialist agent above exists for it.
