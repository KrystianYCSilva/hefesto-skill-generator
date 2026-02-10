---
name: performance
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# JVM Performance Engineering

## JIT Optimization Techniques
- **Inlining**: The most important optimization. Keep methods small (< 325 bytes bytecode).
- **Loop Unrolling**: Compiler creates multiple copies of loop body to reduce overhead.
- **Escape Analysis**: Allocates objects on stack (scalar replacement) if they don't escape the method.

## Memory Model (JMM)
- **Happens-Before**: Understanding `volatile`, `synchronized`, and `final` semantics is crucial for lock-free programming.
- **False Sharing**: Cache line contention. Pad objects using `@Contended` (Java 8+) to prevent threads fighting over cache lines.

## Tools
- **JMH (Java Microbenchmark Harness)**: The ONLY valid way to micro-benchmark Java code.
- **JOL (Java Object Layout)**: Inspect object memory footprint and layout.
- **Async-profiler**: Low-overhead sampling profiler that avoids "Safepoint bias".

