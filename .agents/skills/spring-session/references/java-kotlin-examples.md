---
name: java-kotlin-examples
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Java and Kotlin Usage Examples

```java
@Bean
RedisIndexedSessionRepository redisSessionRepository(RedisConnectionFactory cf) {
  RedisIndexedSessionRepository repo = new RedisIndexedSessionRepository(cf);
  repo.setDefaultMaxInactiveInterval(1800);
  return repo;
}
```

```kotlin
@Configuration
class SessionConfig {
  @Bean
  fun cookieSerializer(): DefaultCookieSerializer = DefaultCookieSerializer().apply {
    setUseSecureCookie(true)
    setSameSite("Lax")
  }
}
```

## Additional Java and Kotlin Tips

- Java: prefer constructor injection, explicit contracts, and stable package boundaries.
- Kotlin: use null-safety and immutable DTOs to reduce runtime inconsistencies.
- Keep serialization formats and enum naming consistent between Java and Kotlin services.

