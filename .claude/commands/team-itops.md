---
description: Delegate a task to the IT Operations & Infrastructure Team (9 agents).
argument-hint: <task for the IT Operations & Infrastructure Team>
---

Task: $ARGUMENTS

Team: **IT Operations & Infrastructure Team** — Run the corporate and production infrastructure that everything else stands on: servers, network, identity, endpoints, and recovery.

Roster:

- `systems-administrator` — Systems Administrator: Keep servers and operating systems healthy, patched, hardened, and inventoried.
- `network-engineer` — Network Engineer: Design and operate networks that are fast, segmented, observable, and recoverable.
- `cloud-operations-engineer` — Cloud Operations Engineer: Operate cloud estates safely: accounts, quotas, guardrails, and day-two operations.
- `endpoint-management-engineer` — Endpoint & Device Management Engineer: Keep every laptop, phone, and workstation compliant, encrypted, and recoverable.
- `iam-engineer` — Identity & Access Management (IAM) Engineer: Ensure the right people and workloads have exactly the access they need, and nothing more.
- `backup-disaster-recovery-engineer` — Backup & Disaster Recovery Engineer: Guarantee the organisation can come back from data loss, ransomware, or site failure.
- `it-service-desk-engineer` — IT Service Desk Engineer: Resolve user-facing IT issues fast and eliminate their causes rather than their symptoms.
- `virtualization-engineer` — Virtualization Engineer: Run hypervisor and virtual desktop platforms with predictable performance and clean capacity headroom.
- `itops-lead` — IT Operations & Infrastructure Lead: Own the outcome, sequencing, and standard of work for the IT Operations & Infrastructure Team.

1. Pick the minimum set of agents above that can complete the task. Name them and
   say in one line why each is needed.
2. Delegate to each with the Agent tool, `subagent_type` = the `slug` in backticks.
   Agents cannot call each other — every hand-off passes through you.
3. For work spanning several agents, run the team's architect or lead first, record
   the decision, then fan out to the implementers.
4. Merge the results, resolve contradictions explicitly, and report using the
   output-discipline rule: claim, evidence (`file:line`), impact, ranked by severity.

Do not do the work inline if a specialist agent above exists for it.
