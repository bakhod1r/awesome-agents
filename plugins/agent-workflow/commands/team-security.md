---
description: Delegate a task to the Security Engineering Team (8 agents).
argument-hint: <task for the Security Engineering Team>
---

Task: $ARGUMENTS

Team: **Security Engineering Team** — Make the system secure by default and prove it with threat models, tests, and controls evidence.

Roster:

- `application-security-engineer` — Application Security Engineer: Build security into applications through review, tooling, and developer enablement.
- `devsecops-engineer` — DevSecOps Engineer: Automate security controls across the software supply chain and runtime.
- `compliance-engineer` — Compliance Engineer: Turn regulatory requirements into automated, evidenced controls rather than paperwork.
- `cryptography-secrets-engineer` — Cryptography & Secrets Engineer: Own key material end to end: generation, storage, rotation, and destruction.
- `supply-chain-security-engineer` — Supply Chain Security Engineer: Prove that what runs in production is exactly what was reviewed, built, and approved.
- `soc-analyst` — Security Operations (SOC) Analyst: Detect, triage, and contain attacks in progress with evidence and speed.
- `penetration-tester` — Penetration Tester: Prove exploitability within authorised scope, and hand back findings engineers can fix.
- `cloud-security-engineer` — Cloud Security Engineer: Secure the cloud estate: identity, configuration, workloads, and data at rest and in motion.

1. Pick the minimum set of agents above that can complete the task. Name them and
   say in one line why each is needed.
2. Delegate to each with the Agent tool, `subagent_type` = the `slug` in backticks.
   Agents cannot call each other — every hand-off passes through you.
3. For work spanning several agents, run the team's architect or lead first, record
   the decision, then fan out to the implementers.
4. Merge the results, resolve contradictions explicitly, and report using the
   output-discipline rule: claim, evidence (`file:line`), impact, ranked by severity.

Do not do the work inline if a specialist agent above exists for it.
