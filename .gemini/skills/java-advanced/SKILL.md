---
name: java-advanced
description: |
  Expert guide for high-performance Java development focusing on LTS versions, architecture, and JVM internals.
  Use when: designing complex systems, optimizing performance, tuning the JVM, or making architectural decisions in enterprise environments.
---

# Advanced Java Development

This skill targets senior-level development, focusing on JVM internals, high-performance concurrency, architectural patterns, and modern LTS features (Java 17, 21).

## How to design scalable architecture

Modern Java applications require robust architectural patterns.

- **Hexagonal Architecture (Ports & Adapters)**: Decouple domain logic from frameworks. Use `domain`, `application`, and `infrastructure` packages.
- **Modular Monolith**: Use Java Modules (JPMS) or strict package boundaries (ArchUnit) to enforce modularity before splitting into microservices.
- **Microservices**: Distributed systems using Spring Cloud or Quarkus. Focus on fault tolerance (Resilience4j) and observability (Micrometer/OpenTelemetry).
- **Reactive Systems**: Use Project Reactor or Mutiny for non-blocking, backpressure-ready I/O in high-throughput systems.

## How to optimize JVM performance

Performance tuning requires understanding the Java Virtual Machine.

- **Garbage Collection**: Choose the right collector.
  - **G1GC**: Default for most server apps. Balanced throughput/latency.
  - **ZGC / Shenandoah**: Low-latency requirements (<1ms pauses) for large heaps.
  - **Epsilon**: No-op GC for short-lived tasks or testing.
- **JIT Compilation**: Understand C1 (fast start) vs C2 (peak performance) optimization tiers.
- **Profiling**: Use Java Flight Recorder (JFR) and Async-profiler. Avoid `System.currentTimeMillis()` for micro-benchmarks; use JMH.

## How to utilize Modern LTS Features (17, 21)

Leverage recent language advancements for cleaner, faster code.

- **Records (Java 16+)**: Use for immutable data carriers. Replacing Lombok `@Value` in many cases.
- **Sealed Classes (Java 17)**: exhaustive modeling of domain states.
- **Virtual Threads (Java 21)**: Project Loom. Replace reactive chaining with imperative blocking code that scales to millions of threads.
- **Pattern Matching**: Switch expressions with type patterns for concise control flow.

## Common Warnings & Pitfalls

### Thread Pinning (Virtual Threads)
- **Issue**: Synchronized blocks (`synchronized`) pin the virtual thread to the carrier thread, blocking execution.
- **Fix**: Replace `synchronized` with `ReentrantLock` when using Virtual Threads.

### Stream Parallelism
- **Issue**: `stream().parallel()` uses the common ForkJoinPool. Heavy tasks can starve the pool, affecting the entire app.
- **Fix**: Use custom `ForkJoinPool` or `ExecutorService` for specific parallel tasks.

### Reflection Overhead
- **Issue**: Deep reflection calls disable JIT optimizations.
- **Fix**: Use `MethodHandles` and `VarHandles` (Java 9+) for faster dynamic access.

## Ecosystem & Applicability

- **Backend**: Spring Boot (Industry Standard), Quarkus (Cloud Native), Micronaut (Serverless), Jakarta EE.
- **Frontend**: Vaadin (Java-only UI), J2CL (Java to Closure/JS).
- **Key Libraries**: See [ECOSYSTEM.md](references/ecosystem.md) for standard stack recommendations.

## Advanced References

- **Architecture Patterns**: See [ARCHITECTURE.md](references/architecture.md).
- **Performance Tuning**: See [PERFORMANCE.md](references/performance.md).
- **Modern LTS Deep Dive**: See [MODERN-LTS.md](references/modern-lts.md).
- **Ecosystem & Libraries**: See [ECOSYSTEM.md](references/ecosystem.md).

## References

- [OpenJDK JEP Dashboard](https://openjdk.org/jeps/0)
- [Java Flight Recorder Docs](https://docs.oracle.com/en/java/java-components/jdk-mission-control/)
- [The Java Virtual Machine Specification](https://docs.oracle.com/javase/specs/jvms/se21/html/index.html)
