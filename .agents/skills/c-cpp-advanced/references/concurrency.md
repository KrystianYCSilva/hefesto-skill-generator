---
name: concurrency
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Concurrency and Parallelism

This document covers advanced concurrency and parallelism techniques in C/C++.

## Lock-Free Programming

### Atomic Operations
- Compare-and-swap (CAS) patterns
- Atomic counters and flags
- Memory ordering considerations
- ABA problem solutions

### Lock-Free Data Structures
- Lock-free stacks
- Lock-free queues
- Hazard pointers
- Read-copy-update (RCU)

### Memory Models
- Sequential consistency
- Acquire-release semantics
- Relaxed memory ordering
- Fence operations

## Thread Management

### Work-Stealing Schedulers
- Task-based parallelism
- Load balancing
- Thread pool optimization
- Granularity control

### Thread-Local Storage
- Performance benefits
- Memory overhead considerations
- Destruction order
- Migration challenges

## Parallel Algorithms

### Parallel STL
- Execution policies
- Parallel algorithms
- Vectorization opportunities
- Performance considerations

### Task-Based Parallelism
- Task graphs
- Dependencies management
- Dynamic load balancing
- Cancellation support

## Synchronization Primitives

### Advanced Mutex Types
- Reader-writer locks
- Recursive mutexes
- Timed mutexes
- Adaptive mutexes

### Condition Variables
- Producer-consumer patterns
- Predicate usage
- Spurious wakeups
- Notification strategies

## Concurrency Patterns

### Actor Model
- Message passing
- State encapsulation
- Asynchronous processing
- Fault tolerance

### Futures and Promises
- Asynchronous computation
- Error propagation
- Composition patterns
- Continuation passing
