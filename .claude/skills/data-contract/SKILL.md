---
name: data-contract
description: Define or review a data contract between a producer and consumers. Use when creating a dataset, event stream, or API that another team depends on.
---

# Data Contract

The producer commits to a shape and a schedule. Consumers build against it.
Breaking it without notice is an outage, not a refactor.

## Template

```yaml
name: <dataset or event name>
owner: <team, plus a named person>
description: <what it represents in business terms>

schema:
  - name: <field>
    type: <type>
    nullable: <bool>
    classification: public | internal | confidential | pii
    description: <semantics, units, allowed values>

semantics:
  grain: <one row per WHAT — answer this first>
  primary_key: [<fields>]
  late_arrival: <how late records are handled, and the cutoff>
  timezone: <explicit. Never "local".>

sla:
  freshness: <max lag, and what consumers should do when breached>
  availability: <target>
  completeness: <expected row count range>

quality_checks: [<the checks that gate publication>]

versioning:
  policy: additive-only | versioned endpoints
  deprecation_notice: <period>
```

## Worked example

Two versions of one field:

**Ambiguous — three consumers will interpret it three ways:**

```yaml
- name: amount
  type: decimal
  description: The order amount
```

*Which* amount? Gross or net? Tax included? Which currency? Refunds negative or a separate row?
Each consumer picks an answer, and the three dashboards disagree forever.

**Unambiguous:**

```yaml
- name: amount_net_minor
  type: integer
  nullable: false
  classification: internal
  description: >
    Order value excluding tax and shipping, after discounts, in the minor unit of
    `currency_code` (cents for USD, yen for JPY — JPY has no minor unit, so the value
    is whole yen). Always positive. Refunds appear as a separate row with
    `transaction_type = 'refund'`, never as a negative amount here.
    Range observed: 1 to 4_200_000.
```

Plus the semantics that make it usable:

```yaml
semantics:
  grain: one row per order line item per transaction event
  primary_key: [order_id, line_item_id, transaction_id]
  late_arrival: >
    Events up to 72h late are merged into their original partition, which is then
    republished. Beyond 72h they land in the current partition with `is_backfill = true`.
    Consumers reading a partition older than 72h can treat it as final.
  timezone: All timestamps UTC. `order_date` is a date in the merchant's local
    timezone — see `merchant_timezone`. These differ; do not join on them.
```

That last line prevents a specific, expensive bug that would otherwise be found in production.

## Breaking vs additive

| Change | Verdict |
|---|---|
| Add a nullable field | Additive |
| Add a non-nullable field | **Breaking** — old producers cannot fill it |
| Remove or rename a field | **Breaking** |
| Widen a type (int32 → int64) | Additive for readers, **breaking** for fixed-width writers |
| Narrow a type | **Breaking** |
| Change units, timezone, or semantics without renaming | **Breaking, and the worst kind** — nothing errors, everything is quietly wrong |
| Change the grain | **Breaking.** Every aggregate downstream is now wrong. |

The dangerous row is the semantic one. A rename fails loudly; a silent unit change
corrupts six months of reporting before anyone notices.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| No grain stated | Consumers guess; their aggregates double-count |
| `status` with undocumented values | Every consumer hardcodes a different subset |
| Timezone unstated or "local" | Off-by-one-day bugs at every month boundary |
| Contract in a wiki, not in the pipeline | Documentation drifts; tests do not |
| Nullable everything "to be safe" | Pushes every decision to consumers, who each decide differently |
| Classification added later | PII has already been copied everywhere by then |

## Rules

- **Grain first.** "One row per what" is the first question and the most common omission.
- Classification at ingestion, never retroactively.
- The contract is enforced by tests in the producer's pipeline, not by a wiki page.
- Units in the field name where feasible: `amount_net_minor`, `duration_ms`, `weight_kg`.
- Breaking a contract without notice is treated as an outage, with a postmortem.

## Done when

- [ ] Grain and primary key stated and verified unique against real data.
- [ ] Every field has semantics, units, and a classification.
- [ ] Timezone explicit for every temporal field.
- [ ] Late arrival and backfill behaviour documented.
- [ ] Quality checks run in the producer's pipeline and gate publication.
- [ ] A named owner exists — a team alone is not an owner.
