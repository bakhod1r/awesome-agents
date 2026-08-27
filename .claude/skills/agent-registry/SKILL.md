---
name: agent-registry
description: Look up which agent or team owns a kind of work in this repository. Use when deciding whom to delegate to, when the user names a role, or when asked "who handles X".
---

# Agent Registry

## Where the roster lives

| File | Contents |
|---|---|
| `.claude/teams/README.md` | Every agent: title, `name`, team, model |
| `.claude/teams/<team>.md` | One team: mission, charter, roster with missions |
| `.claude/agents/<name>.md` | One agent: all ten sections |

The `name` in frontmatter is what the Agent tool takes. It is the kebab-case slug.

## Lookup procedure

1. Reduce the request to a **domain noun**: "migration", "drift", "egress cost", "screen reader".
2. Grep the roster for it. `.claude/teams/README.md` holds all 114 missions in one file.
3. Read the candidate's **Decision Rules** section. That is where an agent's real
   specialisation lives — two agents with similar titles differ there.
4. Pick one. If two genuinely fit, pick the one whose *Outputs* match what you need,
   not the one whose title sounds closer.

## Disambiguation — the pairs people confuse

| Question | Answer | Not |
|---|---|---|
| Design the schema | `database-architect` | `database-engineer` (tunes and migrates an existing one) |
| Build a metrics pipeline | `observability-engineer` | `observability-test-engineer` (verifies signals exist and are correct) |
| Write the model | `ai-engineer` | `mlops-engineer` (ships, versions, monitors it) |
| Is the model still good? | `model-monitoring-engineer` | `ai-evaluation-engineer` (builds the eval sets and metrics) |
| Cloud account hardening | `cloud-security-engineer` | `platform-engineer` (builds on it) |
| Corporate servers, patching, IAM | `systems-administrator`, `iam-engineer` | `platform-engineer` (product infrastructure) |
| Attack it | `penetration-tester` (authorised, proves exploitability) | `security-test-engineer` (in-CI security regression) |
| Watch the alerts | `soc-analyst` | `incident-response-engineer` (commands the response) |
| Cost of a design | `cloud-cost-architect` | `finops-engineer` (attributes and optimises a running bill) |
| Requirements | `business-analyst` (process and rules) | `product-manager` (what to build and why) |

## Worked example

> "Our S3 bill tripled last month."

- Domain noun: **cost**, running system, already spent.
- `finops-engineer` — attribution and waste on an existing bill. **First choice.**
- `cloud-cost-architect` — only if the finding is architectural (egress pattern, storage class
  by design). Escalate to it after attribution, not before.
- `data-engineer` — pulled in if the driver turns out to be pipeline file-sizing.

Answer: **`finops-engineer` first.** Name the follow-ons as conditional, not parallel.

## Rules

- One agent per concern. Do not fan out to five for a one-file change.
- Architects decide, engineers implement, quality verifies. Do not skip the middle.
- If nothing fits, say so plainly and name the roster gap. Do not force the nearest agent —
  a wrong specialist is more confidently wrong than a generalist.

## Done when

- [ ] A single best-fit agent is named, with the `name` value, not just the title.
- [ ] The reason for the fit cites the agent's Decision Rules or Outputs, not its title.
- [ ] Near-misses are named as conditional follow-ons, not as parallel work.
- [ ] A genuine gap is reported as a gap.
