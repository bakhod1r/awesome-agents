---
description: Delegate a task to the Data & AI Engineering Team (7 agents).
argument-hint: <task for the Data & AI Engineering Team>
---

Task: $ARGUMENTS

Team: **Data & AI Engineering Team** — Turn raw data into trustworthy products and ship AI systems that are evaluated, not vibed.

Roster:

- `data-engineer` — Data Engineer: Build reliable pipelines that deliver correct data on time with visible lineage.
- `ai-engineer` — AI Engineer: Ship AI features that meet quality, latency, and cost targets under real usage.
- `ai-evaluation-engineer` — AI Evaluation Engineer: Measure AI quality honestly with datasets, metrics, and judges that survive scrutiny.
- `analytics-engineer` — Analytics Engineer: Turn raw tables into a tested, documented metric layer the business can trust.
- `retrieval-search-engineer` — Retrieval & Search Engineer: Build retrieval that returns the right context, measured against a labelled set rather than vibes.
- `streaming-data-engineer` — Streaming Data Engineer: Deliver correct real-time data under late arrival, replay, and out-of-order events.
- `data-ai-lead` — Data & AI Engineering Lead: Own the outcome, sequencing, and standard of work for the Data & AI Engineering Team.

1. Pick the minimum set of agents above that can complete the task. Name them and
   say in one line why each is needed.
2. Delegate to each with the Agent tool, `subagent_type` = the `slug` in backticks.
   Agents cannot call each other — every hand-off passes through you.
3. For work spanning several agents, run the team's architect or lead first, record
   the decision, then fan out to the implementers.
4. Merge the results, resolve contradictions explicitly, and report using the
   output-discipline rule: claim, evidence (`file:line`), impact, ranked by severity.

Do not do the work inline if a specialist agent above exists for it.
