---
name: gcp-cloud-tasks
description: |
  Guides Cloud Tasks queue architecture, retry policy design, idempotent handlers, and secure HTTP dispatch workflows.
  Use when: orchestrating deferred work, background jobs, and resilient task execution in GCP microservices.
---

# GCP Cloud Tasks

This skill supports professional execution in: queue design, retry/backoff strategy, task routing, and operational safeguards.
Use it to keep architecture decisions explicit, implementation consistent, and operations reliable.

## How to define architecture and boundaries

- Establish explicit contracts for core interfaces, data flows, and ownership.
- Keep domain behavior separate from infrastructure details and framework glue.
- Define compatibility policy before introducing schema or contract changes.
- Document tradeoffs and decisions in architecture records.

## How to implement with Java and Kotlin

- Prefer constructor injection and explicit DTOs in service boundaries.
- Enforce nullability and serialization consistency between Java and Kotlin modules.
- Keep cross-module interfaces small, typed, and version-aware.
- Add contract tests for external integrations and critical internal boundaries.

## How to operate and harden in production

- Define SLOs and alert thresholds tied to user-facing outcomes.
- Implement staged rollout and rollback strategy for every critical change.
- Track dependency saturation, retries, and failure amplification indicators.
- Keep runbooks updated with tested mitigation steps.

## How to use extended references

- Read [Version History](references/version-history.md) before upgrades, migrations, or compatibility decisions.
- Read [Java and Kotlin Examples](references/java-kotlin-examples.md) for implementation-ready snippets and language-specific guidance.
- Read [Advanced Techniques](references/advanced-techniques.md) for specialist playbooks, incident tactics, and performance patterns.

## Common Warnings & Pitfalls

- Architecture decisions are implicit and undocumented, causing long-term drift.
- Operational controls are added late, increasing incident recovery time.
- Compatibility strategy is missing for evolving integrations and schemas.
- Quality gates are inconsistent across environments and release stages.

## Common Errors and Fixes

| Symptom | Root Cause | Fix |
|---|---|---|
| Production regression after deployment | Configuration or contract drift across environments | Add compatibility checks, staged rollout, and rollback criteria. |
| Latency spikes under load | Missing timeout and backpressure policies | Define budgets, tune pools, and monitor saturation indicators. |
| Integration failures after change | Versioning and contract tests not enforced | Apply contract governance and CI compatibility gates. |

## Keywords

- queue and task
- idempotency key
- retry config
- dead-letter
- rate limits

## References

- [Official Documentation](https://cloud.google.com/tasks/docs)
- [Official Documentation](https://cloud.google.com/tasks/docs/creating-http-target-tasks)
- [Official Documentation](https://cloud.google.com/tasks/docs/configuring-queues)
