"""Skill definitions. Every skill carries: when to use, procedure, worked example,
anti-patterns, and a done-when checklist — the same bar the agents are held to.
"""

SKILL_STANDARD = """## Done when

Tick every box or the work is not finished:

"""

SKILLS = {}

SKILLS["delegation-protocol"] = """---
name: delegation-protocol
description: How to route work across teams and agents in this repository. Use when a task spans more than one domain, when you are unsure which agent owns it, or before fanning out to several agents.
---

# Delegation Protocol

## The chain

**Architect decides. Engineer implements. Quality verifies. Release ships.**

Never skip a link. Implementation with no design decision produces rework.
A release with no verification produces an incident. Both cost more than the link you skipped.

## Routing procedure

1. **Name the domain** in one sentence. If you need two sentences, it is two tasks — split first.
2. **Find the owner** in `.claude/teams/README.md`.
3. **Pick the minimum set.** One agent per distinct concern. Not one per file, not one per idea.
4. **Gather the declared Inputs** before delegating. An agent without its inputs guesses, and a
   confident guess is worse than an admitted gap.
5. **Delegate with context**, not with the user's raw prompt. State what was already decided,
   what is out of scope, and what you want back.
6. **Reconcile.** Where two agents disagree, do not average them. State the disagreement
   explicitly and escalate to the team's architect with both positions.

## Fan-out budget

| Task | Agents | Why |
|---|---|---|
| One file, obvious fix | **0** — do it inline | Delegation costs more than the fix |
| One feature, one domain | 1-2 | Implementer, then reviewer |
| Cross-domain feature | 3-4, one per domain | Any more and they overlap |
| System design | Architects first, implementers in a second pass | Design before build, always |

More than four agents on one task means the task is not decomposed yet. Decompose it.

## Worked example

> "Our checkout times out under Black Friday load and we lose orders."

**Wrong:** spawn eight agents — backend, database, SRE, performance, QA, security, PM, release —
and merge eight overlapping reports.

**Right — sequential, each gated on the previous:**

```
1. performance-test-engineer   → where does it actually break?
   Returns: "p99 8.2s at 400 rps; DB connection pool saturated at 200 rps, not CPU."

   → Everything below is now scoped by that finding. Without it, the rest is guesswork.

2. database-architect          → pool sizing, connection strategy, read replica options
   backend-architect           → idempotency so retries do not double-charge
   (parallel — different concerns, same evidence)

3. backend-developer           → implements the agreed design
   database-engineer           → pool config and index changes

4. code-reviewer               → correctness of the retry path
   reliability-test-engineer   → verify it degrades instead of collapsing

5. release-manager             → canary with abort criteria tied to p99
```

Five stages, nine agents total, but **never more than two at once**, and each stage
gets real inputs from the last. Step 1 alone eliminated four wrong directions.

## Anti-patterns

| Anti-pattern | What goes wrong |
|---|---|
| Spawning five agents to answer one question | Five overlapping reports, no decision, high cost |
| Delegating without declared inputs | Agent invents plausible numbers; you cannot tell |
| Skipping the architect on an irreversible decision | Rework at 10x the cost, three weeks later |
| Accepting output without checking evidence | You inherited a hallucination and now own it |
| Forwarding the user's raw prompt to the agent | Agent re-derives context you already have |
| Parallel agents on the same concern | They contradict; you arbitrate with no basis |

## Done when

- [ ] The owning team is named and justified in one line.
- [ ] Each delegated agent received its declared Inputs.
- [ ] No two agents were given the same concern.
- [ ] Contradictions between agents are stated, not silently averaged.
- [ ] Every claim in the merged result traces to an agent's evidence, not to your summary of it.
"""

SKILLS["agent-registry"] = """---
name: agent-registry
description: Look up which agent or team owns a kind of work in this repository. Use when deciding whom to delegate to, when the user names a role, or when asked "who handles X".
---

# Agent Registry

## Where the roster lives

| File | Contents |
|---|---|
| `.claude/teams/README.md` | Every agent: title, `name`, team, model |
| `.claude/teams/<team>.md` | One team: mission, charter, roster with missions |
| `.claude/agents/<name>.md` | One agent: all ten sections |

The `name` in frontmatter is what the Agent tool takes. It is the kebab-case slug.

## Lookup procedure

1. Reduce the request to a **domain noun**: "migration", "drift", "egress cost", "screen reader".
2. Grep the roster for it. `.claude/teams/README.md` holds all __AGENT_COUNT__ missions in one file.
3. Read the candidate's **Decision Rules** section. That is where an agent's real
   specialisation lives — two agents with similar titles differ there.
4. Pick one. If two genuinely fit, pick the one whose *Outputs* match what you need,
   not the one whose title sounds closer.

## Disambiguation — the pairs people confuse

| Question | Answer | Not |
|---|---|---|
| Design the schema | `database-architect` | `database-engineer` (tunes and migrates an existing one) |
| Build a metrics pipeline | `observability-engineer` | `observability-test-engineer` (verifies signals exist and are correct) |
| Write the model | `ai-engineer` | `mlops-engineer` (ships, versions, monitors it) |
| Is the model still good? | `model-monitoring-engineer` | `ai-evaluation-engineer` (builds the eval sets and metrics) |
| Cloud account hardening | `cloud-security-engineer` | `platform-engineer` (builds on it) |
| Corporate servers, patching, IAM | `systems-administrator`, `iam-engineer` | `platform-engineer` (product infrastructure) |
| Attack it | `penetration-tester` (authorised, proves exploitability) | `security-test-engineer` (in-CI security regression) |
| Watch the alerts | `soc-analyst` | `incident-response-engineer` (commands the response) |
| Cost of a design | `cloud-cost-architect` | `finops-engineer` (attributes and optimises a running bill) |
| Requirements | `business-analyst` (process and rules) | `product-manager` (what to build and why) |

## Worked example

> "Our S3 bill tripled last month."

- Domain noun: **cost**, running system, already spent.
- `finops-engineer` — attribution and waste on an existing bill. **First choice.**
- `cloud-cost-architect` — only if the finding is architectural (egress pattern, storage class
  by design). Escalate to it after attribution, not before.
- `data-engineer` — pulled in if the driver turns out to be pipeline file-sizing.

Answer: **`finops-engineer` first.** Name the follow-ons as conditional, not parallel.

## Rules

- One agent per concern. Do not fan out to five for a one-file change.
- Architects decide, engineers implement, quality verifies. Do not skip the middle.
- If nothing fits, say so plainly and name the roster gap. Do not force the nearest agent —
  a wrong specialist is more confidently wrong than a generalist.

## Done when

- [ ] A single best-fit agent is named, with the `name` value, not just the title.
- [ ] The reason for the fit cites the agent's Decision Rules or Outputs, not its title.
- [ ] Near-misses are named as conditional follow-ons, not as parallel work.
- [ ] A genuine gap is reported as a gap.
"""

