# Calling Java from Kotlin

## Null Safety & Platform Types
Java types usually lack nullability info. Kotlin treats them as `T!` (Platform Type).
-   **Safe**: `val len = javaObj.string?.length`
-   **Risky**: `val len = javaObj.string.length` (Throws NPE if null)
-   **Fix**: Annotate Java code with `@Nullable` / `@NonNull` (JSR-305, JetBrains, Android, Lombok annotations).

## Getters and Setters
Kotlin treats Java bean methods as properties.
-   Java: `user.setName("Alice")` -> Kotlin: `user.name = "Alice"`
-   Java: `user.isActive()` -> Kotlin: `user.isActive`

## SAM Conversions (Single Abstract Method)
Kotlin automatically converts Java SAM interfaces (like `Runnable`) to lambdas.
```kotlin
// Java: executor.submit(new Runnable() { void run() { ... } });
executor.submit { println("Running") }
```

## Keywords
Escape Java identifiers that are Kotlin keywords.
`Mockito.`when`(mock)` -> Backticks required.
