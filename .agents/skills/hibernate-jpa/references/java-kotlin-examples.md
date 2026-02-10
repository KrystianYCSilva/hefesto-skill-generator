---
name: java-kotlin-examples
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Java and Kotlin Usage Examples

## Java Example

`java
@Entity class OrderEntity { @Id Long id; @ManyToOne(fetch = FetchType.LAZY) CustomerEntity customer; }
`

## Kotlin Example

`kotlin
@Entity class OrderEntity(@Id var id: Long? = null)
`

## Practical Language Tips

- Keep API and event contracts typed and versioned.
- Align nullability, enums, and date/time serialization across Java and Kotlin.
- Use shared contract tests to prevent cross-language regressions.
- Prefer immutable transport models for integration boundaries.

