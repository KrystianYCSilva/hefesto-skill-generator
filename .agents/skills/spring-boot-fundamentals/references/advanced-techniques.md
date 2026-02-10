---
name: advanced-techniques
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Expert Techniques

- Capture and diff `ConditionEvaluationReport` between `dev` and `prod` to explain startup divergence.
- Use layered jars/buildpacks to improve image cache reuse and deployment speed.
- Build startup failure taxonomy with custom `FailureAnalyzer` for platform teams.
- Define a strict internal starter catalog to avoid dependency drift across services.

## Specialist Playbook

- Define measurable SLOs per critical path and map each technique to a target metric.
- Keep rollback strategies documented before applying high-risk optimizations.
- Run game days to validate failure-path assumptions under realistic load.
- Standardize diagnostics (logs, metrics, traces) before deep tuning.

