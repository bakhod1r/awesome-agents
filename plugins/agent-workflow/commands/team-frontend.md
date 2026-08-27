---
description: Delegate a task to the Frontend Engineering Team (8 agents).
argument-hint: <task for the Frontend Engineering Team>
---

Task: $ARGUMENTS

Team: **Frontend Engineering Team** — Deliver fast, accessible, resilient user interfaces backed by a coherent design system.

Roster:

- `frontend-engineer` — Frontend Engineer: Build accessible, performant interfaces that hold up on slow networks and real devices.
- `product-designer` — Product Designer: Design flows that solve the user problem with the least interface possible.
- `web-ux-quality-engineer` — Web UX Quality Engineer: Verify web experience quality: usability, responsiveness, performance, and polish.
- `design-system-engineer` — Design System Engineer: Build and maintain the component library so every surface stays consistent without forking.
- `web-performance-engineer` — Web Performance Engineer: Hold Core Web Vitals budgets on real user devices and networks, not lab averages.
- `internationalization-engineer` — Internationalization Engineer: Make the product correct in every supported locale, script, and writing direction.
- `desktop-engineer` — Desktop Engineer: Ship desktop applications that integrate with the operating system and update themselves safely.
- `frontend-lead` — Frontend Engineering Lead: Own the outcome, sequencing, and standard of work for the Frontend Engineering Team.

1. Pick the minimum set of agents above that can complete the task. Name them and
   say in one line why each is needed.
2. Delegate to each with the Agent tool, `subagent_type` = the `slug` in backticks.
   Agents cannot call each other — every hand-off passes through you.
3. For work spanning several agents, run the team's architect or lead first, record
   the decision, then fan out to the implementers.
4. Merge the results, resolve contradictions explicitly, and report using the
   output-discipline rule: claim, evidence (`file:line`), impact, ranked by severity.

Do not do the work inline if a specialist agent above exists for it.
