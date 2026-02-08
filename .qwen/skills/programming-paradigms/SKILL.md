---
name: programming-paradigms
description: |
  Guide for understanding and applying core programming paradigms (OOP, FP, Imperative, Declarative).
  Use when: designing system architecture, refactoring legacy code, or choosing the right approach for a specific problem.
---

# Programming Paradigms Expert

A programming paradigm is a style or way of programming. Modern development is often **Multi-Paradigm**, combining the best features of different styles (e.g., using functional `map/filter` inside an OOP Service).

## How to apply Imperative & Declarative

-   **Imperative (How)**: Step-by-step state changes. C, Pascal, Java (basic).
    -   *Use when*: Performance is critical, low-level hardware control.
-   **Declarative (What)**: Express logic without control flow. SQL, HTML, CSS, Prolog.
    -   *Use when*: Querying data, defining UI, configuration.

## How to apply Object-Oriented Programming (OOP)

Modeling software based on "objects" containing data and code.

-   **Core**: Encapsulation, Inheritance, Polymorphism, Abstraction.
-   **Use when**: Modeling complex business domains, managing large stateful systems, GUI development.
-   **Multi-Paradigm**: Combine with FP for cleaner method internals.

## How to apply Functional Programming (FP)

Computation as the evaluation of mathematical functions. Avoids changing-state and mutable data.

-   **Core**: Pure Functions, Immutability, First-Class Functions, Higher-Order Functions.
-   **Use when**: Data processing pipelines, concurrency (no shared state), distributed systems.

## Common Warnings & Pitfalls

### Paradigm War
-   **Issue**: Believing one paradigm is "better" than others.
-   **Fix**: Pragmatism. Use the right tool for the job. (e.g., Don't force OOP patterns in a simple script).

### Mutable State Hell (Imperative/OOP)
-   **Issue**: Shared mutable state leads to race conditions and unpredictable bugs.
-   **Fix**: Adopt FP principles like Immutability even in OOP code.

### Monad Complexity (FP)
-   **Issue**: Over-abstracting simple logic with complex category theory concepts.
-   **Fix**: Use FP for clarity (map/reduce), not just for academic purity.

## Best Practices (Multi-Paradigm)

| Goal | Approach |
|------|----------|
| **Domain Modeling** | Use **OOP**. Classes map well to nouns (User, Order). |
| **Data Transformation** | Use **FP**. Pipelines (stream -> filter -> map) are readable and safe. |
| **System State** | Use **OOP** (Encapsulation) or **FP** (Immutable State Containers like Redux). |
| **Querying** | Use **Declarative** (SQL, LINQ). |

## Deep Dives

-   **Object-Oriented**: See [OOP.md](references/oop.md).
-   **Functional**: See [FUNCTIONAL.md](references/functional.md).
-   **Declarative/Logical**: See [DECLARATIVE.md](references/declarative.md).

## References

-   [Concepts, Techniques, and Models of Computer Programming](https://www.info.ucl.ac.be/~pvr/book.html)
-   [Structure and Interpretation of Computer Programs (SICP)](https://mitpress.mit.edu/sites/default/files/sicp/index.html)
