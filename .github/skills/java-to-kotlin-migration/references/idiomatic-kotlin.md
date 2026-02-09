# Idiomatic Kotlin Patterns

## Scope Functions

-   **`let`**: Execute code on non-null object. `obj?.let { it.run() }`. Returns block result.
-   **`apply`**: Configure object. `User().apply { name = "John" }`. Returns object.
-   **`also`**: Side effects (logging). `User().also { log(it) }`. Returns object.
-   **`run`**: Combination of `with` and `let`. `obj.run { this.calculate() }`. Returns block result.

## Data Classes

Replace POJOs with `data class`. Get `equals`, `hashCode`, `toString`, `copy` for free.

```kotlin
data class User(val id: Int, val name: String)
```

## Extension Functions

Add functionality to existing classes without inheritance.

```kotlin
fun String.toSlug(): String = this.toLowerCase().replace(" ", "-")
```
