---
name: adr
description: Write an Architecture Decision Record. Use when a decision is hard to reverse — technology choice, service boundary, data model, protocol, vendor, or anything a future engineer will ask "why on earth" about.
---

# ADR

## When to write one

Write an ADR when the decision is **expensive to reverse**. The test: would undoing this in
six months require a migration, a rewrite, or a contract negotiation? Then it needs a record.

Do **not** write one for: library version bumps, naming, formatting, or anything a single
pull request can undo.

## Location

`docs/adr/NNNN-kebab-title.md`. Sequential, zero-padded, **never renumbered** — links rot otherwise.

## Template

```markdown
# NNNN. <Title stated as the decision, not the problem>

- Status: Proposed | Accepted | Superseded by NNNN
- Date: YYYY-MM-DD
- Deciders: <names or agent roles>

## Context
<The forces. Facts and constraints only — no narrative, no history lesson.
What makes this hard? What did we measure? What are we not allowed to change?>

## Decision
<What we will do, active voice, present tense. "We will shard by tenant_id."
Not "it was decided that sharding might be considered.">

## Consequences
<What becomes easier. What becomes harder. What we now owe — the debt this creates.
Include the ugly ones; the ADR is worthless if it only lists benefits.>

## Alternatives Considered
<Each real option with the concrete, specific reason it lost.>
```

## Worked example

Two versions of the same Alternatives section:

**Weak — unfalsifiable, tells a future reader nothing:**

```markdown
## Alternatives Considered
- Sharding by user_id: not a good fit for our use case.
- Read replicas: didn't scale well enough.
- Bigger instance: too expensive.
```

**Strong — every rejection is a checkable fact:**

```markdown
## Alternatives Considered
- **Shard by user_id.** Rejected: 38% of queries join across users within one tenant,
  which becomes cross-shard. Measured on 7 days of query logs (`analysis/shard-key-2026-03.md`).
- **Read replicas only.** Rejected: writes are the bottleneck, not reads.
  Write throughput is 4.2k/s against a measured single-primary ceiling of ~5k/s;
  this buys roughly four months of growth at the current 12%/month rate.
- **Vertical scale to the largest instance.** Rejected: +$18k/month for a 1.8x ceiling,
  and the next step after that does not exist. Delays the same decision by two quarters.
```

The second version survives the question "did you actually consider this?" The first does not.

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Consequences lists only benefits | Every real decision costs something. Name it. |
| "Best practice" as a justification | Cite the measurement or the constraint instead. |
| Alternatives that were never seriously considered | Straw men are worse than omission — delete them. |
| Deleting a superseded ADR | Supersede it. The reasoning stays valuable even when wrong. |
| Written after implementation to satisfy process | The record exists to shape the decision, not to document it. |
| Two decisions in one ADR | Split. They will be superseded on different timelines. |

## Rules

- One decision per record.
- Never delete an ADR — set `Status: Superseded by NNNN`.
- Quantify trade-offs in money, latency, or effort. "Faster" is not a consequence.
- Deciders are named. An unowned decision is a rumour.

## Done when

- [ ] The title states the decision, not the problem.
- [ ] Context contains facts and constraints — no story.
- [ ] Consequences include at least one genuine cost.
- [ ] Every alternative has a specific, checkable rejection reason.
- [ ] A stranger could re-derive the decision from the record alone.
