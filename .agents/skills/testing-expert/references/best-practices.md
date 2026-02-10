---
name: best-practices
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Testing Best Practices

## AAA Pattern (Arrange, Act, Assert)
Standard structure for clarity.

```javascript
test('should calculate total', () => {
  // Arrange
  const cart = new Cart();
  cart.add(new Item('Apple', 10));

  // Act
  const total = cart.total();

  // Assert
  expect(total).toBe(10);
});
```

## Naming Conventions
Test names should describe **behavior**, not just method names.
-   *Bad*: `testAdd`
-   *Good*: `should_return_sum_when_adding_two_positive_numbers`
-   *Good*: `given_empty_cart_when_checkout_then_throw_error`

## One Assert Per Concept
Not strictly "one assertion line", but one logical verification. Avoid testing 5 different unrelated things in one test function.

