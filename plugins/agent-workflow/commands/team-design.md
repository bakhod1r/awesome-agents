---
description: Delegate a task to the Design Team (7 agents).
argument-hint: <task for the Design Team>
---

Task: $ARGUMENTS

Team: **Design Team** — Decide what the interface looks like and how it behaves, before a line of component code is written.

Roster:

- `ui-designer` — UI Designer: Turn a requirement into working interface mocks the team can choose between.
- `ux-researcher` — UX Researcher: Replace assumptions about users with evidence, before the team builds on them.
- `interaction-designer` — Interaction Designer: Specify how a flow behaves across every state, transition, and failure.
- `content-designer` — Content Designer: Write the words in the interface so the user knows what happened and what to do next.
- `design-qa-engineer` — Design QA Engineer: Test the design itself before anyone builds it, then test the build against the design.
- `design-ops-engineer` — Design Ops Engineer: Keep the design system and the codebase telling the same story, and make the handoff mechanical.
- `design-lead` — Design Lead: Own the outcome, sequencing, and standard of work for the Design Team.

1. Pick the minimum set of agents above that can complete the task. Name them and
   say in one line why each is needed.
2. Delegate to each with the Agent tool, `subagent_type` = the `slug` in backticks.
   Agents cannot call each other — every hand-off passes through you.
3. For work spanning several agents, run the team's architect or lead first, record
   the decision, then fan out to the implementers.
4. Merge the results, resolve contradictions explicitly, and report using the
   output-discipline rule: claim, evidence (`file:line`), impact, ranked by severity.

Do not do the work inline if a specialist agent above exists for it.
