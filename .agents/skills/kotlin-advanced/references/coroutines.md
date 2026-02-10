---
name: coroutines
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Structured Concurrency & Flows

## Dispatchers
-   **Dispatchers.Main.immediate**: Execute immediately if on main thread (avoids re-dispatch).
-   **Dispatchers.IO**: Elastic thread pool (64+ threads) for blocking I/O.
-   **Dispatchers.Default**: CPU-bound pool (cores size).
-   **Dispatchers.Unconfined**: Starts in current thread, resumes in whatever thread the suspending function finished. *Dangerous.*

## Flow vs Channel
| Feature | Flow | Channel |
| :--- | :--- | :--- |
| **Type** | Cold (Lazy) | Hot (Eager) |
| **Multicast** | No (Use `SharedFlow`) | Yes (BroadcastChannel - Deprecated) |
| **Backpressure**| Automatic (Suspension) | Buffer capacity |
| **Use Case** | Data streams | IPC, Event Bus |

## Best Practices
-   **Avoid `withContext(Dispatchers.IO)` in repositories**: Let the caller decide the context? *NO*. Repositories should be "main-safe", so DO use `withContext`.
-   **Exception Handling**: `catch` operator catches upstream exceptions. `try-catch` around collection works too.
-   **Testing**: Use `runTest` (kotlinx-coroutines-test). Replaces standard dispatchers with `TestDispatcher`.

