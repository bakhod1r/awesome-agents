# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

For this repository the semantics are:

- **major** — a breaking change to how agents are invoked: a removed or renamed agent `name`,
  a removed command, or a change to the plugin layout that breaks an existing install.
- **minor** — new agents, teams, skills, commands, or rules. Additive; nothing breaks.
- **patch** — content corrections, tooling fixes, site fixes.

## [1.0.0] - 2026-08-06

First stable release.

### Added

**109 specialist agents across 16 teams**, generated from a single source of truth.
Every agent carries the same ten sections — Role, Mission, Primary Objective, Responsibilities,
Collaboration, Inputs, Outputs, Decision Rules, Quality Bar, Output Format — plus a shared
operating standard requiring evidence over assertion and measurement over estimate.

| Team | Agents |
|---|---|
| Architecture | 13 |
| Quality Engineering | 15 |
| Security Engineering | 8 |
| IT Operations & Infrastructure | 8 |
| Backend Engineering | 7 |
| Frontend Engineering | 7 |
| Data & AI Engineering | 6 |
| Platform Engineering | 6 |
| MLOps & Model Operations | 6 |
| Mobile Engineering | 5 |
| Release & Reliability | 5 |
| Product Strategy | 5 |
| Enterprise Applications | 5 |
| Governance, Risk & Privacy | 5 |
| FinOps & Cost Engineering | 4 |
| Engineering Excellence | 4 |

Model allocation: 41 `opus` (architecture, security, and judgement-heavy roles), 68 `sonnet`.
Tool access is least-privilege — architects and reviewers are read-only.

**11 slash commands** — `/team`, `/design`, `/review`, `/ship`, `/audit`, `/incident`,
`/threat-model`, `/cost`, `/runbook`, `/agents`, `/onboard`.

**10 skills**, each with a procedure, a worked good-versus-bad example, an anti-pattern table,
and a "Done when" checklist — `delegation-protocol`, `agent-registry`, `adr`, `threat-model`,
`runbook`, `postmortem`, `data-contract`, `cost-review`, `marketplace`, `onboarding`.

**7 standing rules** applied to all work without being asked — engineering standard,
security baseline, testing, documentation, data & privacy, agent authoring, output discipline.

**Plugin marketplace.** The repository is installable via
`/plugin marketplace add <org>/awesome-agents`: one plugin per team plus `agent-workflow`
for the shared commands and skills.

**GitHub Pages site** at `docs/` — searchable roster, tutorial, and install guide.
Self-contained: no external scripts, stylesheets, fonts, or network calls.

**Tooling.**
- `scripts/generate.py` — regenerates everything from the data. Idempotent.
- `scripts/validate.py` — 7 check groups; used as the CI gate.
- CI blocks stale generated files and runs the validator on every pull request.
- Release workflow verifies the tag matches `VERSION` before publishing.

### Security

- Permission allowlist is project-scoped. The validator fails any rule reaching outside the
  repository (absolute, home-anchored, or parent-relative paths).
- Site data is escaped against `</script>` termination and rendered with `textContent`
  rather than `innerHTML`, so agent content cannot inject markup.
- Secrets, `.env` files, and `*secret*` paths are denied in `settings.json`.

### Known limitations

- Agent content is validated for **structure**, not for quality. The validator confirms every
  section exists and meets minimum field counts; it cannot confirm that a decision rule is
  falsifiable or that a quality bar is checkable. That review is human.
- The external plugin table in the `marketplace` skill was accurate when written.
  Marketplaces change — verify with `/plugin` before recommending an entry.
- No automated link checking against external URLs.

[1.0.0]: https://github.com/OWNER/awesome-agents/releases/tag/v1.0.0
