---
name: test-driven-development
description: |
  Apply TDD principles from Red-Green-Refactor to advanced mockist/classicist schools.
  Use when: writing new features, refactoring legacy code, or ensuring high code coverage.
---

# Test-Driven Development (TDD)

TDD is a design discipline, not just a testing technique. It drives loosely coupled, highly cohesive architecture through the Red-Green-Refactor cycle.

## How to execute the TDD Cycle

Follow the cycle strictly to ensure design benefits.

1.  **Red (Write a failing test)**:
    -   Write the *simplest* test case that defines a desired behavior.
    -   Run it. Ensure it fails for the *expected* reason (compilation error or assertion failure).
    -   *Why*: Confirms the test is valid and the feature doesn't already exist.
2.  **Green (Make it pass)**:
    -   Write the *minimum* code necessary to pass the test.
    -   Do not worry about code quality yet ("Make it work").
    -   *Why*: Avoids over-engineering.
3.  **Refactor (Clean up)**:
    -   Remove duplication, improve naming, apply patterns.
    -   Ensure all tests still pass.
    -   *Why*: "Make it right." This is where design happens.

## How to choose a TDD School

Decide based on the architectural boundary.

| School | Focus | Mocking | Best For |
|--------|-------|---------|----------|
| **Classicist (Detroit)** | State verification. | Minimal. Real objects where possible. | Domain logic, algorithms, pure functions. |
| **Mockist (London)** | Interaction verification. | Heavy. Mocks collaborators. | Service layers, controllers, external APIs. |

## How to handle dependencies

-   **Test Doubles**: Use the least powerful double that gets the job done.
    -   *Dummy*: Passed around but never used.
    -   *Stub*: Returns fixed data.
    -   *Spy*: Records interactions.
    -   *Mock*: Verifies interactions (expectations).
    -   *Fake*: Working implementation (e.g., In-Memory DB).
-   **Dependency Injection**: Crucial for testability. Inject dependencies via constructor, not `new` inside methods.

## Common Anti-Patterns

-   **The Liar**: Test passes but doesn't test what it says (e.g., mocks everything).
-   **Excessive Setup**: "Mother" or "Builder" patterns needed? Setup > 10 lines is a smell.
-   **Test-Last**: Writing tests after code is NOT TDD. It misses the design feedback loop.
-   **Testing Implementation Details**: Asserting on private fields or specific method call sequences (overspecification). Test *behavior*, not implementation.

## Examples

### Example: Red-Green-Refactor Step

**Context**: Implementing a Stack.

**Red (Failing Test):**
```java
@Test
void isEmpty_shouldReturnTrue_whenStackIsNew() {
    Stack stack = new Stack();
    assertTrue(stack.isEmpty());
}
```

**Green (Implementation):**
```java
public class Stack {
    public boolean isEmpty() {
        return true; // Hardcoded to pass
    }
}
```

**Refactor (Later step):**
```java
public class Stack {
    private int size = 0;
    public boolean isEmpty() {
        return size == 0;
    }
}
```

## References

-   [Test Driven Development: By Example (Kent Beck)](https://www.amazon.com/Test-Driven-Development-By-Example/dp/0321146530)
-   [Growing Object-Oriented Software, Guided by Tests (Freeman & Pryce)](https://www.amazon.com/Growing-Object-Oriented-Software-Guided-Tests/dp/0321503627)
