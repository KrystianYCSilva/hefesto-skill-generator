---
name: java-kotlin-examples
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Java and Kotlin Usage Examples

```dockerfile
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY build/libs/app.jar app.jar
ENTRYPOINT ["java","-XX:MaxRAMPercentage=75","-jar","/app/app.jar"]
```

```kotlin
@Bean
fun gracefulShutdown() = ApplicationListener<ContextClosedEvent> {
  // flush telemetry and stop consumers gracefully
}
```

## Additional Java and Kotlin Tips

- Java: prefer constructor injection, explicit contracts, and stable package boundaries.
- Kotlin: use null-safety and immutable DTOs to reduce runtime inconsistencies.
- Keep serialization formats and enum naming consistent between Java and Kotlin services.

