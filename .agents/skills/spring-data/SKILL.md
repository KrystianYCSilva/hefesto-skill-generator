---
name: spring-data
description: |
  Guides Spring Data JPA repository design, query strategies, transaction boundaries, relationship mapping, fetch tuning, and N+1 mitigation.
  Use when: implementing persistence in Spring applications, optimizing query performance, or standardizing repository patterns for complex domains.
---

# Spring Data

Spring Data abstracted repetitive DAO code and made repository patterns first-class in Spring ecosystems. This skill helps the agent apply Spring Data JPA with performance awareness and clear transactional boundaries.

## How to design repository interfaces

1. Start with `JpaRepository` for aggregate roots and common CRUD operations.
2. Keep repository methods aligned with domain language.
3. Avoid exposing persistence-specific details to upper layers.
4. Use dedicated repositories per aggregate, not generic mega-repositories.

## How to choose query strategies

1. Use derived query methods for straightforward predicates.
2. Use `@Query` JPQL when intent is clear and reusable.
3. Use native SQL only for database-specific optimizations.
4. Use Specifications/Criteria for dynamic filters and composability.

## How to manage transactions safely

1. Put `@Transactional` primarily at service boundaries.
2. Use read-only transactions for read paths when appropriate.
3. Set explicit propagation/isolation only when business rules demand it.
4. Avoid long transactions with remote calls inside.

## How to model relationships and fetch behavior

1. Default to `LAZY` and fetch only what the use case needs.
2. Keep bidirectional mappings only where navigation is required.
3. Control cascade and `orphanRemoval` to match lifecycle ownership.
4. Prefer explicit DTO projections for API payloads.

## How to solve N+1 and heavy query plans

1. Detect N+1 with SQL logs and integration tests.
2. Use `@EntityGraph` or fetch joins for targeted read use cases.
3. Combine pagination with explicit sorting and index strategy.
4. Validate generated SQL with query plans.

## How to apply auditing and lifecycle metadata

1. Enable JPA auditing for `createdAt`, `updatedAt`, `createdBy`.
2. Keep audit columns in a shared mapped superclass when possible.
3. Ensure timezone consistency (UTC) across application and database.
4. Keep audit writes deterministic and testable.

## Common Warnings & Pitfalls

- Exposing entities directly in API layers increases coupling and leak risk.
- Default EAGER relationships often create hidden query explosions.
- Repository methods that encode business rules become hard to evolve.
- Pagination without deterministic sort can produce unstable pages.
- Native queries without tests break silently during schema evolution.

## Common Errors and Fixes

| Symptom | Root Cause | Fix |
|---|---|---|
| `LazyInitializationException` | Accessing lazy relation outside transaction | Fetch required data in service transaction or map to DTO before leaving boundary |
| Slow list endpoint | N+1 selects or missing index | Add `@EntityGraph`/fetch join and create supporting index |
| `detached entity passed to persist` | Wrong entity state handling | Use merge/save semantics correctly and manage aggregate ownership |
| Deadlock/lock timeout | Transaction scope too wide | Reduce transaction duration and tune lock/order strategy |

## Advanced Tips

- Use projection interfaces for read-mostly queries to reduce hydration cost.
- Adopt outbox pattern when DB write and event publish must stay consistent.
- Review query plans after each significant schema migration.
- Define repository coding conventions and enforce via code review templates.

## How to use extended references

- Read [Version History](references/version-history.md) before upgrades, migrations, or compatibility decisions.
- Read [Java and Kotlin Examples](references/java-kotlin-examples.md) for implementation-ready snippets and language-specific guidance.
- Read [Advanced Techniques](references/advanced-techniques.md) for specialist playbooks, incident tactics, and performance patterns.

