---
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
        │        │  │             interaction-designer, content-designer
        │        │  │             → 2-3 mock files, one recommended,
        │        │  │               flow + state spec, interface copy
        │        │  │             ⛔ visible change with no mock → nothing to build
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
        │        │                  │ ⑦ OBSERVE  qa + site-reliability-engineer
        │        │                  │            + product-manager on the metric
        │        │                  │            → post-deploy smoke on the real
        │        │                  │              environment, error and latency
        │        │                  │              watch, then ①'s metric measured
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
| **Agents** | `ui-designer` for any visible surface; add `ux-researcher` when the user's behaviour is disputed, `interaction-designer` for multi-step flows, `content-designer` for the strings, `design-ops-engineer` to say what the system already covers |
| **Needs** | Stage ① and ② output verbatim — the contract and its limits — plus the design system and the existing screens in the same flow |
| **Returns** | Two to three mock files with paths, the recommended variant marked, flow and state spec, interface copy, and the list of new tokens or components required |
| **Gate** | A user-facing change with no mock does not proceed. A described layout is not a mock. |

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
| **Agents** | `qa` for the smoke pass; `site-reliability-engineer` for error, latency, and saturation; `product-manager` to read ①'s metric; add `web-ux-quality-engineer` when a user-facing flow changed |
| **Needs** | The deployed version, ①'s success metric and kill criterion, the rollout plan's abort threshold, the runbook |
| **Returns** | Smoke result on the real environment, the health window observed with numbers, the metric measured against ①'s target, and the decision: continue, hold, or roll back |
| **Gate** | Smoke failure or a breached abort threshold rolls back immediately. Diagnose from the rolled-back state, never from the burning one. |

**Two checks, on two clocks.** The smoke pass runs within minutes of the deploy and answers
"is it alive": the critical path works end to end against real infrastructure, with real
auth, real data, and the config that environment actually has — the class of failure no test
double can catch. The metric read comes days or weeks later, on the window ① named, and
answers "did it work". Both are this stage. Reporting only the first is the usual failure.

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
