---
name: java-kotlin-examples
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Java and Kotlin Usage Examples

```java
@SpringBootApplication
public class BillingApp {
  public static void main(String[] args) {
    SpringApplication.run(BillingApp.class, args);
  }
}
```

```kotlin
@SpringBootApplication
class BillingApp

fun main(args: Array<String>) {
  runApplication<BillingApp>(*args)
}
```

```kotlin
@ConfigurationProperties("billing")
data class BillingProps(
  var retries: Int = 3,
  var timeoutMs: Long = 1500
)
```

## Additional Java and Kotlin Tips

- Java: prefer constructor injection, explicit contracts, and stable package boundaries.
- Kotlin: use null-safety and immutable DTOs to reduce runtime inconsistencies.
- Keep serialization formats and enum naming consistent between Java and Kotlin services.

