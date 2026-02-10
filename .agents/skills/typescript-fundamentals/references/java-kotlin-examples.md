---
name: java-kotlin-examples
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Java and Kotlin Integration Examples

```yaml
# OpenAPI flow for JVM backend + TS frontend
springdoc-openapi -> openapi.yaml -> openapi-generator typescript client
```

```typescript
type OrderStatus = "CREATED" | "PAID" | "CANCELLED";
function assertNever(x: never): never { throw new Error(`Unexpected: ${x}`); }
```

## Additional Java and Kotlin Tips

- Generate TypeScript clients from Spring/Ktor OpenAPI specs to avoid contract drift.
- Keep enum/date serialization aligned across JVM and TypeScript clients.
- Use shared compatibility tests for error payload schemas.

