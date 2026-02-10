---
name: java-kotlin-examples
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Java and Kotlin Usage Examples

## Java Example

`java
apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: orders-api
`

## Kotlin Example

`kotlin
Use readiness and liveness probes with Kotlin services to avoid restart storms under startup load.
`

## Practical Language Tips

- Keep API and event contracts typed and versioned.
- Align nullability, enums, and date/time serialization across Java and Kotlin.
- Use shared contract tests to prevent cross-language regressions.
- Prefer immutable transport models for integration boundaries.

