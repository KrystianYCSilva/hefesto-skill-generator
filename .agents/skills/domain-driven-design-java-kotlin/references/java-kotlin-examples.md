---
name: java-kotlin-examples
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Java and Kotlin Usage Examples

## Java Example

`java
public final class Money { private final BigDecimal amount; private final Currency currency; }
`

## Kotlin Example

`kotlin
@JvmInline value class CustomerId(val value: UUID)
`

## Java and Kotlin Practical Notes

- Keep contracts typed and versioned at module and API boundaries.
- Align nullability, enum names, and date/time formats across both languages.
- Prefer immutable command/event DTOs for transport and integration layers.
- Validate payloads at ingress boundaries before business-core invocation.

## Topic Keywords

- bounded context
- aggregate
- ubiquitous language
- context map
- domain event

