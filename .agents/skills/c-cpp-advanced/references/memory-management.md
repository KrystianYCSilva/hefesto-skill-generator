---
name: memory-management
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Memory Management Deep Dive

This document provides comprehensive coverage of advanced memory management techniques in C/C++.

## RAII (Resource Acquisition Is Initialization)

RAII is a fundamental C++ idiom that ties resource management to object lifetime. The core principle is that resource acquisition happens during object construction, and resource release occurs during destruction.

### Key Concepts:
- Constructor acquires resources
- Destructor releases resources
- Exception safety through automatic cleanup
- Stack unwinding guarantees resource cleanup

## Smart Pointers

Modern C++ provides several smart pointer types for automatic memory management:

### std::unique_ptr
- Exclusive ownership of dynamically allocated objects
- Zero-cost abstraction over raw pointers
- Move semantics for transferring ownership
- Custom deleters for non-standard cleanup

### std::shared_ptr
- Shared ownership through reference counting
- Thread-safe reference counting
- Custom deleters
- std::weak_ptr for breaking cycles

### std::weak_ptr
- Non-owning observer of shared_ptr-managed objects
- Breaking circular references
- Checking validity before access

## Custom Allocators

Specialized allocators for performance-critical scenarios:

### Memory Pools
- Pre-allocated memory chunks
- Fast allocation/deallocation
- Reduced fragmentation
- Fixed-size allocation patterns

### Arena Allocators
- Bulk allocation and deallocation
- Temporary memory management
- Reduced allocation overhead
- Suitable for short-lived objects

### Cache-Aligned Allocators
- Alignment for optimal cache performance
- Padding to cache line boundaries
- Improved memory access patterns
- Reduced false sharing
