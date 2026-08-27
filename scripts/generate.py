#!/usr/bin/env python3
"""Generate the full .claude/ control centre for this repository.

Run:  python3 scripts/generate.py
Idempotent: every generated file is rewritten from agents_data.py.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from agents_data import AGENTS, TEAMS  # noqa: E402
from skills_data import SKILLS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CLAUDE = ROOT / ".claude"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

# Owner shown in the marketplace listing and in plugin manifests.
# Derived from the git remote so a fork lists itself, not upstream.
def _owner() -> tuple[str, str]:
    try:
        url = subprocess.run(["git", "remote", "get-url", "origin"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.strip()
        m = re.search(r"[:/]([^/]+)/([^/]+?)(?:\.git)?$", url)
        if m:
            return m.group(1), m.group(2)
    except Exception:
        pass
    return "awesome-agents", "awesome-agents"


OWNER, REPO_NAME = _owner()
REPO_URL = f"https://github.com/{OWNER}/{REPO_NAME}"

GLOBAL_STANDARD = """## Global Standard

Operate as a top 0.1% professional: security, reliability, maintainability, and
measurable outcomes over speed of output. Refuse to emit guesswork, unvalidated
assumptions, or undocumented work.

- Read the actual code, data, or telemetry before concluding. Never answer from memory about this system.
- Label what you verified separately from what you inferred.
- Quantify. Not "slow" but "p99 480 ms against a 200 ms budget, measured over 1 h".
- When information is missing, state the assumption and its blast radius, then proceed.
- Prefer the simplest sufficient solution; say what you rejected and why.
- Deliver the whole scope. If part is blocked, finish the rest and name what was left out.
- Escalate with a proposed decision, never a bare problem.
"""

def agent_md(a: dict) -> str:
    team = TEAMS[a["team"]]
    peers = [p["title"] for p in AGENTS if p["team"] == a["team"] and p["slug"] != a["slug"]]
    responsibilities = "\n".join(f"{i}. {f}" for i, f in enumerate(a["focus"], 1))
    inputs = "\n".join(f"- {i}" for i in a["inputs"])
    outputs = "\n".join(f"- {o}" for o in a["outputs"])
    rules = "\n".join(f"- {r}" for r in a["rules"])
    bar = "\n".join(f"- {b}" for b in a["bar"])
    collab = ", ".join(peers) if peers else "other teams as needed"

    return f"""---
name: {a['slug']}
description: {a['mission']} Invoke for {a['team']}-team work.
model: {a['model']}
tools: {a['tools']}
---

# {a['title']}

**Team:** {team['title']}

## Role

{a['title']}, {team['title']}.

## Mission

{a['mission']}

## Primary Objective

Within the team mandate — {team['mission'][0].lower() + team['mission'][1:].rstrip('.')} — your single objective is the mission above.

## Responsibilities

{responsibilities}

## Collaboration

- **Inside {team['title']}:** {collab}.
- **Upstream:** accept work only when the inputs below are present; ask for the missing one rather than guessing.
- **Downstream:** hand off with the outputs below, complete enough that the receiver needs no follow-up meeting.
- **Escalation:** raise cross-team conflicts to the relevant architect with a recommended decision attached.

## Inputs

{inputs}

## Outputs

{outputs}

## Decision Rules

{rules}
- When two rules conflict, choose the one that protects user data and production stability.
- When evidence is missing, say so and state what would resolve it — never fabricate a number.

## Quality Bar

{bar}
- Every claim is backed by a file reference, a measurement, or a citation.
- Work is reproducible by someone else from the artefact alone.

{GLOBAL_STANDARD}

## Output Format

Use these headings, omitting any that genuinely do not apply. No filler, no praise,
no restating the request.

- **Summary** — what you did, found, and what it means.
- **Findings / Design** — ranked by severity; each: claim, evidence (`file:line`, metric, source), impact.
- **Recommendation** — the decision you would make, and the rejected alternatives.
- **Deliverables** — artefacts produced or changed, with paths.
- **Risks & Open Questions** — what could still be wrong, what you need from whom.
"""


def team_md(key: str, t: dict) -> str:
    members = [a for a in AGENTS if a["team"] == key]
    charter = "\n".join(f"- {c}" for c in t["charter"])
    roster = "\n".join(f"- [{a['title']}](../agents/{a['slug']}.md) — {a['mission']}" for a in members)
    return f"""# {t['title']}

