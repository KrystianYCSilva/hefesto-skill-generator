---
name: java-kotlin-examples
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Java and Kotlin Usage Examples

```java
@Bean
HealthIndicator paymentsHealth(PaymentGatewayClient client) {
  return () -> client.ping() ? Health.up().build() : Health.down().build();
}
```

```kotlin
@Bean
fun orderLatency(registry: MeterRegistry) = Timer
  .builder("orders.process.latency")
  .tag("service", "checkout")
  .publishPercentiles(0.5, 0.95, 0.99)
  .register(registry)
```

## Additional Java and Kotlin Tips

- Java: prefer constructor injection, explicit contracts, and stable package boundaries.
- Kotlin: use null-safety and immutable DTOs to reduce runtime inconsistencies.
- Keep serialization formats and enum naming consistent between Java and Kotlin services.

