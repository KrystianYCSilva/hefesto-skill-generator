---
name: spring-boot-advanced
description: |
  Guides advanced Spring Boot capabilities including Actuator, custom auto-configuration, conditional beans, externalized configuration, events, and Micrometer observability.
  Use when: hardening Spring Boot services for production, creating platform-level starters, or troubleshooting behavior in complex deployments.
---

# Spring Boot Advanced

After Spring Boot removed most bootstrap friction, advanced teams started using it as a platform layer for observability, reusable starters, and controlled conventions. This skill helps the agent design those advanced patterns without losing maintainability.

## How to implement Actuator for production operations

1. Add `spring-boot-starter-actuator` and expose only required endpoints.
2. Prioritize `/actuator/health`, `/actuator/info`, `/actuator/metrics`, `/actuator/prometheus`.
3. Separate liveness and readiness probes for orchestrated environments.
4. Protect sensitive endpoints with network policy and authentication.

## How to create custom health indicators and info contributors

1. Implement `HealthIndicator` for critical dependencies (database, broker, third-party APIs).
2. Keep health checks fast and deterministic.
3. Use degraded states (`UP`, `DOWN`, `OUT_OF_SERVICE`, `UNKNOWN`) with useful details.
4. Implement `InfoContributor` for non-sensitive build/runtime metadata.

## How to design custom starters and auto-configuration

1. Split reusable libraries into:
- `*-starter` module for dependencies.
- `*-autoconfigure` module for conditional bean wiring.
2. Register auto-configuration via Spring Boot mechanisms for current version.
3. Keep auto-config opt-out friendly through properties.
4. Document default behavior and extension points.

## How to use conditional annotations safely

1. Prefer `@ConditionalOnClass` for optional integrations.
2. Use `@ConditionalOnMissingBean` to allow override by application teams.
3. Use `@ConditionalOnProperty` for feature toggles.
4. Avoid chains of conditions that are hard to debug without tests.

## How to control externalized configuration precedence

1. Understand precedence: command line, env vars, config files, defaults.
2. Group feature flags and operational toggles by namespace.
3. Use profile-specific overrides intentionally, not as ad-hoc patching.
4. Validate critical configuration with typed properties and constraints.

## How to use application events for decoupled workflows

1. Publish domain/application events for cross-cutting actions.
2. Use `@EventListener` for synchronous reactions that must complete inline.
3. Use async listeners for non-critical side effects (notifications, indexing).
4. Keep event payloads explicit and versionable.

## How to instrument custom metrics with Micrometer

1. Create counters, timers, and gauges for domain-level outcomes.
2. Add tags with bounded cardinality (`service`, `operation`, `result`).
3. Avoid high-cardinality tags (`userId`, random request values).
4. Align naming with dashboards and SLO alert rules.

## Common Warnings & Pitfalls

- Exposing all Actuator endpoints creates unnecessary attack surface.
- Large auto-config modules become a hidden framework inside the product.
- Feature flags without defaults lead to fragile startup behavior.
- Event listeners with side effects can accidentally create retry storms.
- Metrics with uncontrolled labels can overload observability backends.

## Common Errors and Fixes

| Symptom | Root Cause | Fix |
|---|---|---|
| Actuator endpoint returns 404 | Endpoint not exposed | Configure `management.endpoints.web.exposure.include` explicitly |
| Custom auto-config not applied | Registration missing or conditions unmet | Register auto-config correctly and validate conditional report |
| Bean override conflict | Competing definitions without `@ConditionalOnMissingBean` | Add missing-bean condition or explicit primary strategy |
| Metrics not visible in backend | Exporter missing/misconfigured | Add exporter dependency and validate endpoint/scrape config |

## Advanced Tips

- Treat platform starters as product artifacts with semantic versioning.
- Add integration tests for each conditional branch in auto-configuration.
- Build internal runbooks for interpreting health and metric signals.
- Correlate logs, traces, and metrics by propagating trace context.

## How to use extended references

- Read [Version History](references/version-history.md) before upgrades, migrations, or compatibility decisions.
- Read [Java and Kotlin Examples](references/java-kotlin-examples.md) for implementation-ready snippets and language-specific guidance.
- Read [Advanced Techniques](references/advanced-techniques.md) for specialist playbooks, incident tactics, and performance patterns.

