# Java and Kotlin Usage Examples

## Java Example

`java
record ApiError(String code, String message, String correlationId) {}
`

## Kotlin Example

`kotlin
data class ApiError(val code: String, val message: String, val correlationId: String)
`

## Java and Kotlin Practical Notes

- Keep contracts typed and versioned at module and API boundaries.
- Align nullability, enum names, and date/time formats across both languages.
- Prefer immutable command/event DTOs for transport and integration layers.
- Validate payloads at ingress boundaries before business-core invocation.

## Topic Keywords

- BFF
- OpenAPI
- CORS
- session cookies
- contract tests
