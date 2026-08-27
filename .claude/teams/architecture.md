# Architecture Team

## Mission

Own system-wide technical direction: boundaries, contracts, trade-offs, and long-term evolvability.

## Charter

- Define target architecture and the migration path to it.
- Guard cross-cutting concerns: security, data, integration, cost.
- Produce ADRs for every non-reversible decision.

## Roster (14)

- [Enterprise Architect](../agents/enterprise-architect.md) — Align the technology landscape with business capabilities and a multi-year roadmap.
- [Domain Architect](../agents/domain-architect.md) — Model the business domain and define bounded contexts that keep coupling low.
- [Backend Architect](../agents/backend-architect.md) — Design service topology, contracts, and failure behaviour for backend systems.
- [Frontend Architect](../agents/frontend-architect.md) — Define frontend architecture, rendering strategy, and the design system contract.
- [Mobile Architect](../agents/mobile-architect.md) — Define mobile app architecture, offline model, and release strategy across platforms.
- [Data Architect](../agents/data-architect.md) — Design the data platform: modelling, lineage, governance, and access.
- [Database Architect](../agents/database-architect.md) — Design database topology, schemas, and scaling strategy for correctness under load.
- [Integration Architect](../agents/integration-architect.md) — Design how systems exchange data reliably across trust and ownership boundaries.
- [Platform Architect](../agents/platform-architect.md) — Design the internal platform: compute, networking, delivery, and tenancy model.
- [Security Architect](../agents/security-architect.md) — Design security architecture: trust boundaries, identity, secrets, and defence in depth.
- [AI Architect](../agents/ai-architect.md) — Design AI systems end to end: model strategy, retrieval, evaluation, safety, and cost.
- [Product Design Architect](../agents/product-design-architect.md) — Own the design system architecture and interaction patterns across every surface.
- [QA Architect](../agents/qa-architect.md) — Design the quality strategy: what is tested, at which layer, and with what feedback speed.
- [Architecture Lead](../agents/architecture-lead.md) — Own the outcome, sequencing, and standard of work for the Architecture Team.

## How to engage

Delegate to a single agent with the Agent tool using its `name` from the roster above.
For work spanning several of these agents, start with the team's architect or lead,
get the design decision recorded, then fan out to implementers.
