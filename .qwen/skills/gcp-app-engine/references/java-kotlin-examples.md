# Java and Kotlin Usage Examples

```yaml
# app.yaml
runtime: java17
instance_class: F2
automatic_scaling:
  min_instances: 1
  max_instances: 20
env_variables:
  SPRING_PROFILES_ACTIVE: prod
```

```java
@RestController
class HealthController {
  @GetMapping("/internal/health")
  String health() { return "ok"; }
}
```

```kotlin
@RestController
class BuildInfoController {
  @GetMapping("/build")
  fun build(): Map<String, String> = mapOf("service" to "billing", "runtime" to "java17")
}
```

## Additional Java and Kotlin Tips

- Java: prefer constructor injection, explicit contracts, and stable package boundaries.
- Kotlin: use null-safety and immutable DTOs to reduce runtime inconsistencies.
- Keep serialization formats and enum naming consistent between Java and Kotlin services.
