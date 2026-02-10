---
name: architecture
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Advanced Kotlin Architecture

## Clean Architecture with KMP

### Layer Separation
1.  **Domain (commonMain)**:
    -   Entities (Data Classes)
    -   Use Cases (Interactors)
    -   Repository Interfaces
    -   *No framework dependencies.*

2.  **Data (commonMain + platform sources)**:
    -   Repository Implementations
    -   Remote Data Sources (Ktor)
    -   Local Data Sources (SQLDelight/Room)
    -   Mappers (DTO -> Domain)

3.  **Presentation (commonMain/platform)**:
    -   State Holders (ViewModels/Blocs)
    -   UI (Compose Multiplatform or Native SwiftUI/Jetpack Compose)

## MVI (Model-View-Intent)
Preferred pattern for reactive UIs (Compose).
-   **State**: Immutable data class representing the UI.
-   **Intent**: User actions.
-   **Reducer**: Pure function `(State, Intent) -> State`.
-   **Side Effects**: One-off events (Navigation, Toasts) via `Channel`.

## Functional Architecture (Arrow)
-   **Error Handling**: Replace `try-catch` with `Either<Failure, Success>`.
-   **Dependency Injection**: Use Reader Monad or simple constructor injection.
-   **Validation**: Use `Validated` or `Ior` types.

