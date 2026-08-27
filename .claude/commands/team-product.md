---
description: Delegate a task to the Product Strategy Team (5 agents).
argument-hint: <task for the Product Strategy Team>
---

Task: $ARGUMENTS

Team: **Product Strategy Team** — Decide what to build and why, with evidence, sequencing, and measurable outcomes.

Roster:

- `product-manager` — Product Manager: Decide what to build next based on evidence, and define what success means.
- `product-owner` — Product Owner: Keep the backlog ready, ordered, and honest so delivery never stalls on ambiguity.
- `business-analyst` — Business Analyst: Translate business processes and rules into precise, verifiable requirements.
- `product-innovation-engineer` — Product Innovation Engineer: De-risk new bets quickly through prototypes and honest experiments.
- `technical-project-manager` — Technical Project Manager Agent: Drive complex technical delivery: dependencies, risks, and truthful status.

1. Pick the minimum set of agents above that can complete the task. Name them and
   say in one line why each is needed.
2. Delegate to each with the Agent tool, `subagent_type` = the `slug` in backticks.
   Agents cannot call each other — every hand-off passes through you.
3. For work spanning several agents, run the team's architect or lead first, record
   the decision, then fan out to the implementers.
4. Merge the results, resolve contradictions explicitly, and report using the
   output-discipline rule: claim, evidence (`file:line`), impact, ranked by severity.

Do not do the work inline if a specialist agent above exists for it.
