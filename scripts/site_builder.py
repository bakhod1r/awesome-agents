"""Generates the GitHub Pages site in docs/ from the agent data."""

import html
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from agents_data import AGENTS, TEAMS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

REPO = "awesome-agents"


def _slug() -> str:
    """owner/repo from the git remote, so a fork links to itself, not upstream."""
    try:
        url = subprocess.run(["git", "remote", "get-url", "origin"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.strip()
        m = re.search(r"[:/]([^/]+)/([^/]+?)(?:\.git)?$", url)
        if m:
            return f"{m.group(1)}/{m.group(2)}"
    except Exception:
        pass
    return f"awesome-agents/{REPO}"


SLUG = _slug()
REPO_URL = f"https://github.com/{SLUG}"

CSS = """
:root{--bg:#fbfaf8;--fg:#1c1a17;--muted:#6b655c;--line:#e4e0d8;--card:#fff;--accent:#c8603a;--code:#f2efe9}
@media (prefers-color-scheme:dark){:root{--bg:#16150f;--fg:#eee9e0;--muted:#9a9287;--line:#2e2b24;--card:#1e1c16;--accent:#e08050;--code:#232019}}
:root[data-theme="dark"]{--bg:#16150f;--fg:#eee9e0;--muted:#9a9287;--line:#2e2b24;--card:#1e1c16;--accent:#e08050;--code:#232019}
:root[data-theme="light"]{--bg:#fbfaf8;--fg:#1c1a17;--muted:#6b655c;--line:#e4e0d8;--card:#fff;--accent:#c8603a;--code:#f2efe9}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.65 ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
header{border-bottom:1px solid var(--line);padding:56px 0 40px;background:var(--card)}
h1{font-size:clamp(28px,5vw,44px);margin:0 0 8px;letter-spacing:-.02em}
.sub{color:var(--muted);font-size:18px;margin:0 0 24px;max-width:62ch}
.stats{display:flex;gap:28px;flex-wrap:wrap;margin-top:8px}
.stat b{display:block;font-size:30px;line-height:1.1;color:var(--accent)}
.stat span{color:var(--muted);font-size:13px;text-transform:uppercase;letter-spacing:.06em}
nav.top{display:flex;gap:20px;flex-wrap:wrap;margin-top:28px;font-size:15px}
nav.top a{color:var(--fg);text-decoration:none;border-bottom:2px solid var(--accent);padding-bottom:2px}
section{padding:52px 0;border-bottom:1px solid var(--line)}
h2{font-size:26px;margin:0 0 6px;letter-spacing:-.01em}
h3{font-size:19px;margin:32px 0 10px}
.lede{color:var(--muted);margin:0 0 26px;max-width:70ch}
pre{background:var(--code);border:1px solid var(--line);border-radius:8px;padding:14px 16px;overflow-x:auto;font-size:13.5px;line-height:1.6}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.9em}
:not(pre)>code{background:var(--code);padding:2px 6px;border-radius:4px}
table{width:100%;border-collapse:collapse;font-size:14.5px}
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:8px}
th,td{text-align:left;padding:10px 14px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--code);font-size:12.5px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}
tr:last-child td{border-bottom:none}
#q{width:100%;padding:13px 16px;font-size:16px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg);margin-bottom:14px}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px}
.chip{padding:6px 13px;border:1px solid var(--line);border-radius:99px;background:var(--card);color:var(--muted);font-size:13px;cursor:pointer}
.chip[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:#fff}
.cards{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:15px 17px}
.card h4{margin:0 0 4px;font-size:16px}
.card .name{font-family:ui-monospace,monospace;font-size:12px;color:var(--accent)}
.card p{margin:8px 0 0;font-size:13.5px;color:var(--muted);line-height:1.55}
.card .meta{margin-top:10px;font-size:11.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
.empty{color:var(--muted);padding:24px 0}
footer{padding:40px 0 64px;color:var(--muted);font-size:14px}
footer a{color:var(--accent)}
nav.top a.repo{border-color:var(--muted)}
ol li,ul li{margin-bottom:7px}
"""

JS = """
const AG=%s;
const grid=document.getElementById('grid'),q=document.getElementById('q');
let team='all';
function render(){
  const t=q.value.trim().toLowerCase();
  const out=AG.filter(a=>(team==='all'||a.team===team)&&(!t||(a.title+' '+a.slug+' '+a.mission+' '+a.teamTitle).toLowerCase().includes(t)));
  document.getElementById('count').textContent=out.length;
  grid.textContent='';
  if(!out.length){const e=document.createElement('p');e.className='empty';
    e.textContent='No agent matches. That is a roster gap worth filing.';grid.append(e);return;}
  const frag=document.createDocumentFragment();
  for(const a of out){
    const c=document.createElement('div');c.className='card';
    const h=document.createElement('h4');h.textContent=a.title;
    const n=document.createElement('div');n.className='name';n.textContent=a.slug;
    const p=document.createElement('p');p.textContent=a.mission;
    const m=document.createElement('div');m.className='meta';m.textContent=`${a.teamTitle} · ${a.model}`;
    c.append(h,n,p,m);frag.append(c);
  }
  grid.append(frag);
}
q.addEventListener('input',render);
document.querySelectorAll('.chip').forEach(c=>c.addEventListener('click',()=>{
  team=c.dataset.team;
  document.querySelectorAll('.chip').forEach(x=>x.setAttribute('aria-pressed',x===c));
  render();
}));
render();
"""


def esc(s):
    return html.escape(str(s))


def build(write=None):
    if write is None:
        def write(path, content):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    n_cmd = len(list((ROOT / ".claude" / "commands").glob("*.md")))
    n_skill = len(list((ROOT / ".claude" / "skills").glob("*/SKILL.md")))
    n_rule = len(list((ROOT / ".claude" / "rules").glob("*.md")))
    n_plugin = len(json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())["plugins"])
    payload = [
        {"title": a["title"], "slug": a["slug"], "mission": a["mission"],
         "team": a["team"], "teamTitle": TEAMS[a["team"]]["title"], "model": a["model"]}
        for a in sorted(AGENTS, key=lambda x: x["title"])
    ]

    chips = '<button class="chip" data-team="all" aria-pressed="true">All</button>' + "".join(
        f'<button class="chip" data-team="{k}" aria-pressed="false">{esc(t["title"].replace(" Team",""))}</button>'
        for k, t in TEAMS.items()
    )

    team_rows = "".join(
        f"<tr><td><b>{esc(t['title'])}</b></td><td>{len([a for a in AGENTS if a['team']==k])}</td><td>{esc(t['mission'])}</td></tr>"
        for k, t in TEAMS.items()
    )

    page = f"""<title>{REPO} — {len(AGENTS)} Claude Code agents</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{len(AGENTS)} specialist Claude Code subagents across {len(TEAMS)} engineering teams. Architecture to build to verify to ship, with the delegation chain enforced.">
<style>{CSS}</style>

<header><div class="wrap">
  <h1>{REPO}</h1>
  <p class="sub">{len(TEAMS)} engineering teams. {len(AGENTS)} specialist Claude Code subagents.
  One source of truth, generated. Every agent written to a top 0.1% professional standard —
  evidence over assertion, measurement over estimate.</p>
  <div class="stats">
    <div class="stat"><b>{len(AGENTS)}</b><span>Agents</span></div>
    <div class="stat"><b>{len(TEAMS)}</b><span>Teams</span></div>
    <div class="stat"><b>{n_cmd}</b><span>Commands</span></div>
    <div class="stat"><b>{n_skill}</b><span>Skills</span></div>
    <div class="stat"><b>{n_rule}</b><span>Rules</span></div>
    <div class="stat"><b>{n_plugin}</b><span>Plugins</span></div>
  </div>
  <nav class="top">
    <a href="#start">Quick start</a><a href="#roster">Roster</a><a href="#tutorial">Tutorial</a>
    <a href="#install">Install</a><a href="#extend">Extend</a><a href="#structure">Structure</a>
    <a href="{REPO_URL}" class="repo">GitHub ↗</a>
  </nav>
</div></header>

<section id="start"><div class="wrap">
  <h2>Quick start</h2>
  <p class="lede">Three commands. No configuration, no dependencies beyond Python 3.</p>
<pre><code>git clone {REPO_URL}.git
cd {REPO}
python3 scripts/generate.py   # regenerates .claude/ from scripts/agents_data.py</code></pre>
  <p class="lede">Open the folder in Claude Code and ask normally. <code>CLAUDE.md</code> loads automatically,
  Claude reads the roster and delegates to the right specialist. To force one:</p>
<pre><code>Use the database-architect agent to review this schema.</code></pre>
</div></section>

<section id="roster"><div class="wrap">
  <h2>Roster</h2>
  <p class="lede">Search by title, domain, or mission. Showing <b id="count">{len(AGENTS)}</b> agents.</p>
  <input id="q" type="search" placeholder="Search: kubernetes, privacy, migration, cost, drift…" aria-label="Search agents">
  <div class="chips">{chips}</div>
  <div class="cards" id="grid"></div>

  <h3>Teams</h3>
  <div class="scroll"><table>
    <thead><tr><th>Team</th><th>Agents</th><th>Mission</th></tr></thead>
    <tbody>{team_rows}</tbody>
  </table></div>
</div></section>

<section id="tutorial"><div class="wrap">
  <h2>Tutorial</h2>

  <h3>1. The delegation chain</h3>
  <p class="lede"><b>Architect decides. Engineer implements. Quality verifies. Release ships.</b>
  Never skip a link. Implementation with no design decision produces rework; a release with no
  verification produces an incident.</p>

  <h3>2. Commands</h3>
  <div class="scroll"><table>
  <thead><tr><th>Command</th><th>What it does</th><th>Agents it pulls</th></tr></thead><tbody>
  <tr><td><code>/team &lt;task&gt;</code></td><td>Routes any task to the owning team and delegates</td><td>picked per task</td></tr>
  <tr><td><code>/design &lt;system&gt;</code></td><td>Architecture pass ending in a written ADR</td><td>architects</td></tr>
  <tr><td><code>/review</code></td><td>Multi-lens review of the current diff</td><td>code-reviewer, appsec, domain QA</td></tr>
  <tr><td><code>/ship</code></td><td>Production readiness gate — blocks on missing owner, runbook, rollback</td><td>readiness, release, SRE</td></tr>
  <tr><td><code>/audit &lt;scope&gt;</code></td><td>Security and compliance audit</td><td>security architect, appsec, sec-test, compliance</td></tr>
  <tr><td><code>/incident &lt;symptom&gt;</code></td><td>Incident command, mitigate first, postmortem after</td><td>incident response, SRE, SOC</td></tr>
  <tr><td><code>/threat-model &lt;system&gt;</code></td><td>STRIDE model with mitigations and verifying tests</td><td>security architect, pentester, privacy</td></tr>
  <tr><td><code>/cost &lt;scope&gt;</code></td><td>Attribution, waste, unit economics, scale projection</td><td>FinOps, cost architect, capacity</td></tr>
  <tr><td><code>/runbook &lt;alert&gt;</code></td><td>Runbook an on-call engineer can execute cold</td><td>SRE, observability</td></tr>
  <tr><td><code>/agents &lt;domain&gt;</code></td><td>Finds which agents own a kind of work</td><td>—</td></tr>
  <tr><td><code>/onboard</code></td><td>Explains the system to a newcomer</td><td>—</td></tr>
  </tbody></table></div>

  <h3>3. Worked example</h3>
  <p class="lede">Shipping a payments retry mechanism, end to end:</p>
<pre><code>/design payment retry with idempotency keys
  → backend-architect + integration-architect produce options and failure modes
  → decision written to docs/adr/0007-payment-retry.md

/team implement the retry design
  → backend-developer implements; database-engineer adds the idempotency table

/review
  → code-reviewer, application-security-engineer, api-quality-engineer
  → findings ranked by severity, each with a concrete failure scenario

/ship
  → production-readiness-engineer blocks until the runbook and rollback exist
  → release-manager defines canary gates and abort criteria</code></pre>

  <h3>4. What every agent guarantees</h3>
  <p class="lede">All {len(AGENTS)} agents carry the same ten sections — Role, Mission, Primary Objective,
  Responsibilities, Collaboration, Inputs, Outputs, Decision Rules, Quality Bar, Output Format — plus a
  shared operating standard:</p>
  <ul>
    <li>Read the actual code, data, or telemetry before concluding. Never answer from memory about system state.</li>
    <li>Label what was <b>verified</b> versus <b>inferred</b>.</li>
    <li>Quantify. "Slow" is not a finding; "p99 480 ms against a 200 ms budget" is.</li>
    <li>Deliver the whole scope. If part is blocked, finish the rest and name what was left out.</li>
    <li>Escalate with a proposed decision, never a bare problem.</li>
  </ul>

  <h3>5. Standing rules</h3>
  <p class="lede">Applied to all work without being asked: engineering standard, security baseline,
  testing, documentation, data &amp; privacy, agent authoring, output discipline.</p>
</div></section>

<section id="install"><div class="wrap">
  <h2>Install as a plugin</h2>
  <p class="lede">This repository is also a Claude Code plugin marketplace — {n_plugin} plugins,
  one per team plus the shared workflow. Install only the teams you need.</p>
<pre><code>/plugin marketplace add {SLUG}
/plugin install agent-workflow@awesome-agents     # commands + skills
/plugin install security-team@awesome-agents      # that team's agents
/plugin install backend-team@awesome-agents</code></pre>
  <p class="lede">Pair with official marketplaces for vendor tooling and live data access.
  Plugins supply <b>tools</b>; this roster supplies <b>judgement</b>.</p>
<pre><code>/plugin marketplace add anthropics/skills
/plugin marketplace add anthropics/claude-plugins-community</code></pre>
  <div class="scroll"><table>
  <thead><tr><th>Need</th><th>Install</th><th>Pairs with</th></tr></thead><tbody>
  <tr><td>Observability queries</td><td><code>datadog</code>, <code>grafana-mcp</code>, <code>honeycomb</code></td><td>observability-engineer, SRE</td></tr>
  <tr><td>Database access</td><td><code>mongodb</code>, <code>clickhouse</code>, <code>neon</code></td><td>database-engineer</td></tr>
  <tr><td>Security scanning</td><td><code>claude-security</code>, <code>aikido</code></td><td>application-security-engineer</td></tr>
  <tr><td>LLM tracing &amp; evals</td><td><code>langfuse-observability</code>, <code>mlflow</code>, <code>deepeval</code></td><td>ai-evaluation-engineer, llmops-engineer</td></tr>
  <tr><td>Issue tracking</td><td><code>linear</code>, <code>atlassian</code>, <code>github</code></td><td>technical-project-manager</td></tr>
  <tr><td>Design handoff</td><td><code>figma</code></td><td>product-designer</td></tr>
  </tbody></table></div>
  <p class="lede"><b>Install, never vendor.</b> A copied plugin never receives upstream fixes.
  Marketplace plugins are third-party code with tool access — read the source before installing
  anything that touches production credentials.</p>
</div></section>

<section id="extend"><div class="wrap">
  <h2>Extend</h2>
  <p class="lede">Agent and team files are <b>generated</b>. Edit the data, never the output.</p>
<pre><code># scripts/agents_data.py
dict(
    slug="graph-database-engineer", title="Graph Database Engineer", team="backend",
    model="sonnet", tools=FULL,
    mission="Design and operate graph stores for traversal-heavy workloads.",
    focus=[...],      # 5 responsibilities
    inputs=[...], outputs=[...],
    rules=[...],      # decision rules that would survive a design review
    bar=[...],        # what "done well" means, measurably
)</code></pre>
<pre><code>python3 scripts/generate.py   # rewrites .claude/agents/, .claude/teams/, docs/</code></pre>
  <p class="lede">Hand edits to <code>.claude/agents/*.md</code> are lost on the next run. That is deliberate —
  one source of truth means {len(AGENTS)} agents stay consistent.</p>
  <h3>Writing a good agent</h3>
  <ul>
    <li><b>Decision rules must be opinionated.</b> "Index to the query, not to the column" is a rule.
        "Follow best practices" is noise.</li>
    <li><b>Quality bar must be checkable.</b> "Restore drill passing within RTO", not "high quality".</li>
    <li><b>Least privilege on tools.</b> Architects and reviewers get read-only.</li>
    <li><b>Model choice:</b> <code>opus</code> for architecture, security, and judgement-heavy roles;
        <code>sonnet</code> otherwise.</li>
  </ul>
</div></section>

<section id="structure"><div class="wrap">
  <h2>Structure</h2>
<pre><code>CLAUDE.md              always loaded — the delegation rule
.mcp.json              MCP servers (must sit at repo root)
.claude/
  agents/              {len(AGENTS)} agent definitions          (generated)
  teams/               {len(TEAMS)} charters + roster index      (generated)
  commands/            {n_cmd} slash commands
  skills/              {n_skill} on-demand procedures
  rules/               {n_rule} standing standards
  hooks/               SessionStart.sh — loads the roster
  output-styles/       evidence.md
  settings.json        permissions + hook registry
scripts/
  agents_data.py       <b>edit this</b>
  agents_data_ext.py   second wave of teams
  generate.py          <b>then run this</b>
  site_builder.py      builds this page
docs/                  GitHub Pages site        (generated)</code></pre>
</div></section>

<footer><div class="wrap">
  <a href="{REPO_URL}">{SLUG}</a> · MIT licensed ·
  generated by <code>python3 scripts/generate.py</code>.<br>
  Verified over asserted. Measured over estimated. Reversible over clever.
</div></footer>

<script>{JS % json.dumps(payload).replace('</', '<\\/')}</script>
"""
    write(DOCS / "index.html", page)
    write(DOCS / ".nojekyll", "")


if __name__ == "__main__":  # pragma: no cover
    build()
