# Java and Kotlin Usage Examples

## Java Example

`java
Use OpenAPI-first contracts and map Spring controllers to stable response schemas.
`

## Kotlin Example

`kotlin
Keep Ktor or Spring Kotlin route contracts aligned with gateway OpenAPI definitions.
`

## Java and Kotlin Practical Notes

- Keep contracts typed and versioned at module and API boundaries.
- Align nullability, enum names, and date/time formats across both languages.
- Prefer immutable command/event DTOs for transport and integration layers.
- Validate payloads at ingress boundaries before business-core invocation.

## Topic Keywords

- OpenAPI
- JWT auth
- route policies
- quotas
- gateway rollout
