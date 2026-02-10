---
name: java-kotlin-interop
description: |
  Expert guide for Java-Kotlin interoperability, migration strategies, and build system configuration.
  Use when: mixing Java and Kotlin in the same project, migrating legacy Java to Kotlin, or debugging interop issues.
---

# Java & Kotlin Interoperability

Kotlin is designed with Java interoperability as a core feature. This skill covers advanced techniques for seamless integration, build configuration (Gradle/Maven), and pitfalls to avoid in mixed-language projects.

## How to manage Interop Fundamentals

Kotlin compiles to JVM bytecode, making it 100% interoperable with Java.

- **Calling Java from Kotlin**: Generally seamless. Java getters/setters map to Kotlin properties (`obj.name` instead of `obj.getName()`).
- **Calling Kotlin from Java**: Kotlin features (properties, top-level functions, default args) map to static methods or special JVM names.
- **Null Safety**: Java types are "platform types" (`String!`) in Kotlin. Treat them as nullable (`String?`) unless annotated with `@Nullable`/`@NonNull`.

## How to configure Build Systems

Mixed projects require specific plugins to compile both languages.

- **Gradle (Kotlin DSL)**:
  - Apply `org.jetbrains.kotlin.jvm` plugin.
  - Standard source sets: `src/main/java` and `src/main/kotlin`.
  - **Best Practice**: Configure `kapt` or `ksp` if using annotation processors (Lombok, MapStruct).
- **Maven**:
  - Add `kotlin-maven-plugin`.
  - Configure `<execution>` steps to compile Kotlin *before* Java (so Java can see Kotlin classes).

## Common Warnings & Pitfalls

### Lombok Compatibility
- **Issue**: Lombok generates code at compile-time (APT). Kotlin compiler runs *before* Java compiler sees generated methods.
- **Fix**: Use `kapt` or delombok. **Better Fix**: Replace Lombok with Kotlin Data Classes.

### Default Arguments
- **Issue**: Java doesn't support default arguments.
- **Fix**: Annotate Kotlin function with `@JvmOverloads` to generate overloaded methods for Java consumers.

### Static Members
- **Issue**: Kotlin `companion object` members are not static in Java by default.
- **Fix**: Use `@JvmStatic` annotation to expose them as true static methods.

## Best Practices (Migration Strategy)

1.  **Test First**: Ensure unit tests pass before converting.
2.  **Small Chunks**: Migrate Data Transfer Objects (DTOs) first (Data Classes).
3.  **Utilities**: Convert utility classes to top-level functions.
4.  **Business Logic**: Migrate services/controllers last.
5.  **Stop & Refactor**: After `Ctrl+Alt+Shift+K` (auto-convert), manually clean up `!!` assertions and nullable types.

## Deep Dives

- **Calling Java from Kotlin**: See [CALLING-JAVA.md](references/calling-java.md).
- **Calling Kotlin from Java**: See [CALLING-KOTLIN.md](references/calling-kotlin.md).
- **Build Configuration**: See [BUILD-SYSTEMS.md](references/build-systems.md).

## References

- [Kotlin Java Interop Guide](https://kotlinlang.org/docs/java-interop.html)
- [Gradle Kotlin Plugin Docs](https://kotlinlang.org/docs/gradle.html)
- [Maven Kotlin Plugin Docs](https://kotlinlang.org/docs/maven.html)
