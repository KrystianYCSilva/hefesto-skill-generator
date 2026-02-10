---
name: advanced-techniques
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Expert Techniques

- Combine HPA with PodDisruptionBudget and topology spread constraints for resilient scaling.
- Calibrate liveness probes conservatively to avoid restart storms under transient downstream failures.
- Use Workload Identity per namespace/domain, not one shared platform identity.
- Keep progressive delivery (canary/blue-green) integrated with SLO-based promotion checks.

## Specialist Playbook

- Define measurable SLOs per critical path and map each technique to a target metric.
- Keep rollback strategies documented before applying high-risk optimizations.
- Run game days to validate failure-path assumptions under realistic load.
- Standardize diagnostics (logs, metrics, traces) before deep tuning.

