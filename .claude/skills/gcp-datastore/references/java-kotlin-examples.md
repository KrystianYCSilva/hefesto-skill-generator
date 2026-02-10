# Java and Kotlin Usage Examples

## Java Example

`java
Entity task = Entity.newBuilder(keyFactory.newKey("t1")).set("status", "OPEN").build(); datastore.put(task);
`

## Kotlin Example

`kotlin
val task = Entity.newBuilder(keyFactory.newKey("t1")).set("status", "OPEN").build(); datastore.put(task)
`

## Practical Language Tips

- Keep API and event contracts typed and versioned.
- Align nullability, enums, and date/time serialization across Java and Kotlin.
- Use shared contract tests to prevent cross-language regressions.
- Prefer immutable transport models for integration boundaries.
