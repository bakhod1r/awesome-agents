#!/usr/bin/env python3
"""Validate the generated control centre. Run in CI; exits non-zero on any failure.

    python3 scripts/validate.py
"""

import json
import re
import sys
from pathlib import Path


def load_json(path: Path):
    """Parse JSON, or return None. A malformed file is reported once, not crashed on."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

sys.path.insert(0, str(Path(__file__).parent))
from agents_data import AGENTS, TEAMS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CLAUDE = ROOT / ".claude"

SECTIONS = [
    "## Role", "## Mission", "## Primary Objective", "## Responsibilities",
    "## Collaboration", "## Inputs", "## Outputs", "## Decision Rules",
    "## Quality Bar", "## Output Format",
]

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def check_data() -> set[str]:
    """The source of truth must be well formed before anything is generated from it."""
    slugs: set[str] = set()
    for a in AGENTS:
        s = a["slug"]
        if s in slugs:
            err(f"data: duplicate slug {s!r}")
        slugs.add(s)
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", s):
            err(f"data: slug {s!r} is not kebab-case")
        if a["team"] not in TEAMS:
            err(f"data: {s} references unknown team {a['team']!r}")
        if a["model"] not in ("opus", "sonnet", "haiku"):
            err(f"data: {s} has unknown model {a['model']!r}")
        for field, minimum in (("focus", 3), ("inputs", 2), ("outputs", 2), ("rules", 2), ("bar", 2)):
            if len(a[field]) < minimum:
                err(f"data: {s}.{field} has {len(a[field])} items, minimum {minimum}")
        if not a["mission"].endswith("."):
            err(f"data: {s}.mission must end with a full stop")
        # a mission that fits in a description line keeps the roster scannable
        if len(a["mission"]) > 160:
            err(f"data: {s}.mission is {len(a['mission'])} chars, max 160")
    for key, t in TEAMS.items():
        if not any(a["team"] == key for a in AGENTS):
            err(f"data: team {key!r} has no agents")
        for field in ("title", "mission", "charter"):
            if not t.get(field):
                err(f"data: team {key!r} missing {field}")
    return slugs


def check_agents(slugs: set[str]) -> None:
    files = list((CLAUDE / "agents").glob("*.md"))
    if len(files) != len(AGENTS):
        err(f"agents: {len(files)} files but {len(AGENTS)} records — run generate.py")
    for f in files:
        t = f.read_text(encoding="utf-8")
        m = re.match(r"---\nname: (\S+)\ndescription: (.+)\nmodel: (\S+)\ntools: (.+)\n---\n", t)
        if not m:
            err(f"{f.name}: malformed frontmatter")
            continue
        if m.group(1) != f.stem:
            err(f"{f.name}: name {m.group(1)!r} != filename")
        if len(m.group(2)) > 400:
            err(f"{f.name}: description too long ({len(m.group(2))} chars)")
        for s in SECTIONS:
            if s not in t:
                err(f"{f.name}: missing section {s}")
        if "top 0.1%" not in t:
            err(f"{f.name}: missing the global standard block")


def check_skills() -> None:
    for f in sorted((CLAUDE / "skills").glob("*/SKILL.md")):
        t = f.read_text(encoding="utf-8")
        m = re.match(r"---\nname: (\S+)\ndescription: (.+)\n---\n", t, re.DOTALL)
        if not m:
            err(f"skills/{f.parent.name}: malformed frontmatter")
            continue
        if m.group(1) != f.parent.name:
            err(f"skills/{f.parent.name}: name {m.group(1)!r} != directory")
        for section in ("## Done when",):
            if section not in t:
                err(f"skills/{f.parent.name}: missing {section}")
        if "- [ ]" not in t:
            err(f"skills/{f.parent.name}: 'Done when' has no checklist items")


def check_json_and_plugins() -> None:
    for rel in [".claude/settings.json", ".claude-plugin/marketplace.json", ".mcp.json"]:
        p = ROOT / rel
        if not p.exists():
            err(f"{rel}: missing")
            continue
        if load_json(p) is None:
            err(f"{rel}: invalid JSON")

    mk = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    if mk is None:
        return
    for required in ("name", "owner", "plugins"):
        if required not in mk:
            err(f"marketplace.json: missing required key {required!r}")
    seen = set()
    for p in mk.get("plugins", []):
        if p["name"] in seen:
            err(f"marketplace.json: duplicate plugin {p['name']!r}")
        seen.add(p["name"])
        manifest = ROOT / p["source"] / ".claude-plugin" / "plugin.json"
        if not manifest.exists():
            err(f"marketplace.json: {p['name']} source has no plugin.json")
            continue
        pj = load_json(manifest)
        if pj is None:
            err(f"{p['name']}: plugin.json is not valid JSON")
            continue
        if pj["name"] != p["name"]:
            err(f"{p['name']}: plugin.json name {pj['name']!r} != marketplace entry")


def check_references(slugs: set[str]) -> None:
    """Every agent name mentioned in prose must exist, or delegation silently fails."""
    suffixes = ("-engineer", "-architect", "-analyst", "-tester", "-manager", "-developer", "-designer", "-reviewer")
    sources = list((CLAUDE / "commands").glob("*.md")) + list((CLAUDE / "skills").glob("*/SKILL.md"))
    for f in sources:
        for ref in set(re.findall(r"`([a-z][a-z0-9-]{4,})`", f.read_text(encoding="utf-8"))):
            if ref.endswith(suffixes) and ref not in slugs:
                err(f"{f.parent.name}/{f.name}: references nonexistent agent {ref!r}")

    for f in (CLAUDE / "teams").glob("*.md"):
        for link in re.findall(r"\]\(\.\./agents/([a-z0-9-]+\.md)\)", f.read_text(encoding="utf-8")):
            if not (CLAUDE / "agents" / link).exists():
                err(f"teams/{f.name}: broken link to {link}")


def check_site() -> None:
    p = ROOT / "docs" / "index.html"
    if not p.exists():
        err("docs/index.html: missing")
        return
    html = p.read_text(encoding="utf-8")
    # A strict CSP or an offline reader must not need the network.
    for pattern, label in [
        (r'src="https?://', "external script or image"),
        (r'<link[^>]+href="https?://', "external stylesheet"),
        (r"fetch\(|XMLHttpRequest|WebSocket", "network call"),
    ]:
        if re.search(pattern, html):
            err(f"docs/index.html: contains {label}")
    if not (ROOT / "docs" / ".nojekyll").exists():
        err("docs/.nojekyll: missing — GitHub Pages will run Jekyll and may drop files")
    if html.count('"slug"') != len(AGENTS):
        err(f"docs/index.html: embeds {html.count(chr(34) + 'slug' + chr(34))} agents, expected {len(AGENTS)}")
    # A mission containing this sequence would terminate the script block early.
    if "</script>" in html.split("<script>")[-1].rsplit("</script>", 1)[0]:
        err("docs/index.html: script payload contains an unescaped </script>")


def check_permissions() -> None:
    """A permission allowlist shipped to other people must not grant broad host access."""
    settings = load_json(ROOT / ".claude" / "settings.json")
    if settings is None:
        return  # absence and malformation are already reported by check_json_and_plugins
    allow = settings.get("permissions", {}).get("allow", [])
    for rule in allow:
        # Project-relative rules are fine; absolute and home-anchored ones are not.
        if re.search(r"\((//|/|~/|\.\./)", rule):
            err(f"settings.json: allow rule {rule!r} reaches outside the project")


def main() -> int:
    slugs = check_data()
    check_agents(slugs)
    check_skills()
    check_json_and_plugins()
    check_references(slugs)
    check_site()
    check_permissions()

    if errors:
        print(f"FAILED — {len(errors)} problem(s):\n")
        for e in errors:
            print(f"  {e}")
        return 1

    n_cmd = len(list((CLAUDE / "commands").glob("*.md")))
    n_skill = len(list((CLAUDE / "skills").glob("*/SKILL.md")))
    n_rule = len(list((CLAUDE / "rules").glob("*.md")))
    print(f"OK — {len(AGENTS)} agents, {len(TEAMS)} teams, "
          f"{n_cmd} commands, {n_skill} skills, {n_rule} rules")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
