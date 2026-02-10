---
name: java-kotlin-examples
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Java and Kotlin Usage Examples

```java
public interface OrderRepository extends JpaRepository<Order, Long>, JpaSpecificationExecutor<Order> {
  @EntityGraph(attributePaths = {"customer", "items"})
  Optional<Order> findByExternalId(String externalId);
}
```

```kotlin
interface InvoiceRepository : JpaRepository<Invoice, Long> {
  fun findByStatusAndDueDateBefore(status: InvoiceStatus, date: LocalDate): List<Invoice>
}
```

## Additional Java and Kotlin Tips

- Java: prefer explicit DTO mapping over exposing JPA entities from controllers.
- Kotlin: keep entities open/proxy-friendly when using JPA, and avoid data classes for mutable entities.
- Kotlin: use nullable fields intentionally and keep DB nullability aligned with domain invariants.

