# awesome-agents

16 teams, 109 Claude Code subagents, generated from a single source of truth.

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

## Regenerate

```bash
python3 scripts/generate.py
```

Everything marked *(generated)* is rewritten. Hand edits are lost — that is deliberate:
one source of truth keeps 109 agents consistent.

## Install as a plugin

```
/plugin marketplace add <your-org>/awesome-agents
/plugin install agent-workflow@awesome-agents
/plugin install security-team@awesome-agents
```

## Docs

Site: enable GitHub Pages on the `docs/` folder, or let `.github/workflows/pages.yml` deploy it.

## Roster

See [.claude/teams/README.md](.claude/teams/README.md).
