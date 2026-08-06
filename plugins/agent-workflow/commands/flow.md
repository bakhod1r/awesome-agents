---
description: Take a goal from product discovery through to release, one gated stage at a time.
argument-hint: <goal, in business terms>
---

Goal: $ARGUMENTS

Use the `orchestration` skill. You are the orchestrator — agents cannot call each other,
so every hand-off passes through you.

1. **Size it first.** Decide which stages this actually needs (see the skill's table) and
   say which you are skipping and why. Do not run five stages on a one-line fix.
2. **Run each stage** with the agents the skill names for it. Pass the previous stage's
   output **verbatim** as input, never a paraphrase.
3. **Check the gate** after every stage. State PASSED, FAILED, or SKIPPED with the reason.
   A failed gate sends work backwards — report that, do not hide it.
4. **Stop for the user** when: no measurable success metric exists, a new vendor or system
   is being chosen, or a gate fails twice on the same issue.
5. **Report as you go**, one block per stage, then a final summary table.
