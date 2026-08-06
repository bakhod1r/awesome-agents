# Quality Engineering Team

## Mission

Prevent defects from reaching users through risk-based testing, automation, and fast feedback.

## Charter

- Test pyramid: many fast unit tests, few well-chosen end-to-end tests.
- No flaky test stays green-listed; quarantine and fix or delete.
- Every escaped defect produces a regression test and a root cause.

## Roster (15)

- [QA](../agents/qa.md) — Verify that what shipped matches what was intended, and find what nobody specified.
- [Automation QA Engineer](../agents/automation-qa-engineer.md) — Build fast, stable automated test suites that teams actually trust.
- [AI Test Automation Engineer](../agents/ai-test-automation-engineer.md) — Use AI to generate, maintain, and prioritise tests without lowering the evidence bar.
- [API Quality Engineer](../agents/api-quality-engineer.md) — Guarantee API correctness, compatibility, and resilience at the contract level.
- [Accessibility QA Engineer](../agents/accessibility-qa-engineer.md) — Ensure products are usable by people with disabilities and meet WCAG 2.2 AA.
- [Bug Hunter and Exploratory Testing Engineer](../agents/bug-hunter-exploratory-testing-engineer.md) — Find the defects scripted testing never reaches by attacking the system deliberately.
- [Compatibility Test Engineer](../agents/compatibility-test-engineer.md) — Verify the product works across the supported matrix of platforms, versions, and locales.
- [Performance Test Engineer](../agents/performance-test-engineer.md) — Prove the system meets latency and throughput targets and find where it breaks.
- [Reliability Test Engineer](../agents/reliability-test-engineer.md) — Verify the system degrades gracefully and recovers under failure.
- [Observability Test Engineer](../agents/observability-test-engineer.md) — Ensure production is actually debuggable: signals exist, are correct, and are actionable.
- [Security Test Engineer](../agents/security-test-engineer.md) — Test the system the way an attacker would, within authorised scope.
- [Data Quality Test Engineer](../agents/data-quality-test-engineer.md) — Prove data is complete, accurate, timely, and consistent before anyone decides on it.
- [Database Test Engineer](../agents/database-test-engineer.md) — Test the database layer: correctness under concurrency, migrations, and recovery.
- [Test Data Engineer](../agents/test-data-engineer.md) — Provide realistic, safe, on-demand test data for every environment.
- [Code Reviewer](../agents/code-reviewer.md) — Catch correctness, security, and maintainability defects before merge.

## How to engage

Delegate to a single agent with the Agent tool using its `name` from the roster above.
For work spanning several of these agents, start with the team's architect or lead,
get the design decision recorded, then fan out to implementers.
