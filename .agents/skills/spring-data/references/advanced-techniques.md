---
name: advanced-techniques
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Expert Techniques

- Use projection interfaces for read-heavy endpoints to avoid entity hydration overhead.
- Prefer explicit fetch graphs per use case over global eager mapping.
- Pair pagination with deterministic sorting and covering indexes.
- Use outbox tables to decouple transaction commit from event publication.

## Specialist Playbook

- Define measurable SLOs per critical path and map each technique to a target metric.
- Keep rollback strategies documented before applying high-risk optimizations.
- Run game days to validate failure-path assumptions under realistic load.
- Standardize diagnostics (logs, metrics, traces) before deep tuning.

