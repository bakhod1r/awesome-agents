---
name: orchestration
description: Run a task end to end through the full delivery pipeline — product discovery, architecture, build, verification, release. Use when the user gives a goal rather than a specific technical instruction, or invokes /flow.
---

# Orchestration

One task. Five stages. Each stage produces an artefact the next stage consumes.
**No artefact, no advance** — that is the whole mechanism.

You are the orchestrator. Agents cannot call each other; they have no Agent tool.
Every hand-off passes through you, which is what makes the chain inspectable.

## The pipeline

```
  USER GOAL
     │
  ① DISCOVER    product-manager, business-analyst
     │          → problem, affected segment, success metric, non-goals
     │          ⛔ GATE: no measurable success metric → stop and ask the user
     │
  ② DESIGN      the relevant architects
     │          → options, trade-offs, failure modes, ADR
     │          ⛔ GATE: no ADR for an irreversible decision → do not build
     │
  ③ BUILD       engineers from the owning team
     │          → implementation, tests, migrations, instrumentation
     │          ⛔ GATE: no tests on the failure path → not done
     │
  ④ VERIFY      code-reviewer + the quality agent for the changed area
     │          → ranked findings, each with a concrete failure scenario
     │          ⛔ GATE: any unresolved high-severity finding → back to ③
     │
  ⑤ RELEASE     production-readiness-engineer, release-manager, SRE
                → full test run, version decision, CHANGELOG entry,
                  release notes, rollout plan, rollback, abort criteria
                ⛔ GATE: red test, or no owner / runbook / rollback → no ship
                          ↓
                    RELEASE PACKAGE  — handed to the user, ready to tag
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

### ② Design — Architecture Team

| | |
|---|---|
| **Agents** | Route by domain: `backend-architect`, `frontend-architect`, `data-architect`, `security-architect`, `ai-architect`, `mobile-architect`… |
| **Needs** | Stage ① output verbatim, plus the current system state you read yourself |
| **Returns** | Options considered, trade-offs, failure modes, recommendation, ADR path |
| **Gate** | Irreversible decision without an ADR does not proceed. Reversible ones may skip. |

Run architects in parallel **only when their concerns do not overlap**. Where two
disagree, do not average — state both positions and escalate to `enterprise-architect`.

### ③ Build — owning engineering team

| | |
|---|---|
| **Agents** | `backend-developer`, `frontend-engineer`, `mobile-engineer`, `data-engineer`, `platform-engineer`… plus `database-engineer` for schema work |
| **Needs** | The accepted design, the ADR, acceptance criteria from ① |
| **Returns** | Implementation, tests including failure paths, migrations, instrumentation |
| **Gate** | Tests must cover the failure path, not only the happy path |

### ④ Verify — Quality Engineering Team

| | |
|---|---|
| **Agents** | `code-reviewer` always; add the specialist matching the change: `api-quality-engineer`, `accessibility-qa-engineer`, `performance-test-engineer`, `security-test-engineer`, `data-quality-test-engineer` |
| **Needs** | The diff, the design, the test results |
| **Returns** | Ranked findings — claim, evidence at `file:line`, impact, fix |
| **Gate** | Unresolved high-severity finding sends the work back to ③, not forward |

### ⑤ Release — Release & Reliability Team

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

## Skipping stages

The pipeline is a default, not a ritual. Skip deliberately and say so:

| Task | Stages |
|---|---|
| Typo, comment, formatting | none — do it inline |
| Bug fix, cause understood | ③ ④ |
| Feature inside an existing design | ③ ④ ⑤ |
| New feature | ① ② ③ ④ ⑤ |
| New system or vendor choice | ① ② then stop for user approval before ③ |
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

② DESIGN — backend-architect + frontend-architect (parallel, distinct concerns)
   backend-architect:  payment confirmation blocks on a synchronous 3rd-party call,
                       p99 11s, no timeout. Recommends async confirmation + idempotency keys.
   frontend-architect: no optimistic state; the user sees a dead button for 11s.
                       Recommends immediate pending state + resumable session.
   → ADR docs/adr/0012-async-payment-confirmation.md

   ⛔ Gate passed: irreversible (changes the payment contract), ADR written.

③ BUILD — backend-developer + frontend-engineer
   Idempotency table, async confirmation worker, pending UI state,
   tests: duplicate submit, timeout, network loss mid-confirm.

   ⛔ Gate passed: failure paths tested.

④ VERIFY — code-reviewer + api-quality-engineer + web-ux-quality-engineer
   HIGH  api.py:240 — retry has no jitter; a provider blip causes a thundering herd.
   MED   checkout.tsx:88 — pending state has no screen reader announcement.

   ⛔ Gate FAILED on HIGH → back to ③. Fixed, re-verified, then forward.

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
| Running all five stages on a typo | Enormous cost, zero added correctness |
| Paraphrasing stage output into the next stage | Detail loss compounds; stage ③ builds the wrong thing |
| Advancing past a failed gate "to save time" | The gate existed because that failure is expensive later |
| Running every architect in parallel | They overlap, contradict, and you arbitrate with no basis |
| Skipping ① because the user sounded certain | "Fix checkout" has no metric; without one, you cannot tell if you succeeded |
| Hiding a backwards step | Stage ④ pushing back to ③ is the system working — show it |
| "All tests pass" with no output | Unverifiable. Paste the real result. |
| Stopping at "the code works" | The user still has to figure out version, changelog, and rollback |
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
- [ ] Nothing was committed, tagged, or pushed without the user asking.
- [ ] The final summary table lets the user audit the whole chain.
