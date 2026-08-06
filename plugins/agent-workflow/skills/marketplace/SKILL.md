---
name: marketplace
description: Install external Claude Code plugins from official marketplaces, and install this repository's own agent plugins. Use when the user wants a capability this roster does not cover, asks about plugins or marketplaces, or wants to share these agents with a team.
---

# Marketplaces

Plugins are **installed**, never copied into this repository. A vendored plugin never
receives upstream fixes and silently rots.

## This repository is a marketplace

```
/plugin marketplace add <your-org>/awesome-agents
/plugin install agent-workflow@awesome-agents      # commands + skills
/plugin install security-team@awesome-agents       # one team's agents
```

One plugin per team, plus `agent-workflow` for the shared commands and skills.
`plugins/` and `.claude-plugin/marketplace.json` are **generated** — run `python3 scripts/generate.py`.

## Official Anthropic marketplaces

Claude Code adds `claude-plugins-official` automatically on first interactive start.

```
/plugin marketplace add anthropics/skills
/plugin marketplace add anthropics/claude-plugins-community
/plugin                                            # browse and install
```

## What to install, by gap

These fill gaps this roster deliberately does not cover: vendor-specific tooling and
live data access. **Verify the plugin still exists with `/plugin` before recommending it** —
this table was accurate when written and marketplaces change.

| Need | Plugin | Pairs with |
|---|---|---|
| Cloud build and deploy | `aws-core`, `azure`, `cloudflare` | `platform-engineer`, `cloud-operations-engineer` |
| Observability queries | `datadog`, `grafana-mcp`, `honeycomb`, `newrelic` | `observability-engineer`, `site-reliability-engineer` |
| Database access | `mongodb`, `clickhouse`, `neon`, `cockroachdb`, `duckdb-skills` | `database-engineer`, `database-architect` |
| Security scanning | `claude-security`, `aikido`, `42crunch-api-security-testing` | `application-security-engineer`, `devsecops-engineer` |
| Issue tracking | `linear`, `atlassian`, `github`, `gitlab` | `technical-project-manager`, `product-owner` |
| Design handoff | `figma`, `canva` | `product-designer`, `frontend-engineer` |
| LLM tracing and evals | `langfuse-observability`, `mlflow`, `deepeval` | `ai-evaluation-engineer`, `llmops-engineer` |
| Documentation sites | `mintlify` | `technical-writer` |
| Browser automation | `chrome-devtools-mcp`, `browser-use` | `web-ux-quality-engineer` |
| Feature flags | `growthbook`, `confidence` | `release-manager` |

## The division of labour

**A plugin supplies tools and data access. This roster supplies judgement.**

```
User: "Why did checkout latency spike at 14:00?"

  datadog plugin        → fetches the traces and metrics       (capability)
  site-reliability-eng  → reads them, forms a hypothesis,
                          checks it against the deploy log,
                          states what is verified vs inferred  (judgement)
```

Neither alone is enough. The plugin without the agent returns a wall of metrics.
The agent without the plugin reasons about data it cannot see — which is the failure
mode you most want to avoid.

## Security

Marketplace plugins are **third-party code with tool access** running in your repository.

- Read the source before installing anything that touches production credentials, deploys, or customer data.
- Prefer vendor-official plugins (`datadog`, `mongodb`) over community forks of the same thing.
- A plugin that bundles MCP servers can make network calls you did not initiate. Check what hosts.
- Install at the narrowest scope that works — project over user, when the plugin is project-specific.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Copying a plugin's files into `.claude/` | No updates, no security fixes, silent divergence |
| Installing a plugin because the name matched | Plugins carry tool permissions; read first |
| Installing 20 plugins "to be ready" | Each adds context and tool surface; install on demand |
| Assuming a plugin replaces an agent | It supplies data, not the decision about what the data means |
| Recommending from memory | Marketplaces change. Check `/plugin` first. |

## Done when

- [ ] The gap is named before a plugin is proposed.
- [ ] The plugin's existence was verified with `/plugin`, not recalled.
- [ ] The agent that will use its output is named.
- [ ] Security implications stated for anything touching credentials or production.
- [ ] Nothing was vendored.
