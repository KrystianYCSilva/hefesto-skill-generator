# Java and Kotlin Usage Examples

## Java Example

`java
HikariConfig cfg = new HikariConfig(); cfg.setJdbcUrl(jdbcUrl); cfg.setMaximumPoolSize(20); DataSource ds = new HikariDataSource(cfg);
`

## Kotlin Example

`kotlin
val ds = HikariDataSource(HikariConfig().apply { jdbcUrl = url; maximumPoolSize = 20 })
`

## Java and Kotlin Practical Notes

- Keep contracts typed and versioned at module and API boundaries.
- Align nullability, enum names, and date/time formats across both languages.
- Prefer immutable command/event DTOs for transport and integration layers.
- Validate payloads at ingress boundaries before business-core invocation.

## Topic Keywords

- Cloud SQL connector
- Hikari pool tuning
- read replicas
- PITR backups
- failover
