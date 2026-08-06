---
name: postmortem
description: Write a blameless incident postmortem with a timeline and tracked actions. Use after any customer-visible incident, data loss, or security event.
---

# Blameless Postmortem

The purpose is to make this class of failure impossible, not to explain it. A postmortem
that produces no system change was a writing exercise.

## Template

```markdown
# Postmortem: <title>

- Date: <UTC> | Duration: <detection → resolution> | Severity: <level>
- Impact: <users affected, requests failed, data lost, money — quantified>

## Timeline
| Time (UTC) | Event | Source |
<From the first contributing change or signal to full resolution.
Every row cites a log, alert, deploy record, or message. No memory-reconstructed rows.>

## What happened
<The mechanism. What actually broke, technically, in sequence.>

## Contributing factors
<Multiple. Never a single "root cause". Never a person.>

## What went well
## What was hard
## Detection gap
<How long until we knew, and why not sooner. This is its own finding.>

## Action items
| Action | Type (prevent/detect/mitigate) | Owner | Due | Tracking |
```

## Worked example

**Blameful, single-cause — produces one useless action item:**

```markdown
## Root cause
Engineer deployed a migration without checking the lock behaviour, which locked
the orders table for 12 minutes.

## Action items
| Action | Owner |
| Remind the team to check migrations before deploying | Team lead |
```

This blames a person, finds one cause, and produces an action that changes nothing.
The same outage happens again in four months with a different name attached.

**Blameless, multi-factor — produces changes to the system:**

```markdown
## Contributing factors
1. The migration took an `ACCESS EXCLUSIVE` lock. The tool offers no online path
   for this operation, and nothing in review surfaces lock class.
2. Staging holds 40k rows; production holds 90M. The migration ran in 0.3s in staging.
   Nothing compares migration timing across environments.
3. The deploy pipeline has no timing gate — a migration may run unbounded.
4. Alerting fired on API error rate at 4 min, not on DB lock wait at 30 s.
   We detected the consequence, not the cause.
5. Rollback required a second migration; there was no abort path mid-run.

## Detection gap
4 min 12 s from first lock wait to page. Lock-wait metrics exist in the exporter
but are on no dashboard and in no alert.

## Action items
| Action | Type | Owner | Due | Tracking |
| Add lock-class linter to migration CI; block ACCESS EXCLUSIVE on tables >1M rows | prevent | @dbteam | 2026-04-12 | INFRA-2231 |
| Run migrations against an anonymised production-sized snapshot in CI, report timing | prevent | @platform | 2026-04-26 | INFRA-2232 |
| Statement timeout of 30s on all migration sessions | mitigate | @dbteam | 2026-04-05 | INFRA-2233 |
| Alert on `pg_locks` wait > 30s, route to service owner | detect | @sre | 2026-04-05 | INFRA-2234 |
| Document the online migration path in the engineering standard | prevent | @dbteam | 2026-04-19 | INFRA-2235 |
```

Five factors, five system changes, five owners, five dates. Any **one** of them
would have prevented or contained the outage. That is the point: defence in depth,
found by refusing to stop at the first cause.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| A single "root cause" | Incidents are always multi-factor. Stopping at one leaves the rest live. |
| Naming a person | Guarantees the next person hides the near-miss. You lose your best signal. |
| "Human error" as a factor | Humans are constant. The system that let the error through is the finding. |
| Action item "be more careful" | Not an action. Not trackable. Changes nothing. |
| Timeline from memory | Times drift, order inverts, and the analysis inherits the error. |
| No detection gap section | Slow detection is a separate, fixable failure. |
| Action items with no tracking ID | Untracked means undone. The incident will repeat. |

## Rules

- **Blameless.** Name systems and processes. "The deploy was not gated" — not "X deployed without checking".
- Timeline rows cite evidence. A row with no source is deleted or marked as an estimate.
- Quantify impact. "Some users saw errors" is not impact.
- Every action item has an owner, a date, and a tracking ID.
- Publish it. A private postmortem teaches one team.

## Done when

- [ ] At least three contributing factors, none of them a person.
- [ ] Every timeline row cites a log, alert, deploy, or message.
- [ ] Impact quantified in users, requests, money, or data.
- [ ] Detection gap analysed as its own finding.
- [ ] Every action item has owner, date, and tracking ID.
- [ ] Each action is a system change, not a promise to be careful.
