# Java and Kotlin Usage Examples

## Java Example

`java
ForkJoinPool.commonPool().submit(() -> processChunk(chunk));
`

## Kotlin Example

`kotlin
withContext(Dispatchers.Default) { chunks.map { async { process(it) } }.awaitAll() }
`

## Practical Language Tips

- Keep API and event contracts typed and versioned.
- Align nullability, enums, and date/time serialization across Java and Kotlin.
- Use shared contract tests to prevent cross-language regressions.
- Prefer immutable transport models for integration boundaries.
