---
name: software-architect
description: |
  Expert guide for designing, evaluating, and refactoring software architectures. Covers Hexagonal, Event-Driven, Layered, and Microservices patterns, plus trade-off analysis and evolutionary architecture.
  Use when: starting a new project, refactoring legacy systems, choosing architectural patterns, or analyzing system trade-offs.
---

# Software Architect Expert

Software Architecture is about making the expensive decisions. It defines the structure, behavior, and relationships of a system's components. This skill guides you through choosing, mixing, and fixing architectures.

## How to choose an Architectural Pattern

There is no "best" architecture, only the least worst for your specific context (Trade-offs).

-   **Layered (N-Tier)**: Simple, standard. Good for CRUD apps. *Risk*: Database-driven design, tight coupling.
-   **Hexagonal (Ports & Adapters)**: Decoupled domain logic. Good for complex business rules. *Risk*: Complexity overhead.
-   **Event-Driven (EDA)**: Highly decoupled, scalable. Good for async workflows. *Risk*: Consistency, debugging difficulty.
-   **Microservices**: Independent deployment, team autonomy. Good for large orgs. *Risk*: Distributed system complexity (Network, Latency).

## How to analyze Trade-offs (Trade-off Analysis)

Every decision has a cost. Use **ATAM** (Architecture Trade-off Analysis Method) concepts.

-   **Scalability** vs **Complexity**
-   **Consistency** vs **Availability** (CAP Theorem)
-   **Development Speed** vs **Maintainability**

## How to reorganize Legacy Code (Refactoring)

When architecture is broken ("Big Ball of Mud"):

1.  **Identify Boundaries**: Find "Seams" in the code where modules can be separated.
2.  **Strangler Fig Pattern**: Build new features in a new architecture, slowly killing the old system.
3.  **Dependency Breaking**: Invert dependencies to stop high-level policy from depending on low-level details.

## Common Warnings & Pitfalls

### Resume-Driven Development
-   **Issue**: Choosing tech because it's trendy (e.g., Microservices for a startup).
-   **Fix**: Choose boring technology. Solve business problems, not technical vanity.

### Distributed Monolith
-   **Issue**: Microservices that share a database or must be deployed together.
-   **Fix**: Ensure shared-nothing architecture or revert to a Modular Monolith.

### Over-Engineering
-   **Issue**: Applying Hexagonal Architecture to a simple "Hello World".
-   **Fix**: Match architectural complexity to domain complexity.

## Best Practices

| Principle | Meaning |
|-----------|---------|
| **Loose Coupling** | Changes in module A shouldn't break module B. |
| **High Cohesion** | Code that changes together should stay together. |
| **Evolutionary** | Architecture should support change, not prevent it. |

## Deep Dives

-   **Patterns Deep Dive**: See [PATTERNS.md](references/patterns.md).
-   **Decision Framework**: See [DECISION.md](references/decision-framework.md).
-   **Refactoring Strategy**: See [REFACTORING.md](references/refactoring.md).

## References

-   [Fundamentals of Software Architecture (Richards/Ford)](https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/)
-   [Architecture Patterns with Python (Percival/Gregory)](https://www.cosmicpython.com/)
-   [The C4 Model](https://c4model.com/)
