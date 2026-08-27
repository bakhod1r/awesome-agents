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
  │              → written spec: scope, out-of-scope, acceptance criteria
  │              ⛔ no measurable metric → stop, ask the user
  │              ⛔ spec not approved by the user → nothing downstream starts
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

**The stage ends with an approved spec, not a conversation.** `product-lead` writes it and
puts it in front of the user; `business-analyst` supplies the rules where the domain is
involved. Everything downstream quotes this document, so an ambiguity left in it is an
ambiguity built into the product.

| Section | What it must say |
|---|---|
| Problem | Who is blocked, at which step, and what it costs today — with a number |
| Scope | The specific capability being built, in the user's language |
| Out of scope | What a reader might reasonably assume is included and is not |
| Acceptance criteria | Observable conditions, each one testable: given, when, then |
| Success metric | Current value, target value, and the window it is measured over |
| Kill criterion | The condition under which the feature is withdrawn |
| Performance budget | The number the result must hold: page or endpoint latency, payload size, cost per request. Agreed here, so ⑤ has nothing to argue about |
| Assumptions | What is taken as true without proof, and what breaks if it is wrong |
| Open questions | Each with an owner and a date, or the stage is not finished |

**Approval is explicit and it is the user's.** Not "no objection", not silence — a stated
yes to that document. Until it exists, ② has nothing to design against and every later
disagreement about "what we agreed" is unresolvable. An approved spec that changes later is
fine and normal; it is re-approved, with what changed named.

### ② Architect — Architecture Team

| | |
|---|---|
| **Agents** | Route by domain: `backend-architect`, `frontend-architect`, `data-architect`, `security-architect`, `ai-architect`, `mobile-architect`… |
| **Needs** | Stage ① output verbatim, plus the current system state you read yourself |
| **Returns** | Options considered, trade-offs, failure modes, recommendation, ADR path, **and the contract design works inside**: what the system can return, in one call or several, how fast, and what it costs to change |
| **Returns** | Options considered, trade-offs, failure modes, recommendation, ADR path |
| **Gate** | Irreversible decision without an ADR does not proceed. Reversible ones may skip. A change touching authentication, money, personal data, file upload, or third-party input does not proceed without a threat model. A new table, event, or exported dataset does not proceed without a data contract. |

**Threat model where it earns its place.** `security-architect` runs the `threat-model` skill
on anything handling authentication, money, personal data, uploads, or third-party input.
STRIDE per trust boundary, each threat with its mitigation and where that mitigation lives.
A feature that touches none of those skips it and says so.

**Data contract for anything another system will read.** `data-architect` — or the owning
`database-architect` — names the owner, the schema, the grain, the classification, the
retention period, and the deprecation path before the first row exists. Retrofitting a
contract onto a table that already has consumers is the expensive version of this work.

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

**Interface copy is approved with the design, not after it.** `content-designer` delivers the
strings as part of this stage and they are reviewed here. Placeholder text that reaches ④
ships; every team has a screen with a "TODO: better wording" in production to prove it.

**The test plan is written before the code, from the mock.** `quality-lead` names, per case
in the mock: what proves it works, at which layer, and what the failure input is. Written
after the build, a test plan documents what the code happens to do rather than what the
feature is supposed to do.

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
| **Gate** | Red test, missing owner, missing runbook, or a rollback nobody executed → no ship |

**A written rollback is not a rollback.** Run it. Deploy the change to an environment that
matters, roll it back, and confirm the system is serving correctly afterwards — including the
data: a migration that cannot be reversed without loss must say so in the release package and
carry the recovery procedure instead. Paste what you ran and what came back. The middle of an
incident is where untested rollback procedures are discovered to be wrong.

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

**A rollback or a failed smoke earns a post-mortem.** Use the `postmortem` skill: timeline,
what was believed at each point, why the gates let it through, and a regression test that
would have caught it. Blameless, and written before the next release, not "when things calm
down" — that moment does not arrive. The action items land in the pipeline as gate changes,
not as a list nobody rereads.

**Then close the loop.** The measured result returns to ① as input: the metric moved and
the next increment is scoped, it did not move and the problem statement was wrong, or the
feature is withdrawn. This is what makes the pipeline a cycle rather than a queue.

## Definition of done, per stage

A stage is done when its lead can show four things. Anything less is "in progress", however
it feels.

| | |
|---|---|
| **Artefact** | The document, mock, code, or report the stage declares — existing as a file, at a path, not as a description in the chat |
| **Gate verdict** | PASSED, FAILED, or SKIPPED, with the evidence behind it |
| **Hand-off** | Everything the next stage needs, passed verbatim |
| **Open items** | Each with an owner and a date, or the stage is not done |

"Done" is never asserted by the person who did the work alone; the stage lead confirms it
against the artefact.

## Each team plans before it works

Every stage begins with its lead writing a short plan and ends against it. Not a document —
four lines, before the specialists start:

| | |
|---|---|
| **Steps** | What will be done, in order |
| **Owner** | Which agent does each step |
| **Evidence** | What will prove each step is done |
| **Risk** | What could make this stage fail, and the earliest signal of it |

A stage that ends differently from its plan says so and why. Planning that never survives
contact is planning aimed at the wrong things — and the pattern is the useful finding.

## Production ready, not demo ready

The pipeline's output is a feature that survives real use, not one that works when the person
who built it drives it. Before ⑥, the owning lead confirms each of these or names it as
knowingly missing, with the reason:

| | |
|---|---|
| Failure paths | Every external call has a timeout, a retry policy where retry is safe, and a defined behaviour when it fails |
| Idempotency | Anything that can be submitted twice — by a user double-tap, a retry, or a queue redelivery — is safe to submit twice |
| Validation | Input is validated at the boundary, allowlist first, and the error tells the user what to fix |
| Authorisation | Checked at the resource, not only the route, with a negative test proving denial |
| Data | Migration is reversible or its recovery procedure is written; retention and deletion reach every copy |
| Limits | Pagination, payload caps, and rate limits exist on anything a client can call in a loop |
| Observability | The signals named in ④ are emitting, and an alert has a runbook |
| Degradation | The feature fails to a usable state, not a blank screen or a spinner that never resolves |
| Secrets | Nothing in code, logs, fixtures, or error messages |
| Cost | The per-request cost is known and inside the budget ① set |

A "yes" here means someone checked, with a file reference. A checklist filled in from memory
is the artefact of a demo, not a product.

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
- [ ] The spec was approved by the user before anything downstream started.
- [ ] Each stage wrote its plan before starting and reported against it.
- [ ] Threat model and data contract exist where the change required them, or their absence is justified.
- [ ] Interface copy was approved with the design, not left as placeholder.
- [ ] The test plan was written from the mock, before the code.
- [ ] The rollback was executed, not just written, and the result pasted.
- [ ] The production-ready checklist is answered with file references, not from memory.
- [ ] A rollback or failed smoke produced a post-mortem with a regression test.
- [ ] Nothing was committed, tagged, or pushed without the user asking.
- [ ] The final summary table lets the user audit the whole chain.
