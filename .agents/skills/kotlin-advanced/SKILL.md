---
name: kotlin-advanced
description: |
  Expert guide for high-performance Kotlin development focusing on advanced concurrency, multiplatform architecture, and compiler internals.
  Use when: designing complex systems, optimizing performance, implementing KMP, or deep-diving into coroutines.
---

# Advanced Kotlin Development

This skill targets senior-level development, focusing on Coroutines internals, Kotlin Multiplatform (KMP) architecture, compiler plugins (KSP), and functional patterns with Arrow.

## How to architect Multiplatform Systems (KMP)

Share logic effectively across Android, iOS, Web, and Desktop.

- **Architecture**: Clean Architecture works best.
  - `Domain` (Pure Kotlin): Use `commonMain`. No platform dependencies.
  - `Data` (Repositories): Implement interfaces defined in Domain. Use `expect/actual` for platform-specific drivers (SQLDelight, Ktor Client).
  - `Presentation`: Shared ViewModels (KMP-ViewModel) or Compose Multiplatform for UI.
- **Dependency Injection**: Use Koin or Kodein (Runtime) or Kotlin-Inject (Compile-time) for graph management in common code.

## How to master Structured Concurrency

Go beyond basic `launch`.

- **Scope Management**: Always tie coroutines to a lifecycle. Use `coroutineScope` to decompose parallel work safely.
- **Exception Handling**: Exceptions in child coroutines cancel the parent. Use `SupervisorJob` or `supervisorScope` if siblings should survive failures.
- **Flow Control**: Use `Flow` for cold streams. Prefer `StateFlow` (hot, state-holder) over `LiveData` or `RxJava`.
- **Select Expression**: Use `select` to await multiple suspending functions/channels simultaneously.

## How to leverage Compiler Features

Use the compiler to enforce correctness and reduce boilerplate.

- **KSP (Kotlin Symbol Processing)**: Write lightweight compiler plugins for code generation. Faster than KAPT.
- **Inline Classes (Value Classes)**: `value class Password(val s: String)`. Wraps a type without runtime allocation overhead.
- **Contracts**: Inform the compiler about function behavior (`contract { returns() implies (x != null) }`).

## Common Warnings & Pitfalls

### Coroutine Leaks
- **Issue**: Using `GlobalScope` or not cancelling scopes.
- **Fix**: Bind to `viewModelScope`, `lifecycleScope`, or manage a custom `CoroutineScope` tied to component lifecycle.

### Generic Erasure
- **Issue**: JVM erases generics at runtime (`List<String>` becomes `List`).
- **Fix**: Use `inline fun <reified T>` to preserve type information.

### KMP Interop
- **Issue**: Kotlin features (Suspend functions, Sealed classes) map awkwardly to Obj-C/Swift.
- **Fix**: Use SKIE (Swift Kotlin Interface Enhancer) to generate better Swift bindings.

## Applicability & Ecosystem

- **Backend**: Ktor (Asynchronous), Spring Boot (Enterprise), Quarkus/Micronaut (Cloud Native).
- **Frontend**: Kotlin/JS (React wrappers), Compose for Web (Canvas/Wasm).
- **Mobile**: Android (Native), KMP (Cross-platform logic).
- **Tooling**: Gradle Kotlin DSL is the standard build script format.

## Advanced References

- **Architecture & KMP**: See [ARCHITECTURE.md](references/architecture.md).
- **Coroutines Deep Dive**: See [COROUTINES.md](references/coroutines.md).
- **Compiler & Metaprogramming**: See [COMPILER.md](references/compiler.md).
- **Ecosystem & Libraries**: See [ECOSYSTEM.md](references/ecosystem.md).
- **Full Stack Development**: See [STACK.md](references/stack.md).

## References

- [Kotlin Coroutines Core](https://github.com/Kotlin/kotlinx.coroutines)
- [Kotlin Multiplatform Mobile Docs](https://kotlinlang.org/docs/multiplatform.html)
- [Arrow (Functional Kotlin)](https://arrow-kt.io/)
- [SKIE (Swift Interop)](https://touchlab.co/skie)
