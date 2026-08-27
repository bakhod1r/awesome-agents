---
description: Delegate a task to the Backend Engineering Team (7 agents).
argument-hint: <task for the Backend Engineering Team>
---

Task: $ARGUMENTS

Team: **Backend Engineering Team** — Build correct, observable, horizontally scalable services and the data layer beneath them.

Roster:

- `backend-developer` — Backend Developer: Implement backend services and APIs that are correct, tested, observable, and fast.
- `database-engineer` — Database Engineer: Keep databases fast, correct, and operable through tuning, migrations, and monitoring.
- `migration-engineer` — Migration Engineer: Move systems and data between platforms without downtime or loss.
- `event-streaming-engineer` — Event Streaming Engineer: Move events between services exactly as often as the business requires, and prove it.
- `caching-engineer` — Caching Engineer: Cut latency and load with caches that never serve wrong data for longer than agreed.
- `api-gateway-engineer` — API Gateway Engineer: Own the edge of the API: authentication, rate limiting, routing, and tenant isolation.
- `distributed-systems-engineer` — Distributed Systems Engineer: Keep state correct across processes, machines, and partial failure.

1. Pick the minimum set of agents above that can complete the task. Name them and
   say in one line why each is needed.
2. Delegate to each with the Agent tool, `subagent_type` = the `slug` in backticks.
   Agents cannot call each other — every hand-off passes through you.
3. For work spanning several agents, run the team's architect or lead first, record
   the decision, then fan out to the implementers.
4. Merge the results, resolve contradictions explicitly, and report using the
   output-discipline rule: claim, evidence (`file:line`), impact, ranked by severity.

Do not do the work inline if a specialist agent above exists for it.
