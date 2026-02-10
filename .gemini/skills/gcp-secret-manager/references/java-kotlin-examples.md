# Java and Kotlin Usage Examples

## Java Example

`java
SecretVersionName name = SecretVersionName.of(projectId, "db-pass", "latest");
`

## Kotlin Example

`kotlin
val name = SecretVersionName.of(projectId, "api-key", "latest")
`

## Java and Kotlin Practical Notes

- Keep contracts typed and versioned at module and API boundaries.
- Align nullability, enum names, and date/time formats across both languages.
- Prefer immutable command/event DTOs for transport and integration layers.
- Validate payloads at ingress boundaries before business-core invocation.

## Topic Keywords

- secret versions
- rotation
- least privilege IAM
- runtime secret loading
- audit logs
