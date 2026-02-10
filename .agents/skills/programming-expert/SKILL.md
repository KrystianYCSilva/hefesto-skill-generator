---
name: programming-expert
description: |
  Comprehensive guide for language-agnostic programming concepts, from algorithms and data structures to modern architectural patterns.
  Use when: learning new languages, solving algorithmic problems, designing systems, or reviewing code fundamentals.
---

# Programming Expert

This skill covers the universal foundations of software engineering. It focuses on concepts that transcend specific languages, enabling the agent to adapt to any stack.

## How to analyze Algorithm Complexity (Big O)

Performance is measured by how execution time/space grows with input size ($n$).

- **$O(1)$ (Constant)**: Direct access (Array index, Hash Map).
- **$O(\log n)$ (Logarithmic)**: Binary Search, Balanced Trees. Halves input each step.
- **$O(n)$ (Linear)**: Iterating a list.
- **$O(n \log n)$ (Linearithmic)**: Efficient sorting (Merge Sort, Quick Sort).
- **$O(n^2)$ (Quadratic)**: Nested loops (Bubble Sort).
- **$O(2^n)$ (Exponential)**: Recursive solutions (Fibonacci).

## How to choose Data Structures

- **Array/List**: Contiguous memory. Fast access $O(1)$, slow insertion/deletion $O(n)$.
- **Linked List**: Non-contiguous. Fast insertion/deletion $O(1)$, slow access $O(n)$.
- **Hash Map/Table**: Key-Value pairs. Average $O(1)$ access/insertion.
- **Tree**: Hierarchical data. Binary Search Tree (BST) for sorted data.
- **Graph**: Nodes (vertices) and edges. Modeling networks.

## How to apply Programming Paradigms

- **Imperative**: "How" to do it. State changes step-by-step.
- **Object-Oriented (OOP)**: Encapsulation, Inheritance, Polymorphism, Abstraction.
- **Functional (FP)**: Pure functions, immutability, higher-order functions (map/filter/reduce).
- **Declarative**: "What" to do (SQL, HTML).

## Common Warnings & Pitfalls

### Premature Optimization
- **Issue**: Optimizing code before proving it's a bottleneck.
- **Fix**: Make it work, make it right, make it fast.

### Magic Numbers
- **Issue**: Hardcoded values (`if status == 2`).
- **Fix**: Use named constants/enums (`if status == STATUS_ACTIVE`).

### Tight Coupling
- **Issue**: Classes dependent on concrete implementations.
- **Fix**: Dependency Injection and coding to interfaces (SOLID).

## Best Practices (Clean Code)

| Concept | Rule |
|---------|------|
| **DRY** | Don't Repeat Yourself. Abstract common logic. |
| **KISS** | Keep It Simple, Stupid. Avoid over-engineering. |
| **YAGNI** | You Ain't Gonna Need It. Don't implement features "just in case". |
| **SOLID** | Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion. |

## Deep Dives

- **Algorithms**: See [ALGORITHMS.md](references/algorithms.md).
- **Data Structures**: See [DATA-STRUCTURES.md](references/data-structures.md).
- **Design Patterns**: See [PATTERNS.md](references/patterns.md).

## References

- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
- [Design Patterns (Gang of Four)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Clean Code (Robert C. Martin)](https://www.oreilly.com/library/view/clean-code-a/9780132350884/)
