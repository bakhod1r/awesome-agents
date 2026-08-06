---
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
