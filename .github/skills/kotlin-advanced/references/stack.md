# Full Stack Kotlin

Kotlin is viable for the entire stack.

## Backend (Server-Side)
-   **Ktor**: Lightweight, async. Best for microservices.
    ```kotlin
    embeddedServer(Netty, port = 8080) {
        routing {
            get("/") { call.respondText("Hello") }
        }
    }.start(wait = true)
    ```
-   **Spring Boot**: Excellent Kotlin support (extensions, reified types).
    -   Use `kapt` or `ksp` for metadata.
    -   Constructor injection works out of the box.

## Frontend (Web)
-   **Kotlin/JS**: Transpiles to JavaScript.
    -   **React Wrapper**: Write React components in Kotlin.
-   **Compose HTML**: DOM-building DSL.
-   **Compose Multiplatform (Web)**: Renders to Canvas (Skia). Pixel-perfect UI sharing with mobile/desktop.

## Shared Logic (KMP)
The "Secret Sauce" of Kotlin stack.
1.  Define API models in `commonMain` (kotlinx-serialization).
2.  Use these models in Backend (Ktor) and Frontend (Android/iOS/Web).
3.  Share validation logic and business rules.
4.  **Result**: Changes to API models propagate compilation errors to both client and server immediately.
