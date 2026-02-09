# Java and Kotlin Usage Examples

```java
@Cacheable(cacheNames = "products", key = "#sku")
public ProductDto findProduct(String sku) { return productGateway.fetch(sku); }

@CacheEvict(cacheNames = "products", key = "#sku")
public void invalidateProduct(String sku) {}
```

```kotlin
@Cacheable(cacheNames = ["exchange-rate"], key = "#base + ':' + #quote")
fun quote(base: String, quote: String): FxRate = provider.quote(base, quote)
```

## Additional Java and Kotlin Tips

- Java: prefer constructor injection, explicit contracts, and stable package boundaries.
- Kotlin: use null-safety and immutable DTOs to reduce runtime inconsistencies.
- Keep serialization formats and enum naming consistent between Java and Kotlin services.
