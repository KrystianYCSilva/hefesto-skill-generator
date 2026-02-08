---
name: testing-expert
description: |
  Comprehensive guide for software testing fundamentals, strategies, and best practices.
  Use when: planning test strategy, writing unit/integration/e2e tests, reviewing test quality, or debugging CI pipelines.
---

# Testing Expert

This skill transforms the agent into a QA Expert. It covers the Testing Pyramid, how to select scenarios, and how to write effective, maintainable tests.

## How to design a Test Strategy

Apply the **Testing Pyramid**:
1.  **Unit Tests (70%)**: Fast, isolated, test single functions/classes.
2.  **Integration Tests (20%)**: Test interaction between modules/databases.
3.  **E2E Tests (10%)**: Slow, brittle, test full user flows in a real environment.

## How to write Effective Tests

-   **Structure**: Use AAA (Arrange, Act, Assert) or GWT (Given, When, Then).
-   **Isolation**: Tests should not depend on each other or shared global state.
-   **Determinism**: Flaky tests are worse than no tests. Avoid `Thread.sleep` or random data without seeds.

## How to select Scenarios

Don't just test the "Happy Path".
-   **Happy Path**: Standard success case.
-   **Edge Cases**: Empty lists, nulls, max integers, boundary values.
-   **Error Cases**: Exceptions, timeouts, invalid inputs (security).

## Common Warnings & Pitfalls

### Mocking Hell
-   **Issue**: Mocking everything leads to "implementation detail" testing.
-   **Fix**: Only mock external boundaries (Network, DB). Do not mock internal privates.

### Testing Implementation Details
-   **Issue**: Test breaks when refactoring internal logic, even if behavior stays same.
-   **Fix**: Test public behavior/API, not private methods.

### Flaky Tests
-   **Issue**: Tests fail randomly on CI.
-   **Fix**: Eliminate race conditions, use implicit waits (not sleep), ensure clean DB state.

## Best Practices (The "First" Principle)

| Acronym | Meaning |
|---------|---------|
| **F**ast | Tests should run quickly to enable TDD. |
| **I**solated | Failure in one test shouldn't cascade. |
| **R**epeatable | Run anywhere (dev machine, CI) with same result. |
| **S**elf-Validating | Boolean pass/fail. No manual inspection. |
| **T**imely | Written just before or with the code (TDD). |

## Deep Dives

-   **Test Types**: See [TYPES.md](references/types.md) (Unit vs Integration vs E2E).
-   **Best Practices**: See [BEST-PRACTICES.md](references/best-practices.md).
-   **Scenario Selection**: See [SCENARIOS.md](references/scenarios.md).

## References

-   [The Testing Pyramid (Martin Fowler)](https://martinfowler.com/articles/practical-test-pyramid.html)
-   [xUnit Patterns](http://xunitpatterns.com/)
-   [Test Driven Development (Kent Beck)](https://www.oreilly.com/library/view/test-driven-development/0321146530/)
