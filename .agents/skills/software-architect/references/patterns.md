---
name: patterns
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Architectural Patterns Guide

## Layered Architecture
Standard stack: Presentation -> Business -> Persistence -> Database.
-   **Pros**: Easy to learn, clear separation of concerns.
-   **Cons**: "Sinkhole" anti-pattern (requests pass through layers with no logic). Tends to coupling.

## Hexagonal (Ports & Adapters)
Isolates the domain.
-   **Core**: The Domain Logic (inside).
-   **Ports**: Interfaces defining how to talk to the Core.
-   **Adapters**: Implementations (Web Controller, SQL Repository) that plug into Ports.
-   **Pros**: Testability (swap DB for Mock), framework independence.
-   **Cons**: Lots of boilerplate (DTOs, Interfaces).

## Event-Driven Architecture (EDA)
Components communicate via events (Broker/Bus).
-   **Broker Topology**: Central hub (RabbitMQ, Kafka).
-   **Mediator Topology**: Orchestrator service.
-   **Pros**: High decoupling, reactive.
-   **Cons**: Eventual consistency is hard. Hard to trace flow.

## Modular Monolith
Single deployment unit, but strictly separated internal modules.
-   **Pros**: Easy deployment (like Monolith), good structure (like Microservices).
-   **Cons**: Enforcing boundaries requires discipline (or tools like ArchUnit).

