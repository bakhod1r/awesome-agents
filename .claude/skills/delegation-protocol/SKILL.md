---
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
