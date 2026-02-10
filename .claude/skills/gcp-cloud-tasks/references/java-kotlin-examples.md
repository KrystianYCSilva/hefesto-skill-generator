# Java and Kotlin Usage Examples

## Java Example

`java
Task task = Task.newBuilder().setHttpRequest(HttpRequest.newBuilder().setUrl(url).build()).build(); client.createTask(queuePath, task);
`

## Kotlin Example

`kotlin
val task = Task.newBuilder().setHttpRequest(HttpRequest.newBuilder().setUrl(url).build()).build(); client.createTask(queuePath, task)
`

## Practical Language Tips

- Keep API and event contracts typed and versioned.
- Align nullability, enums, and date/time serialization across Java and Kotlin.
- Use shared contract tests to prevent cross-language regressions.
- Prefer immutable transport models for integration boundaries.
