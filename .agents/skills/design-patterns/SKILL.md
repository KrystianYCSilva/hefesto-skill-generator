---
name: design-patterns
description: |
  Guide for identifying, selecting, and implementing software design patterns (Gang of Four).
  Use when: refactoring code, solving recurring design problems, or analyzing system architecture.
---

# Design Patterns Expert

Design patterns are typical solutions to common problems in software design. They are blueprints, not code. This skill helps you choose the right tool for the job.

## How to choose a Pattern Category

1.  **Creational**: Concerns object creation mechanisms.
    -   *Use when*: You need to control how objects are instantiated (e.g., Singleton, Factory).
2.  **Structural**: Concerns class and object composition.
    -   *Use when*: You need to assemble objects into larger structures while keeping them flexible (e.g., Adapter, Decorator).
3.  **Behavioral**: Concerns communication between objects.
    -   *Use when*: You need to manage algorithms, relationships, and responsibilities (e.g., Observer, Strategy).

## How to identify Anti-Patterns (When NOT to use)

-   **Golden Hammer**: Forcing a pattern where it doesn't fit (e.g., using Singleton for everything).
-   **Poltergeist**: Classes with limited roles that just pass data to others (useless wrappers).
-   **Spaghetti Code**: Result of over-using patterns without understanding them, creating unreadable flow.

## Common Warnings & Pitfalls

### Singleton Abuse
-   **Issue**: Singletons hide dependencies and make unit testing difficult (global state).
-   **Fix**: Use Dependency Injection instead.

### Factory Explosion
-   **Issue**: Creating a Factory for every single class, doubling the codebase size.
-   **Fix**: Use simple constructors until complex creation logic is actually needed.

### Decorator Hell
-   **Issue**: Too many small decorators making the object initialization look like an onion.
-   **Fix**: Re-evaluate if composition is the right tool, or use a Builder to manage the complexity.

## Best Practices

| Rule | Explanation |
|------|-------------|
| **Favor Composition** | Composition over Inheritance allows dynamic behavior change. |
| **Program to Interface** | Depend on abstractions, not concrete implementations. |
| **KISS** | Don't use a pattern if a simple `if/else` does the job cleanly. |

## Deep Dives

-   **Creational Patterns**: See [CREATIONAL.md](references/creational.md).
-   **Structural Patterns**: See [STRUCTURAL.md](references/structural.md).
-   **Behavioral Patterns**: See [BEHAVIORAL.md](references/behavioral.md).

## References

-   [Refactoring.guru (Design Patterns)](https://refactoring.guru/design-patterns)
-   [Design Patterns: Elements of Reusable Object-Oriented Software](https://en.wikipedia.org/wiki/Design_Patterns)
