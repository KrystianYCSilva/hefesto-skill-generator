---
name: legacy-code-refactoring
description: |
  Modernize legacy systems using safe strategies like Seams, Characterization Tests, and the Strangler Fig pattern.
  Use when: working with undocumented code, refactoring systems without tests, or breaking down monoliths.
---

# Legacy Code Refactoring

"Legacy code is simply code without tests." — Michael Feathers. This skill guides the safe evolution of such systems.

## How to Analyze Undocumented Systems

Before changing code, understand its behavior.

1.  **Identify Seams**: Find places where you can alter behavior without editing code (e.g., interface boundaries, virtual methods).
2.  **Characterization Tests**: Write tests that capture the *current* behavior (even bugs).
    -   *Goal*: Ensure refactoring doesn't change behavior.
    -   *Technique*: Call the method, assert a dummy value, run test, update assert with actual value.
3.  **Effect Analysis**: Trace variables to see where values come from and go to. Use "Scratch Refactoring" (temporary refactoring to understand) but throw it away.

## How to Plan Refactoring

Refactoring requires a strategy, not just "cleaning up".

-   **Pre-requisites**:
    -   *Source Control*: Ensure strict versioning (Git).
    -   *Reproducibility*: Ability to build and run the system locally.
    -   *Safety Net*: Minimum set of Characterization Tests (Golden Master).
-   **Planning Strategy**:
    -   *Mikado Method*: Explore dependencies by trying a change, failing, reverting, and noting the prerequisite. Build a graph of prerequisites.
    -   *Campground Rule*: Always leave the code behind a little cleaner than you found it.

## How to Make Safe Changes

When you can't get full test coverage, use targeted strategies.

-   **Sprout Method**: Need to add logic? Create a *new* method, test it, and call it from the legacy code.
    -   *Pros*: New code is tested.
    -   *Cons*: Legacy code remains untested.
-   **Wrap Method**: Rename the old method, create a new one with the old name that calls the new logic + old method.
    -   *Use when*: Adding pre/post-processing (logging, validation).
-   **Parallel Change**:
    1.  Add new field/method.
    2.  Write to both old and new.
    3.  Read from old.
    4.  Switch read to new.
    5.  Remove old.

## How to Maintain Critical Systems

For banking/enterprise monoliths where failure is not an option.

-   **Feature Flags**: Wrap changes in toggles. Deploy disabled, enable gradually (Canary).
-   **Database First**: In data-heavy systems, refactor the schema *last*. Use Views or Stored Procedures to shield code from schema changes during transition.
-   **Logs as Truth**: Compare logs from Production vs. Staging to verify behavior identity.

## How to Modernize Monoliths

> See [Modernization Patterns](references/modernization-patterns.md) for detailed architectural moves.

-   **Strangler Fig Pattern**: Create a new system around the edges of the old one, intercepting calls and gradually migrating functionality until the old system is strangled.
-   **Bubble Context**: Isolate a clean domain model within the legacy mess using an Anticorruption Layer (ACL).

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| **Big Bang Rewrite** | High risk, no value delivered for months. | Use Iterative/Strangler approach. |
| **Refactoring without Tests** | "Refactoring" becomes "breaking". | Write Characterization Tests first. |
| **Analysis Paralysis** | Trying to understand *everything* before changing *anything*. | Understand only the "Scratch" area needed for the task. |

## Examples

### Example: Sprout Method

**Task**: Add unique ID validation to `ProcessOrder`.

**Legacy Code:**
```java
void processOrder(Order order) {
    // 500 lines of spaghetti
}
```

**Refactored:**
```java
void processOrder(Order order) {
    if (!isValid(order.id)) return; // Sprout
    // 500 lines of spaghetti
}

// New, tested method
boolean isValid(int id) { ... }
```

## References

-   [Working Effectively with Legacy Code (Michael Feathers)](https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052)
-   [Refactoring: Improving the Design of Existing Code (Martin Fowler)](https://martinfowler.com/books/refactoring.html)
-   [Strangler Fig Pattern](https://martinfowler.com/bliki/StranglerFigApplication.html)
-   [The Mikado Method](https://mikadomethod.info/)