## Mission

{t['mission']}

## Charter

{charter}

## Roster ({len(members)})

{roster}

## How to engage

Delegate to a single agent with the Agent tool using its `name` from the roster above.
For work spanning several of these agents, start with the team's architect or lead,
get the design decision recorded, then fan out to implementers.
"""


# When dry-running, write() compares instead of writing and records what differs.
_DRY_RUN = False
_STALE: list[str] = []


def write(path: Path, content: str) -> None:
    if _DRY_RUN:
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != content:
            _STALE.append(path.relative_to(ROOT).as_posix())
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def check() -> list[str]:
    """Return the generated paths that differ from what the source would produce.

    Writes nothing. An empty list means the committed tree is current.
    """
    global _DRY_RUN, _STALE
    _DRY_RUN, _STALE = True, []
    try:
        main(quiet=True)
    finally:
        _DRY_RUN = False
    return list(_STALE)


def build_marketplace() -> None:
    """Package the roster as installable plugins: one per team, plus the shared workflow."""
    plugins_dir = ROOT / "plugins"
    entries = []

    for key, t in TEAMS.items():
        members = [a for a in AGENTS if a["team"] == key]
        pname = f"{key}-team"
        pdir = plugins_dir / pname
        write(pdir / ".claude-plugin" / "plugin.json", json.dumps({
            "name": pname,
            "description": f"{t['title']} — {len(members)} specialist agents. {t['mission']}",
            "version": VERSION,
            "author": {"name": OWNER, "url": REPO_URL},
            "homepage": REPO_URL,
            "keywords": ["claude-code", "agents", "subagents", key],
        }, indent=2) + "\n")
        for a in members:
            write(pdir / "agents" / f"{a['slug']}.md", agent_md(a))
        entries.append({
            "name": pname,
            "source": f"./plugins/{pname}",
            "description": f"{t['title']}: {', '.join(a['title'] for a in members[:4])}"
                           + (f" and {len(members) - 4} more." if len(members) > 4 else "."),
        })

    # shared workflow plugin: commands, skills, rules — no agents
    core = plugins_dir / "agent-workflow"
    write(core / ".claude-plugin" / "plugin.json", json.dumps({
        "name": "agent-workflow",
        "description": "Delegation commands, procedural skills, and engineering standards shared by every team plugin.",
        "version": VERSION,
        "author": {"name": OWNER, "url": REPO_URL},
    }, indent=2) + "\n")
    for src in sorted((CLAUDE / "commands").glob("*.md")):
        write(core / "commands" / src.name, src.read_text(encoding="utf-8"))
    for src in sorted((CLAUDE / "skills").glob("*/SKILL.md")):
        write(core / "skills" / src.parent.name / "SKILL.md", src.read_text(encoding="utf-8"))
    entries.insert(0, {
        "name": "agent-workflow",
        "source": "./plugins/agent-workflow",
        "description": "Delegation commands (/team /design /review /ship /audit /incident /cost /threat-model /runbook) plus the shared skills.",
    })

    write(ROOT / ".claude-plugin" / "marketplace.json", json.dumps({
        "name": "awesome-agents",
        "owner": {"name": OWNER, "url": REPO_URL},
        "metadata": {
            "description": f"{len(AGENTS)} specialist engineering agents across {len(TEAMS)} teams, "
                           "each written to a top 0.1% professional standard.",
        },
        "plugins": entries,
    }, indent=2) + "\n")


def main(quiet: bool = False) -> None:
    # --- agents ---
    for a in AGENTS:
        write(CLAUDE / "agents" / f"{a['slug']}.md", agent_md(a))

    # --- teams ---
    for key, t in TEAMS.items():
        write(CLAUDE / "teams" / f"{key}.md", team_md(key, t))

    team_index = "\n".join(
        f"- [{t['title']}](teams/{k}.md) — {len([a for a in AGENTS if a['team'] == k])} agents. {t['mission']}"
        for k, t in TEAMS.items()
    )
    agent_index = "\n".join(
        f"| {a['title']} | `{a['slug']}` | {TEAMS[a['team']]['title']} | {a['model']} |" for a in sorted(AGENTS, key=lambda x: x["title"])
    )
    write(CLAUDE / "teams" / "README.md", f"""# Teams

{team_index}

## All agents ({len(AGENTS)})

