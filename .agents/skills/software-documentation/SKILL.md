---
name: software-documentation
description: |
  Create and maintain software documentation using UML, requirement specs, and modern documentation-as-code tactics.
  Use when: documenting requirements, designing system architecture with UML, or creating maintenance guides.
---

# Software Documentation

Effective documentation bridges the gap between stakeholder vision and technical implementation. It focuses on "why" and "how" the system behaves.

## How to document Requirements

Differentiate requirements by scope:

-   **Functional**: What the system *does* (e.g., "User can login with email").
-   **Non-Functional (Quality/Technical)**: How *well* it does it (e.g., "Login response < 200ms", "Data encrypted at rest").
-   **Business**: High-level goals (e.g., "Increase user retention by 10%").

> See [Requirements Template](references/requirements-template.md) for a standard IEEE 830 structure.

## UML 2.5 Diagram Reference

UML 2.5 defines 14 diagram types. **Bold** indicates the most essential diagrams for modern development.

### Structural Diagrams (Static)
*Represent the system's static structure and composition.*

| Diagram | Usage |
|---------|-------|
| **Class** | The backbone of OOP. Shows classes, attributes, methods, and relationships. Use for DB schema or code structure. |
| **Component** | Shows wiring of high-level modules/services. Use for architectural overview and microservices. |
| **Deployment** | Shows hardware/nodes and artifacts. Use for infrastructure, cloud mapping, and topology. |
| Object | Shows specific instances of classes at a point in time. Use for debugging complex states. |
| Package | Shows logical grouping of elements. Use for dependency management and layer organization. |
| Composite Structure | Shows internal structure of a class/component. Use for complex internal wiring. |
| Profile | Defining custom stereotypes/extensions. Use only for metamodeling. |

### Behavioral Diagrams (Dynamic)
*Represent the system's dynamic behavior and interactions.*

| Diagram | Usage |
|---------|-------|
| **Sequence** | Interaction over time. Use for API calls, auth flows, complex logic chains. |
| **Use Case** | System features from user perspective. Use for scoping features with stakeholders. |
| **Activity** | Workflow logic (like flowcharts). Use for business processes or algorithm steps. |
| **State Machine** | Object lifecycle. Use for status transitions (e.g., Order: Pending -> Paid -> Shipped). |
| Communication | Like Sequence, but focuses on links between objects. Use rarely (Sequence is usually clearer). |
| Timing | Interactions with precise timing constraints. Use for embedded/real-time systems. |
| Interaction Overview | Mix of Activity and Sequence. Use for high-level flow control. |

## How to model Use Cases

Use cases capture the "contract" between user and system.

1.  **Actor**: Who initiates it? (e.g., `Admin`).
2.  **Goal**: What do they want? (e.g., `Reset Password`).
3.  **Main Flow (Happy Path)**: Step-by-step success scenario.
4.  **Alternative Flows**: Edge cases and error handling.
5.  **Pre/Post-conditions**: State before and after execution.

## How to apply Modern Tactics

Move from "Write Once, Read Never" to "Living Documentation".

-   **Docs-as-Code**: Store docs in Git (Markdown/AsciiDoc) alongside code.
-   **C4 Model**: Use Context, Container, Component, Code levels instead of raw UML for architecture.
-   **ADR (Architecture Decision Records)**: Capture *decisions* (why we chose X over Y), not just the result.
-   **Mermaid.js**: Generate diagrams from text to keep them version-controllable.

## Common Pitfalls

| Issue | Impact | Fix |
|-------|--------|-----|
| **Stale Docs** | Misleads developers; destroys trust. | Automate diagram generation; review docs in PRs. |
| **Over-Documentation** | Hard to read; high maintenance. | Document *why* (decisions), not *what* (code usually explains itself). |
| **Ambiguity** | "Fast", "User-friendly". | Use measurable metrics ("< 100ms", "3 clicks max"). |

## Examples

### Example: Use Case Diagram (Mermaid)

**Input:** "A Customer buys a Product."

**Output:**
```mermaid
useCaseDiagram
    actor Customer
    usecase "Buy Product" as UC1
    Customer --> UC1
```

### Example: Functional Requirement

**Bad**: "The system should be fast."
**Good**: "The search API must return results within 200ms for 95% of requests under 100 RPS load."

## References

-   [UML 2.5 Specification](https://www.omg.org/spec/UML/)
-   [C4 Model](https://c4model.com/)
-   [Arc42 Template](https://arc42.org/)
