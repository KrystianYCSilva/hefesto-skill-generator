---
name: spring-cloud
description: |
  Guides Spring Cloud patterns for distributed systems including centralized config, service discovery, API gateway, resilience, and inter-service communication.
  Use when: building Spring microservices platforms, implementing cloud-native operational patterns, or standardizing reliability controls across services.
---

# Spring Cloud

Spring Cloud emerged to operationalize distributed systems patterns for Spring teams after microservices adoption accelerated. This skill helps the agent apply those patterns pragmatically, avoiding unnecessary complexity in early stages.

## How to define the right Spring Cloud baseline

1. Start from business and operational needs, not from feature checklists.
2. Adopt only capabilities that solve a current pain point.
3. Keep compatibility aligned across Spring Boot and Spring Cloud release trains.
4. Document platform defaults for all service teams.

## How to centralize configuration safely

1. Use externalized config with versioned sources.
2. Separate non-sensitive config from secrets.
3. Define clear override precedence and environment promotion flow.
4. Add validation/fail-fast behavior for critical properties.

## How to use service discovery and client-side load balancing

1. Register services with stable logical names.
2. Use health-aware discovery for routing decisions.
3. Apply timeouts and retries per dependency profile.
4. Avoid hardcoded host/port wiring in service code.

## How to implement API gateway boundaries

1. Route external traffic through a gateway for policy enforcement.
2. Apply authentication, rate limiting, and header normalization centrally.
3. Keep service-internal APIs separated from public edge contracts.
4. Trace requests end-to-end across gateway and downstream services.

## How to implement resilience patterns

1. Use circuit breakers for unstable dependencies.
2. Apply bulkheads and timeout budgets by downstream risk.
3. Add retries only for transient failures and idempotent operations.
4. Expose resilience metrics to operational dashboards.

## How to manage messaging and eventual consistency

1. Use async messaging where coupling and latency require decoupling.
2. Define event contracts with explicit schema evolution policy.
3. Keep idempotency for consumers and handlers.
4. Use saga/outbox patterns when cross-service consistency is needed.

## Common Warnings & Pitfalls

- Introducing full platform complexity before product-market fit.
- Using service discovery and gateway without observability coverage.
- Applying retries on non-idempotent operations.
- Spreading security policy across services instead of central standards.
- No ownership model for shared platform components.

## Common Errors and Fixes

| Symptom | Root Cause | Fix |
|---|---|---|
| Cascading timeouts across services | Missing timeout/circuit-breaker controls | Define per-hop timeout budget and resilience policies |
| Config changes cause random runtime failures | Unvalidated dynamic configuration | Add schema validation and staged rollout for config updates |
| Gateway latency spikes | Heavy filters or downstream bottlenecks | Optimize filters and profile downstream critical path |
| Service discovery flapping | Unstable health checks | Stabilize health probe logic and thresholds |

## Advanced Tips

- Treat platform primitives as product APIs with versioning and SLAs.
- Build golden paths and templates for common microservice types.
- Keep a decision log for when to add/remove distributed system features.
- Run game days for dependency failures and partial outages.

## How to use extended references

- Read [Version History](references/version-history.md) before upgrades, migrations, or compatibility decisions.
- Read [Java and Kotlin Examples](references/java-kotlin-examples.md) for implementation-ready snippets and language-specific guidance.
- Read [Advanced Techniques](references/advanced-techniques.md) for specialist playbooks, incident tactics, and performance patterns.

