# Kotlin Ecosystem & Libraries

Standard toolkit for effective Kotlin development.

## Core Libraries
-   **kotlinx-coroutines**: Concurrency primitives.
-   **kotlinx-serialization**: JSON/ProtoBuf serialization. Reflection-less, KMP supported. Preferred over Jackson for KMP.
-   **kotlinx-datetime**: Multiplatform Date/Time types.

## Testing
-   **Mockk**: The standard for Kotlin mocking. First-class support for coroutines (`coEvery`, `coVerify`) and extension functions. Replaces Mockito.
-   **Kotest**: Powerful testing framework + assertion library. Supports Behavior Spec (BDD), Property-based testing.
-   **Turbine**: Small library for testing Flows. `flow.test { assertEquals(item, awaitItem()) }`.

## Networking
-   **Ktor**: Pure Kotlin, coroutine-first, multiplatform. Client & Server.
-   **Retrofit**: JVM/Android standard. Uses reflection. Good for Java interop.

## Persistence
-   **SQLDelight**: Generates typesafe Kotlin APIs from SQL statements. KMP ready.
-   **Room**: Google's ORM. Android-first, moving to KMP.
-   **Exposed**: JetBrains' SQL DSL. JVM only. Lightweight.

## Dependency Injection
-   **Koin**: Service Locator (DSL based). Runtime resolution. Easy setup.
-   **Kodein**: Similar to Koin, lazy loading.
-   **Kotlin-Inject**: Compile-time (KSP). Similar to Dagger but for KMP.
-   **Dagger/Hilt**: Annotation processing. Android/JVM standard. Complex.
