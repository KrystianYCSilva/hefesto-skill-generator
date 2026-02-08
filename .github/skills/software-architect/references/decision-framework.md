# Decision Framework

## Architecture Decision Records (ADR)
Document *why* you chose an architecture.

**Template**:
-   **Title**: Short description.
-   **Status**: Proposed/Accepted/Deprecated.
-   **Context**: What is the problem? Constraints?
-   **Decision**: What are we doing?
-   **Consequences**: Pros/Cons/Risks accepted.

## Fitness Functions
Automated tests that verify architectural characteristics.
-   *Example*: "Cyclomatic complexity must not exceed 10."
-   *Example*: "Domain layer must not depend on Web layer." (ArchUnit).

## CAP Theorem Checklist
For distributed data:
-   **Consistency**: Every read receives the most recent write.
-   **Availability**: Every request receives a response (non-error).
-   **Partition Tolerance**: System continues to operate despite message loss.
*Pick two.* (Usually P + A or P + C).
