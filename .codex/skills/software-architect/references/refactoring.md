# Refactoring & Migration Strategy

## The Strangler Fig Pattern
1.  **Intercept**: Put a proxy/gateway in front of the legacy system.
2.  **Route**: Direct specific traffic (e.g., `/api/v2/users`) to the new service.
3.  **Migrate**: Gradually move functionality from Legacy to New.
4.  **Eliminate**: Once Legacy is empty, shut it down.

## Bubble Context Pattern
When extracting a new model from a legacy mess:
1.  Create an **Anticorruption Layer (ACL)**.
2.  Protect the new clean model from the legacy model's influence.
3.  Translate data at the boundary.

## Tactical Patterns
-   **Extract Class**: Move logic to new class.
-   **Invert Dependency**: Change `Service -> Repository` to `Service -> Interface <- Repository`.
-   **Feature Toggles**: Hide new architectural changes behind flags until stable.
