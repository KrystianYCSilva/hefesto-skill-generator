---
name: functional
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Functional Programming (FP)

## Core Concepts
-   **Pure Functions**: Same input always equals same output. No side effects (I/O, changing globals).
-   **Immutability**: Data cannot be changed after creation. Modification creates a copy.
-   **First-Class Functions**: Functions can be assigned to variables and passed as arguments.
-   **Higher-Order Functions**: Functions that take other functions as args (`map`, `filter`, `reduce`).

## Benefits
-   **Testability**: Pure functions are trivial to test.
-   **Concurrency**: No race conditions without shared mutable state.
-   **Reasoning**: Referential Transparency makes code easier to understand.

