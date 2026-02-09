---
name: spring-cache
description: |
  Guides cache architecture with Spring Cache abstraction, provider selection (Caffeine/Redis), invalidation strategy, and cache observability.
  Use when: reducing read latency and database pressure in Spring services, defining cache consistency rules, or troubleshooting stale-data behavior.
---

# Spring Cache

Spring Cache added a standard abstraction over cache providers so teams can optimize read-heavy workloads without coupling business code to vendor APIs. This skill helps the agent design reliable caching with explicit consistency trade-offs.

## How to choose cache scope and provider

1. Use local cache (Caffeine) for low-latency per-instance acceleration.
2. Use distributed cache (Redis) when state must be shared across instances.
3. Match provider choice to consistency, latency, and cost constraints.
4. Keep cache ownership explicit per bounded context.

## How to apply Spring Cache annotations safely

1. Use `@Cacheable` for deterministic read paths.
2. Use `@CachePut` when write operations must refresh cache state.
3. Use `@CacheEvict` for invalidation after updates/deletes.
4. Keep keys explicit and stable; avoid accidental collisions.

## How to design key, TTL, and invalidation strategy

1. Define key schema by entity identity and query dimensions.
2. Set TTL based on business freshness requirements.
3. Prefer event-driven invalidation for high-consistency paths.
4. Document stale-read tolerance per endpoint/use case.

## How to prevent cache stampede and hot keys

1. Use per-key locking or request coalescing for expensive loads.
2. Add jitter to TTL when many keys expire simultaneously.
3. Identify hot keys and consider sharding or local near-cache.
4. Add fallback behavior when cache backend is degraded.

## How to observe cache effectiveness

1. Track hit ratio, miss ratio, eviction counts, and load latency.
2. Monitor backend pressure and fallback behavior.
3. Define alerts for sudden miss spikes.
4. Review cache metrics alongside DB/query latency.

## Common Warnings & Pitfalls

- Caching non-deterministic or permission-sensitive responses.
- No invalidation strategy after writes.
- Overly long TTL causing stale critical data.
- Treating cache as source of truth.
- Missing namespace/versioning in key formats.

## Common Errors and Fixes

| Symptom | Root Cause | Fix |
|---|---|---|
| Stale data after update | Missing `@CacheEvict`/refresh logic | Add write-path invalidation or `@CachePut` strategy |
| Memory spikes in app | Unbounded local cache | Configure max size and eviction policy |
| Low hit ratio despite cache | Poor key design or low temporal locality | Redesign keys and validate cached query pattern |
| Cache outage breaks API | No graceful degradation path | Implement fallback to source-of-truth with circuit controls |

## Advanced Tips

- Use two-level cache (local + distributed) for high-read workloads.
- Version cache keys during schema changes to avoid mixed payloads.
- Run cache warm-up for predictable high-traffic windows.
- Treat cache rules as domain policy, not infrastructure defaults only.

## How to use extended references

- Read [Version History](references/version-history.md) before upgrades, migrations, or compatibility decisions.
- Read [Java and Kotlin Examples](references/java-kotlin-examples.md) for implementation-ready snippets and language-specific guidance.
- Read [Advanced Techniques](references/advanced-techniques.md) for specialist playbooks, incident tactics, and performance patterns.

