---
name: advanced-techniques
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Expert Techniques

- Align Cloud Run concurrency with servlet/reactive thread model and DB connection pool size.
- Use min instances only on latency-sensitive services, not globally.
- Keep startup path minimal: lazy-init non-critical components and preload only hot code.
- Track cold-start percentile separately from steady-state latency.

## Specialist Playbook

- Maintain per-revision golden signals and compare before traffic promotion.
- Tune concurrency with DB pool and downstream QPS limits, not in isolation.
- Use staged rollout policies tied to latency and error budget checkpoints.
- Keep cold-start and steady-state metrics separated in alerts.

