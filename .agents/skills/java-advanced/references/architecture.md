---
name: architecture
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Advanced Java Architecture

## Domain-Driven Design (DDD) Implementation
- **Aggregates**: Transaction boundaries. Ensure consistency within the aggregate.
- **Value Objects**: Immutable, identity-less objects. Use Java `records`.
- **Domain Events**: Decouple side effects. Use Spring's `ApplicationEventPublisher` or CDI Events.

## Testing Strategy for Enterprise
- **ArchUnit**: Unit test your architecture. Assert that `domain` package does not depend on `infrastructure`.
- **Testcontainers**: Integration testing with real databases/brokers in Docker. No H2/mocks for persistence layers.
- **Property-Based Testing**: Use `jqwik` to test invariants rather than specific examples.

## Reactive vs Virtual Threads
- **Reactive (WebFlux/Vert.x)**: Best for maximum throughput on limited hardware. High complexity.
- **Virtual Threads (Spring Boot 3.2+)**: Best for ease of use and maintenance. "Blocking" style, reactive scalability.

