# Java and Kotlin Usage Examples

## Java Example

`java
Use multi-module builds and ADR templates to track boundary and dependency decisions.
`

## Kotlin Example

`kotlin
Use explicit module APIs and versioned contracts for cross-pattern integration points.
`

## Java and Kotlin Practical Notes

- Keep contracts typed and versioned at module and API boundaries.
- Align nullability, enum names, and date/time formats across both languages.
- Prefer immutable command/event DTOs for transport and integration layers.
- Validate payloads at ingress boundaries before business-core invocation.

## Topic Keywords

- hybrid architecture
- phased roadmap
- ADR
- fitness functions
- architecture governance
