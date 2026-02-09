---
name: java-to-kotlin-migration
description: |
  Guide refactoring from Java to Kotlin, leveraging interoperability and modern language features safely.
  Use when: migrating legacy Java codebases, introducing Kotlin to Java projects, or debugging interoperability issues.
---

# Java to Kotlin Migration

Kotlin is designed to be 100% interoperable with Java. This skill guides the safe, incremental migration of legacy systems without breaking existing functionality.

## How to Plan the Migration

Don't rewrite everything at once. Use a "Strangler Fig" approach at the file level.

1.  **Bottom-Up**: Start with "leaf" nodes (Data Classes, DTOs, Utilities) that have few dependencies.
2.  **Test-First**: Ensure the Java class has high test coverage before converting.
3.  **Auto-Convert & Review**: Use IntelliJ's "Convert Java File to Kotlin" (Ctrl+Alt+Shift+K), but *never* commit the result blindly.
    -   *Review Nullability*: The converter often guesses `String?` vs `String`. Verify against business logic.
    -   *Review Mutability*: Prefer `val` over `var` where possible.

## How to Handle Nullability (The Billion Dollar Mistake)

Kotlin's type system distinguishes nullable vs non-nullable. Java does not.

-   **Platform Types (`T!`)**: Types coming from Java are "unknown" (`String!`). Treat them as nullable (`String?`) until proven otherwise.
-   **Annotations**: Add `@Nullable` / `@NotNull` to Java code *before* converting to help the Kotlin compiler.
-   **Defensive Checks**: Use `?.let {}` or `?:` (Elvis operator) at the boundary layer to sanitize inputs.

## How to Leverage Kotlin Features

Don't just write "Java in Kotlin syntax".

| Java Pattern | Kotlin Replacement | Benefit |
|--------------|--------------------|---------|
| `getFoo()`, `setFoo()` | Properties (`val foo`) | Concise syntax, backing fields handled automatically. |
| `static` Util Methods | Top-level functions / Extensions | Better discoverability, cleaner call sites (`string.isValid()`). |
| `Builder` Pattern | `apply {}`, Named Arguments | No boilerplate code needed for object construction. |
| `instanceof` + Cast | Smart Casts (`is String`) | Compiler automatically casts after check. |
| `switch` | `when` (Exhaustive) | Forces handling of all enum/sealed class cases. |

> See [Idiomatic Kotlin](references/idiomatic-kotlin.md) for deeper patterns like Scoped Functions and Coroutines.

## Common Interop Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| **JvmStatic Missing** | Java can't see Kotlin `companion object` methods. | Annotate with `@JvmStatic` or `@JvmField` for static visibility. |
| **Lombok Erasure** | Kotlin compiler runs *before* Lombok generates code. | Delombok Java code before converting, or define explicit getters/setters in Java first. |
| **Checked Exceptions** | Kotlin has no checked exceptions. | Java callers won't be forced to catch exceptions from Kotlin. Add `@Throws` annotation if Java relies on it. |

## Examples

### Example: Converting a Singleton

**Java:**
```java
public class Config {
    private static Config instance;
    private Config() {}
    public static synchronized Config getInstance() { ... }
}
```

**Kotlin (Idiomatic):**
```kotlin
object Config {
    // Thread-safe singleton by default
}
```

### Example: Handling Nulls

**Java Input:**
```java
public String format(String input) {
    if (input == null) return "Default";
    return input.trim();
}
```

**Kotlin Refactor:**
```kotlin
fun format(input: String?): String = input?.trim() ?: "Default"
```

## References

-   [Official Java Interop Guide](https://kotlinlang.org/docs/java-interop.html)
-   [Converting Java to Kotlin (JetBrains)](https://kotlinlang.org/docs/java-to-kotlin-interop.html)
-   [Idiomatic Kotlin Patterns](references/idiomatic-kotlin.md)
