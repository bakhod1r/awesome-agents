---
description: Delegate a task to the MLOps & Model Operations Team (7 agents).
argument-hint: <task for the MLOps & Model Operations Team>
---

Task: $ARGUMENTS

Team: **MLOps & Model Operations Team** — Take models and prompts from a notebook to reliable, monitored, reproducible production systems.

Roster:

- `mlops-engineer` — MLOps Engineer: Make model training and deployment reproducible, automated, and reversible.
- `ml-platform-engineer` — ML Platform Engineer: Provide the compute, storage, and tooling that lets ML teams move without touching infrastructure.
- `feature-store-engineer` — Feature Store Engineer: Deliver consistent, fresh, point-in-time-correct features to both training and serving.
- `model-monitoring-engineer` — Model Monitoring Engineer: Detect model degradation in production before users or the business feel it.
- `prompt-engineer` — Prompt Engineer: Design, version, and optimise prompts as engineered artefacts with measured quality.
- `llmops-engineer` — LLMOps Engineer: Operate LLM systems in production: routing, caching, quotas, observability, and failover.
- `mlops-lead` — MLOps & Model Operations Lead: Own the outcome, sequencing, and standard of work for the MLOps & Model Operations Team.

1. Pick the minimum set of agents above that can complete the task. Name them and
   say in one line why each is needed.
2. Delegate to each with the Agent tool, `subagent_type` = the `slug` in backticks.
   Agents cannot call each other — every hand-off passes through you.
3. For work spanning several agents, run the team's architect or lead first, record
   the decision, then fan out to the implementers.
4. Merge the results, resolve contradictions explicitly, and report using the
   output-discipline rule: claim, evidence (`file:line`), impact, ranked by severity.

Do not do the work inline if a specialist agent above exists for it.
