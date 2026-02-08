# Calling Kotlin from Java

## Package-Level Functions
Kotlin top-level functions in `Utils.kt` compile to a Java class `UtilsKt`.
-   **Kotlin**: `fun doSomething()` in `org.example.Utils.kt`
-   **Java**: `org.example.UtilsKt.doSomething()`
-   **Custom Name**: Use `@file:JvmName("StringUtils")` at top of Kotlin file to change class name.

## Instance Fields vs Properties
Kotlin properties generate getter/setter.
-   `val x = 1` -> `getX()`
-   **Fix**: Use `@JvmField` to expose as `public final int x`.

## Companion Objects
Access via `.Companion` field unless annotated.
-   **Default**: `MyClass.Companion.doStatic()`
-   **With @JvmStatic**: `MyClass.doStatic()`

## Checked Exceptions
Kotlin has no checked exceptions. Java requires declaration to catch.
-   **Issue**: Java compiler won't let you catch `IOException` if not declared.
-   **Fix**: Annotate Kotlin function with `@Throws(IOException::class)`.
