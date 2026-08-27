---
description: Delegate a task to the Quality Engineering Team (15 agents).
argument-hint: <task for the Quality Engineering Team>
---

Task: $ARGUMENTS

Team: **Quality Engineering Team** — Prevent defects from reaching users through risk-based testing, automation, and fast feedback.

Roster:

- `qa` — QA: Verify that what shipped matches what was intended, and find what nobody specified.
- `automation-qa-engineer` — Automation QA Engineer: Build fast, stable automated test suites that teams actually trust.
- `ai-test-automation-engineer` — AI Test Automation Engineer: Use AI to generate, maintain, and prioritise tests without lowering the evidence bar.
- `api-quality-engineer` — API Quality Engineer: Guarantee API correctness, compatibility, and resilience at the contract level.
- `accessibility-qa-engineer` — Accessibility QA Engineer: Ensure products are usable by people with disabilities and meet WCAG 2.2 AA.
- `bug-hunter-exploratory-testing-engineer` — Bug Hunter and Exploratory Testing Engineer: Find the defects scripted testing never reaches by attacking the system deliberately.
- `compatibility-test-engineer` — Compatibility Test Engineer: Verify the product works across the supported matrix of platforms, versions, and locales.
- `performance-test-engineer` — Performance Test Engineer: Prove the system meets latency and throughput targets and find where it breaks.
- `reliability-test-engineer` — Reliability Test Engineer: Verify the system degrades gracefully and recovers under failure.
- `observability-test-engineer` — Observability Test Engineer: Ensure production is actually debuggable: signals exist, are correct, and are actionable.
- `security-test-engineer` — Security Test Engineer: Test the system the way an attacker would, within authorised scope.
- `data-quality-test-engineer` — Data Quality Test Engineer: Prove data is complete, accurate, timely, and consistent before anyone decides on it.
- `database-test-engineer` — Database Test Engineer: Test the database layer: correctness under concurrency, migrations, and recovery.
- `test-data-engineer` — Test Data Engineer: Provide realistic, safe, on-demand test data for every environment.
- `code-reviewer` — Code Reviewer: Catch correctness, security, and maintainability defects before merge.

1. Pick the minimum set of agents above that can complete the task. Name them and
   say in one line why each is needed.
2. Delegate to each with the Agent tool, `subagent_type` = the `slug` in backticks.
   Agents cannot call each other — every hand-off passes through you.
3. For work spanning several agents, run the team's architect or lead first, record
   the decision, then fan out to the implementers.
4. Merge the results, resolve contradictions explicitly, and report using the
   output-discipline rule: claim, evidence (`file:line`), impact, ranked by severity.

Do not do the work inline if a specialist agent above exists for it.
