# Java and Kotlin Usage Examples

## Java Example

`java
FROM eclipse-temurin:21-jre\nWORKDIR /app\nCOPY build/libs/app.jar app.jar\nENTRYPOINT ["java","-jar","/app/app.jar"]
`

## Kotlin Example

`kotlin
Use the same JVM image strategy for Kotlin Spring/Ktor services with deterministic jar naming.
`

## Practical Language Tips

- Keep API and event contracts typed and versioned.
- Align nullability, enums, and date/time serialization across Java and Kotlin.
- Use shared contract tests to prevent cross-language regressions.
- Prefer immutable transport models for integration boundaries.
