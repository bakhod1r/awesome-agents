---
name: runbook
description: Write an operational runbook that an on-call engineer can execute at 3am. Use when adding an alert, launching a service, or after an incident exposed a missing procedure.
---

# Runbook

A runbook is executable by a tired stranger with no context. If it needs the author
present, it is not a runbook — it is notes.

## Template

```markdown
# Runbook: <alert or procedure name>

## What this means
<The user-visible symptom in one sentence. Not the metric — the symptom.>

## Severity and impact
<Who is affected, how badly, how fast it escalates if ignored.>

## Diagnosis
1. <exact query, dashboard link, or command — copy-pasteable>
   - <output A> → cause 1, go to Mitigation row 1
   - <output B> → cause 2, go to Mitigation row 2

## Mitigation
| Symptom | Action | Command | Risk |

## Escalation
<Who, by which channel, after how long, and what to tell them.>

## Rollback
<Exact steps, and how to confirm it worked.>

## Related
<Dashboards, ADRs, past incidents.>
```

## Worked example

Two versions of one diagnosis step:

**Useless at 3am:**

```markdown
## Diagnosis
1. Check if the database is healthy.
2. Look at the connection pool.
3. Restart the service if needed.
```

Every line raises a question the on-call engineer cannot answer alone. *Which* database?
Healthy by what measure? Restart how, and what breaks when they do?

**Executable at 3am:**

```markdown
## Diagnosis
1. Is the pool saturated?
   ```
   kubectl exec -n prod deploy/api -- \
     psql $DB_URL -c "select count(*), state from pg_stat_activity group by state"
   ```
   - `active` ≥ 95 (pool max is 100) → **saturated**, go to Mitigation row 1
   - `idle in transaction` ≥ 20 → **leaked transactions**, go to Mitigation row 2
   - Both under those numbers → not the pool. Check upstream: <dashboard link>

## Mitigation
| Symptom | Action | Command | Risk |
|---|---|---|---|
| Saturated | Raise pool ceiling to 150 | `kubectl set env deploy/api DB_POOL_MAX=150` | DB max_connections is 200; three replicas at 150 will exceed it. Scale replicas to 1 first, or raise the DB limit. |
| Leaked transactions | Terminate idle-in-transaction over 5 min | `psql $DB_URL -f ops/kill-idle-txn.sql` | **Rolls back in-flight work.** Users may see failed requests. Safe for reads, not during the nightly batch (02:00–04:00 UTC). |
```

The second version tells the engineer exactly what to run, what the output means,
and — critically — **what they are about to break**.

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| "Restart the service" | Give the command, and say what restarting drops |
| Actions with no stated risk | On-call needs to know the blast radius before pressing enter |
| Diagnosis using a metric nobody emits | Fix the instrumentation instead; then write the step |
| Links to a dashboard that requires tribal knowledge to read | State what number is bad |
| No escalation timeout | People burn an hour rather than wake someone. Give the deadline. |
| Never walked through | Untested runbook = no runbook |

## Done when

- [ ] Every command is copy-pasteable and was actually run.
- [ ] Every diagnostic step says what each possible output means.
- [ ] Every action states its risk and blast radius.
- [ ] Escalation has a named target and a time limit.
- [ ] Rollback includes how to confirm it worked.
- [ ] Someone other than the author walked it end to end.
