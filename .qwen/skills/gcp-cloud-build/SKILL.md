---
name: gcp-cloud-build
description: |
  Guides Cloud Build pipeline architecture, secure build identities, artifact promotion, and release orchestration for JVM services.
  Use when: implementing CI/CD on GCP for Java and Kotlin microservices with controlled quality and deployment gates.
---

# GCP Cloud Build


The main operating scope is: Build stages, security controls, cache strategy, and progressive delivery. Prioritize stable contracts, operational clarity, and compatibility-first delivery.

## How to design architecture and boundaries

- Use explicit contracts for Build stages, security controls, cache strategy, and progressive delivery.
- Keep ownership clear for each component and avoid implicit shared state.
- Define compatibility policy before introducing breaking changes.
- Keep technology choices aligned with quality attributes and delivery constraints.

## How to implement with Java and Kotlin

- Apply constructor-injected services and explicit DTO contracts.
- Keep framework and transport concerns out of business-core logic.
- Enforce deterministic error mapping and typed responses.
- Use static analysis and tests to prevent boundary regressions.

## How to operate and scale safely

- Define SLOs and alerts for latency, error rate, and saturation.
- Implement rollout plans with canary checks and rollback criteria.
- Keep runbooks updated with known failure modes and mitigations.
- Track dependency risk and budget for resilience patterns.

## How to troubleshoot production incidents

- Start with user-impacting symptoms, then trace to dependencies.
- Correlate logs, metrics, and traces using correlation identifiers.
- Validate recent deployments, config changes, and feature-flag state.
- Capture incident learnings as repeatable diagnostics and tests.

## Common Warnings & Pitfalls

- Over-coupling implementation to specific infrastructure details instead of explicit boundaries.
- Insufficient contract testing for changes touching Build stages, security controls, cache strategy, and progressive delivery.
- Missing observability and rollback strategy for production incidents.
- Drift between runtime behavior and documented operational guidelines.

## Common Errors and Fixes

| Symptom | Root Cause | Fix |
|---|---|---|
| Unexpected behavior after deployment | Configuration and contract mismatch between environments | Add compatibility checks, diff configs, and run canary verification. |
| Latency and error spikes under load | Missing timeout budgets or retry amplification | Set explicit timeout/retry policy and observe dependency saturation. |
| Regression in integrations | Schema or interface drift without version guardrails | Adopt versioning policy and contract tests in CI. |

## How to use extended references

- Read [Version History](references/version-history.md) before upgrades, migrations, or compatibility decisions.
- Read [Java and Kotlin Examples](references/java-kotlin-examples.md) for implementation-ready snippets and language-specific guidance.
- Read [Advanced Techniques](references/advanced-techniques.md) for specialist playbooks, incident tactics, and performance patterns.

## References

- [Official Documentation](https://cloud.google.com/build/docs)
- [Official Documentation](https://cloud.google.com/build/docs/build-config-file-schema)
- [Official Documentation](https://cloud.google.com/build/docs/securing-builds)
