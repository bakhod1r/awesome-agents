---
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
