---
description: Route a task to the right team and delegate to its agents.
argument-hint: <task description>
---

Task: $ARGUMENTS

1. Read `.claude/teams/README.md` and pick the owning team (name it and justify in one line).
2. Pick the minimum set of agents from that team's roster that can complete the task.
3. Delegate to each with the Agent tool, giving each agent its required Inputs.
4. Merge the results, resolve contradictions explicitly, and report using the standard Output Format.

Do not do the work inline if a specialist agent exists for it.
