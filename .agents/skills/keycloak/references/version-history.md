---
name: version-history
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Version History and Usage Divergences

| Keycloak Version Line | Key Change | Practical Divergence |
|---|---|---|
| <= 16 | WildFly-based distribution | Admin and ops model tied to older runtime assumptions |
| >= 17 | Quarkus-based distribution | Startup/runtime/ops model changed; automation scripts required adaptation |

## Deep Divergence Notes

- Major version transitions usually combine runtime baseline upgrades and compatibility breaks.
- Validate transitive dependencies and integration points before promoting framework upgrades.
- Maintain migration checklists with rollback criteria and contract verification.

