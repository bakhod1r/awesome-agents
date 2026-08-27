---
name: onboarding
description: Get a new user or contributor productive with this agent system. Use when someone asks how to start, how it works, or how to add an agent.
---

# Onboarding

## Use it (2 minutes)

Open the repo in Claude Code and ask normally. `CLAUDE.md` loads automatically,
Claude reads the roster and delegates. To force a specific agent, name it:

> Use the `database-architect` agent to review this schema.

Or route by command: `/team <task>`.

## Understand it (10 minutes)

| Path | What it is | Loaded |
|---|---|---|
| `CLAUDE.md` | The delegation rule | Always |
| `.claude/rules/*.md` | Standing standards | Always |
| `.claude/teams/README.md` | Full roster with `name` values | On lookup |
| `.claude/agents/<name>.md` | One agent, ten sections | When delegated to |
| `.claude/commands/*.md` | Slash commands | When invoked |
| `.claude/skills/*/SKILL.md` | Procedures | On demand, by description match |
| `scripts/agents_data.py` | **The only file you edit** | Never — it is the source |

## First tasks to try

| Goal | Say |
|---|---|
| Find the owner | "who handles database migrations here?" |
| Review a diff | `/review` |
| Design something | `/design payment retry logic` |
| Pre-release check | `/ship` |
| Security pass | `/audit src/api` |
| Cost pass | `/cost` |

## Extend it

```bash
# 1. add a record to AGENTS in scripts/agents_data.py
# 2. regenerate everything
python3 scripts/generate.py
```

Never hand-edit `.claude/agents/*.md` — regeneration overwrites it. That is deliberate:
one source of truth is what keeps 135 agents consistent.

### What separates a good agent record from a filler one

The template forces ten sections. It cannot force them to be *useful*. The difference
lives in two fields:

**Decision Rules — must be opinionated and falsifiable:**

```python
# Filler. True of every engineer who ever lived. Changes no behaviour.
rules=["Follow best practices", "Write clean code", "Consider performance"]

# Real. Each one rules out a specific thing the agent would otherwise do.
rules=[
    "Index to the query, not to the column.",
    "Any migration taking a long-lived exclusive lock is rejected; use an online strategy.",
    "Untested restores are not backups.",
]
```

**Quality Bar — must be checkable by someone else:**

```python
# Unfalsifiable. Nobody can fail this, so nobody passes it either.
bar=["High quality output", "Well documented", "Follows standards"]

# Checkable. Someone else can look and say yes or no.
bar=[
    "RTO and RPO measured in a real drill",
    "Hot queries have covering indexes",
    "No unbounded table scans on critical paths",
]
```

The test for both: **could a competent engineer disagree with this?** If not, it is
noise consuming context. Delete it and write something with an edge.

## Common mistakes

| Mistake | Consequence |
|---|---|
| Editing `.claude/agents/*.md` directly | Lost on the next `generate.py` run |
| Adding an agent with vague rules | It behaves exactly like the generalist you already had |
| Spawning five agents for one question | Overlapping reports, no decision |
| Skipping the architect on an irreversible decision | Rework at 10x cost later |
| Forgetting to rerun `generate.py` | CI fails: the Pages workflow blocks stale generated files |

## Done when

- [ ] The person has run one real task through a real agent.
- [ ] They know which file to edit (`scripts/agents_data.py`) and which never to (`.claude/agents/`).
- [ ] They can name the delegation chain: architect → engineer → quality → release.
