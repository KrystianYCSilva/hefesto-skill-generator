---
name: creational
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Creational Patterns

## Factory Method
Defines an interface for creating an object, but lets subclasses alter the type of objects that will be created.
-   *Use when*: You don't know beforehand the exact types and dependencies of the objects your code should work with.

## Abstract Factory
Produces families of related objects without specifying their concrete classes.
-   *Use when*: Code needs to work with various families of related products (e.g., Windows vs Mac UI components).

## Builder
Constructs complex objects step by step.
-   *Use when*: Constructor has 10+ parameters, many optional.

## Singleton
Ensures a class has only one instance and provides a global access point.
-   *Warning*: Often an anti-pattern. Use Dependency Injection where possible.

