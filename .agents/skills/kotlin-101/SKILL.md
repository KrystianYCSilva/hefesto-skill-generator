---
name: kotlin-101
description: |
  Guide for Kotlin development covering paradigms, platforms, versions, and best practices.
  Use when: starting a new Kotlin project, migrating to Kotlin, exploring multiplatform capabilities, or reviewing code for idiomatic usage.
---

# Kotlin Fundamentals (Kotlin 101)

Kotlin is a modern, statically typed programming language that targets the JVM, Android, JavaScript, and Native. It is designed to be concise, safe, and fully interoperable with Java.

## How to apply programming paradigms

Kotlin is a multi-paradigm language. Leverage its features for expressive code.

### Object-Oriented Programming (OOP)
- **Classes & Objects**: Use `class` for blueprints, `object` for singletons/companions.
- **Properties**: Use `val` (read-only) and `var` (mutable). Automatic getters/setters.
- **Inheritance**: Classes are `final` by default. Use `open` to allow inheritance.
- **Data Classes**: Use `data class` for DTOs (automatic `equals`, `hashCode`, `toString`, `copy`).

### Functional Programming (FP)
- **Functions as First-Class Citizens**: Pass functions as parameters, return them.
- **Lambdas**: `{ args -> body }`. If the last arg is a lambda, move it outside parentheses.
- **Immutability**: Prefer `val` and immutable collections (`listOf`, `mapOf`).
- **Extension Functions**: Add functionality to existing classes without inheritance (`fun String.toSlug()`).

## Common Warnings & Pitfalls

### Null Safety
Kotlin's type system aims to eliminate NPEs.
- **Nullable Types**: `String?` can hold null.
- **Safe Calls**: `str?.length` returns length or null.
- **Elvis Operator**: `str?.length ?: 0` provides default value.
- **Not-null Assertion**: `!!` throws NPE if null. **Avoid** unless absolutely certain.

### Interoperability with Java
- **Platform Types**: Types from Java are "platform types" (`String!`). Treat them as nullable to be safe.
- **Keywords**: Escape Kotlin keywords used in Java with backticks (e.g., `Mockito.`when``).

### Coroutines
- **Blocking vs Suspending**: Never block a thread in a coroutine; use suspending functions.
- **Scope**: Ensure structural concurrency (use `coroutineScope`, `viewModelScope`). Avoid `GlobalScope`.

## Best Practices (Beginner to Expert)

| Level | Focus | Key Practices |
|-------|-------|---------------|
| **Beginner** | Idioms | Use `val` by default, `data classes`, expression bodies, string templates. |
| **Intermediate**| Safety & DSLs | Null safety discipline, Type-safe builders, `sealed classes` for state. |
| **Expert** | Multiplatform | `expect`/`actual` mechanism, Coroutines flow, Compiler plugins (KSP). |

## Application Areas

- **Android**: Google's preferred language for Android apps.
- **Backend (JVM)**: Spring Boot, Ktor, Quarkus.
- **Multiplatform (KMP)**: Share logic between iOS, Android, Web, and Desktop.
- **Data Science**: Jupyter notebooks with Kotlin kernel.

## Deep Dives

- **Version History**: See [VERSIONS.md](references/versions.md) for evolution (1.0 to present).
- **Target Platforms**: See [PLATFORMS.md](references/platforms.md) for JVM, JS, Native, and Wasm details.
- **Advanced Techniques**: See [ADVANCED.md](references/advanced.md) for coroutines, delegates, and KMP.

## References

- [Kotlin Official Documentation](https://kotlinlang.org/docs/home.html)
- [Kotlin Keep (Evolution Proposals)](https://github.com/Kotlin/KEEP)
- [Kotlin Coroutines Guide](https://kotlinlang.org/docs/coroutines-guide.html)
- [Google Android Kotlin Guides](https://developer.android.com/kotlin)
