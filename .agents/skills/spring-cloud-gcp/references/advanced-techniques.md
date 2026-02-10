---
name: advanced-techniques
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Expert Techniques

- Use emulator-first test profiles for Pub/Sub and storage-driven workflows.
- Add idempotency keys for message handlers before enabling aggressive retries.
- Debug ADC chain explicitly (metadata server vs local credentials) during incident triage.
- Separate control-plane credentials from data-plane runtime identities.

## Specialist Playbook

- Define measurable SLOs per critical path and map each technique to a target metric.
- Keep rollback strategies documented before applying high-risk optimizations.
- Run game days to validate failure-path assumptions under realistic load.
- Standardize diagnostics (logs, metrics, traces) before deep tuning.

