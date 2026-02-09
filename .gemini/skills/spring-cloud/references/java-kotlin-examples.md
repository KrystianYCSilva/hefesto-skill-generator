# Java and Kotlin Usage Examples

```java
@Bean
Customizer<Resilience4JCircuitBreakerFactory> cb() {
  return factory -> factory.configureDefault(id -> new Resilience4JConfigBuilder(id)
    .timeLimiterConfig(TimeLimiterConfig.custom().timeoutDuration(Duration.ofSeconds(2)).build())
    .circuitBreakerConfig(CircuitBreakerConfig.ofDefaults())
    .build());
}
```

```kotlin
@Component
class InventoryClient(private val webClient: WebClient) {
  fun getStock(sku: String): Mono<StockDto> = webClient.get()
    .uri("/inventory/{sku}", sku)
    .retrieve()
    .bodyToMono(StockDto::class.java)
}
```

## Additional Java and Kotlin Tips

- Java: prefer constructor injection, explicit contracts, and stable package boundaries.
- Kotlin: use null-safety and immutable DTOs to reduce runtime inconsistencies.
- Keep serialization formats and enum naming consistent between Java and Kotlin services.