SKILLS["adr"] = """---
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
"""

SKILLS["threat-model"] = """---
name: threat-model
description: Produce a STRIDE threat model for a system or feature. Use before building anything that handles authentication, money, personal data, file uploads, or third-party input.
---

# Threat Model

Threat modelling is cheap before the build and expensive after. Do it at design time.

## Procedure

1. **Scope.** Name the system, its trust boundaries, and what is explicitly out of scope.
   Out-of-scope items are written down — silence reads as coverage.
2. **Data flow.** Diagram actors, processes, data stores, and every flow that crosses a
   trust boundary. Threats live at the crossings, not inside the boxes.
3. **Enumerate with STRIDE** at each crossing:

   | | Question |
   |---|---|
   | **S**poofing | Can an actor claim another identity? |
   | **T**ampering | Can data be modified in transit or at rest? |
   | **R**epudiation | Can an action be denied because nothing logged it? |
   | **I**nformation disclosure | What leaks, to whom, through which channel? |
   | **D**enial of service | What exhausts under load or deliberate abuse? |
   | **E**levation of privilege | How does a low-privilege actor gain more? |

4. **Rate** by exploitability and impact. Not by gut feel, not by scanner severity.
5. **Mitigate or accept.** Every threat gets a control, or a signed risk acceptance
   with a named owner and an expiry date.
6. **Verify.** Each mitigation names the specific test that proves it works.

## Output

```markdown
# Threat Model: <system>
## Scope and trust boundaries
## Out of scope
## Data flow
## Threats
| ID | Boundary | STRIDE | Threat | Exploitability | Impact | Mitigation | Verified by |
## Accepted risks
| ID | Risk | Owner | Expiry | Rationale |
```

## Worked example

Feature: users upload a profile picture, served from a CDN.

| ID | Boundary | STRIDE | Threat | Mitigation | Verified by |
|---|---|---|---|---|---|
| T1 | Browser→API | T | Content-Type lied about; SVG uploaded as image/png, executes script on view | Re-encode server-side; never trust the declared type; serve from a separate origin | `test_upload_svg_polyglot_is_reencoded` |
| T2 | Browser→API | D | 10 GB upload or a decompression bomb exhausts disk | Size cap before buffering; dimension cap after decode header, before full decode | `test_upload_exceeds_cap_rejected_before_buffer` |
| T3 | API→Storage | E | Filename `../../etc/passwd` escapes the upload directory | Discard the client filename entirely; store under a generated UUID | `test_path_traversal_filename_discarded` |
| T4 | Storage→CDN | I | Object URL is guessable; private avatars enumerable | Random 128-bit object key; deny bucket listing | `test_bucket_listing_denied` |
| T5 | API→Image lib | E | Malformed image triggers a native-code CVE in the decoder | Decode in a sandboxed worker with no network and a memory cap; pin and scan the library | `test_decoder_runs_without_network` |
| T6 | Browser→CDN | S | Attacker replaces another user's avatar via a predictable object key | Ownership check on write; key derived server-side only | `test_cannot_overwrite_other_user_avatar` |

Six threats on a "just an avatar upload" feature. T1 and T5 are the ones that get shipped
without a threat model — and they are the ones that turn into an incident.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| "We validate input" as a mitigation | Which validator? Running where? Against which encoding? |
| Threats without a verifying test | An untested mitigation is an assumption wearing a control's uniform |
| Rating by scanner severity | Scanner severity ignores your architecture and your data |
| Modelling only the happy actor | The attacker does not use your UI |
| Model produced once at launch | It is living. New flow, new crossing, new threats. |
| No out-of-scope section | Readers assume you covered what you silently skipped |

## Done when

- [ ] Every trust boundary crossing has been walked through all six STRIDE categories.
- [ ] Every threat ends in a mitigation **or** a dated, owned risk acceptance.
- [ ] Every mitigation names a specific test, not a policy.
- [ ] Out-of-scope is explicit.
- [ ] The model is stored next to the design, not in a slide deck.
"""

