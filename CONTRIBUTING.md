# Contributing

## The one rule

`.claude/agents/`, `.claude/teams/`, `plugins/`, `docs/`, `README.md`, `CLAUDE.md`, and
`.claude-plugin/marketplace.json` are **generated**. Never edit them — CI rejects the pull request.

| To change | Edit |
|---|---|
| An agent, or add one | `scripts/agents_data.py` (or `agents_data_ext.py`) |
| A skill | `scripts/skills_data.py` |
| A command, rule, or hook | `scripts/generate.py` |
| The website | `scripts/site_builder.py` |

Then:

```bash
python3 scripts/generate.py
python3 scripts/validate.py
```

Both must pass before you open a pull request. No dependencies beyond Python 3.11+.

`generate.py --check` reports which generated files differ from the source without
writing anything — that is what CI uses to reject stale output.

## Adding an agent

```python
dict(
    slug="graph-database-engineer",          # kebab-case, unique
    title="Graph Database Engineer",
    team="backend",                          # must exist in TEAMS
    model="sonnet",                          # opus for architecture/security/judgement
    tools=FULL,                              # FULL | RO | DOC — least privilege
    mission="Design and operate graph stores for traversal-heavy workloads.",
    focus=[...],    # >=3 responsibilities
    inputs=[...], outputs=[...],             # >=2 each
    rules=[...],    # >=2 decision rules
    bar=[...],      # >=2 quality bar items
)
```

### The bar for a new agent

The template forces the ten sections. It cannot force them to be useful.

**Decision rules must be falsifiable.** The test: *could a competent engineer disagree?*

```python
rules=["Follow best practices"]                          # noise, consuming context
rules=["Index to the query, not to the column."]         # rules out a specific wrong move
```

**Quality bar must be checkable by someone else.**

```python
bar=["High quality output"]                              # nobody can fail this
bar=["RTO and RPO measured in a real drill"]             # yes or no, verifiable
```

If a new agent's rules would apply equally to three existing agents, it is not a new
specialist — it is a duplicate. Extend the existing one instead.

## What CI checks

- Generated files match the source (staleness gate).
- Every agent: kebab-case slug, unique, valid team and model, all ten sections, minimum field counts.
- Every skill: frontmatter name matches its directory, has a `## Done when` checklist.
- Every agent name referenced in a command or skill actually exists.
- All JSON valid; every marketplace entry resolves to a real `plugin.json`.
- The site has no external asset references and embeds every agent.
- No permission rule reaches outside the project.
