---
name: declarative
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Declarative & Logical Paradigms

## Declarative
Focuses on *what* the program should accomplish without specifying *how*.
-   **SQL**: `SELECT * FROM Users WHERE Age > 18`. (Database engine decides *how* to scan).
-   **HTML**: `<img src="...">`. (Browser decides *how* to render).
-   **React (UI)**: Define the UI state, React handles DOM updates.

## Logic Programming
Based on formal logic.
-   **Prolog**: Define facts and rules. Query the system.
    ```prolog
    parent(john, mary).
    parent(mary, ann).
    grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
    ?- grandparent(john, ann).
    true.
    ```

