# awesome-agents

**109 specialist Claude Code subagents across 16 engineering teams — installable as a plugin marketplace.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Agents](https://img.shields.io/badge/agents-109-8A63D2)
![Teams](https://img.shields.io/badge/teams-16-8A63D2)
![Commands](https://img.shields.io/badge/commands-12-8A63D2)
![Skills](https://img.shields.io/badge/skills-11-8A63D2)

Most agent collections are a folder of prompts. This one enforces a chain:

> **architect decides → engineer implements → quality verifies → release ships.**

No link is skipped. Every agent is generated from one source of truth, so 109 roles
stay consistent instead of drifting apart file by file.

## Install

```
/plugin marketplace add bakhod1r/awesome-agents
/plugin install agent-workflow@awesome-agents
/plugin install security-team@awesome-agents
```

Install `agent-workflow` for the commands and skills, then one plugin per team you need.

### Pairs well with

[caveman](https://github.com/juliusbrussee/caveman) — strips filler from model prose while
leaving code, commands, file paths, and error strings byte-identical. 109 agents with a
ten-section contract each produce a lot of prose; this cuts the padding, not the reasoning.

```
/plugin marketplace add juliusbrussee/caveman
/plugin install caveman@caveman
/caveman ultra
```

## Use it

| You want | Run |
|---|---|
| A goal taken end to end | `/flow <goal>` |
| An architecture pass ending in an ADR | `/design <system>` |
| The current diff reviewed on three lenses | `/review` |
| A security audit | `/audit <scope>` |
| A STRIDE threat model | `/threat-model <feature>` |
| A production readiness gate | `/ship` |
| To know who owns this work | `/agents <task>` |

`/flow` walks product discovery → architecture → build → verify → release, stopping at each
stage for approval, so the work stays reviewable rather than arriving as one opaque dump.

## Teams

Architecture · Backend Engineering · Frontend Engineering · Mobile Engineering · Data & AI Engineering · Platform Engineering · Quality Engineering · Security Engineering · Release & Reliability · Product Strategy · Engineering Excellence · IT Operations & Infrastructure · MLOps & Model Operations · FinOps & Cost Engineering · Enterprise Applications · Governance, Risk & Privacy

Full roster with every agent's `name`, mission, and model: [.claude/teams/README.md](.claude/teams/README.md).

## Layout

```
CLAUDE.md              always loaded — the delegation rule
.claude/
  agents/              109 agent definitions        (generated)
  teams/               16 charters + roster index    (generated)
  commands/            12 slash commands
  skills/              11 on-demand procedures
  rules/               7 standing standards
  hooks/               SessionStart.sh
  output-styles/       evidence.md
  settings.json
.claude-plugin/
  marketplace.json     this repo, installable            (generated)
plugins/               one plugin per team + workflow    (generated)
docs/                  GitHub Pages site                 (generated)
scripts/
  agents_data.py       <- edit this
  agents_data_ext.py   second wave of teams
  generate.py          <- then run this
  site_builder.py      builds the docs site
```

## Contributing

Agent files are generated. Edit `scripts/agents_data.py`, then regenerate:

```bash
python3 scripts/generate.py   # rewrites everything marked (generated)
```

Hand edits to generated files are lost, deliberately: one source of truth is what keeps
109 agents consistent. See [CONTRIBUTING.md](CONTRIBUTING.md) and
[.claude/rules/agent-authoring.md](.claude/rules/agent-authoring.md).

## Docs

Site: <https://bakhod1r.github.io/awesome-agents/> — deployed by `.github/workflows/pages.yml`.

## Licence

MIT. See [LICENSE](LICENSE).