SKILLS["runbook"] = """---
name: runbook
description: Write an operational runbook that an on-call engineer can execute at 3am. Use when adding an alert, launching a service, or after an incident exposed a missing procedure.
---

# Runbook

A runbook is executable by a tired stranger with no context. If it needs the author
present, it is not a runbook — it is notes.

## Template

```markdown
# Runbook: <alert or procedure name>

## What this means
<The user-visible symptom in one sentence. Not the metric — the symptom.>

## Severity and impact
<Who is affected, how badly, how fast it escalates if ignored.>

## Diagnosis
1. <exact query, dashboard link, or command — copy-pasteable>
   - <output A> → cause 1, go to Mitigation row 1
   - <output B> → cause 2, go to Mitigation row 2

## Mitigation
| Symptom | Action | Command | Risk |

## Escalation
<Who, by which channel, after how long, and what to tell them.>

## Rollback
<Exact steps, and how to confirm it worked.>

## Related
<Dashboards, ADRs, past incidents.>
```

## Worked example

Two versions of one diagnosis step:

**Useless at 3am:**

```markdown
## Diagnosis
1. Check if the database is healthy.
2. Look at the connection pool.
3. Restart the service if needed.
```

Every line raises a question the on-call engineer cannot answer alone. *Which* database?
Healthy by what measure? Restart how, and what breaks when they do?

**Executable at 3am:**

```markdown
## Diagnosis
1. Is the pool saturated?
   ```
   kubectl exec -n prod deploy/api -- \\
     psql $DB_URL -c "select count(*), state from pg_stat_activity group by state"
   ```
   - `active` ≥ 95 (pool max is 100) → **saturated**, go to Mitigation row 1
   - `idle in transaction` ≥ 20 → **leaked transactions**, go to Mitigation row 2
   - Both under those numbers → not the pool. Check upstream: <dashboard link>

## Mitigation
| Symptom | Action | Command | Risk |
|---|---|---|---|
| Saturated | Raise pool ceiling to 150 | `kubectl set env deploy/api DB_POOL_MAX=150` | DB max_connections is 200; three replicas at 150 will exceed it. Scale replicas to 1 first, or raise the DB limit. |
| Leaked transactions | Terminate idle-in-transaction over 5 min | `psql $DB_URL -f ops/kill-idle-txn.sql` | **Rolls back in-flight work.** Users may see failed requests. Safe for reads, not during the nightly batch (02:00–04:00 UTC). |
```

The second version tells the engineer exactly what to run, what the output means,
and — critically — **what they are about to break**.

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| "Restart the service" | Give the command, and say what restarting drops |
| Actions with no stated risk | On-call needs to know the blast radius before pressing enter |
| Diagnosis using a metric nobody emits | Fix the instrumentation instead; then write the step |
| Links to a dashboard that requires tribal knowledge to read | State what number is bad |
| No escalation timeout | People burn an hour rather than wake someone. Give the deadline. |
| Never walked through | Untested runbook = no runbook |

## Done when

- [ ] Every command is copy-pasteable and was actually run.
- [ ] Every diagnostic step says what each possible output means.
- [ ] Every action states its risk and blast radius.
- [ ] Escalation has a named target and a time limit.
- [ ] Rollback includes how to confirm it worked.
- [ ] Someone other than the author walked it end to end.
"""

SKILLS["postmortem"] = """---
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
"""

SKILLS["data-contract"] = """---
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
"""

SKILLS["cost-review"] = """---
name: cost-review
description: Review a design or a running system for cost. Use before committing to an architecture, when a bill jumps, or during quarterly optimisation.
---

# Cost Review

## Procedure

1. **Attribute.** Break spend by team, service, and environment. Untagged spend is
   finding number one — you cannot optimise what you cannot attribute.
2. **Find the drivers.** Rank by absolute spend, then look for the usual suspects:

   | Driver | Typical cause |
   |---|---|
   | Cross-zone / egress traffic | Chatty services split across zones; no locality awareness |
   | Storage class | Everything on hot storage forever; no lifecycle policy |
   | Idle capacity | Non-production running nights and weekends |
   | Over-provisioning | Sized for a peak that never arrived, never revisited |
   | Managed service premium | Paying for an operator you do not need at this scale |
   | Log and metric volume | Debug logging left on; high-cardinality labels |
   | LLM tokens | No caching, oversized model for the task, unbounded context |

3. **Compute unit economics.** Cost per request, per tenant, per model call. Totals hide
   everything — a bill that doubled while traffic tripled is a *win*.
4. **Model at scale.** What does this cost at 10x? A design that is cheap today and
   ruinous at scale is rejected now, while changing it is still cheap.
5. **Recommend with numbers.** Each item: measured monthly saving, effort, and the
   performance or reliability risk it introduces.

## Output

| Finding | Monthly cost | Proposed change | Saving | Risk | Effort |

## Worked example

**Weak — unactionable, and quietly dangerous:**

```
- NAT Gateway costs are high, consider reducing traffic.
- Instances look oversized, recommend downsizing.
- Consider reserved instances for savings.
```

Nobody can act on these, and "downsize" with no risk statement is how a cost review
causes an outage.

**Strong:**

| Finding | Monthly | Change | Saving | Risk | Effort |
|---|---|---|---|---|---|
| NAT Gateway data processing: 41 TB/mo. 78% is S3 traffic routed through NAT. | $4,920 | Add S3 Gateway VPC endpoint | **$3,840** (verified: gateway endpoints are free, traffic bypasses NAT) | None. Route table change, reversible in minutes. | 1h |
| 14 non-prod RDS instances running 24/7 | $6,200 | Stop 19:00–07:00 and weekends via scheduler | **$4,100** (66% of hours) | Overnight CI jobs on 2 of the 14 — exclude those. | 4h |
| `api` service: p99 CPU 12%, sized `m5.4xlarge` × 9 | $3,740 | → `m5.xlarge` × 9, keep replica count | **$2,800** | **Real.** 4x less burst headroom. Verified against the last Black Friday peak: 34% CPU at 4.1x normal traffic. Still 3x headroom after the change. Requires a load test before rollout. | 1d + load test |
| CloudWatch: 2.1 TB logs/mo, 61% is `DEBUG` from one service | $1,480 | Set that service to `INFO`; 7-day retention on debug streams | **$900** | Lose debug detail on that service; it has tracing, so diagnosis is unaffected. | 2h |
| **Total** | | | **$11,640/mo** | | |

Every row: a number, a mechanism, an honest risk. The third row is the important one —
it is the biggest behavioural change and it names the load test as a precondition
instead of pretending the risk is zero.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Recommendation with no measured saving | Unprioritisable. The 5% item gets done, the 40% item does not. |
| Trading reliability for cost silently | The outage costs more than the year of savings |
| Optimising the total instead of the unit cost | Punishes growth; rewards shrinking the business |
| Reserved commitments without utilisation data | Locks in today's mistake for one to three years |
| Findings sent to finance | Finance cannot change a route table. Send to the owning team. |
| Savings never verified | Half of claimed savings do not appear on the next bill |

## Rules

- No recommendation without a measured saving. Estimates are labelled as estimates.
- Never trade away a reliability guarantee without saying so explicitly and loudly.
- Verify in the following billing period. Unverified savings do not count.
- Route findings to the team that can act, not to finance.
- Check for a hard limit before downsizing anything — quotas, connection pools, licences.

## Done when

- [ ] Attribution coverage stated; untagged spend quantified.
- [ ] Findings ranked by absolute saving, not by ease.
- [ ] Every row has a saving, a risk, and an effort estimate.
- [ ] Unit economics reported alongside totals.
- [ ] Cost at 10x scale modelled for design reviews.
- [ ] A verification date is set for the following billing period.
"""

