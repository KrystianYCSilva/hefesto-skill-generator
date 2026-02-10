---
name: advanced
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Advanced Kotlin Techniques

## Asynchronous Programming (Coroutines)
- **Suspend Functions**: Functions that can pause and resume (`suspend fun fetchData()`).
- **Dispatchers**: `IO` (network/disk), `Main` (UI), `Default` (CPU heavy).
- **Flow**: Cold asynchronous stream of data (Reactive Streams implementation).
- **Channels**: Hot stream for communication between coroutines.

## Delegation
- **Property Delegation**: `by lazy`, `by observable`, or custom delegates (`ReadWriteProperty`).
- **Class Delegation**: `class Derived(b: Base) : Base by b`. Avoids boilerplate wrappers.

## Metaprogramming & Generics
- **Reified Types**: Access generic type at runtime in inline functions (`inline fun <reified T> isType(a: Any)`).
- **Variance**: `in` (contravariant) and `out` (covariant) for type safety.
- **KSP (Kotlin Symbol Processing)**: Lightweight alternative to KAPT for annotation processing.

## Kotlin Multiplatform (KMP)
- **Source Sets**: `commonMain`, `androidMain`, `iosMain`.
- **Expect/Actual**: Define interface in `common`, implement in platform-specific sets.
- **Compose Multiplatform**: UI framework sharing code across Android, iOS, Desktop, Web.

