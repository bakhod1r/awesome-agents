---
description: Delegate a task to the Mobile Engineering Team (6 agents).
argument-hint: <task for the Mobile Engineering Team>
---

Task: $ARGUMENTS

Team: **Mobile Engineering Team** — Ship native-quality mobile experiences that survive poor networks, old devices, and store review.

Roster:

- `mobile-engineer` — Mobile Engineer: Build mobile features that are fast, offline-tolerant, and crash-free.
- `mobile-ux-quality-engineer` — Mobile UX Quality Engineer: Validate mobile experience quality across devices, networks, and interruption scenarios.
- `ios-engineer` — iOS Engineer: Build iOS features that feel native, respect platform conventions, and survive App Review.
- `android-engineer` — Android Engineer: Build Android features that behave correctly across a fragmented device, OEM, and version matrix.
- `app-release-engineer` — App Release Engineer: Get mobile builds to users predictably, with staged rollout and a kill switch that works.
- `mobile-lead` — Mobile Engineering Lead: Own the outcome, sequencing, and standard of work for the Mobile Engineering Team.

1. Pick the minimum set of agents above that can complete the task. Name them and
   say in one line why each is needed.
2. Delegate to each with the Agent tool, `subagent_type` = the `slug` in backticks.
   Agents cannot call each other — every hand-off passes through you.
3. For work spanning several agents, run the team's architect or lead first, record
   the decision, then fan out to the implementers.
4. Merge the results, resolve contradictions explicitly, and report using the
   output-discipline rule: claim, evidence (`file:line`), impact, ranked by severity.

Do not do the work inline if a specialist agent above exists for it.
