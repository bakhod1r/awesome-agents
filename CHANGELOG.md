# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

For this repository the semantics are:

- **major** — a breaking change to how agents are invoked: a removed or renamed agent `name`,
  a removed command, or a change to the plugin layout that breaks an existing install.
- **minor** — new agents, teams, skills, commands, or rules. Additive; nothing breaks.
- **patch** — content corrections, tooling fixes, site fixes.

## [1.5.0] - 2026-08-27

### Added

**The spec is approved before anything downstream starts.** Stage ① now ends with a written
spec — problem with a number, scope, out-of-scope, testable acceptance criteria, metric with
its window, kill criterion, assumptions, open questions with owners, and a performance budget
— and an explicit yes from the user. Silence is not approval. A spec that changes later is
re-approved with the change named.

**Gates for the work that is expensive to retrofit.** A threat model on anything touching
authentication, money, personal data, uploads, or third-party input; a data contract before
the first row of any new table, event, or exported dataset; interface copy approved with the
design rather than shipped as placeholder; a test plan written from the mock before the code;
observability signals named before deploy; a rollback that was actually executed rather than
written; and a post-mortem with a regression test whenever a smoke fails or a rollback runs.

**Definition of done, per stage.** Artefact at a path, gate verdict with evidence, hand-off
passed verbatim, and every open item owned and dated. Confirmed by the stage lead, never
asserted by the author alone.

**Each team plans before it works.** Four lines from the lead before the specialists start —
steps, owner per step, evidence per step, and the risk with its earliest signal — and the
stage reports against that plan.

**Production ready, not demo ready.** A ten-point confirmation before release covering failure
paths, idempotency, validation, authorisation at the resource, reversible data changes,
limits, live observability, graceful degradation, secrets, and per-request cost against the
budget. Answered with file references; a checklist filled in from memory is the artefact of a
demo.

### Changed

**Every agent runs on `opus`.** These roles are judgement work end to end and a wrong judgement
costs more than the token difference. The authoring rule changed with it.

## [1.4.0] - 2026-08-27

### Added

**A lead for every team, generated from the team table.** 18 leads — `backend-lead`,
`design-lead`, `quality-lead`, and so on — so a team cannot exist without a named decider.
The lead owns the stage artefact, the gate verdict, and the hand-off, and never reports a
gate passed on evidence they have not seen. Source: `scripts/agents_data_leads.py`.

**Leadership Team.** `it-director` decides across teams when leads cannot agree, picking one
position rather than averaging, and states what would reverse the decision; `delivery-manager`
tracks cross-team dependencies and measures where work waits, since the boundary between two
teams is nobody's specialist job.

**`design-qa-engineer`.** Tests the design before it is built: the missing case, the branch
nobody drew, the state with no way out, contrast and focus order on the mock rather than after
the rebuild. Then compares the shipped screen to the approved mock.

**`user-acceptance-tester`.** Runs the released flow as a panel of concrete profiles across
the age range and sectors the product claims to serve, on their devices, with no instructions.
Findings rank by how many profiles failed. The team cannot produce this evidence itself —
everyone who built it knows where the button is.

### Changed

**Stage ③ ends with a design test.** `design-qa-engineer` closes the stage and an undrawn
reachable case blocks it; `ui-designer` now draws every case the flow reaches, not only the
main one, and an out-of-scope case must be named as such.

**Stage ⑦ has three checks on three clocks:** smoke within minutes, the user panel in the
days after, the success metric on the window discovery named.

**Stage accountability is explicit.** Each stage names its lead; backward steps are reported
by the lead who received the work; conflict surviving two attempts goes to `it-director`.

## [1.3.0] - 2026-08-27

### Added

**Design Team — 5 agents.** `ui-designer`, `ux-researcher`, `interaction-designer`,
`content-designer`, `design-ops-engineer`. Interface work previously started inside
component code because no team owned the step before it. The team's output is a set of
working mock alternatives with one recommended, a flow and state spec, the interface copy,
and a list of what the design system does not yet cover. Source: `scripts/agents_data_design.py`.

**One command per team.** `/team-frontend`, `/team-design`, `/team-backend`, and so on for
all 17 teams — the roster arrives inline, so naming the team is enough and `/team` no longer
has to guess. Generated from `TEAMS` in `generate.py`; 12 commands become 29.

