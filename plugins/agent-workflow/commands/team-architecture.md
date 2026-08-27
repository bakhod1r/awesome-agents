---
description: Delegate a task to the Architecture Team (13 agents).
argument-hint: <task for the Architecture Team>
---

Task: $ARGUMENTS

Team: **Architecture Team** — Own system-wide technical direction: boundaries, contracts, trade-offs, and long-term evolvability.

Roster:

- `enterprise-architect` — Enterprise Architect: Align the technology landscape with business capabilities and a multi-year roadmap.
- `domain-architect` — Domain Architect: Model the business domain and define bounded contexts that keep coupling low.
- `backend-architect` — Backend Architect: Design service topology, contracts, and failure behaviour for backend systems.
- `frontend-architect` — Frontend Architect: Define frontend architecture, rendering strategy, and the design system contract.
- `mobile-architect` — Mobile Architect: Define mobile app architecture, offline model, and release strategy across platforms.
- `data-architect` — Data Architect: Design the data platform: modelling, lineage, governance, and access.
- `database-architect` — Database Architect: Design database topology, schemas, and scaling strategy for correctness under load.
- `integration-architect` — Integration Architect: Design how systems exchange data reliably across trust and ownership boundaries.
- `platform-architect` — Platform Architect: Design the internal platform: compute, networking, delivery, and tenancy model.
- `security-architect` — Security Architect: Design security architecture: trust boundaries, identity, secrets, and defence in depth.
- `ai-architect` — AI Architect: Design AI systems end to end: model strategy, retrieval, evaluation, safety, and cost.
- `product-design-architect` — Product Design Architect: Own the design system architecture and interaction patterns across every surface.
- `qa-architect` — QA Architect: Design the quality strategy: what is tested, at which layer, and with what feedback speed.

1. Pick the minimum set of agents above that can complete the task. Name them and
   say in one line why each is needed.
2. Delegate to each with the Agent tool, `subagent_type` = the `slug` in backticks.
   Agents cannot call each other — every hand-off passes through you.
3. For work spanning several agents, run the team's architect or lead first, record
   the decision, then fan out to the implementers.
4. Merge the results, resolve contradictions explicitly, and report using the
   output-discipline rule: claim, evidence (`file:line`), impact, ranked by severity.

Do not do the work inline if a specialist agent above exists for it.
