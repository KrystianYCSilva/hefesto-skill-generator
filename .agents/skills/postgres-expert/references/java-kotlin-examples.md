---
name: java-kotlin-examples
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Java and Kotlin Usage Examples

```java
HikariConfig cfg = new HikariConfig();
cfg.setJdbcUrl(jdbcUrl);
cfg.setMaximumPoolSize(20);
cfg.setConnectionTimeout(3000);
DataSource ds = new HikariDataSource(cfg);
```

```kotlin
@Transactional(readOnly = true)
fun findOpenInvoices(limit: Int): List<InvoiceDto> =
  jdbcTemplate.query(
    "select id, total from invoice where status = 'OPEN' order by created_at desc limit ?",
    { rs, _ -> InvoiceDto(rs.getLong("id"), rs.getBigDecimal("total")) },
    limit
  )
```

## Additional Java and Kotlin Tips

- Java: prefer constructor injection, explicit contracts, and stable package boundaries.
- Kotlin: use null-safety and immutable DTOs to reduce runtime inconsistencies.
- Keep serialization formats and enum naming consistent between Java and Kotlin services.

