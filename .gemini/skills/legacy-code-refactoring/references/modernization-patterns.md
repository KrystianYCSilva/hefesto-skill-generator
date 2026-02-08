# Modernization Patterns

## Strangler Fig Application

1.  **Identify**: Pick a small, isolated feature (e.g., "UserProfile").
2.  **Intercept**: Put a proxy (API Gateway) in front of the legacy system.
3.  **Route**: Direct "UserProfile" traffic to the new microservice; everything else to Legacy.
4.  **Repeat**: Pick the next feature.
5.  **Retire**: When Legacy is empty, turn it off.

## Anticorruption Layer (ACL)

When new code must talk to legacy code, don't let legacy models leak into the new domain.

-   **Adapter**: Converts New Interface -> Legacy Interface.
-   **Facade**: Simplifies complex legacy calls.
-   **Translator**: Converts Legacy Data -> New Data Model.

## Database Migration Strategies

-   **Expand-Contract**:
    1.  *Expand*: Add new column.
    2.  *Migrate*: Copy data (background job).
    3.  *Contract*: Remove old column.
