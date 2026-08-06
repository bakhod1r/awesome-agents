---
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
