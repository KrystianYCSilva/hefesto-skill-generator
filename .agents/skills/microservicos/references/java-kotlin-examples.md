---
name: java-kotlin-examples
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Java and Kotlin Usage Examples

```java
// BFF/service boundary contract style
record CreatePaymentRequest(String orderId, BigDecimal amount) {}
```

```kotlin
// Explicit timeout budget per outbound dependency
suspend fun reserveStock(cmd: ReserveStockCmd): ReserveStockResult =
  withTimeout(800) { inventoryClient.reserve(cmd) }
```

## Additional Java and Kotlin Tips

- Java: prefer constructor injection, explicit contracts, and stable package boundaries.
- Kotlin: use null-safety and immutable DTOs to reduce runtime inconsistencies.
- Keep serialization formats and enum naming consistent between Java and Kotlin services.

