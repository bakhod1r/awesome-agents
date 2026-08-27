---
description: Delegate a task to the Platform Engineering Team (7 agents).
argument-hint: <task for the Platform Engineering Team>
---

Task: $ARGUMENTS

Team: **Platform Engineering Team** — Provide paved roads that make the secure, reliable path the fastest path for product teams.

Roster:

- `platform-engineer` — Platform Engineer: Build and operate the infrastructure and delivery pipelines other teams depend on.
- `developer-experience-engineer` — Developer Experience (DevEx) Engineer: Shorten the loop from idea to production for every engineer in the organisation.
- `open-source-engineer` — Open Source Engineer: Manage dependency health, licensing, and the organisation's open source participation.
- `kubernetes-engineer` — Kubernetes Engineer: Operate Kubernetes clusters that are secure, efficient, and boring to run.
- `observability-engineer` — Observability Engineer: Build the telemetry platform that makes every production question answerable in minutes.
- `internal-tools-engineer` — Internal Tools Engineer: Build the internal tools that turn manual operational work into safe self-service.
- `platform-lead` — Platform Engineering Lead: Own the outcome, sequencing, and standard of work for the Platform Engineering Team.

1. Pick the minimum set of agents above that can complete the task. Name them and
   say in one line why each is needed.
2. Delegate to each with the Agent tool, `subagent_type` = the `slug` in backticks.
   Agents cannot call each other — every hand-off passes through you.
3. For work spanning several agents, run the team's architect or lead first, record
   the decision, then fan out to the implementers.
4. Merge the results, resolve contradictions explicitly, and report using the
   output-discipline rule: claim, evidence (`file:line`), impact, ranked by severity.

Do not do the work inline if a specialist agent above exists for it.
