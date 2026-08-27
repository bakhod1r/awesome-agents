---
description: Delegate a task to the FinOps & Cost Engineering Team (4 agents).
argument-hint: <task for the FinOps & Cost Engineering Team>
---

Task: $ARGUMENTS

Team: **FinOps & Cost Engineering Team** — Make technology spend visible, attributable, and efficient without slowing delivery down.

Roster:

- `finops-engineer` — FinOps Engineer: Make spend visible and attributable, then drive down waste with evidence.
- `cloud-cost-architect` — Cloud Cost Architect: Design systems whose cost curve stays sane as they scale.
- `capacity-planning-engineer` — Capacity Planning Engineer: Ensure capacity exists when demand arrives, without paying for idle headroom all year.
- `licensing-vendor-manager` — Licensing & Vendor Manager: Keep software licensing compliant and vendor spend justified by actual use.

1. Pick the minimum set of agents above that can complete the task. Name them and
   say in one line why each is needed.
2. Delegate to each with the Agent tool, `subagent_type` = the `slug` in backticks.
   Agents cannot call each other — every hand-off passes through you.
3. For work spanning several agents, run the team's architect or lead first, record
   the decision, then fan out to the implementers.
4. Merge the results, resolve contradictions explicitly, and report using the
   output-discipline rule: claim, evidence (`file:line`), impact, ranked by severity.

Do not do the work inline if a specialist agent above exists for it.
