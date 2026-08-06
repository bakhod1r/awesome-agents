#!/usr/bin/env bash
# Loads the agent roster summary into context at session start.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
# Counts only. Everything else this hook used to say is already in CLAUDE.md,
# and paying for it twice in every session is waste.
echo "Roster: $(ls "$ROOT/.claude/agents"/*.md 2>/dev/null | wc -l | tr -d ' ') agents, $(ls "$ROOT/.claude/teams"/*.md 2>/dev/null | grep -vc README || echo 0) teams."