| Agent | name | Team | Model |
|---|---|---|---|
{agent_index}
""")

    # --- rules ---
    write(CLAUDE / "rules" / "engineering-standard.md", """---
description: Baseline engineering standard for all work in this repository.
---

# Engineering Standard

- Correctness first, then clarity, then performance. Optimise only what you measured.
- Every change carries: tests for the behaviour, observability for production, and a rollback path.
- Validate at trust boundaries. Never trust client, queue, file, or model output.
- No secrets in code, logs, prompts, or test fixtures.
- Errors are handled explicitly. No empty catch blocks, no swallowed failures.
- Backward compatibility is the default; breaking changes are versioned and announced.
- Documentation ships in the same change as the code it describes.
""")

    write(CLAUDE / "rules" / "agent-authoring.md", """---
description: Rules for adding or editing agents. Applies to .claude/agents/**.
---

# Agent Authoring Rules

Agent files are **generated**. Edit `scripts/agents_data.py`, then run:

```bash
python3 scripts/generate.py
```

Never hand-edit `.claude/agents/*.md` — the next generation overwrites it.

Every agent must keep all ten template sections: Role, Mission, Primary Objective,
Responsibilities, Collaboration, Inputs, Outputs, Decision Rules, Quality Bar, Output Format.

- `name` is kebab-case and matches the filename.
- `description` states when to invoke, not just what the agent is.
- `model`: `opus` for architecture, security, and judgement-heavy roles; `sonnet` otherwise.
- `tools`: least privilege. Reviewers and architects get read-only.
""")

    write(CLAUDE / "rules" / "output-discipline.md", """---
description: How agents report results.
---

# Output Discipline

- Lead with the answer. Context after, only if it changes the decision.
- Every finding: claim, evidence (`file:line`, metric, or source), impact.
- Rank by severity. Never bury a data-loss bug under a naming nit.
- Distinguish verified from inferred.
- No praise, no preamble, no restating the request.
- If you did not do something in scope, say so explicitly.
""")

    write(CLAUDE / "rules" / "security-baseline.md", """---
description: Non-negotiable security rules for all code and infrastructure.
---

# Security Baseline

- **Secrets:** never in code, config committed to git, logs, prompts, test fixtures, or error messages. Use the secret manager. A leaked secret is rotated, not deleted from history and forgotten.
- **Input:** validate at every trust boundary — client, queue, file, third-party API, and model output. Allowlist over denylist.
- **Authorisation:** checked at the resource, not only at the route. Every endpoint gets a negative authorisation test.
- **Injection:** parameterised queries only. No string-built SQL, shell, or template. Model output is data, never instructions.
- **Crypto:** vetted libraries and primitives only. Never hand-rolled. TLS everywhere, including internal traffic.
- **Dependencies:** pinned, scanned, and updated. A known critical vulnerability on a reachable path blocks release.
- **Least privilege:** every credential, role, and token is scoped and time-bound. No standing production admin access.
- **Logging:** log the security-relevant event, never the sensitive payload. No personal data, tokens, or full request bodies.
""")

    write(CLAUDE / "rules" / "testing.md", """---
description: What "tested" means in this repository.
---

# Testing Standard

- Push each test to the **lowest layer** that can still catch the defect.
- Tests assert **behaviour**, not implementation. A refactor must not break them.
- Every test covers the failure path, not only the happy path: invalid input, boundary, timeout, concurrent access.
- **No fixed sleeps.** Wait on an observable condition.
- Each test creates and destroys its own data. No shared mutable state, no order dependence.
- A test failing intermittently is quarantined within a day, then fixed or deleted. Never retried into green.
- Coverage is a diagnostic, never a target. A well-chosen 60 percent beats a padded 95 percent.
- Every fixed defect gains a regression test before the fix merges.
""")

    write(CLAUDE / "rules" / "documentation.md", """---
description: Documentation expectations for every change.
---

# Documentation

- Docs ship in the **same change** as the code they describe. A follow-up ticket is not documentation.
- Every procedure is executed exactly as written before publishing. Untested steps do not ship.
- State prerequisites and the expected result for each task.
- Wrong docs are worse than missing docs. Delete stale content rather than letting it rot.
- Irreversible decisions get an ADR (`.claude/skills/adr`). Never delete an ADR — supersede it.
- Every service has: a README, a runbook per alert, and an owner. No owner, no launch.
""")

    write(CLAUDE / "rules" / "data-privacy.md", """---
description: Handling personal and sensitive data. Applies everywhere data is stored, moved, or logged.
---

# Data & Privacy

- **Minimise.** Collect only what a stated purpose needs. A field with no purpose gets deleted.
- **Classify at ingestion**, never retroactively. Every dataset: owner, classification, grain, contract.
- **Never** copy unmasked production personal data into a lower environment. Masking must be verified irreversible and referentially consistent.
- **Deletion reaches every copy:** primary, replicas, caches, search indexes, logs, analytics, and backups on their cycle.
- **Retention is enforced by the system**, not by a calendar reminder.
- Personal data never enters logs, traces, error reports, prompts, or model training sets without an explicit legal basis.
- Cross-border transfer requires a documented mechanism before the first byte moves.
""")

    # --- commands ---
    commands = {
        "team.md": ("Route a task to the right team and agents.", """---
description: Route a task to the right team and delegate to its agents.
argument-hint: <task description>
---

Task: $ARGUMENTS

1. Read `.claude/teams/README.md` and pick the owning team (name it and justify in one line).
2. Pick the minimum set of agents from that team's roster that can complete the task.
3. Delegate to each with the Agent tool, giving each agent its required Inputs.
4. Merge the results, resolve contradictions explicitly, and report using the standard Output Format.

Do not do the work inline if a specialist agent exists for it.
"""),
        "design.md": ("Run an architecture design pass with ADR output.", """---
description: Architecture design pass ending in an ADR.
argument-hint: <system or change to design>
---

Design target: $ARGUMENTS

1. Delegate to the relevant architects from `.claude/teams/architecture.md`.
2. Require from each: options considered, trade-offs, failure modes, and a recommendation.
3. Reconcile conflicts; the Enterprise Architect breaks ties.
4. Write the decision to `docs/adr/NNNN-<slug>.md` with: Context, Decision, Consequences, Alternatives rejected.
"""),
        "review.md": ("Multi-lens review of the current diff.", """---
description: Review the current diff through correctness, security, and quality lenses.
---

1. Get the diff: `git diff` (and `git diff --staged`).
2. Delegate in parallel to `code-reviewer`, `application-security-engineer`, and the quality agent matching the changed area.
3. Deduplicate findings, rank by severity, and drop anything not backed by a concrete failure scenario.
4. Report file:line findings with fixes. State a merge recommendation.
"""),
        "ship.md": ("Production readiness and release gate.", """---
description: Run the production readiness and release gate before shipping.
---

1. Delegate to `production-readiness-engineer` for the readiness checklist.
2. Delegate to `release-manager` for rollout plan, rollback path, and abort criteria.
3. Delegate to `site-reliability-engineer` for SLO and alerting confirmation.
4. Block on any missing owner, runbook, rollback, or alert. Report go/no-go with the blocking list.
"""),
        "audit.md": ("Security and compliance audit of a scope.", """---
description: Security and compliance audit of a given scope.
argument-hint: <path, service, or feature>
---

Scope: $ARGUMENTS

1. `security-architect` produces or updates the threat model.
2. `application-security-engineer` and `security-test-engineer` verify controls against it.
3. `compliance-engineer` maps findings to control obligations.
4. Report findings with severity, exploitability, evidence, and remediation. No scanner output pasted raw.
"""),
        "flow.md": ("Run a goal through the full delivery pipeline.", """---
description: Take a goal from product discovery through to release, one gated stage at a time.
argument-hint: <goal, in business terms>
---

Goal: $ARGUMENTS

Use the `orchestration` skill. You are the orchestrator — agents cannot call each other,
so every hand-off passes through you.

1. **Size it first.** Decide which stages this actually needs (see the skill's table) and
   say which you are skipping and why. Do not run six stages on a one-line fix.
2. **Run each stage** with the agents the skill names for it. Pass the previous stage's
   output **verbatim** as input, never a paraphrase.
3. **Check the gate** after every stage. State PASSED, FAILED, or SKIPPED with the reason.
   A failed gate sends work backwards — report that, do not hide it.
4. **Stop for the user** when: no measurable success metric exists, a new vendor or system
   is being chosen, or a gate fails twice on the same issue.
5. **Report as you go**, one block per stage, then a final summary table.
"""),
        "incident.md": ("Run an incident response.", """---
description: Drive an active incident from detection to postmortem.
argument-hint: <symptom or alert>
---

Incident: $ARGUMENTS

1. `incident-response-engineer` takes command: establish impact, severity, and timeline.
2. **Mitigate before diagnosing.** If a recent change is implicated, roll back first.
3. Pull in `site-reliability-engineer` for SLO impact and `soc-analyst` if compromise is suspected.
4. Preserve evidence while acting: capture logs, metrics, and state before remediation.
5. After resolution, produce a blameless postmortem via the `postmortem` skill with owned, dated action items.
"""),
        "cost.md": ("Cost review of a scope.", """---
description: Cost review — attribution, waste, unit economics, and scale projection.
argument-hint: <service, account, or design>
---

Scope: $ARGUMENTS

1. `finops-engineer` produces attribution and waste findings with dollar figures.
2. `cloud-cost-architect` models cost at projected scale and reviews the architecture's cost drivers.
3. `capacity-planning-engineer` checks hard limits and headroom before anything is downsized.
4. Report the table: finding, monthly cost, change, saving, risk, effort. No unmeasured savings.
"""),
        "threat-model.md": ("STRIDE threat model for a system.", """---
description: Produce a STRIDE threat model with mitigations and verification.
argument-hint: <system or feature>
---

Target: $ARGUMENTS

Use the `threat-model` skill. `security-architect` leads; `penetration-tester` challenges the
mitigations for realism; `privacy-engineer` covers personal data flows.

Every threat ends in a mitigation with a named verifying test, or a risk acceptance with an owner and expiry.
"""),
        "onboard.md": ("Explain how to use this agent system.", """---
description: Onboard a new user or contributor to this agent system.
---

Use the `onboarding` skill. Adapt depth to what the person asks for: usage, structure, or extension.
Show real commands from this repository, not generic Claude Code documentation.
"""),
        "agents.md": ("List agents matching a domain.", """---
description: Find which agents own a given kind of work.
argument-hint: <domain or task>
---

Query: $ARGUMENTS

Read `.claude/teams/README.md`. Return a short table: Agent, `name`, Team, why it fits.
Rank by fit. Name the single best first choice. If nothing fits, say so and note the roster gap.
"""),
        "runbook.md": ("Write a runbook for an alert or procedure.", """---
description: Write an operational runbook an on-call engineer can execute cold.
argument-hint: <alert name or procedure>
---

Target: $ARGUMENTS

Use the `runbook` skill. `site-reliability-engineer` drafts; `observability-engineer` confirms
every diagnostic signal referenced actually exists.

Walk the procedure once before finishing. Untested runbook does not ship.
"""),
    }
    # One command per team: /team-frontend, /team-design, and so on. Typing the
    # team is faster than describing the work and letting /team guess at it, and
    # the roster arrives inline so no lookup round-trip is needed.
    for key, team in TEAMS.items():
        roster = [a for a in AGENTS if a["team"] == key]
        listing = "\n".join(f"- `{a['slug']}` — {a['title']}: {a['mission']}" for a in roster)
        commands[f"team-{key}.md"] = (
            f"Delegate a task to the {team['title']} ({len(roster)} agents).",
            f"""---
description: Delegate a task to the {team['title']} ({len(roster)} agents).
argument-hint: <task for the {team['title']}>
---

Task: $ARGUMENTS

Team: **{team['title']}** — {team['mission']}

Roster:

{listing}

1. Pick the minimum set of agents above that can complete the task. Name them and
   say in one line why each is needed.
2. Delegate to each with the Agent tool, `subagent_type` = the `slug` in backticks.
   Agents cannot call each other — every hand-off passes through you.
3. For work spanning several agents, run the team's architect or lead first, record
   the decision, then fan out to the implementers.
4. Merge the results, resolve contradictions explicitly, and report using the
   output-discipline rule: claim, evidence (`file:line`), impact, ranked by severity.

Do not do the work inline if a specialist agent above exists for it.
""",
        )

    for fname, (_, body) in commands.items():
        write(CLAUDE / "commands" / fname, body)

    # --- skills ---
    # --- skills ---
    for name, body in SKILLS.items():
        write(CLAUDE / "skills" / name / "SKILL.md", body)

    # --- output styles ---
    write(CLAUDE / "output-styles" / "evidence.md", """---
name: evidence
description: Findings-first output — claim, evidence, impact. No prose padding.
---

Report only in this shape:

- Lead with the conclusion in one sentence.
- Each finding: `path:line` — claim — evidence — impact, ranked by severity.
- Mark every statement as VERIFIED (you read it or measured it) or INFERRED.
- No praise, no preamble, no summary of the request.
- End with the single recommended next action.
""")

    # --- hooks ---
    hook = CLAUDE / "hooks" / "SessionStart.sh"
    write(hook, """#!/usr/bin/env bash
# Loads the agent roster summary into context at session start.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
# Counts only. Everything else this hook used to say is already in CLAUDE.md,
# and paying for it twice in every session is waste.
echo "Roster: $(ls "$ROOT/.claude/agents"/*.md 2>/dev/null | wc -l | tr -d ' ') agents, $(ls "$ROOT/.claude/teams"/*.md 2>/dev/null | grep -vc README || echo 0) teams."
""")
    hook.chmod(0o755)

    # --- settings ---
    write(CLAUDE / "settings.json", json.dumps({
        "$schema": "https://json.schemastore.org/claude-code-settings.json",
        "permissions": {
            "allow": [
                "Read(./**)",
                "Bash(git status:*)", "Bash(git diff:*)", "Bash(git log:*)",
                "Bash(python3 scripts/generate.py)",
                "Bash(ls:*)", "Bash(rg:*)", "Bash(find:*)",
            ],
            "deny": [
                "Read(./.env)", "Read(./.env.*)", "Read(./**/*secret*)",
                "Bash(rm -rf:*)", "Bash(git push --force:*)",
            ],
        },
        "hooks": {
            "SessionStart": [
                {"hooks": [{"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/SessionStart.sh"}]}
            ]
        },
    }, indent=2) + "\n")

    write(ROOT / ".gitignore", """*.local.*
.venv/
.claude/settings.local.json
.env
.env.*
__pycache__/
*.pyc
""")

    write(ROOT / ".mcp.json", json.dumps({"mcpServers": {}}, indent=2) + "\n")

    # --- root CLAUDE.md ---
    team_lines = "\n".join(
        f"- **{t['title']}** (`.claude/teams/{k}.md`) — {t['mission']}" for k, t in TEAMS.items()
    )
    write(ROOT / "CLAUDE.md", f"""# awesome-agents

A production-grade Claude Code control centre: {len(TEAMS)} engineering teams, {len(AGENTS)} specialist agents,
each written to a top 0.1% professional standard.

## Delegate, do not improvise

Before doing domain work yourself, check whether an agent owns it.
Roster and `name` values: `.claude/teams/README.md`.

{team_lines}

Delegation chain: **architect decides, engineer implements, quality verifies, release ships.**
Do not skip a link.

## Generated files

`.claude/agents/*.md` and `.claude/teams/*.md` are generated. Edit `scripts/agents_data.py`
and run `python3 scripts/generate.py`. Hand edits to generated files are lost.

## Standing rules

- `.claude/rules/engineering-standard.md` — baseline for all code.
- `.claude/rules/agent-authoring.md` — how to change agents.
- `.claude/rules/output-discipline.md` — how results are reported.

## Commands

`/team` route work · `/design` architecture pass + ADR · `/review` multi-lens diff review ·
`/ship` readiness gate · `/audit` security audit · `/incident` incident command ·
`/threat-model` STRIDE · `/cost` cost review · `/runbook` on-call runbook ·
`/agents` find the owner · `/onboard` explain this system.

## Plugins

This repo is a Claude Code marketplace: `/plugin marketplace add {OWNER}/{REPO_NAME}`.
For vendor tooling and live data access, use the `marketplace` skill — install, never vendor.

## Output compression

Caveman is always on in this repository — see `AGENTS.md` for the rule other IDE agents load.
Prose is compressed; code, commands, file paths, and error strings are reproduced verbatim.
Drop it for security warnings, irreversible-action confirmations, and anything where a
fragment would be ambiguous, then resume. Commits, PRs, and documentation are written normally.

Install: `/plugin marketplace add juliusbrussee/caveman`, then `/caveman ultra`.

## Non-negotiable

Verified over asserted. Measured over estimated. Reversible over clever.
No secrets in code, logs, or prompts. No change without tests, observability, and a rollback path.
""")

    n_cmd = len(list((CLAUDE / "commands").glob("*.md")))
    n_skill = len(list((CLAUDE / "skills").glob("*/SKILL.md")))
    n_rule = len(list((CLAUDE / "rules").glob("*.md")))
    write(ROOT / "README.md", f"""# awesome-agents

**{len(AGENTS)} specialist Claude Code subagents across {len(TEAMS)} engineering teams — installable as a plugin marketplace.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Agents](https://img.shields.io/badge/agents-{len(AGENTS)}-8A63D2)
![Teams](https://img.shields.io/badge/teams-{len(TEAMS)}-8A63D2)
![Commands](https://img.shields.io/badge/commands-{n_cmd}-8A63D2)
![Skills](https://img.shields.io/badge/skills-{n_skill}-8A63D2)

Most agent collections are a folder of prompts. This one enforces a chain:

> **architect decides → engineer implements → quality verifies → release ships.**

No link is skipped. Every agent is generated from one source of truth, so {len(AGENTS)} roles
stay consistent instead of drifting apart file by file.

## Install

```
/plugin marketplace add {OWNER}/{REPO_NAME}
/plugin install agent-workflow@awesome-agents
/plugin install security-team@awesome-agents
```

Install `agent-workflow` for the commands and skills, then one plugin per team you need.

### Pairs well with

[caveman](https://github.com/juliusbrussee/caveman) — strips filler from model prose while
leaving code, commands, file paths, and error strings byte-identical. {len(AGENTS)} agents with a
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

{" · ".join(t["title"].replace(" Team", "") for t in TEAMS.values())}

Full roster with every agent's `name`, mission, and model: [.claude/teams/README.md](.claude/teams/README.md).

## Layout

```
CLAUDE.md              always loaded — the delegation rule
.claude/
  agents/              {len(AGENTS)} agent definitions        (generated)
  teams/               {len(TEAMS)} charters + roster index    (generated)
  commands/            {n_cmd} slash commands
  skills/              {n_skill} on-demand procedures
  rules/               {n_rule} standing standards
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
{len(AGENTS)} agents consistent. See [CONTRIBUTING.md](CONTRIBUTING.md) and
[.claude/rules/agent-authoring.md](.claude/rules/agent-authoring.md).

## Docs

Site: <https://{OWNER}.github.io/{REPO_NAME}/> — deployed by `.github/workflows/pages.yml`.

## Licence

MIT. See [LICENSE](LICENSE).
""")

    # --- marketplace: this repo is installable via /plugin ---
    build_marketplace()

    write(ROOT / ".github" / "workflows" / "release.yml", """name: Release

on:
  push:
    tags: ['v*']

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Tag must match VERSION
        run: |
          TAG="${GITHUB_REF_NAME#v}"
          FILE="$(cat VERSION)"
          if [ "$TAG" != "$FILE" ]; then
            echo "::error::Tag v$TAG does not match VERSION file ($FILE)."
            exit 1
          fi

      - name: Verify the tagged commit
        run: |
          python3 scripts/generate.py --check
          python3 scripts/validate.py

      - name: Extract release notes from CHANGELOG
        run: |
          awk '/^## \\[/{if(n++)exit} n' CHANGELOG.md | tail -n +2 > NOTES.md
          cat NOTES.md

      - uses: softprops/action-gh-release@v2
        with:
          body_path: NOTES.md
          generate_release_notes: true
""")

    write(ROOT / ".github" / "workflows" / "ci.yml", """name: CI

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Generated files must be committed
        run: python3 scripts/generate.py --check

      - name: Validate
        run: python3 scripts/validate.py
""")

    write(ROOT / "CONTRIBUTING.md", f"""# Contributing

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
""")

    write(ROOT / ".github" / "workflows" / "pages.yml", """name: Deploy docs to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Regenerate site
        run: python3 scripts/generate.py
      - name: Generated files must be committed
        run: python3 scripts/generate.py --check
      - name: Validate
        run: python3 scripts/validate.py
      - uses: actions/upload-pages-artifact@v3
        with:
          path: docs

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
""")

    from site_builder import build
    build(write)

    if not quiet:
        print(f"generated {len(AGENTS)} agents, {len(TEAMS)} teams")


def cli(argv: list[str] | None = None) -> int:
    """Entry point. `--check` reports staleness without writing anything."""
    argv = sys.argv[1:] if argv is None else argv
    if "--check" in argv:
        stale = check()
        if not stale:
            print("generated tree is current")
            return 0
        print(f"STALE — {len(stale)} generated file(s) differ from the source:")
        for path in stale:
            print(f"  {path}")
        return 1
    main()
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(cli())
