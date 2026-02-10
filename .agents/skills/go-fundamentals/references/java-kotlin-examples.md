---
name: java-kotlin-examples
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Java and Kotlin Integration Examples

```yaml
# Service interoperability pattern
Go service (gRPC/OpenAPI) <-> Spring Boot/Ktor clients with generated contracts
```

```go
ctx, cancel := context.WithTimeout(parentCtx, 2*time.Second)
defer cancel()
resp, err := client.Do(req.WithContext(ctx))
```

## Additional Java and Kotlin Tips

- Generate JVM clients from Go gRPC/OpenAPI definitions with versioned contracts.
- Normalize timeout and retry semantics across Go and Spring/Ktor clients.
- Keep idempotency and error-code mapping documented for cross-language flows.

