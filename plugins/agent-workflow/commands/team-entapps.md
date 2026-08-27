---
description: Delegate a task to the Enterprise Applications Team (6 agents).
argument-hint: <task for the Enterprise Applications Team>
---

Task: $ARGUMENTS

Team: **Enterprise Applications Team** — Deliver and integrate the internal systems the business runs on: ERP, CRM, workflow, and low-code platforms.

Roster:

- `erp-engineer` — ERP Engineer: Configure and extend the ERP so business processes run correctly and the upgrade path stays open.
- `crm-engineer` — CRM Engineer: Make the CRM a trustworthy system of record for customer relationships and revenue process.
- `workflow-automation-engineer` — Workflow Automation Engineer: Automate business processes end to end with reliable, observable, recoverable workflows.
- `low-code-platform-engineer` — Low-Code Platform Engineer: Enable safe citizen development: governed, monitored, and prevented from becoming shadow IT.
- `systems-integration-engineer` — Systems Integration Engineer: Connect enterprise systems so data stays consistent across every business boundary.
- `entapps-lead` — Enterprise Applications Lead: Own the outcome, sequencing, and standard of work for the Enterprise Applications Team.

1. Pick the minimum set of agents above that can complete the task. Name them and
   say in one line why each is needed.
2. Delegate to each with the Agent tool, `subagent_type` = the `slug` in backticks.
   Agents cannot call each other — every hand-off passes through you.
3. For work spanning several agents, run the team's architect or lead first, record
   the decision, then fan out to the implementers.
4. Merge the results, resolve contradictions explicitly, and report using the
   output-discipline rule: claim, evidence (`file:line`), impact, ranked by severity.

Do not do the work inline if a specialist agent above exists for it.
