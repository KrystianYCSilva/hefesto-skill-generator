---
name: hexagonal-architecture-java-kotlin
description: |
  Guides hexagonal architecture in Java and Kotlin with ports/adapters, domain isolation, and migration from layered legacy systems.
  Use when: refactoring business-critical services to isolate domain logic from frameworks, transport, persistence, and messaging details.
---

# Hexagonal Architecture Java Kotlin


The main operating scope is: Ports and adapters, domain purity, boundary tests, and migration sequencing. Prioritize stable contracts, operational clarity, and compatibility-first delivery.

## How to design architecture and boundaries

- Use explicit contracts for Ports and adapters, domain purity, boundary tests, and migration sequencing.
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
- Insufficient contract testing for changes touching Ports and adapters, domain purity, boundary tests, and migration sequencing.
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

- [Official Documentation](https://alistair.cockburn.us/hexagonal-architecture/)
- [Official Documentation](https://martinfowler.com/bliki/ArchitectureTest.html)
- [Official Documentation](https://herbertograca.com/2017/09/14/ports-adapters-architecture/)
