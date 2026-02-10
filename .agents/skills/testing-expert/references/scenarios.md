---
name: scenarios
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Scenario Selection Cheat Sheet

## Equivalence Partitioning
Divide inputs into classes where behavior should be same. Test one value from each class.
*Example: Age verification (>= 18)*
-   **Class 1 (Valid)**: 25
-   **Class 2 (Invalid)**: 15

## Boundary Value Analysis
Bugs hide at boundaries.
*Example: Age >= 18*
-   Test **17** (Boundary - 1)
-   Test **18** (Boundary)
-   Test **19** (Boundary + 1)

## Error Guessing based on Experience
-   **Strings**: Null, Empty string `""`, Blank string `"  "`, Special chars `ñ, @, emoji`, SQL Injection `' OR 1=1`.
-   **Numbers**: 0, -1, MaxInt, MinInt, Floats (`0.1 + 0.2`).
-   **Collections**: Empty list, List with 1 item, List with duplicates.