SKILLS["marketplace"] = """---
name: marketplace
description: Install external Claude Code plugins from official marketplaces, and install this repository's own agent plugins. Use when the user wants a capability this roster does not cover, asks about plugins or marketplaces, or wants to share these agents with a team.
---

# Marketplaces

Plugins are **installed**, never copied into this repository. A vendored plugin never
receives upstream fixes and silently rots.

## This repository is a marketplace

```
/plugin marketplace add <your-org>/awesome-agents
/plugin install agent-workflow@awesome-agents      # commands + skills
/plugin install security-team@awesome-agents       # one team's agents
```

One plugin per team, plus `agent-workflow` for the shared commands and skills.
`plugins/` and `.claude-plugin/marketplace.json` are **generated** — run `python3 scripts/generate.py`.

## Official Anthropic marketplaces

Claude Code adds `claude-plugins-official` automatically on first interactive start.

```
/plugin marketplace add anthropics/skills
/plugin marketplace add anthropics/claude-plugins-community
/plugin                                            # browse and install
```

## What to install, by gap

These fill gaps this roster deliberately does not cover: vendor-specific tooling and
live data access. **Verify the plugin still exists with `/plugin` before recommending it** —
this table was accurate when written and marketplaces change.

| Need | Plugin | Pairs with |
|---|---|---|
| Cloud build and deploy | `aws-core`, `azure`, `cloudflare` | `platform-engineer`, `cloud-operations-engineer` |
| Observability queries | `datadog`, `grafana-mcp`, `honeycomb`, `newrelic` | `observability-engineer`, `site-reliability-engineer` |
| Database access | `mongodb`, `clickhouse`, `neon`, `cockroachdb`, `duckdb-skills` | `database-engineer`, `database-architect` |
| Security scanning | `claude-security`, `aikido`, `42crunch-api-security-testing` | `application-security-engineer`, `devsecops-engineer` |
| Issue tracking | `linear`, `atlassian`, `github`, `gitlab` | `technical-project-manager`, `product-owner` |
| Design handoff | `figma`, `canva` | `product-designer`, `frontend-engineer` |
| LLM tracing and evals | `langfuse-observability`, `mlflow`, `deepeval` | `ai-evaluation-engineer`, `llmops-engineer` |
| Documentation sites | `mintlify` | `technical-writer` |
| Browser automation | `chrome-devtools-mcp`, `browser-use` | `web-ux-quality-engineer` |
| Feature flags | `growthbook`, `confidence` | `release-manager` |

## The division of labour

**A plugin supplies tools and data access. This roster supplies judgement.**

```
User: "Why did checkout latency spike at 14:00?"

  datadog plugin        → fetches the traces and metrics       (capability)
  site-reliability-eng  → reads them, forms a hypothesis,
                          checks it against the deploy log,
                          states what is verified vs inferred  (judgement)
```

Neither alone is enough. The plugin without the agent returns a wall of metrics.
The agent without the plugin reasons about data it cannot see — which is the failure
mode you most want to avoid.

## Security

Marketplace plugins are **third-party code with tool access** running in your repository.

- Read the source before installing anything that touches production credentials, deploys, or customer data.
- Prefer vendor-official plugins (`datadog`, `mongodb`) over community forks of the same thing.
- A plugin that bundles MCP servers can make network calls you did not initiate. Check what hosts.
- Install at the narrowest scope that works — project over user, when the plugin is project-specific.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Copying a plugin's files into `.claude/` | No updates, no security fixes, silent divergence |
| Installing a plugin because the name matched | Plugins carry tool permissions; read first |
| Installing 20 plugins "to be ready" | Each adds context and tool surface; install on demand |
| Assuming a plugin replaces an agent | It supplies data, not the decision about what the data means |
| Recommending from memory | Marketplaces change. Check `/plugin` first. |

## Done when

- [ ] The gap is named before a plugin is proposed.
- [ ] The plugin's existence was verified with `/plugin`, not recalled.
- [ ] The agent that will use its output is named.
- [ ] Security implications stated for anything touching credentials or production.
- [ ] Nothing was vendored.
"""

SKILLS["onboarding"] = """---
name: onboarding
description: Get a new user or contributor productive with this agent system. Use when someone asks how to start, how it works, or how to add an agent.
---

# Onboarding

## Use it (2 minutes)

Open the repo in Claude Code and ask normally. `CLAUDE.md` loads automatically,
Claude reads the roster and delegates. To force a specific agent, name it:

> Use the `database-architect` agent to review this schema.

Or route by command: `/team <task>`.

## Understand it (10 minutes)

| Path | What it is | Loaded |
|---|---|---|
| `CLAUDE.md` | The delegation rule | Always |
| `.claude/rules/*.md` | Standing standards | Always |
| `.claude/teams/README.md` | Full roster with `name` values | On lookup |
| `.claude/agents/<name>.md` | One agent, ten sections | When delegated to |
| `.claude/commands/*.md` | Slash commands | When invoked |
| `.claude/skills/*/SKILL.md` | Procedures | On demand, by description match |
| `scripts/agents_data.py` | **The only file you edit** | Never — it is the source |

## First tasks to try

| Goal | Say |
|---|---|
| Find the owner | "who handles database migrations here?" |
| Review a diff | `/review` |
| Design something | `/design payment retry logic` |
| Pre-release check | `/ship` |
| Security pass | `/audit src/api` |
| Cost pass | `/cost` |

## Extend it

```bash
# 1. add a record to AGENTS in scripts/agents_data.py
# 2. regenerate everything
python3 scripts/generate.py
```

Never hand-edit `.claude/agents/*.md` — regeneration overwrites it. That is deliberate:
one source of truth is what keeps __AGENT_COUNT__ agents consistent.

### What separates a good agent record from a filler one

The template forces ten sections. It cannot force them to be *useful*. The difference
lives in two fields:

**Decision Rules — must be opinionated and falsifiable:**

```python
# Filler. True of every engineer who ever lived. Changes no behaviour.
rules=["Follow best practices", "Write clean code", "Consider performance"]

# Real. Each one rules out a specific thing the agent would otherwise do.
rules=[
    "Index to the query, not to the column.",
    "Any migration taking a long-lived exclusive lock is rejected; use an online strategy.",
    "Untested restores are not backups.",
]
```

**Quality Bar — must be checkable by someone else:**

```python
# Unfalsifiable. Nobody can fail this, so nobody passes it either.
bar=["High quality output", "Well documented", "Follows standards"]

# Checkable. Someone else can look and say yes or no.
bar=[
    "RTO and RPO measured in a real drill",
    "Hot queries have covering indexes",
    "No unbounded table scans on critical paths",
]
```

The test for both: **could a competent engineer disagree with this?** If not, it is
noise consuming context. Delete it and write something with an edge.

## Common mistakes

| Mistake | Consequence |
|---|---|
| Editing `.claude/agents/*.md` directly | Lost on the next `generate.py` run |
| Adding an agent with vague rules | It behaves exactly like the generalist you already had |
| Spawning five agents for one question | Overlapping reports, no decision |
| Skipping the architect on an irreversible decision | Rework at 10x cost later |
| Forgetting to rerun `generate.py` | CI fails: the Pages workflow blocks stale generated files |

## Done when

- [ ] The person has run one real task through a real agent.
- [ ] They know which file to edit (`scripts/agents_data.py`) and which never to (`.claude/agents/`).
- [ ] They can name the delegation chain: architect → engineer → quality → release.
"""

