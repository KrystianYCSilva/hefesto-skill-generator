---
name: software-engineering-concepts
description: |
  Master core software engineering principles, SDLC models, and planning strategies from Waterfall to Agile.
  Use when: planning projects, choosing development methodologies, or reviewing engineering best practices.
---

# Software Engineering Concepts

Software Engineering is the application of systematic, disciplined, and quantifiable approaches to the development, operation, and maintenance of software.

## How to Apply the SDLC

The Software Development Life Cycle (SDLC) defines the stages a project passes through.

1.  **Requirements Analysis**: Gathering and documenting what the system must do (Functional/Non-Functional).
2.  **Design**: Defining the architecture, data models, and interfaces (High-Level vs. Low-Level).
3.  **Implementation**: Coding based on design specifications.
4.  **Testing**: Verifying that code meets requirements (Unit, Integration, System, UAT).
5.  **Deployment**: releasing to production environments.
6.  **Maintenance**: Fixing bugs, updating features, and retiring legacy systems.

## How to Choose a Process Model

Select a model based on project clarity and stability requirements.

| Model | Description | Best For |
|-------|-------------|----------|
| **Waterfall** (Cascade) | Linear, sequential phases. Phase $N$ must finish before $N+1$ starts. | Critical systems (Medical, Aerospace) with fixed requirements. |
| **Incremental** | Build core features first, then add layers in subsequent releases. | Products needing early market entry with basic functionality. |
| **Iterative** | Repeat the cycle (Analyze->Design->Code->Test) to refine the system. | Projects with vague initial requirements. |
| **Agile (Scrum/Kanban)** | Adaptive, collaborative, time-boxed iterations (Sprints). | Startups, SaaS, projects with rapidly changing needs. |
| **V-Model** | Extension of Waterfall where each dev phase has a corresponding test phase. | Safety-critical systems requiring strict validation. |

## How to Manage Technical Debt

Debt is the implied cost of additional rework caused by choosing an easy solution now instead of a better approach that would take longer.

-   **Inadvertent Debt**: Caused by lack of knowledge ("We didn't know better").
-   **Deliberate Debt**: "We must ship for the demo, we'll fix it later."
-   **Bit Rot**: Code decays over time as dependencies and standards evolve.
-   **Strategy**: Allocate 20% of every sprint to refactoring and debt repayment.

## Key Principles (SOLID & GRASP)

> See [Design Principles](references/design-principles.md) for detailed explanations of SOLID, DRY, KISS, and YAGNI.

## Common Anti-Patterns

| Anti-Pattern | Description | Fix |
|--------------|-------------|-----|
| **Big Ball of Mud** | A system with no distinguishable architecture. | Apply modularity, separation of concerns, and gradual refactoring. |
| **Gold Plating** | Adding features no one asked for. | Stick to requirements; use MVP approach. |
| **Brooks' Law** | "Adding manpower to a late project makes it later." | onboard carefully; focus on communication overhead. |

## Examples

### Example: Choosing a Model

**Scenario**: Building a flight control system for a new aircraft.
**Decision**: **V-Model**.
**Reasoning**: Requirements are fixed by regulation. Testing must be rigorous and correspond strictly to design phases. Cost of failure is catastrophic.

**Scenario**: A social media app for a new niche market.
**Decision**: **Agile (Scrum)**.
**Reasoning**: User feedback is unknown. Features need to evolve based on metrics. Speed to market is critical.

## References

-   [SWEBOK Guide (IEEE)](https://www.computer.org/education/bodies-of-knowledge/software-engineering)
-   [The Mythical Man-Month (Fred Brooks)](https://en.wikipedia.org/wiki/The_Mythical_Man-Month)
-   [Design Principles](references/design-principles.md)
