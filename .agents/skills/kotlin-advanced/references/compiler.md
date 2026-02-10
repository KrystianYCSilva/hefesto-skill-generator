---
name: compiler
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Compiler & Metaprogramming

## Kotlin Symbol Processing (KSP)
API to parse Kotlin code and generate new files.
-   **Why**: Access to type info that KAPT (Java AP) misses. 2x faster build times.
-   **Usage**: Create a `SymbolProcessorProvider`.
-   **Limitation**: Cannot *modify* existing code, only generate new files.

## Inline & Value Classes
-   **`inline class` (Deprecated)** -> **`value class`**.
-   **Optimization**: Wraps a primitive or object without heap allocation (mostly).
-   **Rules**: Single `val` property. No `init` block (until Kotlin 2.0?).

## Contracts
Tell the compiler about code effects.
```kotlin
@OptIn(ExperimentalContracts::class)
fun require(condition: Boolean) {
    contract {
        returns() implies condition
    }
    if (!condition) throw IllegalArgumentException()
}
```
Allows the compiler to know that if `require(x != null)` returns, `x` is safe to cast.

## Compiler Plugins
-   **All-Open**: Makes classes `open` for Spring.
-   **No-Arg**: Generates zero-argument constructor for JPA.
-   **Serialization**: Generates `serializer()` implementation.

