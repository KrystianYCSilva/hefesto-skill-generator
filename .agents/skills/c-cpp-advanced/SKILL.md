---
name: c-cpp-advanced
description: |
  Expert guide for advanced C/C++ development focusing on high-performance algorithms, memory management, and system-level programming.
  Use when: designing complex systems, optimizing performance, managing memory efficiently, or building high-performance applications in C/C++.
---

# Advanced C/C++ Development

This skill targets senior-level development, focusing on advanced memory management, high-performance algorithms, system-level programming, and optimization techniques for building cutting-edge applications.

## How to implement advanced memory management

Efficient memory management is crucial for high-performance C/C++ applications.

- **RAII (Resource Acquisition Is Initialization)**: Tie resource lifetime to object lifetime. Resources are acquired during object construction and released during destruction.
- **Smart Pointers**: Use modern C++ memory management tools.
  - `std::unique_ptr`: Exclusive ownership with zero-cost abstraction.
  - `std::shared_ptr`: Shared ownership using reference counting.
  - `std::weak_ptr`: Break circular references in shared ownership.
- **Custom Allocators**: Implement specialized allocators for performance-critical scenarios.
  - Memory pools for frequent allocations/deallocations.
  - Arena allocators for temporary bulk allocations.
  - Cache-aligned allocators for performance optimization.
- **Move Semantics**: Leverage move constructors and assignment operators to transfer resources efficiently without copying.

## How to optimize performance with low-level techniques

Apply system-level optimizations for maximum performance.

- **Memory Layout Optimization**: Improve cache locality.
  - Structure of Arrays (SoA) vs Array of Structures (AoS) for vectorization.
  - Data alignment using `alignas` and cache line padding.
  - False sharing elimination in multi-threaded contexts.
- **Compiler Optimizations**: Leverage modern compiler capabilities.
  - Profile-guided optimization (PGO) and link-time optimization (LTO).
  - Use `const`, `constexpr`, and `restrict` keywords appropriately.
  - Enable vectorization with `-ftree-vectorize` (GCC) or `/arch:AVX` (MSVC).
- **Assembly-Level Optimizations**: For critical sections.
  - Inline assembly for platform-specific optimizations.
  - Intrinsics for SIMD operations (SSE, AVX, NEON).
  - Atomic operations for lock-free programming.

## How to design high-performance algorithms

Build algorithms optimized for speed and memory efficiency.

- **Algorithm Complexity**: Focus on cache complexity alongside time complexity.
  - Cache-aware algorithms that consider memory hierarchy.
  - Cache-oblivious algorithms that perform well across different cache sizes.
- **Data Structures**: Choose structures optimized for your access patterns.
  - Use `std::vector` over `std::list` in most cases (better cache locality).
  - Consider flat containers (`std::flat_map`, `std::flat_set`) for better performance.
  - Custom structures for domain-specific optimizations.
- **Concurrency Patterns**: Leverage multi-core architectures.
  - Lock-free data structures using atomic operations.
  - Work-stealing schedulers for task-based parallelism.
  - Thread-local storage to minimize synchronization overhead.

## How to build advanced applications

Apply advanced techniques to real-world application development.

- **System Programming**: Direct OS interface for maximum control.
  - Memory-mapped files (mmap) for large dataset processing.
  - Asynchronous I/O (epoll, kqueue, IOCP) for high-throughput servers.
  - Real-time scheduling policies for deterministic behavior.
- **Embedded and Performance-Critical Systems**: Resource-constrained optimization.
  - Static memory allocation to avoid dynamic allocation overhead.
  - Compile-time computations using `constexpr` and templates.
  - Zero-allocation patterns for real-time guarantees.
- **High-Frequency Applications**: Microsecond-level optimization.
  - CPU affinity and NUMA-aware allocation.
  - Preemption mitigation techniques.
  - Deterministic garbage collection strategies.

## Common Warnings & Pitfalls

### Memory Management Issues
- **Use-after-Free**: Accessing memory after deallocation. Use smart pointers to prevent.
- **Double Deletion**: Deleting the same memory twice. RAII prevents most cases.
- **Memory Leaks**: Not deallocating memory. Use tools like Valgrind or AddressSanitizer.

### Performance Pitfalls
- **Pessimization**: Over-optimizing early. Profile first, optimize later.
- **False Sharing**: Multiple threads modifying variables on the same cache line.
- **Cache Misses**: Poor memory access patterns causing performance degradation.

### Undefined Behavior
- **Unaligned Access**: Accessing misaligned data on architectures that don't support it.
- **Integer Overflow**: In signed arithmetic, overflow causes undefined behavior.
- **Lifetime Issues**: Using objects after their lifetime ends.

## Advanced References

- **Memory Management Deep Dive**: See [MEMORY-MANAGEMENT.md](references/memory-management.md).
- **Performance Optimization Techniques**: See [PERFORMANCE.md](references/performance.md).
- **System Programming Patterns**: See [SYSTEM-PROGRAMMING.md](references/system-programming.md).
- **Concurrency and Parallelism**: See [CONCURRENCY.md](references/concurrency.md).

## References

- [ISO C++ Standard](https://eel.is/c++draft/)
- [CppReference.com](https://en.cppreference.com/w/)
- [Agner Fog's Optimization Manuals](https://www.agner.org/optimize/)
- [Effective Modern C++ by Scott Meyers](https://www.aristeia.com/books.html)