# --- derived counts -------------------------------------------------------
# Agent totals are written once, here, from the roster itself. Hard-coding them
# in the prose above means every new agent silently ages three sentences.
from agents_data import AGENTS  # noqa: E402

_AGENT_COUNT = str(len(AGENTS))
SKILLS = {k: v.replace("__AGENT_COUNT__", _AGENT_COUNT) for k, v in SKILLS.items()}

SKILLS["orchestration"] = """---
name: orchestration
description: Run a task end to end through the full delivery pipeline — product discovery, architecture, build, verification, release. Use when the user gives a goal rather than a specific technical instruction, or invokes /flow.
---

# Orchestration

One task. Seven stages. Each stage produces an artefact the next stage consumes.
**No artefact, no advance** — that is the whole mechanism.

You are the orchestrator. Agents cannot call each other; they have no Agent tool.
Every hand-off passes through you, which is what makes the chain inspectable.

## The pipeline

```
                              USER GOAL
                                  │
  ┌───────────────────────────────▼───────────────────────────────┐
  │ ① DISCOVER   Product Strategy — product-manager, business-analyst
  │              → problem, segment, success metric, non-goals, kill criterion
  │              ⛔ no measurable metric → stop, ask the user
  └───────────────────────────────┬───────────────────────────────┘
        ▲                         │  problem + metric, verbatim
        │                         ▼
        │  ┌────────────────────────────────────────────────────────┐
        │  │ ② ARCHITECT  Architecture — backend-, frontend-, security-,
        │  │              database-architect, by domain
        │  │              → options, trade-offs, failure modes, ADR,
        │  │                + the CONTRACT design works in, with its cost
        │  │              ⛔ irreversible decision without an ADR → do not build
        │  └────────────────────────┬───────────────────────────────┘
        │        ▲                  │  ADR + contract, verbatim
        │        │                  ▼
        │        │  ┌─────────────────────────────────────────────────┐
        │        │  │ ③ SHAPE     Design — ui-designer, ux-researcher,
        │        │  │             interaction-designer, content-designer,
        │        │  │             then design-qa-engineer tests the design itself
        │        │  │             → 2-3 mock files, one recommended, every reachable
        │        │  │               case drawn, flow + state spec, interface copy
        │        │  │             ⛔ visible change with no mock → nothing to build
        │        │  │             ⛔ design QA finds an undrawn case → not ready
        │        │  └────────────────────────┬────────────────────────┘
        │        │                           │  chosen mock + state spec
        │        │                           ▼
        │        │  ┌─────────────────────────────────────────────────┐
        │        │  │ ④ BUILD     owning engineering team
        │        │  │             → implementation, tests incl. failure paths,
        │        │  │               migrations, instrumentation
        │        │  │             ⛔ no failure-path test → not done
        │        │  └────────────────────────┬────────────────────────┘
        │        │                  ▲        │  diff + mock + ADR
        │        │                  │        ▼
        │        │                  │  ┌──────────────────────────────┐
        │        │                  │  │ ⑤ VERIFY   Quality — code-reviewer
        │        │                  │  │            + the specialist for the change
        │        │                  │  │            → ranked findings: claim,
        │        │                  │  │              file:line, impact, fix
        │        │                  │  │            ⛔ open HIGH → back to ④
        │        │                  │  └─────────────┬────────────────┘
        │        │                  │  HIGH finding  │
        │        │                  └────────────────┤
        │        │                                   ▼
        │        │                  ┌──────────────────────────────────┐
        │        │                  │ ⑥ RELEASE  production-readiness-engineer,
        │        │                  │            release-manager, SRE
        │        │                  │            → full suite output, version + SemVer
        │        │                  │              rule, CHANGELOG, release notes,
        │        │                  │              rollout, rollback, owner, runbook
        │        │                  │            ⛔ red test / no owner / no rollback
        │        │                  │              / untested rollback → no ship
        │        │                  └─────────────┬────────────────────┘
        │        │                                ▼
        │        │                        RELEASE PACKAGE
        │        │                     handed over, then deployed
        │        │                                │
        │        │                  ┌─────────────▼────────────────────┐
        │        │                  │ ⑦ OBSERVE  qa + user-acceptance-tester
        │        │                  │            + site-reliability-engineer
        │        │                  │            + product-manager on the metric
        │        │                  │            → post-deploy smoke on the real
        │        │                  │              environment, a profile panel of real
        │        │                  │              users by age and sector running the
        │        │                  │              task, error and latency watch, then
        │        │                  │              ①'s metric measured
        │        │                  │            ⛔ smoke fails or abort threshold hit
        │        │                  │              → roll back now, diagnose after
        │        │                  └─────────────┬────────────────────┘
        │        │                                ▼
        │        │                     metric moved? kill criterion hit?
        │        │                                │
        └────────┴────────────────────────────────┘  answer goes back to ①
        │        │
        │        └── ③→② the contract cannot carry the flow the user needs:
        │               widen it and state the cost, or say why it cannot move
        │
        └─────────── ②→① the feature as scoped cannot be built at acceptable
                        cost or risk — product re-scopes, architects do not trim
                     ③→① research or the mocks show ①'s problem or metric is wrong
                     ②⇄③ twice → escalate to ①: the scope is wrong, not the technique
```

## Stage contracts

Each stage declares what it needs and what it must return. A stage that cannot
produce its artefact **fails loudly** — it never guesses forward.

### ① Discover — Product Strategy Team

| | |
|---|---|
| **Agents** | `product-manager`; add `business-analyst` when business rules or process are involved |
| **Needs** | The user's goal, any constraints, existing analytics if available |
| **Returns** | Problem statement, affected segment, **success metric**, non-goals, kill criterion |
| **Gate** | A success metric that is measurable. "Users are happier" fails. "Checkout completion rate, currently 61%, target 70%" passes. |

Ask the user rather than invent a metric. This is the one stage where stopping is correct.

### ② Architect — Architecture Team

| | |
|---|---|
| **Agents** | Route by domain: `backend-architect`, `frontend-architect`, `data-architect`, `security-architect`, `ai-architect`, `mobile-architect`… |
| **Needs** | Stage ① output verbatim, plus the current system state you read yourself |
| **Returns** | Options considered, trade-offs, failure modes, recommendation, ADR path, **and the contract design works inside**: what the system can return, in one call or several, how fast, and what it costs to change |
| **Returns** | Options considered, trade-offs, failure modes, recommendation, ADR path |
| **Gate** | Irreversible decision without an ADR does not proceed. Reversible ones may skip. |

Run architects in parallel **only when their concerns do not overlap**. Where two
disagree, do not average — state both positions and escalate to `enterprise-architect`.

**Architecture leads, but it does not get the last word on the screen.** Return the contract
as a starting position with its cost, not as a wall: "one call with these fields, adding a
field is cheap, realtime is expensive". Stage ③ designs inside it and pushes back when the
user's flow genuinely needs more. A contract that was never questioned is usually one that
was drawn against a guess.

### ③ Shape — Design Team

| | |
|---|---|
| **Agents** | `ui-designer` for any visible surface; add `ux-researcher` when the user's behaviour is disputed, `interaction-designer` for multi-step flows, `content-designer` for the strings, `design-ops-engineer` to say what the system already covers; `design-qa-engineer` closes the stage |
| **Needs** | Stage ① and ② output verbatim — the contract and its limits — plus the design system and the existing screens in the same flow |
| **Returns** | Two to three mock files with paths, the recommended variant marked, flow and state spec, interface copy, and the list of new tokens or components required |
| **Gate** | A user-facing change with no mock does not proceed. A described layout is not a mock. `design-qa-engineer` must find no undrawn reachable case. |

Skip this stage only when nothing visible changes, and say so.

**Design inside the contract.** Stage ② has already said what the system can return, how
fast, and at what cost. Mocks are drawn against that, not against a blank page — which is
what stops a beautiful screen that needs data nobody can produce.

**When the contract does not fit the screen, go back — do not bend the screen.** A mock
that has to add four requests, poll, or hide a field to satisfy the contract is reporting a
design flaw in ②. Send it back with the specific need: this list needs one call with these
fields. Quietly working around the contract in ④ is the failure this ordering exists to prevent.

**Where a mock needs a component the design system lacks**, say so here. It is an input to
④, not something an engineer invents mid-build.

**The design gets tested before anything is built.** `design-qa-engineer` walks the mock set
the way a user would and looks for the case nobody drew: the branch, the role, the limit, the
empty and worst-case content, the state with no way out. Contrast, target size, focus order,
and keyboard operability are checked here, on the mock, where fixing them costs an edit
rather than a rebuild. A design is not ready because it looks finished; it is ready when
every reachable case is drawn or explicitly ruled out of scope.

### ④ Build — owning engineering team

| | |
|---|---|
| **Agents** | `backend-developer`, `frontend-engineer`, `mobile-engineer`, `data-engineer`, `platform-engineer`… plus `database-engineer` for schema work |
| **Needs** | The ADR and contract from ②, the chosen mock and its state spec from ③, acceptance criteria from ① |
| **Returns** | Implementation, tests including failure paths, migrations, instrumentation |
| **Gate** | Tests must cover the failure path, not only the happy path |

### ⑤ Verify — Quality Engineering Team

| | |
|---|---|
| **Agents** | `code-reviewer` always; add the specialist matching the change: `api-quality-engineer`, `accessibility-qa-engineer`, `performance-test-engineer`, `security-test-engineer`, `data-quality-test-engineer` |
| **Needs** | The diff, the chosen mock, the ADR, the test results |
| **Returns** | Ranked findings — claim, evidence at `file:line`, impact, fix |
| **Gate** | Unresolved high-severity finding sends the work back to ④, not forward. A shipped screen that does not match the approved mock is a finding, not a detail. |

### ⑥ Release — Release & Reliability Team

The pipeline does not end at "the code works". It ends at a **release package** the
user can tag and push without doing further work.

| | |
|---|---|
| **Agents** | `production-readiness-engineer`, `release-manager`; `site-reliability-engineer` when SLOs are touched |
| **Needs** | Everything above |
| **Gate** | Red test, missing owner, missing runbook, or untested rollback → no ship |

**Run the full suite yourself.** Not the changed tests — the whole suite, plus lint and
build. Paste the actual result. "Tests pass" without output is an assertion, not evidence.
A test that was already failing before this change is reported as pre-existing, with proof.

**The release package** — every item, or say which is missing and why:

| Item | Content |
|---|---|
| Test evidence | Full suite command and its real output. Failures quoted exactly. |
| Version | The next version and **which SemVer rule applies**: breaking → major, additive → minor, fix → patch. Say which and why. |
| CHANGELOG entry | Added / Changed / Fixed / Security, written for a user, not a commit log |
| Release notes | What changed, who is affected, what they must do |
| Migration steps | Ordered, reversible, with the command for each — or "none" |
| Rollout plan | Canary percentage, health metric watched, abort threshold |
| Rollback | Exact steps, and how to confirm it worked |
| Owner | A named person. No owner, no launch. |
| Runbook | For every new alert this change introduces |

**Then stop and hand over.** Do not commit, tag, or push unless the user explicitly asks.
Present the exact commands and let them run it:

```bash
git add -A
git commit -m "<type>: <summary>"
git tag -a vX.Y.Z -m "vX.Y.Z"
git push origin main --follow-tags
```

### ⑦ Observe — post-release verification

Passing tests in CI is evidence the code does what the author expected. It is not evidence
the feature works for users. This stage closes that gap, and it is the one most often skipped.

| | |
|---|---|
| **Agents** | `qa` for the smoke pass; `user-acceptance-tester` for the profile panel; `site-reliability-engineer` for error, latency, and saturation; `product-manager` to read ①'s metric; add `web-ux-quality-engineer` when a user-facing flow changed |
| **Needs** | The deployed version, ①'s success metric and kill criterion, the rollout plan's abort threshold, the runbook |
| **Returns** | Smoke result on the real environment, the health window observed with numbers, the metric measured against ①'s target, and the decision: continue, hold, or roll back |
| **Gate** | Smoke failure or a breached abort threshold rolls back immediately. Diagnose from the rolled-back state, never from the burning one. |

**Real people, not the team.** `user-acceptance-tester` runs the released flow as a panel of
concrete profiles spanning the age range and the sectors the product claims to serve, on their
devices and their connections, with no instructions. The team cannot produce this evidence
itself: everyone who built it knows where the button is. A finding is ranked by how many
profiles failed, not by how surprising it was — one profile stuck is a case, every profile
stuck is a design defect that ③ and ⑤ both missed.

**Three checks, on three clocks.** The smoke pass runs within minutes of the deploy and answers
"is it alive": the critical path works end to end against real infrastructure, with real
auth, real data, and the config that environment actually has — the class of failure no test
double can catch. The panel runs in the days after, and answers "can a stranger do it". The
metric read comes days or weeks later, on the window ① named, and answers "did it work".
All three are this stage. Reporting only the first is the usual failure.

**Watch what the change can break, not everything.** Name the signals before the deploy:
error rate on the touched endpoints, p99 on the changed path, the funnel step ① measured,
and the resource the change consumes more of. A dashboard nobody named in advance is a
dashboard nobody reads at 3am.

**The kill criterion is real.** ① named the condition under which this feature is withdrawn.
If it is met, say so and withdraw it. A kill criterion that is quietly renegotiated once
the work is done was never a criterion — it was a formality, and every later one is too.

**Then close the loop.** The measured result returns to ① as input: the metric moved and
the next increment is scoped, it did not move and the problem statement was wrong, or the
feature is withdrawn. This is what makes the pipeline a cycle rather than a queue.

## Who is accountable for a stage

Every stage has a lead who owns its result end to end — `product-lead`, `architecture-lead`,
`design-lead`, the owning engineering lead, `quality-lead`, `release-lead`. The specialists
produce the work; the lead is answerable for whether the stage's artefact is real, whether
the gate was honestly assessed, and whether the hand-off carried everything the next stage
needs.

| | |
|---|---|
| **Owns** | The stage artefact, the gate verdict, and the state of the hand-off |
| **Decides** | Disagreements inside the team, and what is sent back rather than shipped with a caveat |
| **Escalates** | To `it-director` when two team leads cannot agree, always with a proposed decision |
| **Never** | Reports a gate as passed on work whose evidence they have not seen |

A backward step is reported by the lead who received the work, naming the stage it went back
to and why. `delivery-manager` tracks the hand-offs between teams — the boundary is where
work waits longest, and it is nobody's specialist job to notice.

Cross-team conflict that survives two attempts goes to `it-director`, who picks one position
rather than averaging them, and states what would reverse the decision.

## Going backwards

The arrows point both ways. A stage that cannot produce its artefact sends the work back
to the stage that made it impossible — with the reason, never silently.

```
  ①  ←──────────  ②        architecture says the feature as scoped cannot be built
  DISCOVER        ARCHITECT   at acceptable cost, risk, or time

  ②  ←──────────  ③        design says the contract cannot carry the flow the user needs
  ARCHITECT       SHAPE

  ①  ←────────────────────  ②→③ deadlock: the contract that fits the design is too
  DISCOVER                    expensive, and the design that fits the contract fails ①'s metric
```

**② back to ①.** When the architects find the feature as scoped is too expensive, too risky,
or blocked, `product-manager` re-opens it rather than the architects trimming it themselves.
Product decides what is cut: a smaller segment, a later phase, a different mechanism, or the
feature is dropped. Return to ② with the re-scoped problem and the metric restated — the
metric may have to move too, and that is a product decision, not an engineering one.

**③ back to ②.** When design shows the contract cannot carry the flow — the screen needs one
call and the contract gives four, or it needs a push and the contract polls — the architects
revisit. They either widen the contract and say what it costs, or state why it cannot move.
If it cannot move, ③ redesigns inside the real limit and says what the user loses.

**③ back to ①.** Design reaches the user before anyone else does, so it is the stage most
likely to find that ① aimed at the wrong thing: research shows the drop-off has a different
cause, or no mock can move the stated metric because the metric measures the wrong step.
That is a product problem, not an architecture one — go straight to ①, do not route it
through ②.

The bar is evidence, not preference. A named observation, a failed task in a usability
session, or a metric the flow demonstrably cannot reach. "This would feel better as a
wizard" is a stage ③ decision and stays inside ③; re-opening ① on taste burns the pipeline's
credibility and everyone starts skipping gates.

**Two bounces means the loop is wrong.** If ② and ③ hand the same problem back and forth
twice, the constraint is not technical — the scope is wrong. Escalate to ①. Product decides
between paying for the expensive contract, accepting the weaker flow, or cutting the feature.

**Every backward step is reported**, with the stage, the reason, and what changed on the way
forward. A hidden bounce turns into a rediscovered problem three stages later.

## Skipping stages

The pipeline is a default, not a ritual. Skip deliberately and say so:

| Task | Stages |
|---|---|
| Typo, comment, formatting | none — do it inline |
| Bug fix, cause understood | ④ ⑤ ⑦ (smoke only) |
| Backend-only change, nothing visible | ② ④ ⑤ ⑥ ⑦ |
| Feature inside an existing design | ③ ④ ⑤ ⑥ ⑦ |
| New feature | ① ② ③ ④ ⑤ ⑥ ⑦ |
| New system or vendor choice | ① ② ③ then stop for user approval before ④ |
| Incident | not this pipeline — use `/incident` |

State which stages you skipped and why. A silent skip is the failure mode.

## Worked example

> "Users abandon checkout. Fix it."

```
① DISCOVER — product-manager
   Reads analytics. Returns:
     Problem: 39% abandon at the payment step, up from 22% in March.
     Segment: mobile users on slow networks — 81% of abandonment.
     Metric: checkout completion 61% → 70%.
     Non-goals: no redesign of the cart, no new payment providers.
     Kill criterion: no movement after two weeks at full rollout.

   ⛔ Gate passed: metric is measurable.

     ↓ this output is the literal input to ②, not a paraphrase

② ARCHITECT — backend-architect + frontend-architect (parallel, distinct concerns)
   backend-architect:  payment confirmation blocks on a synchronous 3rd-party call,
                       p99 11s, no timeout. Recommends async confirmation + idempotency keys.
                       Contract: POST returns immediately with a pending id; status arrives
                       on a poll or a push. Adding fields is cheap; sub-second confirm is not.
   frontend-architect: no optimistic state; the user sees a dead button for 11s.
                       Recommends immediate pending state + resumable session.
   → ADR docs/adr/0012-async-payment-confirmation.md

   ⛔ Gate passed: irreversible (changes the payment contract), ADR written.

③ SHAPE — ui-designer + interaction-designer
   ui-designer:         three mocks of the pending state the contract forces — inline
                        pending, full-page confirmation, resumable drawer. Recommends the
                        drawer: it survives a backgrounded mobile browser.
                        → design/mocks/checkout-pending-{a,b,c}.html
   interaction-designer: state spec — submit, pending, confirmed, timed out, resumed.
                        Input is preserved on every failure path.
                        Pushes back on one point: the poll interval leaves a 4s dead
                        window; asks ② for a push channel on this one event. Granted.

   ⛔ Gate passed: mocks exist, one is chosen, contract gap raised in ③ not patched in ④.

④ BUILD — backend-developer + frontend-engineer
   Idempotency table, async confirmation worker, pending UI state,
   tests: duplicate submit, timeout, network loss mid-confirm.

   ⛔ Gate passed: failure paths tested.

⑤ VERIFY — code-reviewer + api-quality-engineer + web-ux-quality-engineer
   HIGH  api.py:240 — retry has no jitter; a provider blip causes a thundering herd.
   MED   checkout.tsx:88 — pending state has no screen reader announcement.

   ⛔ Gate FAILED on HIGH → back to ④. Fixed, re-verified, then forward.

⑤ RELEASE — production-readiness-engineer, release-manager
   Test run:  pytest -q  →  418 passed, 2 skipped, 0 failed (94s)
              npm test   →  212 passed
              ruff check →  clean
   Version:   1.4.0 → 1.5.0  (minor: async confirmation is additive,
              the old sync path stays until 2.0)
   CHANGELOG: ### Added — async payment confirmation with idempotency keys
              ### Fixed — checkout no longer blocks for up to 11s on provider latency
   Migration: 1 forward-only, adds payment_idempotency. Online, ~0.4s on 12M rows.
   Rollout:   canary 5% → 25% → 100%.
              Abort if completion rate < 61% or worker lag > 60s.
   Rollback:  feature flag payment_async_confirm=false. Table stays; it is unused when off.
   Owner:     @payments-team · Runbook: docs/runbooks/confirmation-worker-lag.md

   ⛔ Gate passed. Release package handed to the user; nothing pushed.
```

Note stage ④ sending work **backwards**. That is the pipeline functioning, not failing.

## Reporting

Report each stage as it completes — do not save everything for the end. Per stage:

```
### ① Discover — product-manager
<the artefact>
Gate: PASSED — metric is checkout completion 61% → 70%
```

At the end, one summary table: stage, agents, artefact, gate result.

## Anti-patterns

| Anti-pattern | What goes wrong |
|---|---|
| Running all seven stages on a typo | Enormous cost, zero added correctness |
| Paraphrasing stage output into the next stage | Detail loss compounds; stage ④ builds the wrong thing |
| Advancing past a failed gate "to save time" | The gate existed because that failure is expensive later |
| Running every architect in parallel | They overlap, contradict, and you arbitrate with no basis |
| Building a screen with no mock | The design gets invented inside component code, then argued about in review |
| Skipping ① because the user sounded certain | "Fix checkout" has no metric; without one, you cannot tell if you succeeded |
| Hiding a backwards step | Stage ⑤ pushing back to ④ is the system working — show it |
| "All tests pass" with no output | Unverifiable. Paste the real result. |
| Stopping at "the code works" | The user still has to figure out version, changelog, and rollback |
| Stopping at "it shipped" | Green CI is not a working feature; nobody checked the real environment |
| Reporting the smoke pass as the outcome | "Alive" is not "it worked". ①'s metric is the outcome. |
| Renegotiating the kill criterion after the build | It was never a criterion, and the next one will not be either |
| Committing or tagging unasked | Release is the user's decision, always |

## Done when

- [ ] Every stage that ran named its agents and produced its declared artefact.
- [ ] Every gate result is stated explicitly — PASSED, FAILED, or SKIPPED with a reason.
- [ ] Each stage received the previous stage's output verbatim, not summarised.
- [ ] Skipped stages are listed with the reason.
- [ ] Backwards steps are reported, not hidden.
- [ ] The full test suite was run and its real output shown — not summarised as "passing".
- [ ] The release package is complete, or each missing item is named with a reason.
- [ ] The version bump cites the SemVer rule that justifies it.
- [ ] Post-deploy smoke ran against the real environment and its result is shown.
- [ ] The signals to watch were named before the deploy, and the observed window is reported with numbers.
- [ ] ①'s metric was measured on the window ① named, or the date it will be is stated.
- [ ] The kill criterion was checked against reality, not renegotiated.
- [ ] Nothing was committed, tagged, or pushed without the user asking.
- [ ] The final summary table lets the user audit the whole chain.
"""
