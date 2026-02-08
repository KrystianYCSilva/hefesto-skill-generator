# Java Ecosystem & Libraries

Expert toolkit for modern Java development.

## Core Utilities
- **Apache Commons Lang3**: `StringUtils`, `ObjectUtils`. Essential standard extensions.
- **Guava**: Immutable collections (pre-Java 9), caches, graph libraries. Use selectively.
- **Lombok**: Boilerplate reduction. *Warning*: Can interfere with Javadoc and strict compilers. Prefer Records where possible.

## JSON & Serialization
- **Jackson**: The industry standard. High performance, massive ecosystem.
- **Gson**: Simpler, but slower than Jackson. Good for small projects.
- **Protobuf/Avro**: Binary formats for high-performance microservices.

## Testing
- **JUnit 5**: Modern testing framework. Use `@ParameterizedTest`.
- **Mockito**: Mocking framework. Use strict stubs (`withSettings().strictness(...)`).
- **AssertJ**: Fluent assertions. `assertThat(result).hasSize(5).contains("A")`.
- **Testcontainers**: Docker-based integration tests.

## Microservices & Cloud
- **Spring Boot**: Dominant framework. Convention over configuration.
- **Quarkus**: "Supersonic Subatomic Java". GraalVM native image first. Fast startup.
- **Micronaut**: Compile-time DI, low memory footprint.
- **Resilience4j**: Circuit Breaker, Rate Limiter, Retry. Replaces Hystrix.
- **Micrometer**: Application metrics facade (Prometheus, Datadog, etc.).

## Frontend (Java)
- **Vaadin**: Server-driven UI. Write UI in Java, runs in browser. Good for enterprise internal apps.
- **J2CL**: Google's Java-to-Closure compiler. Used for GMail/Docs. Advanced usage only.
