---
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
