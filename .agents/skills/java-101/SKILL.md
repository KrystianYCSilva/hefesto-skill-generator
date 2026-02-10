---
name: java-101
description: |
  Guide for Java development covering paradigms, best practices, version history, and advanced patterns.
  Use when: starting a new Java project, upgrading Java versions, reviewing code for best practices, or needing a reference for language features and pitfalls.
---

# Java Fundamentals (Java 101)

Java is a high-level, class-based, object-oriented programming language designed to have as few implementation dependencies as possible. It is a general-purpose language intended to let application developers write once, run anywhere (WORA).

## How to apply programming paradigms

Java supports multiple paradigms. Choose the right one for the task.

### Object-Oriented Programming (OOP)
Core of Java. Use for modeling complex domains and maintaining state.
- **Encapsulation**: Hide internal state (private fields, public accessors).
- **Inheritance**: Use sparingly. Prefer composition over inheritance.
- **Polymorphism**: Use interfaces to define contracts and decoupling.

### Functional Programming (FP)
Introduced in Java 8+. Use for data processing and concise behavior passing.
- **Lambdas**: `(args) -> body`. Use for `Runnable`, `Comparator`, event listeners.
- **Streams API**: Declarative data processing (`map`, `filter`, `reduce`).
- **Immutability**: Prefer `final` variables and immutable collections (`List.of()`).

### Imperative
Use for low-level control flow or when performance requires explicit state management.

## Common Warnings & Pitfalls

### NullPointerException (NPE)
The "billion-dollar mistake".
- **Prevention**: Use `Optional<T>`, annotations (`@NonNull`), and `Objects.requireNonNull()`.
- **Avoid**: Returning `null` from methods returning collections (return empty lists instead).

### Concurrency Issues
- **Race Conditions**: Shared mutable state without synchronization.
- **Deadlocks**: Circular dependencies on locks.
- **Solution**: Prefer `java.util.concurrent` (ExecutorService, ConcurrentHashMap) over `synchronized` blocks and `wait/notify`.

### Memory Leaks
- **Cause**: Static references to objects, unclosed resources (streams, connections).
- **Solution**: Use try-with-resources, weak references, and profiling tools.

## Best Practices (Beginner to Expert)

| Level | Focus | Key Practices |
|-------|-------|---------------|
| **Beginner** | Syntax & Basics | Naming conventions, standard library usage, try-catch blocks. |
| **Intermediate**| Design & APIs | SOLID principles, Unit Testing (JUnit), Build tools (Maven/Gradle). |
| **Expert** | JVM & Tuning | Garbage Collection tuning, ClassLoaders, Bytecode manipulation, Profiling. |

## Application Areas

- **Enterprise (Java EE/Jakarta EE)**: Large-scale backend systems, microservices (Spring Boot).
- **Mobile**: Android development (though Kotlin is preferred, Java is core).
- **Big Data**: Hadoop, Spark, Kafka ecosystem.
- **Embedded**: IoT devices, smart cards.

## Advanced Topics & History

- **Version History**: See [VERSIONS.md](references/versions.md) for detailed release notes (Java 5 to present).
- **Advanced Patterns**: See [ADVANCED.md](references/advanced.md) for design patterns and concurrency models.

## References

- [Oracle Java Documentation](https://docs.oracle.com/en/java/)
- [JEP Dashboard (JDK Enhancement Proposals)](https://openjdk.org/jeps/0)
- [Baeldung (Tutorials)](https://www.baeldung.com/)
- [Effective Java (Book Reference)](https://books.google.com/books/about/Effective_Java.html)
