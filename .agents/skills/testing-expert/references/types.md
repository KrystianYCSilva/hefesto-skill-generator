---
name: types
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Test Types Guide

## Unit Testing
-   **Scope**: Single function, method, or class.
-   **Dependencies**: Mocks/Stubs.
-   **Speed**: Milliseconds.
-   **Tools**: JUnit, NUnit, PyTest, Jest, Mocha.
-   **Goal**: Verify logic correctness.

## Integration Testing
-   **Scope**: Interaction between 2+ units or a unit and a real infrastructure (DB).
-   **Dependencies**: Real DB (Testcontainers), Wiremock for APIs.
-   **Speed**: Seconds to minutes.
-   **Goal**: Verify modules talk to each other correctly.

## End-to-End (E2E) Testing
-   **Scope**: The entire system from user perspective.
-   **Dependencies**: Full environment (Frontend + Backend + DB).
-   **Speed**: Minutes to hours.
-   **Tools**: Selenium, Cypress, Playwright.
-   **Goal**: Verify critical user flows (Login, Checkout).

