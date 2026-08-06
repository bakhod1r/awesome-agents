---
name: cost-review
description: Review a design or a running system for cost. Use before committing to an architecture, when a bill jumps, or during quarterly optimisation.
---

# Cost Review

## Procedure

1. **Attribute.** Break spend by team, service, and environment. Untagged spend is
   finding number one — you cannot optimise what you cannot attribute.
2. **Find the drivers.** Rank by absolute spend, then look for the usual suspects:

   | Driver | Typical cause |
   |---|---|
   | Cross-zone / egress traffic | Chatty services split across zones; no locality awareness |
   | Storage class | Everything on hot storage forever; no lifecycle policy |
   | Idle capacity | Non-production running nights and weekends |
   | Over-provisioning | Sized for a peak that never arrived, never revisited |
   | Managed service premium | Paying for an operator you do not need at this scale |
   | Log and metric volume | Debug logging left on; high-cardinality labels |
   | LLM tokens | No caching, oversized model for the task, unbounded context |

3. **Compute unit economics.** Cost per request, per tenant, per model call. Totals hide
   everything — a bill that doubled while traffic tripled is a *win*.
4. **Model at scale.** What does this cost at 10x? A design that is cheap today and
   ruinous at scale is rejected now, while changing it is still cheap.
5. **Recommend with numbers.** Each item: measured monthly saving, effort, and the
   performance or reliability risk it introduces.

## Output

| Finding | Monthly cost | Proposed change | Saving | Risk | Effort |

## Worked example

**Weak — unactionable, and quietly dangerous:**

```
- NAT Gateway costs are high, consider reducing traffic.
- Instances look oversized, recommend downsizing.
- Consider reserved instances for savings.
```

Nobody can act on these, and "downsize" with no risk statement is how a cost review
causes an outage.

**Strong:**

| Finding | Monthly | Change | Saving | Risk | Effort |
|---|---|---|---|---|---|
| NAT Gateway data processing: 41 TB/mo. 78% is S3 traffic routed through NAT. | $4,920 | Add S3 Gateway VPC endpoint | **$3,840** (verified: gateway endpoints are free, traffic bypasses NAT) | None. Route table change, reversible in minutes. | 1h |
| 14 non-prod RDS instances running 24/7 | $6,200 | Stop 19:00–07:00 and weekends via scheduler | **$4,100** (66% of hours) | Overnight CI jobs on 2 of the 14 — exclude those. | 4h |
| `api` service: p99 CPU 12%, sized `m5.4xlarge` × 9 | $3,740 | → `m5.xlarge` × 9, keep replica count | **$2,800** | **Real.** 4x less burst headroom. Verified against the last Black Friday peak: 34% CPU at 4.1x normal traffic. Still 3x headroom after the change. Requires a load test before rollout. | 1d + load test |
| CloudWatch: 2.1 TB logs/mo, 61% is `DEBUG` from one service | $1,480 | Set that service to `INFO`; 7-day retention on debug streams | **$900** | Lose debug detail on that service; it has tracing, so diagnosis is unaffected. | 2h |
| **Total** | | | **$11,640/mo** | | |

Every row: a number, a mechanism, an honest risk. The third row is the important one —
it is the biggest behavioural change and it names the load test as a precondition
instead of pretending the risk is zero.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Recommendation with no measured saving | Unprioritisable. The 5% item gets done, the 40% item does not. |
| Trading reliability for cost silently | The outage costs more than the year of savings |
| Optimising the total instead of the unit cost | Punishes growth; rewards shrinking the business |
| Reserved commitments without utilisation data | Locks in today's mistake for one to three years |
| Findings sent to finance | Finance cannot change a route table. Send to the owning team. |
| Savings never verified | Half of claimed savings do not appear on the next bill |

## Rules

- No recommendation without a measured saving. Estimates are labelled as estimates.
- Never trade away a reliability guarantee without saying so explicitly and loudly.
- Verify in the following billing period. Unverified savings do not count.
- Route findings to the team that can act, not to finance.
- Check for a hard limit before downsizing anything — quotas, connection pools, licences.

## Done when

- [ ] Attribution coverage stated; untagged spend quantified.
- [ ] Findings ranked by absolute saving, not by ease.
- [ ] Every row has a saving, a risk, and an effort estimate.
- [ ] Unit economics reported alongside totals.
- [ ] Cost at 10x scale modelled for design reviews.
- [ ] A verification date is set for the following billing period.