### Changed

**The delivery pipeline has six stages, not five.** `orchestration` (`/flow`) gains
**③ SHAPE**, owned by the Design Team, gated on a mock: a user-facing change with no mock
does not proceed, and a described layout is not a mock. The order is ① Discover,
② Architect, ③ Shape, ④ Build, ⑤ Verify, ⑥ Release — architecture returns the contract
design works inside, stated with its cost rather than as a wall, and design pushes back when
the user's flow genuinely needs more. A shipped screen that does not match the approved mock
is now a verify-stage finding.

**Post-release verification is a stage, not a hope.** New **⑦ Observe**: a smoke pass on the
real environment within minutes of deploy, a named health window watched with numbers, and
①'s success metric measured on the window ① named — two checks on two clocks. A failed smoke
or a breached abort threshold rolls back first and diagnoses second, and the kill criterion is
checked against reality rather than renegotiated once the work is done. The measured result
returns to ① as input, which makes the pipeline a cycle rather than a queue. Seven stages.

**Backward flow is explicit.** A stage that cannot produce its artefact returns the work to
the stage that made it impossible: ② hands back to ① when the feature as scoped cannot be
built at acceptable cost, and product — not the architects — decides what is cut; ③ hands
back to ② when the contract cannot carry the flow. Two bounces between ② and ③ escalate to
①, on the grounds that the scope is wrong rather than the technique. Every backward step is
reported with its reason.

## [1.2.0] - 2026-08-06

### Added

**Caveman output compression, always on.** Per-IDE rule files for Cursor, Windsurf, Cline,
Copilot, and opencode, plus a root `AGENTS.md`, generated by `caveman-init`. The rule is also
stated in the generated `CLAUDE.md` so Claude Code loads it. Compression applies to prose only:
code, commands, file paths, and error strings are reproduced verbatim, and security warnings,
irreversible-action confirmations, commits, PRs, and documentation stay in normal prose.

**caveman recommended in the README and on the site.** Documented as an install rather than
vendored, per the marketplace rule. No token-saving figure is quoted — the site points at
`/caveman-stats` so readers measure their own.

### Changed

**`CLAUDE.md` marketplace line uses the real repository slug** instead of an `<org>` placeholder,
derived from the git remote like the rest of the generated links.

## [1.1.1] - 2026-08-06

### Fixed

**Real repository links everywhere.** The site and README shipped `<you>` and `<your-org>`
placeholders in the clone and `/plugin marketplace add` commands, so neither could be
copy-pasted. Both are now derived from the git remote, which also means a fork links to
itself rather than to upstream.

### Added

**Repository links on the site** — a `GitHub` entry in the header nav and an `owner/repo`
link in the footer. The site previously had no path back to the source.

**README rewrite** — pitch, badges, an install block, and a command table, replacing a
directory listing that never said what the project does.

## [1.1.0] - 2026-08-06

### Added

**`generate.py --check`** — reports which generated files differ from the source without
writing anything. CI now uses it in place of `git diff`, so staleness detection no longer
depends on being inside a git checkout or on mutating the working tree to find out.

**`/flow` command and `orchestration` skill** — runs a goal through five gated stages:
discover, design, build, verify, release. Each stage declares what it needs and what it
must return; no artefact, no advance. A failed verification gate sends work backwards to
build rather than forward. The final stage produces a release package — full test output,
version decision with the SemVer rule cited, changelog entry, migration steps, rollout
plan, rollback path, owner, runbook — and then stops, because tagging is the user's call.

### Fixed

- **The validator crashed instead of reporting on malformed JSON.** A broken
  `settings.json` raised `JSONDecodeError` out of `check_permissions` rather than
  producing a finding. All JSON reads now go through a single tolerant loader.

### Changed

- CI runs `generate.py --check`, then `validate.py`. Both gate every pull request; the
  release workflow runs the same two at the tagged commit.
- `site_builder.build()` accepts an injected writer, so dry-run generation covers the site.

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

[1.1.0]: https://github.com/bakhod1r/awesome-agents/releases/tag/v1.1.0
[1.0.0]: https://github.com/bakhod1r/awesome-agents/releases/tag/v1.0.0
