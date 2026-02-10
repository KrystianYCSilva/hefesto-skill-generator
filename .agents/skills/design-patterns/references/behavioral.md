---
name: behavioral
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Behavioral Patterns

## Observer
Defines a subscription mechanism to notify multiple objects about any events that happen to the object they're observing.
-   *Use when*: Changes to one object require changing others, and you don't know how many objects need to be changed.

## Strategy
Defines a family of algorithms, puts each into a separate class, and makes their objects interchangeable.
-   *Use when*: You want to use different variants of an algorithm within an object and be able to switch from one to another during runtime.

## Command
Turns a request into a stand-alone object that contains all information about the request.
-   *Use when*: You want to parameterize objects with operations, queue operations, or support undoable operations.

## State
Lets an object alter its behavior when its internal state changes.
-   *Use when*: An object behaves differently depending on its current state, and the number of states is enormous.

