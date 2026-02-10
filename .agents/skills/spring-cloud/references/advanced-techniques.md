---
name: advanced-techniques
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Expert Techniques

- Apply timeout budget decomposition per call chain hop, not one global timeout.
- Keep service discovery optional in local dev to reduce cognitive/operational overhead.
- Centralize gateway policies and verify with integration policy tests.
- Track retry amplification factor to avoid cascading failure under incidents.

## Specialist Playbook

- Define measurable SLOs per critical path and map each technique to a target metric.
- Keep rollback strategies documented before applying high-risk optimizations.
- Run game days to validate failure-path assumptions under realistic load.
- Standardize diagnostics (logs, metrics, traces) before deep tuning.

